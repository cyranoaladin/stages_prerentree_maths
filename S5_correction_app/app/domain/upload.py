# -*- coding: utf-8 -*-
"""Téléversement d'une copie depuis l'interface.

Rien de ce que le navigateur annonce n'est cru : ni le nom, ni l'extension, ni le
``Content-Type``. Seuls les octets font foi, comme au rattachement en ligne de commande.

Le flux est délibérément en deux temps :

1. le fichier arrive dans un **temporaire**, sous plafond de taille, où il est
   contrôlé et haché ;
2. il n'est ingéré dans ``source_copy`` qu'une fois tous les contrôles passés.

En cas d'échec, le temporaire est détruit et **aucune ligne n'est écrite** : il n'y a
pas d'état intermédiaire où une copie serait à moitié rattachée.

L'ordre des pages est arrêté **avant** l'envoi, dans le navigateur : l'utilisateur
voit les miniatures, réordonne, puis confirme. Le serveur enregistre l'ordre reçu et
ne le retrie jamais. Ce choix évite une zone d'attente serveur où des copies d'élèves
non ingérées s'accumuleraient sans statut ni provenance.
"""

import tempfile
from pathlib import Path

from .. import config
from ..security import safe_filename
from . import source_copy as sc

CHUNK = 1 << 20


class UploadError(Exception):
    """Téléversement refusé. Le message dit ce qui bloque et ce qu'il faut faire."""


def _human_size(octets: int) -> str:
    for unit in ("o", "Ko", "Mo", "Go"):
        if octets < 1024 or unit == "Go":
            return "%.0f %s" % (octets, unit)
        octets /= 1024.0
    return "%d o" % octets


def _spool(upload, directory: Path, index: int, budget: dict) -> Path:
    """Écrit un fichier téléversé dans un temporaire, sous plafond global de taille."""
    try:
        name = safe_filename(getattr(upload, "filename", "") or "page_%02d" % index)
    except Exception:
        raise UploadError("nom de fichier invalide pour la pièce n° %d." % index)
    target = directory / ("%02d_%s" % (index, name))
    written = 0
    stream = upload.file
    try:
        stream.seek(0)
    except Exception:
        pass
    with open(target, "wb") as out:
        while True:
            chunk = stream.read(CHUNK)
            if not chunk:
                break
            written += len(chunk)
            budget["total"] += len(chunk)
            if budget["total"] > config.UPLOAD_MAX_BYTES:
                raise UploadError(
                    "l'envoi dépasse la limite de %s. Ajustez "
                    "NEXUS_S5_UPLOAD_MAX_BYTES si un scan volumineux est légitime."
                    % _human_size(config.UPLOAD_MAX_BYTES))
            out.write(chunk)
    if written == 0:
        raise UploadError("le fichier « %s » est vide." % name)
    return target


def _tiff_frames(path: Path):
    """Nombre d'images dans un TIFF. ``None`` si le fichier n'est pas lisible."""
    try:
        from PIL import Image
        with Image.open(path) as img:
            return int(getattr(img, "n_frames", 1))
    except Exception:
        return None


def inspect(paths) -> list:
    """Contrôle les octets de chaque fichier reçu, avant toute écriture définitive."""
    out = []
    for path in paths:
        media_type = sc.detect_media_type(path)
        if media_type is None:
            raise UploadError(
                "« %s » n'est pas dans un format accepté. Formats reconnus : PDF, "
                "PNG, JPEG, TIFF, WEBP. Le type est lu dans les octets : renommer un "
                "fichier ne le convertit pas." % path.name)
        entry = {"path": path, "media_type": media_type,
                 "byte_size": path.stat().st_size, "pages": None}
        if media_type == "image/tiff":
            # Un TIFF peut contenir plusieurs images. Le rendu n'en prendrait que la
            # première : une page de copie disparaîtrait sans que personne ne le voie.
            # On refuse explicitement plutôt que de perdre du travail scolaire.
            frames = _tiff_frames(path)
            if frames is None:
                raise UploadError("« %s » n'est pas un TIFF lisible." % path.name)
            if frames > 1:
                raise UploadError(
                    "« %s » est un TIFF de %d pages. Ce format multipage n'est pas "
                    "pris en charge : la lecture n'en verrait que la première, et une "
                    "page de la copie disparaîtrait silencieusement. Exportez-le en "
                    "PDF, ou en images séparées." % (path.name, frames))
        if media_type == "application/pdf":
            pages = sc.pdf_page_count(path)
            if pages is not None and pages < 1:
                raise UploadError("« %s » ne contient aucune page exploitable."
                                  % path.name)
            entry["pages"] = pages
        out.append(entry)
    return out


def check_admissible(entries) -> int:
    """Règles d'admission. Retourne le nombre de pages annoncé, ou ``None``."""
    if not entries:
        raise UploadError("aucun fichier reçu.")
    if len(entries) > config.UPLOAD_MAX_FILES:
        raise UploadError("%d fichiers reçus, au-delà de la limite de %d."
                          % (len(entries), config.UPLOAD_MAX_FILES))
    kinds = {e["media_type"] for e in entries}
    if "application/pdf" in kinds and len(kinds) > 1:
        raise UploadError(
            "un envoi porte soit un PDF, soit des images, pas les deux : l'ordre des "
            "pages ne serait pas démontrable.")
    if "application/pdf" in kinds and len(entries) > 1:
        raise UploadError(
            "un seul PDF par copie. Plusieurs PDF sont plusieurs pièces distinctes : "
            "fusionnez-les avant l'envoi, ou téléversez-les séparément.")

    if "application/pdf" in kinds:
        pages = entries[0]["pages"]
        if pages is not None and pages > config.UPLOAD_MAX_PAGES:
            raise UploadError(
                "ce PDF compte %d pages, au-delà de la limite de %d. Ajustez "
                "NEXUS_S5_UPLOAD_MAX_PAGES si c'est légitime."
                % (pages, config.UPLOAD_MAX_PAGES))
        return pages
    if len(entries) > config.UPLOAD_MAX_PAGES:
        raise UploadError("%d images reçues, au-delà de la limite de %d pages."
                          % (len(entries), config.UPLOAD_MAX_PAGES))
    return len(entries)


def ingest(session, assessment, uploads, label=None, note=None, replace=False,
           allow_shared=False, is_synthetic=False,
           allow_duplicates=False) -> dict:
    """Contrôle puis ingère un envoi. Tout ou rien.

    ``uploads`` est la liste des fichiers dans l'ordre confirmé par l'utilisateur.
    Cet ordre est l'ordre des pages : il n'est jamais retrié.
    """
    if not uploads:
        raise UploadError("aucun fichier reçu.")
    budget = {"total": 0}
    with tempfile.TemporaryDirectory(prefix="nexus_upload_") as tmp:
        directory = Path(tmp)
        spooled, noms = [], []
        for index, upload in enumerate(uploads, start=1):
            spooled.append(_spool(upload, directory, index, budget))
            # Le nom conservé est celui que l'utilisateur a envoyé, pas le nom
            # temporaire préfixé par l'index d'arrivée.
            noms.append(safe_filename(getattr(upload, "filename", "")
                                      or "page_%02d" % index))
        entries = inspect(spooled)
        pages = check_admissible(entries)

        copy = sc.attach(session, assessment, [e["path"] for e in entries],
                         label=label, note=note, replace=replace,
                         allow_shared=allow_shared, original_names=noms,
                         is_synthetic=is_synthetic,
                         allow_duplicates=allow_duplicates)
        rows = sc.files_of(session, copy)
        return {
            "source_copy_id": copy.source_copy_id,
            "file_count": copy.file_count,
            "page_count": copy.page_count if copy.page_count is not None else pages,
            "octets": budget["total"],
            "octets_lisible": _human_size(budget["total"]),
            "files": [{"page_index": r.page_index, "original_name": r.original_name,
                       "media_type": r.media_type, "byte_size": r.byte_size,
                       "sha256": r.sha256} for r in rows],
        }
    # Le TemporaryDirectory est détruit ici : plus aucune trace de l'envoi hors de
    # source_copy, que l'ingestion ait réussi ou échoué.


def limits() -> dict:
    """Ce que l'interface annonce à l'utilisateur avant qu'il ne choisisse un fichier."""
    return {
        "max_bytes": config.UPLOAD_MAX_BYTES,
        "max_bytes_lisible": _human_size(config.UPLOAD_MAX_BYTES),
        "max_pages": config.UPLOAD_MAX_PAGES,
        "max_files": config.UPLOAD_MAX_FILES,
        "types": ["application/pdf", "image/png", "image/jpeg", "image/tiff",
                  "image/webp"],
    }
