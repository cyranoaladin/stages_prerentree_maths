# Terminale NSI — Séance 4 — Fiche élève
## Algorithmique : préconditions, recherche, tris, coût

**Ton objectif de séance :** savoir dire à quelle condition un algorithme donne un résultat
juste — et combien il coûte.

### Règle de travail

- J'écris la **précondition** avant d'utiliser un algorithme.
- Je compte les comparaisons, je ne me contente pas de mesurer une fois.
- Certitude : $\square$1 $\square$2 $\square$3 $\square$4 · Aide : A, B, C, D ou E.

---

## Contrôle d'entrée (séance 3)

Quelles valeurs prend `i` dans `for i in range(1, 10, 4)` ? Combien de tours ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4

---

## Partie 1 — Prédire, puis exécuter

Voici une recherche dichotomique **correctement écrite** :

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

**Question 0.** Que renvoie `recherche_dichotomique([4, 1, 9, 3], 4)` ?

*Remarque : la valeur 4 est bien présente dans le tableau, à l'indice 0.*

Ma prédiction : ....................  Ma certitude : $\square$1 $\square$2 $\square$3 $\square$4

Sortie réelle : ....................

Déroule maintenant l'algorithme à la main :

| tour | gauche | droite | milieu | tableau[milieu] | décision |
|---:|---:|---:|---:|---:|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

**Ce que je constate :** ...................................................................

....................................................................................................

**Le programme a-t-il affiché une erreur ?** $\square$oui $\square$non

---

## Partie 2 — La trace écrite

> **Précondition.** La recherche dichotomique exige un tableau **trié**. Sur un tableau non
> trié, elle ne renvoie **pas** d'erreur : elle renvoie un résultat **faux**. C'est le pire
> cas possible pour un programme.
>
> On écrit la précondition dans la spécification, et on peut la vérifier :
> ```python
> assert tableau == sorted(tableau), "le tableau doit etre trie"
> ```
>
> **Coût.**
>
> | Taille | Recherche séquentielle | Dichotomie |
> |---:|---:|---:|
> | 16 | 16 | 4 |
> | 1 000 | 1 000 | 10 |
> | 1 000 000 | 1 000 000 | 20 |
>
> Repères : **$2^{10} = 1 024$** et **$2^{20} \approx 1 000 000$**.
>
> **Arbitrage.** Trier puis chercher coûte plus cher qu'une seule recherche séquentielle.
> C'est rentable si l'on fait **beaucoup** de recherches dans le même tableau.

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

**Exercice 1.** Peut-on appliquer directement la recherche dichotomique au tableau
`[4, 1, 9, 3]` ? Que faut-il faire avant ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Dans un tableau trié de 1 000 éléments, combien de comparaisons au pire pour
une recherche dichotomique ? Et pour une recherche séquentielle ?

Dichotomie : ....................  Séquentielle : ....................

Justification : ...................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Déroule la recherche dichotomique de la valeur 13 dans le tableau trié
`[1, 3, 5, 7, 9, 11, 13]`.

| tour | gauche | droite | milieu | tableau[milieu] | décision |
|---:|---:|---:|---:|---:|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

Indice renvoyé : ....................  Nombre de comparaisons : ....................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**Exercice 4.** Ajoute la précondition à la spécification de la fonction, puis un `assert`
qui la vérifie.

```python
def recherche_dichotomique(tableau, valeur):
    """....................................................................
    ...................................................................."""
    assert ....................................................................
    ...
```

### Exercices 3 à 6 — piste Consolider

**Exercice 5.** Écris `recherche_sequentielle(tableau, valeur)` qui renvoie l'indice de la
valeur, ou $- 1$. Quelle est sa précondition ? Combien de comparaisons au pire ?

```python










```

**Exercice 6.** Déroule le tri par insertion sur `[5, 2, 8, 1]`, en comptant les comparaisons
à chaque étape.

| étape | état du tableau | comparaisons faites |
|---:|---|---:|
| départ | `[5, 2, 8, 1]` | 0 |
| 1 | | |
| 2 | | |
| 3 | | |

Total des comparaisons : ....................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

### Exercices 6 à 8 — piste Entretenir

**Exercice 7.** On dispose d'un tableau de n éléments non triés et on prévoit d'y faire k
recherches. À partir de quelle valeur de k vaut-il mieux trier d'abord ? Raisonne avec un tri
en $n \log_2 n$ et une dichotomie en $\log_2 n$.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**Exercice 8.** Exécute les deux fonctions, puis chronomètre-les avec le module `time`.

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

Temps pour `fibo_naif(32)` : ....................

Temps pour `fibo_memo(32)` : ....................

**D'où vient l'écart ?** ....................................................................

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

**Exercice 9.** Recherche dichotomique : l'écrire, puis prouver qu'elle s'arrête et
qu'elle est correcte.

a) Écris `dichotomie(tableau, valeur)`, qui renvoie l'indice de la valeur ou $- 1$.

```python
def dichotomie(tableau, valeur):
    """..............................................................."""










```

b) Écris la précondition et l'`assert` qui la vérifie.

....................................................................................................

....................................................................................................

c) Un **variant de boucle** est une quantité entière positive qui décroît strictement à chaque
tour : son existence prouve que la boucle s'arrête. Donne-en un pour ta fonction.

....................................................................................................

....................................................................................................

d) Un **invariant de boucle** est une propriété vraie avant et après chaque tour : elle sert à
prouver que le résultat est correct. Donne-en un.

....................................................................................................

....................................................................................................

....................................................................................................

e) Sur un tableau trié d'un million d'éléments, combien de comparaisons au pire ? Justifie.

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 10.** Un élève affirme : « le tri par insertion est en $O(n^2)$ et le tri fusion
en $O(n \log n)$, donc le tri fusion est toujours plus rapide ».

a) Sur quelle entrée le tri par insertion effectue-t-il seulement $n - 1$ comparaisons ?

....................................................................................................

....................................................................................................

b) Pour une liste de dix éléments, lequel des deux est le plus rapide en pratique ? Qu'est-ce
que la notation $O$ ne dit pas ?

....................................................................................................

....................................................................................................

....................................................................................................

c) Écris l'énoncé correct.

....................................................................................................

....................................................................................................

d) Un algorithme effectue $3n^2 + 2n$ opérations, un autre $100 n \log_2 n$. À partir de
quelle valeur de n le second devient-il le meilleur ? Estime, puis vérifie par un petit
programme.

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

---

## Partie 4 — Ce que la Terminale en fera

> **Diviser pour régner.** La dichotomie est un cas particulier d'un schéma général : diviser
> le problème en morceaux, résoudre chaque morceau, recombiner. Le tri fusion en est
> l'exemple canonique.
>
> **Programmation dynamique.** L'exercice 8 en est l'illustration : mémoriser les résultats
> déjà calculés dans un **dictionnaire** — celui de la séance 2 — transforme un calcul
> impraticable en calcul instantané.
>
> **Arbres et graphes.** Les parcours en largeur et en profondeur s'analysent avec exactement
> le même raisonnement sur le coût.

---

## Atelier Terminale NSI — 20 minutes

> **Pour qui.** Cet atelier est pour toi si tu as terminé ta piste avant la fin du temps
> différencié, ou si tu suis la piste excellence. Il ne porte pas sur le thème du jour : il
> ouvre une notion du programme de Terminale que la Première n'aborde pas, et que la séance
> rend abordable dès maintenant. Le temps y est prélevé sur la phase différenciée.

**Le lien avec la séance du jour.** Tu viens de comparer le coût de deux algorithmes de recherche. La méthode
**diviser pour régner**, au programme de Terminale, applique à un tri l'idée que tu as
utilisée pour la dichotomie : couper le problème en deux.

Le **tri fusion** coupe la liste en deux moitiés, trie chacune, puis fusionne les deux moitiés
triées.

**a)** Écris la fonction `fusion(A, B)` qui, à partir de deux listes **déjà triées**, renvoie
une liste triée contenant tous leurs éléments.

```python
def fusion(A, B):
    """..............................................................."""








```

**b)** Déroule le tri fusion sur `[5, 2, 8, 1]` : écris les découpages, puis les fusions.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**c)** À chaque niveau de découpage, la fusion parcourt les n éléments une fois. Combien de
niveaux y a-t-il pour une liste de n éléments ? En déduire le coût total.

....................................................................................................

....................................................................................................

....................................................................................................

**d)** Le tri par insertion de la séance coûte $n^2/2$ comparaisons au pire, le tri fusion
$n \log_2 n$. Pour $n = 1000$, calcule les deux et compare.

....................................................................................................

....................................................................................................

**Ce que la Terminale en fera.** Diviser pour régner est l'une des quatre méthodes de
conception au programme, avec les algorithmes gloutons, la programmation dynamique et la
recherche exhaustive. Toutes se jugent au coût, pas au chronomètre.

---

## Partie 5 — Bilan de séance

**Ce que j'ai compris aujourd'hui :** ......................................................

....................................................................................................

**Pourquoi un programme faux est plus dangereux qu'un programme qui plante :**

....................................................................................................

**Ma certitude en algorithmique, aujourd'hui :** $\square$1 $\square$2 $\square$3 $\square$4

**Aide maximale utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune
