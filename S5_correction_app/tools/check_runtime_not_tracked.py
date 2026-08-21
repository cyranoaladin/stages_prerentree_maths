#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Échoue si une donnée réelle de correction est suivie par Git.

Le dépôt peut être public. Une base SQLite, un bilan parents ou un export de correction
qui s'y retrouverait exposerait des données personnelles d'élèves.
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

INTERDITS = (
    "S5_correction_app/runtime/",
    "responses_reelles/",
    "copies_eleves/",
    "bilans_finaux/",
    "corrections_reelles/",
)
SUFFIXES = (".sqlite", ".sqlite3", ".sqlite3-wal", ".sqlite3-shm")


def tracked_files():
    result = subprocess.run(["git", "ls-files"], cwd=str(REPO), capture_output=True,
                            text=True, check=False)
    if result.returncode != 0:
        return None
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    files = tracked_files()
    if files is None:
        print("dépôt Git introuvable : contrôle non exécuté", file=sys.stderr)
        return 0
    fautifs = []
    for path in files:
        if any(path.startswith(prefix) for prefix in INTERDITS):
            fautifs.append(path)
        elif path.endswith(SUFFIXES):
            fautifs.append(path)
    if fautifs:
        print("DONNÉES RÉELLES SUIVIES PAR GIT :", file=sys.stderr)
        for path in fautifs:
            print("  %s" % path, file=sys.stderr)
        print("Retirez-les de l'index avant tout push : git rm --cached <fichier>",
              file=sys.stderr)
        return 1
    print("aucune donnée réelle de correction n'est suivie par Git (%d fichiers contrôlés)"
          % len(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
