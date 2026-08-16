# Stages de pré-rentrée Mathématiques 2026-2027

Ce paquet local rassemble les stages d’entrée en `4e`, `3e`, `2nde` et `1ere_spe`. Il génère un portail hors ligne, des PDF A4 et des packs d’impression à partir des Markdown opérationnels.

## Démarrer

```bash
python3 -m pip install -r requirements.lock
make all
make serve
```

Ouvrez ensuite `http://localhost:8000`. Le portail public est dans `dist/site-public/`; le portail confidentiel est dans `dist/site-private/` et ne doit pas être diffusé.

## Dépendances

- **Python** : dépendances verrouillées dans `requirements.lock` (WeasyPrint, pypdf, pytest, ...).
- **Système** : Pandoc, qpdf, Poppler (`pdftotext`), Ghostscript ou ImageMagick (`convert`/`identify`) pour l’inspection visuelle des PDF.
- Aucune police n’est téléchargée à distance : le build fonctionne hors ligne.

## Source et confidentialité

- `05_SOURCES/` contient les programmes canoniques : le build ne les modifie pas.
- `04_NOMINATIFS/` et `dist/site-private/` contiennent des données de mineurs : circulation locale strictement limitée.
- Les PDF sources initiaux sont préservés et exclus des packs générés.
- Le registre nominatif canonique (13 élèves) est `content/students.json` ; `tools/build.py` ne contient plus aucun nom en dur.

## Module Première NSI

Le dépôt contient également un module indépendant `1re_nsi/` (stage Python, Première NSI). Il n’est **pas** intégré au pipeline mathématique `tools/build.py` (niveaux `4e`, `3e`, `2nde`, `1ere_spe`) : c’est un pipeline de documentation séparé, avec ses propres Markdown, HTML et PDF déjà générés et versionnés directement dans l’arborescence `1re_nsi/`. Point d’entrée : [`1re_nsi/00_MASTER/index.md`](1re_nsi/00_MASTER/index.md).

Voir `QUICK_START.md` et `PRINT_GUIDE.md` pour les usages courants.
