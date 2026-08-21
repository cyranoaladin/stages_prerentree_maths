# -*- coding: utf-8 -*-
"""Garde-fous : chemins, noms de fichiers, jetons de formulaire, sous-processus.

Rien ici n'est décoratif. Chaque fonction ferme une porte précise :

* ``resolve_document`` empêche qu'une route de document serve un fichier hors des
  racines autorisées, quelle que soit la forme du chemin demandé ;
* ``safe_slug`` empêche qu'un nom d'élève se retrouve interprété par un shell ou par le
  système de fichiers ;
* ``run_command`` interdit ``shell=True`` par construction ;
* les jetons de formulaire ferment la porte CSRF si l'application est un jour exposée.
"""

import hashlib
import hmac
import os
import re
import secrets
import subprocess
import time
import unicodedata
from pathlib import Path
from typing import Iterable, Sequence

from . import config


class SecurityError(Exception):
    pass


# ------------------------------------------------------------------- chemins
def resolve_document(candidate: str, roots: Iterable[Path] = None) -> Path:
    """Résout un chemin de document et refuse tout ce qui sort des racines autorisées.

    Refuse : les chemins absolus arbitraires, ``..`` sous toutes ses formes, les liens
    symboliques qui pointent hors des racines, et les fichiers inexistants.
    """
    roots = [Path(r).resolve() for r in (roots or config.DOCUMENT_ROOTS)]
    raw = (candidate or "").strip()
    if not raw:
        raise SecurityError("chemin de document vide")
    if "\x00" in raw:
        raise SecurityError("chemin de document invalide")
    p = Path(raw)
    if not p.is_absolute():
        p = (config.REPO_ROOT / p)
    try:
        resolved = p.resolve(strict=True)
    except (OSError, RuntimeError):
        raise SecurityError("document introuvable : %s" % raw)
    for root in roots:
        try:
            resolved.relative_to(root)
        except ValueError:
            continue
        if not resolved.is_file():
            raise SecurityError("le chemin demandé n'est pas un fichier")
        return resolved
    raise SecurityError("chemin hors des racines autorisées")


def is_inside(path: Path, root: Path) -> bool:
    try:
        Path(path).resolve().relative_to(Path(root).resolve())
        return True
    except (ValueError, OSError):
        return False


# --------------------------------------------------------------------- noms
_SLUG_KEEP = re.compile(r"[^A-Za-z0-9_-]+")


def safe_slug(value: str, fallback: str = "SANS_NOM") -> str:
    """Identifiant de fichier sûr : ASCII, majuscules, tirets bas. Jamais vide."""
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.replace(" ", "_").replace("'", "_").replace("-", "_")
    text = _SLUG_KEEP.sub("_", text).strip("_")
    text = re.sub(r"_{2,}", "_", text).upper()
    return text[:80] or fallback


def safe_filename(name: str) -> str:
    """Nom de fichier sans séparateur ni composant relatif."""
    base = os.path.basename(str(name or ""))
    if base in ("", ".", ".."):
        raise SecurityError("nom de fichier invalide")
    if any(sep in base for sep in ("/", "\\", "\x00")):
        raise SecurityError("nom de fichier invalide")
    return base


# ------------------------------------------------------------------- jetons
_SECRET = os.environ.get("NEXUS_S5_SECRET") or secrets.token_hex(32)


def issue_token(scope: str = "form") -> str:
    stamp = str(int(time.time()))
    sig = hmac.new(_SECRET.encode(), ("%s:%s" % (scope, stamp)).encode(),
                   hashlib.sha256).hexdigest()[:32]
    return "%s.%s" % (stamp, sig)


def check_token(token: str, scope: str = "form", max_age: int = 24 * 3600) -> bool:
    try:
        stamp, sig = str(token).split(".", 1)
        expected = hmac.new(_SECRET.encode(), ("%s:%s" % (scope, stamp)).encode(),
                            hashlib.sha256).hexdigest()[:32]
        if not hmac.compare_digest(sig, expected):
            return False
        return (int(time.time()) - int(stamp)) <= max_age
    except (ValueError, TypeError):
        return False


# ------------------------------------------------------------- sous-processus
def run_command(argv: Sequence[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess:
    """Exécute une commande. ``shell=True`` n'est pas une option ici, jamais.

    Le premier argument doit être un exécutable connu ; les suivants sont passés tels
    quels au système, sans interprétation par un shell.
    """
    if not argv or not isinstance(argv, (list, tuple)):
        raise SecurityError("commande invalide")
    for arg in argv:
        if not isinstance(arg, str) or "\x00" in arg:
            raise SecurityError("argument de commande invalide")
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
           "HOME": str(cwd),
           "TEXMFVAR": str(Path(cwd) / ".texmf"),
           "LANG": os.environ.get("LANG", "C.UTF-8"),
           "SOURCE_DATE_EPOCH": "1755734400"}
    # errors="replace" : un journal LaTeX peut contenir des octets non UTF-8 ; ce n'est
    # pas une raison pour perdre le message d'erreur.
    return subprocess.run(list(argv), cwd=str(cwd), env=env, capture_output=True,
                          encoding="utf-8", errors="replace", timeout=timeout,
                          shell=False, check=False)


# ------------------------------------------------------------------ hachage
def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
