---
title: "Fiche élève S5 - Algorithmes et mini-projet de synthèse"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
<div class="cover">
<img src="logo_slogan_nexus.png" alt="Nexus Réussite">
<div class="kicker">Pré-rentrée 2026-2027</div>
<h1>Séance 5 - Cahier élève</h1>
<div class="subtitle">Algorithmes et mini-projet de synthèse</div>
<div class="meta">5 séances de 2 heures - 10 heures<br>Python 3 - théorie, pratique, tests et projet<br>Nom : ........................................................</div>
</div><div class="student-only"></div>
## Mes objectifs

- [ ] écrire une recherche séquentielle ;
- [ ] calculer extremum et moyenne ;
- [ ] comprendre un tri par insertion ;
- [ ] tracer une recherche dichotomique ;
- [ ] livrer un projet documenté et testé ;

## Rituel sans ordinateur

## Question 1

Dans une liste non triée, quel algorithme simple permet de trouver la première occurrence d’une cible ? Que renvoie-t-on si elle est absente ?

<div class="answer"></div>

**Ma certitude :** ☐ 1 Je devine  ☐ 2 J'hésite  ☐ 3 Je pense avoir juste  ☐ 4 Je peux expliquer

**Mon contrôle :** ........................................................................................................

## Question 2

Quel prérequis est indispensable à la recherche dichotomique et que devient approximativement la zone de recherche à chaque étape ?

<div class="answer"></div>

**Ma certitude :** ☐ 1 Je devine  ☐ 2 J'hésite  ☐ 3 Je pense avoir juste  ☐ 4 Je peux expliquer

**Mon contrôle :** ........................................................................................................


## Notions de cours

### Recherche séquentielle

Parcourt les éléments un à un. Coût proportionnel au nombre d’éléments.

### Tri par insertion

Maintient une partie gauche déjà triée et insère l’élément courant à sa place. Le pire cas est quadratique.

### Recherche dichotomique

Dans une liste triée, compare à l’élément central et élimine la moitié restante. Le nombre d’étapes croît comme un logarithme.

### Correction et terminaison

- invariant : propriété vraie avant et après chaque tour ;
- variant : entier positif qui décroît vers zéro ;
- tests : cas présent, absent, premier, dernier, liste vide.



## Activité commune - choisir l’algorithme

| Besoin | Algorithme | Précondition | Coût intuitif |
|---|---|---|---|
| trouver un identifiant dans une liste quelconque |  |  |  |
| trouver dans une liste triée très longue |  |  |  |
| remettre une petite liste dans l’ordre |  |  |  |
| trouver la plus grande température |  |  |  |

## Projet final

À partir de `mesures_capteurs.csv`, produire un programme qui :

1. charge et valide les données ;
2. calcule moyenne, minimum et maximum ;
3. filtre les alertes ;
4. recherche un capteur par identifiant ;
5. trie les mesures ;
6. affiche un rapport lisible ;
7. contient des fonctions, docstrings et assertions.



## Parcours Projet guidé - Ahmad

- utiliser le fichier `projet_final_starter_ahmad.py` ;
- compléter les fonctions dans l’ordre indiqué ;
- exécuter les tests fournis après chaque fonction ;
- expliquer deux fonctions lors de la restitution.

## Parcours Projet autonome - Ahmed

- utiliser `projet_final_specification_ahmed.md` ;
- définir l’architecture du programme avant de coder ;
- écrire les tests, y compris liste vide et identifiant absent ;
- comparer recherche séquentielle et dichotomique ;
- expliquer la complexité intuitive et un invariant.


## Plan de code ou pseudo-code

<div class="answer-lg"></div>

## Tests prévus avant exécution

| Test | Entrée | Résultat attendu | Résultat obtenu | Validé |
|---:|---|---|---|:---:|
| 1 |  |  |  | ☐ |
| 2 |  |  |  | ☐ |
| 3 |  |  |  | ☐ |
| 4 |  |  |  | ☐ |

## Journal de débogage

| Symptôme observé | Hypothèse | Modification testée | Résultat |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

## Trace écrite personnelle

<div class="answer-lg"></div>

## Exit ticket

1. Une construction Python que je sais utiliser :

<div class="answer"></div>

2. Un test qui m’a aidé :

<div class="answer"></div>

**Ma certitude :** ☐ 1 Je devine  ☐ 2 J'hésite  ☐ 3 Je pense avoir juste  ☐ 4 Je peux expliquer

**Mon contrôle :** ........................................................................................................
