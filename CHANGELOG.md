# Journal des modifications

## 2026.6 — 2026-08-22

- Ajout d'un contrôle des débordements de marge à la construction des PDF : LaTeX les
  signale dans son journal, `tools/build_terminale_pdf.py` les remonte document par
  document. Ils ne font pas échouer la compilation — le PDF sort, avec une ligne hors de
  la page —, et c'est le seul moment où on peut encore les voir.
- Correction des 18 documents que ce contrôle a révélés, sur 65. Trois causes distinctes,
  toutes dans le calcul des largeurs de colonnes :
  - un mot ne se coupe pas, et aucune colonne ne peut être plus étroite que le sien :
    `**CONFRONTER**` débordait de 39 pt dans la table des priorités de chaque livret ;
  - une capitale occupe environ 1,4 fois la chasse d'une bas-de-casse et le gras 1,1 fois
    celle du romain : compter les caractères sans en tenir compte sous-estimait ce mot de
    moitié ;
  - la normalisation appliquée après coup ramenait les colonnes sous leur propre plancher.
    Les planchers sont désormais réservés d'abord, le reste de la justification étant
    réparti au prorata du contenu.
- Correction du dimensionnement des tableaux larges et creux : la table
  hexadécimal/décimal/binaire de la séance 1 de NSI débordait de 23 pt par le seul blanc
  entre ses dix-sept colonnes. Au-delà de huit colonnes courtes, le blanc est resserré
  plutôt que le texte justifié.
- Correction de deux figures de physique-chimie : les trois schémas de lentille de la
  séance 4 se touchaient et se lisaient comme un seul axe portant trois lentilles ; le
  libellé de la flèche du premier principe, en séance 3, mordait sur les deux encadrés
  qu'elle relie.
- `pH` se compose désormais en romain à l'intérieur d'une formule : en italique,
  `10^{-pH}` se lit comme le produit d'un p par un H. Même traitement pour `pOH`, `pKa`
  et `pKe`.
- Ajout de cinq tests sur le calcul des largeurs de colonnes et la composition du pH.
  L'intégration continue peut les exécuter sans distribution TeX ; la composition
  elle-même reste vérifiée à la construction des PDF.

## 2026.5 — 2026-08-22

- Ajout du module **`tle_pc`**, stage de pré-rentrée de spécialité physique-chimie : le
  programme complet du stage, le guide du formateur, cinq séances de deux heures avec pour
  chacune une fiche élève, une fiche professeur, des supports de manipulation et cinq
  cartes d'aide graduées, un mini-diagnostic d'entrée, une évaluation finale avec son
  barème, un mémento de formules et un portfolio. Trois élèves y sont inscrits.
- Progression fondée sur le diagnostic réel du groupe et sur ce que la Terminale exige :
  séance 1 les transformations chimiques — la seule erreur commune aux trois élèves, et le
  domaine qui conditionne cinq chapitres de Terminale ; séance 2 la mécanique, domaine le
  plus faible (16,7 %) ; séance 3 l'énergie ; séance 4 les ondes et l'optique ; séance 5
  l'électricité, la chimie organique, la mesure et l'évaluation.
- Composition de la cohorte portée à neuf élèves et à quatre groupes, définis par les
  stages suivis : maths et NSI (4), maths seules (2), maths et physique-chimie (2),
  physique-chimie seule (1). Huit élèves suivent le stage de mathématiques, quatre celui de
  NSI, trois celui de physique-chimie.
- La progression de physique-chimie de l'établissement n'étant pas disponible, le module
  repose sur le seul programme officiel et le dit explicitement : aucune séance ne présume
  d'un ordre de chapitres.
- Les conventions propres à chaque module — répertoire des sources, nom du support de
  séance, préfixe du mini-diagnostic, contenu du portfolio — passent du code au registre
  `MODULES` : `tools/build_terminale_pdf.py` ne teste plus la clé du module en six
  endroits.
- Correction de sept défauts du convertisseur de notation, tous révélés par la
  physique-chimie : `\ce{}` emballé dans lui-même à chaque passage, `L⁻¹` pris pour un ion,
  une équation de réaction ré-emballée espèce par espèce, `1 200 kg` coupé par son
  séparateur de milliers, `CH₃-CO-CH₃` découpé en trois formules, deux formules contiguës
  refermant et rouvrant le mode mathématique au même endroit — ce que LaTeX lit comme une
  formule hors-texte —, et une unité reconnue par-dessus une fin de ligne (« séance 5 » +
  « L'évaluation » donnait `\SI{5}{\litre}`).
- Correction de deux défauts de rendu que seule l'impression révélait : les commandes LaTeX
  écrites au fil du texte ressortaient littéralement, backslash compris, parce que pandoc
  ne transmet le LaTeX brut qu'à l'intérieur des délimiteurs mathématiques ; et les
  tableaux débordaient de la page, le lecteur `gfm` ne transportant aucune largeur de
  colonne. Les largeurs sont désormais calculées à partir du contenu réel de chaque
  colonne.

## 2026.4 — 2026-08-22

- Passage du rendu des stages Terminale à **LaTeX**. Pandoc traduit chaque document en
  LaTeX, la charte `tools/assets/nexus_terminale.sty` — dérivée de `_common/nexusS5.sty`,
  mêmes couleurs et mêmes encadrés — lui donne sa forme, et `latexmk` compose le PDF avec
  LuaLaTeX. Y sont chargés les paquets propres aux trois disciplines : `amsmath`,
  `mathtools`, `esvect` et `stmaryrd` pour les mathématiques, `siunitx`, `mhchem` et
  `chemfig` pour la physique-chimie, `listings` et `algorithm2e` pour le code, `pgfplots`
  et `tikz` pour les figures.
- Choix de LuaLaTeX plutôt que pdflatex, sur mesure et non par principe : avec pdflatex,
  `listings` et `inputenc` se disputent les caractères accentués des commentaires Python et
  composent « le tableau doit ê tre é tri » au lieu de « doit être trié » ; ni `literate` ni
  `extendedchars` ne corrigent la permutation sous TeX Live 2023. Les modules Terminale
  contiennent du code commenté en français : la contrainte est structurelle.
- Conversion du corpus Terminale en notation mathématique réelle. Les documents écrivaient
  `u₀`, `0,5^n`, `≥`, `☐`, `Δ`, `Cu²⁺` — une approximation en caractères Unicode, fausse
  typographiquement et incapable d'exprimer une limite ou une intégrale. Ils écrivent
  désormais `$u_0$`, `$0{,}5^n$`, `$\geqslant$`, `$\square$`, `$\Delta$`, `\ce{Cu^2+}`.
  `tools/latex_notation.py` fait la conversion, `tools/mathify_terminale.py` l'applique aux
  documents rédigés à la main, et `tools/build_terminale.py` aux livrets nominatifs, dont le
  texte vient des bilans PDF.
- Ajout de la reconnaissance des unités et des équations de réaction pour la
  physique-chimie : « 3,0 × 10⁸ m·s⁻¹ » devient `\SI{3.0e8}{\metre\per\second}` et
  « 2 H₂ + O₂ → 2 H₂O » devient `\ce{2 H2 + O2 -> 2 H2O}`, composés par siunitx et mhchem
  selon les conventions de la discipline.
- Remplacement des douze schémas en art ASCII par de vraies figures : tableaux de signes,
  droite graduée de l'ensemble solution, courbe de l'exponentielle et son asymptote, droites
  parallèles de la séance 4, cube de la géométrie dans l'espace, arbre de probabilité,
  tables des poids binaires et des indices négatifs. Ils passent par des blocs
  `` ```{=latex} `` que pandoc transmet tels quels.
- Ajout de trois tests qui refusent la source plutôt que le PDF : aucun caractère que la
  police ne saurait dessiner, aucun délimiteur mathématique laissé ouvert, aucune prose
  française absorbée dans une formule. Un caractère manquant ne fait pas échouer la
  compilation — il laisse un trou dans la consigne, et personne ne le voit avant
  l'impression.
- Correction, au fil de la conversion, de sept familles d'erreurs du convertisseur, toutes
  vérifiées sur le corpus : la dernière lettre d'un mot français prise pour une variable
  (« la suit$e$ »), le « a » du verbe avoir happé par la formule (« $x^2 - 4 a$ pour
  racines »), l'apostrophe d'élision confondue avec la dérivée (« $e^x = 0 n$'a pas de
  solution »), l'étiquette d'énumération avalée (« $b) u_{n+1}$ »), la parenthèse ouvrante
  de la phrase retenue dans l'expression, l'exposant parenthésé `e^(3x)` scindé en deux, et
  `log_2` laissé sans sa fonction.
- Correction du chevauchement de l'entête : un intitulé de séance long recouvrait la marque
  « NEXUS RÉUSSITE » en haut de chaque page.

## 2026.3 — 2026-08-22

Corrections de la composition de la cohorte Terminale, sur informations de l'organisme.

- Cadre du stage inscrit dans les documents : **Nexus Réussite**, centre d'accompagnement
  scolaire ; **10 heures par enseignement de spécialité**, 2 heures par jour, 5 jours
  consécutifs, **du 24 au 28 août 2026**. Un élève suivant deux spécialités accompagnées
  suit deux stages de 10 heures.
- Retrait d'Ahmed Benhadj Salem, qui ne suit aucun stage en Terminale. Ses six documents
  nominatifs sont supprimés ; le groupe 1 passe de 5 à 4 élèves.
- Les groupes désignent désormais les **stages suivis**, et non une combinaison de
  spécialités : « Mathématiques et NSI » (4 élèves) et « Mathématiques » (4 élèves). Dans le
  second, deux élèves suivent aussi la physique-chimie — sans stage dédié dans ce dispositif
  — et deux ne suivent qu'un enseignement accompagné. Chaque livret annonce les spécialités
  réelles de son élève.
- **Les mathématiques expertes ne font plus l'objet d'un stage ni de documents séparés.**
  L'option est préparée sur le temps différencié du stage de mathématiques, et le diagnostic
  d'option de chaque élève concernée est reversé dans son livret de mathématiques, section
  « Option annuelle », avec la même exigence que le reste : énoncé exact, réponse donnée,
  origine de l'erreur. Leurs exercices d'option complètent leur feuille de remédiation.
- Ajout d'une **détection d'orphelins** à `tools/build_terminale.py` : un document nominatif
  que la génération ne produit plus est supprimé, et un répertoire d'élève vidé l'est aussi.
  Sans cela, le retrait d'un élève laissait ses documents confidentiels sur le disque, prêts
  à être imprimés. `--check` les signale.
- Les tests suivent : un élève doit déclarer les spécialités qu'il suit réellement, l'option
  annuelle doit être fondue dans le livret de mathématiques et nulle part ailleurs, et ses
  exercices doivent atteindre les deux versions de la feuille de remédiation.

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
