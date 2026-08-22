# -*- coding: utf-8 -*-
"""Rendu des pages d'une copie, pour la lecture assistée.

L'original ne bouge pas. On en produit une représentation visuelle page par page,
enregistrée comme pièce **dérivée** rattachée à lui : c'est cette représentation, et
elle seule, qui est montrée à un modèle de vision.

Pourquoi ne pas envoyer le PDF directement à un parseur documentaire : parce que les
pipelines PDF plafonnent le nombre d'images effectivement remontées au modèle, et
qu'une copie manuscrite n'a rien à gagner à être résumée. Chaque page doit être vue.

Résolution : ``config.RASTER_DPI``, 300 par défaut. Le choix n'est pas d'intuition —
``tools/measure_raster_dpi.py`` rend, pour un PDF donné, la taille en pixels de la
hauteur de ligne à 150, 200, 250 et 300 dpi. En dessous de 250, un exposant et un
chiffre de même corps deviennent difficiles à distinguer sur une écriture d'élève.
Au-delà de 300, le gain de lisibilité ne compense plus le poids transmis.
"""

import shutil
import tempfile
from pathlib import Path

from .. import config
from ..security import run_command
from . import source_copy as sc


class RasterError(Exception):
    pass


def _image_size(path: Path):
    """Dimensions en pixels, lues dans l'en-tête. Aucune image n'est décodée entière."""
    try:
        from PIL import Image
        with Image.open(path) as img:
            return img.size
    except Exception:
        # Repli sans dépendance : l'en-tête IHDR d'un PNG porte largeur et hauteur.
        try:
            data = path.read_bytes()[:33]
            if data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
                import struct
                return struct.unpack(">II", data[16:24])
        except Exception:
            pass
    return (None, None)


def _render_pdf(pdf_path: Path, out_dir: Path, dpi: int) -> list:
    """Rend un PDF en PNG, une image par page, via poppler.

    ``pdftoppm`` est déjà l'outil de rendu du dépôt : aucune dépendance nouvelle.
    """
    if shutil.which("pdftoppm") is None:
        raise RasterError(
            "pdftoppm (poppler) est absent : impossible de rendre les pages du PDF. "
            "Installez poppler-utils, ou fournissez la copie sous forme d'images.")
    prefix = out_dir / "page"
    done = run_command(["pdftoppm", "-png", "-r", str(dpi), "-cropbox",
                        str(pdf_path), str(prefix)],
                       cwd=out_dir, timeout=600,
                       cpu_secondes=config.RASTER_CPU_SECONDS,
                       memoire_octets=config.RASTER_MEMORY_BYTES,
                       taille_fichier_octets=config.RASTER_OUTPUT_MAX_BYTES)
    if done.returncode != 0:
        raise RasterError("le rendu du PDF a échoué : %s"
                          % (done.stderr or done.stdout or "")[:300])
    pages = sorted(out_dir.glob("page*.png"))
    if not pages:
        raise RasterError("le rendu du PDF n'a produit aucune page.")
    return pages


def _normalise_image(source: Path, out_dir: Path, index: int) -> Path:
    """Réencode une page fournie en image vers un PNG, sans rien recadrer ni retoucher.

    Le fichier d'origine reste la pièce probante ; ce PNG est une représentation
    dérivée, avec sa propre empreinte. Aucun redressement, aucun filtre, aucun
    rehaussement de contraste : une retouche pourrait effacer un trait de crayon.
    """
    target = out_dir / ("page-%03d.png" % index)
    try:
        from PIL import Image
        with Image.open(source) as img:
            img.load()
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            img.save(target, format="PNG")
        return target
    except ImportError:
        pass
    if shutil.which("convert") is None:
        raise RasterError(
            "ni Pillow ni ImageMagick ne sont disponibles pour préparer les images.")
    done = run_command(["convert", str(source), str(target)], cwd=out_dir, timeout=180,
                       cpu_secondes=config.RASTER_CPU_SECONDS,
                       memoire_octets=config.RASTER_MEMORY_BYTES,
                       taille_fichier_octets=config.RASTER_OUTPUT_MAX_BYTES)
    if done.returncode != 0 or not target.exists():
        raise RasterError("la conversion de %s a échoué." % source.name)
    return target


def render_pages(session, assessment, original=None, dpi: int = None, force=False):
    """Produit (ou réutilise) le jeu de pages dérivé de la pièce originale.

    Idempotent : si un jeu existe déjà pour cette pièce, il est rendu tel quel. Le
    recalcul se demande explicitement avec ``force``.
    """
    dpi = dpi or config.RASTER_DPI
    original = original or sc.current_copy(session, assessment.assessment_id)
    if original is None:
        raise RasterError("aucune copie rattachée à cette évaluation.")

    existing = sc.derived_pages(session, original)
    if existing is not None and not force:
        return existing

    files = sc.files_of(session, original)
    if not files:
        raise RasterError("la pièce rattachée ne contient aucun fichier.")

    with tempfile.TemporaryDirectory(prefix="nexus_raster_") as tmp:
        out_dir = Path(tmp)
        # Le temporaire porte des pages de copie : il est réservé au propriétaire.
        try:
            out_dir.chmod(0o700)
        except OSError:
            pass
        rendered = []
        if len(files) == 1 and files[0].media_type == "application/pdf":
            rendered = _render_pdf(sc.stored_path(files[0]), out_dir, dpi)
        else:
            for index, row in enumerate(files, start=1):
                rendered.append(_normalise_image(sc.stored_path(row), out_dir, index))

        if len(rendered) > config.UPLOAD_MAX_PAGES:
            raise RasterError(
                "cette copie compte %d pages, au-delà de la limite de %d. Ajustez "
                "NEXUS_S5_UPLOAD_MAX_PAGES si c'est légitime."
                % (len(rendered), config.UPLOAD_MAX_PAGES))

        specs = []
        for path in rendered:
            width, height = _image_size(path)
            if width and height and width * height > config.RASTER_MAX_PIXELS:
                raise RasterError(
                    "la page %s fait %d × %d pixels, au-delà de la limite. Réduisez "
                    "NEXUS_S5_RASTER_DPI." % (path.name, width, height))
            specs.append({"path": path, "width": width, "height": height})

        return sc.attach_derived_pages(session, assessment, original, specs, dpi=dpi)


ROTATIONS_ADMISES = (0, 90, 180, 270)


def rotate_page(session, assessment, page_index: int, degrees: int, original=None):
    """Tourne réellement les pixels d'une page, et enregistre la pièce dérivée.

    Une copie scannée peut arriver de travers. Tourner l'affichage dans le navigateur
    ne changerait pas ce que voit le modèle : il recevrait la page couchée. On produit
    donc une **page dérivée tournée**, avec sa propre empreinte, et c'est elle qui part
    en lecture.

    L'original ne bouge pas. Le rendu de base ne bouge pas non plus : la rotation est
    une troisième pièce, traçable jusqu'à eux.

    Comme l'empreinte change, la clé de cache change : la page tournée est relue, et
    la lecture de la page droite reste consultable.
    """
    if degrees not in ROTATIONS_ADMISES:
        raise RasterError("rotation admise : 0, 90, 180 ou 270 degrés (reçu %r)."
                          % degrees)
    original = original or sc.current_copy(session, assessment.assessment_id)
    if original is None:
        raise RasterError("aucune copie rattachée.")
    base = sc.derived_pages(session, original)
    if base is None:
        raise RasterError("les pages ne sont pas rendues.")
    pages_base = {r.page_index: r for r in sc.files_of(session, base)}
    if page_index not in pages_base:
        raise RasterError("page %s inconnue." % page_index)

    existantes = sc.rotated_pages(session, original)
    deja = {r.page_index: r for r in sc.files_of(session, existantes)} \
        if existantes else {}

    with tempfile.TemporaryDirectory(prefix="nexus_rotate_") as tmp:
        out_dir = Path(tmp)
        specs = []
        for rang in sorted(pages_base):
            if rang == page_index:
                angle = degrees
                source = sc.stored_path(pages_base[rang])
            elif rang in deja:
                # Déjà tournée : on la reprend telle quelle, sans la retourner.
                angle = deja[rang].rotation
                source = sc.stored_path(deja[rang])
            else:
                continue
            cible = out_dir / ("page-%03d.png" % rang)
            applique = angle if rang == page_index else 0
            _appliquer_rotation(source, cible, applique)
            largeur, hauteur = _image_size(cible)
            specs.append({"path": cible, "width": largeur, "height": hauteur,
                          "page_index": rang, "rotation": angle})
        if not specs:
            raise RasterError("aucune page à tourner.")
        # Les rangs doivent rester ceux des pages d'origine.
        ordonnees = sorted(specs, key=lambda x: x["page_index"])
        tournees = sc.attach_derived_pages(
            session, assessment, base, ordonnees, dpi=pages_base[page_index].dpi,
            source_kind=sc.DERIVED_ROTATED_PAGES, replaces=existantes,
            label="pages tournées")
    # Le rang enregistré par attach_derived_pages est l'ordre de la liste ; on le
    # rétablit sur le rang réel de la page d'origine.
    for row, spec in zip(sc.files_of(session, tournees), ordonnees):
        row.page_index = spec["page_index"]
    session.flush()
    return tournees


def _appliquer_rotation(source: Path, cible: Path, degrees: int):
    """Rotation sans perte de contenu : la toile s'agrandit, rien n'est rogné."""
    from PIL import Image
    with Image.open(source) as img:
        img.load()
        rendu = img if degrees == 0 else img.rotate(-degrees, expand=True)
        rendu.save(cible, format="PNG")


def measure_legibility(pdf_path: Path, dpis=(150, 200, 250, 300)) -> list:
    """Mesure, pour un PDF, la taille en pixels d'une page selon la résolution.

    Sert à justifier le choix de ``RASTER_DPI`` par une mesure plutôt que par une
    intuition. Ne rend aucun jugement sur la lisibilité de l'écriture : c'est une
    mesure de rendu, et l'appréciation reste humaine.
    """
    out = []
    with tempfile.TemporaryDirectory(prefix="nexus_measure_") as tmp:
        for dpi in dpis:
            folder = Path(tmp) / str(dpi)
            folder.mkdir()
            try:
                pages = _render_pdf(Path(pdf_path), folder, dpi)
            except RasterError as exc:
                out.append({"dpi": dpi, "erreur": str(exc)})
                continue
            first = pages[0]
            width, height = _image_size(first)
            out.append({"dpi": dpi, "pages": len(pages), "largeur_px": width,
                        "hauteur_px": height, "octets_page_1": first.stat().st_size})
    return out
