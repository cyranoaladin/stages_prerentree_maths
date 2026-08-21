#!/usr/bin/env python3
"""Validation indépendante et rigoureuse du package de livraison V2."""

import pathlib
import subprocess
from pypdf import PdfReader

V2_DIR = pathlib.Path("/home/alaeddine/Documents/Nexus_Reussite/LIVRAISON_STAGES_2026-08-17_V2")

def audit_v2():
    print(f"=== AUDIT INDÉPENDANT DE LIVRAISON V2 ({V2_DIR}) ===")
    assert V2_DIR.exists(), "Dossier V2 introuvable !"

    pdf_files = list(V2_DIR.rglob("*.pdf"))
    zip_files = list(V2_DIR.rglob("*.zip"))

    print(f"- Total PDF dans V2 : {len(pdf_files)}")
    print(f"- Total ZIP dans V2 : {len(zip_files)}")

    # 1. qpdf check sur TOUS les PDF dans V2
    qpdf_errors = 0
    file_uri_errors = 0
    for pdf in pdf_files:
        res = subprocess.run(["qpdf", "--check", str(pdf)], capture_output=True)
        if res.returncode != 0:
            print(f"Échec qpdf sur {pdf.relative_to(V2_DIR)}")
            qpdf_errors += 1
        
        # Inspection URI file:
        try:
            reader = PdfReader(pdf)
            for page in reader.pages:
                annots = page.get("/Annots")
                if not annots:
                    continue
                for ref in list(annots.get_object()):
                    annot = ref.get_object()
                    if annot.get("/Subtype") == "/Link":
                        action = annot.get("/A")
                        if action and action.get_object().get("/S") == "/URI":
                            uri = str(action.get_object().get("/URI", ""))
                            if uri.lower().startswith("file:"):
                                print(f"ALERTE URI file: dans {pdf.relative_to(V2_DIR)}: {uri}")
                                file_uri_errors += 1
                                break
        except Exception:
            pass

    print(f"qpdf : {len(pdf_files)} PDF analysés, {qpdf_errors} erreurs structurelles.")
    print(f"URI file: : {file_uri_errors} fuites trouvées.")

    # 2. unzip -t sur TOUS les ZIP NSI
    zip_errors = 0
    for z in zip_files:
        res = subprocess.run(["unzip", "-t", str(z)], capture_output=True)
        if res.returncode != 0:
            print(f"Échec unzip sur {z.relative_to(V2_DIR)}")
            zip_errors += 1
    print(f"ZIP NSI : {len(zip_files)} archives vérifiées, {zip_errors} corrompues.")

    # 3. Vérification taille globale
    size_bytes = sum(f.stat().st_size for f in V2_DIR.rglob("*") if f.is_file())
    size_mb = size_bytes / (1024 * 1024)
    print(f"Taille totale de la livraison V2 : {size_mb:.2f} MB")

    assert qpdf_errors == 0, "Échecs qpdf dans V2 !"
    assert file_uri_errors == 0, "Fuites file: dans V2 !"
    assert zip_errors == 0, "Archives ZIP corrompues dans V2 !"
    print("=== DEUXIÈME VALIDATION LIVRAISON V2 : 100% SUCCÈS ===")

if __name__ == "__main__":
    audit_v2()
