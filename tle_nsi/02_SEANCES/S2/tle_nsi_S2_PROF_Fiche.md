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
| 30 min | Entraînement différencié | Aiguille chaque élève sur sa piste, sur machine | Traite son parcours |
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

L'aiguillage suit les cinq postures de la carte maîtrise $\times$ confiance, et non un niveau
supposé. L'attribution se lit dans le livret individuel de chaque élève, rubrique « Ton
parcours, séance par séance » ; la fiche élève porte le même tableau.

| Piste | Posture au diagnostic | Support |
|---|---|---|
| Diagnostiquer | Le domaine de la séance a été laissé sans réponse | Question 0, puis exercices 1 et 2 ; établir ce que l'élève sait avant toute remédiation |
| Confronter | Réponse fausse donnée avec une certitude de 3 ou 4 | Question 0, puis exercices 1 à 4 ; la réponse fausse est produite avant d'être corrigée |
| Installer | Réponse fausse avec une certitude basse | Exercices 1 à 4, exemples exécutés fournis |
| Consolider | Domaine réussi mais hésitant | Exercices 3 à 6, spécification exigée |
| Entretenir | Domaine acquis et assumé | Exercices 6 à 8, dont une pile et une file |

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

## Corrigé de la piste excellence

**Exercice 9.** a) `enfiler` ajoute à `f['entree']`. `defiler` : si `f['sortie']` est vide,
dépiler tout `f['entree']` dedans, puis dépiler `f['sortie']`.
b) Après les trois `enfiler` : entrée `[1, 2, 3]`, sortie `[]`. Premier `defiler` : bascule en
sortie `[3, 2, 1]`, renvoie 1. Second `defiler` : sortie `[3, 2]`, renvoie 2.
c) `L.pop(0)` décale tous les éléments : coût linéaire à chaque défilement. Ici chaque élément
est basculé une seule fois : coût **constant en moyenne**. C'est le point de l'exercice.
d) Précondition : la file ne doit pas être vide, c'est-à-dire `f['entree']` et `f['sortie']`
pas toutes deux vides. `assert f['entree'] or f['sortie']`.

**Exercice 10.** a) `[1]`, puis `[1, 2]`, puis `[1, 2, 3]`.
b) La liste par défaut est créée **une seule fois**, à la définition de la fonction, et non à
chaque appel. Tous les appels sans argument partagent donc le même objet.
c) `def ajoute(element, liste=None): if liste is None: liste = []` puis le reste inchangé.
d) Faux tel quel. Le tuple garantit que ses **cases** ne changent pas, pas que les objets
qu'elles désignent sont immuables : `t[0].append(3)` fonctionne et donne `([1, 3], 2)`.
Énoncé correct : un tuple est immuable, mais il peut contenir des objets muables.

## Corrigé de l'atelier Terminale NSI

a) Arbre obtenu : racine 8 ; à gauche 3, dont les fils sont 1 et 6, et 6 a pour fils gauche 4 ;
à droite 10, dont le fils droit est 14.
b) Parcours infixe : 1, 3, 4, 6, 8, 10, 14. **Les valeurs sortent triées** — c'est la propriété
qui fait tout l'intérêt de la structure.
c) Comparer la valeur cherchée à celle du nœud, descendre à gauche si elle est plus petite, à
droite sinon, s'arrêter sur `None`.
d) Trois comparaisons au pire, la hauteur de l'arbre. Avec l'insertion dans l'ordre croissant,
chaque valeur part à droite : l'arbre dégénère en une liste de hauteur 7, et la recherche
redevient linéaire. C'est ce cas qui motive les arbres équilibrés.

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
