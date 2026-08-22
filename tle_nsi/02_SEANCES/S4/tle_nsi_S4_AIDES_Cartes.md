# Terminale NSI — Séance 4 — Cartes d'aide
## Algorithmique

---

### Carte A — Rappel de propriété

> **Précondition de la dichotomie :** le tableau doit être **trié**.
> Non respectée, elle ne provoque aucune erreur : le résultat est simplement faux.
>
> **Coûts au pire :** séquentielle n comparaisons ; dichotomie $\log_2 n$.
> Repères : $2^{10} = 1 024 \cdot 2^{20} \approx 1 000 000$.
>
> **Tri par insertion :** de l'ordre de $n^2$ comparaisons au pire.

---

### Carte B — Première ligne écrite

> Pour dérouler la recherche de 13 dans `[1, 3, 5, 7, 9, 11, 13]` :
> ```
> tour 1 : gauche = 0, droite = 6, milieu = (0 + 6) // 2 = 3, tableau[3] = 7
> ```
> À toi : 7 est-il plus petit ou plus grand que 13 ? De quel côté continue-t-on ?
> Que devient `gauche` ou `droite` ?

---

### Carte C — Exemple déroulé à transposer

> **Exemple.** Recherche de 5 dans `[1, 3, 5, 7, 9]`.
>
> | tour | gauche | droite | milieu | tableau[milieu] | décision |
> |---:|---:|---:|---:|---:|---|
> | 1 | 0 | 4 | 2 | 5 | trouvé, on renvoie 2 |
>
> **Exemple.** Recherche de 9 dans `[1, 3, 5, 7, 9]`.
>
> | tour | gauche | droite | milieu | tableau[milieu] | décision |
> |---:|---:|---:|---:|---:|---|
> | 1 | 0 | 4 | 2 | 5 | $5 < 9 \to$ gauche = 3 |
> | 2 | 3 | 4 | 3 | 7 | $7 < 9 \to$ gauche = 4 |
> | 3 | 4 | 4 | 4 | 9 | trouvé, on renvoie 4 |
>
> **À toi de transposer**, en remplissant une ligne par tour et en n'oubliant aucune colonne.

---

### Carte D — Découpage en quatre questions

> **Pour dérouler une dichotomie :**
> 1. Quelles sont les valeurs initiales de `gauche` et `droite` ?
> 2. Que vaut `milieu` à ce tour, et quelle valeur du tableau s'y trouve ?
> 3. Cette valeur est-elle égale, plus petite ou plus grande que celle cherchée ?
> 4. Laquelle des deux bornes se déplace, et à quelle valeur ?
>
> **Pour évaluer un coût :**
> 1. Combien d'éléments au départ ?
> 2. Combien de fois peut-on diviser ce nombre par 2 avant d'arriver à 1 ?
> 3. Compare ce nombre à la taille de départ.

---

### Carte E — Squelette de code à compléter

> ```python
> def recherche_sequentielle(tableau, valeur):
>     """Precondition : ..........................................
>     Renvoie l'indice de valeur dans tableau, ou -1 si absente."""
>     for i in range(..........):
>         if tableau[i] == ..........:
>             return ..........
>     return ..........
>
> # Tests
> assert recherche_sequentielle([4, 1, 9], 9) == ..........
> assert recherche_sequentielle([4, 1, 9], 7) == ..........
> ```

---

## Carte « contrôle » — à utiliser avant toute certitude de 4

> - J'ai écrit la précondition de l'algorithme que j'utilise.
> - J'ai vérifié que mon tableau la respecte.
> - Mon déroulé à la main donne le même résultat que l'exécution.
> - Pour un coût, j'ai raisonné en ordre de grandeur, pas sur une seule mesure.

---

## Carte « erreurs fréquentes » — à distribuer en fin de séance

> 1. Appliquer la dichotomie sans vérifier que le tableau est trié. **Le programme ne
>    prévient pas.**
> 2. Croire qu'un algorithme faux plante : il renvoie un résultat, avec le même aplomb qu'un
>    résultat juste.
> 3. Confondre $\log_2 n$ et n/2 : pour un million d'éléments, c'est 20 contre 500 000.
> 4. Croire qu'il faut toujours trier avant de chercher : cela ne devient rentable qu'à partir
>    d'un certain nombre de recherches.
> 5. Comparer deux algorithmes sur une seule exécution au lieu de compter les opérations.
