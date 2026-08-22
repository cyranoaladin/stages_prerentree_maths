# Terminale NSI — Séance 2 — Fiche élève
## Types construits : tableaux, dictionnaires, mutabilité

**Ton objectif de séance :** savoir dire, avant d'écrire, si une instruction **modifie** un
objet ou en **construit** un nouveau.

### Règle de travail

- Je prédis, puis j'exécute, puis je compare.
- J'écris ma prédiction **avant** de lancer le programme.
- Certitude : $\square$1 $\square$2 $\square$3 $\square$4 · Aide : A, B, C, D ou E.

---

## Contrôle d'entrée (séance 1)

Convertis 0x2A en base 10, puis 60 en hexadécimal.

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4

---

## Partie 1 — Prédire, puis exécuter

**Question 0.** Que va afficher ce programme ?

```python
L = [1, 2, 3]
L = L.append(4)
print(L)
```

Ma prédiction : ..................................................  Certitude : $\square$1 $\square$2 $\square$3 $\square$4

Sortie réelle : ..................................................

Ce que je constate : .....................................................................

Et celui-ci ?

```python
L = [1, 2, 3]
L.append(4)
print(L)
```

Ma prédiction : ....................  Sortie réelle : ....................

**La différence, avec mes mots :** .........................................................

....................................................................................................

---

## Partie 2 — La trace écrite

> **Indexation.** Les indices commencent à **0**. Pour n éléments, le dernier indice valide
> est $n - 1$. L'indice $- 1$ désigne le dernier élément. `L[n]` lève une `IndexError`.
>
> **Modifier ou construire.**
>
> | Écriture | Effet | Ce qu'elle renvoie |
> |---|---|---|
> | `L.append(x)` | modifie L | `None` |
> | `L.insert(i, x)` | modifie L | `None` |
> | `L.sort()` | modifie L | `None` |
> | `L + [x]` | ne modifie rien | une nouvelle liste |
> | `sorted(L)` | ne modifie rien | une nouvelle liste |
>
> **Donc `L = L.append(4)` détruit la liste** : L reçoit `None`.
>
> **Dictionnaires.** `d[cle]` accède · `d[cle] = v` crée ou remplace · `del d[cle]` supprime
> · `d.get(cle, defaut)` évite l'erreur · `d.items()` parcourt les couples.

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

**Exercice 1.** Soit `L = [5, 7, 9, 11]`. Que valent `L[0]`, `L[3]` et `L[-1]` ? Que provoque
`L[4]` ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Soit `L = [1, 2, 3]`. Après `L.insert(0, 9)` puis `L.append(4)`, que contient
L ? Et que vaudrait L après `L = L.append(5)` ?

Prédiction : ....................  Sortie réelle : ....................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Soit `d = {'x': 10, 'y': 20}`. Que vaut `d['y']` ? Que se passe-t-il avec
`d['z']` ? Comment obtenir 0 dans ce cas, sans erreur ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 4.** Écris les instructions qui ajoutent à `d` la clé `'z'` de valeur 30,
suppriment la clé `'x'`, puis parcourent `d` en affichant chaque couple clé-valeur.

```python





```

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

### Exercices 3 à 6 — piste Consolider

**Exercice 5.** Soit `L = [3, 1, 2]`. Prédis puis vérifie la valeur de `L` et de `M` après :

```python
M = sorted(L)
```
puis après :
```python
L.sort()
```

Prédictions : ....................................................................

Sorties réelles : ..................................................................

**Exercice 6.** Écris une fonction `effectifs(mots)` qui prend une liste de mots et renvoie
un dictionnaire associant à chaque mot son nombre d'occurrences. Ajoute deux tests.

```python
def effectifs(mots):
    ...








# Tests
# effectifs(['a', 'b', 'a']) doit valoir ...............
# effectifs([]) doit valoir ...............
```

### Exercices 6 à 8 — piste Entretenir

**Exercice 7.** Implémente une **pile** avec une liste : écris `empiler(p, x)` et `depiler(p)`.
Que doit renvoyer `depiler` sur une pile vide ? Justifie ton choix.

```python












```

**Exercice 8.** Un arbre binaire est décrit par un dictionnaire à trois clés : `'valeur'`,
`'gauche'`, `'droite'` (avec `None` pour une branche absente). Écris une fonction `somme(a)`
qui renvoie la somme de toutes les valeurs de l'arbre.

*Indication : la fonction devra s'appeler elle-même. Ce n'est pas encore au programme — essaie
quand même.*

```python



```

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

**Exercice 9.** Une **file** est une structure « premier entré, premier sorti ». On la
représente ici par un dictionnaire à deux clés, `'entree'` et `'sortie'`, contenant chacune
une liste utilisée comme pile.

a) Écris `enfiler(f, x)` et `defiler(f)`. Quand `'sortie'` est vide, `defiler` y bascule tout
le contenu de `'entree'`, dans l'ordre inverse.

```python
def enfiler(f, x):







def defiler(f):











```

b) Déroule la trace : file vide, puis `enfiler` 1, 2, 3, puis deux `defiler`. Donne le contenu
des deux listes après chaque opération.

| Opération | `'entree'` | `'sortie'` | Valeur renvoyée |
|---|---|---|---|
| `enfiler(f, 1)` | | | |
| `enfiler(f, 2)` | | | |
| `enfiler(f, 3)` | | | |
| `defiler(f)` | | | |
| `defiler(f)` | | | |

c) Pourquoi ne pas simplement écrire `L.pop(0)` sur une seule liste ? Compare le coût des
deux solutions.

....................................................................................................

....................................................................................................

....................................................................................................

d) Que doit faire `defiler` sur une file vide ? Écris la précondition et l'`assert` qui la
vérifie.

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 10.** Prédis, **avant d'exécuter**, ce que renvoient les appels successifs.

```python
def ajoute(element, liste=[]):
    liste.append(element)
    return liste
```

a) Que renvoie `ajoute(1)` ? Puis `ajoute(2)` ? Puis `ajoute(3)` ?

....................................................................................................

....................................................................................................

b) Explique le mécanisme. À quel moment la liste par défaut est-elle créée ?

....................................................................................................

....................................................................................................

....................................................................................................

c) Corrige la fonction pour qu'elle renvoie une liste neuve à chaque appel sans argument.

```python
def ajoute(element, liste=None):




```

d) « Un tuple est immuable, donc son contenu ne peut pas changer. » Vrai ou faux ? Teste avec
`t = ([1], 2)` puis `t[0].append(3)`, et écris l'énoncé correct.

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

---

## Partie 4 — Ce que la Terminale en fera

Exécute ces trois blocs :

```python
# Une pile : dernier entre, premier sorti
pile = []
pile.append(1)
pile.append(2)
sommet = pile.pop()      # vaut ...........

# Une file : premier entre, premier sorti
file = []
file.append(1)
file.append(2)
premier = file.pop(0)    # vaut ...........

# Un arbre binaire decrit par un dictionnaire
arbre = {
    'valeur': 5,
    'gauche': {'valeur': 3, 'gauche': None, 'droite': None},
    'droite': {'valeur': 8, 'gauche': None, 'droite': None},
}
print(arbre['gauche']['valeur'])   # affiche ...........
```

> Une pile, une file, un arbre, un graphe ne sont pas de nouveaux objets Python : ce sont des
> **usages conventionnés** des listes et des dictionnaires.
>
> Ce que tu sais faire aujourd'hui, tu le feras toute l'année — sous d'autres noms.

---

## Atelier Terminale NSI — 20 minutes

> **Pour qui.** Cet atelier est pour toi si tu as terminé ta piste avant la fin du temps
> différencié, ou si tu suis la piste excellence. Il ne porte pas sur le thème du jour : il
> ouvre une notion du programme de Terminale que la Première n'aborde pas, et que la séance
> rend abordable dès maintenant. Le temps y est prélevé sur la phase différenciée.

**Le lien avec la séance du jour.** Tu viens de représenter un arbre par un dictionnaire imbriqué. Un **arbre
binaire de recherche** est le même objet, avec une règle en plus : à gauche les valeurs plus
petites, à droite les plus grandes.

On insère successivement 8, 3, 10, 1, 6, 14, 4 dans un arbre binaire de recherche vide.

**a)** Dessine l'arbre obtenu. Chaque valeur descend depuis la racine en comparant à chaque
nœud.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**b)** Le **parcours infixe** visite le sous-arbre gauche, puis la racine, puis le sous-arbre
droit. Écris la suite des valeurs obtenue. Que remarques-tu ?

....................................................................................................

....................................................................................................

**c)** Écris la fonction de recherche, en réutilisant le dictionnaire à trois clés de
l'exercice 8.

```python
def recherche(arbre, valeur):
    """..............................................................."""






```

**d)** Combien de comparaisons au pire pour trouver une valeur dans cet arbre ? Et si on avait
inséré 1, 3, 4, 6, 8, 10, 14 dans cet ordre ? Que devient l'arbre ?

....................................................................................................

....................................................................................................

....................................................................................................

**Ce que la Terminale en fera.** L'arbre binaire de recherche est la structure du programme de
Terminale qui explique pourquoi un dictionnaire Python est rapide. Sa hauteur décide de tout :
un arbre équilibré cherche en $\log_2 n$ comparaisons, un arbre dégénéré en n.

---

## Partie 5 — Bilan de séance

**Ce que j'ai compris aujourd'hui :** ......................................................

....................................................................................................

**La différence entre modifier et construire, avec mes mots :** .............................

....................................................................................................

**Ma certitude sur les types construits, aujourd'hui :** $\square$1 $\square$2 $\square$3 $\square$4

**Aide maximale utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune
