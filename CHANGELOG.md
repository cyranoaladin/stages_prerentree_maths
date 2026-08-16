# Journal des modifications

## 2026.1 — 2026-08-16

- Ajout d’un catalogue documentaire et d’une chaîne de build Python unique.
- Ajout de sites locaux public et privé, recherche sans réseau, navigation et pages utilitaires.
- Ajout de PDF A4 unitaires, packs, manifests à empreintes et QA automatisée.
- Préservation explicite des sources canoniques et des PDF initiaux.
- Correction d’un bug de classification (documents enseignants routés à tort en zone nominative privée),
  d’un bug de lien relatif dans les pages de niveau, et normalisation de la syntaxe mathématique
  `(...)`/`[...]` du corpus vers `$...$`/`$$...$$` (ERR-005 à ERR-007).
- Correction d’un défaut bloquant de rendu PDF : WeasyPrint ne met pas en page les fractions/exposants/
  indices/racines MathML ; remplacé par un rendu HTML/CSS local (ERR-009).
- Correction d’une fuite de corrigé enseignant dans le pack de travail élève nominatif, par scission des
  documents de remédiation ciblée en version élève et version enseignant (ERR-008).
- Archivage de l’ancienne chaîne `build_all_html.py` et de ses sorties (`_archive/legacy-html-pre-refactor-20260816/`).
- Inspection visuelle réelle de 77 PDF (394+ pages) et contrôle automatisé exhaustif des 227 PDF générés ;
  build reproductible confirmé (511/511 fichiers identiques sur deux builds consécutifs).
