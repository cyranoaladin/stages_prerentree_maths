#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gabarits de saisie V3 : un score, des codes d'erreur et une observation PAR CRITÈRE.

L'erreur majeure de la version précédente était d'attacher les codes d'erreur à
l'item : tous les codes d'un item retombaient alors sur toutes les compétences de
cet item, y compris sur celles que l'élève avait réussies. Ici, un code d'erreur
appartient au critère qui a effectivement échoué, et à lui seul.

Un critère déclaré « mixed » n'est pas saisi globalement : ce sont ses sous-critères
analytiques virtuels qui reçoivent un score, et le score du critère d'origine en est
la somme. Les points et les identifiants du sujet imprimé restent inchangés.
"""

import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd

OUTDIR = os.path.join(pd.V3_ROOT, "responses")
SCOPE = os.path.join(pd.V3_ROOT, "curriculum_scope", "criteria_scope.json")

INSTRUCTIONS = {
    "saisie": ("critère par critère. Jamais au niveau de l'item : c'est du critère que viennent "
               "le score par compétence et le classement N-1 / passerelle."),
    "criteria[].score": ("points attribués à ce critère, entre 0 et max_points. Le crédit partiel "
                         "est admis. Aucune valeur n'est complétée automatiquement."),
    "criteria[].error_codes": ("codes d'erreur du critère, et de lui seul. Ne jamais recopier ici "
                               "les codes d'un autre critère du même item."),
    "criteria[].observation": "note libre facultative, propre à ce critère.",
    "criteria[].accepted_alternative_method": ("true lorsque l'élève emploie une méthode "
                                               "mathématiquement correcte différente de celle du "
                                               "corrigé. Ce n'est jamais une erreur."),
    "criteria[].criterion_scoring_status": (
        "« scored » lorsque le critère est corrigé ; « requires_human_allocation » lorsque la "
        "ventilation n'a pas pu être établie ; « neutralised » lorsque aucune correction "
        "équitable n'est possible et que le critère est retiré des deux décomptes."),
    "criteria[].virtual_subcriteria": ("présent uniquement pour un critère mixte : ce sont ces "
                                       "lignes qui se saisissent, le critère d'origine en est la "
                                       "somme."),
    "responses[].teacher_observation_non_scored": (
        "remarques enseignantes hors barème. Elles n'entrent ni dans le score, ni dans le profil "
        "d'erreurs, ni dans les priorités, ni dans le bilan."),
    "confidence": "1 à 4, uniquement pour les items marqués confidence_probe ; null sinon.",
    "observed_duration_minutes": ("durée réellement observée, si une mesure pédagogiquement "
                                  "raisonnable a été possible. null sinon. Ne jamais interrompre "
                                  "un élève dans le seul but de calibrer le modèle."),
}


def build_for(student, criteria, manifest):
    by_item = {}
    for c in criteria:
        by_item.setdefault(c["item_ref"], []).append(c)
    overlay = pd.read_json(
        os.path.join(pd.V3_ROOT, "correction_overlays", student["student_id"],
                     "ANSWER_KEY_OVERLAY.json"), "overlay")
    ov_items = {i["ref"]: i for i in overlay["items"]}
    responses = []
    for it in manifest["items"]:
        rows = []
        for c in sorted(by_item[it["ref"]], key=lambda x: x["criterion_rank"]):
            row = {
                "criterion_id": c["criterion_id"],
                "analysis_skill_id": c["analysis_skill_id"],
                "original_skill_id": c["original_skill_id"],
                "curriculum_scope": c["curriculum_scope"],
                "evidence_type": c["evidence_type"],
                "subpart": c["subpart"],
                "desc": c["desc"],
                "max_points": c["original_points"],
                "score": None,
                "error_codes": [],
                "observation": None,
                "accepted_alternative_method": False,
                "criterion_scoring_status": "pending",
            }
            if c["curriculum_scope"] == "mixed":
                row["score"] = None
                row["score_is_sum_of_virtual"] = True
                row["virtual_subcriteria"] = [{
                    "virtual_criterion_id": v["virtual_criterion_id"],
                    "analysis_skill_id": v["analysis_skill_id"],
                    "curriculum_scope": v["curriculum_scope"],
                    "desc": v["desc"],
                    "max_points": v["points"],
                    "score": None,
                    "error_codes": [],
                    "observation": None,
                    "accepted_alternative_method": False,
                    "criterion_scoring_status": "pending",
                } for v in c["virtual_subcriteria"]]
            rows.append(row)
        responses.append({
            "item_id": it["item_id"],
            "ref": it["ref"],
            "part": it["part"],
            "kind": it["kind"],
            "max_points": it["points"],
            "estimated_duration_minutes": it["time_estimate"]["minutes"],
            "observed_duration_minutes": None,
            "confidence": None,
            "confidence_probe": bool(it.get("confidence_probe")),
            "criteria": rows,
            "teacher_observation_non_scored":
                [o["observation"] for o in ov_items[it["ref"]]["teacher_observation_non_scored"]],
        })
    est = round(sum(i["time_estimate"]["minutes"] for i in manifest["items"]), 2)
    return {
        "schema": "nexus-s5-responses-v3",
        "generated_on": pd.GENERATED_ON,
        "student_id": student["student_id"],
        "student_name": student["student_name"],
        "level_key": student["level_key"],
        "subject": student["subject"],
        "status": "awaiting_assessment",
        "assessed_on": None,
        "estimated_duration_minutes": est,
        "observed_duration_minutes": None,
        "source_of_truth": ("les documents élèves distribués ne sont pas modifiables ; ce fichier "
                            "ne contient que la correction."),
        "instructions": INSTRUCTIONS,
        "responses": responses,
        "session_observations": {
            "conditions_de_passation": None,
            "interruptions": None,
            "aides_apportees": None,
        },
    }


def main():
    scope = pd.read_json(SCOPE, "carte curriculaire")
    by_student = {}
    for c in scope["criteria"]:
        by_student.setdefault(c["student_id"], []).append(c)
    n = 0
    for st in pd.students():
        obj = build_for(st, by_student[st["student_id"]], pd.manifest_of(st))
        pd.write_json(os.path.join(OUTDIR, "responses_v3_TEMPLATE_%s.json" % st["student_id"]), obj)
        n += 1
    pd.write_text(os.path.join(OUTDIR, "README.md"), """# Saisie des corrections — V3

Un gabarit par élève : `responses_v3_TEMPLATE_<student_id>.json`.

Pour corriger, copier le gabarit sous un nom daté, puis le renseigner :

```
cp responses/responses_v3_TEMPLATE_elyes-kefi.json \\
   responses/responses_elyes-kefi_2026-08-28.json
```

Trois règles, et elles ne souffrent pas d'exception.

1. La saisie se fait **critère par critère**. Le script refuse un fichier incomplet
   plutôt que de compléter une valeur manquante.
2. Un **code d'erreur appartient au critère qui a échoué**, et à aucun autre. Il ne
   se propage ni aux autres critères de l'item, ni aux autres compétences.
3. Une **méthode mathématiquement correcte n'est jamais une erreur**. Cocher
   `accepted_alternative_method` et écrire l'observation.

Puis :

```
python3 tools/analyze_s5_post_distribution.py \\
    --student elyes-kefi \\
    --responses responses/responses_elyes-kefi_2026-08-28.json
```
""")
    print("gabarits V3 écrits : %d" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
