# Terminale NSI — Séance 2 — Fiche élève
## Types construits : tableaux, dictionnaires, mutabilité

**Ton objectif de séance :** savoir dire, avant d'écrire, si une instruction **modifie** un
objet ou en **construit** un nouveau.

### Règle de travail

- Je prédis, puis j'exécute, puis je compare.
- J'écris ma prédiction **avant** de lancer le programme.
- Certitude : $\square$1 $\square$2 $\square$3 $\square$4 · Aide : A, B, C, D ou E.

---

## Contrôle d'entrée (séance 1)

Convertis 0x2A en base 10, puis 60 en hexadécimal.

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4

---

## Partie 1 — Prédire, puis exécuter

**Question 0.** Que va afficher ce programme ?

```python
L = [1, 2, 3]
L = L.append(4)
print(L)
```

Ma prédiction : ..................................................  Certitude : $\square$1 $\square$2 $\square$3 $\square$4

Sortie réelle : ..................................................

Ce que je constate : .....................................................................

Et celui-ci ?

```python
L = [1, 2, 3]
L.append(4)
print(L)
```

Ma prédiction : ....................  Sortie réelle : ....................

**La différence, avec mes mots :** .........................................................

....................................................................................................

---

## Partie 2 — La trace écrite

> **Indexation.** Les indices commencent à **0**. Pour n éléments, le dernier indice valide
> est $n - 1$. L'indice $- 1$ désigne le dernier élément. `L[n]` lève une `IndexError`.
>
> **Modifier ou construire.**
>
> | Écriture | Effet | Ce qu'elle renvoie |
> |---|---|---|
> | `L.append(x)` | modifie L | `None` |
> | `L.insert(i, x)` | modifie L | `None` |
> | `L.sort()` | modifie L | `None` |
> | `L + [x]` | ne modifie rien | une nouvelle liste |
> | `sorted(L)` | ne modifie rien | une nouvelle liste |
>
> **Donc `L = L.append(4)` détruit la liste** : L reçoit `None`.
>
> **Dictionnaires.** `d[cle]` accède · `d[cle] = v` crée ou remplace · `del d[cle]` supprime
> · `d.get(cle, defaut)` évite l'erreur · `d.items()` parcourt les couples.

---

## Partie 3 — Entraînement

### Parcours consolidation (exercices 1 à 4)

**Exercice 1.** Soit `L = [5, 7, 9, 11]`. Que valent `L[0]`, `L[3]` et `L[-1]` ? Que provoque
`L[4]` ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Soit `L = [1, 2, 3]`. Après `L.insert(0, 9)` puis `L.append(4)`, que contient
L ? Et que vaudrait L après `L = L.append(5)` ?

Prédiction : ....................  Sortie réelle : ....................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Soit `d = {'x': 10, 'y': 20}`. Que vaut `d['y']` ? Que se passe-t-il avec
`d['z']` ? Comment obtenir 0 dans ce cas, sans erreur ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 4.** Écris les instructions qui ajoutent à `d` la clé `'z'` de valeur 30,
suppriment la clé `'x'`, puis parcourent `d` en affichant chaque couple clé-valeur.

```python





```

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

### Parcours maîtrise (exercices 3 à 6)

**Exercice 5.** Soit `L = [3, 1, 2]`. Prédis puis vérifie la valeur de `L` et de `M` après :

```python
M = sorted(L)
```
puis après :
```python
L.sort()
```

Prédictions : ....................................................................

Sorties réelles : ..................................................................

**Exercice 6.** Écris une fonction `effectifs(mots)` qui prend une liste de mots et renvoie
un dictionnaire associant à chaque mot son nombre d'occurrences. Ajoute deux tests.

```python
def effectifs(mots):
    ...








# Tests
# effectifs(['a', 'b', 'a']) doit valoir ...............
# effectifs([]) doit valoir ...............
```

### Parcours approfondissement (exercices 6 à 8)

**Exercice 7.** Implémente une **pile** avec une liste : écris `empiler(p, x)` et `depiler(p)`.
Que doit renvoyer `depiler` sur une pile vide ? Justifie ton choix.

```python












```

**Exercice 8.** Un arbre binaire est décrit par un dictionnaire à trois clés : `'valeur'`,
`'gauche'`, `'droite'` (avec `None` pour une branche absente). Écris une fonction `somme(a)`
qui renvoie la somme de toutes les valeurs de l'arbre.

*Indication : la fonction devra s'appeler elle-même. Ce n'est pas encore au programme — essaie
quand même.*

```python



```

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

---

## Partie 4 — Ce que la Terminale en fera

Exécute ces trois blocs :

```python
# Une pile : dernier entre, premier sorti
pile = []
pile.append(1)
pile.append(2)
sommet = pile.pop()      # vaut ...........

# Une file : premier entre, premier sorti
file = []
file.append(1)
file.append(2)
premier = file.pop(0)    # vaut ...........

# Un arbre binaire decrit par un dictionnaire
arbre = {
    'valeur': 5,
    'gauche': {'valeur': 3, 'gauche': None, 'droite': None},
    'droite': {'valeur': 8, 'gauche': None, 'droite': None},
}
print(arbre['gauche']['valeur'])   # affiche ...........
```

> Une pile, une file, un arbre, un graphe ne sont pas de nouveaux objets Python : ce sont des
> **usages conventionnés** des listes et des dictionnaires.
>
> Ce que tu sais faire aujourd'hui, tu le feras toute l'année — sous d'autres noms.

---

## Partie 5 — Bilan de séance

**Ce que j'ai compris aujourd'hui :** ......................................................

....................................................................................................

**La différence entre modifier et construire, avec mes mots :** .............................

....................................................................................................

**Ma certitude sur les types construits, aujourd'hui :** $\square$1 $\square$2 $\square$3 $\square$4

**Aide maximale utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune
