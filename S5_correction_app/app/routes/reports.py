# -*- coding: utf-8 -*-
"""Bilans : prévisualisation, édition bloc par bloc, génération, approbation."""

import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from ..database import get_session
from ..domain import correction as corr
from ..domain import reports as rep
from ..models import Report
from ..schemas import BlockEditIn
from . import delayed_checks, get_assessment, get_correction, page_context, require_writable
from .analysis import load_analysis

router = APIRouter()


def _reports_of(session, assessment):
    out = {}
    for kind in rep.REPORT_TYPES:
        latest = (session.query(Report)
                  .filter_by(assessment_id=assessment.assessment_id, report_type=kind)
                  .order_by(Report.version.desc()).first())
        out[kind] = latest
    return out


@router.get("/eleve/{student_id}/bilan", response_class=HTMLResponse)
def report_screen(student_id: str, request: Request, type: str = "BILAN_PARENTS",
                  session: Session = Depends(get_session)):
    if type not in rep.REPORT_TYPES:
        raise HTTPException(status_code=404, detail="Type de bilan inconnu.")
    assessment = get_assessment(session, student_id)
    correction = get_correction(session, assessment)
    payload, plan = load_analysis(session, assessment, correction)
    delayed = delayed_checks(session, student_id)
    if not request.state.readonly:
        rep.ensure_report(session, assessment, correction, payload, plan, delayed, type)
        session.commit()
    reports = _reports_of(session, assessment)
    from ..main import templates
    return templates.TemplateResponse(
        request, "report.html", page_context(
        request, assessment=assessment, student=assessment.student, correction=correction,
        a=payload, plan=plan, current_type=type, report=reports.get(type),
        reports=reports, report_types=rep.REPORT_TYPES))


@router.post("/eleve/{student_id}/bilan/{type}/bloc/{block_key}")
def edit_block(student_id: str, type: str, block_key: str, payload: BlockEditIn,
               session: Session = Depends(get_session)):
    require_writable()
    assessment = get_assessment(session, student_id)
    report = (session.query(Report)
              .filter_by(assessment_id=assessment.assessment_id, report_type=type)
              .order_by(Report.version.desc()).first())
    if report is None:
        raise HTTPException(status_code=404, detail="Ce bilan n'existe pas encore.")
    if report.status == "APPROVED":
        raise HTTPException(status_code=409,
                            detail="Ce bilan est approuvé : régénérez une nouvelle version "
                                   "pour le modifier.")
    try:
        block = rep.edit_block(session, report, block_key, payload.content, payload.approve)
    except rep.ReportError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    session.commit()
    return JSONResponse({"ok": True, "block_key": block.block_key, "source": block.source,
                         "approved": block.approved,
                         "saved_at": dt.datetime.now().strftime("%H:%M:%S")})


@router.post("/eleve/{student_id}/bilan/{type}/regenerer")
def regenerate(student_id: str, type: str, session: Session = Depends(get_session)):
    require_writable()
    assessment = get_assessment(session, student_id)
    correction = get_correction(session, assessment)
    payload, plan = load_analysis(session, assessment, correction)
    report = rep.ensure_report(session, assessment, correction, payload, plan,
                               delayed_checks(session, student_id), type, regenerate=True)
    session.commit()
    kept = [b.block_key for b in report.blocks if b.source == "human"]
    return JSONResponse({"ok": True, "version": report.version, "blocs_conserves": kept})


@router.post("/eleve/{student_id}/bilan/{type}/generer")
def generate(student_id: str, type: str, session: Session = Depends(get_session)):
    require_writable()
    if type not in rep.REPORT_TYPES:
        raise HTTPException(status_code=404, detail="Type de bilan inconnu.")
    assessment = get_assessment(session, student_id)
    correction = get_correction(session, assessment)
    if correction.status not in ("VALIDATED", "REPORT_READY", "REPORT_APPROVED"):
        raise HTTPException(status_code=409,
                            detail="La correction doit être validée avant toute génération.")
    payload, plan = load_analysis(session, assessment, correction)
    report = rep.ensure_report(session, assessment, correction, payload, plan,
                               delayed_checks(session, student_id), type)
    tex = rep.render_tex(report, assessment, payload, plan)
    result = rep.compile_pdf(report, tex, assessment)
    if not result["ok"]:
        report.tex_path = result.get("tex_path")
        corr.audit(session, "report.compile_failed", "report", report.report_id,
                   assessment.assessment_id, new_value=result.get("error"))
        session.commit()
        raise HTTPException(status_code=500, detail={
            "message": result.get("error"),
            "tex_path": result.get("tex_path"),
            "journal": (result.get("stdout") or "")[-2000:]})
    report.pdf_path = result["pdf_path"]
    report.tex_path = result["tex_path"]
    report.pdf_sha256 = result["pdf_sha256"]
    report.generated_at = dt.datetime.now(dt.timezone.utc)
    report.status = "GENERATED"
    report.manifest_path = rep.write_manifest(report, assessment, result)
    if correction.status == "VALIDATED":
        corr.set_status(session, correction, "REPORT_READY")
    corr.audit(session, "report.generated", "report", report.report_id,
               assessment.assessment_id, new_value=result["pdf_sha256"][:16])
    session.commit()
    return JSONResponse({"ok": True, "report_id": report.report_id,
                         "version": report.version,
                         "pdf": "/rapport/%d/pdf" % report.report_id})


@router.post("/eleve/{student_id}/bilan/{type}/approuver")
def approve(student_id: str, type: str, session: Session = Depends(get_session)):
    require_writable()
    assessment = get_assessment(session, student_id)
    correction = get_correction(session, assessment)
    report = (session.query(Report)
              .filter_by(assessment_id=assessment.assessment_id, report_type=type)
              .order_by(Report.version.desc()).first())
    if report is None or not report.pdf_path:
        raise HTTPException(status_code=409,
                            detail="Le PDF doit être généré avant d'être approuvé.")
    report.status = "APPROVED"
    report.approved_at = dt.datetime.now(dt.timezone.utc)
    if correction.status == "REPORT_READY":
        corr.set_status(session, correction, "REPORT_APPROVED")
    corr.audit(session, "report.approved", "report", report.report_id,
               assessment.assessment_id, new_value="v%d" % report.version)
    session.commit()
    return JSONResponse({"ok": True, "version": report.version})


@router.post("/bilans/generer-tous")
def generate_all(session: Session = Depends(get_session)):
    """Ne génère que pour les corrections validées. Les autres sont listées, pas forcées."""
    require_writable()
    from ..models import Assessment
    produced, skipped, failed = [], [], []
    for assessment in session.query(Assessment).all():
        correction = corr.current_correction(session, assessment.assessment_id)
        if correction is None or correction.status not in ("VALIDATED", "REPORT_READY",
                                                           "REPORT_APPROVED"):
            skipped.append({"student_id": assessment.student_id,
                            "raison": "correction non validée"})
            continue
        payload, plan = load_analysis(session, assessment, correction)
        delayed = delayed_checks(session, assessment.student_id)
        for kind in rep.REPORT_TYPES:
            report = rep.ensure_report(session, assessment, correction, payload, plan,
                                       delayed, kind)
            tex = rep.render_tex(report, assessment, payload, plan)
            result = rep.compile_pdf(report, tex, assessment)
            if not result["ok"]:
                failed.append({"student_id": assessment.student_id, "type": kind,
                               "erreur": result.get("error")})
                continue
            report.pdf_path = result["pdf_path"]
            report.tex_path = result["tex_path"]
            report.pdf_sha256 = result["pdf_sha256"]
            report.generated_at = dt.datetime.now(dt.timezone.utc)
            report.status = "GENERATED"
            report.manifest_path = rep.write_manifest(report, assessment, result)
            produced.append({"student_id": assessment.student_id, "type": kind})
        if correction.status == "VALIDATED":
            corr.set_status(session, correction, "REPORT_READY")
    session.commit()
    return JSONResponse({"generes": produced, "ignores": skipped, "echecs": failed})
