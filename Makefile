.PHONY: audit build pdf packs qa all serve tablet-serve-public tablet-serve-private clean-generated test

audit:
	python3 tools/build.py audit

build:
	python3 tools/build.py html

pdf:
	python3 tools/build.py pdf

packs:
	python3 tools/build.py packs

qa:
	python3 tools/build.py qa

all:
	python3 tools/build.py all

serve:
	python3 -m http.server 8000 --bind 127.0.0.1 --directory dist/site-public

tablet-serve-public:
	@python3 tools/tablet_server.py public

tablet-serve-private:
	@python3 tools/tablet_server.py private

clean-generated:
	rm -rf dist content/catalog.json MANIFEST_PUBLIC.csv MANIFEST_PRIVATE.csv

# La suite S5_cloture/tools/tests/test_analyze_s5.py emploie son propre harnais et ne
# définit aucune fonction test_* : pytest l'importe sans en collecter le moindre cas.
# Elle est donc lancée explicitement, sans quoi ses 48 vérifications ne s'exécuteraient
# jamais — ce qui était le cas jusqu'ici.
test:
	pytest -q
	python3 S5_cloture/tools/tests/test_analyze_s5.py

# --- Stages de pré-rentrée Terminale (tle_spe, tle_nsi) ----------------------
# Pipeline de documentation indépendant de tools/build.py, comme l'est déjà 1re_nsi.
# Aucune cible existante n'est modifiée.
#
# terminale-extract n'est pas exécutée en intégration continue : le rendu du texte d'un PDF
# dépend de la version de pypdf, et content/diagnostics_terminale.json est un artefact
# committé et relu. La CI vérifie en revanche que les documents nominatifs dérivent bien de
# cet artefact (terminale-check).

.PHONY: terminale terminale-extract terminale-check terminale-test \
        terminale-pdf terminale-pdf-list terminale-latex terminale-latex-check \
        terminale-livraison terminale-livraison-check

terminale:
	python3 tools/build_terminale.py

terminale-extract:
	python3 tools/extract_bilans_terminale.py

terminale-check:
	python3 tools/build_terminale.py --check

# Notation mathématique. terminale-latex réécrit les documents rédigés à la main en
# LaTeX ; terminale-latex-check se contente de signaler ce qui resterait à convertir et
# c'est cette forme-là qui tourne en intégration continue.
terminale-latex:
	python3 tools/mathify_terminale.py

terminale-latex-check:
	python3 tools/mathify_terminale.py --check

terminale-test:
	pytest -q tests/test_terminale.py tests/test_cahiers_seances.py

# Contrôles qualité du corpus. Ils ne remplacent pas les tests : ils vérifient ce qu'un test
# ne voit pas — l'exactitude des corrigés, la validité du code donné aux élèves, l'écart réel
# entre deux cahiers, et la mise en page des PDF produits.
terminale-qa:
	python3 tools/qa_science.py
	python3 tools/qa_code.py
	python3 tools/qa_curriculum.py
	python3 tools/qa_personnalisation.py

# Exige que les PDF aient été produits (make terminale-pdf).
terminale-qa-pdf:
	python3 tools/qa_pdf.py

# Planches contact pour l'inspection visuelle. Le motif est facultatif :
#   make terminale-planches MOTIF='*CAHIER_SEANCES_ELEVE.pdf'
MOTIF ?= *.pdf
terminale-planches:
	python3 tools/qa_planches.py '$(MOTIF)'

# Note de remise : qui reçoit quoi, quand, en combien d'exemplaires. Produite à partir du
# registre de la cohorte, donc incapable de décrire une remise différente de ce qui a été
# fabriqué. --check ne l'écrit pas mais vérifie la conformité, et c'est cette forme-là qui
# tourne en intégration continue — où les PDF n'existent pas.
terminale-livraison:
	python3 tools/build_dossier_livraison.py

terminale-livraison-check:
	python3 tools/build_dossier_livraison.py --check

# Rendu imprimable. Exige pandoc, LuaLaTeX et latexmk ; les PDF vont dans dist/terminale/, qui
# est ignoré par git : un PDF n'est pas reproductible d'une machine à l'autre.
terminale-pdf:
	python3 tools/build_terminale_pdf.py

terminale-pdf-list:
	python3 tools/build_terminale_pdf.py --list

# --- Nexus S5 — Correction & Bilans -----------------------------------------
# Cibles ajoutées pour l'application de correction. Aucune cible existante n'est touchée.
S5_APP := S5_correction_app

.PHONY: s5-correction-install s5-correction-init s5-correction-run s5-correction-test \
        s5-correction-qa s5-correction-backup s5-correction-backup-verify \
        s5-correction-longitudinal s5-correction-copie s5-correction-copie-etat \
        s5-correction-readiness s5-correction-today s5-correction-today-rapide \
        s5-correction-pdf-qa s5-correction-pdf-gate \
        s5-ocr-modeles s5-ocr-smoke s5-ocr-bench s5-ocr-rendre s5-ocr-mesure-dpi \
        s5-correction-fsck s5-correction-fsck-json s5-full-gate s5-ocr-live-gate \
        s5-browser-gate s5-debt-gate

s5-correction-install:
	python3 -m pip install --user -r $(S5_APP)/requirements-correction.lock

s5-correction-init:
	cd $(S5_APP) && python3 tools/init_database.py

s5-correction-run:
	cd $(S5_APP) && python3 -m app.cli serve

s5-correction-test:
	cd $(S5_APP) && python3 -m pytest -q

s5-correction-longitudinal:
	cd $(S5_APP) && python3 -m pytest -q tests/test_longitudinal.py

s5-correction-readiness:
	cd $(S5_APP) && python3 tools/build_readiness.py

s5-correction-today:
	cd $(S5_APP) && python3 tools/check_today_readiness.py

s5-correction-today-rapide:
	cd $(S5_APP) && python3 tools/check_today_readiness.py --no-compile

s5-correction-pdf-qa:
	cd $(S5_APP) && python3 tools/synthetic_pipeline_check.py --keep
	cd $(S5_APP) && python3 tools/pdf_visual_qa.py ../tmp/tests/synthetic_reports --dpi 150

s5-correction-pdf-gate:
	cd $(S5_APP) && python3 tools/check_report_pdf_quality.py ../tmp/tests/synthetic_reports --allow-test-markers

s5-correction-qa:
	cd $(S5_APP) && python3 tools/verify_integrity.py && python3 -m pytest -q

s5-correction-backup:
	cd $(S5_APP) && python3 tools/backup.py

# Restaure la dernière archive dans un temporaire et recontrôle chaque empreinte.
# Ne touche pas à runtime/ : c'est un contrôle, pas une restauration.
s5-correction-backup-verify:
	cd $(S5_APP) && python3 tools/backup.py --verifier "$$(ls -1t runtime/backups/backup_*.zip | head -1)"

# Rattache la copie réelle d'un élève. ELEVE=<student_id> COPIE="a.pdf" ou "p1.jpg p2.jpg"
s5-correction-copie:
	cd $(S5_APP) && python3 tools/attach_source_copy.py $(ELEVE) $(COPIE)

# État de la copie rattachée à un élève, empreintes recontrôlées. ELEVE=<student_id>
s5-correction-copie-etat:
	cd $(S5_APP) && python3 tools/attach_source_copy.py $(ELEVE) --lister

# Réconciliation base <-> fichiers. Lecture seule : aucune réparation automatique.
s5-correction-fsck:
	cd $(S5_APP) && python3 tools/fsck.py

s5-correction-fsck-json:
	cd $(S5_APP) && python3 tools/fsck.py --json

# Porte de fermeture : tout ce qui ne coûte rien et ne nécessite aucune clé.
# Chaque étape rend son propre code de retour ; rien n'est masqué.
# Le parcours navigateur, isolé — il démarre un serveur et ouvre Chromium.
# Il est INCLUS dans s5-full-gate : un test critique absent ne doit pas passer
# inaperçu derrière un « skip ».
s5-browser-gate:
	cd $(S5_APP) && python3 -m pytest -q tests/test_browser_ui.py

# Verdict de dette, calculé depuis le registre et les contrôles. Jamais déclaré.
s5-debt-gate:
	cd $(S5_APP) && python3 tools/debt_gate.py --sans-tests

s5-full-gate:
	@echo "=== 1/8  analyse statique ==="
	cd $(S5_APP) && python3 -m ruff check app tools tests migrations --select F,E9
	@echo "=== 2/8  schéma et migrations ==="
	cd $(S5_APP) && python3 -c "import sys; sys.path.insert(0,'.'); \
	from app import database, config; import migrations; \
	print('schéma', migrations.apply(database.engine(), config.DB_PATH, config.BACKUPS_DIR))"
	@echo "=== 3/8  intégrité du référentiel ==="
	cd $(S5_APP) && python3 tools/verify_integrity.py
	@echo "=== 4/8  suite complète, navigateur et échelle 60 pages compris ==="
	@echo "     (un environnement de développement incomplet fait échouer cette étape :"
	@echo "      le parcours navigateur n'est pas facultatif)"
	cd $(S5_APP) && python3 tools/check_dev_profile.py
	cd $(S5_APP) && python3 -m pytest -q -rs
	@echo "=== 5/8  réconciliation base / fichiers ==="
	cd $(S5_APP) && python3 tools/fsck.py
	@echo "=== 6/8  sauvegarde et restauration ==="
	cd $(S5_APP) && python3 tools/backup.py
	cd $(S5_APP) && python3 tools/backup.py --verifier "$$(ls -1t runtime/backups/backup_*.zip | head -1)"
	@echo "=== 7/8  état du jour et corrections réelles ==="
	cd $(S5_APP) && python3 tools/check_today_readiness.py --no-compile
	@echo "=== 8/8  verdict de dette, calculé ==="
	cd $(S5_APP) && python3 tools/debt_gate.py --sans-tests
	@echo
	@echo "S5_FULL_GATE = PASS (aucune étape n'a échoué)"

# Porte OpenRouter en conditions réelles. Séparée : elle coûte de l'argent et
# demande une clé. Fixture synthétique uniquement, jamais une vraie copie.
s5-ocr-live-gate:
	cd $(S5_APP) && python3 tools/openrouter_models.py --limite 5
	cd $(S5_APP) && python3 tools/ocr_smoke.py --verifier-aussi

# --- Lecture assistée des copies (OpenRouter) --------------------------------
# Le catalogue OpenRouter du jour, filtré sur « vision + sorties structurées ».
# Aucune clé n'est nécessaire : cet endpoint est public.
s5-ocr-modeles:
	cd $(S5_APP) && python3 tools/openrouter_models.py

# Contrôle de bout en bout de la chaîne, sur une FIXTURE SYNTHÉTIQUE uniquement.
# Nécessite OPENROUTER_API_KEY. La clé n'est jamais affichée.
s5-ocr-smoke:
	cd $(S5_APP) && python3 tools/ocr_smoke.py --verifier-aussi

# Rend les pages d'une copie rattachée, sans appeler aucun modèle. ELEVE=<student_id>
s5-ocr-rendre:
	cd $(S5_APP) && python3 -c "import sys; sys.path.insert(0,'.'); \
	from app import config, database; import migrations; \
	migrations.apply(database.engine(), config.DB_PATH, config.BACKUPS_DIR); \
	from app.domain import rasterize; from app.models import Assessment; \
	s = database.session_factory()(); \
	a = s.query(Assessment).filter_by(student_id='$(ELEVE)').one(); \
	d = rasterize.render_pages(s, a); s.commit(); \
	print('pages rendues :', d.page_count, '— pièce dérivée n°', d.source_copy_id)"

# Compare plusieurs modèles sur les pages d'une copie. ELEVE=<id> [REFERENCE=<json>]
s5-ocr-bench:
	cd $(S5_APP) && python3 tools/ocr_benchmark.py --eleve $(ELEVE) \
	  $(if $(MODELES),--modeles $(MODELES),) $(if $(REFERENCE),--reference $(REFERENCE),)

# Mesure la taille de rendu d'un PDF selon la résolution, pour justifier RASTER_DPI.
s5-ocr-mesure-dpi:
	cd $(S5_APP) && python3 -c "import sys, json; sys.path.insert(0,'.'); \
	from app.domain import rasterize; \
	print(json.dumps(rasterize.measure_legibility('$(PDF)'), ensure_ascii=False, indent=2))"
