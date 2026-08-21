# -*- coding: utf-8 -*-
"""Force de preuve : combien la copie permet réellement d'affirmer.

Ce n'est pas une fiabilité statistique, et le mot est proscrit : aucune étude de
fiabilité n'a été conduite, et douze items n'en permettraient pas. C'est un décompte
explicite de ce qui étaye une conclusion, avec une règle publiée et rejouable.

Barème, appliqué tel quel :

| condition                                                | poids |
| -------------------------------------------------------- | ----: |
| au moins deux critères indépendants                        |    +1 |
| au moins deux items distincts                              |    +1 |
| au moins deux points en jeu                                |    +1 |
| au moins deux types de preuve différents                   |    +1 |
| une tâche de transfert réussie                             |    +1 |
| énoncé sans limite d'interprétation connue                 |    +1 |
| comparable au diagnostic initial                           |    +1 |
| compétence mesurée moins d'une heure après sa remédiation  |    −1 |

Seuils : ≤ 0 INSUFFICIENT, 1–2 LOW, 3–4 MODERATE, ≥ 5 STRONG.
"""

RUBRIC = [
    ("au moins deux critères indépendants", lambda a: a["evidence_count"] >= 2, +1),
    ("au moins deux items distincts", lambda a: a["independent_items"] >= 2, +1),
    ("au moins deux points en jeu", lambda a: a["points_available_centi"] >= 200, +1),
    ("au moins deux types de preuve différents", lambda a: a["task_diversity"] >= 2, +1),
    ("une tâche de transfert réussie", lambda a: a["has_transfer"], +1),
    ("énoncé sans limite d'interprétation connue", lambda a: not a["limited_by_prompt"], +1),
    ("comparable au diagnostic initial", lambda a: a["comparable_to_baseline"], +1),
    ("mesurée moins d'une heure après sa remédiation", lambda a: a["immediate"], -1),
]

LEVELS = ("INSUFFICIENT", "LOW", "MODERATE", "STRONG")

LABELS = {
    "INSUFFICIENT": "preuve insuffisante",
    "LOW": "preuve faible",
    "MODERATE": "preuve moyenne",
    "STRONG": "preuve forte",
}

ORDER = {name: i for i, name in enumerate(LEVELS)}


def level_from_score(score: int) -> str:
    if score <= 0:
        return "INSUFFICIENT"
    if score <= 2:
        return "LOW"
    if score <= 4:
        return "MODERATE"
    return "STRONG"


def compute(inputs: dict) -> dict:
    """Retourne le niveau, le score et le détail ligne à ligne. Rien n'est implicite."""
    score, detail = 0, []
    for label, test, weight in RUBRIC:
        ok = bool(test(inputs))
        if ok:
            score += weight
        detail.append({"critere": label, "verifie": ok, "poids": weight})
    level = level_from_score(score)
    return {"level": level, "label": LABELS[level], "score": score, "detail": detail,
            "inputs": dict(inputs)}


def at_least(level: str, minimum: str) -> bool:
    return ORDER[level] >= ORDER[minimum]
