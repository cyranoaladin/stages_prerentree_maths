#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Overlays de correction : ce qui se superpose au corrigé, sans le réécrire.

Le corrigé d'origine reste en place dans S5_cloture/…/_ENSEIGNANT/answer_key.json :
il est la preuve de ce qui existait au moment de la distribution. L'overlay ne
change ni les questions, ni les points, ni les identifiants. Il précise seulement
le barème équitable, les méthodes acceptées, ce que chaque critère mesure
réellement, ses limites d'interprétation et son classement curriculaire.

    correction_overlays/<student_id>/CORRECTION_POLICY.json
    correction_overlays/<student_id>/ANSWER_KEY_OVERLAY.json
    correction_overlays/<student_id>/TEACHER_NOTES.md
"""

import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd
import equity_rules

OUTDIR = os.path.join(pd.V3_ROOT, "correction_overlays")
SCOPE = os.path.join(pd.V3_ROOT, "curriculum_scope", "criteria_scope.json")


def policy(student, criteria):
    n1 = round(sum(c["original_points"] for c in criteria
                   if c["curriculum_scope"] == "n_minus_1")
               + sum(v["points"] for c in criteria if c["curriculum_scope"] == "mixed"
                     for v in c["virtual_subcriteria"] if v["curriculum_scope"] == "n_minus_1"), 3)
    br = round(sum(c["original_points"] for c in criteria
                   if c["curriculum_scope"] == "bridge_n")
               + sum(v["points"] for c in criteria if c["curriculum_scope"] == "mixed"
                     for v in c["virtual_subcriteria"] if v["curriculum_scope"] == "bridge_n"), 3)
    return {
        "schema": "nexus-s5-correction-policy-v3",
        "generated_on": pd.GENERATED_ON,
        "student_id": student["student_id"],
        "student_name": student["student_name"],
        "level_key": student["level_key"],
        "level_label": student["level_label"],
        "subject": student["subject"],
        "document_status": "distribué ; figé ; non modifiable",
        "scope": ("cet overlay porte sur la correction et sur l'interprétation. Il ne modifie ni "
                  "l'énoncé, ni les valeurs numériques, ni les points, ni les identifiants."),
        "regles_generales": equity_rules.GENERAL_RULES,
        "regle_ambiguite": [
            "retenir l'interprétation la plus favorable compatible avec la consigne imprimée",
            "accepter toute méthode mathématiquement correcte",
            "n'exiger aucune justification que la consigne ne demande pas explicitement",
            "neutraliser le sous-critère si aucune correction équitable n'est possible",
            "marquer alors evidence_quality = limited_by_prompt",
        ],
        "attribution_des_erreurs": (
            "un code d'erreur se saisit au niveau du critère et ne concerne que ce critère. "
            "Aucune propagation automatique vers les autres critères de l'item, ni vers les "
            "autres compétences de l'item, n'est autorisée."),
        "raw_assessment_score": {
            "label": "score brut au sujet de clôture",
            "max": 20,
            "avertissement": ("ce score n'est pas un diagnostic de consolidation N-1 : le sujet "
                              "contient aussi des éléments de passerelle vers l'année suivante."),
        },
        "curriculum_split": {
            "n_minus_1_available_points": n1,
            "bridge_n_available_points": br,
            "total_points": round(n1 + br, 3),
        },
        "criteria_count": len(criteria),
        "mixed_criteria": [c["criterion_id"] for c in criteria
                           if c["curriculum_scope"] == "mixed"],
        "criteria_with_limited_evidence_quality": [
            c["criterion_id"] for c in criteria if c["evidence_quality"] == "limited_by_prompt"],
        "teacher_observation_non_scored": [
            {"item_ref": ref, "observations": obs}
            for (sid, ref), obs in sorted(equity_rules.NON_SCORED_OBSERVATIONS.items())
            if sid == student["student_id"]
        ],
        "estimated_duration_minutes": student["estimated_duration_minutes"],
        "observed_duration_minutes": None,
        "duration_note": ("l'évaluation ayant été distribuée, sa longueur n'est plus modifiée. La "
                          "durée réellement observée sera saisie si une mesure pédagogiquement "
                          "raisonnable est possible ; elle servira à calibrer les heuristiques, "
                          "pas à juger l'élève."),
    }


def overlay(student, criteria, manifest, key):
    answers = {a["ref"]: a for a in key["answers"]}
    items = []
    for it in manifest["items"]:
        crits = [c for c in criteria if c["item_ref"] == it["ref"]]
        a = answers[it["ref"]]
        items.append({
            "item_id": it["item_id"],
            "ref": it["ref"],
            "part": it["part"],
            "kind": it["kind"],
            "original_points": it["points"],
            "original_answer_preserved": True,
            "original_expected_answer": a["expected_answer"],
            "estimated_duration_minutes": it["time_estimate"]["minutes"],
            "observed_duration_minutes": None,
            "comparison_status": it["comparison_status"],
            "retention": it.get("retention") or {},
            "teacher_observation_non_scored":
                equity_rules.non_scored_for(student["student_id"], it["ref"]),
            "criteria": [{
                "criterion_id": c["criterion_id"],
                "criterion_rank": c["criterion_rank"],
                "subpart": c["subpart"],
                "original_points": c["original_points"],
                "original_skill_id": c["original_skill_id"],
                "analysis_skill_id": c["analysis_skill_id"],
                "curriculum_scope": c["curriculum_scope"],
                "evidence_type": c["evidence_type"],
                "desc": c["desc"],
                "accepted_methods": c["accepted_methods"],
                "interpretation_limits": c["interpretation_limits"],
                "fairness_rules": c["fairness_rules"],
                "error_codes_allowed": c["error_codes_allowed"],
                "evidence_quality": c["evidence_quality"],
                "scope_rationale": c["scope_rationale"],
                **({"printed_prompt": c["printed_prompt"]} if c.get("printed_prompt") else {}),
                **({"proof_levels": c["proof_levels"]} if c.get("proof_levels") else {}),
                **({"teacher_correction": c["teacher_correction"]}
                   if c.get("teacher_correction") else {}),
                **({"rejected_as_general_justification":
                    c["rejected_as_general_justification"]}
                   if c.get("rejected_as_general_justification") else {}),
                **({"rejected_as_detection": c["rejected_as_detection"]}
                   if c.get("rejected_as_detection") else {}),
                **({"virtual_subcriteria": c["virtual_subcriteria"]}
                   if c.get("virtual_subcriteria") else {}),
            } for c in crits],
        })
    return {
        "schema": "nexus-s5-answer-key-overlay-v3",
        "generated_on": pd.GENERATED_ON,
        "confidential": True,
        "student_id": student["student_id"],
        "level_key": student["level_key"],
        "subject": student["subject"],
        "source_answer_key": os.path.relpath(
            os.path.join(student["teacher_dir"], "answer_key.json"), pd.REPO_ROOT),
        "source_answer_key_status": "conservé intact comme preuve de ce qui existait à la "
                                    "distribution",
        "items": items,
    }


def notes(student, criteria, pol):
    L = []
    a = L.append
    a("# Notes de correction — %s" % student["student_name"])
    a("")
    a("**%s — %s.** Document de travail enseignant. Il ne remplace aucun livret et ne modifie "
      "aucune question." % (student["level_label"], student["subject"]))
    a("")
    a("## Ce que ce dossier change, et ce qu'il ne change pas")
    a("")
    a("Le sujet et l'évaluation ont été imprimés et remis à l'élève. Ils sont figés. "
      "Ce qui suit ne porte que sur la correction et sur ce qu'il est légitime d'en conclure.")
    a("")
    a("## Deux décomptes séparés")
    a("")
    a("| | points disponibles |")
    a("| --- | ---: |")
    a("| consolidation des acquis de l'année N-1 | %.2f |"
      % pol["curriculum_split"]["n_minus_1_available_points"])
    a("| passerelles vers l'année N | %.2f |"
      % pol["curriculum_split"]["bridge_n_available_points"])
    a("| **score brut au sujet de clôture** | **%.2f** |"
      % pol["curriculum_split"]["total_points"])
    a("")
    a("Le score brut sur 20 n'est pas le diagnostic de consolidation N-1. Une non-réussite sur "
      "une passerelle ne produit ni « fragile », ni « non acquis », ni priorité de remédiation.")
    a("")
    bridges = [c for c in criteria if c["curriculum_scope"] in ("bridge_n", "mixed")]
    if bridges:
        a("## Critères de passerelle — à ne jamais lire comme un déficit")
        a("")
        for c in bridges:
            if c["curriculum_scope"] == "mixed":
                a("- `%s` (%s, %.2f pt) — **critère mixte**"
                  % (c["criterion_id"], c["item_ref"], c["original_points"]))
                a("  - %s" % c["scope_rationale"])
                a("  - sous-critères analytiques virtuels :")
                for v in c["virtual_subcriteria"]:
                    a("    - `%s` %.2f pt — %s — %s"
                      % (v["virtual_criterion_id"], v["points"], v["curriculum_scope"], v["desc"]))
            else:
                a("- `%s` (%s, %.2f pt) — %s"
                  % (c["criterion_id"], c["item_ref"], c["original_points"],
                     c["analysis_skill_id"]))
                a("  - %s" % c["scope_rationale"])
            for lim in c["interpretation_limits"]:
                a("  - limite : %s" % lim)
        a("")
    delicate = [c for c in criteria if c["evidence_quality"] == "limited_by_prompt"]
    if delicate:
        a("## Questions à correction prudente")
        a("")
        for c in delicate:
            a("### %s — critère `%s` (%.2f pt)"
              % (c["item_ref"], c["criterion_id"], c["original_points"]))
            a("")
            if c.get("printed_prompt"):
                a("Consigne réellement imprimée : « %s »" % c["printed_prompt"])
                a("")
            if c.get("proof_levels"):
                a("- niveau demandé : %s" % c["proof_levels"]["niveau_demande"])
                a("- preuve renforcée : %s" % c["proof_levels"]["preuve_renforcee"])
            for m in c["accepted_methods"]:
                a("- accepté : %s" % m)
            for m in c.get("rejected_as_general_justification", []):
                a("- refusé comme justification générale : %s" % m)
            for m in c.get("rejected_as_detection", []):
                a("- refusé comme preuve de détection : %s" % m)
            if c.get("teacher_correction"):
                a("- correction enseignante : %s" % c["teacher_correction"])
            for r in c["fairness_rules"]:
                a("- règle de correction : %s" % r)
            for lim in c["interpretation_limits"]:
                a("- limite d'interprétation : %s" % lim)
            a("")
    ns = pol["teacher_observation_non_scored"]
    if ns:
        a("## Observations enseignantes non scorées")
        a("")
        for row in ns:
            for o in row["observations"]:
                a("- **%s** — %s" % (row["item_ref"], o["observation"]))
                a("  - %s" % o["raison"])
                a("  - %s" % o["consequence"])
        a("")
    a("## Saisie")
    a("")
    a("La saisie se fait critère par critère, dans "
      "`responses/responses_v3_TEMPLATE_%s.json`. Un code d'erreur ne se porte que sur le "
      "critère effectivement échoué." % student["student_id"])
    return "\n".join(L)


def main():
    scope = pd.read_json(SCOPE, "carte curriculaire")
    by_student = {}
    for c in scope["criteria"]:
        by_student.setdefault(c["student_id"], []).append(c)
    written = 0
    for st in pd.students():
        manifest = pd.manifest_of(st)
        st = dict(st)
        st["estimated_duration_minutes"] = round(
            sum(i["time_estimate"]["minutes"] for i in manifest["items"]), 2)
        crits = by_student[st["student_id"]]
        pol = policy(st, crits)
        d = os.path.join(OUTDIR, st["student_id"])
        pd.write_json(os.path.join(d, "CORRECTION_POLICY.json"), pol)
        pd.write_json(os.path.join(d, "ANSWER_KEY_OVERLAY.json"),
                      overlay(st, crits, manifest, pd.answer_key_of(st)))
        pd.write_text(os.path.join(d, "TEACHER_NOTES.md"), notes(st, crits, pol))
        written += 1
    print("overlays écrits pour %d élèves" % written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
