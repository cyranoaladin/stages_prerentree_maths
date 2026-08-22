"""Planches contact : toutes les pages d'un PDF sur quelques images, pour l'inspection.

Le contrôle automatique de densité (`qa_pdf.py`) trouve les pages presque vides. Il ne voit
ni un tableau qui déborde, ni une figure qui chevauche son voisin, ni un titre resté seul en
bas de page, ni une formule coupée. Cela se voit, et seulement cela.

Une planche porte douze pages numérotées. La résolution suffit à repérer une anomalie de
mise en page ; pour lire le texte d'une page suspecte, on la rend seule à pleine résolution.

Usage : python3 tools/qa_planches.py <motif> [dossier de sortie]
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist" / "terminale"
COLONNES, LIGNES = 4, 3
PAR_PLANCHE = COLONNES * LIGNES
DPI = 42
MARGE = 6
ETIQUETTE = 14


def rendu(pdf: Path, dossier: Path) -> list[Path]:
    subprocess.run(["pdftoppm", "-png", "-r", str(DPI), str(pdf), str(dossier / "p")],
                   check=True, capture_output=True)
    return sorted(dossier.glob("p-*.png"))


def planche(images: list[Path], premier: int, sortie: Path) -> None:
    """Assemble jusqu'à douze pages en une grille, chacune numérotée."""
    vignettes = [Image.open(chemin).convert("RGB") for chemin in images]
    largeur = max(v.width for v in vignettes)
    hauteur = max(v.height for v in vignettes)
    planche = Image.new(
        "RGB",
        (COLONNES * (largeur + MARGE) + MARGE,
         LIGNES * (hauteur + MARGE + ETIQUETTE) + MARGE),
        (210, 214, 220),
    )
    for index, vignette in enumerate(vignettes):
        colonne, ligne = index % COLONNES, index // COLONNES
        x = MARGE + colonne * (largeur + MARGE)
        y = MARGE + ligne * (hauteur + MARGE + ETIQUETTE) + ETIQUETTE
        planche.paste(vignette, (x, y))
        # Le numéro de page est écrit en pixels : sans police garantie, un texte dessiné
        # échouerait sur une machine dépourvue de fontes bitmap.
        for point in range(min(premier + index, 60)):
            planche.paste(Image.new("RGB", (2, 6), (30, 40, 60)),
                          (x + 2 + point * 4, y - ETIQUETTE + 4))
    planche.save(sortie)


def main(argv: list[str]) -> int:
    motif = argv[1] if len(argv) > 1 else "*.pdf"
    sortie = Path(argv[2]) if len(argv) > 2 else Path(tempfile.mkdtemp(prefix="planches-"))
    sortie.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(DIST.rglob(motif))
    if not pdfs:
        print(f"aucun PDF ne correspond à {motif} sous {DIST}")
        return 1
    total = 0
    for pdf in pdfs:
        with tempfile.TemporaryDirectory() as travail:
            pages = rendu(pdf, Path(travail))
            for debut in range(0, len(pages), PAR_PLANCHE):
                lot = pages[debut:debut + PAR_PLANCHE]
                nom = f"{pdf.stem}__p{debut + 1:02d}-{debut + len(lot):02d}.png"
                planche(lot, debut + 1, sortie / nom)
                total += 1
        print(f"  {pdf.name} : {len(pages)} pages")
    print(f"\n{total} planche(s) sous {sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
