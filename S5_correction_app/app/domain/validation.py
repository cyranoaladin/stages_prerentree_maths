# -*- coding: utf-8 -*-
"""Validation d'une correction : la liste de ce qui empêche encore de valider.

La fonction ne renvoie jamais « c'est presque bon ». Elle renvoie des problèmes, chacun
formulé de façon à être corrigeable sans deviner.
"""

import json
from dataclasses import dataclass
from typing import List

from . import correction as corr
from . import immutability, points


@dataclass
class Problem:
    code: str
    message: str
    item_ref: str = None
    scoring_id: str = None


def validate(session, correction, assessment) -> List[Problem]:
    problems: List[Problem] = []
    rows = {r.scoring_id: r for r in correction.responses}
    expected = {row["scoring_id"]: row for row in corr.scoring_rows(assessment)}

    missing = sorted(set(expected) - set(rows))
    unknown = sorted(set(rows) - set(expected))
    for scoring_id in missing:
        problems.append(Problem("critere_absent",
                                "le critère %s n'a pas de ligne de saisie" % scoring_id,
                                expected[scoring_id]["item_ref"], scoring_id))
    for scoring_id in unknown:
        problems.append(Problem("critere_inconnu",
                                "la saisie contient un critère qui n'existe pas au barème : %s"
                                % scoring_id, None, scoring_id))

    for scoring_id, row in sorted(rows.items()):
        meta = expected.get(scoring_id)
        ref = meta["item_ref"] if meta else None
        if row.scoring_status == "PENDING":
            problems.append(Problem("non_saisi",
                                    "item %s : le critère %s n'est pas corrigé"
                                    % (ref or "?", scoring_id), ref, scoring_id))
            continue
        if row.scoring_status == "NEUTRALISED":
            if not (row.observation or "").strip():
                problems.append(Problem("neutralisation_sans_raison",
                                        "critère %s neutralisé sans justification écrite"
                                        % scoring_id, ref, scoring_id))
            continue
        if row.score_centi is None:
            problems.append(Problem("score_absent",
                                    "critère %s : aucun score" % scoring_id, ref, scoring_id))
            continue
        if meta and row.max_score_centi != meta["max_score_centi"]:
            problems.append(Problem("bareme_divergent",
                                    "critère %s : le barème enregistré ne correspond plus au "
                                    "référentiel" % scoring_id, ref, scoring_id))
        if not points.is_acceptable(row.score_centi, row.max_score_centi):
            problems.append(Problem("score_hors_bareme",
                                    "critère %s : %s dépasse le maximum de %s"
                                    % (scoring_id, points.format_fr(row.score_centi),
                                       points.format_fr(row.max_score_centi)), ref, scoring_id))
        codes = json.loads(row.error_codes_json or "[]")
        for code in codes:
            if code not in corr.ERROR_CODES:
                problems.append(Problem("code_inconnu",
                                        "critère %s : code d'erreur inconnu %s"
                                        % (scoring_id, code), ref, scoring_id))
        if codes and row.score_centi == row.max_score_centi:
            problems.append(Problem("erreur_sur_reussite",
                                    "critère %s : intégralement réussi mais porteur d'un code "
                                    "d'erreur" % scoring_id, ref, scoring_id))

    # Les critères mixtes : la somme des sous-critères doit rendre exactement les points
    # du critère imprimé. Ni plus, ni moins, jamais de double comptage.
    for item in assessment.items:
        for crit in item.criteria:
            if crit.curriculum_scope != "mixed":
                continue
            parts = [rows.get(v.virtual_criterion_id) for v in crit.virtual_parts]
            max_sum = sum(v.max_score_centi for v in crit.virtual_parts)
            if max_sum != crit.max_score_centi:
                problems.append(Problem(
                    "mixte_bareme",
                    "critère mixte %s : les sous-critères totalisent %s au lieu de %s"
                    % (crit.criterion_id, points.format_fr(max_sum),
                       points.format_fr(crit.max_score_centi)), item.ref, crit.criterion_id))
            if all(p is not None and p.score_centi is not None for p in parts):
                got = sum(p.score_centi for p in parts)
                if got > crit.max_score_centi:
                    problems.append(Problem(
                        "mixte_somme",
                        "critère mixte %s : la somme des sous-critères dépasse le critère "
                        "d'origine" % crit.criterion_id, item.ref, crit.criterion_id))

    scored = [r for r in rows.values() if r.scoring_status not in ("PENDING", "NEUTRALISED")]
    total = sum(r.score_centi or 0 for r in scored)
    available = sum(r.max_score_centi for r in scored)
    if available > assessment.max_points_centi:
        problems.append(Problem("total_incoherent",
                                "le barème saisi (%s) dépasse le total du sujet (%s)"
                                % (points.format_fr(available),
                                   points.format_fr(assessment.max_points_centi))))
    if total > available:
        problems.append(Problem("total_incoherent",
                                "le score total dépasse le barème disponible"))

    for message in immutability.check_assessment(assessment):
        problems.append(Problem("immutabilite", message))

    for item in assessment.items:
        obs = next((o for o in correction.item_observations if o.item_id == item.item_id), None)
        if obs and obs.confidence is not None and not item.confidence_probe:
            problems.append(Problem("certitude_non_prevue",
                                    "item %s : une certitude est saisie alors que le sujet "
                                    "distribué n'en demande pas" % item.ref, item.ref))
    return problems


def summary(problems: List[Problem]) -> dict:
    by_code = {}
    for p in problems:
        by_code.setdefault(p.code, 0)
        by_code[p.code] += 1
    return {"total": len(problems), "par_code": by_code, "valide": not problems}
