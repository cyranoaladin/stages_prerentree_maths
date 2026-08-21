# -*- coding: utf-8 -*-
"""Analyse déterministe d'une correction validée.

Tout ce qui est chiffré ici est calculé par ce module. Aucun modèle de langage
n'intervient : ni pour les points, ni pour la note, ni pour la ventilation N−1 /
passerelle, ni pour les codes d'erreur, ni pour la force de preuve, ni pour les
priorités.

Trois refus structurent le calcul :

* aucun écart de maîtrise n'est produit — les réponses initiales item par item
  n'existent pas, et convertir « fragile » en 1 pour en soustraire un 3 fabriquerait une
  mesure ;
* un critère de passerelle ne contribue jamais à la consolidation N−1, et son échec ne
  produit ni fragilité, ni priorité de remédiation ;
* un code d'erreur reste attaché au critère qui l'a produit et ne se propage nulle part.
"""

import json
from decimal import Decimal

from ..models import BaselineStatus, SkillReference
from ..security import sha256_text
from . import correction as corr
from . import evidence, points

BASELINE_MEASURE_AVAILABLE = False
DELTA_BLOCKED_REASON = (
    "Les réponses initiales item par item n'étant pas disponibles, aucune progression "
    "chiffrée pré-test/post-test n'est calculée.")

# Statuts pédagogiques des acquis de l'année N−1.
N1_STATUSES = ("SOLIDE", "SATISFAISANT", "A_CONSOLIDER", "PRIORITAIRE", "A_CONFIRMER",
               "PREUVE_INSUFFISANTE")
N1_LABELS = {
    "SOLIDE": "Solide",
    "SATISFAISANT": "Satisfaisant",
    "A_CONSOLIDER": "À consolider",
    "PRIORITAIRE": "Prioritaire",
    "A_CONFIRMER": "À confirmer à distance",
    "PREUVE_INSUFFISANTE": "Preuve insuffisante",
}
N1_READING = {
    "SOLIDE": "réussite actuelle observée, étayée par plusieurs éléments",
    "SATISFAISANT": "réussite actuelle observée, à consolider dans la durée",
    "A_CONSOLIDER": "consolidation engagée, non achevée",
    "PRIORITAIRE": "fragilité de prérequis actuellement documentée",
    "A_CONFIRMER": "réussite immédiate après remédiation ; la rétention reste à vérifier",
    "PREUVE_INSUFFISANTE": "la copie ne contient pas assez d'éléments pour conclure",
}

# Statuts des passerelles vers l'année N. Aucun terme de déficit n'y figure : on ne peut
# pas manquer ce qui n'a pas encore été enseigné.
BRIDGE_STATUSES = ("PROMISING", "FIRST_EXPOSURE", "BRIDGE_REVISIT", "DISCOVERY_TO_CONTINUE",
                   "NO_CONCLUSION")
BRIDGE_LABELS = {
    "PROMISING": "Aisance prometteuse",
    "FIRST_EXPOSURE": "Première confrontation réussie",
    "BRIDGE_REVISIT": "À reprendre à la rentrée",
    "DISCOVERY_TO_CONTINUE": "Découverte à poursuivre",
    "NO_CONCLUSION": "Aucune conclusion possible",
}
BRIDGE_READING = {
    "PROMISING": "l'élève a montré une aisance nette sur cette notion, nouvellement introduite",
    "FIRST_EXPOSURE": "l'élève a montré une première aisance sur cette notion, nouvellement "
                      "introduite",
    "BRIDGE_REVISIT": "cette notion, nouvellement introduite, sera reprise pendant la rentrée",
    "DISCOVERY_TO_CONTINUE": "cette notion vient d'être découverte ; elle n'est pas encore "
                             "installée, ce qui est attendu à ce stade",
    "NO_CONCLUSION": "trop peu d'éléments : rien ne peut être conclu sur cette notion",
}
BRIDGE_ACTIONS = {
    "PROMISING": "DISCOVERY_TO_CONTINUE",
    "FIRST_EXPOSURE": "DISCOVERY_TO_CONTINUE",
    "BRIDGE_REVISIT": "BRIDGE_REVISIT",
    "DISCOVERY_TO_CONTINUE": "BRIDGE_REVISIT",
    "NO_CONCLUSION": "BRIDGE_REVISIT",
}

MAX_P1 = 4
FORBIDDEN_ON_BRIDGE = ("fragile", "non acquis", "lacune", "prioritaire", "P1", "P2")


def _rate(earned: int, available: int) -> Decimal:
    if not available:
        return Decimal("0")
    return (Decimal(earned) / Decimal(available)).quantize(Decimal("0.0001"))


def n1_status(rate: Decimal, strength: str, immediate: bool) -> str:
    """Règle publiée. Un score élevé sur une preuve faible ne donne jamais SOLIDE."""
    if strength == "INSUFFICIENT":
        return "PREUVE_INSUFFISANTE"
    if rate >= Decimal("0.85"):
        if immediate:
            return "A_CONFIRMER"
        return "SOLIDE" if evidence.at_least(strength, "MODERATE") else "SATISFAISANT"
    if rate >= Decimal("0.60"):
        return "SATISFAISANT" if evidence.at_least(strength, "MODERATE") else "A_CONSOLIDER"
    if rate >= Decimal("0.40"):
        return "A_CONSOLIDER"
    return "PRIORITAIRE"


def bridge_status(rate: Decimal, strength: str) -> str:
    if strength == "INSUFFICIENT":
        return "NO_CONCLUSION"
    if rate >= Decimal("0.85"):
        return "PROMISING"
    if rate >= Decimal("0.60"):
        return "FIRST_EXPOSURE"
    if rate >= Decimal("0.25"):
        return "BRIDGE_REVISIT"
    return "DISCOVERY_TO_CONTINUE"


def _priority(status: str, importance: str) -> str:
    critical = importance == "critique"
    if status == "PRIORITAIRE":
        return "P1" if critical else "P2"
    if status == "A_CONSOLIDER":
        return "P2" if critical else "P3"
    if status == "SATISFAISANT":
        return "P3" if critical else "OK"
    if status == "PREUVE_INSUFFISANTE":
        return "P3"
    return "OK"          # SOLIDE, A_CONFIRMER


def _skill_reference(session, level_key, analysis_skill_id):
    return session.query(SkillReference).filter_by(
        level_key=level_key, analysis_skill_id=analysis_skill_id).one_or_none()


def analyse(session, correction, assessment) -> dict:
    """Produit l'analyse complète. La correction doit être cohérente : la validation
    est passée avant."""
    student = assessment.student
    rows = {r.scoring_id: r for r in correction.responses}
    meta = {m["scoring_id"]: m for m in corr.scoring_rows(assessment)}
    items = {i.item_id: i for i in assessment.items}
    criteria = {c.criterion_id: c for i in assessment.items for c in i.criteria}
    virtuals = {v.virtual_criterion_id: v for i in assessment.items for c in i.criteria
                for v in c.virtual_parts}
    baselines = {b.skill_id: b for b in session.query(BaselineStatus).filter_by(
        student_id=student.student_id).all()}

    scored, neutralised, detail = [], [], []
    for scoring_id, row in rows.items():
        m = meta.get(scoring_id)
        if m is None:
            continue
        crit = criteria[m["criterion_id"]]
        virt = virtuals.get(scoring_id)
        item = items[m["item_id"]]
        retention = json.loads(crit.retention_json) if crit.retention_json else {}
        entry = {
            "scoring_id": scoring_id, "criterion_id": m["criterion_id"],
            "is_virtual": bool(virt), "item_ref": item.ref, "item_id": item.item_id,
            "description": m["description"],
            "analysis_skill_id": m["analysis_skill_id"],
            "original_skill_id": crit.original_skill_id,
            "curriculum_scope": m["curriculum_scope"],
            "evidence_type": crit.evidence_type,
            "evidence_quality": crit.evidence_quality,
            "score_centi": row.score_centi, "max_score_centi": row.max_score_centi,
            "error_codes": json.loads(row.error_codes_json or "[]"),
            "observation": row.observation,
            "accepted_alternative_method": bool(row.accepted_alternative_method),
            "scoring_status": row.scoring_status,
            "comparison_status": item.comparison_status,
            "retention": retention,
            "is_transfer_task": (item.kind is not None
                                 and (crit.evidence_type == "transfert")),
        }
        detail.append(entry)
        if row.scoring_status == "NEUTRALISED":
            neutralised.append(entry)
        elif row.scoring_status != "PENDING":
            scored.append(entry)

    raw_centi = sum(e["score_centi"] or 0 for e in scored)
    scored_max_centi = sum(e["max_score_centi"] for e in scored)
    printed_max_centi = assessment.max_points_centi

    def pool(scope):
        sel = [e for e in scored if e["curriculum_scope"] == scope]
        earned = sum(e["score_centi"] or 0 for e in sel)
        available = sum(e["max_score_centi"] for e in sel)
        return {"earned_centi": earned, "available_centi": available,
                "earned": points.format_fr(earned), "available": points.format_fr(available),
                "percentage": (float(points.percentage(earned, available))
                               if available else None),
                "criteria": len(sel)}

    n1_pool, bridge_pool = pool("n_minus_1"), pool("bridge_n")

    # ------------------------------------------------------ agrégation par compétence
    buckets = {}
    for e in scored:
        key = (e["analysis_skill_id"], e["curriculum_scope"])
        b = buckets.setdefault(key, {
            "analysis_skill_id": e["analysis_skill_id"],
            "curriculum_scope": e["curriculum_scope"],
            "original_skill_ids": set(), "criteria": [], "items": set(),
            "evidence_types": set(), "earned": 0, "available": 0,
            "has_transfer": False, "limited_by_prompt": False, "immediate": False,
            "comparable": False, "errors": [], "alternatives": 0, "retention": {},
        })
        b["original_skill_ids"].add(e["original_skill_id"])
        b["criteria"].append(e["scoring_id"])
        b["items"].add(e["item_ref"])
        b["evidence_types"].add(e["evidence_type"])
        b["earned"] += e["score_centi"] or 0
        b["available"] += e["max_score_centi"]
        if e["evidence_type"] == "transfert" and e["max_score_centi"]:
            if Decimal(e["score_centi"] or 0) / Decimal(e["max_score_centi"]) >= Decimal("0.75"):
                b["has_transfer"] = True
        if e["evidence_quality"] == "limited_by_prompt":
            b["limited_by_prompt"] = True
        if e["retention"].get("recommended_delayed_check"):
            b["immediate"] = True
            b["retention"] = e["retention"]
        if (e["comparison_status"] == "indicative_skill_comparison"
                and e["curriculum_scope"] == "n_minus_1"):
            b["comparable"] = True
        if e["accepted_alternative_method"]:
            b["alternatives"] += 1
        for code in e["error_codes"]:
            b["errors"].append({"code": code, "scoring_id": e["scoring_id"],
                                "item_ref": e["item_ref"]})

    skills = []
    for key in sorted(buckets):
        b = buckets[key]
        rate = _rate(b["earned"], b["available"])
        ev = evidence.compute({
            "evidence_count": len(b["criteria"]),
            "independent_items": len(b["items"]),
            "points_available_centi": b["available"],
            "task_diversity": len(b["evidence_types"]),
            "has_transfer": b["has_transfer"],
            "limited_by_prompt": b["limited_by_prompt"],
            "comparable_to_baseline": b["comparable"],
            "immediate": b["immediate"],
        })
        ref = _skill_reference(session, assessment.level_key, b["analysis_skill_id"])
        origins = sorted(b["original_skill_ids"])
        if ref is None and origins:
            ref = _skill_reference(session, assessment.level_key, origins[0])
        importance = ref.importance_n if ref else "importante"
        label = ref.label if ref else b["analysis_skill_id"]
        if b["curriculum_scope"] == "bridge_n":
            status = bridge_status(rate, ev["level"])
            reading = BRIDGE_READING[status]
            status_label = BRIDGE_LABELS[status]
            action = BRIDGE_ACTIONS[status]
            priority = None
        else:
            status = n1_status(rate, ev["level"], b["immediate"])
            reading = N1_READING[status]
            status_label = N1_LABELS[status]
            action = None
            priority = _priority(status, importance)
        baseline = baselines.get(origins[0]) if origins else None
        skills.append({
            "analysis_skill_id": b["analysis_skill_id"],
            "label": label,
            "domain": ref.domain if ref else None,
            "importance_n": importance,
            "is_alias": bool(ref.is_alias) if ref else False,
            "original_skill_ids": origins,
            "curriculum_scope": b["curriculum_scope"],
            "earned_centi": b["earned"], "available_centi": b["available"],
            "earned": points.format_fr(b["earned"]),
            "available": points.format_fr(b["available"]),
            "success_rate": float(rate),
            "percentage": float(points.percentage(b["earned"], b["available"]))
            if b["available"] else None,
            "criteria": sorted(b["criteria"]), "item_refs": sorted(b["items"]),
            "evidence_types": sorted(b["evidence_types"]),
            "evidence_strength": ev["level"],
            "evidence_strength_label": ev["label"],
            "evidence_strength_score": ev["score"],
            "evidence_detail": ev["detail"],
            "status": status, "status_label": status_label, "reading": reading,
            "priority_rank": priority, "bridge_action": action,
            "error_codes": [e["code"] for e in b["errors"]],
            "errors": b["errors"],
            "accepted_alternative_methods": b["alternatives"],
            "recommended_delayed_check": b["immediate"],
            "retention": b["retention"],
            "limited_by_prompt": b["limited_by_prompt"],
            "baseline_status_qualitative": baseline.status_qualitative if baseline else None,
            "mastery_delta": None,
            "delta_blocked_reason": DELTA_BLOCKED_REASON,
        })

    # ------------------------------------------------------------ priorités N−1
    p1 = [s for s in skills if s["priority_rank"] == "P1"]
    if len(p1) > MAX_P1:
        p1.sort(key=lambda s: (s["importance_n"] != "critique", s["success_rate"]))
        for s in p1[MAX_P1:]:
            s["priority_rank"] = "P2"
            s["priority_downgraded"] = True
    order = {"P1": 0, "P2": 1, "P3": 2, "OK": 3}
    priorities = sorted([s for s in skills if s["curriculum_scope"] == "n_minus_1"],
                        key=lambda s: (order.get(s["priority_rank"], 9), s["success_rate"]))
    bridge_actions = [s for s in skills if s["curriculum_scope"] == "bridge_n"]

    # -------------------------------------------------------------- profil d'erreurs
    def error_profile(scope):
        counts = {}
        for s in skills:
            if s["curriculum_scope"] != scope:
                continue
            for e in s["errors"]:
                counts[e["code"]] = counts.get(e["code"], 0) + 1
        return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))

    errors_n1, errors_bridge = error_profile("n_minus_1"), error_profile("bridge_n")

    # ----------------------------------------------------------------- certitude
    confidences = []
    for obs in correction.item_observations:
        item = items.get(obs.item_id)
        if item is not None and item.confidence_probe and obs.confidence is not None:
            confidences.append({"item_ref": item.ref, "confidence": obs.confidence})

    # ------------------------------------------------------------------ rétention
    delayed = [s for s in skills if s["recommended_delayed_check"]]

    payload = {
        "schema": "nexus-s5-correction-analysis-v1",
        "student_id": student.student_id,
        "student_name": student.person.display_name,
        "assessment_id": assessment.assessment_id,
        "correction_revision": correction.revision,
        "level_key": assessment.level_key,
        "level_label": student.level_label,
        "subject": assessment.subject,
        "baseline_measure_available": BASELINE_MEASURE_AVAILABLE,
        "mastery_delta": None,
        "delta_blocked_reason": DELTA_BLOCKED_REASON,
        "raw_assessment_score": {
            "label": "score brut au sujet de clôture",
            "earned_centi": raw_centi,
            "max_centi": printed_max_centi,
            "scored_max_centi": scored_max_centi,
            "earned": points.format_fr(raw_centi),
            "max": points.format_fr(printed_max_centi),
            "sur_20": points.format_fr(
                int(round(raw_centi * 2000 / scored_max_centi)) if scored_max_centi else 0),
            "neutralised_centi": printed_max_centi - scored_max_centi,
            "avertissement": ("ce score n'est ni un score de consolidation, ni une "
                              "progression, ni un niveau N−1 : le sujet contient aussi des "
                              "éléments de passerelle vers l'année suivante."),
        },
        "n_minus_1_consolidation": n1_pool,
        "bridge_n_readiness": dict(bridge_pool, nature=(
            "observation de préparation, pas diagnostic de lacune")),
        "criteria": detail,
        "skills": skills,
        "priorities": priorities,
        "bridge_actions": bridge_actions,
        "error_profile": {
            "attribution": ("au critère effectivement échoué ; aucune propagation à l'item "
                            "ni aux autres compétences"),
            "n_minus_1": errors_n1, "bridge_n": errors_bridge,
            "dominant_n_minus_1": list(errors_n1)[:3],
            "by_criterion": [{"scoring_id": e["scoring_id"], "item_ref": e["item_ref"],
                              "analysis_skill_id": e["analysis_skill_id"],
                              "curriculum_scope": e["curriculum_scope"],
                              "error_codes": e["error_codes"]}
                             for e in scored if e["error_codes"]],
        },
        "retention": {
            "principe": ("une réussite obtenue moins d'une heure après la remédiation de la "
                         "même compétence mesure une performance immédiate, pas une "
                         "consolidation durable."),
            "skills": [{"analysis_skill_id": s["analysis_skill_id"], "label": s["label"],
                        "status": s["status"],
                        "reason": (s["retention"] or {}).get("reason")} for s in delayed],
        },
        "neutralised": [{"scoring_id": e["scoring_id"], "item_ref": e["item_ref"],
                         "raison": e["observation"],
                         "points": points.format_fr(e["max_score_centi"])}
                        for e in neutralised],
        "confidence": {"entries": confidences,
                       "note": "la certitude n'entre pas dans le score."},
        "conclusions": conclusions(skills, n1_pool, bridge_pool, delayed, neutralised),
        "warnings": warnings(skills, n1_pool, bridge_pool, delayed, neutralised),
    }
    payload["analysis_sha256"] = sha256_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return payload


def conclusions(skills, n1_pool, bridge_pool, delayed, neutralised) -> dict:
    """Ce qu'on peut conclure, ce qu'il faut dire prudemment, et ce qu'on ne peut pas dire."""
    solid, careful, limits = [], [], []
    for s in skills:
        if s["curriculum_scope"] == "n_minus_1":
            if s["status"] in ("SOLIDE",) and evidence.at_least(s["evidence_strength"],
                                                                "MODERATE"):
                solid.append("%s : %s (%s)" % (s["label"], s["reading"],
                                               evidence.LABELS[s["evidence_strength"]]))
            elif s["status"] in ("PRIORITAIRE", "A_CONSOLIDER"):
                if evidence.at_least(s["evidence_strength"], "MODERATE"):
                    solid.append("%s : %s" % (s["label"], s["reading"]))
                else:
                    careful.append("%s : %s, mais la preuve disponible est %s"
                                   % (s["label"], s["reading"],
                                      evidence.LABELS[s["evidence_strength"]]))
            elif s["status"] == "A_CONFIRMER":
                careful.append("%s : réussite obtenue juste après remédiation ; la rétention "
                               "reste à vérifier" % s["label"])
            elif s["status"] == "PREUVE_INSUFFISANTE":
                limits.append("%s : trop peu d'éléments pour conclure" % s["label"])
            else:
                careful.append("%s : %s" % (s["label"], s["reading"]))
        else:
            careful.append("%s : %s" % (s["label"], s["reading"]))

    limits.insert(0, DELTA_BLOCKED_REASON)
    if bridge_pool["available_centi"]:
        limits.append(
            "Le score brut inclut %s point(s) de passerelle vers l'année suivante : il n'est "
            "pas un diagnostic des acquis de l'année précédente."
            % points.format_fr(bridge_pool["available_centi"]))
    if delayed:
        limits.append("%d compétence(s) ont été évaluées moins d'une heure après leur "
                      "remédiation : un contrôle différé est nécessaire avant toute "
                      "affirmation de consolidation durable." % len(delayed))
    for s in skills:
        if s["limited_by_prompt"]:
            limits.append("%s : la formulation imprimée de la question ne soutient pas une "
                          "inférence forte." % s["label"])
    if neutralised:
        limits.append("%d critère(s) neutralisé(s) faute de correction équitable possible."
                      % len(neutralised))
    return {"etayees": solid, "prudentes": careful, "limites": limits}


def warnings(skills, n1_pool, bridge_pool, delayed, neutralised) -> list:
    out = [DELTA_BLOCKED_REASON]
    weak = [s["label"] for s in skills
            if s["evidence_strength"] in ("INSUFFICIENT", "LOW")]
    if weak:
        out.append("Force de preuve faible ou insuffisante pour : %s. Ces lectures ne "
                   "peuvent pas fonder une conclusion isolée." % ", ".join(weak))
    if delayed:
        out.append("Compétences mesurées juste après remédiation : %s."
                   % ", ".join(s["label"] for s in delayed))
    if not bridge_pool["available_centi"]:
        out.append("Aucun critère de passerelle dans ce sujet : le score brut porte "
                   "intégralement sur des acquis de l'année N−1.")
    return out
