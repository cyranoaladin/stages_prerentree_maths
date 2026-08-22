# Programme complet du stage de pré-rentrée

## Numérique et sciences informatiques — Entrée en Terminale

### Nexus Réussite — 5 séances de 2 heures — Rentrée 2026-2027

---

# 1. Cadre, données disponibles et informations manquantes

## 1.1 Cadre général

Ce stage prépare l'entrée en classe terminale pour les élèves qui conservent la spécialité
numérique et sciences informatiques.

Il est organisé par **Nexus Réussite**, centre d'accompagnement scolaire, et dure
**10 heures**, à raison de **2 heures par jour pendant 5 jours consécutifs, du 24 au 28 août
2026**. Un stage est organisé par enseignement de spécialité : les élèves concernés suivent
donc également le stage de mathématiques, soit 20 heures au total.

Tous les élèves concernés conservent également la spécialité mathématiques : ils constituent
le **groupe 1** de la cohorte de pré-rentrée et suivent aussi le module `tle_spe`. Le module
NSI est donc conçu pour s'articuler avec le module de mathématiques, notamment sur les
boucles et le raisonnement sur le coût.

L'objet du stage est précis : **consolider les notions de Première NSI dont la Terminale a un
besoin immédiat**, en traitant en priorité les conceptions erronées que le positionnement a
mises au jour.

**Effectif :** 4 élèves.

## 1.2 Documents exploités

### Positionnement de pré-rentrée

Un test de positionnement de **18 items** a été passé par chaque élève, couvrant sept
domaines du programme de Première NSI :

| Domaine | Nombre d'items |
|---|---:|
| Représentation binaire | 2 |
| Booléens et logique | 2 |
| Types construits | 4 |
| Programmation | 4 |
| Algorithmique | 2 |
| Données en tables | 2 |
| Architecture et systèmes | 2 |

Chaque item est accompagné d'un **niveau de certitude déclaré de 1 à 4**.

| Situation | Lecture | Traitement |
|---|---|---|
| Juste et sûr | acquis disponible | on entretient |
| Juste mais hésitant | acquis fragile | on consolide |
| Faux et lucide | notion absente | on installe |
| **Faux et sûr** | **conception erronée** | **on confronte** |

### Bilans individuels

Chaque élève dispose d'un bilan élève et d'un bilan parents détaillant chaque item : énoncé,
réponse donnée, réponse attendue, origine de l'erreur, point à retenir. Ces bilans fondent
l'individualisation des livrets.

## 1.3 Informations à confirmer avant la première séance

1. La version de Python installée et l'environnement de travail retenu par l'établissement.
2. La disponibilité d'un SGBD ou d'un environnement SQL pour la séance 5.
3. Le sujet et le calendrier du projet de Terminale, s'il est déjà arrêté.
4. Le matériel : un poste par élève ou un poste par binôme.

## 1.4 Hypothèses de travail

- Le programme de Première NSI a été traité dans son intégralité.
- Python 3 est disponible sur chaque poste ; aucune bibliothèque externe n'est requise.
- Le stage ne suppose aucun environnement en ligne : tout fonctionne hors réseau.
- Aucune notation chiffrée n'est produite.

---

# 2. Référentiel officiel applicable en 2026-2027

## 2.1 Programme de Première NSI effectivement suivi

Programme de l'enseignement de spécialité NSI de la classe de première
(BO spécial n° 1 du 22 janvier 2019) :

- Histoire de l'informatique.
- Représentation des données : types et valeurs de base.
- Représentation des données : types construits.
- Traitement de données en tables.
- Interactions entre l'homme et la machine sur le Web.
- Architectures matérielles et systèmes d'exploitation.
- Langages et programmation.
- Algorithmique.

## 2.2 Programme de Terminale NSI applicable

Programme de l'enseignement de spécialité NSI de la classe terminale
(BO spécial n° 8 du 25 juillet 2019) :

| Bloc | Contenus |
|---|---|
| Structures de données | Listes, piles, files ; dictionnaires ; arbres ; graphes |
| Bases de données | Modèle relationnel ; langage SQL ; systèmes de gestion de bases de données |
| Architectures matérielles, systèmes d'exploitation et réseaux | Processus, ressources, ordonnancement, interblocage ; protocoles de routage ; sécurisation des communications |
| Langages et programmation | Récursivité ; modularité ; mise au point ; paradigmes ; calculabilité et décidabilité |
| Algorithmique | Diviser pour régner ; programmation dynamique ; algorithmes sur les arbres et les graphes ; recherche textuelle |

## 2.3 Conséquences pour le stage

Chaque bloc de Terminale prolonge un contenu de Première. C'est cette correspondance qui
donne au stage sa cible.

| Bloc de Terminale | Prérequis de Première déterminant |
|---|---|
| Structures de données | Types construits : tableaux, p-uplets, dictionnaires, mutabilité, indexation |
| Bases de données et SQL | Traitement de données en tables : enregistrements, descripteurs, sélection, projection, jointure |
| Récursivité et modularité | Langages et programmation : appel de fonction, paramètre, valeur de retour, portée |
| Diviser pour régner, programmation dynamique | Algorithmique : recherche dichotomique, tris, raisonnement sur le coût |
| Processus, ordonnancement, réseaux | Architectures matérielles et systèmes d'exploitation |
| Sécurisation des communications | Représentation binaire, arithmétique des entiers |

---

# 3. Diagnostic synthétique du groupe

## 3.1 Réussite moyenne par domaine

Sur les quatre élèves de la cohorte :

| Domaine | Réussite moyenne | Certitudes erronées | À installer | À consolider | Acquis |
|---|---:|---:|---:|---:|---:|
| Représentation binaire | 40,0 % | 1 | 2 | 1 | 1 |
| Algorithmique | 53,3 % | 2 | 1 | 1 | 1 |
| Données en tables | 53,3 % | 3 | 0 | 1 | 1 |
| Programmation | 56,7 % | 3 | 1 | 1 | 0 |
| Types construits | 63,3 % | 3 | 1 | 0 | 1 |
| Booléens et logique | 80,0 % | 1 | 1 | 1 | 2 |
| Architecture et systèmes | 100,0 % | 0 | 0 | 1 | 4 |

## 3.2 Difficultés communes les plus structurantes

### A. La représentation binaire n'est pas disponible

C'est le domaine le plus faible du groupe : **40 % de réussite**, avec trois élèves à 0 %.
La conversion entre bases n'est pas installée.

L'enjeu en Terminale est indirect mais réel : le typage des attributs d'une base de données,
le coût mémoire des structures de données, et surtout l'arithmétique modulaire du chiffrement
dans le chapitre « sécurisation des communications » supposent une aisance sur les entiers en
machine.

### B. Les types construits sont manipulés sans modèle mental

Trois élèves portent une certitude erronée sur les types construits. Deux confusions
reviennent : l'indexation des tableaux, et l'effet des méthodes qui modifient en place.

C'est l'obstacle le plus coûteux pour la Terminale : **toutes** les structures de données de
l'année — piles, files, arbres, graphes — s'implémentent avec des listes et des
dictionnaires. Une confusion sur l'indexation ou sur la mutabilité se paie à chaque
implémentation.

### C. La valeur de retour est confondue avec l'effet de bord

Trois élèves portent une certitude erronée en programmation. L'erreur dominante concerne
`return` : une fonction sans `return` renvoie `None`, ce qui n'empêche pas qu'elle ait
modifié un objet mutable reçu en paramètre. Les deux notions sont confondues.

La récursivité de Terminale est inaccessible tant que ce point n'est pas net : une fonction
récursive **renvoie** une valeur construite à partir de la valeur renvoyée par l'appel
suivant.

### D. Le traitement de données en tables n'est pas nommé

Trois élèves portent une certitude erronée sur les données en tables. Ce n'est pas
l'opération qui manque, mais son **nom** : sélection, projection, jointure ne sont pas
distinguées.

Or le chapitre « bases de données » de Terminale reprend exactement ces trois opérations sous
les noms SQL `WHERE`, `SELECT` et `JOIN`. Une confusion de vocabulaire y devient une
confusion de requête.

### E. Le raisonnement sur le coût est fragile

Deux élèves portent une certitude erronée en algorithmique. La précondition de la recherche
dichotomique — un tableau trié — et l'ordre de grandeur du nombre de comparaisons ne sont pas
stabilisés.

C'est ce raisonnement qui justifie « diviser pour régner » et la programmation dynamique en
Terminale.

## 3.3 Points d'appui du groupe

- **Architecture et systèmes est acquis par tout le groupe** (100 %). Ce domaine ne fait
  l'objet d'aucune séance dédiée : il est réinvesti en séance 5.
- Les booléens sont réussis à 80 %, avec deux élèves pour qui le domaine est un point
  d'appui.
- Deux élèves présentent un positionnement quasi complet et disposent d'un parcours
  d'approfondissement dès la séance 1.

## 3.4 Limites du positionnement

- Le positionnement porte sur des questions à réponse courte : il renseigne sur les
  connaissances, peu sur la capacité à **écrire** un programme complet. Une évaluation
  pratique est donc prévue en séance 3.
- Les interactions homme-machine sur le Web, au programme de Première, ne sont pas évaluées
  et ne sont pas traitées : la Terminale ne les prolonge pas directement.
- L'histoire de l'informatique n'est pas évaluée.

---

# 4. Objectifs du stage

## 4.1 Objectifs généraux

1. Faire tomber les conceptions erronées repérées, en priorité celles portées avec certitude.
2. Rétablir le geste de la **table de trace** : écrire l'état des variables avant d'exécuter.
3. Installer les prérequis manquants sans anticiper le programme de Terminale.
4. Nommer, pour chaque notion, ce qu'elle conditionne en Terminale.
5. Réétalonner la confiance.
6. Faire repartir chaque élève avec un plan de travail personnel pour septembre.

## 4.2 Hiérarchie des priorités

**Priorité 1 — Les certitudes erronées**, traitées en premier dans chaque séance.

**Priorité 2 — Les prérequis directs de la Terminale** : indexation et mutabilité, valeur de
retour, opérations sur les tables, coût d'un algorithme.

**Priorité 3 — Les consolidations individuelles**, traitées dans les temps différenciés.

## 4.3 Objectifs opérationnels par séance

| Séance | Thème commun | Objectif opérationnel principal |
|---:|---|---|
| 1 | Représentation des données et booléens | Convertir entre bases 2, 10 et 16 ; évaluer une expression booléenne et sa négation |
| 2 | Types construits | Indexer sans erreur ; distinguer modification en place et création d'un nouvel objet |
| 3 | Programmation | Distinguer valeur renvoyée et effet de bord ; maîtriser les bornes de `range` |
| 4 | Algorithmique | Énoncer la précondition d'un algorithme et évaluer son coût |
| 5 | Données en tables, bases de données, systèmes | Nommer sélection, projection, jointure et les écrire en SQL |

---

# 5. Progression détaillée des cinq séances

L'ordre est déduit du diagnostic : le domaine le plus faible d'abord, puis les domaines
portant le plus de certitudes erronées, dans un ordre qui respecte les dépendances
techniques.

## Séance 1 — Représentation des données et booléens

### Objectifs

- Convertir un entier entre les bases 2, 10 et 16.
- Évaluer une expression booléenne en respectant les priorités.
- Écrire la négation d'une expression composée (lois de De Morgan).

### Déroulé (120 minutes)

| Durée | Phase | Contenu |
|---:|---|---|
| 10 min | Ouverture | Restitution du positionnement ; lecture de la carte maîtrise × confiance |
| 20 min | Confrontation | Écrire 22 en binaire : recueil des réponses, puis vérification par recalcul |
| 25 min | Reconstruction | Décomposition en puissances de 2 ; méthode des divisions successives ; base 16 |
| 30 min | Entraînement différencié | Trois parcours |
| 20 min | Booléens et ouverture | Tables de vérité ; De Morgan ; usage dans les conditions de boucle et les clauses SQL |
| 15 min | Trace écrite et bilan | Fiche de synthèse, auto-évaluation |

### Trace écrite attendue

> **Base 2.** Un entier s'écrit comme somme de puissances de 2 décroissantes.
> 22 = 16 + 4 + 2 = 2⁴ + 2² + 2¹, soit **10110**.
> Méthode alternative : divisions successives par 2, restes lus **de bas en haut**.
>
> **Base 16.** A = 10, B = 11, C = 12, D = 13, E = 14, F = 15.
> 0x2A = 2 × 16 + 10 = 42. Réciproquement 60 = 3 × 16 + 12 = 0x3C.
>
> **Booléens.** Priorités : `not`, puis `and`, puis `or`.
> Lois de De Morgan : non(A et B) = (non A) ou (non B) ; non(A ou B) = (non A) et (non B).
>
> **Ce que la Terminale en fait.** Le typage des attributs d'une base de données, le coût
> mémoire des structures, et l'arithmétique du chiffrement reposent sur la représentation des
> entiers. Les conditions composées structurent les invariants de boucle et les clauses
> `WHERE`.

### Erreurs à surveiller

- Restes lus de haut en bas dans la méthode des divisions successives.
- F confondu avec 16 au lieu de 15.
- Négation d'une conjonction écrite comme conjonction des négations.
- Priorité de `not` ignorée.

## Séance 2 — Types construits : tableaux, dictionnaires, mutabilité

### Objectifs

- Indexer un tableau sans erreur, y compris avec des indices négatifs.
- Distinguer une méthode qui modifie en place d'une expression qui construit un nouvel objet.
- Accéder à un dictionnaire, ajouter, supprimer, parcourir.

### Déroulé (120 minutes)

| Durée | Phase | Contenu |
|---:|---|---|
| 10 min | Ouverture | Contrôle sur la séance 1 : convertir 0x2A |
| 20 min | Confrontation | `L = L.append(4)` : que vaut L ensuite ? Exécution effective |
| 25 min | Reconstruction | Indexation ; méthodes en place et valeur `None` ; dictionnaires |
| 30 min | Entraînement différencié | Trois parcours |
| 20 min | Ouverture Terminale | Une pile et une file construites sur une liste ; un arbre construit sur un dictionnaire |
| 15 min | Trace écrite et bilan | Fiche de synthèse, auto-évaluation |

### Trace écrite attendue

> **Indexation.** Les indices commencent à **0**. Pour un tableau de n éléments, le dernier
> indice valide est n − 1. L'indice −1 désigne le dernier élément.
>
> **Modification en place.** `L.append(x)`, `L.insert(i, x)`, `del L[i]` **modifient** la
> liste et **ne renvoient rien** (`None`). Écrire `L = L.append(4)` détruit la liste.
> À l'inverse, `L + [4]` construit une **nouvelle** liste sans modifier L.
>
> **Dictionnaires.** `d[cle]` accède ; `d[cle] = valeur` crée ou remplace ; `del d[cle]`
> supprime ; `d.get(cle, defaut)` évite l'erreur `KeyError` ; `d.items()` parcourt les couples.
>
> **Ce que la Terminale en fait.** Une pile, une file, un arbre, un graphe : toutes ces
> structures s'implémentent avec des listes et des dictionnaires. Ce sont les mêmes gestes,
> appliqués à des interfaces différentes.

### Erreurs à surveiller

- `L[n]` sur un tableau de n éléments.
- `L = L.append(x)`.
- Accès à une clé absente sans `get`.
- Confusion entre `d[cle]` et `d.get(cle)`.

## Séance 3 — Programmation : fonctions, retour, portée, boucles

### Objectifs

- Distinguer valeur renvoyée et effet de bord.
- Maîtriser les bornes de `range`, y compris avec un pas.
- Construire une table de trace pour un accumulateur.
- Écrire une spécification et deux tests par fonction.

### Déroulé (120 minutes)

| Durée | Phase | Contenu |
|---:|---|---|
| 10 min | Ouverture | Contrôle sur la séance 2 : que contient L après `L.insert(0, 9)` |
| 20 min | Confrontation | `r = h([1, 2])` où h se contente d'un `append` : que vaut r ? |
| 25 min | Reconstruction | Appel, paramètre, retour, `None` ; portée ; bornes de `range` ; table de trace |
| 30 min | Entraînement différencié | Trois parcours, sur machine |
| 20 min | Évaluation pratique | Mini-diagnostic pratique (§ 7) |
| 15 min | Trace écrite et bilan | Fiche de synthèse, auto-évaluation |

### Trace écrite attendue

> **Retour et effet de bord.** Une fonction sans `return` renvoie `None`. Cela n'empêche pas
> qu'elle ait **modifié** un objet mutable reçu en paramètre. Ce sont deux choses distinctes,
> qui peuvent coexister.
>
> **Bornes.** `range(a, b, p)` produit a, a + p, … en s'arrêtant **strictement avant** b.
> `range(3)` produit 0, 1, 2. `range(2, 10, 3)` produit 2, 5, 8.
>
> **Table de trace.** Avant d'exécuter, j'écris l'état des variables tour par tour.
>
> **Ce que la Terminale en fait.** Une fonction récursive renvoie une valeur construite à
> partir de celle que renvoie l'appel suivant : la notion de valeur renvoyée doit être nette.
> La modularité et la mise au point s'appuient sur la spécification et les tests.

### Erreurs à surveiller

- Croire qu'une fonction sans `return` ne fait rien.
- Croire qu'une fonction qui modifie une liste renvoie cette liste.
- Décalage d'une unité sur les bornes de boucle.
- Variable locale confondue avec variable globale.

## Séance 4 — Algorithmique : préconditions, recherche, tris, coût

### Objectifs

- Énoncer la précondition d'un algorithme et dire ce qui se passe si elle n'est pas vérifiée.
- Évaluer le coût d'une recherche séquentielle et d'une recherche dichotomique.
- Comparer deux algorithmes sur un même problème.

### Déroulé (120 minutes)

| Durée | Phase | Contenu |
|---:|---|---|
| 10 min | Ouverture | Contrôle sur la séance 3 : valeurs produites par `range(1, 10, 4)` |
| 20 min | Confrontation | Appliquer la dichotomie à un tableau non trié : que se passe-t-il ? |
| 25 min | Reconstruction | Précondition ; dichotomie ; coût logarithmique ; tri par insertion |
| 30 min | Entraînement différencié | Trois parcours, sur machine |
| 20 min | Ouverture Terminale | Diviser pour régner ; parcours d'arbre ; programmation dynamique |
| 15 min | Trace écrite et bilan | Fiche de synthèse, auto-évaluation |

### Trace écrite attendue

> **Précondition.** La recherche dichotomique exige un tableau **trié**. Sur un tableau non
> trié, elle ne renvoie pas une erreur : elle renvoie un résultat **faux**. C'est le pire cas
> possible pour un programme.
>
> **Coût.** Recherche séquentielle : jusqu'à n comparaisons. Recherche dichotomique : de
> l'ordre de log₂(n). Repères : 2¹⁰ = 1 024, 2²⁰ ≈ 10⁶.
>
> **Arbitrage.** Trier puis chercher coûte plus cher qu'une recherche séquentielle unique.
> C'est rentable si l'on effectue de nombreuses recherches sur le même tableau.
>
> **Ce que la Terminale en fait.** « Diviser pour régner » généralise le geste de la
> dichotomie. La programmation dynamique évite de recalculer plusieurs fois la même
> sous-solution. Les parcours d'arbres et de graphes s'analysent par le même raisonnement sur
> le coût.

### Erreurs à surveiller

- Appliquer la dichotomie sans vérifier la précondition.
- Confondre log₂(n) et n/2.
- Croire qu'un algorithme faux échoue toujours bruyamment.
- Comparer deux algorithmes sur une seule exécution.

## Séance 5 — Données en tables, bases de données, systèmes, projet

### Objectifs

- Nommer sélection, projection et jointure, et les écrire en SQL.
- Réinvestir architecture et systèmes, acquis par tout le groupe.
- Situer le projet de Terminale.
- Mesurer les progrès et fixer le plan de septembre.

### Déroulé (120 minutes)

| Durée | Phase | Contenu |
|---:|---|---|
| 10 min | Ouverture | Contrôle sur la séance 4 : précondition de la dichotomie |
| 25 min | Données en tables | Enregistrement, descripteur ; sélection, projection, jointure |
| 20 min | Ouverture bases de données | Les mêmes opérations en SQL ; clé primaire, clé étrangère |
| 15 min | Architecture et systèmes | Réinvestissement : von Neumann, rôle du système ; ouverture processus et réseaux |
| 35 min | Évaluation finale | Épreuve de synthèse |
| 15 min | Bilan | Restitution, plan de septembre, portfolio |

### Trace écrite attendue

> **Table.** Une **ligne** est un enregistrement (un individu, un objet). Une **colonne** est
> un descripteur (un attribut). La première ligne d'un CSV contient en général les noms des
> descripteurs et ne compte pas comme donnée.
>
> **Trois opérations.**
> Sélection : choisir des **lignes** selon une condition.
> Projection : choisir des **colonnes**.
> Jointure : rapprocher deux tables par un attribut commun.
>
> **En SQL :**
> `SELECT nom, note FROM eleves WHERE note > 10 ;`
> — `SELECT` réalise la projection, `WHERE` la sélection.
> `SELECT ... FROM eleves JOIN classes ON eleves.id_classe = classes.id ;`
> — `JOIN` réalise la jointure.
>
> **Ce que la Terminale en fait.** Le chapitre « bases de données » ajoute le modèle
> relationnel, les contraintes d'intégrité, les clés primaires et étrangères, et le système de
> gestion de bases de données. Les trois opérations restent les mêmes.

### Erreurs à surveiller

- Compter la ligne d'en-tête parmi les enregistrements.
- Confondre sélection et projection.
- Écrire une jointure sans condition de rapprochement.
- Confondre clé primaire et clé étrangère.

---

# 6. Différenciation

## 6.1 Trois parcours

| Parcours | Public | Ce qui change |
|---|---|---|
| **Consolidation** | Domaine de la séance en certitude erronée ou notion absente | Exemple exécuté fourni, table de trace pré-remplie, étayage écrit |
| **Maîtrise** | Domaine réussi mais hésitant | Pas d'exemple ; spécification et tests exigés |
| **Approfondissement** | Domaine acquis avec certitude | Problème ouvert, comparaison d'algorithmes, ouverture explicite sur la Terminale |

## 6.2 Aides graduées

| Aide | Contenu |
|---|---|
| A | Rappel de la syntaxe ou de la propriété, sans application |
| B | Première ligne écrite, suite à la charge de l'élève |
| C | Exemple exécuté analogue, avec sa sortie |
| D | Découpage en trois sous-fonctions |
| E | Squelette de code à compléter |

## 6.3 Rituel de séance

Identique au module de mathématiques : contrôle d'entrée, confrontation, reconstruction,
entraînement différencié, ouverture Terminale, trace écrite. La régularité entre les deux
modules est volontaire : les élèves du groupe 1 suivent les deux.

---

# 7. Évaluation et suivi

## 7.1 Dispositif

**Avant.** Positionnement de 18 items avec certitude déclarée ; bilans ; livret individuel.

**Pendant.** Question de contrôle en ouverture ; observation de quatre indicateurs (lecture
de l'énoncé, choix de la structure, exactitude, mise au point) ; relevé de l'aide maximale ;
mini-diagnostic pratique en séance 3.

**Après.** Évaluation finale ; auto-évaluation ; plan de septembre.

## 7.2 Échelle de maîtrise

| Niveau | Description |
|---:|---|
| 1 | Pas encore : l'élève ne sait pas par où commencer |
| 2 | Avec aide : correct si le squelette est fourni |
| 3 | Seul : programme correct, sans aide |
| 4 | Je peux expliquer : l'élève spécifie, teste et justifie ses choix |

## 7.3 Critères de réussite du stage

1. Plus aucune conception erronée sur les domaines traités.
2. Une table de trace est écrite avant toute exécution, sans qu'on le demande.
3. Chaque fonction écrite est accompagnée d'au moins deux tests.
4. L'aide maximale utilisée a diminué entre la séance 1 et la séance 5.
5. Un plan de travail écrit pour septembre est rempli.

---

# 8. Recommandations didactiques

## 8.1 Exécuter, ne pas raconter

En NSI, la confrontation ne se fait pas au tableau : elle se fait **à l'écran**. L'élève écrit
sa prédiction, puis exécute. L'écart entre les deux est l'objet du travail.

## 8.2 Imposer la table de trace

Avant toute exécution, l'élève écrit l'état des variables tour par tour. Ce geste rend visible
le raisonnement, y compris quand il est faux — ce qu'une exécution seule ne fait jamais.

## 8.3 Exiger la spécification et deux tests

Chaque fonction écrite est accompagnée d'une phrase disant ce qu'elle prend et ce qu'elle
renvoie, et de deux appels dont on connaît le résultat attendu. C'est le geste que la
Terminale attend en mise au point.

## 8.4 Ne pas anticiper la récursivité

La récursivité est un contenu de Terminale. Le stage prépare sa compréhension en stabilisant
la valeur de retour, mais n'écrit aucune fonction récursive.

## 8.5 Articuler avec le module de mathématiques

Les quatre élèves suivent les deux modules. Deux articulations sont explicites :

- les boucles de la séance 5 du module `tle_spe` (calcul des termes d'une suite) sont
  reprises en séance 3 de ce module, sous l'angle de la spécification et des tests ;
- le raisonnement sur le coût de la séance 4 rejoint le travail sur les ordres de grandeur en
  mathématiques.

---

# Synthèse opérationnelle

| Élément | Décision |
|---|---|
| Public | 4 élèves du groupe 1, entrant en Terminale NSI |
| Durée | 10 heures : 2 h/jour, 5 jours consécutifs, du 24 au 28 août 2026 |
| Ordre des séances | Représentation et booléens, types construits, programmation, algorithmique, données et systèmes |
| Principe directeur | Prédire, exécuter, confronter ; table de trace systématique |
| Différenciation | Trois parcours par séance, cinq niveaux d'aide |
| Individualisation | Un livret par élève, construit item par item à partir de son propre bilan |
| Évaluation | Sans note ; matrice réussite × confiance, avant et après |
| Sortie | Un plan de travail personnel écrit pour septembre |
