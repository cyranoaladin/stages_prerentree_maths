# Terminale NSI — Séance 3 — Fiche élève
## Programmation : fonctions, retour, portée, boucles

**Ton objectif de séance :** savoir dire, pour n'importe quelle fonction, ce qu'elle
**renvoie** et ce qu'elle **modifie** — ce sont deux questions différentes.

### Règle de travail

- J'écris ma prédiction **avant** d'exécuter.
- Je fais une table de trace avant de lancer une boucle.
- Chaque fonction que j'écris a une spécification et **deux** tests.
- Certitude : $\square$1 $\square$2 $\square$3 $\square$4 · Aide : A, B, C, D ou E.

---

## Contrôle d'entrée (séance 2)

Soit `L = [1, 2, 3]`. Que contient L après `L.insert(0, 9)` puis `L.append(4)` ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4

---

## Partie 1 — Prédire, puis exécuter

**Question 0.**

```python
def h(L):
    L.append(0)

M = [1, 2]
r = h(M)
print("r vaut :", r)
print("M vaut :", M)
```

Ma prédiction pour `r` : ....................  Certitude : $\square$1 $\square$2 $\square$3 $\square$4

Ma prédiction pour `M` : ....................  Certitude : $\square$1 $\square$2 $\square$3 $\square$4

Sorties réelles : $r =$ ....................  $M =$ ....................

**Ce que je constate :** ...................................................................

....................................................................................................

---

## Partie 2 — La trace écrite

> **Renvoyer et modifier sont deux choses différentes.**
>
> | Fonction | Renvoie | Modifie l'argument |
> |---|---|---|
> | `def f(x): return x * 2` | une valeur | non |
> | `def g(L): L.append(0)` | `None` | oui |
> | `def h(L): L.append(0); return L` | une valeur | oui |
> | `def k(x): print(x)` | `None` | non |
>
> **Sans `return`, une fonction renvoie `None`** — même si elle a fait beaucoup de choses.
>
> **Portée.** Une variable créée dans une fonction disparaît à la fin de l'appel.
>
> **Bornes de `range`.** La borne supérieure est **exclue**.
>
> | Écriture | Valeurs | Tours |
> |---|---|---:|
> | `range(3)` | 0, 1, 2 | 3 |
> | `range(1, 4)` | 1, 2, 3 | 3 |
> | `range(2, 10, 3)` | 2, 5, 8 | 3 |
>
> **Table de trace.** Avant d'exécuter, j'écris l'état des variables tour par tour.

---

## Partie 3 — Entraînement

### Parcours consolidation (exercices 1 à 4)

**Exercice 1.** Soit `def g(n): return n*n + 1`. Que renvoie `g(4)` ? Que vaut `g(g(1))` ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Combien d'itérations effectue `for i in range(2, 10, 3)` ? Quelles valeurs
prend `i` ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Soit `s = 0` puis `for i in range(1, 6): s = s + i*i`. Remplis la table de
trace, **puis** vérifie par exécution.

| tour | i | i*i | s après |
|---:|---:|---:|---:|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

Valeur finale de s : ....................  Vérifiée par exécution : $\square$oui $\square$non

**Exercice 4.** Écris une fonction `somme_jusqua(n)` qui renvoie 1 + 2 + … + n. Ajoute une
spécification et deux tests.

```python
def somme_jusqua(n):
    """..............................................................."""










# Tests
assert somme_jusqua(....) == ....
assert somme_jusqua(....) == ....
```

### Parcours maîtrise (exercices 3 à 6)

**Exercice 5.** Cette fonction contient une erreur. Trouve-la **par une table de trace**,
avant d'exécuter.

```python
def moyenne(notes):
    for note in notes:
        total = 0
        total = total + note
    return total / len(notes)
```

L'erreur : ........................................................................

La correction : ...................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**Exercice 6.** Écris `maximum(L)` qui renvoie le plus grand élément d'une liste **non vide**,
sans utiliser `max`. Spécifie et teste. Que devrait faire ta fonction sur une liste vide ?

```python










```

### Parcours approfondissement (exercices 6 à 8)

**Exercice 7.** Écris `normaliser(L)` qui divise chaque élément d'une liste de nombres par le
maximum, **sans modifier L** et en renvoyant une nouvelle liste. Puis écris
`normaliser_en_place(L)` qui fait la même chose **en modifiant L** et sans rien renvoyer.
Écris deux tests pour chacune.

```python










```

**Exercice 8.** Que renvoie et que modifie chacune de ces fonctions ? Réponds **avant**
d'exécuter, puis vérifie.

```python
def a(L):
    L = L + [0]

def b(L):
    L += [0]

def c(L):
    return L + [0]
```

| Fonction | Renvoie | Modifie L | Pourquoi |
|---|---|---|---|
| `a` | | | |
| `b` | | | |
| `c` | | | |

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

---

## Partie 4 — Ce que la Terminale en fera

> Une fonction **récursive** s'appelle elle-même. Elle renvoie une valeur construite à partir
> de la valeur renvoyée par l'appel suivant :
>
> ```python
> def factorielle(n):
>     if n == 0:
>         return 1
>     return n * factorielle(n - 1)
> ```
>
> Sans un `return` net à chaque branche, ce mécanisme ne fonctionne pas : la fonction
> renverrait `None`, et le calcul échouerait.
>
> C'est pour cela que la valeur de retour devait être sûre aujourd'hui.
>
> La **mise au point** et la **modularité**, également au programme de Terminale, reposent sur
> la spécification et les tests que tu as écrits pendant cette séance.

---

## Partie 5 — Bilan de séance

**Ce que j'ai compris aujourd'hui :** ......................................................

....................................................................................................

**La différence entre renvoyer et modifier, avec mes mots :** ...............................

....................................................................................................

**Ma certitude en programmation, aujourd'hui :** $\square$1 $\square$2 $\square$3 $\square$4

**Aide maximale utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune
