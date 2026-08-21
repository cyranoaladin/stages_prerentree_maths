# Terminale NSI — Mini-diagnostic pratique (Corrigé enseignant)

## Objet

Le positionnement initial est un questionnaire à réponse courte : il mesure des connaissances
déclaratives. Il ne dit rien de la capacité d'un élève à **écrire un programme qui tourne**,
ni à le vérifier.

Cette épreuve comble ce manque. Elle est passée sur machine en séance 3, et dépouillée avant
la séance 4.

## Corrigé et lecture

### Exercice 1 — Prédire une sortie

`r` vaut **`None`** ; `M` vaut **`[1, 2, 3]`**.

*Ce qui est mesuré.* La distinction entre valeur renvoyée et effet de bord, travaillée en
confrontation le jour même. Une prédiction juste **avant** exécution vaut mieux qu'une réponse
juste après.

*Lecture.* Trois cas à distinguer au dépouillement :

| Prédictions | Interprétation |
|---|---|
| `None` et `[1, 2, 3]` | la distinction est acquise |
| `[1, 2, 3]` et `[1, 2, 3]` | la fonction est crue renvoyer ce qu'elle modifie |
| `None` et `[1, 2]` | la valeur de retour est acquise, l'effet de bord ne l'est pas |

Le troisième cas est le plus fréquent et le plus discret : il faut le repérer.

### Exercice 2 — Table de trace

`range(2, 9, 3)` produit **2, 5, 8**.

| tour | i | s après |
|---:|---:|---:|
| 1 | 2 | 2 |
| 2 | 5 | 7 |
| 3 | 8 | 15 |

Valeur finale : **15**.

*Erreur attendue.* Inclure 11 (borne mal comprise), ou s'arrêter à 5 (croire que 8 dépasse la
borne alors que c'est 11 qui la dépasse).

*Lecture.* Un élève qui remplit correctement la table mais se trompe sur les valeurs de
`range` a un problème de borne, pas de trace. Ce sont deux remédiations différentes.

### Exercice 3 — Écrire une fonction

```python
def compte_pairs(L):
    """Prend une liste d'entiers, renvoie le nombre d'entiers pairs qu'elle contient."""
    total = 0
    for element in L:
        if element % 2 == 0:
            total = total + 1
    return total

assert compte_pairs([1, 2, 3, 4]) == 2
assert compte_pairs([]) == 0        # cas limite
```

*Ce qui est mesuré.* L'accumulateur initialisé **avant** la boucle, et la présence d'un cas
limite parmi les tests.

*Points à relever séparément.* Fonction correcte / spécification présente / deux tests /
au moins un cas limite. Un élève peut réussir le code et manquer complètement la
spécification : c'est un constat à part.

### Exercice 4 — Déboguer

a) `maximum([-5, -2, -8])` renvoie **0**, alors que le maximum est **−2**. Tout appel avec une
liste d'entiers strictement négatifs convient.

b) L'accumulateur est initialisé à **0**, valeur arbitraire qui n'appartient pas
nécessairement à la liste. Le programme ne renvoie pas le maximum de la liste, mais le maximum
entre 0 et les éléments.

c) Correction :

```python
def maximum(L):
    """Prend une liste non vide, renvoie son plus grand element."""
    plus_grand = L[0]
    for element in L:
        if element > plus_grand:
            plus_grand = element
    return plus_grand
```

*Ce qui est mesuré.* La capacité à **construire un contre-exemple**, qui est le même geste
qu'en mathématiques (module `tle_spe`, séance 4). C'est l'exercice le plus discriminant de
l'épreuve.

*Lecture.* Un élève qui repère l'initialisation à 0 sans savoir produire un appel qui échoue a
compris la cause mais pas encore le geste de réfutation. Le noter distinctement.

### Exercice 5 — Dictionnaire

```python
def effectifs(mots):
    """Prend une liste de mots, renvoie un dictionnaire mot -> nombre d'occurrences."""
    resultat = {}
    for mot in mots:
        resultat[mot] = resultat.get(mot, 0) + 1
    return resultat

assert effectifs(['a', 'b', 'a']) == {'a': 2, 'b': 1}
assert effectifs([]) == {}
```

*Erreur attendue.* Accéder à `resultat[mot]` sans `get` sur une clé encore absente, ce qui
lève un `KeyError` au premier mot. La variante avec un `if mot in resultat` est également
correcte et doit être acceptée sans réserve.

## Grille de dépouillement

| Compétence | Pas encore | Avec aide | Seul | Peut expliquer |
|---|:---:|:---:|:---:|:---:|
| Prédire une sortie (ex. 1) | | | | |
| Distinguer retour et effet de bord (ex. 1) | | | | |
| Table de trace (ex. 2) | | | | |
| Bornes de `range` (ex. 2) | | | | |
| Écrire une fonction avec accumulateur (ex. 3) | | | | |
| Spécifier et tester (ex. 3 et 5) | | | | |
| Construire un contre-exemple (ex. 4) | | | | |
| Dictionnaire avec `get` (ex. 5) | | | | |

## Décisions à prendre à l'issue du dépouillement

| Constat | Décision |
|---|---|
| Plus de la moitié du groupe échoue à l'exercice 1 | Reprendre les quatre cas de figure en ouverture de la séance 4 |
| Bornes de `range` échouées | Redistribuer les cartes `range` de la séance 3 en séance 4 |
| Spécification absente chez la majorité | Rendre la spécification obligatoire dans toutes les fiches restantes |
| Contre-exemple non produit (ex. 4) | Renforcer la confrontation de la séance 4 : c'est le même geste |
| `KeyError` sur l'exercice 5 | Reprendre `get` en cinq minutes au début de la séance 5 |

---
_Document enseignant. Ne pas diffuser aux élèves avant dépouillement._
