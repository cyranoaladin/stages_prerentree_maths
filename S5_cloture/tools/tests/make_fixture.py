#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit un jeu de données SYNTHETIQUE pour tester analyze_s5.py.

Aucune donnée réelle d'élève n'est utilisée. L'élève fictif s'appelle
« ELEVE SYNTHETIQUE » et son identifiant est « eleve-synthetique-test ».
Le marqueur SYNTHETIQUE figure dans chaque fichier produit ; validate_s5.py
vérifie qu'il n'apparaît nulle part ailleurs que sous tools/tests/.
"""

import json
import os
import sys
sys.dont_write_bytecode = True  # aucune trace de cache dans la livraison

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import core                     # noqa: E402
import generate_s5              # noqa: E402
from data import common         # noqa: E402

FIXTURE_DIR = os.path.join(HERE, "fixture_synthetique")


def synthetic_student():
    """Élève fictif de niveau 4e : noyau commun réel, items individualisés fictifs."""
    def indiv(ref, skill, points, minutes, difficulty, task, baseline, comparability):
        return {
            "skill": skill, "points": points, "minutes": minutes, "task": task,
            "difficulty": difficulty, "space": "lines:2",
            "tex": r"[SYNTHETIQUE] Item fictif %s pour le jeu de tests." % ref,
            "answer": r"[SYNTHETIQUE] réponse fictive %s" % ref,
            "steps": ["étape fictive 1", "étape fictive 2"],
            "errors": [{"code": "CALCUL", "desc": "erreur fictive de calcul"}],
            "criteria": [{"points": points, "desc": "critère fictif complet"}],
            "baseline_item": baseline, "comparability": comparability,
            "role_rentree": "item SYNTHETIQUE, sans valeur pédagogique",
        }

    return {
        "id": "eleve-synthetique-test", "name": "ELEVE SYNTHETIQUE",
        "dir": "ELEVE_SYNTHETIQUE", "level": "4e",
        "parcours": "jeu de données SYNTHETIQUE",
        "baseline": {
            "available": True, "date": None, "items": "SYNTHETIQUE",
            "calibration": "50 %", "summary": "profil SYNTHETIQUE de test",
            "appuis": ["appui fictif"], "priorites": ["priorité fictive"],
            "observations": [],
        },
        "domain_status": {"Nombres relatifs": "a_rectifier", "Fractions": "a_rectifier",
                          "Proportionnalité": "solide", "Calcul littéral": "a_installer",
                          "Géométrie": "solide", "Grandeurs et mesures": "solide",
                          "Statistiques": "a_diagnostiquer"},
        "skill_overrides": {},
        "p1": "M4E_REL_02", "p2": "M4E_FRAC_02",
        "objectif": "objectif SYNTHETIQUE de test",
        "watch": ["observation SYNTHETIQUE"],
        "extra_sources": [],
        "eval_individual": {
            "A5": indiv("A5", "M4E_REL_02", 1, 1.5, "socle", "automatisme", "4E_TI_Q17", "comparable"),
            "A6": indiv("A6", "M4E_FRAC_02", 1, 1.5, "socle", "automatisme", "4E_TI_Q04", "comparable"),
            "B4": indiv("B4", "M4E_GEO_02", 2, 4, "standard", "application", "4E_TI_Q14", "comparable"),
            "C2": indiv("C2", "M4E_STAT_01", 2, 4, "transfert", "transfert", None,
                        "non_comparable_absence_baseline"),
        },
    }


def build():
    st = synthetic_student()
    tdir = os.path.join(FIXTURE_DIR, "_ENSEIGNANT")
    os.makedirs(tdir, exist_ok=True)
    generate_s5.write_json(os.path.join(FIXTURE_DIR, "student_learning_profile.json"),
                           generate_s5.build_profile(st))
    generate_s5.write_json(os.path.join(FIXTURE_DIR, "evaluation_blueprint.json"),
                           generate_s5.build_blueprint(st))
    generate_s5.write_json(os.path.join(FIXTURE_DIR, "post_stage_analysis_schema.json"),
                           generate_s5.build_post_schema(st))
    generate_s5.write_json(os.path.join(FIXTURE_DIR, "four_week_action_plan_TEMPLATE.json"),
                           generate_s5.build_action_plan_template(st))
    generate_s5.write_json(os.path.join(tdir, "evaluation_manifest.json"),
                           generate_s5.build_manifest(st))
    generate_s5.write_json(os.path.join(tdir, "answer_key.json"),
                           generate_s5.build_answer_key(st))

    items = core.exam_items(st)
    # Copie vierge, puis copie renseignée avec des scores connus à l'avance.
    template = generate_s5.build_responses_template(st)
    generate_s5.write_json(os.path.join(FIXTURE_DIR, "responses_TEMPLATE.json"), template)

    # Scores visés au niveau de l'item ; ils sont ensuite répartis sur les critères
    # dans l'ordre, en remplissant chaque critère avant de passer au suivant.
    scores = {"A1": 1, "A2": 1, "A3": 1, "A4": 0, "A5": 1, "A6": 0,
              "B1": 2, "B2": 0, "B3": 2, "B4": 1, "C1": 3, "C2": 0}
    errs = {"A4": ["METHODE"], "A6": ["CONCEPT"], "B2": ["CONCEPT"], "B4": ["JUSTIFICATION"],
            "C1": ["CALCUL"], "C2": ["CONCEPT", "LECTURE"]}
    conf = {"B2": 4, "C1": 2}
    filled = json.loads(json.dumps(template))
    filled["status"] = "assessed"
    filled["assessed_on"] = "2026-08-28"
    filled["note"] = "JEU DE DONNEES SYNTHETIQUE — ne correspond à aucun élève réel."
    for row in filled["responses"]:
        reste = float(scores[row["ref"]])
        for c in row["criteria"]:
            pris = min(reste, float(c["max_points"]))
            c["score"] = round(pris, 4)
            reste = round(reste - pris, 4)
        assert reste == 0, (row["ref"], reste)
        row["error_codes"] = errs.get(row["ref"], [])
        row["confidence"] = conf.get(row["ref"])
    generate_s5.write_json(os.path.join(FIXTURE_DIR, "responses_SYNTHETIQUE.json"), filled)
    return st, items, scores


if __name__ == "__main__":
    st, items, scores = build()
    print("fixture SYNTHETIQUE écrite dans %s" % FIXTURE_DIR)
    print("total attendu : %s / %s" % (sum(scores.values()), sum(i["points"] for i in items)))
