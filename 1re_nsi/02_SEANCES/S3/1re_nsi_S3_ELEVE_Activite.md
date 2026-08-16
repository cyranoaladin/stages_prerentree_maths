---
title: "Fiche élève S3 - Fonctions, contrats, tests et débogage"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
<div class="cover">
<img src="logo_slogan_nexus.png" alt="Nexus Réussite">
<div class="kicker">Pré-rentrée 2026-2027</div>
<h1>Séance 3 - Cahier élève</h1>
<div class="subtitle">Fonctions, contrats, tests et débogage</div>
<div class="meta">5 séances de 2 heures - 10 heures<br>Python 3 - théorie, pratique, tests et projet<br>Nom : ........................................................</div>
</div><div class="student-only"></div>
# Mes objectifs

- [ ] distinguer paramètre et argument ;
- [ ] distinguer print, return et None ;
- [ ] comprendre la portée locale ;
- [ ] documenter une fonction ;
- [ ] écrire des assertions de test ;

# Rituel sans ordinateur

## Question 1

Que vaut `r` après l’exécution ?

```python
def double(x):
    print(2 * x)

r = double(5)
```

<div class="answer"></div>

**Ma certitude :** ☐ 1 Je devine  ☐ 2 J'hésite  ☐ 3 Je pense avoir juste  ☐ 4 Je peux expliquer

**Mon contrôle :** ........................................................................................................

## Question 2

Dans `def aire_disque(rayon):`, distinguer le paramètre, l’argument dans `aire_disque(3)` et la valeur renvoyée.

<div class="answer"></div>

**Ma certitude :** ☐ 1 Je devine  ☐ 2 J'hésite  ☐ 3 Je pense avoir juste  ☐ 4 Je peux expliquer

**Mon contrôle :** ........................................................................................................


## Notions de cours

```python
def carre(n: int) -> int:
    """Renvoie le carré de n."""
    return n * n
```

- `n` est un paramètre ;
- dans `carre(5)`, `5` est l’argument ;
- `return` termine la fonction et transmet une valeur ;
- `print` affiche mais ne renvoie pas cette valeur ;
- sans `return`, Python renvoie `None` ;
- les variables créées dans la fonction sont locales.

### Contrat

- précondition : ce qui doit être vrai avant l’appel ;
- postcondition : ce qui est garanti après l’appel ;
- `assert` peut vérifier une condition ;
- un jeu de tests ne prouve pas l’absence de bugs, mais il réduit le risque.



## Activité commune - prédire les retours

```python
def f(x):
    print(x + 1)

resultat = f(4)
```

1. Qu’est-ce qui est affiché ?
2. Que vaut `resultat` ?
3. Comment modifier `f` pour renvoyer 5 ?

### Conception de tests

Pour une fonction `maximum_deux(a, b)`, proposer :

- un cas ordinaire ;
- un cas où `a == b` ;
- un cas avec deux valeurs négatives.



## Parcours Fondations - Ahmad

1. Écrire `est_pair(n)`.
2. Écrire `maximum_deux(a, b)`.
3. Écrire `compte_occurrences(valeurs, cible)`.
4. Ajouter une docstring à chaque fonction.
5. Écrire deux assertions par fonction.

## Parcours Fiabilisation - Ahmed

1. Écrire une précondition pour une fonction de moyenne.
2. Choisir le comportement sur liste vide : assertion ou `None`, et le justifier.
3. Écrire des tests limites et invalides.
4. Corriger une fonction qui modifie une variable globale.
5. Lire la documentation de `math.isclose` et l’utiliser pour tester un flottant.


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
