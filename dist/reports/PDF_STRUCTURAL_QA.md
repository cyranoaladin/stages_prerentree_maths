# QA structurelle PDF — 2026-08-16

Contrôle exhaustif (pas d'échantillonnage) des **216 PDF générés** : 138 documents unitaires dans
`dist/pdf/` (4 niveaux × [élèves, enseignants, évaluations, supports, nominatifs-prives]) et 78 packs
combinés dans `dist/packs/` (par niveau, par séance, par élève). Les PDF sources d'origine
(`04_NOMINATIFS/*/bilan-nexus-*.pdf`, `03_EVALUATIONS/*_Test_Initial.pdf`) ne sont pas des PDF générés et
sont exclus de ce contrôle — ils sont copiés sans altération (voir `MANIFEST_PRIVATE.csv`).

## Outils utilisés

Réellement exécutés en ligne de commande sur chacun des 216 fichiers, pas de simulation :

- `qpdf 11.9.0 --check` — intégrité structurelle du PDF.
- `pdfinfo 24.02.0` — format de page, nombre de pages, chiffrement.
- `pdffonts 24.02.0` — incorporation des polices.
- `pdftotext 24.02.0` — extractibilité du texte et recherche de fuite de corrigé.
- Contrôle Python additionnel : `tools/build.py::is_a4_page` (tolérance 2 pt) et recherche de PII
  croisée entre élèves dans les packs `nominatifs-prives`.

Script conservé sous `tmp/pdf_qa/structural_qa.py` (hors dépôt de production, résultat détaillé dans
`tmp/pdf_qa/structural_results.csv`).

## Résultats globaux

```text
PDF contrôlés         : 216 (138 unitaires + 78 packs)
Pages totales          : 2622
qpdf --check échecs    : 0
Format non-A4           : 0
PDF chiffrés            : 0
Polices non incorporées : 0
Texte non extractible   : 0
Fuite de corrigé (côté élève, 34 PDF eleves + 12 packs eleves contrôlés) : 0
PII croisée (22 dossiers/packs nominatifs-prives contrôlés)              : 0
PDF_STRUCTURAL_FAILURE_COUNT = 0
```

## Détail des contrôles

1. **Intégrité (`qpdf --check`)** — 216/216 PDF sans erreur ni avertissement de structure interne
   (xref, flux, objets).
2. **Format A4** — 216/216 pages rapportées par `pdfinfo` à 595,28 × 841,89 pt (tolérance ± 2 pt),
   portrait, conforme à la section 8.1 du mandat. Aucun document en paysage (aucun support n'en avait
   besoin).
3. **Chiffrement** — 0 PDF chiffré ; tous ouvrables et imprimables sans mot de passe.
4. **Polices** — toutes les polices utilisées (Arimo, DejaVu Sans, variantes gras) sont incorporées
   (colonne `emb=yes` de `pdffonts` sur l'intégralité des fichiers), donc rendu fidèle sur tout poste sans
   dépendre des polices système.
5. **Texte extractible** — `pdftotext` produit du texte non vide sur les 216 fichiers ; aucun document
   n'est une image scannée sans couche texte.
6. **Absence de corrigé côté élève** — recherche des mots « corrigé », « corrigée », « barème » (et
   variantes) dans le texte extrait de chaque PDF du bucket `eleves` et de chaque pack élève (`PACK_ELEVE*`,
   `S*_PACK_ELEVE`) : 0 occurrence. Un premier passage avec une expression régulière trop large avait
   signalé à tort les champs de réponse vierges (« Réponse : ..... ») comme suspects ; vérifié
   individuellement et confirmé sans rapport avec un corrigé — expression corrigée avant ce résultat final.
7. **Étanchéité nominative** — pour chaque pack `PACK_TRAVAIL_PERSONNALISE` et
   `DOSSIER_ENSEIGNANT_CONFIDENTIEL` (22 fichiers, 11 élèves × 2), recherche des 10 autres noms d'élèves
   dans le texte extrait : 0 occurrence croisée.
8. **Pages vides/taille** — 0 PDF de taille nulle, 0 échec d'ouverture par `pypdf`/`qpdf`.

## Ce qui reste couvert par l'inspection visuelle, pas par ce contrôle structurel

Ce contrôle vérifie la structure et le contenu textuel extractible, pas le rendu visuel (mise en page,
débordement, chevauchement, netteté des figures SVG). Voir `reports/PDF_VISUAL_QA.md` pour l'inspection
visuelle réelle (planches-contact rasterisées et relecture image par image).
