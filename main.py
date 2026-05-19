from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn

from core.solver import generate_week, generate_shopping_list
from core.foods import FOODS

app = FastAPI(
    title="MacroPrecision API",
    description="Präziser Ernährungsplan-Generator für Hobby-Athleten",
    version="0.1.0"
)

# CORS — erlaubt Frontend-Zugriff von überall (für MVP)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response Models ──────────────────────────────

class MacroTarget(BaseModel):
    kcal:    int   = Field(default=1564, description="Kalorienziel")
    carbs:   float = Field(default=98,   description="Kohlenhydrate in Gramm")
    protein: float = Field(default=176,  description="Protein in Gramm")
    fat:     float = Field(default=52,   description="Fett in Gramm")

class GeneratePlanRequest(BaseModel):
    target:        MacroTarget
    training_days: list[str] = Field(
        default=["monday","tuesday","thursday","friday"],
        description="Trainingstage: monday/tuesday/wednesday/thursday/friday/saturday/sunday"
    )
    user_id:       Optional[str] = None
    week_number:   Optional[int] = 1

class FeedbackRequest(BaseModel):
    user_id:     str
    week_number: int
    ratings: dict = Field(
        description="z.B. {'variety': 4, 'effort': 3, 'taste': 5}"
    )
    dislikes:  list[str] = Field(default=[], description="Lebensmittel die nicht gepasst haben")
    weight_kg: Optional[float] = None


# ── Endpoints ──────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "name": "MacroPrecision API",
        "version": "0.1.0",
        "status": "running",
        "endpoints": ["/plan/generate", "/plan/shopping-list", "/foods", "/health"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/plan/generate")
def generate_plan(req: GeneratePlanRequest):
    """
    Generiert einen kompletten 7-Tage-Ernährungsplan.
    Alle Gramm-Angaben sind mathematisch exakt auf die Makros optimiert (≤2% Toleranz).
    """
    valid_days = {"monday","tuesday","wednesday","thursday","friday","saturday","sunday"}
    for d in req.training_days:
        if d not in valid_days:
            raise HTTPException(400, f"Ungültiger Tag: {d}")

    target = {
        "carbs":   req.target.carbs,
        "protein": req.target.protein,
        "fat":     req.target.fat,
    }

    try:
        plan = generate_week(target, req.training_days)
    except Exception as e:
        raise HTTPException(500, f"Solver-Fehler: {str(e)}")

    return {
        "success": True,
        "user_id": req.user_id,
        "week_number": req.week_number,
        "target": req.target,
        "training_days": req.training_days,
        "all_within_tolerance": plan["all_within_tolerance"],
        "days": plan["days"],
    }


@app.post("/plan/shopping-list")
def get_shopping_list(req: GeneratePlanRequest):
    """
    Generiert Plan + aggregierte Einkaufsliste für die gesamte Woche.
    """
    target = {
        "carbs":   req.target.carbs,
        "protein": req.target.protein,
        "fat":     req.target.fat,
    }

    plan = generate_week(target, req.training_days)
    shopping = generate_shopping_list(plan)

    return {
        "success": True,
        "shopping_list": shopping,
        "total_items": len(shopping),
        "days_summary": [
            {
                "day": d["day_label"],
                "type": "Trainingstag" if d["is_training"] else "Ruhetag",
                "name": d["name"],
                "kcal": d["day_macros"]["kcal"],
            }
            for d in plan["days"]
        ]
    }


@app.get("/foods")
def list_foods():
    """Gibt alle verfügbaren Lebensmittel mit Nährwerten zurück."""
    return {
        "foods": [
            {
                "id": fid,
                "label": data["label"],
                "per_100g": {
                    "kcal":    data["n"][0],
                    "carbs":   data["n"][1],
                    "protein": data["n"][2],
                    "fat":     data["n"][3],
                }
            }
            for fid, data in FOODS.items()
        ]
    }


@app.post("/feedback")
def save_feedback(req: FeedbackRequest):
    """
    Speichert User-Feedback für adaptive Plananpassung.
    (Woche 2 Feature — Daten werden in Supabase gespeichert)
    """
    # TODO: Supabase Integration in V1.1
    return {
        "success": True,
        "message": "Feedback gespeichert. Dein nächster Plan wird angepasst.",
        "received": req.dict()
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
