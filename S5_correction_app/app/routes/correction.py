# -*- coding: utf-8 -*-
"""Écran de correction : PDF à gauche, grille critère par critère à droite."""

import json

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from ..database import get_session
from ..domain import correction as corr
from ..domain import points, source_copy as sc, upload as up, validation
from ..schemas import GeneralObservationsIn, ReopenIn, ResponseIn
from . import get_assessment, get_correction, loads, page_context, require_writable

router = APIRouter()

SCOPE_BADGES = {
    "n_minus_1": {"code": "N-1", "label": "Acquis de l'année précédente", "css": "scope-n1",
                  "icon": "◆"},
    "bridge_n": {"code": "PASSERELLE N", "label": "Passerelle vers l'année à venir",
                 "css": "scope-bridge", "icon": "▲"},
    "mixed": {"code": "MIXTE", "label": "Critère mixte, éclaté analytiquement",
              "css": "scope-mixed", "icon": "◈"},
}

BRIDGE_NOTICE = ("Cette question participe au score brut mais ne doit pas dégrader le "
                 "diagnostic des acquis de l'année précédente.")


def _fallback_neutral(criterion) -> str:
    """Libellé neutre pour un critère que la revue curriculaire n'a pas encore couvert.

    On préfère un intitulé générique fondé sur le type de preuve à l'affichage de la
    description du barème, qui contient la réponse attendue.
    """
    return {
        "automatisme": "Résultat attendu, sans rédaction longue",
        "procedure": "Méthode conduite jusqu'au résultat",
        "justification": "Justification écrite, propriété nommée",
        "controle": "Contrôle du résultat effectivement mené",
        "transfert": "Mobilisation des acquis dans une situation nouvelle",
        "communication": "Formulation destinée à être lue par un tiers",
    }.get(criterion.evidence_type, "Critère de correction")


def _copy_context(session, assessment) -> dict:
    """Ce que l'écran affiche sur la copie, limites de téléversement comprises."""
    described = sc.describe(session, assessment)
    described["limites"] = up.limits()
    return described


def _require_source_copy(session, assessment):
    """En mode copie numérisée, on ne saisit pas un score sans source observable.

    En mode humain la liste est vide : l'enseignant a la copie papier devant lui, et
    la correction se déroule exactement comme avant.
    """
    blocking = sc.guard(session, assessment)
    if blocking:
        raise HTTPException(status_code=409, detail=" ".join(blocking))


def _grid(session, assessment, correction):
    """Construit la grille affichée : items, critères, sous-critères, saisies actuelles."""
    responses = {r.scoring_id: r for r in correction.responses}
    observations = {o.item_id: o for o in correction.item_observations}
    items = []
    for item in assessment.items:
        criteria = []
        for crit in item.criteria:
            badge = SCOPE_BADGES[crit.curriculum_scope]
            base = {
                "criterion_id": crit.criterion_id, "rank": crit.rank,
                "subpart": crit.subpart, "description": crit.description,
                "max_score_centi": crit.max_score_centi,
                "max_score": points.format_fr(crit.max_score_centi),
                "curriculum_scope": crit.curriculum_scope, "badge": badge,
                "bridge_notice": BRIDGE_NOTICE if crit.curriculum_scope == "bridge_n" else None,
                "evidence_type": crit.evidence_type,
                "analysis_skill_id": crit.analysis_skill_id,
                "analysis_skill_label": crit.analysis_skill_label,
                "evidence_quality": crit.evidence_quality,
                "scope_rationale": crit.scope_rationale,
                "official_source": crit.official_source,
                "scope_certainty": crit.scope_certainty,
                "accepted_methods": loads(crit.accepted_methods_json),
                "interpretation_limits": loads(crit.interpretation_limits_json),
                "fairness_rules": loads(crit.fairness_rules_json),
                "error_codes_allowed": loads(crit.error_codes_allowed_json),
                "printed_prompt": crit.printed_prompt,
                "proof_levels": loads(crit.proof_levels_json, {}),
                "teacher_correction": crit.teacher_correction,
                "rejected": loads(crit.rejected_json, {}),
                "retention": loads(crit.retention_json, {}),
                "retention_notice": corr.retention_notice(
                    loads(crit.retention_json, {})),
                "rows": [],
            }
            if crit.curriculum_scope == "mixed":
                targets = [(v.virtual_criterion_id, v.description, v.max_score_centi,
                            v.curriculum_scope, v.analysis_skill_id, True,
                            v.neutral_label, v.score_rubric_json,
                            v.error_suggestions_json) for v in crit.virtual_parts]
            else:
                targets = [(crit.criterion_id, crit.description, crit.max_score_centi,
                            crit.curriculum_scope, crit.analysis_skill_id, False,
                            crit.neutral_label, crit.score_rubric_json,
                            crit.error_suggestions_json)]
            for (scoring_id, desc, max_centi, scope, skill, is_virtual,
                 neutral, rubric_json, errors_json) in targets:
                row = responses.get(scoring_id)
                rubric = loads(rubric_json)
                # La rubrique fait autorité sur les valeurs proposées : un score partiel
                # qu'on ne sait pas justifier n'a pas à figurer sur un bouton.
                if rubric:
                    allowed = [{"centi": r["score_centi"],
                                "label": points.format_fr(r["score_centi"]),
                                "regle": r["regle"]} for r in
                               sorted(rubric, key=lambda r: r["score_centi"])]
                else:
                    allowed = [{"centi": v, "label": points.format_fr(v), "regle": None}
                               for v in points.allowed_scores(max_centi)]
                suggestions = loads(errors_json)
                base["rows"].append({
                    "scoring_id": scoring_id, "description": desc,
                    "neutral_label": neutral or _fallback_neutral(crit),
                    "max_score_centi": max_centi,
                    "max_score": points.format_fr(max_centi),
                    "curriculum_scope": scope, "badge": SCOPE_BADGES[scope],
                    "analysis_skill_id": skill, "is_virtual": is_virtual,
                    "allowed": allowed,
                    "rubric": sorted(rubric, key=lambda r: -r["score_centi"]),
                    "error_suggestions": suggestions,
                    "suggested_codes": [e["error_code"] for e in suggestions],
                    "score_centi": row.score_centi if row else None,
                    "score": points.format_fr(row.score_centi) if row and
                    row.score_centi is not None else None,
                    "error_codes": loads(row.error_codes_json) if row else [],
                    "observation": row.observation if row else None,
                    "accepted_alternative_method": bool(
                        row.accepted_alternative_method) if row else False,
                    "scoring_status": row.scoring_status if row else "PENDING",
                })
            criteria.append(base)
        obs = observations.get(item.item_id)
        items.append({
            "item_id": item.item_id, "ref": item.ref, "part": item.part, "kind": item.kind,
            "statement": item.statement,
            "max_points": points.format_fr(item.max_points_centi),
            "expected_answer": item.expected_answer,
            "significant_steps": loads(item.significant_steps_json),
            "likely_errors": loads(item.likely_errors_json),
            "accepted_methods": loads(item.accepted_methods_json),
            "non_scored": loads(item.teacher_observation_non_scored_json),
            "confidence_probe": item.confidence_probe,
            "confidence": obs.confidence if obs else None,
            "observation": obs.observation if obs else None,
            "criteria": criteria,
        })
    return items


@router.get("/eleve/{student_id}", response_class=HTMLResponse)
def correction_screen(student_id: str, request: Request, rapide: int = 0,
                      verif: int = 0, session: Session = Depends(get_session)):
    assessment = get_assessment(session, student_id)
    copy_blocking = sc.guard(session, assessment)
    # Une correction ne s'ouvre pas en mode copie numérisée tant qu'aucune pièce
    # source vérifiée n'est rattachée : il n'y aurait rien à observer.
    if copy_blocking and corr.current_correction(session, assessment.assessment_id) is None:
        raise HTTPException(status_code=409, detail=" ".join(copy_blocking))
    correction = get_correction(session, assessment,
                                create=not request.state.readonly and not copy_blocking)
    session.commit()
    grid = _grid(session, assessment, correction)
    problems = validation.validate(session, correction, assessment)
    from ..main import templates
    return templates.TemplateResponse(
        request, "correction.html", page_context(
        request, assessment=assessment, student=assessment.student,
        correction=correction, items=grid, progress=corr.progress(correction),
        problems=problems, quick=bool(rapide),
        validation_attempted=bool(verif),
        general=json.loads(correction.general_observations_json or "{}"),
        general_fields=corr.GENERAL_OBSERVATIONS,
        source_copy=_copy_context(session, assessment),
        source_copy_blocking=copy_blocking,
        locked=correction.status in corr.LOCKED_STATUSES))


@router.post("/eleve/{student_id}/critere/{scoring_id}")
def save_criterion(student_id: str, scoring_id: str, request: Request,
                   payload: ResponseIn, session: Session = Depends(get_session)):
    require_writable()
    assessment = get_assessment(session, student_id)
    _require_source_copy(session, assessment)
    correction = get_correction(session, assessment)
    try:
        row = corr.save_response(session, correction, scoring_id, payload.score_centi,
                                 payload.error_codes, payload.observation,
                                 payload.accepted_alternative_method, payload.scoring_status)
    except corr.LockedError as exc:
        raise HTTPException(status_code=423, detail=str(exc))
    except corr.CorrectionError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    session.commit()
    progress = corr.progress(correction)
    return JSONResponse({
        "ok": True, "scoring_id": scoring_id,
        "score_centi": row.score_centi,
        "score": points.format_fr(row.score_centi) if row.score_centi is not None else None,
        "scoring_status": row.scoring_status,
        "error_codes": json.loads(row.error_codes_json),
        "progress": progress,
        "saved_at": row.updated_at.astimezone().strftime("%H:%M:%S"),
    })


@router.post("/eleve/{student_id}/item/{item_id}/observation")
def save_item_observation(student_id: str, item_id: str, payload: dict,
                          session: Session = Depends(get_session)):
    require_writable()
    assessment = get_assessment(session, student_id)
    _require_source_copy(session, assessment)
    correction = get_correction(session, assessment)
    try:
        corr.save_item_observation(session, correction, item_id,
                                   payload.get("confidence"), payload.get("observation"))
    except corr.LockedError as exc:
        raise HTTPException(status_code=423, detail=str(exc))
    except corr.CorrectionError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    session.commit()
    import datetime as dt
    return JSONResponse({"ok": True,
                         "saved_at": dt.datetime.now().strftime("%H:%M:%S")})


@router.post("/eleve/{student_id}/observations")
def save_general(student_id: str, payload: GeneralObservationsIn,
                 session: Session = Depends(get_session)):
    require_writable()
    assessment = get_assessment(session, student_id)
    _require_source_copy(session, assessment)
    correction = get_correction(session, assessment)
    try:
        corr.save_general_observations(session, correction, payload.model_dump())
        if payload.observed_duration_minutes is not None:
            correction.observed_duration_minutes = payload.observed_duration_minutes
    except corr.LockedError as exc:
        raise HTTPException(status_code=423, detail=str(exc))
    except corr.CorrectionError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    session.commit()
    import datetime as dt
    return JSONResponse({"ok": True, "saved_at": dt.datetime.now().strftime("%H:%M:%S")})


@router.post("/eleve/{student_id}/valider", response_class=HTMLResponse)
def validate_correction(student_id: str, request: Request,
                        session: Session = Depends(get_session)):
    require_writable()
    assessment = get_assessment(session, student_id)
    correction = get_correction(session, assessment)
    problems = validation.validate(session, correction, assessment)
    if problems:
        from ..main import templates
        return templates.TemplateResponse(
        request, "partials/validation_problems.html", page_context(
            request, problems=problems, assessment=assessment,
            progress=corr.progress(correction)), status_code=400)
    if correction.status == "DRAFT":
        corr.set_status(session, correction, "REVIEW_READY")
    corr.set_status(session, correction, "VALIDATED")
    session.commit()
    return RedirectResponse("/eleve/%s/analyse" % student_id, status_code=303)


@router.post("/eleve/{student_id}/rouvrir")
def reopen_correction(student_id: str, payload: ReopenIn,
                      session: Session = Depends(get_session)):
    require_writable()
    assessment = get_assessment(session, student_id)
    correction = get_correction(session, assessment)
    try:
        new = corr.reopen(session, correction, payload.reason)
    except corr.CorrectionError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    session.commit()
    return JSONResponse({"ok": True, "revision": new.revision})


@router.get("/eleve/{student_id}/suivant")
def next_student(student_id: str, session: Session = Depends(get_session)):
    """« Valider et passer au suivant » : uniquement vers un élève non terminé."""
    from .dashboard import _rows
    rows = _rows(session)
    order = [r["student_id"] for r in rows]
    remaining = [sid for sid in order[order.index(student_id) + 1:]
                 if next(r for r in rows if r["student_id"] == sid)["status"]
                 in ("NOT_STARTED", "DRAFT", "REVIEW_READY")]
    target = remaining[0] if remaining else None
    return RedirectResponse("/eleve/%s" % target if target else "/", status_code=303)
