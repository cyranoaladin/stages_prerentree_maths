# -*- coding: utf-8 -*-
"""Copie réelle de l'élève : téléversement, consultation, lecture assistée, revue.

Deux voies d'entrée coexistent pour une copie : ``tools/attach_source_copy.py`` pour
l'administration, et le téléversement depuis l'écran de correction pour l'usage
courant. Les deux passent par les mêmes contrôles d'octets et la même ingestion.

Aucune route ne modifie une pièce déjà rattachée. Un remplacement passe par le
mécanisme ``SUPERSEDED``, qui conserve l'ancienne.
"""

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from .. import config
from ..database import get_session
from ..domain import openrouter, rasterize, transcription, upload as up
from ..domain import source_copy as sc
from ..security import SecurityError, resolve_document
from . import get_assessment, page_context, require_writable

router = APIRouter()


def _copy_or_404(session, assessment):
    copy = sc.current_copy(session, assessment.assessment_id)
    if copy is None:
        raise HTTPException(status_code=404, detail="Aucune copie élève rattachée.")
    return copy


# --------------------------------------------------------------- consultation
@router.get("/eleve/{student_id}/copie/manifeste")
def copy_manifest(student_id: str, session: Session = Depends(get_session)):
    """« Quelle copie réelle a servi à cette correction ? » — la réponse complète."""
    assessment = get_assessment(session, student_id)
    described = sc.describe(session, assessment)
    described["limites"] = up.limits()
    return JSONResponse(described, media_type="application/json")


@router.get("/eleve/{student_id}/copie/page/{page_index}")
def copy_page(student_id: str, page_index: int, session: Session = Depends(get_session)):
    """Un fichier de la pièce originale, en lecture seule."""
    assessment = get_assessment(session, student_id)
    copy = _copy_or_404(session, assessment)
    row = next((r for r in sc.files_of(session, copy) if r.page_index == page_index),
               None)
    if row is None:
        raise HTTPException(status_code=404,
                            detail="Cette copie n'a pas de page %d." % page_index)
    return _serve(row)


@router.get("/eleve/{student_id}/copie/rendu/{page_index}")
def rendered_page(student_id: str, page_index: int,
                  session: Session = Depends(get_session)):
    """La page telle que le modèle la voit — rotation comprise.

    L'humain doit regarder exactement la même image que le modèle. Servir le rendu de
    base alors qu'une version tournée part en lecture ferait diverger les deux : le
    correcteur validerait une transcription faite sur une image qu'il n'a pas vue.
    """
    assessment = get_assessment(session, student_id)
    copy = _copy_or_404(session, assessment)
    pages = sc.pages_for_reading(session, copy)
    if not pages:
        raise HTTPException(status_code=404, detail="Les pages ne sont pas rendues.")
    row = next((r for r in pages if r.page_index == page_index), None)
    if row is None:
        raise HTTPException(status_code=404, detail="Page %d absente." % page_index)
    return _serve(row)


def _serve(row):
    try:
        path = resolve_document(str(sc.stored_path(row)),
                                [config.SOURCE_COPIES_DIR.resolve()])
    except SecurityError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return FileResponse(path, media_type=row.media_type,
                        headers={"Content-Disposition":
                                 'inline; filename="%s"' % path.name,
                                 "X-Content-Type-Options": "nosniff"})


@router.get("/eleve/{student_id}/copie/pages")
def pages_index(student_id: str, session: Session = Depends(get_session)):
    """Index de navigation multipage : miniatures, état de lecture, page courante."""
    assessment = get_assessment(session, student_id)
    copy = sc.current_copy(session, assessment.assessment_id)
    if copy is None:
        return JSONResponse({"attached": False, "pages": [],
                             "limites": up.limits()})
    # Ce que la visionneuse affiche est ce qui part en lecture : rotation comprise.
    derived_rows = sc.pages_for_reading(session, copy)
    resume = transcription.summary(session, assessment)
    par_page = {}
    if derived_rows:
        from ..models import TranscriptionBlock
        for row in (session.query(TranscriptionBlock)
                    .filter_by(source_copy_id=copy.source_copy_id).all()):
            entry = par_page.setdefault(row.page_index,
                                        {"blocs": 0, "a_trancher": 0, "verifies": 0})
            entry["blocs"] += 1
            if row.reconciliation == transcription.RECONCILE_REVIEW \
                    and row.review_state == transcription.REVIEW_AI_PROPOSED:
                entry["a_trancher"] += 1
            if row.review_state != transcription.REVIEW_AI_PROPOSED:
                entry["verifies"] += 1
    return JSONResponse({
        "attached": True,
        "source_copy_id": copy.source_copy_id,
        "page_count": copy.page_count,
        "original_files": [{"page_index": r.page_index, "name": r.original_name,
                            "media_type": r.media_type, "sha256": r.sha256}
                           for r in sc.files_of(session, copy)],
        "rendered": [{"page_index": r.page_index, "width": r.width_px,
                      "height": r.height_px, "dpi": r.dpi, "sha256": r.sha256,
                      "rotation": r.rotation,
                      "url": "/eleve/%s/copie/rendu/%d" % (student_id, r.page_index),
                      "ocr": par_page.get(r.page_index)}
                     for r in derived_rows],
        "transcription": resume,
        "limites": up.limits(),
    })


# -------------------------------------------------------------- téléversement
@router.post("/eleve/{student_id}/copie/televerser")
async def upload_copy(student_id: str,
                      fichiers: list[UploadFile] = File(...),
                      libelle: str = Form(None),
                      note: str = Form(None),
                      remplacer: int = Form(0),
                      autoriser_doublons: int = Form(0),
                      session: Session = Depends(get_session)):
    """Ingère une copie envoyée depuis le navigateur.

    L'ordre des fichiers reçus est l'ordre des pages : il a été confirmé par
    l'utilisateur avant l'envoi, et n'est jamais retrié ici.
    """
    require_writable()
    assessment = get_assessment(session, student_id)
    try:
        result = up.ingest(session, assessment, fichiers, label=libelle, note=note,
                           replace=bool(remplacer),
                           allow_duplicates=bool(autoriser_doublons))
    except up.UploadError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except sc.SourceCopyError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    session.commit()
    result["manifeste"] = sc.describe(session, assessment)
    return JSONResponse(result)


@router.post("/eleve/{student_id}/copie/rendre")
def render_pages_route(student_id: str, session: Session = Depends(get_session)):
    """Produit les pages dérivées destinées à la lecture assistée."""
    require_writable()
    assessment = get_assessment(session, student_id)
    try:
        derived = rasterize.render_pages(session, assessment)
    except rasterize.RasterError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    session.commit()
    return JSONResponse({"ok": True, "derived_copy_id": derived.source_copy_id,
                         "pages": derived.page_count})


# ----------------------------------------------------------- lecture assistée
@router.post("/eleve/{student_id}/copie/rendu/{page_index}/rotation")
def rotate_page_route(student_id: str, page_index: int, payload: dict = None,
                      session: Session = Depends(get_session)):
    """Tourne réellement les pixels d'une page, et enregistre la pièce dérivée.

    Tourner l'affichage ne suffirait pas : le modèle recevrait la page couchée.
    """
    require_writable()
    assessment = get_assessment(session, student_id)
    payload = payload or {}
    try:
        tournees = rasterize.rotate_page(session, assessment, page_index,
                                         int(payload.get("degrees", 0)))
    except (rasterize.RasterError, ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    session.commit()
    return JSONResponse({"ok": True, "derived_copy_id": tournees.source_copy_id,
                         "page_index": page_index,
                         "degrees": int(payload.get("degrees", 0))})


@router.get("/eleve/{student_id}/transcription", response_class=HTMLResponse)
def transcription_screen(student_id: str, request: Request, page: int = 1,
                         session: Session = Depends(get_session)):
    """Écran de revue : la page scannée à gauche, la transcription à droite."""
    assessment = get_assessment(session, student_id)
    resume = transcription.summary(session, assessment)
    vue = transcription.page_view(session, assessment, page)
    from ..main import templates
    return templates.TemplateResponse(
        request, "transcription.html", page_context(
            request, assessment=assessment, student=assessment.student,
            resume=resume, page_index=page, vue=vue,
            source_copy=sc.describe(session, assessment),
            openrouter_status=openrouter.configuration_status()))


@router.get("/eleve/{student_id}/transcription/etat")
def transcription_state(student_id: str, session: Session = Depends(get_session)):
    assessment = get_assessment(session, student_id)
    return JSONResponse(transcription.summary(session, assessment))


@router.get("/eleve/{student_id}/transcription/page/{page_index}")
def transcription_page(student_id: str, page_index: int,
                       session: Session = Depends(get_session)):
    assessment = get_assessment(session, student_id)
    return JSONResponse(transcription.page_view(session, assessment, page_index))


@router.post("/eleve/{student_id}/transcription/lancer")
def start_primary(student_id: str, payload: dict = None,
                  session: Session = Depends(get_session)):
    """Lance la première lecture. Explicite : rien ne se déclenche tout seul."""
    require_writable()
    assessment = get_assessment(session, student_id)
    payload = payload or {}
    try:
        run = transcription.run_primary(session, assessment,
                                        model=payload.get("model"),
                                        force=bool(payload.get("force")))
    except transcription.RemoteOcrForbiddenError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
    except (transcription.TranscriptionError, rasterize.RasterError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except openrouter.MissingKeyError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except openrouter.NoCompliantEndpointError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except openrouter.OpenRouterError as exc:
        raise HTTPException(status_code=502, detail=openrouter.redact(str(exc)))
    session.commit()
    return JSONResponse({"ok": True, "run_id": run.run_id,
                         "resume": transcription.summary(session, assessment)})


@router.post("/eleve/{student_id}/transcription/verifier")
def start_verify(student_id: str, payload: dict = None,
                 session: Session = Depends(get_session)):
    """Lance la seconde lecture. Elle est **aveugle** : elle ne voit pas la première."""
    require_writable()
    assessment = get_assessment(session, student_id)
    payload = payload or {}
    try:
        run = transcription.run_blind(session, assessment,
                                      model=payload.get("model"),
                                      force=bool(payload.get("force")))
    except transcription.RemoteOcrForbiddenError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
    except transcription.TranscriptionError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except openrouter.MissingKeyError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except openrouter.NoCompliantEndpointError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except openrouter.OpenRouterError as exc:
        raise HTTPException(status_code=502, detail=openrouter.redact(str(exc)))
    session.commit()
    return JSONResponse({"ok": True, "run_id": run.run_id,
                         "resume": transcription.summary(session, assessment)})


@router.post("/eleve/{student_id}/transcription/page/{page_index}/attester")
def attest_page_route(student_id: str, page_index: int, payload: dict = None,
                      session: Session = Depends(get_session)):
    """Attestation humaine de complétude pour une page.

    C'est le seul mécanisme qui puisse révéler une zone omise par **les deux**
    lectures : l'interface ne montre que ce que les modèles ont vu.
    """
    require_writable()
    assessment = get_assessment(session, student_id)
    payload = payload or {}
    try:
        row = transcription.attest_page(session, assessment, page_index,
                                        attested=bool(payload.get("attested", True)),
                                        note=payload.get("note"))
    except transcription.TranscriptionError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    session.commit()
    return JSONResponse({"ok": True, "page_index": row.page_index,
                         "attested": bool(row.attested),
                         "resume": transcription.summary(session, assessment)})


@router.get("/eleve/{student_id}/transcription/bloc/{block_pk}/historique")
def block_history_route(student_id: str, block_pk: int,
                        session: Session = Depends(get_session)):
    """Historique append-only des décisions humaines sur un bloc."""
    get_assessment(session, student_id)
    return JSONResponse({"historique": transcription.block_history(session, block_pk)})


@router.post("/eleve/{student_id}/transcription/bloc/{block_pk}")
def review_block_route(student_id: str, block_pk: int, payload: dict,
                       session: Session = Depends(get_session)):
    """Décision humaine sur un bloc : accepter, modifier, illisible, rejeter."""
    require_writable()
    assessment = get_assessment(session, student_id)
    try:
        row = transcription.review_block(
            session, assessment, block_pk, payload.get("action"),
            verbatim=payload.get("verbatim"), latex=payload.get("latex"),
            note=payload.get("note"), item_ref=payload.get("item_ref"))
    except transcription.TranscriptionError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    session.commit()
    return JSONResponse({"ok": True, "bloc": transcription._block_dict(row),
                         "resume": transcription.summary(session, assessment)})
