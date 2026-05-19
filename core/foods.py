# Nährwerte pro 100g [kcal, carbs, protein, fat]
# Quellen: USDA FoodData Central + Standard-DE-Labels

FOODS = {
    # Protein
    "haehnchenbrust":       {"label": "Hähnchenbrust (roh)",        "n": [114, 0.0,  21.2, 2.6]},
    "rinderhack_5":         {"label": "Rinderhack 5% Fett (roh)",   "n": [137, 0.0,  21.4, 5.0]},
    "rindersteak":          {"label": "Rindersteak mager (roh)",    "n": [137, 0.0,  21.4, 5.0]},
    "thunfisch_dose":       {"label": "Thunfisch Dose (i.E.)",      "n": [116, 0.0,  25.5, 0.8]},
    "skyr":                 {"label": "Skyr 0,2%",                  "n": [63,  4.0,  11.0, 0.2]},
    "magerquark":           {"label": "Magerquark",                 "n": [67,  4.1,  12.0, 0.3]},
    "frischkaese_light":    {"label": "Frischkäse light <10%",      "n": [120, 4.0,  12.0, 6.0]},
    "eier":                 {"label": "Eier (ganz)",                "n": [143, 0.7,  12.6, 9.5]},
    "eiklar":               {"label": "Eiklar",                     "n": [52,  0.7,  10.9, 0.2]},
    "whey":                 {"label": "Whey Protein",               "n": [375, 5.0,  75.0, 5.0]},
    # Carbs
    "reis_basmati":         {"label": "Reis Basmati (roh)",         "n": [350, 77.0, 7.5,  0.6]},
    "reisnudeln":           {"label": "Reisnudeln (trocken)",       "n": [364, 80.0, 6.0,  0.6]},
    "kartoffel":            {"label": "Kartoffel (roh)",            "n": [77,  17.0, 2.0,  0.1]},
    "reispapier":           {"label": "Reispapier",                 "n": [330, 80.0, 2.5,  0.3]},
    "haferflocken":         {"label": "Haferflocken",               "n": [370, 58.7, 13.5, 6.9]},
    "banane":               {"label": "Banane",                     "n": [89,  22.8, 1.1,  0.3]},
    "heidelbeeren":         {"label": "Heidelbeeren",               "n": [57,  14.5, 0.7,  0.3]},
    # Fette
    "olivenoel":            {"label": "Olivenöl",                   "n": [884, 0.0,  0.0,  100.0]},
    "walnuesse":            {"label": "Walnüsse",                   "n": [654, 13.7, 15.2, 65.2]},
    "mandelmus":            {"label": "Mandelmus",                  "n": [614, 18.8, 21.0, 55.5]},
    "chiasamen":            {"label": "Chiasamen",                  "n": [486, 42.1, 16.5, 30.7]},
    "flohsamenschalen":     {"label": "Flohsamenschalen",           "n": [82,  3.0,  1.5,  0.5]},
    # Gemüse
    "brokkoli":             {"label": "Brokkoli",                   "n": [34,  6.6,  2.8,  0.4]},
    "paprika":              {"label": "Paprika rot",                "n": [31,  6.0,  1.0,  0.3]},
    "spinat":               {"label": "Spinat",                     "n": [23,  3.6,  2.9,  0.4]},
    "zucchini":             {"label": "Zucchini",                   "n": [17,  3.1,  1.2,  0.3]},
    "gurke":                {"label": "Gurke",                      "n": [15,  3.6,  0.7,  0.1]},
    "tomate":               {"label": "Tomate",                     "n": [18,  3.9,  0.9,  0.2]},
    "champignons":          {"label": "Champignons",                "n": [22,  3.3,  3.1,  0.3]},
    "weisskohl":            {"label": "Weißkohl",                   "n": [25,  5.8,  1.3,  0.1]},
    "karotten":             {"label": "Karotten",                   "n": [41,  9.6,  0.9,  0.2]},
    "eisbergsalat":         {"label": "Eisbergsalat",               "n": [14,  2.9,  0.9,  0.1]},
    "zwiebel":              {"label": "Zwiebel",                    "n": [40,  9.3,  1.1,  0.1]},
}

def get_macros(food_id: str, grams: float) -> dict:
    f = FOODS[food_id]["n"]
    factor = grams / 100
    return {
        "kcal":    round(f[0] * factor, 1),
        "carbs":   round(f[1] * factor, 1),
        "protein": round(f[2] * factor, 1),
        "fat":     round(f[3] * factor, 1),
    }

def sum_macros(items: list) -> dict:
    """items = [{"food_id": ..., "grams": ...}, ...]"""
    totals = {"kcal": 0, "carbs": 0, "protein": 0, "fat": 0}
    for item in items:
        m = get_macros(item["food_id"], item["grams"])
        for k in totals:
            totals[k] += m[k]
    return {k: round(v, 1) for k, v in totals.items()}
