# Documentation stages maths — design

## Décision

Le paquet devient une documentation statique locale générée par un unique outil Python. Les Markdown existants restent les sources pédagogiques dérivées ; les quatre programmes de `05_SOURCES` restent canoniques et ne sont jamais réécrits par le build.

## Architecture

- `content/catalog.json` est le registre généré des documents actifs et de leur audience.
- `tools/build.py` produit catalogues, HTML, PDF, packs, manifests et rapports QA via des sous-commandes cohérentes.
- `dist/site-public/` ne contient aucun document nominatif ; `dist/site-private/` contient les accès nominatifs, explicitement signalés comme confidentiels.
- `dist/pdf/` contient les PDF unitaires séparés par audience ; `dist/packs/` contient les assemblages.
- Les index, la recherche et les menus sont générés à partir du catalogue ; aucune page de navigation n'est maintenue en parallèle.

## Rendu et confidentialité

Pandoc produit le contenu HTML avec MathML local, puis une enveloppe sémantique commune applique `assets/site.css` et `assets/print.css`. WeasyPrint est l'unique moteur PDF choisi : il est local, déjà disponible, lit le HTML/CSS et permet un rendu A4 reproductible. Les PDF nominatifs gardent les seules données du dossier concerné ; les sources PDF nominatives ne sont ni copiées dans les packs ni référencées par le site public.

## Validation

Les tests vérifient le classement public/privé, la génération du registre et les règles de nommage. La QA vérifie liens, structure HTML, ressources externes, fuites de corrigés/PII, documents attendus, structure PDF et calcul des séances. Chaque PDF généré est rasterisé, indexé dans un rapport de QA visuelle et vérifié par planche-contact.
