# Terminale NSI — Évaluation finale (Élève)
## Séance 5 — 35 minutes

Cette évaluation **n'est pas notée**. Elle est lue avec la même grille que ton positionnement
de départ : ce qui compte est le déplacement entre les deux.

Sept exercices, un par domaine du stage.

### Consignes

- Je prédis avant d'exécuter, quand une exécution est possible.
- Je déclare ma certitude à chaque exercice : ☐1 ☐2 ☐3 ☐4.
- Je laisse vide plutôt que de deviner.

**Nom :** ..............................................  **Date :** ......................

---

## Exercice 1 — Représentation binaire

a) Écris 37 en binaire, puis **vérifie** en recalculant la valeur décimale.

Écriture : ....................  Vérification : ....................

b) Convertis 0x3C en base 10.

....................................................................................................

c) Combien de valeurs différentes peut-on coder sur 8 bits ?

....................................................................................................

**Certitude :** ☐1 ☐2 ☐3 ☐4

---

## Exercice 2 — Booléens et logique

a) Que vaut `not (True and False) or False` ? Détaille l'ordre d'évaluation.

....................................................................................................

b) Écris la négation de la condition `age > 18 and classe == 'TG3'`. Justifie.

....................................................................................................

**Certitude :** ☐1 ☐2 ☐3 ☐4

---

## Exercice 3 — Types construits

Soit `L = [4, 8, 15, 16]` et `d = {'a': 1, 'b': 2}`.

a) Que valent `L[2]`, `L[-1]` et `len(L)` ? Que provoque `L[4]` ?

....................................................................................................

b) Que vaut `L` après `L = L.append(23)` ? Pourquoi ?

....................................................................................................

c) Écris l'instruction qui ajoute la clé `'c'` de valeur 3 à `d`, puis celle qui renvoie 0 si
la clé `'z'` est absente, sans erreur.

....................................................................................................

**Certitude :** ☐1 ☐2 ☐3 ☐4

---

## Exercice 4 — Programmation

a) Remplis la table de trace **avant** d'exécuter.

```python
s = 1
for i in range(1, 5):
    s = s * i
```

| tour | i | s après |
|---:|---:|---:|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |

Valeur finale de `s` : ....................

b) Écris `compte_positifs(L)` qui renvoie le nombre d'éléments strictement positifs d'une
liste. Ajoute une spécification et deux tests, dont un cas limite.

```python
def compte_positifs(L):
    """..............................................................."""


assert compte_positifs(..........) == ..........
assert compte_positifs(..........) == ..........
```

c) Que renvoie une fonction sans `return` ? Cela l'empêche-t-il de modifier une liste reçue en
paramètre ?

....................................................................................................

**Certitude :** ☐1 ☐2 ☐3 ☐4

---

## Exercice 5 — Algorithmique

a) Quelle est la précondition de la recherche dichotomique ?

....................................................................................................

b) Que se passe-t-il si on l'applique à un tableau non trié ? Le programme signale-t-il
quelque chose ?

....................................................................................................

c) Dans un tableau trié de 100 000 éléments, combien de comparaisons au pire pour une
recherche dichotomique ? Justifie par un ordre de grandeur.

....................................................................................................

**Certitude :** ☐1 ☐2 ☐3 ☐4

---

## Exercice 6 — Données en tables et bases de données

Un fichier CSV décrit 200 livres par 5 attributs, avec une ligne d'en-tête.

a) Combien de lignes le fichier contient-il ? Combien d'enregistrements ? Combien de
descripteurs ?

....................................................................................................

b) Nomme l'opération : « ne garder que les livres publiés après 2010 ». Et : « ne garder que
les colonnes titre et auteur ».

....................................................................................................

c) Écris en SQL : « afficher le titre et l'auteur des livres publiés après 2010 », depuis une
table `livres`.

```sql

```

**Certitude :** ☐1 ☐2 ☐3 ☐4

---

## Exercice 7 — Architecture et systèmes

a) Dans le modèle de von Neumann, quel élément effectue les calculs ? Quel élément stocke les
instructions du programme en cours ?

....................................................................................................

b) Cite deux ressources gérées par un système d'exploitation.

....................................................................................................

**Certitude :** ☐1 ☐2 ☐3 ☐4

---

## Bilan personnel

**Le domaine sur lequel je me sens le plus sûr aujourd'hui :** ..............................

**Le domaine que je dois encore travailler en septembre :** .................................

**Une chose que je faisais avant le stage et que je ne fais plus :** ........................

....................................................................................................
