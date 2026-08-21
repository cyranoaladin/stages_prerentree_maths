# -*- coding: utf-8 -*-
"""Administration : historique, intégrité, sauvegardes, exports."""

import datetime as dt
import json
import shutil
import zipfile
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from .. import APP_VERSION, config
from ..database import get_session
from ..domain import immutability, importer
from ..domain import points
from ..models import (AnalysisSnapshot, Assessment, AuditEvent, ImportSource, Report,
                      Student)
from ..security import safe_slug, sha256_file
from . import get_assessment, page_context, require_writable

router = APIRouter()


@router.get("/historique", response_class=HTMLResponse)
def history(request: Request, student_id: str = "", limit: int = 400,
            session: Session = Depends(get_session)):
    query = session.query(AuditEvent).order_by(AuditEvent.id.desc())
    if student_id:
        query = query.filter(AuditEvent.assessment_id == "asm-%s" % student_id)
    events = query.limit(min(limit, 2000)).all()
    students = session.query(Student).all()
    from ..main import templates
    return templates.TemplateResponse(
        request, "history.html", page_context(
        request, events=events, students=sorted(students, key=lambda s: s.student_id),
        student_id=student_id))


@router.get("/admin", response_class=HTMLResponse)
def admin_screen(request: Request, session: Session = Depends(get_session)):
    report = immutability.verify()
    drift = importer.check_sources_unchanged(session)
    sources = session.query(ImportSource).order_by(ImportSource.id).all()
    backups = sorted(Path(config.BACKUPS_DIR).glob("*.sqlite3"), reverse=True)
    from ..main import templates
    return templates.TemplateResponse(
        request, "admin.html", page_context(
        request, immutability_report=report, summary=report.summary(), drift=drift,
        sources=sources, backups=[{"name": b.name, "size": b.stat().st_size} for b in backups],
        db_path=str(config.DB_PATH), app_version=APP_VERSION))


@router.post("/admin/backup")
def backup(session: Session = Depends(get_session)):
    """Sauvegarde : base, manifestes et rapports générés. Pas les sources lourdes."""
    require_writable()
    config.ensure_runtime()
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    target = Path(config.BACKUPS_DIR) / ("backup_%s.zip" % stamp)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        if config.DB_PATH.exists():
            zf.write(config.DB_PATH, "corrections.sqlite3")
        for path in sorted(Path(config.REPORTS_DIR).rglob("*")):
            if path.is_file():
                zf.write(path, str(Path("reports") / path.relative_to(config.REPORTS_DIR)))
        meta = {
            "created_at": dt.datetime.now().astimezone().isoformat(),
            "app_version": APP_VERSION,
            "immutability": immutability.verify().summary(),
            "note": ("les documents distribués ne sont pas recopiés : ils sont identifiés "
                     "par leurs empreintes dans IMMUTABLE_STUDENT_ARTIFACTS.json"),
        }
        zf.writestr("BACKUP_MANIFEST.json", json.dumps(meta, ensure_ascii=False, indent=2))
    return JSONResponse({"ok": True, "fichier": target.name,
                         "octets": target.stat().st_size,
                         "sha256": sha256_file(target)})


def _export_payload(session, assessment) -> dict:
    from ..domain import correction as corr
    correction = corr.current_correction(session, assessment.assessment_id)
    snapshot = None
    if correction is not None:
        snapshot = (session.query(AnalysisSnapshot)
                    .filter_by(correction_id=correction.correction_id)
                    .order_by(AnalysisSnapshot.id.desc()).first())
    payload = {
        "schema": "nexus-s5-correction-export-v1",
        "exported_at": dt.datetime.now().astimezone().isoformat(),
        "student_id": assessment.student_id,
        "student_name": assessment.student.person.display_name,
        "level_key": assessment.level_key,
        "subject": assessment.subject,
        "assessment": {
            "assessment_id": assessment.assessment_id,
            "evaluation_pdf_sha256": assessment.evaluation_pdf_sha256,
            "travail_pdf_sha256": assessment.travail_pdf_sha256,
            "max_points": points.format_fr(assessment.max_points_centi),
        },
        "correction": None,
        "analysis": json.loads(snapshot.payload_json) if snapshot else None,
        "reports": [],
    }
    if correction is not None:
        payload["correction"] = {
            "revision": correction.revision, "status": correction.status,
            "observed_duration_minutes": correction.observed_duration_minutes,
            "general_observations": json.loads(correction.general_observations_json or "{}"),
            "responses": [{
                "scoring_id": r.scoring_id, "criterion_id": r.criterion_id,
                "is_virtual": r.is_virtual,
                "score": points.format_fr(r.score_centi) if r.score_centi is not None else None,
                "max_score": points.format_fr(r.max_score_centi),
                "error_codes": json.loads(r.error_codes_json or "[]"),
                "observation": r.observation,
                "accepted_alternative_method": r.accepted_alternative_method,
                "criterion_scoring_status": r.scoring_status.lower(),
            } for r in sorted(correction.responses, key=lambda x: x.scoring_id)],
            "item_observations": [{
                "item_id": o.item_id, "confidence": o.confidence,
                "observation": o.observation} for o in correction.item_observations],
        }
        for report in session.query(Report).filter_by(
                assessment_id=assessment.assessment_id).all():
            payload["reports"].append({
                "report_type": report.report_type, "version": report.version,
                "status": report.status, "pdf_sha256": report.pdf_sha256,
                "analysis_sha256": report.analysis_sha256})
    return payload


@router.get("/admin/export/{student_id}")
def export_student(student_id: str, session: Session = Depends(get_session)):
    """Un export d'élève ne contient que cet élève. C'est vérifié par un test."""
    assessment = get_assessment(session, student_id)
    payload = _export_payload(session, assessment)
    config.ensure_runtime()
    target = Path(config.EXPORTS_DIR) / ("export_%s.json" % safe_slug(student_id).lower())
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    return JSONResponse(payload)


@router.post("/admin/export-tout")
def export_all(session: Session = Depends(get_session)):
    require_writable()
    config.ensure_runtime()
    stamp = dt.datetime.now().strftime("%Y%m%d")
    target = Path(config.EXPORTS_DIR) / ("export_corrections_%s.json" % stamp)
    payload = {"schema": "nexus-s5-correction-export-bundle-v1",
               "exported_at": dt.datetime.now().astimezone().isoformat(),
               "eleves": [_export_payload(session, a)
                          for a in session.query(Assessment).all()]}
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    return JSONResponse({"ok": True, "fichier": target.name,
                         "eleves": len(payload["eleves"])})


@router.post("/admin/export-cloture")
def export_closure(session: Session = Depends(get_session)):
    """Export de clôture de stage : les documents approuvés, rangés et empreintés."""
    require_writable()
    config.ensure_runtime()
    stamp = dt.datetime.now().strftime("%Y%m%d")
    root = Path(config.EXPORTS_DIR) / ("stage_cloture_%s" % stamp)
    folders = {"BILAN_PARENTS": "bilans_parents",
               "SYNTHESE_ENSEIGNANT": "syntheses_enseignants",
               "PLAN_RENTREE": "plans_4_semaines",
               "FICHE_ELEVE": "fiches_eleves"}
    for name in list(folders.values()) + ["analyses_json"]:
        (root / name).mkdir(parents=True, exist_ok=True)
    manifest, missing = [], []
    for assessment in session.query(Assessment).all():
        from ..domain import correction as corr
        correction = corr.current_correction(session, assessment.assessment_id)
        if correction is None or correction.status not in ("REPORT_READY", "REPORT_APPROVED"):
            missing.append({"student_id": assessment.student_id,
                            "raison": "aucun bilan généré"})
            continue
        for kind, folder in folders.items():
            report = (session.query(Report)
                      .filter_by(assessment_id=assessment.assessment_id, report_type=kind)
                      .order_by(Report.version.desc()).first())
            if report is None or not report.pdf_path or not Path(report.pdf_path).exists():
                missing.append({"student_id": assessment.student_id, "type": kind,
                                "raison": "PDF absent"})
                continue
            target = root / folder / Path(report.pdf_path).name
            shutil.copy2(report.pdf_path, target)
            manifest.append({"student_id": assessment.student_id, "type": kind,
                             "fichier": str(target.relative_to(root)),
                             "sha256": sha256_file(target)})
        payload = _export_payload(session, assessment)
        analysis_path = root / "analyses_json" / ("%s.json" % assessment.student_id)
        analysis_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
        manifest.append({"student_id": assessment.student_id, "type": "ANALYSE",
                         "fichier": str(analysis_path.relative_to(root)),
                         "sha256": sha256_file(analysis_path)})
    (root / "MANIFEST_SHA256.json").write_text(json.dumps({
        "schema": "nexus-s5-stage-closure-v1",
        "created_at": dt.datetime.now().astimezone().isoformat(),
        "documents": manifest, "manquants": missing,
        "immutability": immutability.verify().summary(),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return JSONResponse({"ok": True, "repertoire": str(root), "documents": len(manifest),
                         "manquants": missing})


@router.get("/admin/integrite")
def integrity(session: Session = Depends(get_session)):
    report = immutability.verify()
    return JSONResponse({"immutabilite": report.summary(),
                         "changes": report.changed, "missing": report.missing,
                         "derive_des_sources": importer.check_sources_unchanged(session)})
