# -*- coding: utf-8 -*-
"""Routes HTTP. Le rendu vit ici, le calcul vit dans ``app/domain``."""

import json

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from .. import config
from ..models import Assessment, Correction, DelayedCheck, Student
from ..domain import correction as corr


def page_context(request, **extra):
    from ..main import STATE
    base = {
        "request": request,
        "readonly": config.settings.readonly,
        "readonly_reason": config.settings.readonly_reason,
        "pilot_mode": config.settings.pilot_mode,
        "drift": STATE.get("drift") or [],
        "immutability": STATE.get("immutability"),
    }
    base.update(extra)
    return base


def get_assessment(session, student_id: str) -> Assessment:
    assessment = (session.query(Assessment)
                  .options(joinedload(Assessment.student).joinedload(Student.person))
                  .filter(Assessment.student_id == student_id).one_or_none())
    if assessment is None:
        raise HTTPException(status_code=404, detail="Aucun élève ne porte l'identifiant « %s »."
                            % student_id)
    return assessment


def get_correction(session, assessment: Assessment, create: bool = False) -> Correction:
    current = corr.current_correction(session, assessment.assessment_id)
    if current is None:
        if not create:
            raise HTTPException(status_code=404,
                                detail="Aucune correction n'est ouverte pour cet élève.")
        current = corr.get_or_create_correction(session, assessment)
    return current


def delayed_checks(session, student_id: str):
    return session.query(DelayedCheck).filter_by(student_id=student_id).all()


def require_writable():
    if config.settings.readonly:
        raise HTTPException(status_code=423,
                            detail="Application en lecture seule : %s"
                                   % config.settings.readonly_reason)


def loads(value, default=None):
    try:
        return json.loads(value) if value else (default if default is not None else [])
    except (TypeError, ValueError):
        return default if default is not None else []
