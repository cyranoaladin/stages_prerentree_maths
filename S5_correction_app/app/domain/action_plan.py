# -*- coding: utf-8 -*-
"""Plan des quatre premières semaines, déduit des priorités et jamais inventé.

Deux familles, qui ne se mélangent pas :

* la **consolidation N−1** peut produire P1, P2, P3 ou OK ;
* les **passerelles vers N** ne produisent que `BRIDGE_REVISIT` ou
  `DISCOVERY_TO_CONTINUE`. Une notion découverte le jour même ne devient pas un déficit
  scolaire parce qu'elle n'est pas encore installée.

Deux à trois objectifs par semaine, pas davantage : un plan que personne ne tient ne
sert à rien.
"""

from . import points

WEEK_SHAPES = [
    (1, 2, "reprise guidée puis exercices gradués", 15, "3 séances de 15 minutes",
     "priorités immédiates des acquis de l'année précédente"),
    (2, 2, "réactivation espacée, avec contrôle écrit", 15, "3 séances de 15 minutes",
     "poursuite des priorités et contrôle différé de rétention"),
    (3, 2, "problème mixte et transfert", 20, "2 séances de 20 minutes",
     "stabilisation et transfert"),
    (4, 3, "bilan cumulatif court", 20, "2 séances de 20 minutes",
     "bilan cumulatif des quatre semaines"),
]


def build(analysis: dict, delayed_checks: list) -> dict:
    pool = [s for s in analysis["priorities"] if s["priority_rank"] in ("P1", "P2", "P3")]
    cursor, weeks = 0, []
    for number, size, work_type, duration, frequency, focus in WEEK_SHAPES:
        take = pool[cursor:cursor + size]
        cursor += len(take)
        objectives = [{
            "analysis_skill_id": s["analysis_skill_id"],
            "label": s["label"],
            "priority_rank": s["priority_rank"],
            "objective": "porter « %s » au statut Satisfaisant, contrôle écrit à l'appui"
                         % s["label"],
            "success_criterion": "trois réussites consécutives sans aide, chacune assortie "
                                 "du contrôle demandé",
            "dominant_error_codes": sorted(set(s["error_codes"]))[:2],
        } for s in take]
        week = {"week": number, "focus": focus, "work_type": work_type,
                "duration_minutes": duration, "frequency": frequency,
                "objectives": objectives, "delayed_check": None}
        if number == 2 and delayed_checks:
            week["delayed_check"] = {
                "titre": "Mini-test différé",
                "duree_minutes": 10,
                "format": "deux items par compétence, parallèles à ceux de l'évaluation de "
                          "clôture, sans aide ni carte de rappel",
                "critere": "réussite maintenue sur au moins un item par compétence",
                "skills": [{"skill_id": d.skill_id, "label": d.label} for d in delayed_checks],
            }
        weeks.append(week)

    bridge = [{
        "analysis_skill_id": s["analysis_skill_id"], "label": s["label"],
        "action": s["bridge_action"],
        "action_label": ("Découverte à poursuivre" if s["bridge_action"] ==
                         "DISCOVERY_TO_CONTINUE" else "À reprendre à la rentrée"),
        "quand": "à la reprise du chapitre correspondant, en classe",
        "regle": "cette ligne n'est pas une remédiation : la notion n'a pas encore été "
                 "enseignée en classe.",
    } for s in analysis["bridge_actions"]]

    return {
        "schema": "nexus-s5-four-week-plan-v1",
        "student_id": analysis["student_id"],
        "progression_chiffree_possible": False,
        "progression_chiffree_raison": analysis["delta_blocked_reason"],
        "weeks": weeks,
        "bridge_actions": bridge,
        "follow_up": follow_up(analysis),
    }


def follow_up(analysis: dict) -> dict:
    p1 = [s for s in analysis["priorities"] if s["priority_rank"] == "P1"]
    n1 = analysis["n_minus_1_consolidation"]
    rate = (n1["percentage"] or 0) / 100.0
    if len(p1) >= 3 or rate < 0.5:
        proposed = "accompagnement régulier recommandé"
    elif p1:
        proposed = "points de contrôle ciblés recommandés"
    else:
        proposed = "aucun accompagnement supplémentaire justifié par les données"
    return {
        "proposed": proposed,
        "justification": "%d compétence(s) classée(s) P1 ; consolidation des acquis de "
                         "l'année précédente à %s %%."
                         % (len(p1), ("%.0f" % (100 * rate)).replace(".", ",")),
        "data_basis": ["n_minus_1_consolidation.percentage", "priorities[].priority_rank"],
    }
