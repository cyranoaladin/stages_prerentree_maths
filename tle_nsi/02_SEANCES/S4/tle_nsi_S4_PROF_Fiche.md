# Terminale NSI — Séance 4 — Fiche professeur
## Algorithmique : préconditions, recherche, tris, coût

**Durée :** 2 heures · **Source pédagogique :** `stage_prerentree_terminale_nsi.md`

## Pourquoi cette séance

L'algorithmique affiche 53,3 % de réussite, avec deux certitudes erronées. Deux points ne
sont pas stabilisés : la **précondition** de la recherche dichotomique — un tableau trié — et
l'**ordre de grandeur** du nombre de comparaisons.

C'est ce raisonnement qui justifie tout le bloc algorithmique de Terminale : « diviser pour
régner » généralise le geste de la dichotomie, la programmation dynamique se justifie par un
comptage d'opérations, et les parcours d'arbres et de graphes s'analysent de la même façon.

## Objectifs de la séance

1. Énoncer la précondition d'un algorithme et dire ce qui se passe si elle n'est pas vérifiée.
2. Évaluer le coût d'une recherche séquentielle et d'une recherche dichotomique.
3. Arbitrer entre deux algorithmes selon l'usage.

## Déroulé minuté

| Durée | Phase | Ce que fait le professeur | Ce que fait l'élève |
|---:|---|---|---|
| 10 min | Ouverture | Contrôle sur la séance 3 : valeurs produites par `range(1, 10, 4)` | Répond, déclare sa certitude |
| 20 min | Confrontation | Appliquer une dichotomie à un tableau **non trié** : que se passe-t-il ? | Prédit, puis exécute |
| 25 min | Reconstruction | Précondition ; dichotomie ; coût logarithmique ; tri par insertion | Prend la trace écrite |
| 30 min | Entraînement différencié | Distribue les trois parcours, sur machine | Traite son parcours |
| 20 min | Ouverture Terminale | Diviser pour régner ; parcours d'arbre ; programmation dynamique | Observe, exécute |
| 15 min | Trace écrite et bilan | Fait remplir la fiche de synthèse | Remplit, déclare sa certitude |

## Conduite de la phase de confrontation

C'est la confrontation la plus importante du module, parce que l'erreur y est **silencieuse**.

1. Fournir une implémentation correcte de la dichotomie :
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
2. Demander la prédiction pour `recherche_dichotomique([4, 1, 9, 3], 4)`.
   La valeur 4 **est** dans le tableau, à l'indice 0 : la plupart des élèves prédiront 0.
3. **Faire exécuter.** La fonction renvoie **−1** : « valeur absente ».
4. Laisser le silence. Faire dire ce qui vient de se passer : le programme n'a pas planté, il
   n'a affiché aucune erreur — **il a simplement menti**.
5. Faire dérouler à la main :

   | tour | gauche | droite | milieu | tableau[milieu] | décision |
   |---:|---:|---:|---:|---:|---|
   | 1 | 0 | 3 | 1 | 1 | 1 < 4, on cherche à droite : gauche = 2 |
   | 2 | 2 | 3 | 2 | 9 | 9 > 4, on cherche à gauche : droite = 1 |
   | — | 2 | 1 | — | — | gauche > droite : la boucle s'arrête, on renvoie −1 |

   La valeur 4, à l'indice 0, n'a jamais été regardée : l'algorithme l'a écartée dès le
   premier tour, parce qu'il a supposé le tableau trié.
6. Faire formuler la conclusion :

> Un algorithme dont la précondition n'est pas respectée ne signale rien. Il renvoie un
> résultat faux, avec l'aplomb d'un résultat juste. C'est le pire cas possible pour un
> programme — et c'est pour cela qu'une précondition s'écrit dans la spécification.

7. Faire ajouter la précondition à la docstring, puis un `assert` :
   ```python
   def recherche_dichotomique(tableau, valeur):
       """Precondition : tableau trie par ordre croissant.
       Renvoie l'indice de valeur, ou -1 si absente."""
       assert tableau == sorted(tableau), "le tableau doit etre trie"
       ...
   ```

## Reconstruction

**Coût.** Construire le tableau avec les élèves :

| Taille du tableau | Recherche séquentielle (pire cas) | Dichotomie (pire cas) |
|---:|---:|---:|
| 16 | 16 | 4 |
| 100 | 100 | 7 |
| 1 000 | 1 000 | 10 |
| 1 000 000 | 1 000 000 | 20 |

Repères à mémoriser : **2¹⁰ = 1 024** et **2²⁰ ≈ 10⁶**.

Faire dire la règle : à chaque étape, la dichotomie divise la taille par deux. Le nombre
d'étapes est le nombre de fois qu'on peut diviser n par 2, c'est-à-dire log₂(n).

**L'arbitrage.** Poser la question : faut-il toujours trier avant de chercher ?

| Situation | Meilleur choix | Pourquoi |
|---|---|---|
| Une seule recherche dans un tableau non trié | Recherche séquentielle | Le tri coûte plus cher que la recherche évitée |
| Beaucoup de recherches dans le même tableau | Trier une fois, puis dichotomies | Le coût du tri est amorti |
| Tableau déjà trié | Dichotomie | Aucun coût supplémentaire |

C'est le premier raisonnement d'arbitrage algorithmique de leur scolarité : le nommer comme
tel.

**Tri par insertion.** Le faire dérouler sur `[5, 2, 8, 1]` avec des cartes physiques, en
comptant les comparaisons. Coût : de l'ordre de n² dans le pire cas.

## Entraînement différencié

| Parcours | Élèves concernés | Support |
|---|---|---|
| Consolidation | Algorithmique en priorité 1 ou 2 dans le livret | Exercices 1 à 4, code fourni à exécuter et tracer |
| Maîtrise | Domaine réussi mais hésitant | Exercices 3 à 6, comptage des comparaisons exigé |
| Approfondissement | Domaine acquis avec certitude | Exercices 6 à 8, dont une comparaison expérimentale |

## Ouverture sur la Terminale — 20 minutes

**Diviser pour régner.** Montrer que la dichotomie est un cas particulier d'un schéma
général : diviser le problème, résoudre les morceaux, recombiner. Citer le tri fusion, sans
l'implémenter.

**Programmation dynamique.** Faire exécuter les deux versions du calcul de Fibonacci :

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

Faire chronométrer `fibo_naif(32)` puis `fibo_memo(32)`. L'écart est spectaculaire et se
mesure. Faire formuler : la version naïve recalcule des milliers de fois les mêmes valeurs ;
la seconde les mémorise dans un **dictionnaire** — celui de la séance 2.

Ne pas demander d'écrire une fonction récursive pendant le stage : ces deux fonctions sont
fournies, exécutées, commentées, pas reproduites.

## Erreurs à surveiller et réponses à apporter

| Erreur observée | Réponse |
|---|---|
| Dichotomie appliquée sans vérifier le tri | Reprendre l'exécution de la recherche de 4 dans `[4, 1, 9, 3]` |
| Croire qu'un algorithme faux plante | Insister : il renvoie −1 sans aucune erreur |
| log₂(n) confondu avec n/2 | Faire remplir le tableau de coûts : 1 000 000 donne 20, pas 500 000 |
| « Il faut toujours trier d'abord » | Faire l'arbitrage : combien de recherches prévoit-on ? |
| Comparer deux algorithmes sur une seule exécution | Faire compter les comparaisons, pas mesurer une seule fois |

## Indicateurs de fin de séance

- L'élève énonce la précondition avant d'utiliser un algorithme.
- L'élève sait dire l'ordre de grandeur du coût d'une dichotomie sur 1 000 éléments.
- L'élève sait dire dans quel cas trier avant de chercher est rentable.

---
_Source pédagogique unique : `stage_prerentree_terminale_nsi.md`._
