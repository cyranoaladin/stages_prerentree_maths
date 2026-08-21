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
