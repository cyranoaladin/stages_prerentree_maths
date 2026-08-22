# -*- coding: utf-8 -*-
"""Écran du bilan longitudinal : ce que le système sait, et d'où il le sait.

L'écran est délibérément austère. Il ne cherche pas à impressionner : il montre,
côte à côte et sans les fusionner, le point de départ, ce qui a été proposé pendant
le stage, ce que l'évaluation établit, et ce qui reste à faire. La colonne
« travail réalisé » et la colonne « état observé » sont séparées à l'écran comme
elles le sont dans le document, pour la même raison.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from ..database import get_session
from ..domain.longitudinal import LongitudinalError, LongitudinalReportService
from ..domain.longitudinal import narrative as long_narrative
from ..domain.longitudinal import readiness as long_readiness
from ..domain.longitudinal import render as long_render
from .. import config
from . import get_assessment, get_correction, page_context

router = APIRouter()


@router.get("/eleve/{student_id}/bilan-longitudinal", response_class=HTMLResponse)
def longitudinal_screen(student_id: str, request: Request,
                        session: Session = Depends(get_session)):
    assessment = get_assessment(session, student_id)
    correction = get_correction(session, assessment)
    service = LongitudinalReportService(session)

    obstacles = service.check_ready(correction)
    # L'état des sources se lit AVANT toute correction : c'est ce qui permet de
    # savoir, dès aujourd'hui, ce que le bilan pourra dire et ce qu'il devra taire.
    etat_sources = long_readiness.evaluate(session, assessment, config)
    faits = None
    blocs = []
    peremption = None
    if not obstacles:
        faits = service.build_longitudinal_facts(assessment, correction, persist=False)
        blocs = long_narrative.parent_blocks(faits)
        peremption = service.is_stale(correction)

    from ..main import templates
    return templates.TemplateResponse(
        request, "longitudinal.html",
        page_context(request, assessment=assessment, student=assessment.student,
                     correction=correction, obstacles=obstacles, facts=faits,
                     blocks=blocs, staleness=peremption, readiness=etat_sources))


@router.get("/eleve/{student_id}/bilan-longitudinal/faits")
def longitudinal_facts(student_id: str, session: Session = Depends(get_session)):
    """Les faits, tels quels. C'est la réponse à « d'où sort cette phrase ? »."""
    assessment = get_assessment(session, student_id)
    correction = get_correction(session, assessment)
    try:
        faits = LongitudinalReportService(session).build_longitudinal_facts(
            assessment, correction, persist=False)
    except LongitudinalError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return JSONResponse(faits)


@router.post("/eleve/{student_id}/bilan-longitudinal/generer")
def generate_longitudinal(student_id: str, session: Session = Depends(get_session)):
    """Fige les faits, rend le document, le contrôle, puis compile.

    Un document qui ne passe pas le contrôle de langue n'est pas compilé : à ce
    stade il serait déjà transmissible.
    """
    assessment = get_assessment(session, student_id)
    correction = get_correction(session, assessment)
    try:
        faits = LongitudinalReportService(session).build_longitudinal_facts(
            assessment, correction, persist=True)
    except LongitudinalError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    base = "BILAN_LONGITUDINAL_%s" % student_id.replace("-", "_").upper()
    # §58 : les bilans réels vivent sous runtime/reports/, hors de Git.
    from ..config import REPORTS_DIR
    resultat = long_render.compile_pdf(faits, base, work_dir=REPORTS_DIR)
    if not resultat["ok"]:
        raise HTTPException(status_code=422, detail={
            "reason": resultat.get("reason"),
            "violations": resultat.get("validation", {}).get("violations", []),
        })
    session.commit()
    return JSONResponse({"ok": True, "pdf_path": resultat["pdf_path"],
                         "pdf_sha256": resultat["pdf_sha256"],
                         "facts_sha256": faits["facts_sha256"]})
