#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit la carte curriculaire critère par critère, sans toucher au sujet.

Sorties, toutes dans S5_post_distribution_v3/curriculum_scope/ :

    curriculum_references.json   textes réglementaires applicables en 2026-2027
    analysis_skills.json         alias analytiques et compétences d'origine
    criteria_scope.json          les 337 critères réels, chacun classé et justifié
    SCOPE_RATIONALE.md           la même chose, lisible par un humain
"""

import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd
import scope_rules
import equity_rules

OUTDIR = os.path.join(pd.V3_ROOT, "curriculum_scope")

# --------------------------------------------------------------------------
# Références curriculaires. Seuls les NOR effectivement documentés dans le
# dossier de mission sont portés ; aucun numéro n'est fabriqué. Lorsqu'un texte
# n'est pas documenté ici, le champ vaut null et le fait est dit.
# --------------------------------------------------------------------------
CURRICULUM_REFERENCES = {
    "schema": "nexus-s5-curriculum-references-v3",
    "generated_on": pd.GENERATED_ON,
    "annee_scolaire": "2026-2027",
    "avertissement": ("aucun NOR n'est inventé. Lorsqu'un texte applicable n'est pas documenté "
                      "dans le dossier, « nor » vaut null et « nor_documente » vaut false : "
                      "l'absence est déclarée, elle n'est pas comblée."),
    "levels": {
        "4e": {
            "grade_n": "Quatrième", "grade_n_minus_1": "Cinquième",
            "curriculum_current": {
                "nor": "MENE2018714A", "nor_documente": True,
                "objet": "programme du cycle 4 (Cinquième, Quatrième, Troisième)",
                "applicable_2026_2027": True,
                "couvre": ["n_minus_1", "bridge_n"],
            },
            "curriculum_successor": {
                "nor": "MENE2602912A", "nor_documente": True,
                "applicable_to_grade_2026_2027": False,
                "note": "changement ultérieur pour la Quatrième : ne pas appliquer par anticipation",
            },
        },
        "3e": {
            "grade_n": "Troisième", "grade_n_minus_1": "Quatrième",
            "curriculum_current": {
                "nor": "MENE2018714A", "nor_documente": True,
                "objet": "programme du cycle 4 (Cinquième, Quatrième, Troisième)",
                "applicable_2026_2027": True,
                "couvre": ["n_minus_1", "bridge_n"],
            },
            "curriculum_successor": {
                "nor": "MENE2602912A", "nor_documente": True,
                "applicable_to_grade_2026_2027": False,
                "note": "changement ultérieur pour la Troisième : ne pas appliquer par anticipation",
            },
        },
        "2nde": {
            "grade_n": "Seconde générale et technologique", "grade_n_minus_1": "Troisième",
            "curriculum_current": {
                "nor": "MENE2602914A", "nor_documente": True,
                "objet": "programme de mathématiques de la classe de Seconde",
                "applicable_2026_2027": True, "couvre": ["bridge_n"],
            },
            "curriculum_n_minus_1": {
                "nor": "MENE2018714A", "nor_documente": True,
                "objet": "programme du cycle 4, dont la classe de Troisième",
                "couvre": ["n_minus_1"],
            },
        },
        "1ere_spe": {
            "grade_n": "Première générale — spécialité mathématiques",
            "grade_n_minus_1": "Seconde générale et technologique",
            "curriculum_current": {
                "nor": "MENE2602917A", "nor_documente": True,
                "objet": "programme de la spécialité mathématiques en classe de Première",
                "applicable_2026_2027": True, "couvre": ["bridge_n"],
            },
            "curriculum_n_minus_1": {
                "nor": None, "nor_documente": False,
                "objet": "programme de mathématiques de la classe de Seconde suivi par ces élèves "
                         "en 2025-2026",
                "note": "le numéro NOR de ce texte n'est pas documenté dans le dossier de "
                        "mission ; il n'est donc pas renseigné.",
                "couvre": ["n_minus_1"],
            },
        },
        "1re_nsi": {
            "grade_n": "Première générale — numérique et sciences informatiques",
            "grade_n_minus_1": "Seconde générale et technologique",
            "curriculum_current": {
                "nor": "MENE1901633A", "nor_documente": True,
                "objet": "programme de la spécialité numérique et sciences informatiques en "
                         "classe de Première",
                "applicable_2026_2027": True, "couvre": ["bridge_n"],
            },
            "curriculum_n_minus_1": {
                "nor": None, "nor_documente": False,
                "objet": "acquis de programmation antérieurs : algorithmique et programmation du "
                         "cycle 4, sciences numériques et technologie en Seconde, et séances S1 "
                         "à S4 du stage",
                "note": "la NSI n'a pas de programme d'année N-1 ; les prérequis mobilisés sont "
                        "de sources multiples, dont les numéros NOR ne sont pas documentés dans "
                        "le dossier de mission.",
                "couvre": ["n_minus_1"],
            },
        },
    },
    "transitions_n_minus_1_vers_n": {
        "4e": ["somme et différence de relatifs (5e) -> produit et quotient de relatifs (4e)",
               "expression littérale (5e) -> mise en équation et équation du premier degré (4e)"],
        "3e": ["distributivité simple k(ax+b) (4e) -> double distributivité (a+b)(c+d) (3e)",
               "cosinus (4e) -> sinus et tangente (3e)",
               "expressions littérales (4e) -> notion de fonction, image et antécédent (3e)"],
        "2nde": ["inégalités écrites en phrases (3e) -> notation en intervalle (2nde)",
                 "notion de fonction, image, antécédent et notation f(x), DÉJÀ au programme de "
                 "Troisième -> approfondissements et notations propres à la Seconde"],
        "1ere_spe": ["évolutions successives et coefficient multiplicateur (2nde) -> suite "
                     "géométrique définie par récurrence (1re)",
                     "coefficient directeur d'une droite (2nde) -> taux de variation moyen (1re)"],
        "1re_nsi": ["parcours de liste et contrat d'une fonction (acquis antérieurs) -> "
                    "recherche séquentielle et dichotomique, précondition, coût, invariant (1re)"],
    },
    "mise_au_point_seconde": (
        "la notion de fonction, l'image, l'antécédent et la notation f(x) appartiennent déjà à la "
        "progression de Troisième. Le livret de la séance 5 des élèves entrant en Seconde les "
        "présente globalement comme nouveaux : cette formulation est inexacte et ne peut plus être "
        "reprise dans les métadonnées ni dans les bilans. Seules certaines notations et certains "
        "approfondissements propres à la Seconde relèvent de bridge_n. Le livret distribué n'est "
        "pas modifié ; la mise au point figure dans teacher_guidance/CLARIFICATIONS_ORALES_S5.md."),
}


def _crit_meta(item, criterion, rank, student, exc, case):
    """Assemble la métadonnée d'un critère, sans rien changer à ses points ni à son id."""
    original_skill = criterion["skill_id"]
    scope = exc["scope"] if exc else "n_minus_1"
    alias = (exc or {}).get("analysis_skill_id") or original_skill
    accepted = list(item.get("methodes_alternatives_acceptees") or [])
    accepted += list((exc or {}).get("accepted_methods") or [])
    accepted += list((case or {}).get("accepted_methods") or [])
    limits = list((exc or {}).get("interpretation_limits") or [])
    limits += list((case or {}).get("interpretation_limits") or [])
    fairness = list((exc or {}).get("fairness_rules") or [])
    if case and case.get("grading_rule"):
        fairness.append(case["grading_rule"])
    row = {
        "criterion_id": criterion["criterion_id"],
        "item_id": item["item_id"],
        "item_ref": item["ref"],
        "item_kind": item["kind"],
        "criterion_rank": rank,
        "subpart": criterion["subpart"],
        "original_points": criterion["points"],
        "original_skill_id": original_skill,
        "analysis_skill_id": alias,
        "curriculum_scope": scope,
        "evidence_type": criterion["evidence_type"],
        "desc": criterion["desc"],
        "accepted_methods": accepted,
        "interpretation_limits": limits,
        "fairness_rules": fairness,
        "error_codes_allowed": sorted(item.get("error_codes") or []),
        "evidence_quality": "limited_by_prompt" if case else "standard",
        "scope_rationale": (exc or {}).get(
            "rationale",
            "aucune notion du programme de l'année N n'est requise pour traiter la question "
            "imprimée : le critère mesure un acquis de l'année N-1."),
    }
    if case:
        row["printed_prompt"] = case.get("printed_prompt")
        if case.get("proof_levels"):
            row["proof_levels"] = case["proof_levels"]
        if case.get("rejected_as_general_justification"):
            row["rejected_as_general_justification"] = case["rejected_as_general_justification"]
        if case.get("rejected_as_detection"):
            row["rejected_as_detection"] = case["rejected_as_detection"]
        if case.get("teacher_correction"):
            row["teacher_correction"] = case["teacher_correction"]
    if scope == "mixed":
        virtual = []
        total = 0.0
        for v in exc["virtual"]:
            pts = round(criterion["points"] * v["share"], 6)
            total += pts
            virtual.append({
                "virtual_criterion_id": "%s_%s" % (criterion["criterion_id"], v["suffix"]),
                "parent_criterion_id": criterion["criterion_id"],
                "points": pts,
                "curriculum_scope": v["scope"],
                "analysis_skill_id": v.get("analysis_skill_id") or original_skill,
                "desc": v["desc"],
                "virtual": True,
            })
        if round(total, 6) != round(criterion["points"], 6):
            raise pd.PostDistributionError(
                "critère mixte %s : la somme des sous-critères virtuels (%s) diffère des points "
                "d'origine (%s)" % (criterion["criterion_id"], total, criterion["points"]))
        row["virtual_subcriteria"] = virtual
    return row


def build():
    rows = []
    aliases = {}
    for st in pd.students():
        manifest = pd.manifest_of(st)
        for item in manifest["items"]:
            for rank, crit in enumerate(item["grading_criteria"], start=1):
                exc = scope_rules.lookup(st["student_id"], st["level_key"], item["kind"],
                                         item["ref"], rank)
                case = equity_rules.case_for(st["student_id"], st["level_key"], item["kind"],
                                             item["ref"], rank)
                row = _crit_meta(item, crit, rank, st, exc, case)
                row["student_id"] = st["student_id"]
                row["level_key"] = st["level_key"]
                rows.append(row)
                if exc and exc.get("analysis_skill_id"):
                    aliases.setdefault(exc["analysis_skill_id"], {
                        "analysis_skill_id": exc["analysis_skill_id"],
                        "label": exc.get("analysis_skill_label", ""),
                        "curriculum_scope": exc["scope"],
                        "original_skill_ids": set(),
                        "level_keys": set(),
                    })
                    aliases[exc["analysis_skill_id"]]["original_skill_ids"].add(
                        row["original_skill_id"])
                    aliases[exc["analysis_skill_id"]]["level_keys"].add(st["level_key"])
                for v in row.get("virtual_subcriteria", []):
                    if v["analysis_skill_id"] != row["original_skill_id"]:
                        a = aliases.setdefault(v["analysis_skill_id"], {
                            "analysis_skill_id": v["analysis_skill_id"],
                            "label": next((x.get("analysis_skill_label", "")
                                           for x in exc["virtual"]
                                           if x.get("analysis_skill_id") == v["analysis_skill_id"]),
                                          ""),
                            "curriculum_scope": v["curriculum_scope"],
                            "original_skill_ids": set(), "level_keys": set(),
                        })
                        a["original_skill_ids"].add(row["original_skill_id"])
                        a["level_keys"].add(st["level_key"])
    for a in aliases.values():
        a["original_skill_ids"] = sorted(a["original_skill_ids"])
        a["level_keys"] = sorted(a["level_keys"])
    return rows, aliases


def summarise(rows):
    per_student = {}
    for r in rows:
        s = per_student.setdefault(r["student_id"], {
            "student_id": r["student_id"], "level_key": r["level_key"],
            "criteria": 0, "points_total": 0.0,
            "n_minus_1_points": 0.0, "bridge_n_points": 0.0,
            "n_minus_1_criteria": 0, "bridge_n_criteria": 0, "mixed_criteria": 0,
        })
        s["criteria"] += 1
        s["points_total"] += r["original_points"]
        if r["curriculum_scope"] == "mixed":
            s["mixed_criteria"] += 1
            for v in r["virtual_subcriteria"]:
                s["%s_points" % v["curriculum_scope"]] += v["points"]
        else:
            s["%s_points" % r["curriculum_scope"]] += r["original_points"]
            s["%s_criteria" % r["curriculum_scope"]] += 1
    for s in per_student.values():
        for k in ("points_total", "n_minus_1_points", "bridge_n_points"):
            s[k] = round(s[k], 3)
    return per_student


def main():
    rows, aliases = build()
    per_student = summarise(rows)
    pd.write_json(os.path.join(OUTDIR, "curriculum_references.json"), CURRICULUM_REFERENCES)
    pd.write_json(os.path.join(OUTDIR, "analysis_skills.json"), {
        "schema": "nexus-s5-analysis-skills-v3",
        "generated_on": pd.GENERATED_ON,
        "objet": ("alias analytiques créés pour ne plus fusionner, sous un même identifiant, une "
                  "compétence de l'année N-1 et une notion de l'année N. Les skill_id d'origine "
                  "sont conservés tels quels pour la compatibilité."),
        "aliases": [aliases[k] for k in sorted(aliases)],
    })
    pd.write_json(os.path.join(OUTDIR, "criteria_scope.json"), {
        "schema": "nexus-s5-criteria-scope-v3",
        "generated_on": pd.GENERATED_ON,
        "principe": scope_rules.__doc__.strip(),
        "regles_generales_de_correction": equity_rules.GENERAL_RULES,
        "bridge_declared_in_livret": scope_rules.BRIDGE_DECLARED_IN_LIVRET,
        "counts": {
            "criteria_total": len(rows),
            "n_minus_1": sum(1 for r in rows if r["curriculum_scope"] == "n_minus_1"),
            "bridge_n": sum(1 for r in rows if r["curriculum_scope"] == "bridge_n"),
            "mixed": sum(1 for r in rows if r["curriculum_scope"] == "mixed"),
            "virtual_subcriteria": sum(len(r.get("virtual_subcriteria", [])) for r in rows),
            "criteria_with_limited_evidence_quality":
                sum(1 for r in rows if r["evidence_quality"] == "limited_by_prompt"),
        },
        "per_student": [per_student[k] for k in sorted(per_student)],
        "criteria": rows,
    })
    print("critères classés : %d" % len(rows))
    for k in ("n_minus_1", "bridge_n", "mixed"):
        print("  %-10s %d" % (k, sum(1 for r in rows if r["curriculum_scope"] == k)))
    print("alias analytiques : %d" % len(aliases))
    return 0


if __name__ == "__main__":
    sys.exit(main())
