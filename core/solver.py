import numpy as np
from scipy.optimize import minimize
from .foods import FOODS, sum_macros

# Alle Tages-Templates: Trainingstag + Ruhetag
# Jedes Template definiert Mahlzeiten-Struktur + Lebensmittel + Bounds

TRAINING_TEMPLATES = [
    {
        "id": "training_a",
        "name": "Hähnchen + Ofenkartoffeln",
        "carb_source": "Kartoffel",
        "meals": [
            {"name": "Frühstück", "timing": "low_carb",  "foods": ["eier","eiklar","spinat","paprika","frischkaese_light","olivenoel"],        "bounds": [(60,150),(80,200),(80,150),(60,120),(30,70),(3,12)]},
            {"name": "Mittag",    "timing": "low_carb",  "foods": ["thunfisch_dose","gurke","tomate","eisbergsalat","olivenoel"],               "bounds": [(130,220),(100,200),(60,120),(60,120),(4,10)]},
            {"name": "Pre-WO",   "timing": "carbs",     "foods": ["banane","skyr","whey"],                                                     "bounds": [(80,130),(120,220),(8,22)]},
            {"name": "Post-WO",  "timing": "carbs",     "foods": ["haehnchenbrust","kartoffel","brokkoli","olivenoel"],                        "bounds": [(160,240),(150,250),(120,200),(3,10)]},
        ]
    },
    {
        "id": "training_b",
        "name": "Rindersteak + Reisnudeln",
        "carb_source": "Reisnudeln",
        "meals": [
            {"name": "Frühstück", "timing": "low_carb",  "foods": ["eier","eiklar","champignons","zucchini","olivenoel"],                      "bounds": [(60,150),(80,180),(100,180),(80,150),(3,10)]},
            {"name": "Mittag",    "timing": "low_carb",  "foods": ["haehnchenbrust","eisbergsalat","gurke","tomate","frischkaese_light"],       "bounds": [(100,180),(80,150),(100,180),(60,120),(30,70)]},
            {"name": "Pre-WO",   "timing": "carbs",     "foods": ["banane","magerquark","whey"],                                              "bounds": [(70,120),(100,200),(8,22)]},
            {"name": "Post-WO",  "timing": "carbs",     "foods": ["rindersteak","reisnudeln","brokkoli","olivenoel"],                         "bounds": [(160,240),(40,65),(120,200),(3,10)]},
        ]
    },
    {
        "id": "training_c",
        "name": "Lahmacun Reispapier + Basmati",
        "carb_source": "Reispapier + Reis",
        "meals": [
            {"name": "Frühstück", "timing": "low_carb",  "foods": ["eier","eiklar","spinat","paprika","frischkaese_light","olivenoel"],        "bounds": [(60,130),(80,180),(80,150),(60,100),(25,60),(3,10)]},
            {"name": "Mittag",    "timing": "low_carb",  "foods": ["thunfisch_dose","gurke","tomate","frischkaese_light","eisbergsalat"],      "bounds": [(120,200),(100,180),(60,100),(20,50),(60,100)]},
            {"name": "Pre-WO",   "timing": "carbs",     "foods": ["skyr","haferflocken","whey"],                                             "bounds": [(120,220),(20,35),(5,18)]},
            {"name": "Post-WO",  "timing": "carbs",     "foods": ["rinderhack_5","reispapier","reis_basmati","tomate","paprika","zwiebel","olivenoel"], "bounds": [(150,220),(25,35),(25,40),(50,80),(50,80),(30,60),(3,8)]},
        ]
    },
    {
        "id": "training_d",
        "name": "Hähnchen + Reisnudeln Asia",
        "carb_source": "Reisnudeln",
        "meals": [
            {"name": "Frühstück", "timing": "low_carb",  "foods": ["eier","eiklar","zucchini","frischkaese_light","olivenoel"],               "bounds": [(60,140),(80,180),(80,150),(25,60),(3,10)]},
            {"name": "Mittag",    "timing": "low_carb",  "foods": ["haehnchenbrust","champignons","spinat","olivenoel"],                      "bounds": [(100,180),(100,180),(80,150),(4,10)]},
            {"name": "Pre-WO",   "timing": "carbs",     "foods": ["skyr","banane","walnuesse"],                                              "bounds": [(120,220),(70,120),(5,12)]},
            {"name": "Post-WO",  "timing": "carbs",     "foods": ["haehnchenbrust","reisnudeln","brokkoli","olivenoel"],                     "bounds": [(140,220),(40,65),(150,220),(3,10)]},
        ]
    },
]

REST_TEMPLATES = [
    {
        "id": "rest_a",
        "name": "Reisnudeln Mittag",
        "carb_source": "Reisnudeln",
        "meals": [
            {"name": "Frühstück", "timing": "carbs",     "foods": ["skyr","haferflocken","whey","walnuesse","mandelmus","chiasamen"],         "bounds": [(150,300),(20,35),(10,28),(5,12),(5,12),(4,8)]},
            {"name": "Mittag",    "timing": "carbs",     "foods": ["haehnchenbrust","reisnudeln","zucchini","tomate","olivenoel"],            "bounds": [(150,230),(40,65),(80,150),(60,100),(3,8)]},
            {"name": "Snack",     "timing": "low_carb",  "foods": ["frischkaese_light","paprika","gurke","karotten"],                        "bounds": [(50,100),(80,150),(100,180),(60,100)]},
            {"name": "Abend",     "timing": "no_carb",   "foods": ["rinderhack_5","weisskohl","zucchini","olivenoel"],                       "bounds": [(170,260),(120,200),(80,150),(3,10)]},
        ]
    },
    {
        "id": "rest_b",
        "name": "Ofenkartoffeln Mittag",
        "carb_source": "Kartoffel",
        "meals": [
            {"name": "Frühstück", "timing": "carbs",     "foods": ["eier","eiklar","haferflocken","frischkaese_light","paprika","olivenoel"], "bounds": [(60,140),(100,220),(20,35),(30,70),(60,120),(3,10)]},
            {"name": "Mittag",    "timing": "carbs",     "foods": ["haehnchenbrust","kartoffel","brokkoli","olivenoel"],                     "bounds": [(150,230),(150,250),(150,220),(3,10)]},
            {"name": "Snack",     "timing": "low_carb",  "foods": ["reispapier","frischkaese_light","spinat","gurke","paprika"],             "bounds": [(15,25),(50,100),(60,100),(80,150),(60,100)]},
            {"name": "Abend",     "timing": "no_carb",   "foods": ["haehnchenbrust","champignons","spinat","olivenoel"],                    "bounds": [(150,230),(120,180),(100,180),(3,10)]},
        ]
    },
    {
        "id": "rest_c",
        "name": "Rindersteak + Ofenkartoffel",
        "carb_source": "Kartoffel",
        "meals": [
            {"name": "Frühstück", "timing": "carbs",     "foods": ["skyr","haferflocken","whey","chiasamen","heidelbeeren","walnuesse"],     "bounds": [(150,280),(20,35),(8,22),(4,8),(40,80),(5,15)]},
            {"name": "Mittag",    "timing": "carbs",     "foods": ["rindersteak","kartoffel","brokkoli","olivenoel"],                       "bounds": [(160,240),(150,250),(120,200),(5,15)]},
            {"name": "Snack",     "timing": "low_carb",  "foods": ["frischkaese_light","paprika","gurke","karotten","tomate"],              "bounds": [(50,100),(80,150),(80,150),(50,80),(60,100)]},
            {"name": "Abend",     "timing": "no_carb",   "foods": ["thunfisch_dose","eisbergsalat","tomate","gurke","olivenoel"],           "bounds": [(130,220),(100,180),(60,100),(80,150),(5,15)]},
        ]
    },
]


def _solve_day(template: dict, target: dict, seed: int = 42) -> dict:
    """
    Löst Optimierungsproblem für einen Tagestyp.
    Gibt Template zurück mit exakten Gramm-Mengen.
    """
    all_foods = []
    all_bounds = []
    meal_splits = []

    for meal in template["meals"]:
        all_foods.extend(meal["foods"])
        all_bounds.extend(meal["bounds"])
        meal_splits.append(len(meal["foods"]))

    n = len(all_foods)
    M = np.array([[FOODS[f]["n"][i] for f in all_foods] for i in range(1, 4)]) / 100  # (3, n) — carbs/protein/fat
    T = np.array([target["carbs"], target["protein"], target["fat"]])

    def obj(x):
        total = M @ x
        rel = (total - T) / T
        return np.sum(rel**2 * np.array([4, 4, 1])) * 10000

    rng = np.random.RandomState(seed)
    best = None
    for _ in range(60):
        x0 = np.array([rng.uniform(a, b) for a, b in all_bounds])
        r = minimize(obj, x0, bounds=all_bounds, method='SLSQP',
                     options={'maxiter': 2000, 'ftol': 1e-12})
        if best is None or r.fun < best.fun:
            best = r

    x = best.x
    total_macros = M @ x
    kcal_vec = np.array([FOODS[f]["n"][0] for f in all_foods]) / 100
    total_kcal = kcal_vec @ x

    # Deviation check
    dev = {
        "carbs":   round((total_macros[0] - T[0]) / T[0] * 100, 2),
        "protein": round((total_macros[1] - T[1]) / T[1] * 100, 2),
        "fat":     round((total_macros[2] - T[2]) / T[2] * 100, 2),
    }
    within_tolerance = all(abs(v) <= 2.0 for v in dev.values())

    # Build result meals
    result_meals = []
    pos = 0
    for meal, n_items in zip(template["meals"], meal_splits):
        items = []
        for i, food_id in enumerate(meal["foods"]):
            grams = round(x[pos + i])
            if grams > 0:
                items.append({
                    "food_id": food_id,
                    "label": FOODS[food_id]["label"],
                    "grams": grams,
                    "macros": get_macros_inline(food_id, grams),
                })
        result_meals.append({
            "name": meal["name"],
            "timing": meal["timing"],
            "items": items,
            "macros": sum_macros([{"food_id": it["food_id"], "grams": it["grams"]} for it in items]),
        })
        pos += n_items

    return {
        "template_id": template["id"],
        "name": template["name"],
        "carb_source": template["carb_source"],
        "meals": result_meals,
        "day_macros": {
            "kcal":    round(total_kcal),
            "carbs":   round(total_macros[0], 1),
            "protein": round(total_macros[1], 1),
            "fat":     round(total_macros[2], 1),
        },
        "deviation": dev,
        "within_tolerance": within_tolerance,
    }


def get_macros_inline(food_id: str, grams: float) -> dict:
    f = FOODS[food_id]["n"]
    factor = grams / 100
    return {
        "kcal":    round(f[0] * factor, 1),
        "carbs":   round(f[1] * factor, 1),
        "protein": round(f[2] * factor, 1),
        "fat":     round(f[3] * factor, 1),
    }


def generate_week(
    target: dict,
    training_days: list,  # z.B. ["monday", "tuesday", "thursday", "friday"]
) -> dict:
    """
    Generiert einen kompletten 7-Tage-Plan.
    target = {"carbs": 98, "protein": 176, "fat": 52}
    """
    week_order = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    day_labels = {
        "monday": "Montag", "tuesday": "Dienstag", "wednesday": "Mittwoch",
        "thursday": "Donnerstag", "friday": "Freitag",
        "saturday": "Samstag", "sunday": "Sonntag"
    }

    training_set = set(training_days)
    training_count = 0
    rest_count = 0
    result = []

    for day in week_order:
        is_training = day in training_set

        if is_training:
            template = TRAINING_TEMPLATES[training_count % len(TRAINING_TEMPLATES)]
            training_count += 1
        else:
            template = REST_TEMPLATES[rest_count % len(REST_TEMPLATES)]
            rest_count += 1

        day_result = _solve_day(template, target, seed=42 + len(result))
        day_result["day"] = day
        day_result["day_label"] = day_labels[day]
        day_result["is_training"] = is_training
        result.append(day_result)

    return {
        "target": target,
        "training_days": training_days,
        "days": result,
        "all_within_tolerance": all(d["within_tolerance"] for d in result),
    }


def generate_shopping_list(week_plan: dict) -> list:
    """Aggregiert alle Zutaten der Woche zu einer Einkaufsliste."""
    totals = {}
    for day in week_plan["days"]:
        for meal in day["meals"]:
            for item in meal["items"]:
                fid = item["food_id"]
                if fid not in totals:
                    totals[fid] = {"food_id": fid, "label": item["label"], "total_grams": 0}
                totals[fid]["total_grams"] += item["grams"]

    # Runden auf sinnvolle Kaufmengen (50g-Schritte für Fleisch/Gemüse)
    shopping = []
    for fid, data in sorted(totals.items(), key=lambda x: x[1]["label"]):
        g = data["total_grams"]
        # Kaufmenge: nächste 50g aufgerundet für Fleisch/Gemüse, exakt für Trockenwaren
        dry_foods = {"reis_basmati","reisnudeln","reispapier","haferflocken","chiasamen",
                     "flohsamenschalen","whey","walnuesse","mandelmus","olivenoel"}
        if fid in dry_foods:
            buy_grams = g  # exakt
        else:
            buy_grams = int(np.ceil(g / 50) * 50)  # auf 50g aufrunden

        shopping.append({
            "food_id": fid,
            "label": data["label"],
            "total_grams": g,
            "buy_grams": buy_grams,
            "buy_display": f"{buy_grams} g" if buy_grams < 1000 else f"{buy_grams/1000:.1f} kg",
        })

    return shopping
