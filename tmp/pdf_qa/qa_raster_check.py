#!/usr/bin/env python3
"""QA Visuelle et textuelle exhaustive des PDF générés pour Nexus Réussite."""

import pathlib
import subprocess
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
PDF_DIR = ROOT / "dist" / "pdf"
PACKS_DIR = ROOT / "dist" / "packs"
TMP_QA_DIR = ROOT / "tmp" / "pdf_qa" / "renders"
TMP_QA_DIR.mkdir(parents=True, exist_ok=True)

def verify_pdf_titles_with_pdftotext():
    print("=== 1. Vérification textuelle pdftotext des titres PDF ===")
    all_pdfs = list(PDF_DIR.rglob("*.pdf")) + list(PACKS_DIR.rglob("*.pdf"))
    errors = 0
    checked = 0
    for pdf in all_pdfs:
        res = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Échec pdftotext sur {pdf.name}")
            errors += 1
            continue
        checked += 1
        txt = res.stdout.strip()
        lines = [l.strip() for l in txt.splitlines() if l.strip()][:5]
        for l in lines:
            if re.search(r'\b(4e|3e|2nde|1ere_spe|1re_nsi)_S\d_', l) or (l.count("_") > 1 and "http" not in l):
                print(f"ALERTE Titre technique dans {pdf.relative_to(ROOT)}: '{l}'")
                errors += 1
    print(f"pdftotext : {checked} PDF vérifiés, {errors} erreurs trouvées.")
    assert errors == 0, f"{errors} titres techniques trouvés dans les PDF !"

def rasterize_key_pdfs():
    print("=== 2. QA Visuelle : Rasterization PNG des premières pages ===")
    key_packs = [
        # Packs Maths 4e, 3e, 2nde, 1ere_spe
        PACKS_DIR / "eleves" / "4e_PACK_ELEVE_COMPLET.pdf",
        PACKS_DIR / "eleves" / "4e_S1_PACK_ELEVE.pdf",
        PACKS_DIR / "enseignants" / "4e_S1_PACK_ENSEIGNANT.pdf",
        PACKS_DIR / "eleves" / "3e_S1_PACK_ELEVE.pdf",
        PACKS_DIR / "enseignants" / "3e_S1_PACK_ENSEIGNANT.pdf",
        PACKS_DIR / "eleves" / "2nde_S1_PACK_ELEVE.pdf",
        PACKS_DIR / "enseignants" / "2nde_S1_PACK_ENSEIGNANT.pdf",
        PACKS_DIR / "eleves" / "1ere_spe_S1_PACK_ELEVE.pdf",
        PACKS_DIR / "enseignants" / "1ere_spe_S1_PACK_ENSEIGNANT.pdf",
        # NSI
        ROOT / "1re_nsi" / "08_PACKS_PDF" / "1re_nsi_PACK_ELEVE_COMPLET.pdf",
        ROOT / "1re_nsi" / "08_PACKS_PDF" / "1re_nsi_PACK_ENSEIGNANT_COMPLET.pdf",
    ]
    
    rasterized = 0
    for pdf in key_packs:
        if not pdf.exists():
            print(f"Pack introuvable pour QA visuelle : {pdf}")
            continue
        output_prefix = TMP_QA_DIR / pdf.stem
        cmd = ["pdftoppm", "-png", "-f", "1", "-l", "1", str(pdf), str(output_prefix)]
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode == 0:
            rasterized += 1
            png_file = list(TMP_QA_DIR.glob(f"{pdf.stem}*.png"))
            if png_file:
                print(f"Rasterisé : {pdf.name} -> {png_file[-1].name}")
        else:
            print(f"Échec pdftoppm sur {pdf.name}")
    print(f"Rasterization terminée : {rasterized} pages clés générées en PNG dans {TMP_QA_DIR}")

if __name__ == "__main__":
    verify_pdf_titles_with_pdftotext()
    rasterize_key_pdfs()
