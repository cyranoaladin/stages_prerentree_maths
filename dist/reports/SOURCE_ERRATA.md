# Journal des écarts et corrections — sources et documents opérationnels

Ce journal consigne, conformément à la procédure de gestion des écarts, toute erreur mathématique,
contradiction, coquille ou impossibilité d'impression prouvée, ainsi que la correction retenue.
Aucune source canonique (`05_SOURCES/`) n'a été modifiée par les corrections listées ici : toutes
portent sur des documents opérationnels dérivés (`02_SEANCES/`), sans changement de la progression,
de l'ordre des séances ni des priorités par élève.

---

## ERR-001 — 3e Séance 4 : banque d'exercices dupliquée de la Séance 3 (Pythagore/Thalès au lieu de trigonométrie)

- **Fichiers concernés** : `3e/02_SEANCES/S4/3e_S4_PROF_Fiche.md`, `3e/02_SEANCES/S4/3e_S4_ELEVE_Activite.md`.
- **Section** : « Banque d'exercices et corrigé » (fiche professeur) et section correspondante de la fiche élève.
- **Problème** : la Séance 4 de 3e a pour objet les rapports trigonométriques (cosinus, sinus, tangente —
  objectifs, déroulé horaire, activité de construction, trace écrite et « erreurs à surveiller » de la fiche
  sont bien consacrés à la trigonométrie), mais sa banque d'exercices et son corrigé étaient un copier-coller
  strictement identique à ceux de la Séance 3 (théorème de Pythagore et Thalès), y compris le titre
  « Série 3 — Pythagore, Thalès et trigonométrie ». Aucun exercice de la Séance 4 ne faisait donc travailler
  la notion réellement enseignée ce jour-là.
- **Preuve** : `diff 3e/02_SEANCES/S3/3e_S3_PROF_Fiche.md 3e/02_SEANCES/S4/3e_S4_PROF_Fiche.md` montre une
  identité byte à byte à partir du titre « ## Banque d'exercices et corrigé » jusqu'à la fin de la section
  « Corrigé rapide à garder sous la main » dans les deux fichiers ; la fiche élève S4 portait le même intitulé
  « Série 3 — Pythagore, Thalès et trigonométrie » et les mêmes énoncés que la Séance 3, en contradiction avec
  ses propres objectifs affichés (« utiliser le cosinus », « distinguer cosinus, sinus et tangente »).
- **Correction retenue** : remplacement de la banque d'exercices par une nouvelle série
  « Série 4 — Rapports trigonométriques dans le triangle rectangle » (4 exercices de consolidation, 3 de
  maîtrise, 2 d'approfondissement), cohérente avec les objectifs, le vocabulaire (adjacent/opposé/hypoténuse,
  cosθ = adjacent/hypoténuse) et les erreurs à surveiller déjà présents dans la fiche. Chaque résultat a été
  recalculé indépendamment (script Python, fonctions trigonométriques en degrés) avant intégration :
  cos60°×8=4 cm ; 10×cos30°≈8,7 cm ; arccos(0,5)=60° ; 5/cos45°≈7,1 cm ; 1,2/cos70°≈3,5 m ;
  triangle 6-8-10 → sinθ=0,8, tanθ=4/3≈1,33, cos²θ+sin²θ=0,36+0,64=1 ; 4×tan50°≈4,8 m. La fiche élève a été
  mise à jour à l'identique (énoncés seuls, sans corrigé) pour rester strictement synchronisée avec la fiche
  professeur.
- **Portée** : ne modifie ni la progression, ni l'ordre des séances, ni les parcours nominatifs des élèves de
  3e ; la source canonique `3e/05_SOURCES/stage_prerentree_troisieme_maths.md` n'a pas été touchée.

---

## ERR-002 — 4e Séance 4 : corrigé mal numéroté (décalage exercice 7/8)

- **Fichier concerné** : `4e/02_SEANCES/S4/4e_S4_PROF_Fiche.md`.
- **Section** : « Banque d'exercices et corrigé » et « Corrigé rapide à garder sous la main ».
- **Problème** : la série comportait 8 exercices, mais seules 7 corrections numérotées étaient fournies.
  L'exercice 7 (« Rédiger la justification : données ; propriété ; conclusion », une tâche méthodologique
  sans réponse chiffrée unique) n'avait pas de corrigé associé, et l'élément numéroté « 7. »
  (« 9+16=25 ; le triangle semble rectangle ») était en réalité la réponse à l'exercice 8 (triangle 3-4-5),
  mal étiqueté. Un professeur consultant rapidement le corrigé pouvait donc associer par erreur la réponse
  du triangle 3-4-5 à l'exercice de rédaction.
- **Preuve** : comptage direct des énoncés (8) contre les entrées du corrigé (7) ; le contenu de l'entrée « 7 »
  correspond mathématiquement à l'énoncé 8 (3²+4²=9+16=25=5²) et non à l'énoncé 7.
- **Correction retenue** : ajout d'une entrée de corrigé explicite pour l'exercice 7 précisant qu'il s'agit
  d'une tâche de rédaction évaluée sur la présence des trois parties (données, propriété, conclusion) et non
  d'un résultat chiffré, et renumérotation de l'ancienne entrée « 7 » en entrée « 8 » (réponse du triangle
  3-4-5), dans les deux occurrences du corrigé (banque complète et corrigé rapide).
- **Portée** : correction purement rédactionnelle, aucun changement de contenu mathématique, de progression
  ni de priorités par élève.

---

## ERR-003 — 4e Évaluation finale : deux exercices sans énoncé chiffré ni corrigé (items 15 et 16)

- **Fichiers concernés** : `4e/03_EVALUATIONS/4e_Evaluation_Finale_ELEVE.md`,
  `4e/03_EVALUATIONS/4e_Evaluation_Finale_PROF_Corrige_Bareme.md`.
- **Problème** : les items 15 (« Problème de proportionnalité ») et 16 (« Problème intégré aire + expression
  littérale ») n'étaient que des intitulés génériques sans aucune donnée chiffrée ni question précise, à
  l'identique dans la fiche élève et dans le corrigé professeur ; la section « Réponses attendues » du corrigé
  s'arrêtait d'ailleurs à l'item 14, sans réponse pour 15 et 16. Un élève ne pouvait donc pas répondre à ces
  deux questions, et le professeur n'avait aucun corrigé à donner.
- **Preuve** : lecture directe des deux fichiers — l'énoncé « Problème de proportionnalité » ne comporte ni
  contexte, ni valeurs, ni question ; la liste numérotée des réponses attendues comporte 14 entrées pour 16
  énoncés.
- **Correction retenue** : rédaction de deux énoncés complets et chiffrés, cohérents avec le niveau et le
  style des items voisins (proportionnalité directe pour l'item 15, mise en équation d'une aire pour l'item
  16), avec calcul vérifié indépendamment : (450\div6=75) g/personne puis (75\times8=600) g ; et
  (4(x+5)=44\Rightarrow x=6), longueur (=11) cm (vérification : (4\times11=44)). Les deux fichiers (élève et
  professeur) ont été mis à jour de façon synchronisée.
- **Portée** : ajoute un contenu chiffré manquant sans modifier la structure de l'évaluation (16 items,
  barème inchangé) ni la progression du niveau.

---

## ERR-004 — 3e Séance 1, Séance 3 et Séance 5 : exercices d'approfondissement sans corrigé

- **Fichiers concernés** : `3e/02_SEANCES/S1/3e_S1_PROF_Fiche.md`, `3e/02_SEANCES/S3/3e_S3_PROF_Fiche.md`,
  `3e/02_SEANCES/S5/3e_S5_PROF_Fiche.md`.
- **Problème** : dans chacune de ces trois fiches, le dernier exercice d'approfondissement (un exercice de
  justification ou de construction d'exemple) ne figurait pas dans la liste numérotée des corrections, alors
  que la consigne mission impose une correction professeur pour chaque exercice.
- **Preuve** : script de comptage comparant, pour les 20 fiches professeur et les 8 corrigés d'évaluation, la
  numérotation des énoncés à celle des corrections ; seuls ces trois fichiers présentaient un écart
  (exercice 11 et 12 pour S1, exercice 9 pour S3, exercice 9 pour S5, non couverts par le corrigé).
- **Correction retenue** : ajout d'un corrigé pour chacun.
  * S1-11 (justifier via la distributivité que le produit de deux négatifs est positif) : démonstration
    standard ((-a)\times0=(-a)\times(b+(-b))=(-a)\times b+(-a)\times(-b)), avec ((-a)\times0=0) et
    ((-a)\times b=-ab), d'où ((-a)\times(-b)=ab>0)).
  * S1-12 (contre-exemple à une règle fausse de multiplication de fractions) : exemple chiffré
    (\frac12\times\frac13=\frac16\neq\frac1{2+3}=\frac15).
  * S3-9 (rapports trigonométriques égaux pour des triangles semblables) : exemple triangle 3-4-5 / triangle
    6-8-10, justification par le facteur d'échelle commun à tous les côtés.
  * S5-9 (deux séries de même moyenne, étendues différentes) : exemple chiffré vérifié — série (4;5;6)
    (moyenne 5, étendue 2) contre série (1;5;9) (moyenne 5, étendue 8).
- **Portée** : complète des corrigés manquants sans modifier les énoncés existants, la progression ou les
  parcours par élève.

---

## ERR-005 — 1re spécialité : formules à plusieurs lignes corrompues en faux titres Markdown (6 formules, 28 occurrences)

- **Fichiers concernés** : `1ere_spe/05_SOURCES/stage_prerentree_premiere_maths.md` (source canonique, 6
  occurrences), `1ere_spe/00_MASTER/1ere_spe_MASTER_Documentation_Stage.md` (11 occurrences),
  `1ere_spe/02_SEANCES/S2/1ere_spe_S2_PROF_Fiche.md` (2), `1ere_spe/02_SEANCES/S3/1ere_spe_S3_PROF_Fiche.md`
  (3), `1ere_spe/02_SEANCES/S3/1ere_spe_S3_ELEVE_Activite.md` (1),
  `1ere_spe/02_SEANCES/S4/1ere_spe_S4_PROF_Fiche.md` (3), `1ere_spe/02_SEANCES/S4/1ere_spe_S4_ELEVE_Activite.md`
  (1), `1ere_spe/03_EVALUATIONS/1ere_spe_Evaluation_Finale_PROF_Corrige_Bareme.md` (1).
- **Problème** : six formules mathématiques à plusieurs lignes utilisaient un signe « = » isolé sur sa propre
  ligne comme séparateur entre l'expression de départ et le résultat (convention d'écriture manuscrite
  courante). En Markdown (CommonMark/GFM), une ligne composée uniquement de caractères « = » directement sous
  une ligne de texte est interprétée comme le soulignement d'un titre de niveau 1 (syntaxe *setext*). Un
  passage antérieur du contenu par un normaliseur/sérialiseur Markdown a donc converti ces signes « = »
  isolés en soulignements de titre étirés à la largeur du texte (`===================`), voire en titres ATX
  (`# ...`), faisant disparaître le signe « = » et, dans un cas, le membre de droite du calcul
  (`1ere_spe_S2_PROF_Fiche.md`, taux de variation de (g(x)=x^2)). Le même défaut, avec les mêmes six
  formules, était déjà présent dans la source canonique elle-même.
- **Preuve** : `grep -rn "^====*$"` sur l'ensemble du paquet ne renvoyait des occurrences que dans ces huit
  fichiers de 1re spécialité (aucune autre section, aucun autre niveau) ; le nombre de caractères « = » de
  chaque occurrence correspond exactement à la longueur de la ligne de texte précédente, confirmant la
  conversion setext→soulignement étiré.
- **Correction retenue** : chaque formule a été réécrite sur une seule ligne avec un signe « = » explicite,
  y compris pour le taux de variation qui avait perdu son résultat :
  (\frac{(1+h)^2-1}{h}=\frac{2h+h^2}{h}=2+h) ;
  (\overrightarrow{AB}=\begin{pmatrix}x_B-x_A\\y_B-y_A\end{pmatrix}) ;
  (\vec u\cdot\vec v=2\times1+(-1)\times2=0) ;
  (P(A\cup B)=P(A)+P(B)-P(A\cap B)) ;
  (0{,}60\times0{,}40+0{,}40\times0{,}10=0{,}28) ;
  (\frac{(2+h)^2-4}{h}=4+h).
  Un script de substitution a appliqué ces six réécritures aux 28 occurrences des huit fichiers concernés
  (source canonique comprise, conformément à la procédure de gestion des écarts : la source canonique n'a été
  touchée que pour retirer une corruption de mise en forme prouvée, sans aucun changement de contenu, de
  progression ou d'ordre des séances). Une vérification `grep -rn "^====*$"` après correction ne renvoie plus
  aucune occurrence dans le paquet.
- **Portée** : correction de mise en forme et de contenu manquant, aucun changement pédagogique. Un défaut
  distinct et plus large — l'absence totale de rendu mathématique réel pour la convention `(...)`/`[...]`
  utilisée dans tout le corpus (Pandoc ne reconnaît pas ces délimiteurs et affiche le LaTeX brut aux élèves)
  — a été identifié pendant cet audit mais relève du pipeline de build (`tools/build.py`), pas du contenu
  mathématique ; il est signalé séparément à l'équipe responsable de la chaîne de production HTML/PDF et n'a
  pas été corrigé dans le cadre de cet audit de contenu.

---

## ERR-006 — Normalisation des délimiteurs mathématiques `(...)`/`[...]` vers `$...$`/`$$...$$` (pipeline)

- **Fichiers concernés** : 72 documents opérationnels sur les 4 niveaux (`00_MASTER`, `01_ENSEIGNANT`,
  `02_SEANCES/S1..S5`, `03_EVALUATIONS`) ainsi que les 4 sources canoniques `05_SOURCES/*.md`, qui utilisaient
  toutes la même convention d'écriture manuscrite `(...)` / `[...]` pour délimiter des expressions
  mathématiques, non reconnue par Pandoc (voir ERR-005 et `reports/CONTENT_GAPS.md` §1).
- **Problème** : Pandoc (`--from=gfm --to=html5 --mathml`) ne reconnaît que `$...$` (math en ligne) et
  `$$...$$` (math hors ligne) ; laissé tel quel, le code LaTeX (`\frac`, `\times`, `\overrightarrow`, etc.)
  s'affichait en clair dans le HTML et le PDF, y compris côté élève — défaut bloquant au sens de la section
  6.4 du mandat.
- **Correction retenue** : script de normalisation ponctuel (conservé sous
  `tools/normalize_math_delimiters.py` pour traçabilité et réutilisation si de nouveaux contenus reproduisent
  le même défaut), exécuté une fois sur les 72 fichiers concernés et dont le résultat a été écrit directement
  dans les fichiers `.md` (source unique conservée lisible et correcte, sans étape de préprocessing cachée
  dans la chaîne de build). Le script convertit
  uniquement les passages contenant un signal LaTeX univoque (commande `\xxx`, exposant `^`, indice `_`, macro
  décimale française `{,}`) — jamais une parenthèse de prose ordinaire (« (voir plus loin) », « (15 minutes) »
  restent inchangées). Trois cas traités : bloc `[`/`]` multi-lignes → `$$...$$` ; parenthèse `(...)` avec
  signal LaTeX → `$...$` (parenthèses imbriquées préservées à l'intérieur) ; ligne « nue » (blockquote ou
  élément de liste) entièrement formule avec signal LaTeX et sans mot de prose résiduel → `$...$`.
  **Validation** : rendu Pandoc de chacun des 72 fichiers concernés puis recherche de tout `\commande` visible
  hors de la balise `<annotation>` (métadonnée MathML normale, non affichée) — 0 fuite résiduelle sur les 72
  fichiers. Deux blocs `[`/`]` non refermés ont été détectés à cette occasion dans
  `1ere_spe/00_MASTER/1ere_spe_MASTER_Documentation_Stage.md` (lignes 1469 et 1509) et
  `1ere_spe/02_SEANCES/S2/1ere_spe_S2_PROF_Fiche.md` (lignes 180 et 220) — la formule de taux de variation
  réécrite par ERR-005 avait perdu son crochet fermant lors de la réécriture sur une seule ligne. Corrigé en
  réinsérant le `]` manquant après chacune des 4 occurrences ; contrôle de correspondance ouverture/fermeture
  rejoué sur l'ensemble du paquet après correction : 0 anomalie restante.
- **Portée** : correction de rendu, aucun changement de valeur numérique, de progression ni d'ordre des
  séances. Les 4 sources canoniques ont été normalisées de la même façon (même défaut de délimiteur présent
  nativement dans les 4 fichiers), conformément à la procédure de gestion des écarts : correction nécessaire
  au maintien d'une source unique cohérente, sans changement de contenu pédagogique.

---

## ERR-007 — Compléments à ERR-006 : fichiers omis par la sélection initiale, et fuite MathML propre au PDF

Deux défauts supplémentaires ont été découverts lors de l'**inspection visuelle réelle** des PDF générés
(`reports/PDF_VISUAL_QA.md`), après application d'ERR-006 :

- **6 fichiers omis par la sélection initiale d'ERR-006** : la liste des 72 fichiers à corriger avait été
  constituée par recherche de noms de commandes précis (`\frac`, `\times`, `\overrightarrow`, etc.) ; elle
  ne couvrait pas `\circ` (degré) ni `\cup` (union), présents isolément dans
  `4e/01_ENSEIGNANT/4e_Guide_Formateur.md`, `4e/02_SEANCES/S1/4e_S1_SUPPORTS_Manipulation.md`,
  `4e/02_SEANCES/S4/4e_S4_ELEVE_Activite.md`, `4e/02_SEANCES/S4/4e_S4_PROF_Fiche.md`,
  `4e/02_SEANCES/S4/4e_S4_SUPPORTS_Manipulation.md` et
  `1ere_spe/04_NOMINATIFS/Donia_Khadhrani/1ere_spe_Dossier_Individuel_Donia_Khadhrani.md` (dossier nominatif
  confidentiel). **Preuve** : recherche exhaustive, sur les 142 fichiers opérationnels des 4 niveaux, de tout
  `\commande` situé hors d'une paire `$...$`/`$$...$$`, plutôt que sur une liste de noms de commandes
  présupposée — 6 fichiers restants trouvés, tous corrigés avec le même script
  `tools/normalize_math_delimiters.py`. Un second passage confirme 0 fichier restant sur l'ensemble des 142.
- **Fuite MathML propre à WeasyPrint, absente du rendu navigateur** : la vérification d'ERR-006 avait été
  faite sur le HTML brut de Pandoc (élément `<annotation encoding="application/x-tex">`, non affiché par
  défaut par un navigateur — confirmé par capture d'écran Chrome headless) et sur un rendu Chrome. Mais
  WeasyPrint 68.1 (moteur de production des PDF) n'applique pas la même règle par défaut : il affichait le
  contenu de `<annotation>` à la suite du symbole déjà rendu (ex. « −4° » suivi du texte brut
  « -4^\circC »), visible uniquement en inspectant réellement les PDF rasterisés, jamais dans le HTML. Cette
  fuite concernait potentiellement **toutes** les formules de tout le corpus dans les PDF (pas seulement les
  6 fichiers ci-dessus), puisqu'elle vient du moteur de rendu et non du contenu. **Correction** : règle CSS
  explicite `math annotation, math annotation-xml { display:none; }` ajoutée à `assets/print.css` (et, par
  précaution, à `assets/site.css`). Un nouveau build complet puis une nouvelle inspection visuelle
  confirment sa disparition (voir `reports/PDF_VISUAL_QA.md`).
- **Portée** : correction de rendu uniquement (fichiers de contenu et feuilles de style), aucun changement
  de valeur mathématique, de progression ni d'ordre des séances. Illustre pourquoi l'inspection visuelle
  réelle des PDF (section 10.4 du mandat) ne peut pas être remplacée par un contrôle du seul HTML source.

---

## ERR-008 — Corrigé enseignant présent dans le pack de travail élève nominatif (11 élèves)

- **Fichiers concernés** : les 11 fichiers `*_Remediation_Ciblee_{élève}.md` sous `04_NOMINATIFS/` (un par
  élève, 4 niveaux confondus).
- **Problème** : découvert par **inspection visuelle réelle** des PDF (`reports/PDF_VISUAL_QA.md`), pas par
  le contrôle automatisé initial. Chaque fichier de remédiation ciblée contenait, dans un seul document
  Markdown, à la fois les exercices destinés à l'élève et une section « Corrigé enseignant » avec les
  réponses et un « Relevé de maîtrise ». Comme ce type de document (`type: remediation`) n'est ni une fiche
  professeur (`PROF` dans le nom) ni un corrigé (`Corrige` dans le nom), `tools/build.py::is_teacher()` le
  classait comme document élève, et `student_pack_documents()` l'incluait donc dans
  `[niveau]_[Nom_Prenom]_PACK_TRAVAIL_PERSONNALISE.pdf` — **le pack remis à l'élève et à la famille contenait
  le corrigé de l'enseignant**, en violation directe de la section 3 (règle 7 : « pas de corrigé dans un
  document élève ») et de la section 9.3 (« le pack élève ne doit jamais contenir les corrigés
  professeur »). Le contrôle QA automatisé initial ne l'avait pas détecté car il ne recherchait la mention
  « corrigé » que dans le bucket `eleves/` et les packs nommés `PACK_ELEVE*`, pas dans
  `PACK_TRAVAIL_PERSONNALISE` (corrigé depuis dans `tmp/pdf_qa/structural_qa.py`).
- **Preuve** : `pdftotext dist/packs/nominatifs-prives/4e_Fares_Darghouth_PACK_TRAVAIL_PERSONNALISE.pdf -`
  contenait littéralement la section « Corrigé enseignant » suivie des 8 réponses numérotées, avant
  correction.
- **Correction retenue** : chaque fichier a été scindé en deux, sur le modèle déjà utilisé pour les séances
  (`*_ELEVE.md` / `*_PROF_Corrige.md`) : `{niveau}_Remediation_Ciblee_{élève}_ELEVE.md` (consignes et
  exercices seuls, sans corrigé) et `{niveau}_Remediation_Ciblee_{élève}_PROF_Corrige.md` (contenu complet,
  exercices + corrigé + relevé de maîtrise, pour le dossier enseignant confidentiel). Le nom de fichier
  suffit à faire fonctionner la classification existante (`is_teacher()` détecte déjà `PROF`/`Corrige` dans
  le chemin) sans aucune modification de `tools/build.py`. Après reconstruction complète, `pdftotext` sur
  les 11 `PACK_TRAVAIL_PERSONNALISE` ne contient plus aucune section « Corrigé enseignant » ; les 11
  `DOSSIER_ENSEIGNANT_CONFIDENTIEL` contiennent bien les deux versions (élève et corrigé).
- **Portée** : correction structurelle (fichiers de contenu nominatifs, un par élève), aucun changement des
  exercices eux-mêmes, de leurs réponses ni de la personnalisation par élève — uniquement leur répartition
  entre les deux publics. Confirme, comme ERR-007, la nécessité de l'inspection visuelle réelle des PDF :
  aucun contrôle sur le seul contenu source Markdown n'aurait révélé qu'un document par ailleurs correct se
  retrouvait, une fois assemblé en pack, dans la mauvaise main.

---

## ERR-009 — WeasyPrint ne met pas en page les fractions, exposants, indices et racines MathML (défaut moteur, tout le corpus PDF)

- **Fichiers concernés** : aucun fichier de contenu — défaut du moteur de production PDF
  (`tools/build.py`), affectant potentiellement toutes les formules `\frac`, `^` (exposant), `_` (indice) et
  `\sqrt`/`\root` de tout le paquet, dans les quatre niveaux.
- **Problème** : découvert par **inspection visuelle réelle** d'un PDF généré (`2nde_S1_ELEVE_Activite.pdf`),
  pas par un contrôle automatisé. Pandoc convertit correctement `\frac34\div\frac25` en MathML structuré
  (`<mfrac><mn>3</mn><mn>4</mn></mfrac>...`, vérifié directement) — mais **WeasyPrint 68.1 ne met pas en page
  les éléments structurels `<mfrac>`, `<msup>`, `<msub>`, `<msqrt>` de MathML** : il aplatit leur contenu en
  texte concaténé sans aucune mise en forme. Concrètement, `3/4 ÷ 2/5` s'affichait « 34÷25 » (les numérateurs
  et dénominateurs collés, sans barre de fraction, lisible comme le nombre 34), `2^3` s'affichait « 23 » sans
  exposant, `x_n` s'affichait « xn » sans indice. C'est un défaut bloquant et potentiellement le plus grave
  du paquet : une fraction affichée comme un nombre entier est mathématiquement trompeuse, pas seulement
  inélégante.
- **Preuve** : test isolé — rendu direct d'un fragment MathML minimal
  (`<math><mfrac><mn>3</mn><mn>4</mn></mfrac></math>`) par WeasyPrint : sortie « 34 », confirmé à la fois par
  extraction de texte (`pdftotext`) et par inspection visuelle du PDF rasterisé à 200 dpi. Testé de la même
  façon pour `<msup>`, `<msub>`, `<msqrt>` : même défaut systématique.
- **Correction retenue** : décision d'architecture au sens de la section 6.3 du mandat (« fais un essai
  comparatif, choisis le moteur qui rend correctement les mathématiques, documente ce choix »). Plutôt que de
  changer entièrement de moteur PDF (risque élevé si tard dans la production) ou d'ajouter une dépendance
  réseau (KaTeX local aurait nécessité `npm install`, donc un accès réseau interdit par la règle « travail
  local uniquement »), un post-traitement a été ajouté dans `tools/build.py`
  (`_render_mathml_node`/`render_math_for_print`) : après conversion Pandoc, chaque élément `<math>` est
  reparcouru et converti en HTML/CSS pur — `<msup>`/`<msub>` en `<sup>`/`<sub>` natifs (correctement mis en
  page par WeasyPrint), `<mfrac>` en fraction empilée par CSS (`display:inline-block` avec numérateur/
  dénominateur en `display:block` et bordure — le premier essai avec `display:inline-flex` faisait aussi
  échouer WeasyPrint, qui casse chaque élément flexible sur sa propre ligne ; confirmé par test isolé avant
  application générale), `<msqrt>`/`<mroot>` avec le symbole racine et une bordure supérieure sur le
  radicande, `<mspace>` (généré par `\qquad`) en espace insécable. Aucune dépendance nouvelle, aucun accès
  réseau, rendu vérifié case par case par test isolé WeasyPrint avant application au pipeline complet.
- **Portée** : correction du pipeline de production uniquement, aucun changement de contenu mathématique.
  Application automatique à tous les documents lors du prochain `python3 tools/build.py all` — aucune
  modification de fichier `.md` requise pour ce défaut précis. Un second défaut lié, la présence de crochets
  `[ ]` littéraux autour de formules déjà correctement délimitées en `$...$` par ERR-006/ERR-007 (le bloc
  d'affichage indenté sous un élément de liste n'était pas reconnu par le script de normalisation, qui
  n'acceptait qu'un crochet seul en tout début de ligne), a été corrigé dans le même passage : 34 fichiers,
  environ 264 blocs, `tools/normalize_math_delimiters.py` mis à jour pour accepter l'indentation et fusionner
  proprement avec un contenu déjà délimité plutôt que d'imbriquer un second jeu de délimiteurs.
