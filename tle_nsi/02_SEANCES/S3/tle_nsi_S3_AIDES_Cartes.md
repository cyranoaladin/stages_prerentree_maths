# Terminale NSI — Séance 3 — Cartes d'aide
## Programmation

---

### Carte A — Rappel de syntaxe et de propriété

> Sans `return`, une fonction renvoie `None`.
> Modifier un argument mutable et renvoyer une valeur sont **indépendants**.
> `range(a, b, p)` : borne supérieure **exclue**.
> Une variable créée dans une fonction est locale.
> `assert expression` n'affiche rien si l'expression est vraie, et arrête le programme sinon.

---

### Carte B — Première ligne écrite

> Pour `somme_jusqua(n)` :
> ```python
> def somme_jusqua(n):
>     total = 0
>     for i in range(1, ..........):
>         ...
>     return total
> ```
> À toi : quelle borne mettre pour que `n` soit **inclus** ? Que faire dans la boucle ?

---

### Carte C — Exemple exécuté à transposer

> **Exemple.** Somme des carrés de 1 à n.
> ```python
> def somme_carres(n):
>     """Prend un entier n >= 0, renvoie 1^2 + 2^2 + ... + n^2."""
>     total = 0
>     for i in range(1, n + 1):
>         total = total + i * i
>     return total
>
> assert somme_carres(3) == 14   # 1 + 4 + 9
> assert somme_carres(0) == 0    # cas limite
> ```
> Trois points clés : l'accumulateur est initialisé **avant** la boucle ; la borne est
> `n + 1` pour inclure n ; il y a **deux** tests, dont un cas limite.
>
> **À toi de transposer**, en gardant ces trois points.

---

### Carte D — Découpage en quatre questions

> 1. Quelle valeur ta fonction doit-elle **renvoyer** ? (Si la réponse est « rien », il n'y a
>    pas de `return`.)
> 2. As-tu besoin d'un accumulateur ? Où l'initialises-tu — avant ou dans la boucle ?
> 3. Sur quelles valeurs boucles-tu ? Écris-les toutes avant de coder.
> 4. Quels sont tes deux tests, dont un cas limite ?

---

### Carte E — Squelette de code à compléter

> ```python
> def somme_jusqua(n):
>     """Prend un entier n >= 0, renvoie .................................."""
>     total = ..........
>     for i in range(.........., ..........):
>         total = ..........
>     return ..........
>
> assert somme_jusqua(4) == ..........
> assert somme_jusqua(0) == ..........
> ```
>
> ```python
> def maximum(L):
>     """Prend une liste non vide, renvoie .................................."""
>     plus_grand = L[..........]
>     for element in L:
>         if element > ..........:
>             plus_grand = ..........
>     return ..........
> ```

---

## Carte « contrôle » — à utiliser avant toute certitude de 4

> - J'ai rempli ma table de trace **avant** d'exécuter.
> - Ma prédiction et la sortie réelle coïncident.
> - Mon accumulateur est initialisé **avant** la boucle, pas dedans.
> - Ma fonction a une spécification et deux tests, dont un cas limite.
> - Je sais dire ce qu'elle renvoie **et** ce qu'elle modifie.

---

## Carte « erreurs fréquentes » — à distribuer en fin de séance

> 1. Croire qu'une fonction sans `return` « ne fait rien » : elle peut très bien avoir modifié
>    une liste.
> 2. Croire qu'une fonction qui modifie une liste la renvoie : non, elle renvoie `None`.
> 3. Initialiser l'accumulateur **dans** la boucle : il est remis à zéro à chaque tour.
> 4. Oublier le `+ 1` dans `range(1, n + 1)` : la dernière valeur manque.
> 5. Écrire une boucle qui ne s'exécute jamais : `range(5, 5)` et `range(4, 1)` produisent
>    zéro tour, sans aucune erreur affichée.
