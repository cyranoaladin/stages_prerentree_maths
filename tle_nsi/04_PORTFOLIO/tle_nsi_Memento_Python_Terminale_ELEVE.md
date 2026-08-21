# Terminale NSI — Mémento Python
## À conserver toute l'année

Ce mémento reprend exactement ce qui a été travaillé pendant le stage. Il ne contient rien de
plus : c'est un aide-mémoire, pas un cours.

---

## 1. Représentation des données

```python
bin(22)            # '0b10110'
int('10110', 2)    # 22
hex(42)            # '0x2a'
int('2A', 16)      # 42
```

| Hex | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Déc | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |

Un chiffre hexadécimal vaut exactement **quatre bits**. Sur 8 bits : 256 valeurs, de 0 à 255.

**Le contrôle :** je recalcule la valeur décimale de ce que j'ai écrit.

---

## 2. Booléens

Priorités : `not`, puis `and`, puis `or`.

| A | B | `A and B` | `A or B` | `not A` |
|---|---|---|---|---|
| V | V | V | V | F |
| V | F | F | V | F |
| F | V | F | V | V |
| F | F | F | F | V |

**Lois de De Morgan.**
`not (A and B)` = `(not A) or (not B)`
`not (A or B)` = `(not A) and (not B)`

---

## 3. Listes

```python
L = [4, 8, 15, 16]
L[0]        # 4      premier
L[-1]       # 16     dernier
len(L)      # 4
L[4]        # IndexError : le dernier indice valide est 3
L[1:3]      # [8, 15]  tranche, borne de fin exclue
```

**Modifier ou construire — la distinction qui compte :**

| Écriture | Modifie L ? | Renvoie |
|---|:---:|---|
| `L.append(x)` | oui | `None` |
| `L.insert(i, x)` | oui | `None` |
| `L.sort()` | oui | `None` |
| `del L[i]` | oui | — |
| `L.pop()` | oui | l'élément retiré |
| `L + [x]` | non | une nouvelle liste |
| `sorted(L)` | non | une nouvelle liste |

> **Ne jamais affecter le résultat d'une méthode qui modifie en place.**
> `L = L.append(4)` détruit la liste.

---

## 4. Dictionnaires

```python
d = {'x': 10, 'y': 20}
d['x']              # 10
d['z']              # KeyError
d.get('z', 0)       # 0, sans erreur
d['z'] = 30         # cree ou remplace
del d['x']          # supprime
len(d)              # nombre de cles
'y' in d            # True

for cle in d:               # parcourt les cles
    print(cle)
for cle, valeur in d.items():   # parcourt les couples
    print(cle, valeur)
```

**Le motif du comptage**, à connaître par cœur :

```python
resultat[cle] = resultat.get(cle, 0) + 1
```

---

## 5. Fonctions

```python
def moyenne(notes):
    """Prend une liste non vide de nombres, renvoie leur moyenne."""
    return sum(notes) / len(notes)

assert moyenne([10, 20]) == 15
assert moyenne([5]) == 5
```

**Renvoyer et modifier sont indépendants :**

| Fonction | Renvoie | Modifie l'argument |
|---|---|---|
| `def f(x): return x * 2` | une valeur | non |
| `def g(L): L.append(0)` | `None` | oui |
| `def k(x): print(x)` | `None` | non |

**Sans `return`, une fonction renvoie `None`** — même si elle a modifié une liste.

---

## 6. Boucles

```python
range(3)            # 0, 1, 2          -> 3 tours
range(1, 4)         # 1, 2, 3          -> 3 tours
range(2, 10, 3)     # 2, 5, 8          -> 3 tours
range(10, 0, -2)    # 10, 8, 6, 4, 2   -> 5 tours
range(5, 5)         # aucune           -> 0 tour
```

**La borne supérieure est toujours exclue.**

**Motif de l'accumulateur** — l'initialisation est **avant** la boucle :

```python
total = 0
for element in L:
    total = total + element
```

---

## 7. Algorithmique

```python
def recherche_dichotomique(tableau, valeur):
    """Precondition : tableau trie par ordre croissant.
    Renvoie l'indice de valeur, ou -1 si absente."""
    gauche, droite = 0, len(tableau) - 1
    while gauche <= droite:
        milieu = (gauche + droite) // 2
        if tableau[milieu] == valeur:
            return milieu
        if tableau[milieu] < valeur:
            gauche = milieu + 1
        else:
            droite = milieu - 1
    return -1
```

> **Une précondition non respectée ne provoque aucune erreur : elle donne un résultat faux.**

| Taille | Séquentielle | Dichotomie |
|---:|---:|---:|
| 1 000 | 1 000 | 10 |
| 1 000 000 | 1 000 000 | 20 |

Repères : **2¹⁰ = 1 024** · **2²⁰ ≈ 1 000 000**.

---

## 8. Données en tables

```python
import csv

with open('donnees.csv', encoding='utf-8') as fichier:
    table = list(csv.DictReader(fichier))
    # DictReader traite la premiere ligne comme l'en-tete :
    # elle ne compte pas comme enregistrement

retenus = [ligne for ligne in table if int(ligne['note']) > 12]   # selection
projete = [{'nom': l['nom']} for l in retenus]                    # projection
```

| Opération | Ce qu'on garde | SQL |
|---|---|---|
| Sélection | des lignes | `WHERE` |
| Projection | des colonnes | `SELECT` |
| Jointure | deux tables, attribut commun | `JOIN ... ON ...` |

```sql
SELECT nom, note FROM eleves WHERE note > 12 ;
SELECT eleves.nom, classes.professeur
FROM eleves JOIN classes ON eleves.classe = classes.code ;
```

---

## 9. Les cinq contrôles à faire sans y penser

1. **Conversion** : je recalcule la valeur décimale.
2. **Liste** : je sais si l'instruction modifie ou construit.
3. **Boucle** : j'écris les valeurs de `range` avant de coder.
4. **Fonction** : une spécification et deux tests, dont un cas limite.
5. **Algorithme** : j'écris sa précondition et je vérifie qu'elle est respectée.

---

## 10. Ce qui arrive en Terminale

| Chapitre | Ce sur quoi il s'appuie |
|---|---|
| Structures de données (piles, files, arbres, graphes) | listes et dictionnaires |
| Bases de données et SQL | sélection, projection, jointure |
| Récursivité, modularité | valeur de retour, spécification, tests |
| Diviser pour régner, programmation dynamique | dichotomie, raisonnement sur le coût |
| Processus, ordonnancement, réseaux | architecture, systèmes |
| Sécurisation des communications | représentation binaire |

**Rien n'y part de zéro.**
