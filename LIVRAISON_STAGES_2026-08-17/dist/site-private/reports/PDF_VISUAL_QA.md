# QA visuelle des PDF — inspection réelle, 2026-08-16

Ce rapport documente l'inspection visuelle réelle (lecture d'images rasterisées par l'outil de vision,
page par page) exigée par la section 10.4 du mandat, et distingue clairement ce qui a été **vu à l'œil**
de ce qui a été **contrôlé automatiquement** sur l'ensemble du paquet. Aucune inspection n'est déclarée
sans avoir été réellement effectuée.

## 1. Méthode

- Rasterisation avec `pdftoppm` (110–200 dpi selon le contrôle) et planches-contact assemblées avec
  `montage` (ImageMagick), conservées sous `tmp/pdf_qa/` (hors dépôt de production).
- Lecture directe des images par l'outil de vision, une planche à la fois, en comparant au gabarit attendu
  (section 8 du mandat : consigne, espace de réponse, absence de corrigé côté élève, figures nettes,
  tableaux non coupés, etc.).
- Tout défaut trouvé a été corrigé dans les sources, puis un **nouveau build complet** a été lancé et le
  point précis re-vérifié (texte extrait et/ou nouvelle capture) avant de continuer.

## 2. Échantillon inspecté à l'œil (échantillon stratifié, pas un sondage aléatoire)

**77 documents PDF sur 227 (34 %)**, choisis pour couvrir chaque type de document à chaque niveau plutôt
qu'un tirage aléatoire :

- 100 % des 22 dossiers/remédiations nominatifs (11 élèves × 2 documents, après la scission élève/corrigé
  d'ERR-008) ;
- 100 % des 8 évaluations finales + mini-diagnostics (élève et corrigé) par niveau ;
- 100 % des 4 guides formateur et 4 tableaux de bord enseignant ;
- la séance 1 complète (élève, professeur, supports, aides) des 4 niveaux ;
- un échantillon des 4 documents maître (« MASTER ») : 21 pages sur ~94 à 113 par document (les 10
  premières, 5 centrales, 5 dernières) — ce sont les documents les plus longs et les plus à risque de
  problème de pagination ; ils n'ont **pas** été inspectés intégralement page par page, voir §5.

Soit environ 394 pages effectivement vues à l'œil sur les 2 749 pages totales du paquet (~14 %), en plus
des quatre échantillons partiels de MASTER.

## 3. Défauts réels trouvés par cette inspection (et seulement par elle — aucun script ne les aurait vus)

Chacun est documenté en détail, avec preuve et correction, dans `reports/SOURCE_ERRATA.md` :

1. **ERR-009 — WeasyPrint ne met pas en page `<mfrac>`/`<msup>`/`<msub>`/`<msqrt>`** : une fraction
   `3/4 ÷ 2/5` s'affichait « 34÷25 » (chiffres concaténés, sans barre de fraction), un exposant `2^3`
   s'affichait « 23 ». Défaut le plus grave du paquet : trouvé en ouvrant une simple fiche de 2nde Séance 1
   et en constatant que le résultat affiché ne ressemblait à aucune fraction lisible. Corrigé par un
   post-traitement MathML → HTML/CSS dans `tools/build.py` (voir ERR-009 pour le détail et les tests
   unitaires WeasyPrint isolés qui ont validé chaque brique — `<sup>`/`<sub>` natifs, fraction empilée en
   `display:inline-block`, `\qquad` en espace).
2. **Fuite de l'annotation MathML côté PDF (partie d'ERR-007/ERR-009)** : une formule apparaissait deux
   fois — une fois rendue, une fois en LaTeX brut juste après (`−4° -4^\circ` C) — parce que WeasyPrint
   affichait l'élément `<annotation>` (censé rester invisible) que Pandoc ajoute pour l'accessibilité.
   Corrigé par une règle CSS explicite (`math annotation { display:none }`), le rendu par post-traitement
   MathML→HTML/CSS d'ERR-009 rend d'ailleurs cette fuite structurellement impossible désormais.
3. **Liens d'image cassés (14 fichiers, 41 figures)** : les droites graduées et bandes fractionnaires des
   documents SUPPORTS ne s'affichaient pas — syntaxe `![légende](chemin.svg)` corrompue en
   `![légende]$chemin.svg$` par un effet de bord du script de normalisation mathématique (voir ERR-006/007).
   Trouvé en constatant l'absence totale de figure sur `4e_S1_SUPPORTS_Manipulation`. Corrigé, script
   normalisateur durci pour ne plus jamais toucher une parenthèse de lien Markdown.
4. **ERR-008 — corrigé enseignant dans le pack de travail élève nominatif** : la section « Corrigé
   enseignant » d'un exercice de remédiation ciblée apparaissait dans le PDF remis à la famille. Trouvé en
   lisant intégralement un dossier `Remediation_Ciblee` d'élève et en voyant le corrigé enchaîner
   directement après les exercices, sans séparation de document. Corrigé par scission en deux fichiers
   (voir ERR-008).
5. **Crochets `[ ]` littéraux résiduels et signes `$` isolés** : plusieurs dizaines d'occurrences à travers
   le paquet où une formule par ailleurs correcte restait entourée de crochets bruns visibles, ou où un `$`
   isolé apparaissait dans le texte (conflit entre deux passages successifs du script de normalisation sur
   un même contenu). Trouvé en lisant les corrigés de fin de fiche (« 3²=9 $5. 8,3×10⁻⁴$ ») et une ligne de
   tableau du guide formateur de 2nde transformée en texte brut par le même mécanisme. Corrigé fichier par
   fichier avec preuve avant/après (voir ERR-006/007/009) ; contrôle de non-régression ajouté : recherche de
   tout caractère `$` isolé dans le texte extrait (`pdftotext`) des 227 PDF générés — **0 occurrence**
   restante, et recherche de tout déséquilibre de parenthèses supérieur à 3 dans le même texte — **0**
   occurrence.

## 4. Contrôle automatisé complémentaire — 100 % des 227 PDF, 2 749 pages

Après correction, en plus de la relecture visuelle ciblée des zones précédemment cassées, un contrôle
automatisé (pas visuel, texte extrait) a été relancé sur l'intégralité des PDF générés :

```text
PDF contrôlés (structurel, qpdf/pdfinfo/pdffonts/pdftotext/A4) : 227 / 227 — 0 défaut
PDF avec code LaTeX brut visible (recherche \commande hors <annotation>) : 0 / 153 fichiers source
PDF avec signe $ isolé résiduel dans le texte extrait : 0 / 227
PDF avec déséquilibre de parenthèses (> 3) dans le texte extrait : 0 / 227
Build reconstruit deux fois de suite : 511 / 511 fichiers identiques (sha256)
```

## 5. Ce qui n'a pas été inspecté à l'œil, page par page, et doit rester marqué comme tel

- Les pages 22 à 88 environ des quatre documents MASTER (les plus longs du paquet) n'ont pas été vues
  individuellement à l'œil — seul un échantillon de 21 pages par document l'a été, plus le contrôle
  automatisé texte (leak, `$`, parenthèses) qui, lui, couvre bien 100 % de leurs pages.
- Les 78 PDF de packs (`dist/packs/`) sont des concaténations directes des PDF unitaires déjà contrôlés
  (via `pypdf`, sans nouveau rendu) : leur contenu visuel est donc identique page à page à celui des PDF
  unitaires déjà inspectés ; seule leur structure d'assemblage (page manquante, ordre, pack élève/enseignant
  correctement séparé) a été vérifiée, pas un second passage visuel intégral de leurs pages.
- Le rendu réel dans un lecteur PDF grand public (Adobe Acrobat, aperçu macOS/Windows) n'a pas été testé ;
  seuls WeasyPrint (production), `pdftoppm`/`mutool` (rasterisation de contrôle) et l'extraction texte
  Poppler ont servi de référence.

## 6. Verdict

Aucun défaut visuel connu ne subsiste dans l'échantillon inspecté à l'œil ni dans le contrôle texte
exhaustif des 227 PDF. `PDF_VISUAL_DEFECT_COUNT = 0` (défauts trouvés puis corrigés, listés au §3 ;
compteur final après correction et re-contrôle).
