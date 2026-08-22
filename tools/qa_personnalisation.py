"""Contrôle de personnalisation : deux élèves aux bilans différents doivent recevoir deux
documents différents.

Le test décisif est celui du cahier des charges : si l'on retire le prénom de la couverture
et qu'on donne le document à un élève dont le bilan diffère, resterait-il aussi adapté ? Un
écart faible entre deux documents répond « oui » et signale une personnalisation de façade.

Le seuil de 10 % n'est pas une cible marketing : c'est le point en deçà duquel deux cahiers
ne diffèrent plus que par leur en-tête et un ou deux exercices.
"""
from __future__ import annotations

import difflib
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEUIL = 0.10
MODULES = {"tle_spe": "04_NOMINATIFS", "tle_nsi": "05_NOMINATIFS", "tle_pc": "04_NOMINATIFS"}


def cahiers(module: str, folder: str) -> dict[str, list[str]]:
    return {
        path.parent.name: path.read_text(encoding="utf-8").split("\n")
        for path in sorted((ROOT / module / folder).glob(f"*/{module}_Cahier_Seances_*.md"))
    }


def diagnostics_differents(a: str, b: str, cartes: dict[str, dict]) -> bool:
    """Deux élèves ont-ils des bilans réellement différents sur cette matière ?"""
    return cartes.get(a) != cartes.get(b)


def main() -> int:
    registry = json.loads((ROOT / "content/students_terminale.json").read_text(encoding="utf-8"))
    diagnostics = json.loads(
        (ROOT / "content/diagnostics_terminale.json").read_text(encoding="utf-8"))["diagnostics"]
    slugs = {s["slug"]: s for s in registry["students"]}

    problems: list[str] = []
    for module, folder in MODULES.items():
        documents = cahiers(module, folder)
        cartes = {}
        for slug, student in slugs.items():
            for subject in student.get("matieres", []):
                if subject["module"] == module:
                    cartes[slug] = diagnostics[subject["diagnosticId"]]["carte_maitrise_confiance"]
        print(f"\n{module} — {len(documents)} cahier(s)")
        for a, b in itertools.combinations(sorted(documents), 2):
            ecart = 1 - difflib.SequenceMatcher(None, documents[a], documents[b]).ratio()
            marque = ""
            if ecart < SEUIL and diagnostics_differents(a, b, cartes):
                marque = "  <-- bilans différents, cahiers trop proches"
                problems.append(f"{module} : {a} / {b} ({100*ecart:.1f} %)")
            print(f"   {a:24} / {b:24} {100*ecart:5.1f} %{marque}")

    print()
    if problems:
        print(f"{len(problems)} paire(s) insuffisamment différenciée(s) :")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("Aucune paire de cahiers n'est un quasi-doublon d'un bilan différent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
