# Journal des modifications

## 2026.11 — 2026-08-22

Audit de la pagination des cahiers d'élèves, déclenché par un doute sur leur épaisseur.
Le doute était fondé, et il désignait trois défauts qui allaient tous dans le même sens :
**les meilleurs élèves recevaient le moins de travail.**

- **Le bloc de la piste excellence était introuvable dans dix fiches sur quinze.** Le titre
  s'écrit « Exercices 9 et 10 — piste Excellence » en mathématiques et « Piste excellence —
  exercices 11 et 12 » en NSI, « Piste excellence — exercices 9 et 10 » en physique-chimie.
  Le motif cherché était sensible à la casse. Aucun élève de NSI ni de physique-chimie n'est
  aujourd'hui routé sur cette piste, donc rien ne s'était vu : le premier qui l'aurait été
  aurait reçu une séance **sans le moindre exercice d'entraînement**. Le repérage ignore
  désormais la casse, et un test parcourt les douze couples (module, séance) concernés.
- **L'atelier Terminale n'entrait dans aucun cahier** — zéro séance sur soixante-quinze. Le
  drapeau qui l'ouvre était calculé pour l'option maths expertes, qui ne concerne que les
  mathématiques : pour NSI et physique-chimie il valait donc toujours faux. Dix ateliers
  écrits, destinés par leur propre texte à « quiconque a terminé sa piste avant la fin du
  temps différencié », n'ont jamais quitté la fiche collective. Ils rejoignent les cahiers
  des pistes qui les atteignent — Consolider, Entretenir, Excellence — et pas les autres :
  donner un bloc de trente-cinq lignes à un élève qui a huit exercices devant lui épaissit
  son cahier sans le nourrir, et noie ce qui lui est propre sous un contenu identique pour
  tout le groupe.
- **La piste excellence n'ouvrait que deux exercices**, contre six en médiane pour les
  pistes de remédiation, pour le même créneau de trente minutes. Un élève d'excellence en
  mathématiques qui ne suit pas l'option maths expertes n'avait donc rien d'autre. Il reçoit
  d'abord la série d'entretien — qu'il traitera vite, et qui exige déjà la démonstration
  rédigée en entier — puis ses deux problèmes.

Après correction, la médiane de tâches par séance va de 5 à 7 selon la piste, contre 2 à 6
avant. L'écart minimal entre deux cahiers d'élèves aux bilans différents passe de 17,3 % à
20,5 %.

Six tests tiennent ces trois correctifs, et les trois régressions correspondantes ont été
réintroduites une à une pour vérifier qu'ils les rattrapent : ils les rattrapent.

## 2026.10 — 2026-08-22

Relecture des documents que rien n'avait encore contrôlés : le mémento de physique-chimie,
la place curriculaire de chaque notion, et les 416 pages destinées à l'enseignant.

**Le mémento de formules de physique-chimie**, relu ligne à ligne contre le programme de
Première de 2019, portait quatre défauts. C'est le seul document du corpus que l'élève
emporte en septembre : ce qui y est faux le suit toute l'année.

- `P = U I = R I²` enchaînait une loi générale et une loi qui ne vaut que pour un conducteur
  ohmique — ni pour une pile, ni pour un moteur. Les deux relations sont désormais séparées,
  avec leur domaine de validité.
- La conservation de l'énergie mécanique était réduite à « sans frottement ». Une force
  motrice la rompt tout autant : la condition est que le poids soit la seule force qui
  travaille.
- La longueur d'onde d'un son audible était donnée « de quelques centimètres à quelques
  mètres ». À 20 Hz elle vaut 17 m.
- Un espace parasite séparait les deux arguments d'un `\SI`.

**Audit curriculaire.** `tools/qa_curriculum.py` vérifie qu'aucune notion de Terminale n'est
présentée comme un acquis antérieur, que chaque domaine du positionnement porte son prérequis
et son ouverture, que le programme de mathématiques publié en avril 2026 n'est jamais donné
pour applicable à cette cohorte, et que toute notion de Terminale qui apparaît est annoncée
comme telle. 1524 contrôles. Il a trouvé :

- **la variante de l'item 9 de physique-chimie demandait le vecteur accélération** — introduit
  en Terminale — pour remédier à une lacune de Première. Un élève qui échouait dessus était
  compté en déficit sur une notion qu'il n'a pas encore rencontrée ;
- **le champ `ouverture_terminale` était servi au professeur comme « argument à donner à
  l'élève »** : cinq notions de l'année à venir, à citer à quelqu'un qui bute sur l'année
  passée. C'est un repère curriculaire, pas un texte à lire ;
- un piège de Première se corrigeait par l'énergie interne, une question de recul demandait
  du SQL sans dire que SQL est de Terminale, et l'auto-évaluation finale de NSI mettait huit
  énoncés de Première et deux de Terminale sur le même plan.

**Balayage visuel des documents enseignant.** Il a trouvé ce que le contrôle de densité ne
pouvait pas voir : **les files de points étaient converties en filets `\rule` jusque dans les
blocs de code**. En verbatim, `\rule` n'est pas interprété — il s'imprime. Trente blocs
étaient concernés, dont les fiches Python à trous distribuées aux élèves, qui sortaient avec
`u = \rule{15mm}{0.32pt}` à la place du trou. La substitution connaît désormais les blocs de
code, et cinq tests la tiennent.

Le même balayage a montré que les documents de cadrage annonçaient encore **trois parcours**
quand les fiches élèves en portent six : les guides du formateur, les documentations de
module et les trois documents sources sont alignés. La distinction entre les **cinq cartes
d'aide collectives** et les **trois indices gradués du cahier nominatif** est écrite là où
elle manquait.

**Index des modules.** Le générateur branchait sur la clé du module au lieu d'employer les
champs prévus pour ces différences — `diagnostic_prefix`, `portfolio_dir`,
`extra_portfolio`. La physique-chimie héritait donc de la forme de NSI : son index
proposait un mini-diagnostic « pratique », un mémento Python et un portfolio dans
`04_PORTFOLIO`, soit **quatre documents qui n'existent pas**. Le mémento de formules, lui,
n'était lié depuis aucun index — alors que c'est le seul document du corpus destiné à
servir après le stage. Les trois index mènent en outre désormais au guide d'impression et
à la note de remise. Six tests refusent un lien mort, un mémento non lié, ou un index qui
ne mènerait pas à la remise.

**Dossier de remise.** `tools/build_dossier_livraison.py` produit `NOTE_DE_REMISE.md` à partir
du registre de la cohorte : qui reçoit quoi, en combien de pages, ce qui se photocopie et en
combien d'exemplaires, ce qui ne sort pas du dossier pédagogique. Le même outil échoue si un
document nominatif se trouve dans la liasse collective, si un document attendu manque, ou si
un fichier est attribué à quelqu'un qui n'est pas au registre. Il tourne sans distribution
TeX, et donc en intégration continue.

Le guide d'impression annonçait encore WeasyPrint, une cohorte de huit élèves et l'absence de
stage de physique-chimie. Les trois sont faux depuis plusieurs versions.

## 2026.9 — 2026-08-22

Balayage visuel des 327 pages des quinze cahiers nominatifs, en trente planches contact.
Cinq défauts que ni les tests, ni la compilation, ni le contrôle de densité ne voyaient.

- **Les exercices de la piste excellence figuraient dans le cahier de tous les élèves en
  séance 5.** Cette séance n'est pas découpée en pistes : son contenu est repris par thème,
  et le filtre laissait passer « Partie 3 bis — Exercices 9 et 10, piste Excellence ». Un
  élève en remédiation recevait donc un problème de type bac au milieu de sa séance. Au
  passage, l'évaluation finale et la carte de sortie, qui doublonnaient avec la question de
  sortie du cahier, sont également retirées de cette reprise.
- **Le décalage du point d'entrée suivait le mauvais domaine.** Il était calculé sur la
  réussite du domaine travaillé en temps différencié, puis appliqué aux exercices du thème
  de la séance. Adam Zahouani, à 0 % sur l'exponentielle, sautait une application directe
  d'exponentielle parce qu'il avait 43 % sur les suites. Le décalage suit désormais le
  domaine des exercices.
- **Le décalage s'appliquait à la piste Confronter.** Un élève porteur d'une certitude
  erronée a besoin de la reconstruction complète : son taux de réussite ne dit pas qu'il
  maîtrise l'accès, il dit qu'une partie de ce qu'il croit savoir est juste. Le décalage ne
  vaut plus que pour la piste Installer.
- **Le cahier d'un élève sans positionnement parlait d'un positionnement qui n'a pas eu
  lieu**, et répétait cinq fois la même phrase d'attente. Il porte désormais l'énoncé de sa
  situation, une fois, et un objectif qui nomme le thème de chaque séance sans rien préjuger
  de son niveau.
- **Le tableau de suivi final débordait seul sur une dernière page presque vide** dans trois
  cahiers sur quinze. Placé avant les questions ouvertes du bilan, c'est désormais une ligne
  de réponse qui déborde le cas échéant — et une ligne de réponse sur une page neuve n'est
  pas un défaut.

Ajout de `tools/qa_planches.py`, qui assemble toutes les pages d'un PDF en planches de douze
pour l'inspection. Le contrôle de densité trouve les pages vides ; il ne voit ni un tableau
qui déborde, ni un exercice donné au mauvais élève.

## 2026.8 — 2026-08-22

- Ajout des **cahiers de séances nominatifs** : un cahier par élève et par matière, couvrant
  les cinq séances. Les fiches collectives restaient la seule chose que l'élève avait sous
  les yeux pendant la séance ; il y trouvait les huit exercices du groupe, dont la moitié ne
  le concernait pas, et devait ouvrir son livret pour savoir lesquels étaient les siens. Le
  cahier assemble, pour lui seul, la progression commune et ce que son bilan dit de lui :
  objectif personnel, rappel de son diagnostic, automatismes, définitions et propriétés,
  méthode pas à pas, exemple résolu quand sa posture le demande, uniquement les exercices de
  sa piste, ses exercices issus de ses propres erreurs, indices gradués, transfert,
  passerelle Terminale, prise de recul, question de sortie et travail inter-séances.
  Quinze cahiers, de 17 à 25 pages.
- L'étayage dépend désormais de la posture diagnostique et non d'un niveau supposé. Un élève
  porteur d'une certitude erronée produit sa réponse avant toute correction ; un élève lucide
  sur ce qui lui manque reçoit l'exemple résolu tout de suite ; un élève qui réussit sans
  assurance s'en passe, c'est précisément l'objet du travail. Sans cette distinction, quatre
  élèves de mathématiques recevaient quatre cahiers identiques à leur exercice personnel près.
- Le point d'entrée dans une série d'exercices suit le taux de réussite du domaine : à plus
  de 70 %, les deux premières applications directes sont passées, et le cahier dit pourquoi.
  Aucun objectif n'est retiré — les exercices sautés restent dans la fiche collective.
- Reprise espacée : le domaine travaillé en séance n revient en séance n+2, sous forme d'une
  question de rappel sans notes. Une réussite le jour même ne prouve pas qu'une notion est
  installée.
- Correction d'un défaut d'interprétation du bilan : un domaine laissé **sans réponse**
  affichait « 0 % de réussite ». Ce zéro ne mesure rien, et l'écrire annonçait un échec là où
  le positionnement n'avait produit aucune information.
- Ajout de `CURRICULUM_SOURCES.md`. Le nouveau programme de spécialité mathématiques publié
  au BO du 2 avril 2026 n'entre en vigueur qu'à la rentrée 2027-2028 : il ne s'applique pas à
  cette cohorte, qui relève du programme de 2019 en Première comme en Terminale. Une erreur
  de génération de programme est indétectable dans un document fini ; la référence est donc
  écrite, avec ses adresses et ses dates.
- Charte enrichie : logo Nexus Réussite en page de garde et en tête de page, et huit encadrés
  nommés — définition, propriété, méthode, automatisme, remarque, piège, exemple, rappel de
  Première — reconnus depuis le Markdown à leur étiquette en gras.
- Correction d'un échec de compilation : `\degree` n'est pas défini par siunitx v3. La macro
  avait été introduite au commit précédent et n'avait jamais été compilée.
- Pages presque vides ramenées de 17 à 5 : un sommaire de moins de six pièces ne prend plus
  sa propre feuille, et les pénalités de veuves, d'orphelines et de coupure de liste
  empêchent une ou deux lignes de partir seules. Les cinq restantes sont deux pages de
  signature — faites pour être écrites — et trois queues de documents enseignant.
- Ajout de quatre outils de contrôle : `qa_pdf.py` (pages presque vides), `qa_science.py`
  (80 vérifications numériques des corrigés), `qa_code.py` (validité du code Python, en
  distinguant les squelettes à compléter et les exercices de débogage) et
  `qa_personnalisation.py` (deux bilans différents doivent produire deux cahiers différents).

## 2026.7 — 2026-08-22

- Élargissement de l'espace d'écriture des exercices qui demandent une rédaction, dans les
  quinze fiches élève des trois modules. Deux lignes suffisent pour une conversion en
  binaire ou le calcul d'un terme de rang 12 ; elles ne suffisent pas pour une démonstration,
  une étude de fonction ou un bilan des forces. Les exercices à réponse courte gardent leur
  espace : l'élargir n'aurait fait que gonfler la fiche. Les blocs de code sont traités à
  part, en agrandissant la plage vide où l'élève écrit plutôt qu'en y insérant des lignes
  de points.
- Ajout de la **piste excellence** aux cinq séances de mathématiques : un problème de type
  bac (exercice 9) et une question ouverte (exercice 10) par séance, avec leur corrigé dans
  la fiche professeur. Deux élèves du groupe ont un positionnement sans aucune erreur : le
  parcours d'approfondissement s'arrêtait à l'exercice 8, ils atteignaient donc la fin de la
  fiche avant la fin de la phase différenciée. Les questions ouvertes portent toutes sur un
  énoncé faux à réfuter, une réciproque à examiner ou un contre-exemple à produire — ce que
  le positionnement ne mesure pas.
- Ajout de l'**ouverture maths expertes** aux cinq fiches de séance, avec son corrigé :
  division euclidienne, diviseurs et nombres premiers, algorithme d'Euclide, logique,
  systèmes et ouverture sur les matrices et les complexes. Le livret individuel annonçait
  ces vingt minutes par séance et en donnait le programme, mais aucune fiche ne portait le
  contenu correspondant : la promesse était invérifiable. Chaque encadré part du thème de
  la séance, pour que l'option prolonge le travail commun au lieu de le doubler.
- Remplacement des trois parcours par un **aiguillage à six pistes**, dans les fiches élève,
  les fiches professeur et le guide du formateur. Trois parcours pour cinq postures
  diagnostiques : un élève ayant laissé un domaine sans réponse recevait le même traitement
  qu'un élève porteur d'une certitude erronée, alors que le premier a besoin qu'on établisse
  ce qu'il sait et le second qu'on mette sa conviction en défaut. Le livret et la fiche
  nomment désormais la même piste de la même façon.
- Remplacement de la phrase d'attente « Réinvestir ce qui a été repris, automatiser, mesurer
  le chemin parcouru. Le contenu précis est ajusté avec le groupe. » par un objectif propre
  à chaque thème de séance et à chaque module. Elle remplissait les cinq séances des élèves
  sans domaine à reprendre, c'est-à-dire précisément les livrets qui avaient le plus besoin
  d'un contenu.
- La piste excellence est attribuée aux séances sans focus personnel des élèves dont le
  bilan ne comporte aucune erreur à reprendre. Un acquis hésitant ne compte pas comme une
  erreur : il se travaille par répétition, pas par remédiation.
- Extension de l'aiguillage à NSI et à la physique-chimie. Le générateur de livrets est
  commun aux trois modules : renommer les parcours d'après les postures du diagnostic les a
  renommés partout, et un élève de NSI lisait « Consolider » dans son livret sans trouver la
  ligne correspondante sur sa fiche. Les deux modules reçoivent le même tableau, sans la
  piste excellence : aucun élève de ces groupes n'a un bilan sans erreur à reprendre, et les
  exercices 9 et 10 n'existent que dans les fiches de mathématiques.
- Les titres de section des fiches élève nomment la piste plutôt que l'ancien parcours :
  « Exercices 3 à 6 — piste Consolider » au lieu de « Parcours maîtrise (exercices 3 à 6) ».

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
