# Terminale NSI — Évaluation finale (Corrigé et grille de lecture)

## Principe de lecture

Cette évaluation **n'est pas notée**. Elle est dépouillée avec la matrice réussite $\times$
confiance, exactement comme le positionnement initial. On mesure le **déplacement** de chaque
élève entre les deux.

| | Certitude faible (1-2) | Certitude forte (3-4) |
|---|---|---|
| **Réponse fausse** | Notion absente | Conception erronée |
| **Réponse juste** | Acquis fragile | Acquis disponible |

Sortir d'une case « conception erronée » est la progression la plus importante du stage, même
si la réponse n'est pas encore assurée.

---

## Corrigé

### Exercice 1 — Représentation binaire

a) $37 = 32 + 4 + 1 = 2^5 + 2^2 + 2^0 \to$ **100101**. Vérification : $32 + 0 + 0 + 4 + 0 + 1 = 37 \checkmark$

b) $0x3C = 3 \times 16 + 12 =$ **60**.

c) Sur 8 bits : **256** valeurs, de 0 à 255.

*Ce qui est visé.* Le geste de vérification installé en séance 1. Un élève qui donne la bonne
écriture **sans** faire la vérification demandée n'a pas acquis le contrôle : le noter.

### Exercice 2 — Booléens et logique

a) `True and False` vaut `False` ; `not False` vaut `True` ; `True or False` vaut **`True`**.

b) La négation est `age <= 18 or classe != 'TG3'`. Par la loi de De Morgan, la négation d'une
conjonction est la **disjonction** des négations.

*Erreur attendue.* Écrire `age <= 18 and classe != 'TG3'` : c'est l'erreur exacte visée par la
séance 1, transposée à un contexte SQL.

### Exercice 3 — Types construits

a) `L[2]` vaut **15**, `L[-1]` vaut **16**, `len(L)` vaut **4**. `L[4]` lève une
**`IndexError`** : le dernier indice valide est 3.

b) `L` vaut **`None`**. `append` modifie la liste et **ne renvoie rien** ; l'affectation
écrase donc `L` avec `None`, et la liste est perdue.

c) `d['c'] = 3` puis `d.get('z', 0)`.

*Ce qui est visé.* La question b) est la confrontation de la séance 2, reprise à l'identique.
Un élève qui répond `[4, 8, 15, 16, 23]` a reproduit sa conception initiale.

### Exercice 4 — Programmation

a) `range(1, 5)` produit 1, 2, 3, 4.

| tour | i | s après |
|---:|---:|---:|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 6 |
| 4 | 4 | 24 |

Valeur finale : **24** — c'est 4 factorielle.

b)
```python
def compte_positifs(L):
    """Prend une liste de nombres, renvoie le nombre d'elements strictement positifs."""
    total = 0
    for element in L:
        if element > 0:
            total = total + 1
    return total

assert compte_positifs([-1, 0, 3, 7]) == 2
assert compte_positifs([]) == 0        # cas limite
```

c) Elle renvoie **`None`**. Cela ne l'empêche **pas** de modifier une liste reçue en
paramètre : renvoyer et modifier sont deux choses indépendantes.

*Ce qui est visé.* La question c) est le cœur de la séance 3 et le prérequis de la récursivité
de Terminale. Une réponse partielle — « elle renvoie `None` » sans la seconde partie — signale
que la distinction n'est pas encore nette.

### Exercice 5 — Algorithmique

a) Le tableau doit être **trié**.

b) L'algorithme **ne signale rien** : ni erreur, ni exception, ni ralentissement. Il renvoie
simplement un résultat faux — par exemple « valeur absente » pour une valeur pourtant
présente.

c) De l'ordre de **17 comparaisons**, car $2^{17} \approx 131 000$ dépasse 100 000. Une réponse « environ
17 » ou « une vingtaine » est correcte : c'est un ordre de grandeur qui est demandé, pas une
valeur exacte.

*Ce qui est visé.* La question b) est la confrontation de la séance 4. C'est la seule question
de l'épreuve où la réponse attendue est « il ne se passe rien de visible » — un élève qui
répond « ça plante » ou « ça affiche une erreur » n'a pas intégré le point.

### Exercice 6 — Données en tables et bases de données

a) **201 lignes** (200 données plus l'en-tête), **200 enregistrements**, **5 descripteurs**.

b) « Ne garder que les livres publiés après 2010 » est une **sélection**. « Ne garder que les
colonnes titre et auteur » est une **projection**.

c)
```sql
SELECT titre, auteur FROM livres WHERE annee > 2010 ;
```

*Erreur attendue.* Répondre 200 lignes à la première question, en oubliant l'en-tête ; ou
inverser sélection et projection.

### Exercice 7 — Architecture et systèmes

a) L'**unité arithmétique et logique** effectue les calculs. La **mémoire** stocke les
instructions du programme en cours — c'est le principe même du modèle de von Neumann : données
et instructions y cohabitent.

b) Mémoire, processeur, périphériques, système de fichiers, processus — deux suffisent.

*Ce qui est visé.* Rien de nouveau : le domaine était acquis à 100 % au positionnement. Cet
exercice sert de point d'appui en fin d'épreuve, et vérifie que l'acquis a tenu.

---

## Grille de dépouillement individuelle

| Exercice | Domaine | Juste | Faux | Vide | Certitude | Case de la matrice |
|---:|---|:---:|:---:|:---:|:---:|---|
| 1 | Représentation binaire | $\square$ | $\square$ | $\square$ | ...../4 | |
| 2 | Booléens et logique | $\square$ | $\square$ | $\square$ | ...../4 | |
| 3 | Types construits | $\square$ | $\square$ | $\square$ | ...../4 | |
| 4 | Programmation | $\square$ | $\square$ | $\square$ | ...../4 | |
| 5 | Algorithmique | $\square$ | $\square$ | $\square$ | ...../4 | |
| 6 | Données en tables | $\square$ | $\square$ | $\square$ | ...../4 | |
| 7 | Architecture et systèmes | $\square$ | $\square$ | $\square$ | ...../4 | |

## Comparaison initiale / finale

| Domaine | Case au positionnement initial | Case à l'évaluation finale | Déplacement |
|---|---|---|---|
| Représentation binaire | | | |
| Booléens et logique | | | |
| Types construits | | | |
| Programmation | | | |
| Algorithmique | | | |
| Données en tables | | | |
| Architecture et systèmes | | | |

## Indicateurs transversaux

| Indicateur | Constat |
|---|---|
| Vérification effectuée à l'exercice 1 | $\square$oui $\square$non |
| Table de trace remplie avant exécution (ex. 4a) | $\square$oui $\square$non |
| Spécification écrite (ex. 4b) | $\square$oui $\square$non |
| Deux tests dont un cas limite (ex. 4b) | $\square$oui $\square$non |
| Aide maximale utilisée en séance 5 | ....... |

## Critères de réussite du stage

1. Plus aucune case « conception erronée » sur les domaines traités.
2. La table de trace est faite avant exécution, sans qu'on le demande.
3. Chaque fonction écrite porte une spécification et deux tests.
4. L'aide maximale utilisée a diminué entre la séance 1 et la séance 5.
5. Le plan de septembre est rempli et argumenté.

---
_Document enseignant. Ne pas diffuser aux élèves avant la fin de l'évaluation._
