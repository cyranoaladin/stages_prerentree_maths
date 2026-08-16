---
title: "Fiche élève S2 - Boucles, compteurs et accumulateurs"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
<div class="cover">
<img src="logo_slogan_nexus.png" alt="Nexus Réussite">
<div class="kicker">Pré-rentrée 2026-2027</div>
<h1>Séance 2 - Cahier élève</h1>
<div class="subtitle">Boucles, compteurs et accumulateurs</div>
<div class="meta">5 séances de 2 heures - 10 heures<br>Python 3 - théorie, pratique, tests et projet<br>Nom : ........................................................</div>
</div><div class="student-only"></div>
# Mes objectifs

- [ ] comprendre les valeurs produites par range ;
- [ ] choisir entre for et while ;
- [ ] utiliser compteur et accumulateur ;
- [ ] éviter les erreurs de borne ;
- [ ] justifier une terminaison simple ;

# Rituel sans ordinateur

## Question 1

Écrire, dans l’ordre, les valeurs produites par :

```python
range(2, 9, 3)
```

<div class="answer"></div>

**Ma certitude :** ☐ 1 Je devine  ☐ 2 J'hésite  ☐ 3 Je pense avoir juste  ☐ 4 Je peux expliquer

**Mon contrôle :** ........................................................................................................

## Question 2

Tracer puis donner la valeur finale de `s` :

```python
s = 0
for i in range(4):
    s = s + i
```

<div class="answer"></div>

**Ma certitude :** ☐ 1 Je devine  ☐ 2 J'hésite  ☐ 3 Je pense avoir juste  ☐ 4 Je peux expliquer

**Mon contrôle :** ........................................................................................................


## Notions de cours

### Boucle bornée

```python
for i in range(3):
    print(i)
```

produit `0`, `1`, `2`. La borne supérieure est exclue.

### Boucle non bornée

```python
while condition:
    # corps
```

Elle convient lorsque le nombre de répétitions n’est pas connu à l’avance. Il faut identifier un **variant** qui évolue vers l’arrêt.

### Schémas de base

- compteur : `compteur += 1` ;
- accumulateur : `somme += valeur` ;
- recherche d’extremum : initialiser avec le premier élément, puis comparer ;
- parcours : traiter chaque élément exactement une fois.



## Activité commune - prévoir avant d’exécuter

```python
s = 0
for i in range(1, 4):
    s = s + i
```

| Tour | `i` | `s` avant | `s` après |
|---:|---:|---:|---:|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |

### Choisir la boucle

| Situation | `for` ou `while` ? | Justification |
|---|---|---|
| parcourir une liste |  |  |
| demander un mot de passe jusqu’à réussite |  |  |
| afficher 10 nombres |  |  |
| lire des valeurs jusqu’au mot `fin` |  |  |



## Parcours Fondations - Ahmad

1. Écrire les valeurs de `i` pour `range(5)`, `range(2, 6)` et `range(10, 3, -2)`.
2. Compléter un programme qui calcule la somme de `1` à `n`.
3. Compter le nombre de valeurs positives d’une liste.
4. Calculer le maximum sans utiliser `max`.
5. Corriger une boucle `while` qui ne se termine jamais.

## Parcours Fiabilisation - Ahmed

1. Écrire une fonction de test manuel pour vérifier une somme cumulée.
2. Calculer simultanément somme, effectif, minimum et maximum en un seul parcours.
3. Traiter proprement la liste vide.
4. Expliquer un invariant du calcul de somme.
5. Écrire une boucle `while` dont le variant est explicite.


# Plan de code ou pseudo-code

<div class="answer-lg"></div>

# Tests prévus avant exécution

| Test | Entrée | Résultat attendu | Résultat obtenu | Validé |
|---:|---|---|---|:---:|
| 1 |  |  |  | ☐ |
| 2 |  |  |  | ☐ |
| 3 |  |  |  | ☐ |
| 4 |  |  |  | ☐ |

# Journal de débogage

| Symptôme observé | Hypothèse | Modification testée | Résultat |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

# Trace écrite personnelle

<div class="answer-lg"></div>

# Exit ticket

1. Une construction Python que je sais utiliser :

<div class="answer"></div>

2. Un test qui m’a aidé :

<div class="answer"></div>

**Ma certitude :** ☐ 1 Je devine  ☐ 2 J'hésite  ☐ 3 Je pense avoir juste  ☐ 4 Je peux expliquer

**Mon contrôle :** ........................................................................................................
