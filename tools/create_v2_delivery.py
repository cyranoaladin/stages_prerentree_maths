#!/usr/bin/env python3
"""Génération et assemblage déterministe du dossier de livraison V2 et du plan d'impression."""

import os
import shutil
import pathlib
import subprocess
from pypdf import PdfReader

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DELIVERY_V2 = ROOT.parent / "LIVRAISON_STAGES_2026-08-17_V2"

# Données exactes du registre
ENROLLMENT_COUNTS = {
    "4e": 3,
    "3e": 5,
    "2nde": 2,
    "1ere_spe": 3,
    "1re_nsi": 2,
}

STUDENT_NAMES = {
    "4e": ["Sinda Chikhaoui", "Fares Darghouth", "Ines KEFI"],
    "3e": ["Sarah Bargaoui", "Selim Mansouri", "Amine Mansouri", "Fares Laajili", "Elyes KEFI"],
    "2nde": ["Noa Maniaci", "Ahmed Bakir"],
    "1ere_spe": ["Donia Khadhrani", "Malek Khadhrani", "Ahmad Beldi"],
    "1re_nsi": ["Ahmad BELDI", "Ahmed BENHADJ SALEM"],
}

def get_pdf_page_count(path: pathlib.Path) -> int:
    try:
        reader = PdfReader(path)
        return len(reader.pages)
    except Exception:
        return 0

def create_delivery_structure():
    if DELIVERY_V2.exists():
        shutil.rmtree(DELIVERY_V2)
    DELIVERY_V2.mkdir(parents=True, exist_ok=True)

    pret_imprimer = DELIVERY_V2 / "PRET_A_IMPRIMER"
    maths_dir = pret_imprimer / "MATHS"
    nsi_dir = pret_imprimer / "NSI"
    packs_pdf_dir = DELIVERY_V2 / "PACKS_PDF"
    nominatifs_dir = DELIVERY_V2 / "DOSSIERS_NOMINATIFS_CONFIDENTIELS"
    nsi_code_dir = DELIVERY_V2 / "NSI_ZIP_CODE"

    pret_imprimer.mkdir()
    maths_dir.mkdir()
    nsi_dir.mkdir()
    packs_pdf_dir.mkdir()
    nominatifs_dir.mkdir()
    nsi_code_dir.mkdir()

    # Copie des packs Maths dans PRET_A_IMPRIMER
    for level in ("4e", "3e", "2nde", "1ere_spe"):
        level_target = maths_dir / level
        level_target.mkdir(parents=True, exist_ok=True)
        
        # S1..S5 packs
        for s in range(1, 6):
            eleve_pdf = DIST / "packs" / "eleves" / f"{level}_S{s}_PACK_ELEVE.pdf"
            prof_pdf = DIST / "packs" / "enseignants" / f"{level}_S{s}_PACK_ENSEIGNANT.pdf"
            if eleve_pdf.exists():
                shutil.copy2(eleve_pdf, level_target / eleve_pdf.name)
            if prof_pdf.exists():
                shutil.copy2(prof_pdf, level_target / prof_pdf.name)
        
        # Complet & Evaluations
        for name in (f"{level}_PACK_ELEVE_COMPLET.pdf", f"{level}_PACK_EVALUATIONS_ELEVE.pdf"):
            src = DIST / "packs" / "eleves" / name
            if src.exists():
                shutil.copy2(src, level_target / name)
        for name in (f"{level}_PACK_ENSEIGNANT_COMPLET.pdf", f"{level}_PACK_EVALUATIONS_CORRIGE.pdf"):
            src = DIST / "packs" / "enseignants" / name
            if src.exists():
                shutil.copy2(src, level_target / name)

    # Copie des packs NSI dans PRET_A_IMPRIMER/NSI
    nsi_src_packs = ROOT / "1re_nsi" / "08_PACKS_PDF"
    if nsi_src_packs.exists():
        for pdf in nsi_src_packs.glob("*.pdf"):
            shutil.copy2(pdf, nsi_dir / pdf.name)

    # Copie de l'intégralité des packs PDF dans PACKS_PDF
    for p in (DIST / "packs").rglob("*.pdf"):
        shutil.copy2(p, packs_pdf_dir / p.name)

    # Copie des dossiers nominatifs confidentiels
    for p in (DIST / "packs" / "nominatifs-prives").glob("*.pdf"):
        shutil.copy2(p, nominatifs_dir / p.name)
    nsi_nom = ROOT / "1re_nsi" / "08_PACKS_PDF"
    if nsi_nom.exists():
        for p in nsi_nom.glob("*PACK_TRAVAIL_*.pdf"):
            shutil.copy2(p, nominatifs_dir / p.name)

    # Copie des ZIP NSI
    nsi_zip_src = ROOT / "1re_nsi" / "09_PACKS_CODE"
    if nsi_zip_src.exists():
        for z in nsi_zip_src.glob("*.zip"):
            shutil.copy2(z, nsi_code_dir / z.name)

    print(f"Structure V2 créée dans {DELIVERY_V2}")

def generate_plan_impression():
    rows = []

    # Headings for table
    table_lines = [
        "# PLAN D’IMPRESSION — Nexus Réussite (Stages Pré-rentrée 2026-2027)",
        "",
        "> **Note d’information centre** : Ce plan est généré dynamiquement depuis le registre officiel des inscriptions.",
        "> **Total inscriptions** : 15 (13 en Mathématiques, 2 en NSI).",
        "> **Total élèves physiques uniques** : 14 (Ahmad BELDI est inscrit en 1re Spé Mathématiques ET en 1re NSI).",
        "",
        "## 1. Répartition des effectifs par groupe",
        "",
        "- **4e Mathématiques** : 3 élèves (Sinda Chikhaoui, Fares Darghouth, Ines KEFI) + 1 enseignant",
        "- **3e Mathématiques** : 5 élèves (Sarah Bargaoui, Selim Mansouri, Amine Mansouri, Fares Laajili, Elyes KEFI) + 1 enseignant",
        "- **2nde Mathématiques** : 2 élèves (Noa Maniaci, Ahmed Bakir) + 1 enseignant",
        "- **1re Spé Mathématiques** : 3 élèves (Donia Khadhrani, Malek Khadhrani, Ahmad Beldi) + 1 enseignant",
        "- **1re NSI** : 2 élèves (Ahmad BELDI, Ahmed BENHADJ SALEM) + 1 enseignant",
        "",
        "---",
        "",
        "## 2. Plan d’impression détaillé — Dossier PRET_A_IMPRIMER",
        "",
        "| Discipline / Niveau | Fichier PDF | Audience | Pages / ex | Ex. Élève | Ex. Prof | Feuillets Recto Simple | Statut / Confidentialité |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ]

    total_sheets = 0

    pret_imprimer = DELIVERY_V2 / "PRET_A_IMPRIMER"
    for pdf_path in sorted(pret_imprimer.rglob("*.pdf")):
        rel = pdf_path.relative_to(pret_imprimer).as_posix()
        name = pdf_path.name
        pages = get_pdf_page_count(pdf_path)

        level = "4e"
        if "3e" in rel: level = "3e"
        elif "2nde" in rel: level = "2nde"
        elif "1ere_spe" in rel: level = "1ere_spe"
        elif "NSI" in rel: level = "1re_nsi"

        n_students = ENROLLMENT_COUNTS.get(level, 1)

        is_teacher = "ENSEIGNANT" in name or "CORRIGE" in name or "PROF" in name
        is_eleve = "ELEVE" in name and not is_teacher

        if is_eleve:
            ex_eleve = n_students
            ex_prof = 0
            conf = "PUBLIC — À distribuer aux élèves"
        elif is_teacher:
            ex_eleve = 0
            ex_prof = 1
            conf = "CONFIDENTIEL — Enseignant uniquement"
        else:
            ex_eleve = n_students
            ex_prof = 1
            conf = "USAGE INTERNE"

        sheets = pages * (ex_eleve + ex_prof)
        total_sheets += sheets

        table_lines.append(
            f"| {level} | `{name}` | {'Enseignant' if is_teacher else 'Élève'} | {pages} | {ex_eleve} | {ex_prof} | **{sheets}** | {conf} |"
        )

    table_lines.extend([
        "",
        f"### **GRAND TOTAL FEUILLES RECTO SIMPLE POUR OUVERTURE : {total_sheets} pages**",
        "",
        "---",
        "",
        "## 3. Consignes strictes d’impression",
        "",
        "1. **Imprimer exclusivement en RECTO SIMPLE** pour permettre aux élèves de manipuler les fiches et d'écrire sans transparence.",
        "2. **Dossiers d’évaluation et de corrigés (CONFIDENTIEL)** : Ne JAMAIS remettre de document portant la mention `CORRIGE` ou `ENSEIGNANT` à un élève.",
        "3. **Dossiers nominatifs privés** : Stockés dans `DOSSIERS_NOMINATIFS_CONFIDENTIELS/`. Impression réservée à la remise individuelle sous pli confidentiel.",
        "4. **Archives de code NSI** : Les fichiers `.zip` dans `NSI_ZIP_CODE/` doivent être copiés sur les postes de travail Python des élèves concernés (ne pas copier `1re_nsi_CODE_ENSEIGNANT.zip` sur les postes élèves).",
    ])

    plan_path = DELIVERY_V2 / "PLAN_IMPRESSION.md"
    plan_path.write_text("\n".join(table_lines) + "\n", encoding="utf-8")
    print(f"PLAN_IMPRESSION.md généré avec succès dans {plan_path} (Total feuilles: {total_sheets})")

def main():
    create_delivery_structure()
    generate_plan_impression()

if __name__ == "__main__":
    main()
