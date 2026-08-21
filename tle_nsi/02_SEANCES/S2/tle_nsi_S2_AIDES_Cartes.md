# Terminale NSI — Séance 2 — Cartes d'aide
## Types construits

---

### Carte A — Rappel de syntaxe et de propriété

> Indices de 0 à n − 1 ; `L[-1]` est le dernier élément.
> `append`, `insert`, `sort`, `del` **modifient** et renvoient `None`.
> `L + [x]` et `sorted(L)` **construisent** un nouvel objet.
> `d[cle]` lève `KeyError` si la clé est absente ; `d.get(cle, defaut)` ne lève rien.

---

### Carte B — Première ligne écrite

> Pour compter les occurrences de mots :
> ```python
> def effectifs(mots):
>     resultat = {}
>     for mot in mots:
>         ...
>     return resultat
> ```
> À toi : dans la boucle, que faire si `mot` est déjà une clé de `resultat` ? Et sinon ?
> *Indication : `resultat.get(mot, 0)` renvoie 0 quand la clé est absente.*

---

### Carte C — Exemple exécuté à transposer

> **Exemple.** Compter les lettres d'un mot.
> ```python
> def compter_lettres(mot):
>     resultat = {}
>     for lettre in mot:
>         resultat[lettre] = resultat.get(lettre, 0) + 1
>     return resultat
>
> print(compter_lettres('abracadabra'))
> # {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}
> ```
> Le point clé : `resultat.get(lettre, 0)` renvoie 0 la première fois, puis la valeur
> accumulée. Aucun test `if` n'est nécessaire.
>
> **À toi de transposer** à une liste de mots plutôt qu'à une chaîne de caractères.

---

### Carte D — Découpage en trois questions

> **Pour une fonction sur un dictionnaire :**
> 1. Quel dictionnaire vide dois-tu créer avant la boucle ?
> 2. Sur quoi boucles-tu — les éléments, ou les indices ?
> 3. À l'intérieur, comment mets-tu à jour la valeur associée à la clé courante ?
>
> **Pour une pile :**
> 1. Quelle liste représente la pile ?
> 2. Empiler, c'est ajouter **où** ?
> 3. Dépiler, c'est retirer **où** ? Que renvoyer si la pile est vide ?

---

### Carte E — Squelette de code à compléter

> ```python
> def effectifs(mots):
>     resultat = ..........
>     for mot in mots:
>         resultat[mot] = resultat.get(mot, ..........) + ..........
>     return ..........
>
> # Tests
> # effectifs(['a', 'b', 'a']) doit valoir ..........................
> # effectifs([])              doit valoir ..........................
> ```
>
> ```python
> def empiler(p, x):
>     p...........(x)
>
> def depiler(p):
>     if len(p) == ..........:
>         return None
>     return p...........()
> ```

---

## Carte « contrôle » — à utiliser avant toute certitude de 4

> - J'ai écrit ma prédiction **avant** d'exécuter.
> - Je sais dire si chaque instruction modifie ou construit.
> - Je n'ai affecté le résultat d'aucune méthode qui modifie en place.
> - J'ai testé ma fonction sur au moins **deux** cas, dont un cas vide.

---

## Carte « erreurs fréquentes » — à distribuer en fin de séance

> 1. `L = L.append(x)` : la liste est remplacée par `None`. **Ne jamais affecter `append`.**
> 2. `L[n]` sur un tableau de n éléments : le dernier indice est n − 1.
> 3. Accéder à une clé absente sans `get` : `KeyError`.
> 4. Croire que `sorted(L)` trie L : non, il en renvoie une copie triée.
> 5. Confondre `pop()` et `pop(0)` : c'est toute la différence entre une pile et une file.
