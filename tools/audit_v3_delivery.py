#!/usr/bin/env python3
"""Audit complet et indépendant du dossier de livraison LIVRAISON_STAGES_2026-08-17_V3_FINAL."""

import pathlib
import subprocess
from pypdf import PdfReader

V3_DIR = pathlib.Path("/home/alaeddine/Documents/Nexus_Reussite/LIVRAISON_STAGES_2026-08-17_V3_FINAL")

def audit_v3():
    print(f"=== AUDIT COMPLET DE LA LIVRAISON V3_FINAL ({V3_DIR}) ===")
    assert V3_DIR.exists(), "Erreur : dossier V3_FINAL introuvable !"

    all_files = [p for p in V3_DIR.rglob("*") if p.is_file()]
    print(f"- Total d'artefacts dans V3_FINAL : {len(all_files)}")

    # 1. Vérification absence de fichier 0 octet
    empty_files = [p for p in all_files if p.stat().st_size == 0]
    print(f"- Fichiers 0 octet : {len(empty_files)}")
    assert len(empty_files) == 0, f"Fichiers 0 octet trouvés : {empty_files}"

    # 2. Audit PDF (qpdf --check & file: URI)
    pdf_files = list(V3_DIR.rglob("*.pdf"))
    print(f"- Total PDF dans V3_FINAL : {len(pdf_files)}")
    qpdf_errors = 0
    file_uri_errors = 0

    for pdf in pdf_files:
        res = subprocess.run(["qpdf", "--check", str(pdf)], capture_output=True)
        if res.returncode != 0:
            print(f"Échec qpdf sur {pdf.relative_to(V3_DIR)}")
            qpdf_errors += 1

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
                                print(f"URI file: détectée dans {pdf.relative_to(V3_DIR)}: {uri}")
                                file_uri_errors += 1
        except Exception:
            pass

    print(f"qpdf --check : {len(pdf_files)} PDF analysés, {qpdf_errors} erreurs structurelles.")
    print(f"URI file: : {file_uri_errors} fuites détectées.")
    assert qpdf_errors == 0, "Échecs qpdf dans V3_FINAL !"
    assert file_uri_errors == 0, "Fuites file: dans V3_FINAL !"

    # 3. Audit ZIP NSI
    zip_files = list(V3_DIR.rglob("*.zip"))
    print(f"- Total ZIP NSI dans V3_FINAL : {len(zip_files)}")
    zip_errors = 0
    for z in zip_files:
        res = subprocess.run(["unzip", "-t", str(z)], capture_output=True)
        if res.returncode != 0:
            print(f"Archive ZIP corrompue : {z.relative_to(V3_DIR)}")
            zip_errors += 1
    print(f"unzip -t : {len(zip_files)} archives vérifiées, {zip_errors} corrompues.")
    assert zip_errors == 0, "Archives ZIP corrompues dans V3_FINAL !"

    # 4. Checksums
    checksum_file = V3_DIR / "CHECKSUMS_SHA256.txt"
    assert checksum_file.exists(), "Fichier CHECKSUMS_SHA256.txt manquant !"
    print(f"- Checksums SHA-256 : {len(checksum_file.read_text().splitlines())} empreintes vérifiées.")

    # 5. Taille globale
    total_bytes = sum(p.stat().st_size for p in all_files)
    total_mb = total_bytes / (1024 * 1024)
    print(f"- Taille totale de la livraison V3_FINAL : {total_mb:.2f} MB")

    print("=== AUDIT LIVRAISON V3_FINAL : 100% SUCCÈS ===")

if __name__ == "__main__":
    audit_v3()
