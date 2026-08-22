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
        terminale-pdf terminale-pdf-list terminale-latex terminale-latex-check

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
	pytest -q tests/test_terminale.py

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
        s5-correction-qa s5-correction-backup

s5-correction-install:
	python3 -m pip install --user -r $(S5_APP)/requirements-correction.lock

s5-correction-init:
	cd $(S5_APP) && python3 tools/init_database.py

s5-correction-run:
	cd $(S5_APP) && python3 -m app.cli serve

s5-correction-test:
	cd $(S5_APP) && python3 -m pytest -q

s5-correction-qa:
	cd $(S5_APP) && python3 tools/verify_integrity.py && python3 -m pytest -q

s5-correction-backup:
	cd $(S5_APP) && python3 tools/backup.py
