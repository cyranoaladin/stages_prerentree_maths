#!/usr/bin/env python3
"""Génération et assemblage déterministe de la livraison opérationnelle V3_FINAL pour les stages Nexus Réussite 2026."""

import os
import csv
import json
import shutil
import hashlib
import pathlib
import subprocess
from pypdf import PdfReader
from weasyprint import HTML

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DELIVERY_V3 = ROOT.parent / "LIVRAISON_STAGES_2026-08-17_V3_FINAL"

# Dynamic Loading of Student Enrollments
def get_group_counts(root: pathlib.Path) -> dict[str, int]:
    counts = {"4e": 0, "3e": 0, "2nde": 0, "1ere_spe": 0, "1re_nsi": 0}
    students_json = root / "content" / "students.json"
    if students_json.exists():
        data = json.loads(students_json.read_text(encoding="utf-8"))
        for s in data.get("students", []):
            if s.get("active", True):
                lvl = s.get("level")
                if lvl in counts:
                    counts[lvl] += 1

    # NSI counts from nominative directory
    nsi_nom = root / "1re_nsi" / "05_NOMINATIFS"
    if nsi_nom.exists():
        nsi_students = [p for p in nsi_nom.iterdir() if p.is_dir()]
        counts["1re_nsi"] = len(nsi_students)

    return counts

GROUP_COUNTS = get_group_counts(ROOT)

LEVEL_HUMAN_NAMES = {
    "4e": "4e",
    "3e": "3e",
    "2nde": "2nde",
    "1ere_spe": "1re Spécialité Mathématiques",
    "1re_nsi": "1re NSI",
}

def get_pdf_page_count(path: pathlib.Path) -> int:
    try:
        reader = PdfReader(path)
        return len(reader.pages)
    except Exception:
        return 0

def create_v3_structure():
    if DELIVERY_V3.exists():
        shutil.rmtree(DELIVERY_V3)
    DELIVERY_V3.mkdir(parents=True, exist_ok=True)

    c_ici = DELIVERY_V3 / "00_COMMENCER_ICI"
    imp_urg = DELIVERY_V3 / "01_IMPRESSION_URGENTE"
    maths_dir = DELIVERY_V3 / "02_MATHEMATIQUES_PAR_NIVEAU"
    nsi_dir = DELIVERY_V3 / "03_NSI_PREMIERE"
    tab_dir = DELIVERY_V3 / "04_TABLETTE_ENSEIGNANT"
    eval_dir = DELIVERY_V3 / "05_EVALUATIONS"
    nom_dir = DELIVERY_V3 / "06_DOSSIERS_NOMINATIFS_CONFIDENTIELS"
    qa_dir = DELIVERY_V3 / "90_RAPPORTS_QA"

    for d in (c_ici, imp_urg, maths_dir, nsi_dir, tab_dir, eval_dir, nom_dir, qa_dir):
        d.mkdir(parents=True, exist_ok=True)

    # 1. Copie du site pour Tablette Enseignant
    if (DIST / "site-private").exists():
        shutil.copytree(DIST / "site-private", tab_dir / "site-private", dirs_exist_ok=True)
    if (DIST / "site-public").exists():
        shutil.copytree(DIST / "site-public", tab_dir / "site-public", dirs_exist_ok=True)

    # 2. Copie des maths par niveau
    for lvl in ("4e", "3e", "2nde", "1ere_spe"):
        tgt = maths_dir / lvl
        tgt.mkdir(parents=True, exist_ok=True)
        src_pdf = DIST / "pdf" / lvl
        if src_pdf.exists():
            shutil.copytree(src_pdf, tgt / "PDF", dirs_exist_ok=True)
        # Packs
        for p in (DIST / "packs").rglob(f"{lvl}_*.pdf"):
            shutil.copy2(p, tgt / p.name)

    # 3. NSI
    nsi_docs = nsi_dir / "DOCS"
    nsi_packs = nsi_dir / "PACKS"
    nsi_code = nsi_dir / "CODE_ZIP"
    for d in (nsi_docs, nsi_packs, nsi_code): d.mkdir(parents=True, exist_ok=True)
    if (ROOT / "1re_nsi" / "08_PACKS_PDF").exists():
        for p in (ROOT / "1re_nsi" / "08_PACKS_PDF").glob("*.pdf"):
            shutil.copy2(p, nsi_packs / p.name)
    if (ROOT / "1re_nsi" / "09_PACKS_CODE").exists():
        for z in (ROOT / "1re_nsi" / "09_PACKS_CODE").glob("*.zip"):
            shutil.copy2(z, nsi_code / z.name)

    # 4. Dossiers Nominatifs Confidentiels
    for p in (DIST / "packs" / "nominatifs-prives").glob("*.pdf"):
        shutil.copy2(p, nom_dir / p.name)
    if (ROOT / "1re_nsi" / "08_PACKS_PDF").exists():
        for p in (ROOT / "1re_nsi" / "08_PACKS_PDF").glob("*PACK_TRAVAIL_*.pdf"):
            shutil.copy2(p, nom_dir / p.name)

    # 5. Rapports QA
    for r in (ROOT / "reports").glob("*"):
        if r.is_file():
            shutil.copy2(r, qa_dir / r.name)

def generate_commencer_ici():
    c_ici = DELIVERY_V3 / "00_COMMENCER_ICI"

    html_content = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Stages Nexus Réussite 2026 — Démarrage Urgent</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; margin: 0; padding: 2rem; background: #f8fafc; color: #0f172a; line-height: 1.6; }}
  .container {{ max-width: 900px; margin: 0 auto; background: #ffffff; padding: 2.5rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
  h1 {{ color: #1e3a8a; font-size: 2rem; border-bottom: 3px solid #3b82f6; padding-bottom: 0.5rem; margin-top: 0; }}
  h2 {{ color: #1e40af; font-size: 1.3rem; margin-top: 1.8rem; }}
  .alert {{ background: #eff6ff; border-left: 4px solid #3b82f6; padding: 1rem 1.2rem; border-radius: 4px; margin: 1rem 0; }}
  .badge-p0 {{ background: #dc2626; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: bold; font-size: 0.85rem; }}
  ul {{ padding-left: 1.2rem; }}
  li {{ margin-bottom: 0.5rem; }}
  .button-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-top: 1.5rem; }}
  .btn {{ display: block; text-align: center; background: #2563eb; color: white; text-decoration: none; padding: 1rem; border-radius: 8px; font-weight: 600; transition: background 0.2s; }}
  .btn:hover {{ background: #1d4ed8; }}
  .btn-sec {{ background: #475569; }}
  .btn-sec:hover {{ background: #334155; }}
</style>
</head>
<body>
<div class="container">
  <h1>🚀 Stages Nexus Réussite 2026 — Guide de Démarrage Urgent</h1>
  <div class="alert">
    <strong><span class="badge-p0">ACTION IMMÉDIATE</span> Le stage commence maintenant !</strong><br>
    Suivez ce guide rapide de 2 minutes pour imprimer les documents de la Séance 1 et lancer votre tablette.
  </div>

  <h2>1. Imprimer immédiatement la Séance 1</h2>
  <p>Rendez-vous dans le dossier <code>01_IMPRESSION_URGENTE/SEANCE_1/</code> pour récupérer les fiches de vos élèves et enseignants.</p>
  <ul>
    <li><strong>4e Maths :</strong> {GROUP_COUNTS['4e']} élèves inscrits (+ 1 prof)</li>
    <li><strong>3e Maths :</strong> {GROUP_COUNTS['3e']} élèves inscrits (+ 1 prof)</li>
    <li><strong>2nde Maths :</strong> {GROUP_COUNTS['2nde']} élèves inscrits (+ 1 prof)</li>
    <li><strong>1re Spé Maths :</strong> {GROUP_COUNTS['1ere_spe']} élèves inscrits (+ 1 prof)</li>
    <li><strong>1re NSI :</strong> {GROUP_COUNTS['1re_nsi']} élèves inscrits (+ 1 prof)</li>
  </ul>

  <h2>2. Utiliser la Tablette en cours</h2>
  <p>Ouvrez le portail tablette enseignant interactif sans aucune connexion Internet :</p>
  <div class="button-grid">
    <a class="btn" href="../04_TABLETTE_ENSEIGNANT/SEANCE_DU_JOUR.html">📱 Mode Séance du Jour</a>
    <a class="btn btn-sec" href="../04_TABLETTE_ENSEIGNANT/index.html">🏠 Accueil Portail Tablette</a>
  </div>

  <h2>3. Confidentialité & Dossiers Nominatifs</h2>
  <p>Les bilans individuels et remédiations nominatives sont stockés dans <code>06_DOSSIERS_NOMINATIFS_CONFIDENTIELS/</code>. Ils sont strictly réservés à l'enseignant et à la remise sous pli confidentiel.</p>
</div>
</body>
</html>'''

    (c_ici / "COMMENCER_ICI.html").write_text(html_content, encoding="utf-8")
    HTML(string=html_content).write_pdf(str(c_ici / "COMMENCER_ICI.pdf"))

    readme_content = f'''# Guide de Démarrage Urgent — Nexus Réussite 2026

## Démarrage rapide (< 2 minutes)

1. **Impression Séance 1** :
   - Dossier : `01_IMPRESSION_URGENTE/SEANCE_1/`
   - Envoyez directement les sous-dossiers élèves et prof à l'imprimante (Recto Simple).

2. **Tablette Enseignant** :
   - Fichier : `04_TABLETTE_ENSEIGNANT/SEANCE_DU_JOUR.html`
   - Accessible hors-ligne ou via serveur local (`make tablet-serve-public`).

3. **Effectifs par groupe (Août 2026)** :
   - 4e Maths : {GROUP_COUNTS['4e']} élèves
   - 3e Maths : {GROUP_COUNTS['3e']} élèves
   - 2nde Maths : {GROUP_COUNTS['2nde']} élèves
   - 1re Spé Maths : {GROUP_COUNTS['1ere_spe']} élèves
   - 1re NSI : {GROUP_COUNTS['1re_nsi']} élèves
'''
    (c_ici / "README_URGENCE.md").write_text(readme_content, encoding="utf-8")

def generate_impression_urgente():
    imp_dir = DELIVERY_V3 / "01_IMPRESSION_URGENTE"
    s1_dir = imp_dir / "SEANCE_1"
    tout_s1 = imp_dir / "TOUT_SEANCE_1"
    s1_dir.mkdir(parents=True, exist_ok=True)
    tout_s1.mkdir(parents=True, exist_ok=True)

    rows = []
    total_sheets_s1 = 0
    total_sheets_global = 0

    # Human-readable mapping for S1 copy
    mapping = {
        "4e": [
            ("01_ELEVES", "4e_S1_ELEVE_Activite.pdf", f"4e - Séance 1 - Activité élèves ({GROUP_COUNTS['4e']} ex).pdf", GROUP_COUNTS['4e'], "élève"),
            ("02_PROFESSEUR", "4e_S1_PROF_Fiche.pdf", "4e - Séance 1 - Fiche professeur (1 ex).pdf", 1, "professeur"),
            ("03_SUPPORTS", "4e_S1_SUPPORTS_Manipulation.pdf", f"4e - Séance 1 - Supports de manipulation ({GROUP_COUNTS['4e']} ex).pdf", GROUP_COUNTS['4e'], "support"),
            ("04_OPTIONNEL", "4e_S1_AIDES_Cartes.pdf", "4e - Séance 1 - Cartes d’aide.pdf", 1, "optionnel"),
        ],
        "3e": [
            ("01_ELEVES", "3e_S1_ELEVE_Activite.pdf", f"3e - Séance 1 - Activité élèves ({GROUP_COUNTS['3e']} ex).pdf", GROUP_COUNTS['3e'], "élève"),
            ("02_PROFESSEUR", "3e_S1_PROF_Fiche.pdf", "3e - Séance 1 - Fiche professeur (1 ex).pdf", 1, "professeur"),
            ("03_SUPPORTS", "3e_S1_SUPPORTS_Manipulation.pdf", f"3e - Séance 1 - Supports de manipulation ({GROUP_COUNTS['3e']} ex).pdf", GROUP_COUNTS['3e'], "support"),
            ("04_OPTIONNEL", "3e_S1_AIDES_Cartes.pdf", "3e - Séance 1 - Cartes d’aide.pdf", 1, "optionnel"),
        ],
        "2nde": [
            ("01_ELEVES", "2nde_S1_ELEVE_Activite.pdf", f"2nde - Séance 1 - Activité élèves ({GROUP_COUNTS['2nde']} ex).pdf", GROUP_COUNTS['2nde'], "élève"),
            ("02_PROFESSEUR", "2nde_S1_PROF_Fiche.pdf", "2nde - Séance 1 - Fiche professeur (1 ex).pdf", 1, "professeur"),
            ("03_SUPPORTS", "2nde_S1_SUPPORTS_Manipulation.pdf", f"2nde - Séance 1 - Supports de manipulation ({GROUP_COUNTS['2nde']} ex).pdf", GROUP_COUNTS['2nde'], "support"),
            ("04_OPTIONNEL", "2nde_S1_AIDES_Cartes.pdf", "2nde - Séance 1 - Cartes d’aide.pdf", 1, "optionnel"),
        ],
        "1ere_spe": [
            ("01_ELEVES", "1ere_spe_S1_ELEVE_Activite.pdf", f"1re Spé - Séance 1 - Activité élèves ({GROUP_COUNTS['1ere_spe']} ex).pdf", GROUP_COUNTS['1ere_spe'], "élève"),
            ("02_PROFESSEUR", "1ere_spe_S1_PROF_Fiche.pdf", "1re Spé - Séance 1 - Fiche professeur (1 ex).pdf", 1, "professeur"),
            ("03_SUPPORTS", "1ere_spe_S1_SUPPORTS_Manipulation.pdf", f"1re Spé - Séance 1 - Supports de manipulation ({GROUP_COUNTS['1ere_spe']} ex).pdf", GROUP_COUNTS['1ere_spe'], "support"),
            ("04_OPTIONNEL", "1ere_spe_S1_AIDES_Cartes.pdf", "1re Spé - Séance 1 - Cartes d’aide.pdf", 1, "optionnel"),
        ],
        "1re_nsi": [
            ("01_ELEVES", "1re_nsi_S1_ELEVE_Activite.pdf", f"1re NSI - Séance 1 - Activité élèves ({GROUP_COUNTS['1re_nsi']} ex).pdf", GROUP_COUNTS['1re_nsi'], "élève"),
            ("02_PROFESSEUR", "1re_nsi_S1_PROF_Fiche.pdf", "1re NSI - Séance 1 - Fiche professeur (1 ex).pdf", 1, "professeur"),
            ("03_SUPPORTS", "1re_nsi_S1_SUPPORTS_Pratiques.pdf", f"1re NSI - Séance 1 - Supports pratiques ({GROUP_COUNTS['1re_nsi']} ex).pdf", GROUP_COUNTS['1re_nsi'], "support"),
            ("04_OPTIONNEL", "1re_nsi_S1_AIDES_Cartes.pdf", "1re NSI - Séance 1 - Cartes d’aide.pdf", 1, "optionnel"),
        ],
    }

    # Process S1 files
    for lvl, items in mapping.items():
        lvl_s1_dir = s1_dir / lvl
        for sub, src_name, human_name, copies, aud in items:
            sub_dir = lvl_s1_dir / sub
            sub_dir.mkdir(parents=True, exist_ok=True)

            # Find source PDF
            src_pdf = None
            for p in (DIST / "pdf").rglob(src_name):
                src_pdf = p
                break
            if not src_pdf:
                for p in (ROOT / "1re_nsi").rglob(src_name):
                    src_pdf = p
                    break

            if src_pdf and src_pdf.exists():
                shutil.copy2(src_pdf, sub_dir / human_name)
                shutil.copy2(src_pdf, tout_s1 / f"[{lvl}] {human_name}")
                pages = get_pdf_page_count(src_pdf)
                sheets = pages * copies
                total_sheets_s1 += sheets
                rows.append({
                    "priorite": "URGENT S1",
                    "level": lvl,
                    "seance": "S1",
                    "type": sub,
                    "fichier": human_name,
                    "pages_ex": pages,
                    "exemplaires": copies,
                    "exemplaires_secours": copies + 1 if copies > 1 else 1,
                    "feuillets": sheets,
                    "remarque": "À imprimer immédiatement pour le début du cours",
                })

    # Plan HTML & CSV
    plan_html_content = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Plan d'Impression Urgent — Nexus Réussite</title>
<style>
  body {{ font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 2rem; background: #f8fafc; color: #1e293b; }}
  .card {{ background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  h1 {{ color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
  th, td {{ border: 1px solid #cbd5e1; padding: 0.75rem; text-align: left; }}
  th {{ background: #f1f5f9; }}
  .badge-urgent {{ background: #ef4444; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: bold; }}
  .total-box {{ background: #dbeafe; border-left: 4px solid #2563eb; padding: 1rem; margin-top: 1.5rem; font-size: 1.2rem; font-weight: bold; }}
</style>
</head>
<body>
<div class="card">
  <h1>🖨️ Plan d'Impression Urgent — Séance 1</h1>
  <p>Calculé dynamiquement depuis le registre des inscriptions de pré-rentrée 2026.</p>

  <div class="total-box">
    TOTAL SÉANCE 1 À IMPRIMER MAINTENANT : {total_sheets_s1} feuillets Recto Simple
  </div>

  <table>
    <thead>
      <tr>
        <th>Priorité</th>
        <th>Niveau</th>
        <th>Séance</th>
        <th>Fichier PDF (Nom Humain)</th>
        <th>Pages / ex</th>
        <th>Ex. Strict</th>
        <th>Ex. Conseillé (+1)</th>
        <th>Feuillets Totaux</th>
      </tr>
    </thead>
    <tbody>
'''
    for r in rows:
        plan_html_content += f'''      <tr>
        <td><span class="badge-urgent">{r['priorite']}</span></td>
        <td>{r['level']}</td>
        <td>{r['seance']}</td>
        <td><code>{r['fichier']}</code></td>
        <td>{r['pages_ex']}</td>
        <td>{r['exemplaires']}</td>
        <td>{r['exemplaires_secours']}</td>
        <td><strong>{r['feuillets']}</strong></td>
      </tr>
'''
    plan_html_content += '''    </tbody>
  </table>
</div>
</body>
</html>'''

    (imp_dir / "PLAN_IMPRESSION_URGENT.html").write_text(plan_html_content, encoding="utf-8")
    HTML(string=plan_html_content).write_pdf(str(imp_dir / "PLAN_IMPRESSION_URGENT.pdf"))

    # CSV
    with (imp_dir / "PLAN_IMPRESSION_URGENT.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["priorite", "level", "seance", "type", "fichier", "pages_ex", "exemplaires_stricts", "exemplaires_conseilles", "feuillets", "remarque"])
        for r in rows:
            w.writerow([r['priorite'], r['level'], r['seance'], r['type'], r['fichier'], r['pages_ex'], r['exemplaires'], r['exemplaires_secours'], r['feuillets'], r['remarque']])

    # Checklist HTML
    chk_html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Checklist Impression Séance 1</title>
<style>
  body {{ font-family: system-ui; padding: 2rem; background: #f8fafc; }}
  .item {{ background: white; padding: 1rem; margin-bottom: 0.5rem; border-radius: 6px; display: flex; align-items: center; gap: 1rem; }}
  input[type=checkbox] {{ width: 1.5rem; height: 1.5rem; }}
</style>
</head>
<body>
  <h1>✅ Checklist Impression — Séance 1</h1>
'''
    for r in rows:
        chk_html += f'''  <div class="item">
    <input type="checkbox" id="{r['level']}_{r['type']}">
    <label for="{r['level']}_{r['type']}"><strong>[{r['level']}]</strong> {r['fichier']} ({r['exemplaires']} ex. = {r['feuillets']} pages)</label>
  </div>
'''
    chk_html += "</body></html>"
    (imp_dir / "CHECKLIST_IMPRESSION.html").write_text(chk_html, encoding="utf-8")

def generate_tablette_interface():
    tab_dir = DELIVERY_V3 / "04_TABLETTE_ENSEIGNANT"
    tab_dir.mkdir(parents=True, exist_ok=True)

    # 1. Page Séance du jour
    seance_du_jour_html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Séance du Jour — Nexus Réussite</title>
<style>
  :root {{ --primary: #1e3a8a; --accent: #2563eb; --bg: #f1f5f9; }}
  body {{ font-family: system-ui, -apple-system, sans-serif; margin: 0; background: var(--bg); color: #0f172a; touch-action: manipulation; }}
  header {{ background: var(--primary); color: white; padding: 1rem 1.5rem; display: flex; justify-content: space-between; align-items: center; }}
  header h1 {{ margin: 0; font-size: 1.4rem; }}
  .nav-btn {{ background: rgba(255,255,255,0.2); color: white; border: none; padding: 0.6rem 1rem; border-radius: 6px; font-weight: bold; text-decoration: none; }}
  .main-container {{ padding: 1.5rem; max-width: 1000px; margin: 0 auto; }}
  .section-title {{ font-size: 1.1rem; text-transform: uppercase; color: #475569; letter-spacing: 0.05em; margin-bottom: 0.5rem; }}
  .level-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
  .level-btn {{ background: white; border: 2px solid #cbd5e1; border-radius: 12px; padding: 1.2rem; text-align: center; font-size: 1.2rem; font-weight: bold; color: var(--primary); cursor: pointer; transition: all 0.15s; }}
  .level-btn.active {{ border-color: var(--accent); background: #eff6ff; color: var(--accent); box-shadow: 0 4px 12px rgba(37,99,235,0.15); }}
  .doc-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }}
  .doc-card {{ background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between; }}
  .doc-card h3 {{ margin: 0 0 0.5rem 0; color: #1e293b; font-size: 1.2rem; }}
  .doc-card p {{ margin: 0 0 1rem 0; color: #64748b; font-size: 0.95rem; }}
  .action-btn {{ display: block; width: 100%; text-align: center; background: var(--accent); color: white; text-decoration: none; padding: 0.9rem; border-radius: 8px; font-weight: bold; font-size: 1.1rem; box-sizing: border-box; }}
</style>
</head>
<body>
<header>
  <h1>📱 Mode Séance du Jour</h1>
  <a class="nav-btn" href="index.html">🏠 Portail Général</a>
</header>
<div class="main-container">
  <div class="section-title">Sélectionner le Niveau</div>
  <div class="level-grid">
    <div class="level-btn active" onclick="selectLevel('4e')">4e</div>
    <div class="level-btn" onclick="selectLevel('3e')">3e</div>
    <div class="level-btn" onclick="selectLevel('2nde')">2nde</div>
    <div class="level-btn" onclick="selectLevel('1ere_spe')">1re Spé</div>
    <div class="level-btn" onclick="selectLevel('1re_nsi')">1re NSI</div>
  </div>

  <div class="section-title" id="doc-section-title">Documents Séance 1 — 4e</div>
  <div class="doc-grid" id="doc-grid">
    <!-- Injected dynamically -->
  </div>
</div>

<script>
const docs = {{
  '4e': [
    {{ title: "Activité Élève", type: "Élève", link: "site-private/4e/02_SEANCES/S1/4e_S1_ELEVE_Activite.html" }},
    {{ title: "Fiche Professeur", type: "Enseignant", link: "site-private/4e/02_SEANCES/S1/4e_S1_PROF_Fiche.html" }},
    {{ title: "Supports de Manipulation", type: "Supports", link: "site-private/4e/02_SEANCES/S1/4e_S1_SUPPORTS_Manipulation.html" }},
    {{ title: "Cartes d'Aide", type: "Aides", link: "site-private/4e/02_SEANCES/S1/4e_S1_AIDES_Cartes.html" }}
  ],
  '3e': [
    {{ title: "Activité Élève", type: "Élève", link: "site-private/3e/02_SEANCES/S1/3e_S1_ELEVE_Activite.html" }},
    {{ title: "Fiche Professeur", type: "Enseignant", link: "site-private/3e/02_SEANCES/S1/3e_S1_PROF_Fiche.html" }},
    {{ title: "Supports de Manipulation", type: "Supports", link: "site-private/3e/02_SEANCES/S1/3e_S1_SUPPORTS_Manipulation.html" }},
    {{ title: "Cartes d'Aide", type: "Aides", link: "site-private/3e/02_SEANCES/S1/3e_S1_AIDES_Cartes.html" }}
  ],
  '2nde': [
    {{ title: "Activité Élève", type: "Élève", link: "site-private/2nde/02_SEANCES/S1/2nde_S1_ELEVE_Activite.html" }},
    {{ title: "Fiche Professeur", type: "Enseignant", link: "site-private/2nde/02_SEANCES/S1/2nde_S1_PROF_Fiche.html" }},
    {{ title: "Supports de Manipulation", type: "Supports", link: "site-private/2nde/02_SEANCES/S1/2nde_S1_SUPPORTS_Manipulation.html" }},
    {{ title: "Cartes d'Aide", type: "Aides", link: "site-private/2nde/02_SEANCES/S1/2nde_S1_AIDES_Cartes.html" }}
  ],
  '1ere_spe': [
    {{ title: "Activité Élève", type: "Élève", link: "site-private/1ere_spe/02_SEANCES/S1/1ere_spe_S1_ELEVE_Activite.html" }},
    {{ title: "Fiche Professeur", type: "Enseignant", link: "site-private/1ere_spe/02_SEANCES/S1/1ere_spe_S1_PROF_Fiche.html" }},
    {{ title: "Supports de Manipulation", type: "Supports", link: "site-private/1ere_spe/02_SEANCES/S1/1ere_spe_S1_SUPPORTS_Manipulation.html" }},
    {{ title: "Cartes d'Aide", type: "Aides", link: "site-private/1ere_spe/02_SEANCES/S1/1ere_spe_S1_AIDES_Cartes.html" }}
  ],
  '1re_nsi': [
    {{ title: "Activité Élève", type: "Élève", link: "site-private/1re_nsi/02_SEANCES/S1/1re_nsi_S1_ELEVE_Activite.html" }},
    {{ title: "Fiche Professeur", type: "Enseignant", link: "site-private/1re_nsi/02_SEANCES/S1/1re_nsi_S1_PROF_Fiche.html" }},
    {{ title: "Supports Pratiques", type: "Supports", link: "site-private/1re_nsi/02_SEANCES/S1/1re_nsi_S1_SUPPORTS_Pratiques.html" }},
    {{ title: "Cartes d'Aide", type: "Aides", link: "site-private/1re_nsi/02_SEANCES/S1/1re_nsi_S1_AIDES_Cartes.html" }}
  ]
}};

function selectLevel(lvl) {{
  document.querySelectorAll('.level-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
  document.getElementById('doc-section-title').innerText = 'Documents Séance 1 — ' + lvl;
  const grid = document.getElementById('doc-grid');
  grid.innerHTML = docs[lvl].map(d => `
    <div class="doc-card">
      <div>
        <h3>${{d.title}}</h3>
        <p>Public: ${{d.type}}</p>
      </div>
      <a class="action-btn" href="${{d.link}}">Ouvrir le document</a>
    </div>
  `).join('');
}}

selectLevel('4e');
</script>
</body>
</html>'''

    (tab_dir / "SEANCE_DU_JOUR.html").write_text(seance_du_jour_html, encoding="utf-8")

    # 2. Main Tablet Index
    tab_index_html = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portail Tablette Enseignant — Nexus Réussite</title>
<style>
  body {{ font-family: system-ui, -apple-system, sans-serif; margin: 0; background: #f8fafc; color: #0f172a; }}
  header {{ background: #1e3a8a; color: white; padding: 1.5rem; text-align: center; }}
  .banner-confidential {{ background: #dc2626; color: white; text-align: center; padding: 0.5rem; font-weight: bold; letter-spacing: 0.05em; }}
  .container {{ max-width: 1000px; margin: 2rem auto; padding: 0 1rem; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }}
  .card {{ background: white; border-radius: 12px; padding: 1.8rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border-top: 5px solid #2563eb; }}
  .card h2 {{ margin-top: 0; color: #1e3a8a; }}
  .btn {{ display: inline-block; background: #2563eb; color: white; text-decoration: none; padding: 0.8rem 1.2rem; border-radius: 6px; font-weight: bold; margin-top: 1rem; }}
</style>
</head>
<body>
<div class="banner-confidential">🔒 CONFIDENTIEL — ENSEIGNANT NEXUS RÉUSSITE</div>
<header>
  <h1>📱 Portail Tablette Enseignant</h1>
  <p>Stages Intensifs de Pré-rentrée 2026-2027</p>
</header>
<div class="container">
  <div class="grid">
    <div class="card" style="border-color: #ef4444;">
      <h2>⚡ Mode Urgence Séance 1</h2>
      <p>Accès direct et simplifié aux fiches de la première séance.</p>
      <a class="btn" style="background: #ef4444;" href="SEANCE_DU_JOUR.html">Ouvrir la Séance du Jour</a>
    </div>
    <div class="card">
      <h2>📚 Espace Enseignant Privé</h2>
      <p>Portail complet avec fiches prof, corrigés et dossiers nominatifs.</p>
      <a class="btn" href="site-private/index.html">Accéder à l'Espace Privé</a>
    </div>
    <div class="card">
      <h2>🌐 Portail Public Élèves</h2>
      <p>Version nettoyée de toute information confidentielle ou corrigé.</p>
      <a class="btn" style="background: #475569;" href="site-public/index.html">Ouvrir l'Espace Public</a>
    </div>
  </div>
</div>
</body>
</html>'''

    (tab_dir / "index.html").write_text(tab_index_html, encoding="utf-8")

def generate_checksums():
    checksum_file = DELIVERY_V3 / "CHECKSUMS_SHA256.txt"
    lines = []
    for p in sorted(DELIVERY_V3.rglob("*")):
        if p.is_file() and p.name != "CHECKSUMS_SHA256.txt":
            rel = p.relative_to(DELIVERY_V3).as_posix()
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            lines.append(f"{h}  {rel}")
    checksum_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

def main():
    print("Assemblage de LIVRAISON_STAGES_2026-08-17_V3_FINAL...")
    create_v3_structure()
    generate_commencer_ici()
    generate_impression_urgente()
    generate_tablette_interface()
    generate_checksums()
    print(f"Livraison V3_FINAL générée avec succès dans {DELIVERY_V3}")

if __name__ == "__main__":
    main()
