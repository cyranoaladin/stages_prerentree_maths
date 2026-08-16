---
title: "Mémento Python Première NSI"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
<div class="cover">
<img src="logo_slogan_nexus.png" alt="Nexus Réussite">
<div class="kicker">Pré-rentrée 2026-2027</div>
<h1>Mémento Python</h1>
<div class="subtitle">Première NSI - référence de l’élève</div>
<div class="meta">5 séances de 2 heures - 10 heures<br>Python 3 - théorie, pratique, tests et projet<br>Syntaxe, méthodes, tests et erreurs fréquentes</div>
</div>
# 1. Lire un programme

Python exécute les instructions dans l’ordre, sauf lorsqu’une condition, une boucle ou un appel de fonction modifie le flux.

```python
x = 3          # affectation
x = x + 1      # évalue x + 1 puis remplace x
x == 4         # comparaison, renvoie True ou False
```

# 2. Types et conversions

| Type | Exemple | Conversion |
|---|---|---|
| entier | `12` | `int("12")` |
| flottant | `2.5` | `float("2.5")` |
| chaîne | `"NSI"` | `str(12)` |
| booléen | `True` | `bool(expression)` |
| absence | `None` | pas de conversion usuelle |

Attention : `input()` renvoie toujours une chaîne.

# 3. Opérateurs

- calcul : `+ - * / // % **` ;
- comparaison : `== != < <= > >=` ;
- logique : `and or not` ;
- appartenance : `in`, `not in`.

# 4. Conditions

```python
if condition:
    ...
elif autre_condition:
    ...
else:
    ...
```

Négations utiles :

| Condition | Négation |
|---|---|
| `x > a` | `x <= a` |
| `x >= a` | `x < a` |
| `A and B` | `(not A) or (not B)` |
| `A or B` | `(not A) and (not B)` |

# 5. Boucles

## `for`

```python
for i in range(debut, fin, pas):
    ...
```

La valeur `fin` est exclue.

## `while`

```python
while condition:
    ...
```

Vérifier que la condition peut devenir fausse.

## Schémas

```python
compteur = 0
somme = 0
for valeur in valeurs:
    if valeur > 0:
        compteur += 1
    somme += valeur
```

# 6. Fonctions

```python
def moyenne(valeurs: list[float]) -> float:
    """Renvoie la moyenne d'une liste non vide."""
    assert len(valeurs) > 0
    return sum(valeurs) / len(valeurs)
```

- paramètre : nom dans la définition ;
- argument : valeur donnée à l’appel ;
- `return` : valeur transmise ;
- sans `return` : résultat `None` ;
- variable locale : créée dans la fonction.

# 7. Tests

```python
assert est_pair(4) is True
assert est_pair(5) is False
assert maximum_deux(-3, -7) == -3
```

Tester : cas ordinaire, borne, égalité, vide ou invalide selon le contrat.

# 8. Chaînes, tuples et listes

```python
texte = "python"
texte[0]          # 'p'

point = (3, 5)    # tuple

L = [4, 8, 15]
L[0]              # 4
L[-1]             # 15
len(L)            # 3
L.append(16)
```

Compréhension :

```python
carres = [x*x for x in L if x >= 0]
```

# 9. Mutation et copie

```python
a = [1, 2]
b = a             # alias
c = a.copy()      # copie superficielle
```

Modifier `b` modifie `a`, mais pas `c`.

# 10. Dictionnaires

```python
mesure = {"id": "C01", "temperature": 28.4}
mesure["temperature"]
mesure["statut"] = "OK"

for cle, valeur in mesure.items():
    print(cle, valeur)
```

# 11. CSV

```python
import csv

with open("mesures_capteurs.csv", encoding="utf-8", newline="") as fichier:
    lignes = list(csv.DictReader(fichier))
```

Les valeurs sont des chaînes : convertir avant de calculer.

# 12. Algorithmes essentiels

## Recherche séquentielle

```python
def indice_de(valeurs, cible):
    for i in range(len(valeurs)):
        if valeurs[i] == cible:
            return i
    return None
```

## Maximum

```python
def maximum(valeurs):
    assert len(valeurs) > 0
    meilleur = valeurs[0]
    for valeur in valeurs[1:]:
        if valeur > meilleur:
            meilleur = valeur
    return meilleur
```

## Dichotomie

Nécessite une liste triée. À chaque tour, élimine environ la moitié de la zone restante.

# 13. Erreurs fréquentes

| Erreur | Symptôme | Correction |
|---|---|---|
| `=` au lieu de `==` | syntaxe ou mauvaise intention | `=` affecte, `==` compare |
| borne de `range` | un tour en moins | écrire les valeurs produites |
| index à partir de 1 | mauvais élément | premier indice 0 |
| `len(L)` | confusion avec dernier indice | dernier indice `len(L)-1` |
| oubli de `return` | résultat `None` | ajouter `return` si une valeur est attendue |
| accumulateur mal initialisé | somme fausse | initialiser avant la boucle |
| liste vide | erreur au premier élément | définir un contrat |
| aliasing | modification inattendue | utiliser `copy()` si nécessaire |
| CSV non converti | concaténation de chaînes | convertir avec `int`/`float` |

# 14. Checklist avant de rendre un programme

- [ ] noms explicites ;
- [ ] fonctions courtes ;
- [ ] docstrings ;
- [ ] aucun code dupliqué ;
- [ ] cas limites traités ;
- [ ] tests exécutés ;
- [ ] sorties lisibles ;
- [ ] aucun affichage de débogage inutile ;
- [ ] programme expliqué oralement.
