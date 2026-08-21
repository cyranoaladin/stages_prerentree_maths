# -*- coding: utf-8 -*-
"""Écran d'analyse : ce que la correction validée permet d'établir."""

import json

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from ..database import get_session
from ..domain import action_plan
from ..domain import analysis as ana
from ..domain import correction as corr
from ..models import AnalysisSnapshot
from . import delayed_checks, get_assessment, get_correction, page_context

router = APIRouter()


def compute_and_store(session, assessment, correction) -> dict:
    payload = ana.analyse(session, correction, assessment)
    existing = (session.query(AnalysisSnapshot)
                .filter_by(correction_id=correction.correction_id)
                .order_by(AnalysisSnapshot.id.desc()).first())
    if existing is None or existing.analysis_sha256 != payload["analysis_sha256"]:
        session.add(AnalysisSnapshot(correction_id=correction.correction_id,
                                     analysis_sha256=payload["analysis_sha256"],
                                     payload_json=json.dumps(payload, ensure_ascii=False)))
        corr.audit(session, "analysis.computed", "correction", correction.correction_id,
                   assessment.assessment_id, new_value=payload["analysis_sha256"][:16])
    return payload


def load_analysis(session, assessment, correction):
    if correction.status not in ("VALIDATED", "REPORT_READY", "REPORT_APPROVED"):
        raise HTTPException(status_code=409,
                            detail="La correction doit être validée avant l'analyse.")
    payload = compute_and_store(session, assessment, correction)
    plan = action_plan.build(payload, delayed_checks(session, assessment.student_id))
    return payload, plan


@router.get("/eleve/{student_id}/analyse", response_class=HTMLResponse)
def analysis_screen(student_id: str, request: Request,
                    session: Session = Depends(get_session)):
    assessment = get_assessment(session, student_id)
    correction = get_correction(session, assessment)
    payload, plan = load_analysis(session, assessment, correction)
    session.commit()
    from ..main import templates
    return templates.TemplateResponse(
        request, "analysis.html", page_context(
        request, assessment=assessment, student=assessment.student,
        correction=correction, a=payload, plan=plan,
        error_total=sum(payload["error_profile"]["n_minus_1"].values())
        + sum(payload["error_profile"]["bridge_n"].values())))


@router.get("/eleve/{student_id}/analyse.json")
def analysis_json(student_id: str, session: Session = Depends(get_session)):
    assessment = get_assessment(session, student_id)
    correction = get_correction(session, assessment)
    payload, plan = load_analysis(session, assessment, correction)
    session.commit()
    return JSONResponse({"analysis": payload, "plan": plan})
