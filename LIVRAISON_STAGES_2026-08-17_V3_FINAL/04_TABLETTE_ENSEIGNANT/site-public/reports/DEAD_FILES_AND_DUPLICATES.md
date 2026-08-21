# Fichiers morts et doublons — 2026-08-16

## Doublons de contenu HTML actif

**DUPLICATE_ACTIVE_FILE_COUNT = 0 défaut réel.**

60 paires de fichiers HTML strictement identiques (sha256) ont été trouvées entre `dist/site-public/...` et `dist/site-private/...` pour un même document non confidentiel (ex. `1ere_spe_S1_ELEVE_Activite.html`). **Ce n'est pas un doublon problématique** : c'est le comportement voulu de `tools/build.py::build_html`, qui écrit chaque document public à la fois dans le site public et en miroir dans le site privé (pour qu'un utilisateur en zone privée retrouve tout, sans devoir naviguer entre deux portails). Les chemins relatifs internes (racine, niveau) sont recalculés indépendamment pour chaque site mais aboutissent au même texte car les deux arborescences ont la même profondeur — d'où l'identité byte à byte. Aucune action requise.

## Doublons de sources Markdown

**0 doublon exact** trouvé parmi les `.md` opérationnels des 4 niveaux (142 fichiers, hachage sha256, hors `05_SOURCES`). Chaque fiche élève/professeur/support est un contenu distinct. Conforme à la section 5.1.

## Fichiers morts — HTML hérité de l'ancienne chaîne de build

**138 fichiers `.html`** trouvés directement à côté de leur source `.md` dans `4e/`, `3e/`, `2nde/`, `1ere_spe/` (ex. `4e/02_SEANCES/S1/4e_S1_ELEVE_Activite.html`) sont la sortie de l'ancien script `build_all_html.py` (`pandoc -s --mathml --css assets/print.css --embed-resources ...`, un HTML autonome par fichier Markdown, sans portail, sans breadcrumb, sans séparation public/privé). Cette chaîne est **remplacée** par `tools/build.py`, qui régénère l'intégralité de `dist/site-public` et `dist/site-private` à partir du même contenu source. Ces 138 fichiers ne sont plus référencés par aucune page active de `dist/` (confirmé par l'analyse de liens de `reports/NAVIGATION_QA.md`) ni par `content/catalog.json`.

**Recommandation** (non appliquée par ce script, à valider par l'intégrateur) : conformément à la règle « ne détruis aucun travail existant » (section 4.1) et à la préservation des originaux, ne pas supprimer mais **archiver** ces 138 fichiers, par exemple en les déplaçant sous `_archive/legacy-html-pre-refactor-20260816/` en conservant l'arborescence relative, puis en retirant `build_all_html.py` de la racine (remplacé par `python3 tools/build.py html`) une fois l'archivage confirmé. Ne pas les inclure dans un futur `make clean-generated`, qui doit se limiter à `dist/`.

Liste complète des 138 chemins : `reports/LEGACY_HTML_TO_ARCHIVE.txt`. Échantillon représentatif :

```text
4e/00_MASTER/4e_MASTER_Documentation_Stage.html
4e/02_SEANCES/S1/4e_S1_ELEVE_Activite.html
4e/02_SEANCES/S1/4e_S1_PROF_Fiche.html
4e/04_NOMINATIFS/Sinda_Chikhaoui/4e_Dossier_Individuel_Sinda_Chikhaoui.html
... (un fichier .html hérité par fichier .md source, 138 au total sur les 4 niveaux)
```

## Fichiers morts — racine

**Traité par l'intégrateur le 2026-08-16, après validation que `tools/build.py` reconstruit correctement les deux sites, tous les PDF et tous les packs.** Rien n'a été supprimé : tout a été déplacé (pas de perte de travail) sous `_archive/legacy-html-pre-refactor-20260816/`, arborescence relative conservée :

- Les 138 `.html` hérités à côté des sources `.md` des 4 niveaux + les 4 `.html` hérités des sources canoniques `05_SOURCES/` (142 fichiers au total).
- `build_all_html.py` (chaîne remplacée par `python3 tools/build.py all`, seule chaîne canonique désormais).
- `INDEX.md` / `INDEX.html` : pointaient vers les anciens `.html` hérités par niveau, désormais archivés ; remplacés par le portail généré `dist/site-public/index.html`.
- `RAPPORT_LIVRAISON.md` / `.html` : rapport de livraison de la première version, remplacé par `reports/FINAL_DELIVERY_REPORT.md`.
- `MANIFEST.csv` : manifeste tenu à la main, remplacé par `MANIFEST_PUBLIC.csv` / `MANIFEST_PRIVATE.csv` générés depuis `content/catalog.json` (empreintes SHA-256, régénérés à chaque build).

Aucune source canonique, aucun PDF nominatif d'origine, aucun bilan élève/parent n'a été déplacé ni modifié par cette opération.

## Fichiers vides

0 fichier vide trouvé parmi les sources actives (confirmé par la baseline `reports/AUDIT_INITIAL.md`, non recontrôlé ici).

## Compteur retenu

```text
DUPLICATE_ACTIVE_FILE_COUNT=0
```

(60 miroirs public/privé intentionnels exclus du décompte ; 138 fichiers HTML hérités classés comme fichiers morts à archiver, pas comme doublons actifs puisqu'ils ne sont plus dans le graphe de navigation actif.)
