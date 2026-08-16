.PHONY: audit build pdf packs qa all serve clean-generated test

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

clean-generated:
	rm -rf dist content/catalog.json MANIFEST_PUBLIC.csv MANIFEST_PRIVATE.csv

test:
	pytest -q
