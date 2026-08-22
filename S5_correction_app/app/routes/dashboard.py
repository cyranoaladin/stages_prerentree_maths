# -*- coding: utf-8 -*-
"""Tableau de bord et vue de groupe."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload

from ..database import get_session
from ..domain import correction as corr
from ..domain.longitudinal import readiness as long_readiness
from .. import config
from ..models import Assessment, AnalysisSnapshot, Report, Student
from . import loads, page_context

router = APIRouter()

ORDER = ["4e", "3e", "2nde", "1ere_spe", "1re_nsi"]


# Deux axes distincts, jamais confondus : l'avancement de la correction décrit ce
# que l'enseignant a saisi ; l'état longitudinal décrit ce que les sources
# permettent d'écrire. Un élève peut être « non commencé » et son bilan « prêt ».
LONGITUDINAL_LABELS = {
    long_readiness.READY: "Prêt",
    long_readiness.WARNING: "Prêt avec réserve documentaire",
    long_readiness.BLOCKED: "Bloqué",
}


def _rows(session: Session):
    rows = []
    assessments = (session.query(Assessment)
                   .options(joinedload(Assessment.student).joinedload(Student.person))
                   .all())
    # L'immutabilité est relevée une seule fois : elle est identique pour tous.
    etats = {e["student_id"]: e
             for e in long_readiness.evaluate_all(session, config)}
    for a in assessments:
        current = corr.current_correction(session, a.assessment_id)
        progress = corr.progress(current) if current else {"total": 0, "done": 0,
                                                           "percent": 0, "remaining": 0}
        reports = (session.query(Report).filter_by(assessment_id=a.assessment_id).all())
        approved = [r for r in reports if r.status == "APPROVED"]
        generated = [r for r in reports if r.pdf_path]
        if approved:
            report_state, report_label = "REPORT_APPROVED", "Bilan approuvé"
        elif generated:
            report_state, report_label = "REPORT_GENERATED", "Bilan généré"
        elif current is not None and current.status in ("VALIDATED", "REPORT_READY"):
            report_state, report_label = "REPORT_READY", "Bilan à générer"
        else:
            report_state, report_label = "NONE", "—"
        rows.append({
            "student_id": a.student_id,
            "display_name": a.student.person.display_name,
            "level_key": a.level_key, "level_label": a.student.level_label,
            "subject": a.subject,
            "status": current.status if current else "NOT_STARTED",
            "status_label": corr.STATUS_LABELS.get(
                current.status if current else "NOT_STARTED", "—"),
            "revision": current.revision if current else 0,
            "progress": progress,
            "report_state": report_state, "report_label": report_label,
            "reports": len(generated),
            "longitudinal_state": (etats.get(a.student_id) or {}).get(
                "status", long_readiness.BLOCKED),
            "longitudinal_label": LONGITUDINAL_LABELS.get(
                (etats.get(a.student_id) or {}).get("status"), "—"),
            "longitudinal_warnings": len(
                ((etats.get(a.student_id) or {}).get("longitudinal_report") or {})
                .get("warnings") or []),
        })
    rows.sort(key=lambda r: (ORDER.index(r["level_key"]) if r["level_key"] in ORDER else 9,
                             r["display_name"]))
    return rows


def _counters(rows):
    def count(*statuses):
        return sum(1 for r in rows if r["status"] in statuses)
    return {
        "total": len(rows),
        "non_commencees": count("NOT_STARTED"),
        "en_cours": count("DRAFT"),
        "a_verifier": count("REVIEW_READY"),
        "validees": count("VALIDATED", "REPORT_READY", "REPORT_APPROVED"),
        "bilans_prets": sum(1 for r in rows if r["report_state"] == "REPORT_GENERATED"),
        "bilans_approuves": sum(1 for r in rows if r["report_state"] == "REPORT_APPROVED"),
    }


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, niveau: str = "", matiere: str = "", etat: str = "",
              q: str = "", session: Session = Depends(get_session)):
    rows = _rows(session)
    filtered = rows
    if niveau:
        filtered = [r for r in filtered if r["level_key"] == niveau]
    if matiere:
        filtered = [r for r in filtered if r["subject"] == matiere]
    if etat:
        filtered = [r for r in filtered if r["status"] == etat]
    if q:
        needle = q.strip().lower()
        filtered = [r for r in filtered if needle in r["display_name"].lower()]
    from ..main import templates
    return templates.TemplateResponse(
        request, "dashboard.html", page_context(
        request, rows=filtered, all_rows=rows, counters=_counters(rows),
        niveaux=sorted({r["level_key"] for r in rows},
                       key=lambda k: ORDER.index(k) if k in ORDER else 9),
        matieres=sorted({r["subject"] for r in rows}),
        etats=list(corr.STATUS_LABELS.items()),
        filtres={"niveau": niveau, "matiere": matiere, "etat": etat, "q": q}))


@router.get("/groupe", response_class=HTMLResponse)
def group_view(request: Request, session: Session = Depends(get_session)):
    """Vue de groupe : ce qui aide à organiser la rentrée. Pas un classement."""
    rows = []
    for a in session.query(Assessment).all():
        current = corr.current_correction(session, a.assessment_id)
        snapshot = None
        if current is not None:
            snapshot = (session.query(AnalysisSnapshot)
                        .filter_by(correction_id=current.correction_id)
                        .order_by(AnalysisSnapshot.id.desc()).first())
        payload = loads(snapshot.payload_json, {}) if snapshot else {}
        priorities = [p for p in payload.get("priorities", [])
                      if p.get("priority_rank") in ("P1", "P2")]
        reports = session.query(Report).filter_by(assessment_id=a.assessment_id).all()
        rows.append({
            "student_id": a.student_id,
            "display_name": a.student.person.display_name,
            "level_label": a.student.level_label, "subject": a.subject,
            "analysed": bool(payload),
            "n1": payload.get("n_minus_1_consolidation", {}),
            "bridge": payload.get("bridge_n_readiness", {}),
            "priorities": [p["label"] for p in priorities][:3],
            "report": "approuvé" if any(r.status == "APPROVED" for r in reports)
            else ("généré" if any(r.pdf_path for r in reports) else "—"),
        })
    rows.sort(key=lambda r: r["display_name"])
    from ..main import templates
    return templates.TemplateResponse(
        request, "group.html", page_context(request, rows=rows))
