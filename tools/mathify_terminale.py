#!/usr/bin/env python3
"""Réécrit les documents Terminale rédigés à la main en notation LaTeX.

Les documents nominatifs n'ont pas besoin de ce passage : `tools/build_terminale.py`
applique la même conversion à chaque génération. Ce script s'adresse aux documents
écrits directement — séances, évaluations, guides, programmes — dont la source est le
fichier Markdown lui-même.

La conversion est faite une fois et le résultat est committé : la source du dépôt porte
désormais de vraies mathématiques, relues et modifiables, et non une transformation
opérée à l'impression que personne ne pourrait corriger.

Usage :
    python3 tools/mathify_terminale.py --check    # signale ce qui reste à convertir
    python3 tools/mathify_terminale.py            # réécrit les fichiers
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.latex_notation import to_latex, unsupported_characters  # noqa: E402

# Modules concernés, et pour chacun le répertoire des documents nominatifs, qui est
# produit par le générateur et ne doit pas être réécrit ici.
MODULE_DIRECTORIES = {
    "tle_spe": "04_NOMINATIFS",
    "tle_nsi": "05_NOMINATIFS",
    "tle_pc": "04_NOMINATIFS",
}
# La physique-chimie seule active la reconnaissance des formules et des unités : hors
# de ce module, « A + B → C » est une étape d'algorithme, pas une réaction.
CHEMISTRY_MODULES = {"tle_pc"}


def handwritten_documents(root: Path = ROOT) -> list[Path]:
    paths: list[Path] = []
    for module, nominative in MODULE_DIRECTORIES.items():
        base = root / module
        if not base.is_dir():
            continue
        paths += [
            path for path in sorted(base.rglob("*.md"))
            if nominative not in path.parts and "00_MASTER/index.md" not in path.as_posix()
        ]
    return paths


def module_of(path: Path, root: Path = ROOT) -> str:
    return path.relative_to(root).parts[0]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="ne rien écrire ; signaler les documents à convertir")
    args = parser.parse_args(argv)

    pending: list[str] = []
    changed = 0
    for path in handwritten_documents():
        original = path.read_text(encoding="utf-8")
        converted = to_latex(original, chemistry=module_of(path) in CHEMISTRY_MODULES)
        left = unsupported_characters(converted)
        if left:
            pending.append(
                f"{path.relative_to(ROOT)} : « {' '.join(left)} » sans traduction LaTeX"
            )
        if converted == original:
            continue
        if args.check:
            pending.append(f"{path.relative_to(ROOT)} : notation à convertir")
        else:
            path.write_text(converted, encoding="utf-8")
            changed += 1

    if pending:
        print(f"ÉCHEC : {len(pending)} point(s) à traiter.")
        for line in pending:
            print(f"  - {line}")
        return 1
    print(f"OK : {changed} document(s) réécrit(s)." if not args.check
          else "OK : tous les documents rédigés à la main sont en notation LaTeX.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
