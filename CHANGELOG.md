# Journal des modifications

## 2026.2 — 2026-08-21

- Ajout des stages de pré-rentrée **Terminale** : module `tle_spe` (spécialité
  mathématiques) et module `tle_nsi` (numérique et sciences informatiques), pour une cohorte
  de 8 élèves répartis en deux groupes selon la seconde spécialité conservée (NSI ou
  physique-chimie).
- Ajout de la documentation individualisée des élèves : un livret individuel, un plan de
  remédiation élève et un corrigé enseignant par couple (élève, matière), soit 43 documents
  nominatifs, plus les tableaux de bord et les index.
- Les livrets sont dérivés des bilans de positionnement, item par item : chaque erreur y
  figure avec son énoncé exact, la réponse donnée, la réponse attendue et l'origine de
  l'erreur. Aucun contenu n'est extrapolé au-delà du bilan.
- Ajout de `tools/extract_bilans_terminale.py`, qui fige les 14 bilans PDF en
  `content/diagnostics_terminale.json`, et de `tools/build_terminale.py`, qui génère les
  documents nominatifs à partir de ce fichier, du registre `content/students_terminale.json`
  et de la banque d'items `content/items_terminale.json`.
- La banque d'items relie chacune des 54 questions du positionnement à la compétence de
  Première évaluée, au geste correct attendu, au chapitre de Terminale qu'elle conditionne
  (BO spécial n° 8 du 25 juillet 2019) et à un exercice-variante corrigé.
- Ajout de `tests/test_terminale.py` (29 tests) : cohérence des trois sources, réalité de
  l'individualisation, confidentialité, et non-régression du pipeline mathématique existant.
- Garde-fou d'extraction : `pypdf` antérieur à la 6.16 coupe les mots des bilans sans rien
  signaler ; le script refuse désormais de s'exécuter sous ces versions, et la comparaison
  des énoncés à la banque fait échouer les tests si une extraction dégradée était committée.
- Les modules Terminale ne sont pas intégrés à `tools/build.py` : `LEVELS`,
  `content/students.json` et les manifests du pipeline mathématique sont inchangés.
- Ajout du rendu imprimable `tools/build_terminale_pdf.py` : dossiers élèves nominatifs,
  corrigés enseignants tenus à part, fiches de séances à photocopier, packs complets et
  manifeste, sous `dist/terminale/` (non versionné). L'assemblage refuse de placer un
  document enseignant dans un pack élève.
- Correction d'un défaut de poids à l'impression : WeasyPrint trace chaque point d'une
  bordure pointillée comme un objet vectoriel distinct. Les lignes de réponse des livrets
  faisaient passer un dossier de 19 pages à 1,4 Mio ; en trait plein, le même dossier pèse
  40 Kio, et l'ensemble des PDF 2,6 Mio au lieu d'une trentaine.
- Ajout de l'élève Inès Ben Yahia (groupe 2). Inscrite après la campagne de positionnement,
  elle reçoit le livret « diagnostic à établir » ; elle ne suit que les mathématiques, ce que
  son livret précise — le groupe organise les séances, il ne décrit pas une combinaison
  stricte de spécialités.
- Ajout de deux garde-fous contre la dérive des chiffres de cohorte : les effectifs de groupe
  et le total d'élèves écrits dans les documents rédigés sont comparés au registre.
- Ajout d'un PDF par séance, dans les deux modules : une fiche élève et une préparation
  enseignante pour chacune des séances S1 à S5, soit 20 fichiers. Les packs d'ensemble
  restent produits ; préparer une séance n'oblige plus à imprimer un pack de cent pages.
- Audit du rendu des cinq séances : les 40 documents de séance sont présents et complets dans
  les PDF, sans page blanche, sans section perdue, code Python et requêtes SQL rendus.
- Correction d'une régression sur le pipeline mathématique : la feuille de style d'impression
  Terminale, d'abord placée sous `assets/`, entrait dans les deux sites publiés par
  `tools/build.py` et donc dans `MANIFEST_PUBLIC.csv` et `MANIFEST_PRIVATE.csv`, faisant
  échouer l'intégration continue loin de sa cause. Elle vit désormais sous `tools/assets/`,
  et un test compare l'arborescence de `assets/` au manifeste committé pour que l'erreur se
  signale localement.

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
