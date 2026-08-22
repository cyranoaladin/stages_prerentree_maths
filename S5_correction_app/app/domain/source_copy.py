# -*- coding: utf-8 -*-
"""Copie réelle de l'élève : identité, provenance, immutabilité.

Ce module ne lit pas la copie. Il ne segmente rien, n'extrait aucune réponse et
ne devine aucun score. Il répond à une seule question, et il doit pouvoir y
répondre des mois plus tard :

    « quelle copie réelle a servi à cette correction ? »

Deux modes d'usage coexistent, et la distinction est structurante :

* **mode humain** — l'enseignant regarde une copie papier posée à côté de lui
  puis saisit les résultats. La pièce probante est physique ; aucune pièce jointe
  n'est nécessaire, et son absence n'est pas un défaut ;
* **mode copie numérisée** — un PDF ou des photographies servent de source
  observable à la correction. Là, l'absence de rattachement est un trou de
  provenance : rien ne permettrait de démontrer quelle copie a été observée.

Le fichier fourni est **recopié**, jamais déplacé ni réécrit. La copie stockée est
passée en ``0400`` — lecture seule **et** réservée à son propriétaire — et son
empreinte est recalculée à chaque affichage. L'intégrité vient du hachage, pas des
droits ; les droits, eux, servent la confidentialité : sur un poste partagé, un mode
``0444`` rendrait la copie d'un élève lisible par tout le monde. Si une
normalisation devient un jour nécessaire, elle produit une pièce *dérivée*
distincte, qui pointe vers son original et porte sa propre empreinte : l'original
n'est jamais remplacé silencieusement par une version recompressée.
"""

import shutil
import subprocess
from pathlib import Path

from .. import config
from ..models import Assessment, SourceCopy, SourceCopyFile
from ..security import safe_slug, sha256_file
from .correction import audit, current_correction

REAL_STUDENT_COPY = "REAL_STUDENT_COPY"
# Rendus de pages produits pour la lecture assistée. Ce ne sont pas des pièces
# probantes : ils dérivent de l'original et ne le remplacent jamais.
DERIVED_PAGE_IMAGES = "DERIVED_PAGE_IMAGES"
# Pages dont les pixels ont réellement été tournés. Une rotation d'affichage dans le
# navigateur ne change pas ce que voit un modèle : celle-ci, si. L'original et le
# rendu de base restent intacts, et la page tournée porte sa propre empreinte.
DERIVED_ROTATED_PAGES = "DERIVED_ROTATED_PAGES"

ORIGIN_ORIGINAL = "ORIGINAL"
ORIGIN_DERIVED = "DERIVED"

STATUS_ATTACHED = "ATTACHED"
STATUS_SUPERSEDED = "SUPERSEDED"

# Types acceptés, reconnus par leurs octets de tête et non par leur extension : une
# photographie renommée en « .pdf » n'est pas un PDF, et le rattachement doit le dire.
MEDIA_SIGNATURES = (
    ("application/pdf", b"%PDF-"),
    ("image/png", b"\x89PNG\r\n\x1a\n"),
    ("image/jpeg", b"\xff\xd8\xff"),
    ("image/tiff", b"II*\x00"),
    ("image/tiff", b"MM\x00*"),
)

IMAGE_TYPES = {"image/png", "image/jpeg", "image/tiff", "image/webp"}

EXTENSIONS = {"application/pdf": ".pdf", "image/png": ".png", "image/jpeg": ".jpg",
              "image/tiff": ".tif", "image/webp": ".webp"}


class SourceCopyError(Exception):
    """Rattachement refusé. Le message dit ce qui bloque et ce qu'il faut faire."""


# ------------------------------------------------------------------ inspection
def detect_media_type(path: Path) -> str:
    """Type MIME lu dans les octets. ``None`` si le format n'est pas accepté."""
    with open(path, "rb") as f:
        head = f.read(16)
    for media_type, signature in MEDIA_SIGNATURES:
        if head.startswith(signature):
            return media_type
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "image/webp"
    return None


def pdf_page_count(path: Path):
    """Nombre de pages d'un PDF, lu par ``pdfinfo``. ``None`` si l'outil est absent.

    Le nombre de pages est une information de confort : le barème n'en dépend pas.
    Il n'y a donc aucune raison d'ajouter une dépendance Python pour l'obtenir, ni
    de faire échouer un rattachement parce que poppler n'est pas installé.
    """
    if shutil.which("pdfinfo") is None:
        return None
    try:
        done = subprocess.run(["pdfinfo", str(path)], capture_output=True,
                              encoding="utf-8", errors="replace", timeout=30,
                              shell=False, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    if done.returncode != 0:
        return None
    for line in done.stdout.splitlines():
        if line.startswith("Pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
    return None


# --------------------------------------------------------------------- lecture
def current_copy(session, assessment_id: str):
    """La copie réellement rattachée à cette évaluation, ou ``None``.

    Filtrée sur ``REAL_STUDENT_COPY`` : les rendus de pages destinés à la lecture
    assistée vivent dans la même table mais ne sont pas la pièce probante, et ne
    doivent jamais l'éclipser.
    """
    return (session.query(SourceCopy)
            .filter(SourceCopy.assessment_id == assessment_id,
                    SourceCopy.source_kind == REAL_STUDENT_COPY,
                    SourceCopy.status == STATUS_ATTACHED)
            .order_by(SourceCopy.source_copy_id.desc())
            .first())


def rotated_pages(session, original):
    """Le jeu de pages tournées courant pour cette pièce, ou ``None``."""
    base = derived_pages(session, original)
    if base is None:
        return None
    return (session.query(SourceCopy)
            .filter(SourceCopy.derived_from_id == base.source_copy_id,
                    SourceCopy.source_kind == DERIVED_ROTATED_PAGES,
                    SourceCopy.status == STATUS_ATTACHED)
            .order_by(SourceCopy.source_copy_id.desc())
            .first())


def pages_for_reading(session, original):
    """Les pages réellement montrées au modèle, rotation comprise.

    Pour chaque rang : la version tournée si elle existe, sinon le rendu de base.
    C'est cette liste — et elle seule — qui part en lecture, et dont les empreintes
    entrent dans la clé de cache.
    """
    base = derived_pages(session, original)
    if base is None:
        return []
    pages = {row.page_index: row for row in files_of(session, base)}
    tournees = rotated_pages(session, original)
    if tournees is not None:
        for row in files_of(session, tournees):
            pages[row.page_index] = row
    return [pages[index] for index in sorted(pages)]


def derived_pages(session, original):
    """Le jeu de pages rastérisées courant pour cette pièce, ou ``None``."""
    return (session.query(SourceCopy)
            .filter(SourceCopy.derived_from_id == original.source_copy_id,
                    SourceCopy.source_kind == DERIVED_PAGE_IMAGES,
                    SourceCopy.status == STATUS_ATTACHED)
            .order_by(SourceCopy.source_copy_id.desc())
            .first())


def files_of(session, copy) -> list:
    return (session.query(SourceCopyFile)
            .filter(SourceCopyFile.source_copy_id == copy.source_copy_id)
            .order_by(SourceCopyFile.page_index)
            .all())


def _cible_libre(target: Path):
    """Refuse d'écrire là où un fichier existe déjà.

    Aucun identifiant n'est réutilisé en production : rien n'y est jamais supprimé.
    Si un résidu se présente malgré tout — nettoyage manuel, restauration partielle —
    écraser silencieusement une pièce probante serait la pire des réponses. On
    s'arrête, et ``tools/fsck.py`` dira ce qui traîne.
    """
    if target.exists():
        raise SourceCopyError(
            "un fichier occupe déjà %s. Une pièce stockée ne s'écrase pas : "
            "diagnostiquez avec « make s5-correction-fsck »." % target)


def _restreindre(chemin: Path):
    """Répertoire réservé à son propriétaire. Une copie d'élève n'est pas publique."""
    try:
        chemin.chmod(0o700)
        parent = chemin.parent
        if parent != Path(config.SOURCE_COPIES_DIR):
            parent.chmod(0o700)
    except OSError:
        pass


def stored_path(row) -> Path:
    return Path(config.RUNTIME_DIR) / row.stored_path


def verify(session, copy) -> dict:
    """Recalcule les empreintes des fichiers stockés et les compare à l'enregistrement."""
    rows = files_of(session, copy)
    checked, changed, missing = [], [], []
    for row in rows:
        full = stored_path(row)
        if not full.exists():
            missing.append(row.stored_path)
            continue
        observed = sha256_file(full)
        if observed != row.sha256:
            changed.append({"path": row.stored_path, "expected": row.sha256,
                            "observed": observed})
            continue
        checked.append(row.stored_path)
    ok = not changed and not missing and bool(rows)
    return {"ok": ok, "files_total": len(rows), "files_verified": len(checked),
            "changed": changed, "missing": missing,
            "verdict": "EMPREINTE VÉRIFIÉE" if ok else "EMPREINTE NON VÉRIFIÉE"}


def describe(session, assessment) -> dict:
    """Ce que l'écran de correction et l'audit ont besoin de savoir. Jamais deviné."""
    copy = current_copy(session, assessment.assessment_id)
    if copy is None:
        return {"attached": False, "mode": correction_mode(),
                "message": "Aucune copie élève rattachée."}
    rows = files_of(session, copy)
    correction = current_correction(session, assessment.assessment_id)
    return {
        "attached": True,
        "mode": correction_mode(),
        "source_copy_id": copy.source_copy_id,
        "assessment_id": copy.assessment_id,
        "correction_id": correction.correction_id if correction else None,
        "correction_revision": correction.revision if correction else None,
        "source_kind": copy.source_kind,
        "origin": copy.origin,
        "derived_from_id": copy.derived_from_id,
        "label": copy.label,
        "page_count": copy.page_count,
        "file_count": len(rows),
        # ISO plutôt que datetime : ce dictionnaire part aussi bien dans un gabarit
        # que dans une réponse JSON, et la seconde ne sait pas sérialiser un datetime.
        "ingested_at": copy.ingested_at.isoformat() if copy.ingested_at else None,
        "is_immutable": bool(copy.is_immutable),
        "is_synthetic": bool(copy.is_synthetic),
        "note": copy.note,
        "files": [{"page_index": r.page_index, "original_name": r.original_name,
                   "media_type": r.media_type, "byte_size": r.byte_size,
                   "sha256": r.sha256, "stored_path": r.stored_path}
                  for r in rows],
        "verification": verify(session, copy),
    }


# ----------------------------------------------------------------- rattachement
def _check_not_bound_elsewhere(session, digest: str, assessment_id: str, allow_shared: bool):
    """Un même fichier ne se rattache pas par inadvertance à deux élèves différents."""
    clash = (session.query(SourceCopyFile)
             .join(SourceCopy, SourceCopy.source_copy_id == SourceCopyFile.source_copy_id)
             .filter(SourceCopyFile.sha256 == digest,
                     SourceCopy.assessment_id != assessment_id)
             .first())
    if clash is None:
        return
    other = session.get(SourceCopy, clash.source_copy_id)
    if not allow_shared:
        raise SourceCopyError(
            "ce fichier (sha256 %s…) est déjà rattaché à une autre évaluation (%s). "
            "Un même fichier ne peut pas appartenir à deux élèves sans décision "
            "explicite : relancez avec --autoriser-partage si c'est réellement voulu."
            % (digest[:16], other.assessment_id))


def _prepare(paths, assessment_id, session, allow_shared, original_names=None,
             allow_duplicates=False) -> list:
    """Contrôle les fichiers fournis avant d'écrire quoi que ce soit.

    ``original_names`` permet à l'appelant de donner le nom réellement soumis par
    l'utilisateur, lorsqu'il diffère du nom du fichier examiné — c'est le cas d'un
    téléversement, qui passe par un temporaire. Le nom conservé doit être celui que
    la personne a envoyé, pas un artefact interne.
    """
    if not paths:
        raise SourceCopyError("aucun fichier fourni.")
    prepared, seen = [], {}
    for position, raw in enumerate(paths):
        path = Path(raw).expanduser()
        nom_soumis = (original_names[position] if original_names
                      and position < len(original_names) else path.name)
        if not path.exists() or not path.is_file():
            raise SourceCopyError("source introuvable : %s" % raw)
        media_type = detect_media_type(path)
        if media_type is None:
            raise SourceCopyError(
                "format non reconnu : %s. Formats acceptés : PDF, PNG, JPEG, TIFF, WEBP. "
                "Une conversion préalable produirait une pièce dérivée : convertissez "
                "d'abord, puis rattachez l'original ET le dérivé." % path.name)
        digest = sha256_file(path)
        if digest in seen and not allow_duplicates:
            # Deux pages identiques ne sont pas nécessairement une erreur : deux pages
            # blanches d'un même scan le sont légitimement. Mais c'est aussi la
            # signature d'un double envoi. On avertit et on demande confirmation,
            # plutôt que de trancher à la place de l'utilisateur.
            raise SourceCopyError(
                "DOUBLON DÉTECTÉ : %s et %s portent la même empreinte (%s…). "
                "Deux pages identiques sont parfois légitimes — deux pages blanches, "
                "un document répétitif — mais c'est aussi la signature d'un double "
                "envoi. Confirmez explicitement avec --autoriser-doublons si les deux "
                "pages figurent réellement dans la copie."
                % (seen[digest], nom_soumis, digest[:16]))
        seen.setdefault(digest, nom_soumis)
        _check_not_bound_elsewhere(session, digest, assessment_id, allow_shared)
        prepared.append({"path": path, "media_type": media_type, "sha256": digest,
                         "byte_size": path.stat().st_size,
                         "original_name": nom_soumis})

    kinds = {p["media_type"] for p in prepared}
    if "application/pdf" in kinds and len(kinds) > 1:
        raise SourceCopyError("un rattachement porte soit un PDF, soit des images, "
                              "pas les deux : l'ordre des pages ne serait pas défini.")
    if "application/pdf" in kinds and len(prepared) > 1:
        raise SourceCopyError("un seul PDF par copie. Plusieurs PDF distincts sont "
                              "plusieurs pièces : rattachez-les séparément.")
    return prepared


def attach(session, assessment, paths, label=None, note=None, allow_shared=False,
           replace=False, derived_from=None, source_kind=REAL_STUDENT_COPY,
           original_names=None, is_synthetic=False,
           allow_duplicates=False) -> SourceCopy:
    """Rattache une copie réelle à une évaluation. Les originaux ne sont pas touchés.

    ``paths`` est soit un PDF multipage unique, soit une liste d'images dans l'ordre
    des pages. L'ordre fourni est l'ordre enregistré : il n'est jamais réordonné sur
    la foi d'un nom de fichier.
    """
    if not isinstance(assessment, Assessment):
        raise SourceCopyError("évaluation inconnue.")
    existing = current_copy(session, assessment.assessment_id)
    if existing is not None and not replace:
        raise SourceCopyError(
            "une copie est déjà rattachée à %s (pièce n° %d). Rien n'est écrasé ici : "
            "relancez avec --remplacer pour que l'ancienne devienne SUPERSEDED, ce qui "
            "la conserve." % (assessment.assessment_id, existing.source_copy_id))
    if derived_from is not None:
        if derived_from.assessment_id != assessment.assessment_id:
            raise SourceCopyError("une pièce dérivée appartient à la même évaluation "
                                  "que son original.")
        if derived_from.origin != ORIGIN_ORIGINAL:
            raise SourceCopyError("une pièce dérivée dérive d'un original, "
                                  "pas d'un autre dérivé.")

    prepared = _prepare(paths, assessment.assessment_id, session, allow_shared,
                        original_names=original_names,
                        allow_duplicates=allow_duplicates)

    copy = SourceCopy(
        assessment_id=assessment.assessment_id,
        source_kind=source_kind,
        origin=ORIGIN_DERIVED if derived_from is not None else ORIGIN_ORIGINAL,
        derived_from_id=derived_from.source_copy_id if derived_from is not None else None,
        label=label, note=note, status=STATUS_ATTACHED, is_immutable=True,
        is_synthetic=bool(is_synthetic),
        file_count=len(prepared), page_count=None)
    session.add(copy)
    session.flush()      # l'identifiant est nécessaire pour construire le répertoire

    root = Path(config.SOURCE_COPIES_DIR) / safe_slug(assessment.assessment_id) / (
        "copy_%d" % copy.source_copy_id)
    root.mkdir(parents=True, exist_ok=True)
    _restreindre(root)

    written = []
    try:
        for index, spec in enumerate(prepared, start=1):
            stem = safe_slug(Path(spec["original_name"]).stem)[:40] or "PAGE"
            target = root / ("%02d_%s%s" % (index, stem, EXTENSIONS[spec["media_type"]]))
            # copy2 : les octets et les dates de l'original sont préservés, et
            # l'original lui-même n'est ni déplacé ni modifié.
            _cible_libre(target)
            shutil.copy2(spec["path"], target)
            observed = sha256_file(target)
            if observed != spec["sha256"]:
                raise SourceCopyError("la copie de %s ne correspond pas à l'original "
                                      "(empreinte différente après recopie)."
                                      % spec["path"].name)
            target.chmod(0o400)
            written.append(target)
            session.add(SourceCopyFile(
                source_copy_id=copy.source_copy_id, page_index=index,
                original_name=spec["original_name"], media_type=spec["media_type"],
                byte_size=spec["byte_size"], sha256=spec["sha256"],
                stored_path=str(target.relative_to(Path(config.RUNTIME_DIR)))))
    except Exception:
        for target in written:
            try:
                target.chmod(0o600)
                target.unlink()
            except OSError:
                pass
        raise

    if len(prepared) == 1 and prepared[0]["media_type"] == "application/pdf":
        copy.page_count = pdf_page_count(written[0])
    else:
        copy.page_count = len(prepared)

    if existing is not None:
        existing.status = STATUS_SUPERSEDED
        audit(session, "source_copy.superseded", "source_copy", existing.source_copy_id,
              assessment.assessment_id, new_value=STATUS_SUPERSEDED,
              reason="remplacée par la pièce n° %d" % copy.source_copy_id)

    audit(session, "source_copy.attached", "source_copy", copy.source_copy_id,
          assessment.assessment_id,
          new_value="%d fichier(s) ; %s" % (len(prepared),
                                            ", ".join(p["sha256"][:16] for p in prepared)),
          reason=note)
    session.flush()
    return copy


def attach_derived_pages(session, assessment, original, page_specs, dpi=None,
                         label=None, note=None, source_kind=DERIVED_PAGE_IMAGES,
                         replaces=None) -> SourceCopy:
    """Enregistre un jeu de pages rastérisées dérivé d'une pièce originale.

    ``page_specs`` est une liste ordonnée de dictionnaires ``{path, width, height}``
    déjà produits par la rastérisation. Contrairement à ``attach``, deux pages de
    contenu identique sont acceptées : deux pages blanches d'un même scan ont
    légitimement la même empreinte, et ce n'est pas une erreur de saisie.

    L'original n'est pas touché. Un jeu antérieur devient ``SUPERSEDED``.
    """
    if not page_specs:
        raise SourceCopyError("aucune page à enregistrer.")
    ancien = replaces if replaces is not None else derived_pages(session, original)

    copy = SourceCopy(
        assessment_id=assessment.assessment_id,
        source_kind=source_kind,
        origin=ORIGIN_DERIVED,
        derived_from_id=original.source_copy_id,
        label=label or ("pages rendues à %d dpi" % dpi if dpi else "pages rendues"),
        note=note, status=STATUS_ATTACHED, is_immutable=True,
        is_synthetic=bool(original.is_synthetic),
        file_count=len(page_specs), page_count=len(page_specs))
    session.add(copy)
    session.flush()

    root = Path(config.SOURCE_COPIES_DIR) / safe_slug(assessment.assessment_id) / (
        "derived_%d" % copy.source_copy_id)
    root.mkdir(parents=True, exist_ok=True)
    _restreindre(root)

    written = []
    try:
        for index, spec in enumerate(page_specs, start=1):
            source = Path(spec["path"])
            target = root / ("page_%03d.png" % index)
            _cible_libre(target)
            shutil.copy2(source, target)
            digest = sha256_file(target)
            target.chmod(0o400)
            written.append(target)
            session.add(SourceCopyFile(
                source_copy_id=copy.source_copy_id, page_index=index,
                original_name=source.name, media_type="image/png",
                byte_size=target.stat().st_size, sha256=digest,
                stored_path=str(target.relative_to(Path(config.RUNTIME_DIR))),
                width_px=spec.get("width"), height_px=spec.get("height"),
                dpi=dpi, rotation=int(spec.get("rotation") or 0)))
    except Exception:
        for target in written:
            try:
                target.chmod(0o600)
                target.unlink()
            except OSError:
                pass
        raise

    if ancien is not None:
        ancien.status = STATUS_SUPERSEDED

    audit(session, "source_copy.rasterised", "source_copy", copy.source_copy_id,
          assessment.assessment_id,
          new_value="%d page(s) rendues depuis la pièce n° %d"
                    % (len(page_specs), original.source_copy_id))
    session.flush()
    return copy


# ------------------------------------------------------- mode et garde-fous
def correction_mode() -> str:
    return config.settings.correction_mode


def guard(session, assessment) -> list:
    """Ce qui empêche de corriger en mode numérique. Vide en mode humain.

    Le mode humain est le mode historique : il n'exige aucune pièce jointe, et les
    dossiers déjà corrigés continuent de fonctionner sans qu'aucune copie numérique
    ne soit inventée pour eux.
    """
    if correction_mode() != "digital":
        return []
    copy = current_copy(session, assessment.assessment_id)
    if copy is None:
        return ["mode copie numérisée : aucune copie élève n'est rattachée à cette "
                "évaluation. La correction ne peut pas s'appuyer sur une source "
                "observable qui n'existe pas."]
    report = verify(session, copy)
    if not report["ok"]:
        details = ", ".join([c["path"] for c in report["changed"]] + report["missing"])
        return ["mode copie numérisée : l'empreinte de la copie rattachée ne se vérifie "
                "plus (%s)." % (details or "aucun fichier")]
    return []
