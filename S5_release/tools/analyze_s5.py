#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analyse déterministe du diagnostic de sortie de la séance S5.

Ce script fait la totalité des calculs. Aucun modèle de langage n'intervient à ce
niveau : score, taux de réussite, maîtrise par compétence, delta lorsqu'il est
légitime, profil d'erreurs, priorités et matière du plan de quatre semaines sont
produits exclusivement à partir des fichiers structurés.

ENTRÉES
    student_learning_profile.json   état de départ et métadonnées d'items
    _ENSEIGNANT/evaluation_manifest.json   points, barème, comparabilité
    _ENSEIGNANT/answer_key.json     corrigé structuré (contrôle de cohérence)
    <responses>.json                copie renseignée de responses_TEMPLATE.json

SORTIES
    post_stage_analysis.json        conforme à post_stage_analysis_schema.json
    four_week_action_plan.json      plan des quatre premières semaines
    bilan_facts.json                faits chiffrés utilisables pour le bilan écrit

EXEMPLES
    # 1. copier le gabarit de saisie et le renseigner
    cp S5_cloture/3e/Mathematiques/Elyes_KEFI/responses_TEMPLATE.json \\
       S5_cloture/3e/Mathematiques/Elyes_KEFI/responses_2026-08-28.json

    # 2. lancer l'analyse
    python3 S5_cloture/tools/analyze_s5.py \\
        --student elyes-kefi \\
        --responses S5_cloture/3e/Mathematiques/Elyes_KEFI/responses_2026-08-28.json

    # 3. contrôler sans rien écrire
    python3 S5_cloture/tools/analyze_s5.py --student elyes-kefi \\
        --responses .../responses_2026-08-28.json --dry-run

RÈGLES APPLIQUÉES
    * un delta n'est calculé que lorsque la compétence dispose d'une mesure
      initiale ET d'au moins un item final parallèle (comparison_status
      « item_level ») ;
    * sinon la sortie porte « comparison_status »: « skill_level » ou
      « not_comparable », et « mastery_delta »: null ;
    * une valeur absente n'est jamais remplacée par une valeur par défaut :
      le script s'arrête et signale la saisie incomplète ;
    * la maîtrise 4 exige une réussite constatée sur une tâche de transfert.
"""

import argparse
import json
import os
import sys
sys.dont_write_bytecode = True  # aucune trace de cache dans la livraison

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core
from data import common

SCHEMA = "nexus-s5-post-stage-analysis-v2"

# Le diagnostic initial ne fournit qu'un statut qualitatif par domaine ; les réponses
# de l'élève aux 18 questions du positionnement n'ont pas été conservées. Convertir
# ce statut en score pour en soustraire un autre produirait un écart sans valeur de
# mesure. Tant qu'aucune mesure initiale nominative appariée n'existe, le script
# impose donc mastery_delta = null, quelle que soit la compétence.
BASELINE_MEASURE_AVAILABLE = False
DELTA_BLOCKED_REASON = ("aucune mesure initiale nominative appariée : le dossier ne conserve "
                        "qu'un statut qualitatif par domaine, pas les réponses de l'élève")

# Seuils de conversion taux de réussite -> niveau de maîtrise final.
MASTERY_THRESHOLDS = [(0.20, 0), (0.45, 1), (0.65, 2), (0.85, 3)]
MAX_P1 = 4

# Force de preuve : ce que la copie permet réellement d'affirmer sur une compétence.
# Ce n'est pas une fiabilité psychométrique — le mot serait abusif sur douze items —
# mais un décompte explicite de ce qui étaye la conclusion.
EVIDENCE_RUBRIC = [
    ("au moins deux critères indépendants", lambda a: a["n_criteria"] >= 2, +1),
    ("au moins deux items distincts", lambda a: a["n_items"] >= 2, +1),
    ("au moins deux points en jeu", lambda a: a["max"] >= 2, +1),
    ("évaluée sur une tâche de transfert", lambda a: a["has_transfer"], +1),
    ("mesurée juste après remédiation", lambda a: a["immediate"], -1),
]


class InputError(Exception):
    pass


def load(path, label):
    if not os.path.exists(path):
        raise InputError("%s introuvable : %s" % (label, path))
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise InputError("%s illisible (%s) : %s" % (label, exc, path))


def find_student(sid):
    for st in core.all_students():
        if st["id"] == sid:
            return st
    raise InputError("identifiant d'élève inconnu : %s. Identifiants disponibles : %s"
                     % (sid, ", ".join(s["id"] for s in core.all_students())))


def mastery_from_rate(rate):
    for threshold, level in MASTERY_THRESHOLDS:
        if rate < threshold:
            return level
    return 4


def analyse(student, responses, base_dir=None):
    """base_dir n'est utilisé que par le jeu de tests synthétique de tools/tests/."""
    d = base_dir or core.student_output_dir(student)
    td = os.path.join(d, "_ENSEIGNANT")
    profile = load(os.path.join(d, "student_learning_profile.json"), "profil")
    manifest = load(os.path.join(td, "evaluation_manifest.json"), "manifeste")
    key = load(os.path.join(td, "answer_key.json"), "corrigé")
    lv = core.level_of(student)

    # ------------------------------------------------------ contrôles d'entrée
    if responses.get("student_id") != student["id"]:
        raise InputError("le fichier de saisie porte student_id=%r alors que l'élève demandé est %r"
                         % (responses.get("student_id"), student["id"]))
    m = {i["ref"]: i for i in manifest["items"]}
    k = {a["ref"]: a for a in key["answers"]}
    r = {x["ref"]: x for x in responses.get("responses", [])}
    if sorted(r) != sorted(m):
        raise InputError("les items saisis ne correspondent pas au manifeste : "
                         "saisis %s, attendus %s" % (sorted(r), sorted(m)))

    per_criterion = []
    for ref in common.EXAM_ITEM_ORDER:
        it, row = m[ref], r[ref]
        saisis = {c["criterion_id"]: c for c in row.get("criteria") or []}
        attendus = {c["criterion_id"]: c for c in it["grading_criteria"]}
        if sorted(saisis) != sorted(attendus):
            raise InputError("item %s : les critères saisis ne correspondent pas au barème. "
                             "Saisis %s, attendus %s. La saisie se fait critère par critère."
                             % (ref, sorted(saisis), sorted(attendus)))
        for cid, cref in attendus.items():
            got = saisis[cid].get("score")
            if got is None:
                raise InputError("critère %s : aucun score saisi. Le script ne complète jamais "
                                 "une valeur manquante." % cid)
            try:
                got = float(got)
            except (TypeError, ValueError):
                raise InputError("critère %s : score non numérique (%r)" % (cid, got))
            if got < 0 or got > cref["points"]:
                raise InputError("critère %s : score %s hors de l'intervalle [0 ; %s]"
                                 % (cid, got, cref["points"]))
            per_criterion.append({
                "criterion_id": cid, "item_ref": ref, "item_id": it["item_id"],
                "skill_id": cref["skill_id"], "evidence_type": cref["evidence_type"],
                "subpart": cref["subpart"], "points": got, "max_points": cref["points"],
                "difficulty": it["difficulty"], "part": it["part"], "kind": it["kind"],
            })
        if k[ref]["points"] != it["points"]:
            raise InputError("incohérence manifeste/corrigé sur les points de %s" % ref)
        for code in row.get("error_codes") or []:
            if code not in common.ERROR_CODES:
                raise InputError("item %s : code d'erreur inconnu %r" % (ref, code))
        if it.get("confidence_probe"):
            c = row.get("confidence")
            if c is not None and c not in (1, 2, 3, 4):
                raise InputError("item %s : certitude %r hors de l'échelle 1-4" % (ref, c))

    # ----------------------------------------------------- score, item par item
    per_item = []
    for ref in common.EXAM_ITEM_ORDER:
        it, row = m[ref], r[ref]
        crits = [c for c in per_criterion if c["item_ref"] == ref]
        score = round(sum(c["points"] for c in crits), 4)
        per_item.append({
            "item_id": it["item_id"], "ref": ref, "part": it["part"], "kind": it["kind"],
            "skill_id": it["skill_id"], "skills": sorted({c["skill_id"] for c in crits}),
            "difficulty": it["difficulty"], "task_type": it["task_type"],
            "points": score, "max_points": it["points"],
            "success_rate": round(score / it["points"], 4) if it["points"] else None,
            "criteria": [{"criterion_id": c["criterion_id"], "skill_id": c["skill_id"],
                          "evidence_type": c["evidence_type"],
                          "points": c["points"], "max_points": c["max_points"]} for c in crits],
            "error_codes": list(row.get("error_codes") or []),
            "confidence": row.get("confidence"),
            "comparison_status": it["comparison_status"],
        })
    total = sum(i["points"] for i in per_item)
    maxp = sum(i["max_points"] for i in per_item)
    by_part = {}
    for p in ("A", "B", "C"):
        sel = [i for i in per_item if i["part"] == p]
        by_part[p] = {"points": round(sum(i["points"] for i in sel), 4),
                      "max_points": sum(i["max_points"] for i in sel),
                      "success_rate": round(sum(i["points"] for i in sel)
                                            / sum(i["max_points"] for i in sel), 4)}

    # ------------------- agrégation par compétence, depuis les critères réussis
    pre = {row["skill_id"]: row for row in profile["baseline"]["skills"]}
    acc = {}
    for c in per_criterion:
        a = acc.setdefault(c["skill_id"], {"got": 0.0, "max": 0.0, "items": set(),
                                           "criteria": [], "evidences": set(),
                                           "has_transfer": False})
        a["got"] += c["points"]
        a["max"] += c["max_points"]
        a["items"].add(c["item_ref"])
        a["criteria"].append(c["criterion_id"])
        a["evidences"].add(c["evidence_type"])
        if c["difficulty"] == "transfert":
            a["has_transfer"] = a["has_transfer"] or (c["points"] / c["max_points"] >= 0.75)
    errors_by_skill = {}
    for i in per_item:
        for sid in i["skills"]:
            errors_by_skill.setdefault(sid, []).extend(i["error_codes"])

    skills = []
    for sid, a in sorted(acc.items()):
        rate = a["got"] / a["max"] if a["max"] else 0.0
        post = mastery_from_rate(rate)
        capped = False
        if post == 4 and not a["has_transfer"]:
            post, capped = 3, True
        statuses = {i["comparison_status"] for i in per_item if sid in i["skills"]}
        if "indicative_skill_comparison" in statuses:
            status = "indicative_skill_comparison"
        elif "post_only" in statuses:
            status = "post_only"
        else:
            status = "not_comparable"
        if not BASELINE_MEASURE_AVAILABLE and status == "parallel_measures":
            status = "indicative_skill_comparison"
        ret = pre[sid].get("retention") or {}
        ev = {"n_criteria": len(a["criteria"]), "n_items": len(a["items"]),
              "max": a["max"], "has_transfer": a["has_transfer"],
              "immediate": bool(ret.get("recommended_delayed_check"))}
        pts_ev, detail = 0, []
        for label, test, weight in EVIDENCE_RUBRIC:
            ok = bool(test(ev))
            if ok:
                pts_ev += weight
            detail.append({"critere": label, "verifie": ok, "poids": weight})
        strength = "forte" if pts_ev >= 4 else ("moyenne" if pts_ev >= 2 else "faible")
        skills.append({
            "skill_id": sid,
            "label": lv["skills"][sid]["label"],
            "domain": lv["skills"][sid]["domain"],
            "importance_n": lv["skills"][sid]["importance_n"],
            "items": sorted(a["items"]),
            "criteria": sorted(a["criteria"]),
            "evidence_types": sorted(a["evidences"]),
            "points": round(a["got"], 3), "max_points": round(a["max"], 3),
            "success_rate": round(rate, 4),
            "baseline_status_qualitative": pre[sid]["statut_avant_s5"],
            "baseline_mastery": None,
            "baseline_measure_available": BASELINE_MEASURE_AVAILABLE,
            "post_mastery": post,
            "post_mastery_capped_by_transfer": capped,
            "mastery_delta": None,
            "delta_blocked_reason": DELTA_BLOCKED_REASON,
            "comparison_status": status,
            "evidence_strength": strength,
            "evidence_strength_score": pts_ev,
            "evidence_strength_detail": detail,
            "post_test_context": ret.get("post_test_context"),
            "retention_status": ret.get("retention_status"),
            "recommended_delayed_check": bool(ret.get("recommended_delayed_check")),
            "retention_reason": ret.get("reason"),
            "errors": errors_by_skill.get(sid, []),
        })

    # ---------------------------------------------------------------- erreurs
    profile_after = {}
    for i in per_item:
        for c in i["error_codes"]:
            profile_after[c] = profile_after.get(c, 0) + 1
    dominant = [c for c, _ in sorted(profile_after.items(), key=lambda kv: -kv[1])[:3]]

    # -------------------------------------------------------------- certitude
    probes = [i for i in per_item if m[i["ref"]].get("confidence_probe")]
    cells = {"juste_confiance_haute": 0, "juste_confiance_basse": 0,
             "faux_confiance_basse": 0, "faux_confiance_haute": 0,
             "partiel_non_classe": 0}
    saisies = [p for p in probes if p["confidence"] is not None]
    for p in saisies:
        rate = p["success_rate"] or 0
        if 0.25 < rate < 0.75:
            cells["partiel_non_classe"] += 1
            continue
        haute = p["confidence"] >= 3
        cells["%s_confiance_%s" % ("juste" if rate >= 0.75 else "faux",
                                   "haute" if haute else "basse")] += 1
    conf_after = (round(sum(p["confidence"] for p in saisies) / len(saisies), 2)
                  if saisies else None)

    priorities = rank_priorities(skills, profile_after)

    warnings = [
        "aucun écart de maîtrise n'est calculé : " + DELTA_BLOCKED_REASON + ".",
    ]
    if not saisies:
        warnings.append("aucune certitude saisie : la calibration réussite-confiance ne peut pas être établie.")
    if len(saisies) < len(probes):
        warnings.append("certitude saisie sur %d des %d items pivots seulement."
                        % (len(saisies), len(probes)))
    faibles = [s["skill_id"] for s in skills if s["evidence_strength"] == "faible"]
    if faibles:
        warnings.append("force de preuve faible pour : %s. Ces niveaux de maîtrise sont indicatifs "
                        "et ne doivent pas fonder une conclusion isolée." % ", ".join(faibles))
    immediats = [s["skill_id"] for s in skills if s["recommended_delayed_check"]]
    if immediats:
        warnings.append("compétences évaluées moins d'une heure après leur remédiation : %s. "
                        "La réussite y mesure une performance immédiate ; la rétention reste à "
                        "vérifier par un contrôle différé en semaine 1 ou 2."
                        % ", ".join(immediats))
    nouveau = [s["skill_id"] for s in skills if s["comparison_status"] == "not_comparable"]
    if nouveau:
        warnings.append("contenus introduits pendant la séance 5 et donc exclus de toute lecture "
                        "de progression : %s." % ", ".join(nouveau))

    return {
        "schema": SCHEMA,
        "student_id": student["id"],
        "student_name": student["name"],
        "level_key": lv["key"], "subject": lv["subject"],
        "analysed_on": responses.get("assessed_on"),
        "status": "analysed",
        "scoring_model": "par critère : chaque critère porte une compétence unique",
        "baseline_measure_available": BASELINE_MEASURE_AVAILABLE,
        "score": {
            "total_points": round(total, 2), "max_points": maxp,
            "note_sur_20": round(20.0 * total / maxp, 2),
            "success_rate": round(total / maxp, 4),
            "by_part": by_part,
            "common_core_points": round(sum(i["points"] for i in per_item if i["kind"] == "commun"), 2),
            "individual_points": round(sum(i["points"] for i in per_item if i["kind"] == "individuel"), 2),
        },
        "items": per_item,
        "criteria": per_criterion,
        "skills": skills,
        "confidence": {
            "confidence_before_reported": profile["baseline"].get("confidence_calibration"),
            "confidence_before": None,
            "confidence_after": conf_after,
            "calibration_cells": cells,
            "note": ("la certitude n'entre pas dans la note ; elle sert à distinguer ce qui est su "
                     "de ce qui est cru. Un item réussi partiellement (entre 25 et 75 %) n'est classé "
                     "ni en juste ni en faux."),
        },
        "errors": {"error_profile_before": None,
                   "error_profile_after": profile_after,
                   "dominant_codes": dominant},
        "priorities": priorities,
        "warnings": warnings,
    }


def rank_priorities(skills, error_profile):
    """Attribue P1/P2/P3/OK. Le nombre de P1 est plafonné pour rester opérationnel."""
    graded = []
    for s in skills:
        crit = s["importance_n"] == "critique"
        m = s["post_mastery"]
        if m >= 4 or (m == 3 and s["success_rate"] >= 0.85):
            rank = "OK"
        elif m <= 1:
            rank = "P1" if crit else "P2"
        elif m == 2:
            rank = "P2" if crit else "P3"
        else:
            rank = "P3" if crit else "OK"
        reason = ("maîtrise %d sur 4, taux de réussite %.0f %%, compétence %s pour l'entrée dans l'année"
                  % (m, 100 * s["success_rate"], s["importance_n"]))
        graded.append({"skill_id": s["skill_id"], "label": s["label"],
                       "priority_rank": rank, "reason": reason,
                       "post_mastery": m, "success_rate": s["success_rate"],
                       "importance_n": s["importance_n"],
                       "dominant_error_codes": _top_errors(s)})
    p1 = [g for g in graded if g["priority_rank"] == "P1"]
    if len(p1) > MAX_P1:
        p1.sort(key=lambda g: (g["importance_n"] != "critique", g["post_mastery"], g["success_rate"]))
        for g in p1[MAX_P1:]:
            g["priority_rank"] = "P2"
            g["reason"] += " ; rétrogradée en P2 pour conserver un plan de rentrée réaliste"
    order = {"P1": 0, "P2": 1, "P3": 2, "OK": 3}
    graded.sort(key=lambda g: (order[g["priority_rank"]], -(1 - g["success_rate"])))
    return graded


def _top_errors(skill_row):
    counts = {}
    for c in skill_row.get("errors") or []:
        counts[c] = counts.get(c, 0) + 1
    return [c for c, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:2]]


def build_plan(student, analysis):
    """Plan de quatre semaines déduit des priorités calculées, jamais inventé."""
    lv = core.level_of(student)
    p1 = [p for p in analysis["priorities"] if p["priority_rank"] == "P1"]
    p2 = [p for p in analysis["priorities"] if p["priority_rank"] == "P2"]
    p3 = [p for p in analysis["priorities"] if p["priority_rank"] == "P3"]
    pool = p1 + p2 + p3
    weeks = []
    cursor = 0
    for n in (1, 2, 3, 4):
        take = pool[cursor:cursor + (2 if n < 4 else 3)]
        cursor += len(take)
        if not take:
            weeks.append({"week": n, "skills": [], "objective": None,
                          "work_type": "problème mixte de réinvestissement",
                          "frequency": "1 fois", "duration_minutes": 25,
                          "success_criterion": "aucune priorité restante : consolidation libre",
                          "control_exercise": None,
                          "derived_from": []})
            continue
        crit = any(t["importance_n"] == "critique" for t in take)
        weeks.append({
            "week": n,
            "skills": [t["skill_id"] for t in take],
            "labels": [t["label"] for t in take],
            "objective": "atteindre le niveau de maîtrise 3 sur : "
                         + " ; ".join(t["label"] for t in take),
            "work_type": ("reprise guidée puis exercices gradués" if n <= 2
                          else "réactivation espacée et problème mixte"),
            "frequency": "3 séances de travail" if crit else "2 séances de travail",
            "duration_minutes": 15 if n <= 2 else 20,
            "success_criterion": "trois réussites consécutives sans aide, chacune assortie du contrôle écrit",
            "control_exercise": {
                "type": "item parallèle",
                "reference_items": sorted({i for t in take
                                           for i in _items_of_skill(analysis, t["skill_id"])}),
                "baseline_reference": sorted({b for t in take
                                              for b in lv["skills"][t["skill_id"]]["baseline_items"]}),
            },
            "derived_from": [{"skill_id": t["skill_id"], "priority_rank": t["priority_rank"],
                              "post_mastery": t["post_mastery"],
                              "success_rate": t["success_rate"],
                              "dominant_error_codes": t["dominant_error_codes"]} for t in take],
        })
    differes = [s for s in analysis["skills"] if s["recommended_delayed_check"]]
    controle_differe = {
        "semaine": 2,
        "objet": "vérifier que les réussites obtenues immédiatement après remédiation se sont "
                 "maintenues à distance",
        "skills": [s["skill_id"] for s in differes],
        "format": "mini-test de 10 minutes, deux items par compétence, items parallèles à ceux "
                  "de l'évaluation finale",
        "critere": "réussite maintenue sans aide sur au moins un item par compétence",
        "obligatoire": bool(differes),
    }
    return {
        "schema": "nexus-s5-four-week-plan-v2",
        "delayed_retention_check": controle_differe,
        "progression_chiffree_possible": False,
        "student_id": student["id"], "level_key": lv["key"], "subject": lv["subject"],
        "status": "generated_from_analysis",
        "source": "post_stage_analysis.json",
        "note_sur_20": analysis["score"]["note_sur_20"],
        "weeks": weeks,
        "follow_up_recommendation": build_follow_up(analysis),
        "warnings": analysis["warnings"],
    }


def _items_of_skill(analysis, sid):
    return [i["ref"] for i in analysis["items"] if sid in i["skills"]]


def build_follow_up(analysis):
    p1 = [p for p in analysis["priorities"] if p["priority_rank"] == "P1"]
    rate = analysis["score"]["success_rate"]
    if len(p1) >= 3 or rate < 0.5:
        proposed = "accompagnement régulier recommandé"
    elif p1:
        proposed = "points de contrôle ciblés recommandés"
    else:
        proposed = "aucun accompagnement supplémentaire justifié par les données"
    return {
        "proposed": proposed,
        "justification": "%d compétences classées P1 ; taux de réussite global de %.0f %%."
                         % (len(p1), 100 * rate),
        "data_basis": ["score.success_rate", "priorities[].priority_rank"],
    }


def build_facts(student, analysis):
    """Faits que le bilan écrit peut citer, et rien d'autre.

    Aucune progression chiffrée n'y figure : elle ne serait pas défendable. La
    confrontation initial / final reste qualitative et explicitement étiquetée
    comme indicative.
    """
    lv = core.level_of(student)
    solides = [s for s in analysis["skills"] if s["post_mastery"] >= 3]
    fragiles = [s for s in analysis["skills"] if s["post_mastery"] <= 1]
    a_confirmer = [s for s in solides if s["recommended_delayed_check"]]
    return {
        "schema": "nexus-s5-bilan-facts-v2",
        "student_id": student["id"], "student_name": student["name"],
        "level": lv["label"], "subject": lv["subject"],
        "note_sur_20": analysis["score"]["note_sur_20"],
        "success_rate_pct": round(100 * analysis["score"]["success_rate"], 1),
        "by_part": analysis["score"]["by_part"],
        "baseline_measure_available": analysis["baseline_measure_available"],
        "progression_chiffree_possible": False,
        "progression_chiffree_raison": DELTA_BLOCKED_REASON,
        "comparaison_qualitative": [{
            "skill_id": s["skill_id"], "label": s["label"],
            "statut_initial_qualitatif": s["baseline_status_qualitative"],
            "maitrise_finale": s["post_mastery"],
            "comparison_status": s["comparison_status"],
            "evidence_strength": s["evidence_strength"],
            "lecture_autorisee": ("confrontation indicative entre un statut de domaine et une "
                                  "performance finale ; aucun écart chiffré"),
        } for s in analysis["skills"] if s["comparison_status"] == "indicative_skill_comparison"],
        "skills_demonstrated": [{"skill_id": s["skill_id"], "label": s["label"],
                                 "post_mastery": s["post_mastery"],
                                 "evidence_strength": s["evidence_strength"],
                                 "a_confirmer_a_distance": s["recommended_delayed_check"]}
                                for s in solides],
        "skills_fragile": [{"skill_id": s["skill_id"], "label": s["label"],
                            "post_mastery": s["post_mastery"],
                            "evidence_strength": s["evidence_strength"]} for s in fragiles],
        "reussites_immediates_a_confirmer": [s["skill_id"] for s in a_confirmer],
        "retention_a_verifier": [{"skill_id": s["skill_id"], "label": s["label"],
                                  "post_test_context": s["post_test_context"],
                                  "retention_status": s["retention_status"]}
                                 for s in analysis["skills"] if s["recommended_delayed_check"]],
        "contenus_nouveaux_hors_progression": [s["skill_id"] for s in analysis["skills"]
                                               if s["comparison_status"] == "not_comparable"],
        "etat_final_seul": [s["skill_id"] for s in analysis["skills"]
                            if s["comparison_status"] == "post_only"],
        "dominant_error_codes": analysis["errors"]["dominant_codes"],
        "calibration_cells": analysis["confidence"]["calibration_cells"],
        "priorities": analysis["priorities"],
        "warnings": analysis["warnings"],
        "formulations_interdites": [
            "maîtrise X vers Y", "progression de N points", "a progressé de",
            "acquis durablement consolidé sur la seule évaluation finale",
        ],
        "usage": ("toute phrase chiffrée du bilan doit renvoyer à une clé de ce fichier ; "
                  "aucune affirmation quantitative ne doit être produite autrement, et "
                  "aucune progression chiffrée ne peut être écrite"),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="analyze_s5.py",
        description="Analyse déterministe du diagnostic de sortie S5 (aucun calcul par LLM).",
        epilog=__doc__.split("EXEMPLES", 1)[1] if "EXEMPLES" in __doc__ else None,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--student", metavar="ID",
                    help="identifiant de l'élève, par exemple elyes-kefi")
    ap.add_argument("--responses", metavar="FICHIER",
                    help="fichier de saisie renseigné, copie de responses_TEMPLATE.json")
    ap.add_argument("--outdir", metavar="RÉPERTOIRE",
                    help="répertoire de sortie (par défaut : celui du fichier de saisie)")
    ap.add_argument("--data-dir", metavar="RÉPERTOIRE",
                    help="répertoire contenant le profil et le sous-dossier _ENSEIGNANT "
                         "(réservé au jeu de tests synthétique)")
    ap.add_argument("--dry-run", action="store_true",
                    help="calcule et affiche sans écrire aucun fichier")
    ap.add_argument("--list-students", action="store_true",
                    help="affiche les identifiants disponibles et quitte")
    args = ap.parse_args(argv)

    if args.list_students:
        for st in core.all_students():
            print("%-24s %-10s %-8s %s" % (st["id"], st["level"],
                                           core.level_of(st)["subject"][:7], st["name"]))
        return 0
    if not args.student or not args.responses:
        ap.error("--student et --responses sont requis (ou utiliser --list-students)")
    try:
        student = find_student(args.student)
        responses = load(args.responses, "fichier de saisie")
        analysis = analyse(student, responses, base_dir=args.data_dir)
    except InputError as exc:
        print("ERREUR DE SAISIE : %s" % exc, file=sys.stderr)
        return 2

    plan = build_plan(student, analysis)
    facts = build_facts(student, analysis)

    print("Élève            : %s (%s, %s)" % (student["name"], analysis["level_key"], analysis["subject"]))
    print("Note             : %.2f / 20  (réussite %.0f %%)"
          % (analysis["score"]["note_sur_20"], 100 * analysis["score"]["success_rate"]))
    for p in ("A", "B", "C"):
        b = analysis["score"]["by_part"][p]
        print("  partie %s       : %.1f / %s" % (p, b["points"], b["max_points"]))
    print("Compétences P1   : %s" % ", ".join(x["skill_id"] for x in analysis["priorities"]
                                              if x["priority_rank"] == "P1") or "(aucune)")
    print("Écarts chiffrés  : 0 sur %d compétences (mesure initiale nominative indisponible)"
          % len(analysis["skills"]))
    print("Force de preuve  : %s"
          % ", ".join("%s %d" % (k, len([s for s in analysis["skills"] if s["evidence_strength"] == k]))
                      for k in ("forte", "moyenne", "faible")))
    for w in analysis["warnings"]:
        print("  AVERTISSEMENT : %s" % w)

    if args.dry_run:
        print("\n(--dry-run : aucun fichier écrit)")
        return 0
    outdir = args.outdir or os.path.dirname(os.path.abspath(args.responses))
    os.makedirs(outdir, exist_ok=True)
    for name, obj in (("post_stage_analysis.json", analysis),
                      ("four_week_action_plan.json", plan),
                      ("bilan_facts.json", facts)):
        p = os.path.join(outdir, name)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("écrit : %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
