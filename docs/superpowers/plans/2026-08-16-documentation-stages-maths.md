# Documentation Stages Maths Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produire localement un portail statique, des PDF A4, des packs séparés et des contrôles qualité pour les quatre stages de mathématiques.

**Architecture:** Un registre généré pilote la navigation, les HTML, les PDF et les manifests. Pandoc rend les Markdown en HTML/MathML local, WeasyPrint produit les PDF et pypdf assemble les packs.

**Tech Stack:** Python 3.12, Pandoc, WeasyPrint, pypdf, pytest, SymPy, Poppler, qpdf.

---

## Chunk 1: Baseline et registre

### Task 1: Tester le classement documentaire

**Files:**
- Create: `tests/test_build.py`
- Create: `tools/build.py`

- [ ] Écrire un test rouge de classification public/privé et de noms de packs.
- [ ] Lancer `pytest -q tests/test_build.py` et constater l'échec attendu.
- [ ] Implémenter les fonctions minimales de classification.
- [ ] Relancer le test et constater le succès.

### Task 2: Générer le catalogue

**Files:**
- Create: `content/catalog.json`
- Modify: `tools/build.py`

- [ ] Parcourir uniquement les quatre niveaux mathématiques et classifier audience, séance, type et confidentialité.
- [ ] Générer le catalogue et les manifests depuis ce registre.
- [ ] Tester l'exclusion des documents privés du catalogue public.

## Chunk 2: Portail et HTML

### Task 3: Rendre les sorties HTML

**Files:**
- Create: `assets/site.css`
- Create: `assets/site.js`
- Modify: `tools/build.py`

- [ ] Générer les pages documentaires avec `lang=fr`, landmarks, lien d'évitement, breadcrumbs et actions PDF.
- [ ] Générer accueil, pages de niveau, préparation de séance, packs et suivi privé depuis le registre.
- [ ] Tester les chemins générés et l'absence d'URL externe.

## Chunk 3: PDF et packs

### Task 4: Générer les PDF unitaires

**Files:**
- Modify: `tools/build.py`
- Create: `requirements.txt`

- [ ] Tester le nommage et les métadonnées d'un PDF élève.
- [ ] Produire les PDF via WeasyPrint et enrichir leurs métadonnées avec pypdf.
- [ ] Contrôler A4, ouverture et absence de chiffrement.

### Task 5: Assembler les packs

**Files:**
- Modify: `tools/build.py`

- [ ] Tester qu'un pack élève ne sélectionne ni corrigé ni dossier d'un autre élève.
- [ ] Assembler les packs par niveau, séance et élève.
- [ ] Générer les manifests public et privé avec SHA-256.

## Chunk 4: QA et livraison

### Task 6: Automatiser les contrôles

**Files:**
- Modify: `tools/build.py`
- Create: `Makefile`
- Create: `README.md`, `QUICK_START.md`, `PRINT_GUIDE.md`, `PRINT_CHECKLIST.csv`, `CHANGELOG.md`

- [ ] Vérifier les liens, l'accessibilité statique, les documents attendus, les calculs de durée et les fuites PII/corrigés.
- [ ] Rasteriser tous les PDF, créer les planches-contact et le rapport visuel.
- [ ] Exécuter deux builds propres et comparer les inventaires.
- [ ] Écrire les rapports et le statut final avec compteurs factuels.
