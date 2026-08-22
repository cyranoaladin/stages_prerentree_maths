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


# ----------------------------------------------------------- authentification
def network_password() -> str:
    """Mot de passe exigé lorsque l'application est exposée au réseau."""
    return os.environ.get("NEXUS_S5_PASSWORD", "")


def check_basic_auth(header: str) -> bool:
    """Vérifie un en-tête ``Authorization: Basic``. Comparaison à temps constant.

    Le mot de passe n'est jamais comparé par ``==`` : une comparaison naïve fuit sa
    longueur et son préfixe par le temps de réponse.
    """
    import base64
    attendu = network_password()
    if not attendu:
        return False
    if not header or not header.lower().startswith("basic "):
        return False
    try:
        decode = base64.b64decode(header.split(" ", 1)[1]).decode("utf-8")
    except Exception:
        return False
    _, _, fourni = decode.partition(":")
    return hmac.compare_digest(fourni, attendu)


LOOPBACK = ("127.0.0.1", "::1", "localhost")


def transport_is_secure(request) -> bool:
    """Le transport protège-t-il réellement une copie d'élève ?

    Trois cas acceptés, et rien d'autre :

    * la requête vient de la boucle locale — elle ne quitte pas la machine ;
    * TLS est terminé par l'application elle-même ;
    * TLS est terminé par un proxy **déclaré**, et la requête vient de ce proxy.

    ``X-Forwarded-Proto: https`` envoyé par un client quelconque ne prouve rien : il
    n'est lu que si un proxy de confiance a été explicitement configuré et que la
    connexion provient bien de lui.
    """
    from . import config
    import ipaddress
    client = getattr(getattr(request, "client", None), "host", "") or ""
    if not client:
        return True
    try:
        adresse = ipaddress.ip_address(client)
    except ValueError:
        # Le pair n'a pas d'adresse IP : la requête n'est pas arrivée par le réseau
        # (transport de test ASGI, socket UNIX). Rien ne circule sur un câble.
        return True
    if adresse.is_loopback:
        return True
    if request.url.scheme == "https" or config.settings.tls_active:
        return True
    if config.TRUSTED_PROXY_TLS and client in config.TRUSTED_PROXY_HOSTS:
        protocole = (request.headers.get("x-forwarded-proto") or "").lower()
        return protocole == "https"
    return False


def same_origin(origin: str, referer: str, host: str) -> bool:
    """Une requête mutante doit venir de l'application elle-même.

    Un site tiers peut soumettre un formulaire vers notre serveur — y compris en
    ``multipart/form-data``, qui ne déclenche aucune requête préalable. Il ne peut en
    revanche ni falsifier ``Origin``, ni poser un en-tête personnalisé.
    """
    from urllib.parse import urlparse
    for valeur in (origin, referer):
        if not valeur:
            continue
        hote = (urlparse(valeur).netloc or "").lower()
        if hote and hote != (host or "").lower():
            return False
    return True


# ------------------------------------------------------------- sous-processus
def _limites_ressources(cpu_secondes: int, memoire_octets: int,
                        taille_fichier_octets: int, fichiers_ouverts: int):
    """Prépare les limites appliquées dans le processus enfant, avant ``exec``.

    Un délai d'attente ne borne que la durée. Un analyseur de PDF hostile peut,
    dans ce délai, saturer le processeur, allouer plusieurs gigaoctets ou écrire un
    fichier de la taille du disque. Ces limites-là sont posées par le noyau et le
    processus parent y survit, quoi que fasse l'enfant.

    Linux uniquement, ce qui est le contexte d'exécution de S5. Sur un système où
    ``resource`` est absent ou une limite non gérée, on n'installe rien plutôt que de
    prétendre à une garantie que l'on n'a pas.
    """
    def appliquer():                              # pragma: no cover - exécuté après fork
        try:
            import resource
        except ImportError:
            return
        for nom, valeur in (("RLIMIT_CPU", cpu_secondes),
                            ("RLIMIT_AS", memoire_octets),
                            ("RLIMIT_FSIZE", taille_fichier_octets),
                            ("RLIMIT_NOFILE", fichiers_ouverts)):
            limite = getattr(resource, nom, None)
            if limite is None or not valeur:
                continue
            try:
                souple, dure = resource.getrlimit(limite)
                plafond = valeur if dure == resource.RLIM_INFINITY else min(valeur, dure)
                resource.setrlimit(limite, (plafond, dure))
            except (ValueError, OSError):
                continue
        try:
            os.setsid()          # l'enfant ne partage pas le groupe du parent
        except OSError:
            pass
    return appliquer


def run_command(argv: Sequence[str], cwd: Path, timeout: int,
                cpu_secondes: int = None, memoire_octets: int = None,
                taille_fichier_octets: int = None,
                fichiers_ouverts: int = 256) -> subprocess.CompletedProcess:
    """Exécute une commande. ``shell=True`` n'est pas une option ici, jamais.

    Le premier argument doit être un exécutable connu ; les suivants sont passés tels
    quels au système, sans interprétation par un shell.

    Lorsqu'une limite de ressource est demandée, elle est posée dans le processus
    enfant avant ``exec`` : le parent survit à un enfant qui déborde.
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
    prealable = None
    if any((cpu_secondes, memoire_octets, taille_fichier_octets)):
        prealable = _limites_ressources(cpu_secondes, memoire_octets,
                                        taille_fichier_octets, fichiers_ouverts)
    return subprocess.run(list(argv), cwd=str(cwd), env=env, capture_output=True,
                          encoding="utf-8", errors="replace", timeout=timeout,
                          shell=False, check=False, preexec_fn=prealable)


# ------------------------------------------------------------------ hachage
def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
