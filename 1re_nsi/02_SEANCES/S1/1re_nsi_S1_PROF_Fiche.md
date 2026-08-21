---
title: "Fiche enseignant S1 - Variables, types, booléens et conditions"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
<div class="cover">
<img src="logo_slogan_nexus.png" alt="Nexus Réussite">
<div class="kicker">Pré-rentrée 2026-2027</div>
<h1>Séance 1 - Fiche enseignant</h1>
<div class="subtitle">Variables, types, booléens et conditions</div>
<div class="meta">5 séances de 2 heures - 10 heures<br>Python 3 - théorie, pratique, tests et projet<br>Corrigé, différenciation et pilotage</div>
</div><div class="prof-only"></div>
## Objectifs

- comprendre l’ordre d’évaluation d’une affectation ;
- distinguer affectation et comparaison ;
- identifier les types de base ;
- écrire une condition et sa négation ;
- programmer un classificateur robuste ;

## Déroulé minute par minute

- 0-10 installation et rituel ;
- 10-25 tables de trace ;
- 25-45 types et conversions ;
- 45-65 booléens et conditions ;
- 65-70 pause ;
- 70-95 atelier guidé ;
- 95-110 différenciation ;
- 110-118 tests et revue ;
- 118-120 exit ticket ;

## Rituel prêt à l’emploi

## Question 1

Tracer sans exécuter :

```python
a = 4
b = a + 2
a = 10
```

Que valent `a` et `b` à la fin ?

**Réponse attendue :** `a` vaut 10 et `b` vaut 6 : l’affectation de `b` a copié la valeur 6.

## Question 2

Écrire en Python la négation exacte de :

```python
age >= 18
```

**Réponse attendue :** `age < 18`.


## Notions de cours

### État et affectation

Une variable est un nom associé à une valeur dans l’état courant du programme. Pour `x = expression`, Python :

1. évalue l’expression à droite ;
2. stocke la valeur obtenue sous le nom à gauche.

Ainsi, après `a = 3; b = a; a = 5`, `b` vaut encore `3`.

### Types de base

| Type | Exemple | Usage |
|---|---|---|
| `int` | `12`, `-4` | entier |
| `float` | `3.5` | approximation d’un réel |
| `str` | `"NSI"` | texte |
| `bool` | `True`, `False` | condition |
| `NoneType` | `None` | absence de valeur |

### Booléens et conditions

- `and` exige que les deux conditions soient vraies ;
- `or` exige qu’au moins une condition soit vraie ;
- `not` nie la condition ;
- la négation de `x > 5` est `x <= 5`.

```python
if temperature < 0:
    etat = "gel"
elif temperature <= 30:
    etat = "normal"
else:
    etat = "alerte"
```



## Activité commune - tables de trace

### A. Affectations

Compléter les états successifs.

```python
a = 3
b = a
a = 5
c = a + b
```

| Ligne exécutée | `a` | `b` | `c` |
|---|:---:|:---:|:---:|
| départ | non défini | non défini | non défini |
| `a = 3` |  |  |  |
| `b = a` |  |  |  |
| `a = 5` |  |  |  |
| `c = a + b` |  |  |  |

### B. Conditions aux bornes

Pour chacune des valeurs `-1`, `0`, `5`, `10`, `11`, indiquer la valeur de :

```python
(x > 0) and (x < 10)
```

| x | résultat | justification |
|---:|:---:|---|
| -1 |  |  |
| 0 |  |  |
| 5 |  |  |
| 10 |  |  |
| 11 |  |  |



## Parcours Fondations - Ahmad

1. Corriger le programme suivant :

```python
age = "16"
print(age + 1)
```

2. Compléter pour afficher `pair`, `impair` ou `nul`.

```python
n = -3
## À compléter
```

3. Écrire la négation Python de chacune des conditions :

- `x >= 0` ;
- `age < 18` ;
- `(x > 0) and (x < 10)`.

4. Écrire un programme qui classe une température en `gel`, `normal` ou `alerte`.

## Parcours Fiabilisation - Ahmed

1. Écrire une condition vraie exactement lorsque `x` n’appartient pas à l’intervalle `[0, 10]`.
2. Simplifier la négation de `(x >= 2) and (x <= 8)`.
3. Corriger un programme comportant une branche inaccessible.
4. Écrire des tests sur les valeurs limites `-1`, `0`, `30`, `31` du classificateur de température.



## Corrigé essentiel

- trace : `a=3`, puis `b=3`, puis `a=5`, enfin `c=8` ;
- la condition est vraie seulement pour `x=5` dans la liste proposée ;
- `age = int("16")` permet `age + 1` ;
- négation de `x >= 0` : `x < 0` ; de `age < 18` : `age >= 18` ;
- négation de `(x > 0) and (x < 10)` : `(x <= 0) or (x >= 10)`.


## Consignes prêtes à dire

- « Avant d’exécuter, écris ce que tu prévois. »
- « Une réponse sans contrôle reste une hypothèse. »
- « Le bug utile est celui que l’on peut reproduire. »
- « Ne change qu’une chose à la fois, puis relance les tests. »
- « Explique le rôle de cette variable sans lire le code mot à mot. »

## Points de vigilance

- ne pas transformer l’activité en copie de code projeté ;
- vérifier que les deux élèves alternent pilote et navigateur ;
- ne pas confondre réussite après aide D/E et autonomie ;
- demander un test sur les bornes ;
- conserver le fichier final et le journal des erreurs.

## Indicateurs de réussite

| Élève | Prévision exacte | Code exécutable | Tests pertinents | Explication | Aide maximale |
|---|:---:|:---:|:---:|:---:|:---:|
| Ahmad BELDI |  |  |  |  |  |
| Ahmed BENHADJ SALEM |  |  |  |  |  |
