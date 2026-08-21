# Terminale NSI — Mini-diagnostic pratique (Élève)
## À passer en séance 3, sur machine — 20 minutes

Le positionnement initial mesurait des **connaissances**. Cette épreuve mesure autre chose :
ta capacité à écrire un programme **qui tourne**, et à le vérifier.

Elle n'est pas notée.

### Consignes

- Je fais une **table de trace** avant d'exécuter, pour chaque exercice.
- J'accompagne chaque fonction d'une spécification et de **deux** tests.
- Je déclare ma certitude : ☐1 ☐2 ☐3 ☐4.
- Si je ne sais pas, je laisse vide.

**Nom :** ..............................................  **Date :** ......................

---

## Exercice 1 — Prédire une sortie

Sans exécuter, prédis les deux sorties.

```python
def ajoute(L, x):
    L.append(x)

M = [1, 2]
r = ajoute(M, 3)
print(r)
print(M)
```

Prédiction pour `r` : ....................  Prédiction pour `M` : ....................

**Puis exécute.** Sorties réelles : ....................  et  ....................

Écart avec ma prédiction : ☐aucun ☐oui, sur : ..............................

Certitude : ☐1 ☐2 ☐3 ☐4

---

## Exercice 2 — Table de trace

```python
s = 0
for i in range(2, 9, 3):
    s = s + i
```

Remplis la table **avant** d'exécuter.

| tour | i | s après |
|---:|---:|---:|
| 1 | | |
| 2 | | |
| 3 | | |

Valeur finale de `s` : ....................

Vérifiée par exécution : ☐oui ☐non   Certitude : ☐1 ☐2 ☐3 ☐4

---

## Exercice 3 — Écrire une fonction

Écris `compte_pairs(L)` qui prend une liste d'entiers et renvoie le nombre d'entiers pairs
qu'elle contient. Ajoute une spécification et deux tests, dont un cas limite.

```python
def compte_pairs(L):
    """..............................................................."""


# Tests
assert compte_pairs(..........) == ..........
assert compte_pairs(..........) == ..........
```

Mes tests passent : ☐oui ☐non   Certitude : ☐1 ☐2 ☐3 ☐4

---

## Exercice 4 — Déboguer

Cette fonction devrait renvoyer le plus grand élément d'une liste non vide. Elle est fausse.

```python
def maximum(L):
    plus_grand = 0
    for element in L:
        if element > plus_grand:
            plus_grand = element
    return plus_grand
```

a) Trouve un appel pour lequel elle renvoie un résultat faux.

....................................................................................................

b) Où est l'erreur ?

....................................................................................................

c) Corrige-la.

```python

```

Certitude : ☐1 ☐2 ☐3 ☐4

---

## Exercice 5 — Dictionnaire

Écris `effectifs(mots)` qui prend une liste de mots et renvoie un dictionnaire associant à
chaque mot son nombre d'occurrences.

```python
def effectifs(mots):
    """..............................................................."""


# Tests
assert effectifs(['a', 'b', 'a']) == ..........................
assert effectifs([]) == ..........................
```

Mes tests passent : ☐oui ☐non   Certitude : ☐1 ☐2 ☐3 ☐4

---

## Mon auto-positionnement

| Affirmation | Pas encore | Avec aide | Seul | Je peux expliquer |
|---|:---:|:---:|:---:|:---:|
| Je prédis une sortie avant d'exécuter | ☐ | ☐ | ☐ | ☐ |
| Je fais une table de trace | ☐ | ☐ | ☐ | ☐ |
| Je distingue valeur renvoyée et effet de bord | ☐ | ☐ | ☐ | ☐ |
| J'écris une spécification | ☐ | ☐ | ☐ | ☐ |
| J'écris deux tests, dont un cas limite | ☐ | ☐ | ☐ | ☐ |
| Je trouve un contre-exemple à un programme faux | ☐ | ☐ | ☐ | ☐ |
