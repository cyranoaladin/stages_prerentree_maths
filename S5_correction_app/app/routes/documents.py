# -*- coding: utf-8 -*-
"""Service des documents : PDF distribués et PDF générés.

Aucun chemin n'arrive de l'extérieur. Le client demande un élève et une nature ; le
serveur reconstruit le chemin depuis la base, puis le confine aux racines autorisées.
Une demande contenant « .. », un chemin absolu ou une séquence encodée n'a rien à
résoudre : elle n'est simplement jamais utilisée comme chemin.
"""


from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .. import config
from ..database import get_session
from ..models import Report
from ..security import SecurityError, resolve_document
from . import get_assessment

router = APIRouter()

KINDS = {"evaluation": "evaluation_pdf_path", "travail": "travail_pdf_path"}


@router.get("/document/{student_id}/{kind}")
def distributed_document(student_id: str, kind: str, session: Session = Depends(get_session)):
    if kind not in KINDS:
        raise HTTPException(status_code=404, detail="Type de document inconnu.")
    assessment = get_assessment(session, student_id)
    relative = getattr(assessment, KINDS[kind])
    try:
        path = resolve_document(relative, [config.CLOTURE_ROOT])
    except SecurityError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return FileResponse(path, media_type="application/pdf",
                        headers={"Content-Disposition":
                                 'inline; filename="%s"' % path.name,
                                 "X-Content-Type-Options": "nosniff"})


@router.get("/rapport/{report_id}/pdf")
def report_pdf(report_id: int, session: Session = Depends(get_session)):
    report = session.get(Report, report_id)
    if report is None or not report.pdf_path:
        raise HTTPException(status_code=404, detail="Ce rapport n'a pas encore de PDF.")
    try:
        path = resolve_document(report.pdf_path, [config.REPORTS_DIR.resolve()])
    except SecurityError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return FileResponse(path, media_type="application/pdf",
                        headers={"Content-Disposition":
                                 'inline; filename="%s"' % path.name,
                                 "X-Content-Type-Options": "nosniff"})


@router.get("/rapport/{report_id}/tex")
def report_tex(report_id: int, session: Session = Depends(get_session)):
    report = session.get(Report, report_id)
    if report is None or not report.tex_path:
        raise HTTPException(status_code=404, detail="Aucune source LaTeX pour ce rapport.")
    try:
        path = resolve_document(report.tex_path, [config.REPORTS_DIR.resolve(),
                                                  config.BUILD_DIR.resolve()])
    except SecurityError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return FileResponse(path, media_type="text/plain; charset=utf-8",
                        headers={"Content-Disposition":
                                 'attachment; filename="%s"' % path.name})
