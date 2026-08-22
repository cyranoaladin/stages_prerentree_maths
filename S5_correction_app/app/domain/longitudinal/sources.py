# -*- coding: utf-8 -*-
"""Collecte et empreinte des sources d'un bilan longitudinal.

Deux exigences, également importantes :

* **ne rien supposer.** Les chemins ne sont pas devinés à partir d'une convention
  de nommage : ils sont lus dans le profil d'apprentissage de l'élève, qui les
  déclare, puis vérifiés sur le disque ;
* **dire ce qui manque.** Une source absente est enregistrée avec ``present =
  False`` et une note, jamais omise en silence. Un bilan doit pouvoir énoncer ce
  qu'il n'a pas pu lire, faute de quoi le lecteur croit qu'il a tout lu.

Chaque source présente est empreintée en SHA-256. Pour un répertoire de séance,
l'empreinte est celle de la liste triée « nom + empreinte » de ses fichiers : deux
collectes donnent le même condensé si et seulement si le contenu est identique.
"""

import hashlib
import os

from ... import config

SESSIONS = ("S1", "S2", "S3", "S4", "S5")

# Rôle attribué à une source d'après son chemin. L'ordre compte : la première
# règle qui s'applique gagne.
_ROLE_RULES = (
    ("Test_Initial", "initial_diagnostic_instrument", "diagnostic initial"),
    ("Dossier_Individuel", "individual_dossier", "dossier individuel de l'élève"),
    ("Remediation_Ciblee", "remediation", "plan de remédiation ciblée"),
    ("02_SEANCES", "session_material", "matériel de séance du niveau"),
    ("DOSSIER_ELEVE_PERSONNALISE", "personalised_session_dossier",
     "dossier de séance personnalisé"),
    ("LIVRETS", "personalised_session_dossier", "livrets de séance personnalisés"),
)


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_dir(path) -> str:
    """Empreinte stable d'un répertoire : nom et contenu de chaque fichier."""
    h = hashlib.sha256()
    for racine, dossiers, fichiers in os.walk(path):
        dossiers[:] = sorted(d for d in dossiers if d != "__pycache__")
        for nom in sorted(fichiers):
            complet = os.path.join(racine, nom)
            h.update(os.path.relpath(complet, path).encode("utf-8"))
            h.update(sha256_file(complet).encode("ascii"))
    return h.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _classify(relative_path: str):
    for motif, role, libelle in _ROLE_RULES:
        if motif in relative_path:
            return role, libelle
    return "other", "source complémentaire"


def _sessions_of(relative_path: str) -> list:
    """Séances concernées par un chemin.

    Un document peut en couvrir plusieurs : « LIVRETS_S4_S5_PERSONNALISES » vaut
    pour la quatrième et la cinquième séance. Ne retenir que la première le ferait
    déclarer manquant pour la seconde, ce qui serait faux.
    """
    trouvees = []
    for s in SESSIONS:
        if (relative_path.endswith("/%s" % s) or ("/%s/" % s) in relative_path
                or ("_%s_" % s) in relative_path or ("_%s." % s) in relative_path):
            trouvees.append(s)
    return trouvees


def _session_of(relative_path: str):
    """Première séance concernée, ou None. Conservé pour la lisibilité des relevés."""
    trouvees = _sessions_of(relative_path)
    return trouvees[0] if trouvees else None


def _record(role, source_type, relative_path, session=None, note=None):
    complet = os.path.join(str(config.REPO_ROOT), relative_path)
    present = os.path.exists(complet)
    empreinte = None
    if present:
        empreinte = sha256_dir(complet) if os.path.isdir(complet) else sha256_file(complet)
    return {
        "role": role, "source_type": source_type, "source_path": relative_path,
        "source_sha256": empreinte, "session": session, "present": present,
        "note": note if present else (note or "source déclarée mais introuvable sur le disque"),
    }


def collect(profile: dict, profile_path: str = None) -> list:
    """Sources d'un élève, d'après son profil d'apprentissage.

    Le profil lui-même est enregistré comme source : il est l'intrant normalisé du
    diagnostic initial et de la trajectoire de stage, et son empreinte doit figurer
    au manifeste du bilan.
    """
    releves = []

    if profile_path:
        chemin = os.path.relpath(str(profile_path), str(config.REPO_ROOT))
        releves.append(_record("learning_profile", "student_learning_profile", chemin))

    instrument = (profile.get("baseline") or {}).get("instrument") or {}
    fichier = instrument.get("file")
    declarees = list(profile.get("sources") or [])
    if fichier and fichier not in declarees:
        declarees.append(fichier)

    for brut in declarees:
        chemin = brut.get("path") if isinstance(brut, dict) else brut
        if not chemin:
            continue
        role, libelle = _classify(chemin)
        releve = _record(role, libelle, chemin, session=_session_of(chemin))
        releve["sessions_covered"] = _sessions_of(chemin)
        releves.append(releve)

    # Séances sans dossier personnalisé : le constat est porté explicitement plutôt
    # que déduit d'une absence. Le matériel de niveau existe pour les cinq séances ;
    # le dossier nominatif, lui, n'a pas été produit pour toutes.
    avec_dossier = set()
    for r in releves:
        if r["role"] == "personalised_session_dossier" and r["present"]:
            avec_dossier.update(_sessions_of(r["source_path"] or ""))
    for s in SESSIONS:
        if s not in avec_dossier:
            releves.append({
                "role": "personalised_session_dossier", "source_type":
                    "dossier de séance personnalisé", "source_path": None,
                "source_sha256": None, "session": s, "present": False,
                "note": "aucun dossier de séance personnalisé n'a été produit pour %s ; "
                        "le matériel de niveau reste la seule source documentaire" % s,
            })

    return releves


def missing(releves) -> list:
    return [r for r in releves if not r["present"]]


def summary(releves) -> dict:
    return {
        "total": len(releves),
        "present": sum(1 for r in releves if r["present"]),
        "missing": sum(1 for r in releves if not r["present"]),
        "roles": sorted({r["role"] for r in releves}),
    }
