"""Contrôle qualité des PDF produits : ce qu'on ne voit pas en lisant le Markdown.

Trois familles de défauts échappent à la relecture du source et n'apparaissent qu'à
l'impression : ce qui déborde de la justification, ce qui laisse une page presque vide, et
ce qui laisse un titre seul en bas de page. LaTeX signale le premier dans son journal ; les
deux autres se mesurent sur le PDF fini.

Usage : python3 tools/qa_pdf.py [dossier]
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "dist" / "terminale"

# En deçà de cette proportion de caractères par rapport à la page médiane du document, une
# page est presque vide. Une page de fin de document l'est légitimement ; une page au milieu
# signale une rupture de page mal placée.
SPARSE_RATIO = 0.18


def page_texts(pdf: Path) -> list[str]:
    result = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"pdftotext a échoué sur {pdf}")
    return result.stdout.split("\f")[:-1]


def inspect(pdf: Path) -> list[str]:
    """Les anomalies de mise en page d'un document, en clair."""
    pages = page_texts(pdf)
    if not pages:
        return [f"{pdf.name} : aucune page lisible"]
    sizes = sorted(len(page.strip()) for page in pages)
    median = sizes[len(sizes) // 2] or 1
    problems: list[str] = []
    for number, page in enumerate(pages, 1):
        body = page.strip()
        # La dernière page d'un document est courte par nature, et la couverture aussi.
        if number in (1, len(pages)):
            continue
        if len(body) < SPARSE_RATIO * median:
            problems.append(
                f"{pdf.name} : page {number}/{len(pages)} presque vide "
                f"({len(body)} caractères contre {median} en médiane)"
            )
    return problems


def main(argv: list[str]) -> int:
    target = Path(argv[1]) if len(argv) > 1 else DEFAULT
    pdfs = sorted(target.rglob("*.pdf"))
    if not pdfs:
        print(f"aucun PDF sous {target}")
        return 1
    problems: list[str] = []
    for pdf in pdfs:
        problems.extend(inspect(pdf))
    print(f"{len(pdfs)} PDF inspectés, {sum(len(page_texts(p)) for p in pdfs)} pages.")
    if problems:
        print(f"\n{len(problems)} anomalie(s) de mise en page :")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("Aucune page presque vide au milieu d'un document.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
