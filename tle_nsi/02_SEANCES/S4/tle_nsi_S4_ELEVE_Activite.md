# Terminale NSI — Séance 4 — Fiche élève
## Algorithmique : préconditions, recherche, tris, coût

**Ton objectif de séance :** savoir dire à quelle condition un algorithme donne un résultat
juste — et combien il coûte.

### Règle de travail

- J'écris la **précondition** avant d'utiliser un algorithme.
- Je compte les comparaisons, je ne me contente pas de mesurer une fois.
- Certitude : $\square$1 $\square$2 $\square$3 $\square$4 · Aide : A, B, C, D ou E.

---

## Contrôle d'entrée (séance 3)

Quelles valeurs prend `i` dans `for i in range(1, 10, 4)` ? Combien de tours ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4

---

## Partie 1 — Prédire, puis exécuter

Voici une recherche dichotomique **correctement écrite** :

```python
def recherche_dichotomique(tableau, valeur):
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

**Question 0.** Que renvoie `recherche_dichotomique([4, 1, 9, 3], 4)` ?

*Remarque : la valeur 4 est bien présente dans le tableau, à l'indice 0.*

Ma prédiction : ....................  Ma certitude : $\square$1 $\square$2 $\square$3 $\square$4

Sortie réelle : ....................

Déroule maintenant l'algorithme à la main :

| tour | gauche | droite | milieu | tableau[milieu] | décision |
|---:|---:|---:|---:|---:|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

**Ce que je constate :** ...................................................................

....................................................................................................

**Le programme a-t-il affiché une erreur ?** $\square$oui $\square$non

---

## Partie 2 — La trace écrite

> **Précondition.** La recherche dichotomique exige un tableau **trié**. Sur un tableau non
> trié, elle ne renvoie **pas** d'erreur : elle renvoie un résultat **faux**. C'est le pire
> cas possible pour un programme.
>
> On écrit la précondition dans la spécification, et on peut la vérifier :
> ```python
> assert tableau == sorted(tableau), "le tableau doit etre trie"
> ```
>
> **Coût.**
>
> | Taille | Recherche séquentielle | Dichotomie |
> |---:|---:|---:|
> | 16 | 16 | 4 |
> | 1 000 | 1 000 | 10 |
> | 1 000 000 | 1 000 000 | 20 |
>
> Repères : **$2^{10} = 1 024$** et **$2^{20} \approx 1 000 000$**.
>
> **Arbitrage.** Trier puis chercher coûte plus cher qu'une seule recherche séquentielle.
> C'est rentable si l'on fait **beaucoup** de recherches dans le même tableau.

---

## Partie 3 — Entraînement

### Parcours consolidation (exercices 1 à 4)

**Exercice 1.** Peut-on appliquer directement la recherche dichotomique au tableau
`[4, 1, 9, 3]` ? Que faut-il faire avant ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Dans un tableau trié de 1 000 éléments, combien de comparaisons au pire pour
une recherche dichotomique ? Et pour une recherche séquentielle ?

Dichotomie : ....................  Séquentielle : ....................

Justification : ...................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Déroule la recherche dichotomique de la valeur 13 dans le tableau trié
`[1, 3, 5, 7, 9, 11, 13]`.

| tour | gauche | droite | milieu | tableau[milieu] | décision |
|---:|---:|---:|---:|---:|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

Indice renvoyé : ....................  Nombre de comparaisons : ....................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**Exercice 4.** Ajoute la précondition à la spécification de la fonction, puis un `assert`
qui la vérifie.

```python
def recherche_dichotomique(tableau, valeur):
    """....................................................................
    ...................................................................."""
    assert ....................................................................
    ...
```

### Parcours maîtrise (exercices 3 à 6)

**Exercice 5.** Écris `recherche_sequentielle(tableau, valeur)` qui renvoie l'indice de la
valeur, ou $- 1$. Quelle est sa précondition ? Combien de comparaisons au pire ?

```python










```

**Exercice 6.** Déroule le tri par insertion sur `[5, 2, 8, 1]`, en comptant les comparaisons
à chaque étape.

| étape | état du tableau | comparaisons faites |
|---:|---|---:|
| départ | `[5, 2, 8, 1]` | 0 |
| 1 | | |
| 2 | | |
| 3 | | |

Total des comparaisons : ....................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

### Parcours approfondissement (exercices 6 à 8)

**Exercice 7.** On dispose d'un tableau de n éléments non triés et on prévoit d'y faire k
recherches. À partir de quelle valeur de k vaut-il mieux trier d'abord ? Raisonne avec un tri
en $n \log_2 n$ et une dichotomie en $\log_2 n$.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**Exercice 8.** Exécute les deux fonctions, puis chronomètre-les avec le module `time`.

```python
def fibo_naif(n):
    if n <= 1:
        return n
    return fibo_naif(n - 1) + fibo_naif(n - 2)

def fibo_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fibo_memo(n - 1, memo) + fibo_memo(n - 2, memo)
    return memo[n]
```

Temps pour `fibo_naif(32)` : ....................

Temps pour `fibo_memo(32)` : ....................

**D'où vient l'écart ?** ....................................................................

....................................................................................................

---

## Partie 4 — Ce que la Terminale en fera

> **Diviser pour régner.** La dichotomie est un cas particulier d'un schéma général : diviser
> le problème en morceaux, résoudre chaque morceau, recombiner. Le tri fusion en est
> l'exemple canonique.
>
> **Programmation dynamique.** L'exercice 8 en est l'illustration : mémoriser les résultats
> déjà calculés dans un **dictionnaire** — celui de la séance 2 — transforme un calcul
> impraticable en calcul instantané.
>
> **Arbres et graphes.** Les parcours en largeur et en profondeur s'analysent avec exactement
> le même raisonnement sur le coût.

---

## Partie 5 — Bilan de séance

**Ce que j'ai compris aujourd'hui :** ......................................................

....................................................................................................

**Pourquoi un programme faux est plus dangereux qu'un programme qui plante :**

....................................................................................................

**Ma certitude en algorithmique, aujourd'hui :** $\square$1 $\square$2 $\square$3 $\square$4

**Aide maximale utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune
