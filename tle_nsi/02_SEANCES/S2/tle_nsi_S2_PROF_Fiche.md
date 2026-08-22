# Terminale NSI — Séance 2 — Fiche professeur
## Types construits : tableaux, dictionnaires, mutabilité

**Durée :** 2 heures · **Source pédagogique :** `stage_prerentree_terminale_nsi.md`

## Pourquoi cette séance

Les types construits portent **trois certitudes erronées** sur cinq élèves — le maximum du
positionnement, à égalité avec la programmation et les données en tables. La réussite moyenne
est de 63,3 %.

C'est l'obstacle le plus coûteux pour la Terminale : **toutes** les structures de données de
l'année — piles, files, arbres, graphes — s'implémentent avec des listes et des
dictionnaires. Une confusion sur l'indexation ou sur la mutabilité se paie à chaque
implémentation, pendant toute l'année.

## Objectifs de la séance

1. Indexer un tableau sans erreur, y compris avec des indices négatifs.
2. Distinguer une méthode qui **modifie en place** d'une expression qui **construit** un
   nouvel objet.
3. Accéder à un dictionnaire, ajouter, supprimer, parcourir, et éviter `KeyError`.

## Déroulé minuté

| Durée | Phase | Ce que fait le professeur | Ce que fait l'élève |
|---:|---|---|---|
| 10 min | Ouverture | Contrôle sur la séance 1 : convertir 0x2A en base 10 | Répond, déclare sa certitude |
| 20 min | Confrontation | `L = [1,2,3]` puis `L = L.append(4)` : que vaut L ? | Prédit, puis exécute |
| 25 min | Reconstruction | Indexation ; méthodes en place et `None` ; dictionnaires | Prend la trace écrite |
| 30 min | Entraînement différencié | Distribue les trois parcours, sur machine | Traite son parcours |
| 20 min | Ouverture Terminale | Pile et file sur une liste ; arbre sur un dictionnaire | Observe, exécute les exemples |
| 15 min | Trace écrite et bilan | Fait remplir la fiche de synthèse | Remplit, déclare sa certitude |

## Conduite de la phase de confrontation

**Prédire, exécuter, confronter.** L'écran fait le travail.

1. Écrire au tableau :
   ```python
   L = [1, 2, 3]
   L = L.append(4)
   print(L)
   ```
   Demander à chaque élève d'écrire sa **prédiction** et sa certitude.
2. Les prédictions attendues : `[1, 2, 3, 4]` — l'erreur — et `None` — la réponse correcte.
3. **Faire exécuter** par chaque binôme. La sortie `None` est déroutante : laisser le temps
   du silence.
4. Faire exécuter ensuite la version correcte :
   ```python
   L = [1, 2, 3]
   L.append(4)
   print(L)      # [1, 2, 3, 4]
   ```
5. Faire verbaliser : `append` **modifie** la liste et **ne renvoie rien**. L'affectation
   `L = ...` écrase donc la liste avec `None`.
6. **Puis** généraliser : `insert`, `del`, `sort`, `reverse` sont dans le même cas.

**Contraste à installer.** Faire exécuter `M = L + [4]` : ici L est inchangée et M est une
**nouvelle** liste. Deux gestes, deux effets : l'un modifie, l'autre construit.

## Reconstruction

**Indexation.**

| Expression | Sur `L = [5, 7, 9, 11]` |
|---|---|
| `L[0]` | 5 |
| `L[3]` | 11 |
| `L[-1]` | 11 |
| `L[4]` | `IndexError` |
| `len(L)` | 4 |

Faire dire la règle : pour n éléments, les indices valides vont de 0 à $n - 1$.

**En place ou pas.**

| Écriture | Effet | Valeur renvoyée |
|---|---|---|
| `L.append(x)` | modifie L | `None` |
| `L.insert(i, x)` | modifie L | `None` |
| `del L[i]` | modifie L | — |
| `L.sort()` | modifie L | `None` |
| `L + [x]` | ne modifie rien | nouvelle liste |
| `sorted(L)` | ne modifie rien | nouvelle liste |

**Dictionnaires.**

```python
d = {'x': 10, 'y': 20}
d['y']            # 20
d['z']            # KeyError
d.get('z', 0)     # 0, sans erreur
d['z'] = 30       # cree l'entree
del d['x']        # supprime
for cle, valeur in d.items():
    print(cle, valeur)
```

## Entraînement différencié

| Parcours | Élèves concernés | Support |
|---|---|---|
| Consolidation | Types construits en priorité 1 ou 2 dans le livret | Exercices 1 à 4, exemples exécutés fournis |
| Maîtrise | Domaine réussi mais hésitant | Exercices 3 à 6, spécification exigée |
| Approfondissement | Domaine acquis avec certitude | Exercices 6 à 8, dont une pile et une file |

## Ouverture sur la Terminale — 20 minutes

Montrer que les structures de Terminale **sont** des listes et des dictionnaires :

```python
# Une pile : dernier entre, premier sorti
pile = []
pile.append(1)      # empiler
pile.append(2)
sommet = pile.pop() # depiler -> 2

# Une file : premier entre, premier sorti
file = []
file.append(1)      # enfiler
file.append(2)
premier = file.pop(0)  # defiler -> 1

# Un arbre binaire, decrit par un dictionnaire
arbre = {
    'valeur': 5,
    'gauche': {'valeur': 3, 'gauche': None, 'droite': None},
    'droite': {'valeur': 8, 'gauche': None, 'droite': None},
}
print(arbre['gauche']['valeur'])   # 3
```

Faire exécuter les trois blocs. Faire formuler la conclusion :

> Une pile, une file, un arbre ne sont pas de nouveaux objets Python : ce sont des **usages
> conventionnés** des listes et des dictionnaires. Ce que vous savez faire aujourd'hui, vous
> le ferez toute l'année — avec des noms différents.

Ne pas demander d'implémenter une structure complète pendant le stage.

## Erreurs à surveiller et réponses à apporter

| Erreur observée | Réponse |
|---|---|
| `L = L.append(x)` | Faire exécuter et lire `None` ; faire réécrire sans affectation |
| `L[n]` sur n éléments | Faire compter les indices à voix haute à partir de 0 |
| Clé absente sans `get` | Faire provoquer le `KeyError`, puis montrer `get` |
| `d[0]` sur un dictionnaire | Faire distinguer clé et position ; montrer que `0` peut être une clé |
| `sorted(L)` cru modifier L | Faire afficher L avant et après |

## Indicateurs de fin de séance

- L'élève dit, avant d'écrire, si la méthode qu'il utilise modifie ou construit.
- L'élève utilise `get` quand la clé peut être absente.
- L'élève sait dire qu'une pile est une liste utilisée d'une certaine façon.

---
_Source pédagogique unique : `stage_prerentree_terminale_nsi.md`._
