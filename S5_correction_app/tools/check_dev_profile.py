#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le profil de développement est-il complet ?

Une porte de fermeture qui passe au vert parce qu'un test critique a été ignoré ne
démontre rien. Cet outil déclare l'environnement **incomplet** plutôt que de laisser
la porte réussir silencieusement sans couverture navigateur.

    make s5-full-gate      # échoue ici si le profil est incomplet
"""

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

EXIGENCES = [
    ("playwright (module)", lambda: importlib.util.find_spec("playwright") is not None,
     "pip install --user playwright"),
    ("chromium (navigateur)", lambda: _chromium_present(),
     "python3 -m playwright install chromium"),
    ("poppler (pdftoppm)", lambda: shutil.which("pdftoppm") is not None,
     "apt install poppler-utils"),
    ("poppler (pdfinfo)", lambda: shutil.which("pdfinfo") is not None,
     "apt install poppler-utils"),
    ("pillow", lambda: importlib.util.find_spec("PIL") is not None,
     "pip install --user pillow"),
    ("ruff", lambda: importlib.util.find_spec("ruff") is not None,
     "pip install --user ruff"),
]


def _chromium_present() -> bool:
    if importlib.util.find_spec("playwright") is None:
        return False
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            navigateur = p.chromium.launch()
            navigateur.close()
        return True
    except Exception:
        return False


def versions() -> dict:
    """Ce dont dépend le diagnostic, quand un rendu se comporte autrement demain."""
    def sortie(argv):
        # poppler écrit sa version sur la sortie d'erreur : ne lire que stdout
        # donnait « indisponible » alors que l'outil était bien présent.
        try:
            done = subprocess.run(argv, capture_output=True, text=True, timeout=20)
            texte = (done.stdout or "") + (done.stderr or "")
            lignes = [l for l in texte.splitlines() if l.strip()]
            return lignes[0] if lignes else "indisponible"
        except Exception:
            return "indisponible"
    import sqlite3
    from app import APP_VERSION, DOMAIN_SCHEMA_VERSION
    return {
        "python": sys.version.split()[0],
        "sqlite": sqlite3.sqlite_version,
        "pdftoppm": sortie(["pdftoppm", "-v"]),
        "chromium": _version_chromium(),
        "application": APP_VERSION,
        "schema": DOMAIN_SCHEMA_VERSION,
    }


def _version_chromium() -> str:
    if importlib.util.find_spec("playwright") is None:
        return "absent"
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            navigateur = p.chromium.launch()
            version = navigateur.version
            navigateur.close()
        return version
    except Exception:
        return "indisponible"


def main() -> int:
    manquants = []
    print("PROFIL DE DÉVELOPPEMENT")
    for nom, present, remede in EXIGENCES:
        ok = present()
        print("  %-24s %s" % (nom, "présent" if ok else "ABSENT — %s" % remede))
        if not ok:
            manquants.append(nom)
    print()
    print("VERSIONS")
    for cle, valeur in versions().items():
        print("  %-24s %s" % (cle, valeur))
    print()
    if manquants:
        print("ENVIRONNEMENT INCOMPLET : %s" % ", ".join(manquants))
        print("La porte de fermeture s'arrête ici. Un test critique ignoré ne "
              "démontre rien,\net un « skip » ne doit pas se confondre avec un succès.")
        return 1
    print("PROFIL COMPLET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
