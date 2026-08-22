# Terminale NSI — Séance 3 — Fiche élève
## Programmation : fonctions, retour, portée, boucles

**Ton objectif de séance :** savoir dire, pour n'importe quelle fonction, ce qu'elle
**renvoie** et ce qu'elle **modifie** — ce sont deux questions différentes.

### Règle de travail

- J'écris ma prédiction **avant** d'exécuter.
- Je fais une table de trace avant de lancer une boucle.
- Chaque fonction que j'écris a une spécification et **deux** tests.
- Certitude : $\square$1 $\square$2 $\square$3 $\square$4 · Aide : A, B, C, D ou E.

---

## Contrôle d'entrée (séance 2)

Soit `L = [1, 2, 3]`. Que contient L après `L.insert(0, 9)` puis `L.append(4)` ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4

---

## Partie 1 — Prédire, puis exécuter

**Question 0.**

```python
def h(L):
    L.append(0)

M = [1, 2]
r = h(M)
print("r vaut :", r)
print("M vaut :", M)
```

Ma prédiction pour `r` : ....................  Certitude : $\square$1 $\square$2 $\square$3 $\square$4

Ma prédiction pour `M` : ....................  Certitude : $\square$1 $\square$2 $\square$3 $\square$4

Sorties réelles : $r =$ ....................  $M =$ ....................

**Ce que je constate :** ...................................................................

....................................................................................................

---

## Partie 2 — La trace écrite

> **Renvoyer et modifier sont deux choses différentes.**
>
> | Fonction | Renvoie | Modifie l'argument |
> |---|---|---|
> | `def f(x): return x * 2` | une valeur | non |
> | `def g(L): L.append(0)` | `None` | oui |
> | `def h(L): L.append(0); return L` | une valeur | oui |
> | `def k(x): print(x)` | `None` | non |
>
> **Sans `return`, une fonction renvoie `None`** — même si elle a fait beaucoup de choses.
>
> **Portée.** Une variable créée dans une fonction disparaît à la fin de l'appel.
>
> **Bornes de `range`.** La borne supérieure est **exclue**.
>
> | Écriture | Valeurs | Tours |
> |---|---|---:|
> | `range(3)` | 0, 1, 2 | 3 |
> | `range(1, 4)` | 1, 2, 3 | 3 |
> | `range(2, 10, 3)` | 2, 5, 8 | 3 |
>
> **Table de trace.** Avant d'exécuter, j'écris l'état des variables tour par tour.

---

## Partie 3 — Entraînement

### Comment tu trouves ton parcours

Ton livret individuel porte, pour cette séance, une **posture** et un **parcours**. Le tableau
ci-dessous dit ce que tu traites. Tu ne fais pas les huit exercices : tu fais les tiens, et tu
les fais entièrement.

| Ta posture du jour | Ce que tu traites | Ce qu'on attend de toi |
|---|---|---|
| **DIAGNOSTIQUER** — tu avais laissé ce domaine sans réponse | Question 0, puis exercices 1 et 2 | Répondre même sans être sûr : déclarer une certitude de 1 est une réponse, pas un aveu |
| **CONFRONTER** — tu t'es trompé en étant sûr de toi | Question 0, puis exercices 1 à 4 | Écrire ce que tu croyais, puis ce qui l'a mis en défaut |
| **INSTALLER** — il te manque quelque chose, et tu le sais | Exercices 1 à 4 | Exécuter avant de conclure, et écrire la table de trace |
| **CONSOLIDER** — tu réussis, sans en être sûr | Exercices 3 à 6 | Spécifier la fonction et écrire ses tests, sans carte d'aide |
| **ENTRETENIR** — c'est acquis et assumé | Exercices 6 à 8 | Justifier le choix d'algorithme par son coût, pas par le temps mesuré |
| **EXCELLENCE** — ton bilan ne comporte aucun domaine à reprendre, ou tu as terminé ta piste | Exercices 9 et 10, puis l'atelier Terminale | Produire une fonction spécifiée et testée, puis relire la copie d'un camarade **sans lui donner la réponse** |

### Exercices 1 à 4 — pistes Diagnostiquer, Confronter et Installer

**Exercice 1.** Soit `def g(n): return n*n + 1`. Que renvoie `g(4)` ? Que vaut `g(g(1))` ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Combien d'itérations effectue `for i in range(2, 10, 3)` ? Quelles valeurs
prend `i` ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Soit `s = 0` puis `for i in range(1, 6): s = s + i*i`. Remplis la table de
trace, **puis** vérifie par exécution.

| tour | i | i*i | s après |
|---:|---:|---:|---:|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

Valeur finale de s : ....................  Vérifiée par exécution : $\square$oui $\square$non

**Exercice 4.** Écris une fonction `somme_jusqua(n)` qui renvoie 1 + 2 + … + n. Ajoute une
spécification et deux tests.

```python
def somme_jusqua(n):
    """..............................................................."""










# Tests
assert somme_jusqua(....) == ....
assert somme_jusqua(....) == ....
```

### Exercices 3 à 6 — piste Consolider

**Exercice 5.** Cette fonction contient une erreur. Trouve-la **par une table de trace**,
avant d'exécuter.

```python
def moyenne(notes):
    for note in notes:
        total = 0
        total = total + note
    return total / len(notes)
```

L'erreur : ........................................................................

La correction : ...................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**Exercice 6.** Écris `maximum(L)` qui renvoie le plus grand élément d'une liste **non vide**,
sans utiliser `max`. Spécifie et teste. Que devrait faire ta fonction sur une liste vide ?

```python










```

### Exercices 6 à 8 — piste Entretenir

**Exercice 7.** Écris `normaliser(L)` qui divise chaque élément d'une liste de nombres par le
maximum, **sans modifier L** et en renvoyant une nouvelle liste. Puis écris
`normaliser_en_place(L)` qui fait la même chose **en modifiant L** et sans rien renvoyer.
Écris deux tests pour chacune.

```python










```

**Exercice 8.** Que renvoie et que modifie chacune de ces fonctions ? Réponds **avant**
d'exécuter, puis vérifie.

```python
def a(L):
    L = L + [0]

def b(L):
    L += [0]

def c(L):
    return L + [0]
```

| Fonction | Renvoie | Modifie L | Pourquoi |
|---|---|---|---|
| `a` | | | |
| `b` | | | |
| `c` | | | |

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

---

## Piste excellence — exercices 9 et 10

> **Pour qui.** Ces deux exercices sont les tiens si ton bilan ne comporte aucun domaine à
> reprendre, ou si tu as terminé ta piste avant la fin du temps différencié. Le premier est un
> problème complet : on attend une fonction spécifiée, testée, et dont tu sais dire le coût.
> Le second part d'un énoncé faux : on attend un contre-exemple, puis l'énoncé corrigé.
>
> Une fois tes deux exercices rendus, le professeur pourra te confier la copie d'un camarade.
> Tu ne corriges pas : tu dis si la fonction est spécifiée, si le cas limite est traité, et où
> le raisonnement s'interrompt.

**Exercice 9.** Écris `second_max(L)`, qui renvoie le deuxième plus grand élément
**distinct** d'une liste de nombres, sans trier et en un seul parcours.

a) La fonction, avec sa spécification en docstring.

```python
def second_max(L):
    """..............................................................."""








```

b) Quelle précondition faut-il sur `L` ? Écris l'`assert` correspondant.

....................................................................................................

....................................................................................................

c) Deux tests, dont un cas limite que ta précondition n'exclut pas.

```python
assert second_max(....) == ....
assert second_max(....) == ....
```

d) Combien de comparaisons ta fonction effectue-t-elle au pire pour n éléments ? Compare avec
la solution « trier la liste puis prendre l'avant-dernier ».

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 10.** Ce programme échoue à l'exécution.

```python
compteur = 0

def incremente(n):
    compteur = compteur + n
    return compteur
```

a) Quelle erreur Python signale-t-il, et pourquoi ? Le nom `compteur` existe pourtant.

....................................................................................................

....................................................................................................

....................................................................................................

b) Propose deux corrections. Laquelle est préférable, et pour quelle raison ?

....................................................................................................

....................................................................................................

....................................................................................................

c) « Une fonction qui ne renvoie rien ne sert à rien. » Réfute par un exemple tiré de cette
séance.

....................................................................................................

....................................................................................................

d) Une fonction peut-elle à la fois renvoyer une valeur et modifier son argument ? Écris un
exemple, puis explique pourquoi c'est une mauvaise idée.

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

---

## Partie 4 — Ce que la Terminale en fera

> Une fonction **récursive** s'appelle elle-même. Elle renvoie une valeur construite à partir
> de la valeur renvoyée par l'appel suivant :
>
> ```python
> def factorielle(n):
>     if n == 0:
>         return 1
>     return n * factorielle(n - 1)
> ```
>
> Sans un `return` net à chaque branche, ce mécanisme ne fonctionne pas : la fonction
> renverrait `None`, et le calcul échouerait.
>
> C'est pour cela que la valeur de retour devait être sûre aujourd'hui.
>
> La **mise au point** et la **modularité**, également au programme de Terminale, reposent sur
> la spécification et les tests que tu as écrits pendant cette séance.

---

## Atelier Terminale NSI — 20 minutes

> **Pour qui.** Cet atelier est pour toi si tu as terminé ta piste avant la fin du temps
> différencié, ou si tu suis la piste excellence. Il ne porte pas sur le thème du jour : il
> ouvre une notion du programme de Terminale que la Première n'aborde pas, et que la séance
> rend abordable dès maintenant. Le temps y est prélevé sur la phase différenciée.

**Le lien avec la séance du jour.** Tu viens de séparer ce qu'une fonction **renvoie** de ce qu'elle
**modifie**. La programmation orientée objet, au programme de Terminale, range les deux au
même endroit : les données et les fonctions qui les manipulent.

**a)** Voici une pile écrite en objet. Complète les deux méthodes manquantes.

```python
class Pile:
    def __init__(self):
        self.contenu = []

    def empiler(self, x):


    def depiler(self):



    def est_vide(self):

```

**b)** Écris les trois lignes qui créent une pile, y empilent 5, puis dépilent.

....................................................................................................

....................................................................................................

**c)** À quoi sert `self` ? Que se passerait-il si on l'oubliait dans la définition de
`empiler` ?

....................................................................................................

....................................................................................................

....................................................................................................

**d)** Compare avec la fonction `empiler(p, x)` de la séance 2, où `p` était une liste. Qu'est-ce
que l'écriture objet garantit que l'écriture par fonctions ne garantissait pas ?

....................................................................................................

....................................................................................................

....................................................................................................

**Ce que la Terminale en fera.** Toutes les structures de données de l'année — pile, file,
liste chaînée, arbre, graphe — sont définies ainsi : une classe, ses attributs, ses méthodes,
et une interface qu'on peut utiliser sans connaître l'implémentation.

---

## Partie 5 — Bilan de séance

**Ce que j'ai compris aujourd'hui :** ......................................................

....................................................................................................

**La différence entre renvoyer et modifier, avec mes mots :** ...............................

....................................................................................................

**Ma certitude en programmation, aujourd'hui :** $\square$1 $\square$2 $\square$3 $\square$4

**Aide maximale utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune
