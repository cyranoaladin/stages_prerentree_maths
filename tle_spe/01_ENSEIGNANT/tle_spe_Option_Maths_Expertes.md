# Terminale Spécialité Mathématiques — Module complémentaire
## Enseignement optionnel de mathématiques expertes

**Public :** deux élèves de la cohorte, l'un du groupe 1, l'autre du groupe 2.
**Format :** 20 minutes par séance, prélevées sur le temps différencié. Pas de séance dédiée.
**Source pédagogique :** `05_SOURCES/stage_prerentree_terminale_maths.md`, § 9.

> Ce document ne contient aucune donnée nominative. Le profil de chaque élève figure dans son
> livret individuel, sous `04_NOMINATIFS/`.

---

## 1. Ce que l'option demande

L'enseignement optionnel de mathématiques expertes (BO spécial n° 8 du 25 juillet 2019)
comporte trois blocs :

| Bloc | Contenus |
|---|---|
| Nombres complexes | Point de vue algébrique, point de vue géométrique, équations polynomiales |
| Arithmétique | Divisibilité, division euclidienne, congruences, PGCD, Bézout, Gauss, nombres premiers, petit théorème de Fermat |
| Matrices et graphes | Calcul matriciel, systèmes linéaires, graphes, marches aléatoires |

C'est un enseignement **de démonstration** : plus que dans la spécialité, l'élève y rédige
des preuves. Les prérequis ne sont donc pas seulement calculatoires.

## 2. Les prérequis évalués

Un positionnement distinct de 18 items a été proposé, portant sur six domaines. Réussite
moyenne sur les deux élèves :

| Domaine | Réussite moyenne | Items | Ce que l'option en fait |
|---|---:|---:|---|
| Suites numériques | 100 % | 2 | Suites définies par U(n+1) = A U(n) ; marches aléatoires |
| Logique | 83,3 % | 2 | Contraposée, absurde, disjonction de cas : l'outillage des preuves d'arithmétique |
| Dénombrement | 83,3 % | 2 | Comptage des diviseurs à partir de la décomposition en facteurs premiers |
| Arithmétique | 79,2 % | 8 | Divisibilité, congruences, PGCD, Bézout, Gauss, Fermat |
| Calcul littéral | 50 % | 2 | Identités remarquables dans ℂ, factorisations de z^n − 1 |
| Systèmes d'équations | 50 % | 2 | Écriture matricielle AX = B, résolution par inversion |

Les deux domaines à 50 % le sont pour des raisons opposées selon l'élève : chez l'un ils sont
acquis, chez l'autre ils sont restés **sans réponse**. La moyenne est donc trompeuse : le
module doit être conduit **individuellement**, jamais en petit groupe de deux.

## 3. Répartition sur les cinq séances

| Séance | Contenu du module | Articulation avec le thème commun |
|---:|---|---|
| 1 | Division euclidienne : poser a = bq + r et contrôler 0 ≤ r < b | Suites : la relation de récurrence est un calcul répété, comme l'algorithme d'Euclide |
| 2 | Diviseurs, nombres premiers, décomposition en facteurs premiers | Aucun lien direct : temps autonome |
| 3 | PGCD et algorithme d'Euclide ; fractions irréductibles | Second degré : le contrôle somme/produit est le même geste de vérification |
| 4 | Logique : contraposée, réciproque, contre-exemple | Dérivation : le contre-exemple de la séance est un objet logique, à nommer comme tel |
| 5 | Calcul littéral et systèmes ; ouverture matrices et complexes | Produit scalaire : le système d'orthogonalité est un système linéaire |

## 4. Conduite du module

### Séance 1 — Division euclidienne

**Ce qui est visé.** L'égalité a = bq + r avec l'encadrement 0 ≤ r < b, systématiquement
écrite. L'encadrement est le contrôle : un reste supérieur ou égal au diviseur signale une
erreur immédiate.

**Activité (20 min).** Poser trois divisions euclidiennes : 83 par 9, 250 par 12, 1 000 par
37. Exiger à chaque fois l'égalité complète **et** l'encadrement du reste.

**Ouverture.** Annoncer, sans le traiter : en Terminale, « a ≡ b modulo n » signifie que a et
b ont le même reste dans la division par n. Toute l'arithmétique de l'année repose sur cette
définition.

### Séance 2 — Diviseurs et nombres premiers

**Ce qui est visé.** L'énumération des diviseurs **par paires**, jusqu'à la racine carrée ; le
critère d'arrêt du test de primalité ; la décomposition en facteurs premiers.

**Activité (20 min).** Énumérer les diviseurs de 18, de 36, de 84 par paires. Décomposer 84
et 360. Faire découvrir la formule du nombre de diviseurs à partir des exposants :
84 = 2² × 3 × 7 possède (2+1)(1+1)(1+1) = 12 diviseurs.

**Ouverture.** Le théorème fondamental de l'arithmétique — l'unicité de la décomposition —
est le résultat sur lequel repose tout le bloc.

### Séance 3 — PGCD et algorithme d'Euclide

**Ce qui est visé.** L'algorithme d'Euclide écrit ligne par ligne, chaque ligne étant une
division euclidienne complète.

**Activité (20 min).** Calculer PGCD(84 ; 60), PGCD(105 ; 135), PGCD(1 071 ; 462) par
l'algorithme. Rendre irréductible 105/135 en une seule étape.

**Ouverture.** Le théorème de Bézout affirme qu'il existe des entiers u et v tels que
au + bv = PGCD(a ; b), et l'algorithme d'Euclide « remonté » les fournit. C'est le résultat
central de l'année.

### Séance 4 — Logique

**Ce qui est visé.** Contraposée, réciproque, contre-exemple, et la conscience que ces objets
sont des outils de preuve, pas du vocabulaire.

**Activité (20 min).** Pour chacun des énoncés suivants : écrire la contraposée, écrire la
réciproque, dire si chacune est vraie.

| Énoncé | Contraposée | Réciproque vraie ? |
|---|---|---|
| Si n est multiple de 6, alors n est pair | Si n est impair, alors n n'est pas multiple de 6 | Non (n = 4) |
| Si a = b, alors a² = b² | Si a² ≠ b², alors a ≠ b | Non (a = 1, b = −1) |
| Si n² est pair, alors n est pair | Si n est impair, alors n² est impair | Oui |

**Ouverture.** La preuve classique « si n² est pair alors n est pair » se fait **par
contraposée** : c'est le premier exemple de l'année où l'outil logique est indispensable.

### Séance 5 — Calcul littéral, systèmes, ouvertures

**Ce qui est visé.** Factorisation par identités remarquables ; résolution d'un système par
combinaison et par substitution.

**Activité (20 min).** Factoriser 9x² − 25, puis x² + 1 — impossible dans ℝ, ce qui ouvre sur
les complexes. Résoudre { 2x + y = 11 ; x − y = 1 } par combinaison, puis réécrire ce système
sous la forme d'un tableau de coefficients.

**Ouverture.** Deux annonces, sans traitement :

> **Complexes.** Il existe un nombre noté i tel que i² = −1. Alors x² + 1 = (x − i)(x + i) :
> toute équation du second degré admet des solutions.
>
> **Matrices.** Le système { 2x + y = 11 ; x − y = 1 } s'écrit AX = B avec A le tableau des
> coefficients. On le résout en inversant A.

## 5. Conduite individualisée

Le module est **individuel**. Deux conduites types selon le profil :

| Profil | Conduite |
|---|---|
| Positionnement quasi complet, une seule consolidation | Traiter directement les ouvertures ; consacrer les 20 minutes à la rédaction de preuves courtes |
| Domaines laissés sans réponse | Commencer par un diagnostic ciblé sur ces domaines (séance 1), puis installer ; ne pas aborder les ouvertures avant la séance 4 |

Dans le second cas, **ne rien conclure du silence** : un domaine sans réponse peut relever
d'un manque de temps, d'un oubli, ou d'une lacune réelle. Le diagnostic de la séance 1 tranche.

## 6. Indicateurs de fin de module

- L'élève écrit l'égalité a = bq + r **avec** l'encadrement du reste, sans qu'on le lui
  demande.
- L'élève pose l'algorithme d'Euclide ligne par ligne plutôt que de chercher le PGCD « de
  tête ».
- L'élève distingue contraposée et réciproque, et sait qu'une seule des deux est équivalente
  à l'implication de départ.
- L'élève sait dire ce que l'option ajoutera à la spécialité dans l'année.

---
_Source pédagogique unique : `stage_prerentree_terminale_maths.md`._
