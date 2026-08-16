---
title: "Fiche élève S4 - Listes, tuples, dictionnaires et tables CSV"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
<div class="cover">
<img src="logo_slogan_nexus.png" alt="Nexus Réussite">
<div class="kicker">Pré-rentrée 2026-2027</div>
<h1>Séance 4 - Cahier élève</h1>
<div class="subtitle">Listes, tuples, dictionnaires et tables CSV</div>
<div class="meta">5 séances de 2 heures - 10 heures<br>Python 3 - théorie, pratique, tests et projet<br>Nom : ........................................................</div>
</div><div class="student-only"></div>
# Mes objectifs

- [ ] maîtriser indexation et longueur ;
- [ ] comprendre mutation et aliasing ;
- [ ] utiliser listes et dictionnaires ;
- [ ] importer une table CSV ;
- [ ] filtrer, trier et contrôler des données ;

# Rituel sans ordinateur

## Question 1

Pour `L = [4, 8, 15, 16]`, donner `L[1]`, `len(L)` et le dernier indice.

<div class="answer"></div>

**Ma certitude :** ☐ 1 Je devine  ☐ 2 J'hésite  ☐ 3 Je pense avoir juste  ☐ 4 Je peux expliquer

**Mon contrôle :** ........................................................................................................

## Question 2

Prédire la valeur de `a` :

```python
a = [1, 2]
b = a
b.append(3)
```

<div class="answer"></div>

**Ma certitude :** ☐ 1 Je devine  ☐ 2 J'hésite  ☐ 3 Je pense avoir juste  ☐ 4 Je peux expliquer

**Mon contrôle :** ........................................................................................................


## Notions de cours

### Listes

- premier élément : `L[0]` ;
- dernier élément : `L[-1]` ;
- longueur : `len(L)` ;
- ajout : `L.append(x)` ;
- parcours : `for valeur in L:` ;
- compréhension : `[x*x for x in L if x >= 0]`.

### Alias

```python
a = [1, 2]
b = a
b.append(3)
```

`a` et `b` désignent la même liste. Pour une copie superficielle : `b = a.copy()`.

### Dictionnaires

```python
mesure = {"id": "C01", "temperature": 28.4}
```

Parcours : `for cle, valeur in mesure.items():`.

### CSV

La bibliothèque standard `csv` permet d’importer une table. Chaque ligne peut devenir un dictionnaire avec `csv.DictReader`.



## Activité commune - index, longueur et mutation

```python
L = [4, 8, 15, 16]
```

| Expression | Valeur |
|---|---|
| `L[0]` |  |
| `L[1]` |  |
| `len(L)` |  |
| `L[len(L)-1]` |  |

### Alias

Prédire puis exécuter :

```python
a = [1, 2]
b = a
b.append(3)
print(a)
```

Expliquer le résultat.



## Parcours Fondations - Ahmad

1. Corriger cinq expressions d’indexation.
2. Écrire une boucle qui double chaque valeur sans modifier la liste d’origine.
3. Construire un dictionnaire décrivant une mesure.
4. Parcourir `keys`, `values` et `items`.
5. Importer `mesures_capteurs.csv` et afficher les identifiants.

## Parcours Fiabilisation - Ahmed

1. Démontrer un effet d’aliasing et le corriger.
2. Construire une compréhension filtrant les alertes.
3. Valider chaque ligne du CSV.
4. Détecter un identifiant dupliqué.
5. Trier les mesures par température puis par identifiant.


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
