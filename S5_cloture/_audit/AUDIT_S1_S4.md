# Audit du stage — du diagnostic initial à la séance 4

> Document de travail produit avant toute rédaction de livret, conformément au §2 du
> cahier des charges. Il consigne ce qui a été trouvé dans le dépôt, et uniquement cela.

**Date de l'audit :** 2026-08-20
**Périmètre :** 15 couples élève × matière, 5 niveaux, 2 matières.

---

## 1. Ce que contient réellement le dépôt

| Élément | Constat |
|---|---|
| Répertoires de stage | `4e`, `3e`, `2nde`, `1ere_spe` (mathématiques) et `1re_nsi` (NSI) |
| Structure par niveau | `00_MASTER`, `01_ENSEIGNANT`, `02_SEANCES/S1..S5`, `03_EVALUATIONS`, `04_NOMINATIFS` (ou `05_NOMINATIFS` en NSI), `05_SOURCES` |
| Diagnostic initial | un test de positionnement par niveau, 18 items QCM, 25 minutes, certitude 1 à 4 |
| Documents par séance | fiche élève, fiche professeur, cartes d'aide, supports de manipulation |
| Dossiers nominatifs | dossier individuel, plan de remédiation ciblée élève et professeur, bilans élève et parents |
| Format de production historique | Markdown → HTML → PDF (`tools/build.py`), avec `assets/print.css` |
| Format LaTeX le plus récent | `Bilans/1re_NSI_S4_Ahmad_BELDI_DOSSIER_ELEVE_PERSONNALISE.tex` |
| Données structurées existantes | `content/students.json`, `content/catalog.json`, `reports/AUDIT_INITIAL.json`, `reports/QA_STATUS.json` |

**Charte graphique retenue.** Aucune identité nouvelle n'a été créée. Le fichier
`S5_cloture/_common/nexusS5.sty` reprend, sans modification, les couleurs, les encadrés,
les titres et les réglages typographiques du seul fichier LaTeX du dépôt, qui est aussi
le plus récent.

---

## 2. Ce qui manque

1. **Aucune observation de séance n'a été saisie.** Les dossiers individuels prévoient,
   pour chacune des cinq séances, un tableau « procédure choisie / exactitude /
   justification / contrôle / certitude » ainsi qu'une colonne « preuve recueillie ».
   Ces tableaux sont vierges dans les quinze dossiers. Il n'existe donc **aucune preuve
   documentée postérieure au diagnostic initial**.
2. **Aucun dossier personnalisé S2 à S5 en Première spécialité.** Les quatre autres
   niveaux disposent de livrets élèves individualisés pour S2, S3 et S4 ; la Première
   spécialité n'en a aucun.
3. **Aucun corrigé nominatif renseigné.** Les plans de remédiation professeur existent,
   mais aucune production d'élève corrigée n'est archivée.
4. **Aucun résultat item par item du diagnostic initial.** Les dossiers restituent des
   statuts par domaine et des observations qualitatives, non les réponses aux 18 items.
   La comparaison initial/final sera donc conduite **au niveau de la compétence**, non
   au niveau de la réponse.

Ces quatre lacunes déterminent une règle appliquée partout dans `S5_cloture` : le statut
d'une compétence avant la séance 5 est qualifié à partir du diagnostic initial, jamais
à partir d'une acquisition supposée pendant les séances.

---

## 3. Trajectoire de niveau reconstruite


### Entrée en Quatrième — Mathématiques

Année N−1 : Cinquième. Année N : Quatrième.

| Séance | Thème réellement travaillé |
|---|---|
| S1 | Calculer avec du sens (relatifs, fractions) |
| S2 | Mesurer une surface ou un contour (aires et périmètres) |
| S3 | Donner du sens aux lettres (calcul littéral) |
| S4 | Voir, raisonner, démontrer (géométrie) |
| S5 | Réinvestir, mesurer les progrès et préparer septembre |

Prérequis critiques retenus pour l'entrée en Quatrième : M4E_REL_01, M4E_REL_02, M4E_FRAC_02, M4E_LIT_01, M4E_LIT_02, M4E_GEO_01, M4E_AIRE_01, M4E_PROP_01.

Ponts vers l'année N introduits en phase 4 de la S5 : produit et quotient de nombres relatifs ; résolution d'une équation du premier degré ax + b = c ; médiane d'une série et événement contraire.

### Entrée en Troisième — Mathématiques

Année N−1 : Quatrième. Année N : Troisième.

| Séance | Thème réellement travaillé |
|---|---|
| S1 | Sécuriser le moteur numérique (nombres, fractions, puissances) |
| S2 | Passer du calcul à l'algèbre (calcul littéral, équations) |
| S3 | Construire et justifier (Pythagore, Thalès) |
| S4 | Choisir un rapport trigonométrique |
| S5 | Lire les données et mobiliser l'ensemble des acquis |

Prérequis critiques retenus pour l'entrée en Troisième : M3E_REL_01, M3E_FRAC_02, M3E_LIT_01, M3E_LIT_02, M3E_EQ_01, M3E_PROP_01, M3E_GEO_01, M3E_TRIG_01.

Ponts vers l'année N introduits en phase 4 de la S5 : double distributivité (a+b)(c+d) et amorce des identités remarquables ; notion de fonction : image, antécédent, tableau de valeurs ; théorème de Thalès et agrandissement-réduction.

### Entrée en Seconde générale et technologique — Mathématiques

Année N−1 : Troisième. Année N : Seconde.

| Séance | Thème réellement travaillé |
|---|---|
| S1 | Réparer le moteur de calcul (priorités, fractions, puissances) |
| S2 | Construire l'algèbre du lycée (développement, factorisation, équations) |
| S3 | Modéliser une situation (pourcentages, fonctions) |
| S4 | Choisir le bon théorème (Pythagore, Thalès, trigonométrie) |
| S5 | Relier, contrôler et expliquer (statistiques, probabilités, algorithmique) |

Prérequis critiques retenus pour l'entrée en Seconde : M2DE_CALC_01, M2DE_FRAC_01, M2DE_PUIS_01, M2DE_ALG_01, M2DE_EQ_01, M2DE_EQ_02, M2DE_POURC_01, M2DE_GEO_01.

Ponts vers l'année N introduits en phase 4 de la S5 : intervalles de réels et ensembles de nombres ; notion de fonction : image, antécédent, tableau de valeurs, courbe ; repérage dans le plan et algorithmique en Python.

### Entrée en Première générale — Spécialité mathématiques — Mathématiques

Année N−1 : Seconde. Année N : Première spécialité.

| Séance | Thème réellement travaillé |
|---|---|
| S1 | Calcul algébrique, inéquations et transition vers le second degré |
| S2 | Fonctions, fonctions de référence et première approche de la dérivation |
| S3 | Vecteurs, droites et transition vers le produit scalaire |
| S4 | Pourcentages, événements et probabilités conditionnelles |
| S5 | Suites numériques, Python et évaluation de synthèse |

Prérequis critiques retenus pour l'entrée en Première spécialité : M1RE_ALG_01, M1RE_ALG_02, M1RE_INEQ_01, M1RE_INEQ_02, M1RE_FONC_01, M1RE_FONC_02, M1RE_VECT_01, M1RE_VECT_02, M1RE_DROIT_01, M1RE_POURC_01, M1RE_POURC_02.

Ponts vers l'année N introduits en phase 4 de la S5 : suite définie par récurrence à partir d'une évolution en pourcentage ; taux de variation moyen d'une fonction, préparation du nombre dérivé ; second degré : forme développée, forme factorisée, signe.

### Entrée en Première — Numérique et sciences informatiques — NSI

Année N−1 : Seconde (SNT et algorithmique). Année N : Première NSI.

| Séance | Thème réellement travaillé |
|---|---|
| S1 | Variables, affectation et conditions |
| S2 | Boucles, compteurs et accumulateurs |
| S3 | Fonctions, contrats et tests |
| S4 | Listes, enregistrements et données CSV |
| S5 | Algorithmes et mini-projet de synthèse |

Prérequis critiques retenus pour l'entrée en Première NSI : NSI1_AFF_01, NSI1_LOG_01, NSI1_BOUCLE_01, NSI1_BOUCLE_02, NSI1_ACC_01, NSI1_LIST_01, NSI1_FONC_01, NSI1_TEST_01, NSI1_CSV_01.

Ponts vers l'année N introduits en phase 4 de la S5 : recherche séquentielle : parcours complet, valeur sentinelle de retour ; recherche dichotomique : précondition de tri, division de l'espace de recherche ; spécifier une fonction avant de l'écrire, puis la tester.

---

## 4. Élèves détectés

| Élève | Niveau | Matière | Diagnostic | S1 | S2 | S3 | S4 | Priorité 1 | Priorité 2 |
|---|---|---|:--:|:--:|:--:|:--:|:--:|---|---|
| Fares DARGHOUTH | 4e | Mathématiques | oui | niveau | perso. | perso. | perso. | M4E_AIRE_01 | M4E_GEO_02 |
| Ines KEFI | 4e | Mathématiques | oui | niveau | perso. | perso. | perso. | M4E_REL_02 | M4E_FRAC_02 |
| Sinda CHIKHAOUI | 4e | Mathématiques | oui | niveau | perso. | perso. | perso. | M4E_REL_01 | M4E_LIT_02 |
| Amine MANSOURI | 3e | Mathématiques | oui | niveau | perso. | perso. | perso. | M3E_LIT_02 | M3E_TRIG_01 |
| Elyes KEFI | 3e | Mathématiques | oui | niveau | perso. | perso. | perso. | M3E_FRAC_02 | M3E_LIT_02 |
| Fares LAAJILI | 3e | Mathématiques | oui | niveau | perso. | perso. | perso. | M3E_FRAC_02 | M3E_TRIG_01 |
| Sarah BARGAOUI | 3e | Mathématiques | oui | niveau | perso. | perso. | perso. | M3E_LIT_02 | M3E_EQ_01 |
| Selim MANSOURI | 3e | Mathématiques | oui | niveau | perso. | perso. | perso. | M3E_REL_01 | M3E_LIT_01 |
| Ahmed BAKIR | 2nde | Mathématiques | oui | niveau | perso. | perso. | perso. | M2DE_CALC_01 | M2DE_ALG_01 |
| Noa MANIACI | 2nde | Mathématiques | oui | niveau | perso. | perso. | perso. | M2DE_EQ_02 | M2DE_POURC_01 |
| Ahmad BELDI | 1ere_spe | Mathématiques | oui | niveau | niveau | niveau | niveau | M1RE_ALG_02 | M1RE_FONC_02 |
| Donia KHADHRANI | 1ere_spe | Mathématiques | oui | niveau | niveau | niveau | niveau | M1RE_FONC_02 | M1RE_INEQ_01 |
| Malek KHADHRANI | 1ere_spe | Mathématiques | oui | niveau | niveau | niveau | niveau | M1RE_FONC_01 | M1RE_VECT_02 |
| Ahmad BELDI | 1re_nsi | NSI | oui | niveau | perso. | perso. | perso. | NSI1_FONC_01 | NSI1_BOUCLE_01 |
| Ahmed BENHADJ SALEM | 1re_nsi | NSI | oui | niveau | perso. | perso. | perso. | NSI1_ACC_01 | NSI1_TEST_01 |

*« niveau »* : seuls les documents communs du niveau sont attestés pour cette séance.
*« perso. »* : un livret personnalisé de cette séance existe pour cet élève.

---

## 5. Lecture élève par élève


### Fares DARGHOUTH — Entrée en Quatrième (Mathématiques)

**Diagnostic initial.** Diagnostic initial (18 items) — Points d'appui en proportionnalité et statistiques ; géométrie, aires/périmètres et fractions à rectifier ; calcul littéral à diagnostiquer.

**Points d'appui documentés.** Proportionnalité ; Statistiques ; Nombres relatifs presque acquis

**Difficultés documentées.** Fractions équivalentes. Aire versus périmètre. Angles du triangle. Symétrie centrale. Calcul littéral à situer.

*Le dossier individuel de cet élève ne comporte pas de tableau détaillé par domaine : seuls la synthèse, les points d'appui et les priorités sont documentés.*

**Axes retenus pour la séance 5.** Priorité 1 : `M4E_AIRE_01`. Priorité 2 : `M4E_GEO_02`.

**Objectif de la séance.** Séparer nettement aire et périmètre, avec l'unité comme premier contrôle, puis rédiger un raisonnement géométrique complet sans hypothèse ajoutée.

**Compétences non évaluées ou non travaillées à ce jour.** `M4E_FRAC_01`, `M4E_LIT_01`, `M4E_LIT_02`

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Ines KEFI — Entrée en Quatrième (Mathématiques)

**Diagnostic initial.** 18 questions traitées sur 18 — Trois domaines solides, un domaine à installer et trois domaines à rectifier en priorité. Calibration réussite-confiance : 67 %.

**Points d'appui documentés.** Proportionnalité ; Aires et périmètres ; Statistiques

**Difficultés documentées.** Fractions : conversion complète vers un dénominateur commun. Nombres relatifs : ordre croissant et déplacements sur une droite graduée. Géométrie : somme des angles et caractérisation d'un parallélogramme par un centre de symétrie. Calcul littéral : réduction des constantes en tenant compte des signes.

| Domaine | Statut au diagnostic | Observation issue du bilan |
|---|---|---|
| Nombres relatifs | À rectifier | Deux réponses fausses données avec certitude 4 : ordre décroissant au lieu de croissant ; déplacement vers la gauche au lieu de la droite. |
| Fractions | À rectifier | Pour 5/6 − 1/3, le dénominateur est converti mais le numérateur de 1/3 ne l'est pas. |
| Proportionnalité | Solide | Deux réponses exactes et assurées. |
| Calcul littéral | À installer | Distributivité disponible ; erreur de signe sur 2 − 6 dans une réduction. |
| Géométrie | À rectifier | Hypothèse isocèle ajoutée sans justification ; centre de symétrie confondu avec la seule classe des carrés. |
| Aires et périmètres | Solide | Aire du rectangle et du triangle correctement calculées. |
| Statistiques | Solide | Moyenne et fréquence correctement calculées. |

**Axes retenus pour la séance 5.** Priorité 1 : `M4E_REL_02`. Priorité 2 : `M4E_FRAC_02`.

**Objectif de la séance.** Vérifier que les deux erreurs données avec une certitude maximale au diagnostic (ordre des relatifs, déplacement sur une droite graduée) ne réapparaissent plus, et que la transformation d'une fraction porte bien sur ses deux termes.

**Compétences non évaluées ou non travaillées à ce jour.** `M4E_FRAC_01`

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Sinda CHIKHAOUI — Entrée en Quatrième (Mathématiques)

**Diagnostic initial.** Diagnostic initial (18 items) — Trois domaines solides ; priorité aux relatifs, fractions, calcul littéral et aire du triangle.

**Points d'appui documentés.** Proportionnalité ; Géométrie ; Statistiques

**Difficultés documentées.** Soustraction d'un négatif. Fractions équivalentes. Distributivité. Réduction avec constantes négatives. Aire du triangle.

*Le dossier individuel de cet élève ne comporte pas de tableau détaillé par domaine : seuls la synthèse, les points d'appui et les priorités sont documentés.*

**Axes retenus pour la séance 5.** Priorité 1 : `M4E_REL_01`. Priorité 2 : `M4E_LIT_02`.

**Objectif de la séance.** Stabiliser la soustraction d'un nombre négatif et la réduction d'une expression comportant des constantes négatives, deux points nommés dans le plan de remédiation.

**Compétences non évaluées ou non travaillées à ce jour.** `M4E_FRAC_01`

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Amine MANSOURI — Entrée en Troisième (Mathématiques)

**Diagnostic initial.** Diagnostic initial (18 items) — Nombreuses réussites accompagnées d'une confiance très faible ; calcul littéral à installer ; fractions et trigonométrie à situer.

**Points d'appui documentés.** Relatifs ; Puissances ; Équations ; Proportionnalité ; Pythagore ; Statistiques — sous réserve d'explicitation

**Difficultés documentées.** Justifier les procédures. Réduire avec signes. Multiplier des fractions. Installer la trigonométrie. Calibrer la confiance.

*Le dossier individuel de cet élève ne comporte pas de tableau détaillé par domaine : seuls la synthèse, les points d'appui et les priorités sont documentés.*

**Axes retenus pour la séance 5.** Priorité 1 : `M3E_LIT_02`. Priorité 2 : `M3E_TRIG_01`.

**Objectif de la séance.** Rendre explicite la procédure utilisée — la réussite existe, la justification manque — et installer le choix d'un rapport trigonométrique.

**Compétences non évaluées ou non travaillées à ce jour.** `M3E_FRAC_01`, `M3E_FRAC_02`, `M3E_TRIG_01`

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Elyes KEFI — Entrée en Troisième (Mathématiques)

**Diagnostic initial.** 18 questions traitées sur 18 — Six domaines solides et trois domaines à rectifier en priorité. Calibration réussite-confiance : 82 %.

**Points d'appui documentés.** Nombres relatifs ; Puissances ; Équations ; Proportionnalité ; Géométrie ; Trigonométrie

**Difficultés documentées.** Fractions : multiplication des numérateurs et des dénominateurs dans le bon ordre. Calcul littéral : addition des constantes signées lors d'une réduction. Statistiques : prise en compte de toutes les valeurs avant la division.

| Domaine | Statut au diagnostic | Observation issue du bilan |
|---|---|---|
| Nombres relatifs | Solide | Produits, quotients et priorités correctement maîtrisés. |
| Fractions | À rectifier | Pour 2/3 × 9/4, croisement inversé donnant 8/27 au lieu de 3/2. |
| Puissances | Solide | Calcul et produit de puissances de même base réussis. |
| Calcul littéral | À rectifier | Distributivité correcte ; réduction erronée : −7 + 3 traité comme −10. |
| Équations | Solide | Deux équations du premier degré correctement résolues. |
| Proportionnalité | Solide | Prix unitaire et vitesse correctement mobilisés. |
| Géométrie | Solide | Pythagore utilisé correctement dans les deux configurations. |
| Trigonométrie | Solide | Cosinus et calcul d'angle correctement maîtrisés. |
| Statistiques | À rectifier | Une valeur oubliée dans la somme lors du calcul de la moyenne simple. |

**Axes retenus pour la séance 5.** Priorité 1 : `M3E_FRAC_02`. Priorité 2 : `M3E_LIT_02`.

**Objectif de la séance.** Séparer définitivement la procédure du produit de fractions de celle de la somme, et faire porter le signe sur la constante lors d'une réduction.

**Compétences non évaluées ou non travaillées à ce jour.** `M3E_FRAC_01`

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Fares LAAJILI — Entrée en Troisième (Mathématiques)

**Diagnostic initial.** Diagnostic initial (18 items) — Six domaines solides ; multiplication de fractions, Pythagore et cosinus à rectifier.

**Points d'appui documentés.** Relatifs ; Puissances ; Calcul littéral ; Équations ; Proportionnalité ; Statistiques

**Difficultés documentées.** Produit de fractions. Pythagore sur les carrés. Cosinus versus sinus.

*Le dossier individuel de cet élève ne comporte pas de tableau détaillé par domaine : seuls la synthèse, les points d'appui et les priorités sont documentés.*

**Axes retenus pour la séance 5.** Priorité 1 : `M3E_FRAC_02`. Priorité 2 : `M3E_TRIG_01`.

**Objectif de la séance.** Stabiliser le produit et le quotient de fractions, puis choisir le rapport trigonométrique à partir du nom des côtés et non d'une habitude.

**Compétences non évaluées ou non travaillées à ce jour.** `M3E_FRAC_01`

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Sarah BARGAOUI — Entrée en Troisième (Mathématiques)

**Diagnostic initial.** Diagnostic initial (18 items) — Socle numérique solide ; calcul littéral à rectifier ; équations, proportionnalité, géométrie, trigonométrie et statistiques à installer.

**Points d'appui documentés.** Nombres relatifs ; Fractions ; Puissances

**Difficultés documentées.** Réduction avec signes. Équations. Proportionnalité. Pythagore longueur manquante. Trigonométrie. Moyenne.

*Le dossier individuel de cet élève ne comporte pas de tableau détaillé par domaine : seuls la synthèse, les points d'appui et les priorités sont documentés.*

**Axes retenus pour la séance 5.** Priorité 1 : `M3E_LIT_02`. Priorité 2 : `M3E_EQ_01`.

**Objectif de la séance.** Écrire la relation avant d'insérer les nombres — conseil explicite du dossier — en commençant par la réduction signée puis par la résolution d'équations vérifiées.

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Selim MANSOURI — Entrée en Troisième (Mathématiques)

**Diagnostic initial.** Diagnostic initial (18 items) — Puissances solides ; signes, distributivité, proportionnalité et Pythagore à rectifier ; fractions, équations et trigonométrie à diagnostiquer.

**Points d'appui documentés.** Puissances

**Difficultés documentées.** Signe d'un produit. Distributivité. Retour à l'unité. Pythagore. Fractions. Équations. Trigonométrie.

*Le dossier individuel de cet élève ne comporte pas de tableau détaillé par domaine : seuls la synthèse, les points d'appui et les priorités sont documentés.*

**Axes retenus pour la séance 5.** Priorité 1 : `M3E_REL_01`. Priorité 2 : `M3E_LIT_01`.

**Objectif de la séance.** Choisir l'opération à partir de la relation et non des nombres présents — conseil du dossier — en sécurisant d'abord le signe d'un produit puis la distributivité complète.

**Compétences non évaluées ou non travaillées à ce jour.** `M3E_EQ_01`, `M3E_FRAC_01`, `M3E_FRAC_02`, `M3E_STAT_01`, `M3E_TRIG_01`

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Ahmed BAKIR — Entrée en Seconde générale et technologique (Mathématiques)

**Diagnostic initial.** Diagnostic initial (18 items) — Sept domaines avec certitudes erronées ; proportionnalité à installer. Les procédures doivent être reconstruites et contrôlées.

**Points d'appui documentés.** Règle des puissances de 10 ponctuellement réussie ; Hausse simple de 15 % réussie

**Difficultés documentées.** Priorités et signes. Fractions. Écriture scientifique normalisée. Identités remarquables. Équations. Pythagore/Thalès. Trigonométrie. Proportionnalité.

*Le dossier individuel de cet élève ne comporte pas de tableau détaillé par domaine : seuls la synthèse, les points d'appui et les priorités sont documentés.*

**Axes retenus pour la séance 5.** Priorité 1 : `M2DE_CALC_01`. Priorité 2 : `M2DE_ALG_01`.

**Objectif de la séance.** Ne plus considérer une règle comme acquise sans pouvoir l'expliquer et la contrôler — conseil explicite du dossier — en commençant par les priorités opératoires puis par les identités remarquables.

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Noa MANIACI — Entrée en Seconde générale et technologique (Mathématiques)

**Diagnostic initial.** Diagnostic initial (18 items) — Sept domaines comportent des certitudes erronées ; équations à installer.

**Points d'appui documentés.** Équation linéaire ponctuellement réussie ; Réciproque 6-8-10 reconnue ; Facteur d'aire 9 trouvé ; Écriture scientifique ponctuellement correcte

**Difficultés documentées.** Priorités et signes. Fractions. Exposants négatifs. Double distributivité. Produit nul. Évolutions successives. Pythagore/Thalès. Trigonométrie.

*Le dossier individuel de cet élève ne comporte pas de tableau détaillé par domaine : seuls la synthèse, les points d'appui et les priorités sont documentés.*

**Axes retenus pour la séance 5.** Priorité 1 : `M2DE_EQ_02`. Priorité 2 : `M2DE_POURC_01`.

**Objectif de la séance.** Écrire la relation avant le calcul et effectuer un contrôle de vraisemblance — conseil du dossier — en installant d'abord l'équation produit nul puis les évolutions successives.

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Ahmad BELDI — Entrée en Première générale — Spécialité mathématiques (Mathématiques)

**Diagnostic initial.** Diagnostic initial (18 items) — Inéquations et vecteurs solides ; factorisation et langage des fonctions à rectifier ; fonctions de référence et probabilités à installer.

**Points d'appui documentés.** Inéquations ; Vecteurs ; Droites et calcul numérique à consolider

**Difficultés documentées.** Différence de carrés. Image/antécédent. Comparaison x²/x. Union/intersection/complémentaire. Certitude systématique.

*Le dossier individuel de cet élève ne comporte pas de tableau détaillé par domaine : seuls la synthèse, les points d'appui et les priorités sont documentés.*

**Axes retenus pour la séance 5.** Priorité 1 : `M1RE_ALG_02`. Priorité 2 : `M1RE_FONC_02`.

**Objectif de la séance.** Reconnaître une différence de carrés sans hésitation et employer image et antécédent dans le bon sens, deux points nommés au dossier.

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Donia KHADHRANI — Entrée en Première générale — Spécialité mathématiques (Mathématiques)

**Diagnostic initial.** Diagnostic initial (18 items) — Vecteurs solides ; calcul littéral et numérique à consolider ; inéquations, fonctions, fonctions de référence et pourcentages à installer ; droites et probabilités à rectifier.

**Points d'appui documentés.** Vecteurs ; Procédures disponibles en calcul littéral et numérique

**Difficultés documentées.** Image/antécédent. Fonctions de référence. Inéquations. Coefficient directeur. Pourcentages. Union de probabilités.

*Le dossier individuel de cet élève ne comporte pas de tableau détaillé par domaine : seuls la synthèse, les points d'appui et les priorités sont documentés.*

**Axes retenus pour la séance 5.** Priorité 1 : `M1RE_FONC_02`. Priorité 2 : `M1RE_INEQ_01`.

**Objectif de la séance.** Écrire ce qui est cherché puis la relation utilisée — conseil explicite du dossier — en commençant par le vocabulaire fonctionnel puis par les inéquations.

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Malek KHADHRANI — Entrée en Première générale — Spécialité mathématiques (Mathématiques)

**Diagnostic initial.** Diagnostic initial (18 items) — Calcul littéral et pourcentages solides ; fonctions, fonctions de référence, vecteurs et calcul numérique à rectifier ; droites à installer.

**Points d'appui documentés.** Calcul littéral ; Pourcentages et évolutions

**Difficultés documentées.** Substitution négative. Image/antécédent. Fonction inverse. Coordonnées de vecteur. Colinéarité. Pente. Puissances.

*Le dossier individuel de cet élève ne comporte pas de tableau détaillé par domaine : seuls la synthèse, les points d'appui et les priorités sont documentés.*

**Axes retenus pour la séance 5.** Priorité 1 : `M1RE_FONC_01`. Priorité 2 : `M1RE_VECT_02`.

**Objectif de la séance.** Ralentir lorsque la question paraît familière et contrôler la règle activée — conseil du dossier — en sécurisant la substitution d'une valeur négative puis le test de colinéarité.

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Ahmad BELDI — Entrée en Première — Numérique et sciences informatiques (NSI)

**Diagnostic initial.** 13 questions traitées sur 18 — Aucun domaine encore totalement stabilisé ; Web meilleur point d'appui ; programmation priorité principale, réussite 22,2 %.

**Points d'appui documentés.** Web ; Représentation binaire et données en tables : réussites hésitantes

**Difficultés documentées.** Modèle d'affectation : b = a copie la valeur, sans lien dynamique ultérieur. x = x + 1 est une affectation, non une équation. Négation d'une condition ; valeurs produites par range. Indexation à partir de 0 et signification de len. Paramètre, valeur renvoyée et None.

| Domaine | Statut au diagnostic | Observation issue du bilan |
|---|---|---|
| Affectation | Niveau initial 1 | Compétence relevée au niveau 1 dans le tableau de suivi du dossier. |
| Conditions | Niveau initial 2 | Compétence relevée au niveau 2. |
| Boucles | Niveau initial 1 | Compétence relevée au niveau 1. |
| Fonctions | Niveau initial 1 | Compétence relevée au niveau 1. |
| Listes | Niveau initial 1 | Compétence relevée au niveau 1. |
| Tables CSV | Niveau initial 2 | Compétence relevée au niveau 2. |
| Autonomie | Niveau initial 1 | Compétence relevée au niveau 1. |

**Axes retenus pour la séance 5.** Priorité 1 : `NSI1_FONC_01`. Priorité 2 : `NSI1_BOUCLE_01`.

**Objectif de la séance.** Écrire des fonctions qui renvoient réellement une valeur, et maîtriser les bornes de range — deux compétences relevées au niveau 1 en début de stage et travaillées en S2 et S3.

**Compétences non évaluées ou non travaillées à ce jour.** `NSI1_ALGO_01`, `NSI1_RES_01`

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


### Ahmed BENHADJ SALEM — Entrée en Première — Numérique et sciences informatiques (NSI)

**Diagnostic initial.** 18 questions traitées sur 18 (positionnement Première) — Représentation binaire, Web, réseaux et données en tables solides ; programmation à 55,6 %, priorité à rectifier. Erreur persistante sur un accumulateur : la somme 1+2+3 est confondue avec le nombre d'itérations.

**Points d'appui documentés.** Représentation binaire ; Web ; Réseaux ; Données en tables ; Algorithmique et types construits théoriquement disponibles

**Difficultés documentées.** Négation d'une condition. Choix for / while. len et indices. None et valeur renvoyée. Accumulateurs. Tests et cas limites.

| Domaine | Statut au diagnostic | Observation issue du bilan |
|---|---|---|
| Logique | Niveau initial 2 | Compétence relevée au niveau 2 dans le tableau de suivi du dossier. |
| Boucles | Niveau initial 2 | Compétence relevée au niveau 2. |
| Accumulateurs | Niveau initial 2 | Erreur persistante documentée dans les deux bilans. |
| Fonctions | Niveau initial 3 | Compétence relevée au niveau 3. |
| Tests | Niveau initial 1 | Compétence la plus basse du profil. |
| Structures | Niveau initial 3 | Compétence relevée au niveau 3. |
| CSV | Niveau initial 3 | Compétence relevée au niveau 3. |
| Autonomie | Niveau initial 2 | Compétence relevée au niveau 2. |
| Oral | Niveau initial 2 | Compétence relevée au niveau 2. |

**Axes retenus pour la séance 5.** Priorité 1 : `NSI1_ACC_01`. Priorité 2 : `NSI1_TEST_01`.

**Objectif de la séance.** Fiabiliser les accumulateurs — erreur documentée dans les deux bilans — et installer une pratique de test systématique, compétence la plus basse du profil, décisive pour un parcours en autonomie.

**Compétences non évaluées ou non travaillées à ce jour.** `NSI1_ALGO_01`

**Progression objectivable avant la S5.** aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges.


---

## 6. Conséquences pour la conception de la séance 5

1. La S5 ne peut pas être présentée comme une mesure de progrès déjà acquis : elle
   **produit** la mesure. Toutes les formulations des livrets et des dossiers enseignants
   emploient « à vérifier lors de l'évaluation finale » plutôt que « désormais maîtrisé ».
2. La comparaison initial/final est possible pour toute compétence disposant d'au moins
   un item du test de positionnement. Elle est impossible pour les compétences sans item
   de référence : elles sont marquées `non_comparable_absence_baseline`.
3. Les compétences introduites en phase 4 (ponts vers l'année N) sont marquées
   `non_comparable_contenu_nouveau` : elles sont notées, mais ne peuvent pas produire de delta.
4. Les axes de consolidation retenus proviennent exclusivement des priorités écrites
   dans les dossiers individuels ; aucun besoin n'a été déduit du seul niveau scolaire.
