#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analyseur post-distribution V3 : le script calcule, le modèle de langage interprète ensuite.

Ce que fait ce script, et rien d'autre :

    * il additionne les points saisis critère par critère ;
    * il sépare strictement la consolidation des acquis de l'année N-1 de la
      disponibilité sur les passerelles vers l'année N ;
    * il attache chaque code d'erreur au seul critère qui l'a produit ;
    * il mesure la force de la preuve disponible pour chaque compétence ;
    * il signale ce qui a été mesuré immédiatement après remédiation ;
    * il refuse toute progression chiffrée en l'absence de mesure initiale appariée.

Ce qu'il ne fait jamais : compléter une valeur manquante, convertir un statut
qualitatif en nombre, transformer une non-réussite sur une passerelle en déficit.

    python3 tools/analyze_s5_post_distribution.py --student elyes-kefi \\
        --responses responses/responses_elyes-kefi_2026-08-28.json
"""

import argparse
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd
import scope_rules

SCHEMA = "nexus-s5-post-distribution-analysis-v3"

# Aucune mesure initiale nominative item par item n'existe : le dossier ne conserve
# qu'un statut qualitatif par domaine. Convertir « fragile » en 1 et « maîtrisé » en 3
# pour en faire une différence produirait un écart sans valeur de mesure.
BASELINE_MEASURE_AVAILABLE = False
DELTA_BLOCKED_REASON = ("aucune mesure initiale nominative appariée : le dossier ne conserve "
                        "qu'un statut qualitatif par domaine, pas les réponses de l'élève "
                        "item par item")

MAX_P1 = 4

# Force de preuve : un décompte explicite de ce qui étaye la conclusion. Ce n'est pas
# une fiabilité psychométrique, et le mot « measurement_reliability » est proscrit :
# aucune étude de fiabilité n'a été conduite sur douze items.
EVIDENCE_RUBRIC = [
    ("au moins deux critères indépendants", lambda a: a["evidence_count"] >= 2, +1),
    ("au moins deux items distincts", lambda a: a["independent_items"] >= 2, +1),
    ("au moins deux points en jeu", lambda a: a["points_available"] >= 2.0, +1),
    ("au moins deux types de tâche différents", lambda a: a["task_diversity"] >= 2, +1),
    ("évaluée sur une tâche de transfert", lambda a: a["has_transfer"], +1),
    ("énoncé sans limite d'interprétation connue", lambda a: not a["limited_by_prompt"], +1),
    ("comparable au diagnostic initial", lambda a: a["comparable_to_baseline"], +1),
    ("mesurée moins d'une heure après sa remédiation", lambda a: a["immediate"], -1),
]


class InputError(Exception):
    pass


def _strength(score):
    if score <= 0:
        return "insufficient"
    if score <= 2:
        return "low"
    if score <= 4:
        return "moderate"
    return "strong"


def _n1_status(rate, strength):
    if strength == "insufficient":
        return "non_conclusif"
    if rate >= 0.85:
        return "acquis_observe"
    if rate >= 0.60:
        return "en_cours_de_consolidation"
    return "fragile"


def _bridge_status(rate, strength):
    if strength == "insufficient":
        return "no_conclusion"
    if rate >= 0.75:
        return "first_exposure"
    if rate >= 0.30:
        return "bridge_to_revisit"
    return "not_yet_installed"


N1_READING = {
    "acquis_observe": "acquis observé sur le sujet de clôture ; à confirmer dans la durée",
    "en_cours_de_consolidation": "consolidation engagée, non achevée",
    "fragile": "fragilité de prérequis actuellement documentée",
    "non_conclusif": "la copie ne contient pas assez d'éléments pour conclure",
}
BRIDGE_READING = {
    "first_exposure": "première confrontation réussie ; aisance intéressante à confirmer",
    "bridge_to_revisit": "notion découverte, à reprendre à la rentrée",
    "not_yet_installed": "notion nouvellement introduite, pas encore installée",
    "no_conclusion": "un seul élément de preuve : aucune conclusion n'est autorisée",
}


def load_inputs(student_id):
    students = {s["student_id"]: s for s in pd.students()}
    if student_id not in students:
        raise InputError("identifiant d'élève inconnu : %s. Identifiants : %s"
                         % (student_id, ", ".join(sorted(students))))
    st = students[student_id]
    overlay = pd.read_json(os.path.join(pd.V3_ROOT, "correction_overlays", student_id,
                                        "ANSWER_KEY_OVERLAY.json"), "overlay de correction")
    policy = pd.read_json(os.path.join(pd.V3_ROOT, "correction_overlays", student_id,
                                       "CORRECTION_POLICY.json"), "politique de correction")
    refs = pd.read_json(os.path.join(pd.V3_ROOT, "curriculum_scope",
                                     "curriculum_references.json"), "références curriculaires")
    return st, overlay, policy, refs, pd.manifest_of(st), pd.profile_of(st)


def flatten_overlay(overlay):
    """Toutes les lignes réellement notées : critères simples et sous-critères virtuels."""
    rows = {}
    for it in overlay["items"]:
        for c in it["criteria"]:
            if c["curriculum_scope"] == "mixed":
                for v in c["virtual_subcriteria"]:
                    rows[v["virtual_criterion_id"]] = {
                        "scoring_id": v["virtual_criterion_id"],
                        "criterion_id": c["criterion_id"], "virtual": True,
                        "item_ref": it["ref"], "item_id": it["item_id"], "part": it["part"],
                        "kind": it["kind"], "points": v["points"],
                        "analysis_skill_id": v["analysis_skill_id"],
                        "original_skill_id": c["original_skill_id"],
                        "curriculum_scope": v["curriculum_scope"],
                        "evidence_type": c["evidence_type"],
                        "evidence_quality": c["evidence_quality"],
                        "desc": v["desc"],
                        "error_codes_allowed": c["error_codes_allowed"],
                    }
            else:
                rows[c["criterion_id"]] = {
                    "scoring_id": c["criterion_id"], "criterion_id": c["criterion_id"],
                    "virtual": False,
                    "item_ref": it["ref"], "item_id": it["item_id"], "part": it["part"],
                    "kind": it["kind"], "points": c["original_points"],
                    "analysis_skill_id": c["analysis_skill_id"],
                    "original_skill_id": c["original_skill_id"],
                    "curriculum_scope": c["curriculum_scope"],
                    "evidence_type": c["evidence_type"],
                    "evidence_quality": c["evidence_quality"],
                    "desc": c["desc"],
                    "error_codes_allowed": c["error_codes_allowed"],
                }
    return rows


def read_scored_rows(responses, expected, error_codes):
    """Lit la saisie et refuse tout ce qui n'est pas explicite."""
    got = {}
    for item in responses.get("responses", []):
        for c in item.get("criteria", []):
            if c.get("curriculum_scope") == "mixed":
                subs = c.get("virtual_subcriteria") or []
                if not subs:
                    raise InputError("critère mixte %s : les sous-critères analytiques sont "
                                     "absents de la saisie" % c["criterion_id"])
                for v in subs:
                    got[v["virtual_criterion_id"]] = v
            else:
                got[c["criterion_id"]] = c
    missing = sorted(set(expected) - set(got))
    extra = sorted(set(got) - set(expected))
    if missing or extra:
        raise InputError("la saisie ne correspond pas au barème : manquants %s ; inconnus %s"
                         % (missing, extra))
    out = []
    for sid, ref in sorted(expected.items()):
        row = got[sid]
        status = row.get("criterion_scoring_status", "pending")
        if status == "requires_human_allocation":
            raise InputError(
                "critère %s : criterion_scoring_status = requires_human_allocation. La "
                "ventilation par critère doit être établie par un correcteur humain ; le script "
                "ne la devine pas." % sid)
        if status == "neutralised":
            out.append(dict(ref, score=None, neutralised=True, error_codes=[],
                            observation=row.get("observation"),
                            accepted_alternative_method=bool(
                                row.get("accepted_alternative_method")),
                            scoring_status=status))
            continue
        score = row.get("score")
        if score is None:
            raise InputError("critère %s : aucun score saisi. Le script ne complète jamais une "
                             "valeur manquante." % sid)
        try:
            score = float(score)
        except (TypeError, ValueError):
            raise InputError("critère %s : score non numérique (%r)" % (sid, score))
        if score < 0 or score > ref["points"] + 1e-9:
            raise InputError("critère %s : score %s hors de l'intervalle [0 ; %s]"
                             % (sid, score, ref["points"]))
        codes = list(row.get("error_codes") or [])
        for code in codes:
            if code not in error_codes:
                raise InputError("critère %s : code d'erreur inconnu %r" % (sid, code))
        if codes and score >= ref["points"] - 1e-9:
            raise InputError(
                "critère %s : des codes d'erreur sont portés alors que le critère est "
                "intégralement réussi. Un code d'erreur appartient au critère effectivement "
                "échoué." % sid)
        out.append(dict(ref, score=score, neutralised=False, error_codes=codes,
                        observation=row.get("observation"),
                        accepted_alternative_method=bool(row.get("accepted_alternative_method")),
                        scoring_status="scored"))
    return out


def analyse(student_id, responses):
    st, overlay, policy, refs, manifest, profile = load_inputs(student_id)
    if responses.get("student_id") != student_id:
        raise InputError("le fichier de saisie porte student_id=%r alors que l'élève demandé est "
                         "%r" % (responses.get("student_id"), student_id))
    sys.path.insert(0, pd.S5_TOOLS)
    from data import common
    from data.levels import LEVELS
    level = LEVELS[st["level_key"]]

    expected = flatten_overlay(overlay)
    rows = read_scored_rows(responses, expected, common.ERROR_CODES)
    items = {i["ref"]: i for i in manifest["items"]}

    scored = [r for r in rows if not r["neutralised"]]
    neutralised = [r for r in rows if r["neutralised"]]

    total = round(sum(r["score"] for r in scored), 4)
    max_scored = round(sum(r["points"] for r in scored), 4)
    max_printed = round(sum(i["points"] for i in manifest["items"]), 4)

    def pool(scope):
        sel = [r for r in scored if r["curriculum_scope"] == scope]
        earned = round(sum(r["score"] for r in sel), 4)
        avail = round(sum(r["points"] for r in sel), 4)
        return {"earned": earned, "available": avail,
                "percentage": round(100.0 * earned / avail, 2) if avail else None,
                "criteria": len(sel)}

    n1, bridge = pool("n_minus_1"), pool("bridge_n")

    # ------------------------------------------------- agrégation par compétence
    acc = {}
    for r in scored:
        a = acc.setdefault((r["analysis_skill_id"], r["curriculum_scope"]), {
            "analysis_skill_id": r["analysis_skill_id"],
            "curriculum_scope": r["curriculum_scope"],
            "original_skill_ids": set(), "criteria": [], "items": set(),
            "evidence_types": set(), "task_types": set(),
            "earned": 0.0, "available": 0.0,
            "has_transfer": False, "limited_by_prompt": False,
            "errors": [], "alternative_methods": 0,
        })
        a["original_skill_ids"].add(r["original_skill_id"])
        a["criteria"].append(r["scoring_id"])
        a["items"].add(r["item_ref"])
        a["evidence_types"].add(r["evidence_type"])
        a["task_types"].add(items[r["item_ref"]]["task_type"])
        a["earned"] += r["score"]
        a["available"] += r["points"]
        if items[r["item_ref"]]["difficulty"] == "transfert" and r["points"]:
            a["has_transfer"] = a["has_transfer"] or (r["score"] / r["points"] >= 0.75)
        if r["evidence_quality"] == "limited_by_prompt":
            a["limited_by_prompt"] = True
        if r["accepted_alternative_method"]:
            a["alternative_methods"] += 1
        for code in r["error_codes"]:
            a["errors"].append({"code": code, "criterion_id": r["scoring_id"],
                                "item_ref": r["item_ref"]})

    baseline = {row["skill_id"]: row for row in profile["baseline"]["skills"]}
    skills = []
    for key in sorted(acc):
        a = acc[key]
        rate = a["earned"] / a["available"] if a["available"] else 0.0
        origins = sorted(a["original_skill_ids"])
        ret = {}
        for ref in sorted(a["items"]):
            for sid in origins:
                r = (items[ref].get("retention") or {}).get(sid)
                if r:
                    ret = r
                    break
            if ret:
                break
        statuses = {items[ref]["comparison_status"] for ref in a["items"]}
        comparable = ("indicative_skill_comparison" in statuses
                      and a["curriculum_scope"] == "n_minus_1")
        ev = {
            "evidence_count": len(a["criteria"]),
            "independent_items": len(a["items"]),
            "points_available": round(a["available"], 3),
            "task_diversity": len(a["evidence_types"] | a["task_types"]),
            "has_transfer": a["has_transfer"],
            "limited_by_prompt": a["limited_by_prompt"],
            "comparable_to_baseline": comparable,
            "immediate": bool(ret.get("recommended_delayed_check")),
        }
        pts, detail = 0, []
        for label, test, weight in EVIDENCE_RUBRIC:
            ok = bool(test(ev))
            if ok:
                pts += weight
            detail.append({"critere": label, "verifie": ok, "poids": weight})
        strength = _strength(pts)
        if a["curriculum_scope"] == "bridge_n":
            status = _bridge_status(rate, strength)
            reading = BRIDGE_READING[status]
        else:
            status = _n1_status(rate, strength)
            reading = N1_READING[status]
        label = None
        for sid in origins:
            if sid in level["skills"]:
                label = level["skills"][sid]["label"]
                break
        alias_label = None
        for (skey, ref_, rank), exc in scope_rules.EXCEPTIONS.items():
            if exc.get("analysis_skill_id") == a["analysis_skill_id"]:
                alias_label = exc.get("analysis_skill_label")
                break
            for v in exc.get("virtual", []):
                if v.get("analysis_skill_id") == a["analysis_skill_id"]:
                    alias_label = v.get("analysis_skill_label")
        importance = next((level["skills"][s]["importance_n"] for s in origins
                           if s in level["skills"]), "importante")
        skills.append({
            "analysis_skill_id": a["analysis_skill_id"],
            "label": alias_label or label,
            "original_skill_ids": origins,
            "is_analysis_alias": a["analysis_skill_id"] not in level["skills"],
            "domain": next((level["skills"][s]["domain"] for s in origins
                            if s in level["skills"]), None),
            "importance_n": importance,
            "curriculum_scope": a["curriculum_scope"],
            "score": {"earned": round(a["earned"], 3), "available": round(a["available"], 3),
                      "success_rate": round(rate, 4)},
            "items": sorted(a["items"]),
            "criteria": sorted(a["criteria"]),
            "evidence_types": sorted(a["evidence_types"]),
            "evidence": ev,
            "evidence_strength": strength,
            "evidence_strength_score": pts,
            "evidence_strength_detail": detail,
            "error_codes": [e["code"] for e in a["errors"]],
            "errors": a["errors"],
            "accepted_alternative_methods": a["alternative_methods"],
            "baseline_status_qualitative": (baseline.get(origins[0], {})
                                            .get("statut_avant_s5")),
            "baseline_measure_available": BASELINE_MEASURE_AVAILABLE,
            "mastery_delta": None,
            "delta_blocked_reason": DELTA_BLOCKED_REASON,
            "post_test_context": ret.get("post_test_context"),
            "retention_status": ret.get("retention_status"),
            "recommended_delayed_check": bool(ret.get("recommended_delayed_check")),
            "retention_reason": ret.get("reason"),
            "interpretation": {
                "status": status,
                "reading": reading,
                "authorised_wording": _wording(a["curriculum_scope"], status, strength,
                                               ev["immediate"]),
                "forbidden_wording": _forbidden(a["curriculum_scope"]),
                "evidence_quality": ("limited_by_prompt" if a["limited_by_prompt"]
                                     else "standard"),
            },
        })

    # ------------------------------------------------------- profil d'erreurs
    def err_profile(scope):
        counts = {}
        for s in skills:
            if s["curriculum_scope"] != scope:
                continue
            for e in s["errors"]:
                counts[e["code"]] = counts.get(e["code"], 0) + 1
        return counts

    err_n1, err_br = err_profile("n_minus_1"), err_profile("bridge_n")
    error_profile = {
        "attribution": "au critère effectivement échoué ; aucune propagation à l'item ni aux "
                       "autres compétences",
        "n_minus_1": err_n1,
        "bridge_n": err_br,
        "dominant_codes_n_minus_1": [c for c, _ in sorted(err_n1.items(), key=lambda kv: -kv[1])[:3]],
        "by_criterion": [{"criterion_id": r["scoring_id"], "item_ref": r["item_ref"],
                          "analysis_skill_id": r["analysis_skill_id"],
                          "curriculum_scope": r["curriculum_scope"],
                          "error_codes": r["error_codes"]}
                         for r in scored if r["error_codes"]],
    }

    priorities = _priorities(skills)
    delayed = _delayed_checks(skills)
    retention = {
        "principe": ("une réussite obtenue moins d'une heure après la remédiation de la même "
                     "compétence mesure une performance immédiate, pas une consolidation "
                     "durable."),
        "skills": [{"analysis_skill_id": s["analysis_skill_id"],
                    "post_test_context": s["post_test_context"],
                    "retention_status": s["retention_status"],
                    "recommended_delayed_check": s["recommended_delayed_check"]}
                   for s in skills if s["recommended_delayed_check"]],
    }

    probes = [i for i in manifest["items"] if i.get("confidence_probe")]
    conf_in = {r["ref"]: r.get("confidence") for r in responses.get("responses", [])}
    saisies = [conf_in.get(p["ref"]) for p in probes if conf_in.get(p["ref"]) is not None]
    for c in saisies:
        if c not in (1, 2, 3, 4):
            raise InputError("certitude %r hors de l'échelle 1-4" % c)

    warnings = _warnings(skills, neutralised, saisies, probes, n1, bridge)
    observed = responses.get("observed_duration_minutes")

    return {
        "schema": SCHEMA,
        "generated_on": pd.GENERATED_ON,
        "student_id": student_id,
        "student_name": st["student_name"],
        "level_key": st["level_key"],
        "level_label": st["level_label"],
        "subject": st["subject"],
        "analysed_on": responses.get("assessed_on"),
        "status": "analysed",
        "scoring_model": "par critère ; un critère porte une compétence et un seul classement "
                         "curriculaire",
        "curriculum_references": refs["levels"][st["level_key"]],
        "student_artifacts_modified": 0,
        "baseline_measure_available": BASELINE_MEASURE_AVAILABLE,
        "raw_assessment_score": {
            "label": "score brut au sujet de clôture",
            "score": total,
            "max": max_printed,
            "scored_max": max_scored,
            "note_sur_20": round(20.0 * total / max_scored, 2) if max_scored else None,
            "avertissement": ("ce score n'est ni un score de consolidation, ni une progression, "
                              "ni un niveau N-1 : le sujet contient aussi des éléments de "
                              "passerelle vers l'année suivante."),
            "neutralised_points": round(max_printed - max_scored, 4),
        },
        "n_minus_1_consolidation": n1,
        "bridge_n_readiness": dict(
            bridge,
            nature=("disponibilité et préparation à l'entrée dans la notion ; ce n'est pas une "
                    "mesure d'acquisition attendue")),
        "criteria": [{
            "criterion_id": r["criterion_id"], "scoring_id": r["scoring_id"],
            "virtual": r["virtual"], "item_ref": r["item_ref"], "item_id": r["item_id"],
            "analysis_skill_id": r["analysis_skill_id"],
            "original_skill_id": r["original_skill_id"],
            "curriculum_scope": r["curriculum_scope"], "evidence_type": r["evidence_type"],
            "score": r["score"], "max_score": r["points"],
            "error_codes": r["error_codes"], "observation": r["observation"],
            "accepted_alternative_method": r["accepted_alternative_method"],
            "scoring_status": r["scoring_status"],
            "evidence_quality": r["evidence_quality"],
        } for r in rows],
        "skills": skills,
        "error_profile": error_profile,
        "retention": retention,
        "delayed_checks": delayed,
        "action_plan_inputs": {
            "n_minus_1_priorities": [p for p in priorities if p["family"] == "n_minus_1"],
            "bridge_actions": [p for p in priorities if p["family"] == "bridge_n"],
            "regle": ("un échec sur une passerelle ne produit jamais de P1 ni de P2 : il ne peut "
                      "produire que BRIDGE_REVISIT ou DISCOVERY_TO_CONTINUE."),
        },
        "confidence": {
            "probes": [p["ref"] for p in probes],
            "entered": len(saisies),
            "mean": round(sum(saisies) / len(saisies), 2) if saisies else None,
            "note": "la certitude n'entre pas dans le score.",
        },
        "timing": {
            "estimated_duration_minutes": responses.get("estimated_duration_minutes"),
            "observed_duration_minutes": observed,
            "note": ("les deux estimateurs internes du modèle de durée partagent leurs entrées : "
                     "ils ne constituent pas deux mesures indépendantes."),
        },
        "neutralised_criteria": [{"criterion_id": r["criterion_id"],
                                  "scoring_id": r["scoring_id"],
                                  "points": r["points"],
                                  "raison": r["observation"]} for r in neutralised],
        "warnings": warnings,
    }


def _wording(scope, status, strength, immediate):
    if scope == "bridge_n":
        base = {
            "first_exposure": "l'élève a montré une première aisance sur cette notion, "
                              "nouvellement introduite",
            "bridge_to_revisit": "cette notion, nouvellement introduite, sera reprise pendant "
                                 "la rentrée",
            "not_yet_installed": "cette notion vient d'être découverte ; elle n'est pas encore "
                                 "installée, ce qui est attendu à ce stade",
            "no_conclusion": "un seul élément de preuve : rien ne peut être conclu",
        }[status]
        return [base, "aucun jugement d'acquisition n'est autorisé sur cette notion"]
    out = {
        "acquis_observe": ["réussite actuelle observée sur le sujet de clôture"],
        "en_cours_de_consolidation": ["consolidation engagée, non achevée"],
        "fragile": ["fragilité de prérequis actuellement documentée"],
        "non_conclusif": ["résultat final non comparable ; compétence à vérifier dans la durée"],
    }[status]
    if immediate:
        out.append("réussite immédiate après remédiation : la rétention reste à vérifier")
    if strength in ("insufficient", "low"):
        out.append("preuve faible : cette lecture ne peut pas fonder une conclusion isolée")
    return out


def _forbidden(scope):
    common_ = ["progression de X %", "a progressé de X niveaux",
               "maîtrise désormais, sur une seule preuve faible",
               "consolidation durable après une remédiation immédiate",
               "niveau insuffisant, sur la seule note brute sur 20"]
    if scope == "bridge_n":
        return common_ + ["non acquis", "lacune", "compétence non acquise",
                          "fragile", "priorité de remédiation"]
    return common_


def _priorities(skills):
    graded = []
    for s in skills:
        if s["curriculum_scope"] == "bridge_n":
            rank = ("DISCOVERY_TO_CONTINUE" if s["interpretation"]["status"] == "first_exposure"
                    else "BRIDGE_REVISIT")
            graded.append({
                "family": "bridge_n", "analysis_skill_id": s["analysis_skill_id"],
                "label": s["label"], "action": rank,
                "reason": "notion introduite pendant la séance 5 : %s"
                          % s["interpretation"]["reading"],
                "success_rate": s["score"]["success_rate"],
                "evidence_strength": s["evidence_strength"],
                "interdiction": "ne peut produire ni P1, ni P2, ni « non acquis »",
            })
            continue
        crit = s["importance_n"] == "critique"
        status = s["interpretation"]["status"]
        if status == "acquis_observe":
            rank = "OK"
        elif status == "fragile":
            rank = "P1" if crit else "P2"
        elif status == "en_cours_de_consolidation":
            rank = "P2" if crit else "P3"
        else:
            rank = "P3"
        graded.append({
            "family": "n_minus_1", "analysis_skill_id": s["analysis_skill_id"],
            "label": s["label"], "priority_rank": rank,
            "reason": "%s ; taux de réussite %.0f %% ; compétence %s pour l'entrée dans l'année ; "
                      "force de preuve %s"
                      % (s["interpretation"]["reading"], 100 * s["score"]["success_rate"],
                         s["importance_n"], s["evidence_strength"]),
            "success_rate": s["score"]["success_rate"],
            "importance_n": s["importance_n"],
            "evidence_strength": s["evidence_strength"],
            "dominant_error_codes": _top(s["error_codes"]),
        })
    p1 = [g for g in graded if g.get("priority_rank") == "P1"]
    if len(p1) > MAX_P1:
        p1.sort(key=lambda g: (g["importance_n"] != "critique", g["success_rate"]))
        for g in p1[MAX_P1:]:
            g["priority_rank"] = "P2"
            g["reason"] += " ; rétrogradée en P2 pour conserver un plan de rentrée réaliste"
    order = {"P1": 0, "P2": 1, "P3": 2, "OK": 3}
    graded.sort(key=lambda g: (g["family"] != "n_minus_1",
                               order.get(g.get("priority_rank"), 9), g["success_rate"]))
    return graded


def _top(codes):
    counts = {}
    for c in codes:
        counts[c] = counts.get(c, 0) + 1
    return [c for c, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:2]]


def _delayed_checks(skills):
    sel = [s for s in skills if s["recommended_delayed_check"]]
    return {
        "semaine": 2,
        "obligatoire": bool(sel),
        "objet": ("vérifier que les réussites obtenues immédiatement après remédiation se sont "
                  "maintenues à distance"),
        "format": ("mini-test de 10 minutes, deux items par compétence, items parallèles à ceux "
                   "de l'évaluation de clôture"),
        "critere": "réussite maintenue sans aide sur au moins un item par compétence",
        "skills": [{"analysis_skill_id": s["analysis_skill_id"], "label": s["label"],
                    "curriculum_scope": s["curriculum_scope"],
                    "success_rate": s["score"]["success_rate"],
                    "raison": s["retention_reason"]} for s in sel],
    }


def _warnings(skills, neutralised, saisies, probes, n1, bridge):
    w = ["aucun écart de maîtrise n'est calculé : " + DELTA_BLOCKED_REASON + ".",
         "le score brut sur 20 n'est pas un diagnostic de consolidation N-1 : %.2f point(s) "
         "relèvent d'une passerelle vers l'année suivante." % bridge["available"]]
    if not bridge["available"]:
        w[-1] = ("aucun critère de passerelle dans ce sujet : le score brut porte intégralement "
                 "sur des acquis de l'année N-1, ce qui reste distinct d'un diagnostic complet.")
    faibles = [s["analysis_skill_id"] for s in skills
               if s["evidence_strength"] in ("insufficient", "low")]
    if faibles:
        w.append("force de preuve faible ou insuffisante pour : %s. Ces lectures ne peuvent pas "
                 "fonder une conclusion isolée." % ", ".join(faibles))
    imm = [s["analysis_skill_id"] for s in skills if s["recommended_delayed_check"]]
    if imm:
        w.append("compétences évaluées moins d'une heure après leur remédiation : %s. Un contrôle "
                 "différé en semaine 2 est nécessaire avant toute affirmation de consolidation "
                 "durable." % ", ".join(imm))
    lim = [s["analysis_skill_id"] for s in skills
           if s["interpretation"]["evidence_quality"] == "limited_by_prompt"]
    if lim:
        w.append("énoncé à interprétation limitée pour : %s. La formulation ne soutient pas une "
                 "inférence forte." % ", ".join(lim))
    if neutralised:
        w.append("%d critère(s) neutralisé(s) faute de correction équitable possible ; ils sont "
                 "retirés des deux décomptes." % len(neutralised))
    if len(saisies) < len(probes):
        w.append("certitude saisie sur %d des %d items pivots seulement."
                 % (len(saisies), len(probes)))
    return w


# ------------------------------------------------------- plan et faits du bilan
def build_plan(analysis):
    p = analysis["action_plan_inputs"]["n_minus_1_priorities"]
    pool = [x for x in p if x["priority_rank"] in ("P1", "P2", "P3")]
    weeks, cursor = [], 0
    for n in (1, 2, 3, 4):
        take = pool[cursor:cursor + (2 if n < 4 else 3)]
        cursor += len(take)
        weeks.append({
            "week": n,
            "family": "consolidation_n_minus_1",
            "skills": [t["analysis_skill_id"] for t in take],
            "labels": [t["label"] for t in take],
            "objective": ("consolider : " + " ; ".join(t["label"] for t in take)) if take
                         else "aucune priorité N-1 restante : réinvestissement libre",
            "work_type": ("reprise guidée puis exercices gradués" if n <= 2
                          else "réactivation espacée et problème mixte"),
            "duration_minutes": 15 if n <= 2 else 20,
            "success_criterion": "trois réussites consécutives sans aide, chacune assortie du "
                                 "contrôle écrit",
            "derived_from": take,
        })
    return {
        "schema": "nexus-s5-four-week-plan-v3",
        "generated_on": pd.GENERATED_ON,
        "student_id": analysis["student_id"],
        "level_key": analysis["level_key"],
        "source": "post_stage_analysis_v3.json",
        "progression_chiffree_possible": False,
        "progression_chiffree_raison": DELTA_BLOCKED_REASON,
        "consolidation_n_minus_1": weeks,
        "bridge_n_actions": [{
            "analysis_skill_id": b["analysis_skill_id"], "label": b["label"],
            "action": b["action"],
            "quand": "à la reprise du chapitre correspondant, en classe",
            "regle": "cette ligne n'est pas une remédiation : la notion n'a pas encore été "
                     "enseignée en classe.",
        } for b in analysis["action_plan_inputs"]["bridge_actions"]],
        "delayed_retention_check": analysis["delayed_checks"],
        "warnings": analysis["warnings"],
    }


def build_facts(analysis):
    sk = analysis["skills"]
    n1 = [s for s in sk if s["curriculum_scope"] == "n_minus_1"]
    br = [s for s in sk if s["curriculum_scope"] == "bridge_n"]
    return {
        "schema": "nexus-s5-bilan-facts-v3",
        "generated_on": pd.GENERATED_ON,
        "student_id": analysis["student_id"],
        "student_name": analysis["student_name"],
        "level": analysis["level_label"],
        "subject": analysis["subject"],
        "raw_assessment_score": analysis["raw_assessment_score"],
        "n_minus_1_consolidation": analysis["n_minus_1_consolidation"],
        "bridge_n_readiness": analysis["bridge_n_readiness"],
        "progression_chiffree_possible": False,
        "progression_chiffree_raison": DELTA_BLOCKED_REASON,
        "acquis_n_minus_1_observes": [
            {"analysis_skill_id": s["analysis_skill_id"], "label": s["label"],
             "evidence_strength": s["evidence_strength"],
             "a_confirmer_a_distance": s["recommended_delayed_check"]}
            for s in n1 if s["interpretation"]["status"] == "acquis_observe"],
        "points_n_minus_1_a_consolider": [
            {"analysis_skill_id": s["analysis_skill_id"], "label": s["label"],
             "status": s["interpretation"]["status"],
             "evidence_strength": s["evidence_strength"]}
            for s in n1 if s["interpretation"]["status"] in ("fragile",
                                                            "en_cours_de_consolidation")],
        "premieres_passerelles": [
            {"analysis_skill_id": s["analysis_skill_id"], "label": s["label"],
             "status": s["interpretation"]["status"],
             "phrase_autorisee": s["interpretation"]["authorised_wording"][0]}
            for s in br],
        "reussites_immediates_a_confirmer": [
            s["analysis_skill_id"] for s in sk
            if s["recommended_delayed_check"] and s["score"]["success_rate"] >= 0.75],
        "comparaison_initiale_qualitative": [
            {"analysis_skill_id": s["analysis_skill_id"],
             "statut_initial_qualitatif": s["baseline_status_qualitative"],
             "lecture_autorisee": "confrontation indicative entre un statut de domaine et une "
                                  "performance finale ; aucun écart chiffré"}
            for s in n1 if s["baseline_status_qualitative"]],
        "profil_erreurs": analysis["error_profile"],
        "controle_differe": analysis["delayed_checks"],
        "formulations_interdites": [
            "progression de X %", "a progressé de X niveaux",
            "maîtrise désormais (sur une seule preuve faible)",
            "non acquis (sur une notion de passerelle)",
            "lacune (sur une notion jamais enseignée)",
            "consolidation durable (après une remédiation immédiate)",
            "niveau insuffisant (sur la seule note brute sur 20)",
        ],
        "usage": ("toute phrase chiffrée du bilan doit renvoyer à une clé de ce fichier. Le "
                  "modèle de langage rédige ; il ne recalcule ni ne corrige aucun score."),
        "warnings": analysis["warnings"],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(prog="analyze_s5_post_distribution.py",
                                 description=__doc__.splitlines()[0])
    ap.add_argument("--student", required=True, metavar="ID")
    ap.add_argument("--responses", required=True, metavar="FICHIER")
    ap.add_argument("--outdir", metavar="RÉPERTOIRE",
                    help="par défaut : S5_post_distribution_v3/analysis/<student_id>/")
    ap.add_argument("--dry-run", action="store_true", help="n'écrit rien")
    args = ap.parse_args(argv)
    try:
        responses = pd.read_json(args.responses, "fichier de saisie")
        analysis = analyse(args.student, responses)
    except (InputError, pd.PostDistributionError) as exc:
        print("SAISIE REFUSÉE : %s" % exc, file=sys.stderr)
        return 2
    plan = build_plan(analysis)
    facts = build_facts(analysis)
    print("%s — score brut au sujet de clôture : %.2f / %.0f"
          % (analysis["student_name"], analysis["raw_assessment_score"]["score"],
             analysis["raw_assessment_score"]["max"]))
    print("  consolidation N-1  : %.2f / %.2f (%s %%)"
          % (analysis["n_minus_1_consolidation"]["earned"],
             analysis["n_minus_1_consolidation"]["available"],
             analysis["n_minus_1_consolidation"]["percentage"]))
    print("  passerelles vers N : %.2f / %.2f (%s %%)"
          % (analysis["bridge_n_readiness"]["earned"],
             analysis["bridge_n_readiness"]["available"],
             analysis["bridge_n_readiness"]["percentage"]))
    for w in analysis["warnings"]:
        print("  ! %s" % w)
    if args.dry_run:
        return 0
    out = args.outdir or os.path.join(pd.V3_ROOT, "analysis", args.student)
    pd.write_json(os.path.join(out, "post_stage_analysis_v3.json"), analysis)
    pd.write_json(os.path.join(out, "four_week_action_plan_v3.json"), plan)
    pd.write_json(os.path.join(out, "bilan_facts_v3.json"), facts)
    print("écrit dans %s" % os.path.relpath(out, pd.REPO_ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
