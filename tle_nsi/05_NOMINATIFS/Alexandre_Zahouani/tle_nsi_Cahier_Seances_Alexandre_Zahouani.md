# Terminale NSI — Cahier des cinq séances — Alexandre Zahouani
## NSI — Stage de pré-rentrée 2026-2027

> **DOCUMENT CONFIDENTIEL — DONNÉES NOMINATIVES**  
> À conserver dans le dossier pédagogique de l'élève. Ne pas diffuser hors de Nexus Réussite et de la famille concernée.

**Élève :** Alexandre Zahouani  
**Groupe :** Groupe 1 — Stages de mathématiques et de NSI  
**Matière :** NSI  
**Organisme :** Nexus Réussite  
**Stage :** 10 heures, 2 heures par jour, 5 jours consécutifs  
**Dates :** du 24 au 28 août 2026

---

## Ton parcours de pré-rentrée

Le thème de chaque séance est commun au groupe. L'objectif, la piste et les exercices sont les tiens : ils viennent de ton positionnement.

| Séance | Thème | Ton objectif | Ta piste |
|---:|---|---|:---:|
| 1 | Représentation des données et booléens | Rectifier une certitude erronée sur les données en tables. | Confronter |
| 2 | Types construits : tableaux, dictionnaires, mutabilité | Faire apparaître, puis lever, l'idée fausse installée en algorithmique. | Confronter |
| 3 | Programmation : fonctions, retour, portée, boucles | Reconstruire une notion tenue pour acquise sur les types construits. | Confronter |
| 4 | Algorithmique : préconditions, recherche, tris, coût | Installer les repères indispensables en représentation binaire. | Installer |
| 5 | Données en tables, bases de données, systèmes, évaluation | Poser les définitions et les gestes de base en programmation. | Installer |

## Comment utiliser ce cahier

- Chaque séance suit le même ordre : réactivation, essentiel, méthode, entraînement, transfert, ouverture, bilan.
- Tu ne traites que les exercices de ta piste. Ils sont déjà sélectionnés ici : ce cahier ne contient pas ceux des autres.
- Écris la propriété ou la relation **avant** de calculer. C'est la seule habitude que ce stage cherche à installer partout.
- Note à chaque fois la lettre de l'aide utilisée. Ce n'est pas un aveu : c'est la mesure de ton autonomie, et on veut la voir baisser d'ici la séance 5.

---

<div class="page-break"></div>

# Séance 1 — Représentation des données et booléens

**Le thème du groupe aujourd'hui :** Représentation des données et booléens.  
**Ton point personnel pendant le temps différencié :** Données en tables.  
**Ta piste :** Confronter. Écris d'abord ce que tu croyais, puis ce qui l'a mis en défaut. C'est cette trace-là qui empêche l'erreur de revenir.

## Aujourd'hui, tu vas…

Rectifier une certitude erronée sur les données en tables.

L'entraînement collectif porte sur représentation des données et booléens ; ton exercice personnel, plus bas, porte sur données en tables. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Données en tables (CONFRONTER). Sur ce domaine, tu as réussi 0 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Booléens et logique — réponses justes, données avec assurance : c'est un vrai point d'appui pour la suite.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. Écrire 13 en binaire.  ....................
2. Que vaut `1011` en base 10 ?  ....................
3. Combien de valeurs sur 4 bits ? Sur 8 bits ?  ....................
4. Que vaut `0xF` en base 10 ?  ....................
5. Combien de bits code un chiffre hexadécimal ?  ....................
6. Que vaut `not (True and False)` ?  ....................
7. Écrire la négation de `a > 3 and b == 2`.  ....................
8. Sur 8 bits non signés, quelle est la plus grande valeur ?  ....................

## Avant tout : ta réponse spontanée

> **Remarque.** Réponds **avant** de lire la suite, et note ta certitude honnêtement. Sur ce domaine, ton positionnement a donné une réponse fausse assurée : c'est cette réponse-là qu'il faut voir apparaître pour pouvoir la reprendre.

**Question 0.** Écris l'entier 22 en binaire.

Ma réponse : ..................................................  Ma certitude : $\square$1 $\square$2 $\square$3 $\square$4

Vérification — recalcule la valeur décimale de **ta** réponse :

....................................................................................................

Est-ce que tu retombes sur 22 ? $\square$oui $\square$non

---

## L'essentiel à retenir

> **Base 2 — méthode 1 : puissances de 2.**
>
> | $2^7$ | $2^6$ | $2^5$ | $2^4$ | $2^3$ | $2^2$ | $2^1$ | $2^0$ |
> |---:|---:|---:|---:|---:|---:|---:|---:|
> | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
>
> $22 = 16 + 4 + 2 \to$ **10110**.
>
> **Base 2 — méthode 2 : divisions successives.** On divise par 2 et on lit les restes
> **de bas en haut**.
>
> **Base 16.** $A = 10$, $B = 11$, $C = 12$, $D = 13$, $E = 14$, **$F = 15$**.
> $0x2A = 2 \times 16 + 10 = 42$. Et $60 = 3 \times 16 + 12 = 0x3C$.
>
> **Le contrôle, toujours le même :** je recalcule la valeur décimale de ce que j'ai écrit.

---

## La méthode, dans l'ordre

1. Pour convertir vers le binaire : divisions successives par 2, puis je lis les restes de bas en haut.
2. Pour convertir vers le décimal : je place les puissances de 2 au-dessus des bits, puis j'additionne celles qui portent un 1.
3. Pour l'hexadécimal : je découpe le binaire en paquets de quatre bits en partant de la droite.
4. Pour une expression booléenne : j'évalue les parenthèses, puis `not`, puis `and`, puis `or`.
5. Je vérifie toute conversion en la refaisant dans l'autre sens.

## Un exemple mené jusqu'au bout

> **Exemple.** Convertir 37 en binaire.
> Puissances utiles : $32 + 4 + 1 = 37$.
> On place un 1 sous 32, 4 et 1, un 0 ailleurs :
>
> | 32 | 16 | 8 | 4 | 2 | 1 |
> |---:|---:|---:|---:|---:|---:|
> | 1 | 0 | 0 | 1 | 0 | 1 |
>
> Résultat : **100101**.
> **Vérification :** $32 + 0 + 0 + 4 + 0 + 1 = 37 \checkmark$
>
> **À toi de transposer**, en gardant les trois étapes : décomposition, écriture,
> vérification.

---

## Les pièges de ce domaine

- Lire les restes des divisions successives de haut en bas au lieu de bas en haut.
- Nier `a and b` en `not a and not b` : De Morgan donne `not a or not b`.
- Confondre le nombre de valeurs représentables et la plus grande valeur : sur n bits, $2^n$ valeurs mais un maximum de $2^n - 1$.
- Découper le binaire en paquets de quatre en partant de la gauche.

## Ton entraînement

**Exercice 1.** Écris 22 en binaire, puis vérifie en recalculant.

Écriture : ....................  Vérification : ....................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Écris 45 en binaire par la méthode des divisions successives.

```{=latex}
\begin{center}
$\begin{aligned}
45 &= 2 \times \rule{16mm}{0.3pt} + \rule{8mm}{0.3pt} \\[2.2mm]
\rule{16mm}{0.3pt} &= 2 \times \rule{16mm}{0.3pt} + \rule{8mm}{0.3pt} \\[2.2mm]
\rule{16mm}{0.3pt} &= 2 \times \rule{16mm}{0.3pt} + \rule{8mm}{0.3pt} \\[2.2mm]
\rule{16mm}{0.3pt} &= 2 \times \rule{16mm}{0.3pt} + \rule{8mm}{0.3pt} \\[2.2mm]
\rule{16mm}{0.3pt} &= 2 \times \rule{16mm}{0.3pt} + \rule{8mm}{0.3pt} \\[2.2mm]
\rule{16mm}{0.3pt} &= 2 \times \rule{16mm}{0.3pt} + \rule{8mm}{0.3pt}
\end{aligned}$
\end{center}
```

Lecture de bas en haut : ....................  Vérification : ....................

**Exercice 3.** Convertis 0x2A en base 10, puis convertis 60 en hexadécimal.

$0x2A =$ ....................    $60 =$ ....................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 4.** Combien de valeurs différentes peut-on coder sur 8 bits ? Quelle est la plus
grande, écrite en base 10 ?

....................................................................................................

## Tes exercices, ceux qui viennent de ton positionnement

**1. Données en tables — Distinguer enregistrement et descripteur.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Un fichier CSV décrit 500 élèves par 6 attributs, avec une ligne d'en-tête. Combien de lignes contient le fichier ? Combien d'enregistrements ? Combien de descripteurs ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** La colonne est verticale ; la ligne décrit un enregistrement.

> **Méthode.** Une ligne est un enregistrement (un individu, un objet) ; une colonne est un descripteur (un attribut). La première ligne du fichier contient en général les noms des descripteurs.

**2. Données en tables — Nommer les opérations sur une table.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Ne garder que les colonnes « nom » et « note » d'une table : de quelle opération s'agit-il ? Et rapprocher une table « élèves » d'une table « classes » par l'identifiant de classe ? Écrire la première en SQL.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Le tri réordonne les lignes sans en supprimer.

> **Méthode.** Sélection : on choisit des lignes selon une condition. Projection : on choisit des colonnes. Jointure : on rapproche deux tables par un attribut commun.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Un capteur transmet ses mesures sur un octet non signé. On relève la
trame `11001010`. a) Quelle valeur décimale ? b) Le constructeur annonce une plage de 0 à
200 : la valeur relevée est-elle plausible ? c) On passe à un codage signé en complément à
deux, sans changer les bits. Que devient la valeur ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

> **Invariants de boucle.** Pour démontrer qu'un algorithme est correct, on exhibe une
> propriété vraie à chaque tour de boucle. Cette propriété est une expression booléenne, et
> sa négation est la condition d'arrêt.
>
> **Requêtes SQL.** `WHERE age > 18 AND classe = 'TG3'` est une expression booléenne. Sa
> négation n'est **pas** `age <= 18 AND classe != 'TG3'` — c'est De Morgan qui donne
> l'écriture correcte.
>
> **Sécurisation des communications.** Le chiffrement repose sur l'arithmétique des entiers
> en machine : la représentation binaire y est un outil de tous les jours.

---

## Prendre du recul

- Comment vérifier une conversion binaire sans refaire les divisions ?

....................................................................................................

- Pourquoi le nombre de valeurs et la valeur maximale ne sont-ils pas le même nombre ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** Écris 26 en binaire.

....................................................................................................

**2.** Que vaut `0x1F` en base 10 ?

....................................................................................................

**3.** Écris la négation de `x >= 0 and y < 10`.

....................................................................................................

### D'ici la prochaine séance — quinze minutes, pas davantage

D'ici la première séance, repère une question sur les données en tables dont la réponse te paraît évidente : on la mettra à l'épreuve ensemble.

Fait : $\square$oui $\square$non    Ce que j'ai noté : ..................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 2 — Types construits : tableaux, dictionnaires, mutabilité

**Le thème du groupe aujourd'hui :** Types construits : tableaux, dictionnaires, mutabilité.  
**Ton point personnel pendant le temps différencié :** Algorithmique.  
**Ta piste :** Confronter. Écris d'abord ce que tu croyais, puis ce qui l'a mis en défaut. C'est cette trace-là qui empêche l'erreur de revenir.

## Aujourd'hui, tu vas…

Faire apparaître, puis lever, l'idée fausse installée en algorithmique.

L'entraînement collectif porte sur types construits ; ton exercice personnel, plus bas, porte sur algorithmique. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Algorithmique (CONFRONTER). Sur ce domaine, tu as réussi 33 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Tu peux t'appuyer sur l'architecture des ordinateurs : les réponses sont justes et assumées, rien à reprendre pour l'instant.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. `L = [4, 7, 2]` : que vaut `L[0]` ? `L[-1]` ?  ....................
2. Que provoque `L[3]` sur cette liste ?  ....................
3. Après `L.append(9)`, que contient `L` ?  ....................
4. Différence entre `L.append(x)` et `L + [x]` ?  ....................
5. `d = {'a': 1}` : que vaut `d['a']` ? Et `d['b']` ?  ....................
6. Comment ajouter la clé `'b'` de valeur 2 à `d` ?  ....................
7. Une chaîne de caractères est-elle muable ?  ....................
8. Après `M = L` puis `M.append(0)`, que contient `L` ?  ....................

## L'essentiel à retenir

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

## La méthode, dans l'ordre

1. J'écris le contenu de la structure avant l'instruction, puis après : deux lignes, pas une.
2. Je distingue ce que l'instruction renvoie de ce qu'elle modifie.
3. Pour un dictionnaire, je vérifie qu'une clé existe avant de la lire.
4. Pour un accès par indice, je vérifie que l'indice est dans les bornes.
5. Je teste sur un cas de taille 1 et sur un cas vide.

## Un exemple mené jusqu'au bout

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

## Les pièges de ce domaine

- Croire que `M = L` recopie la liste : les deux noms désignent le même objet.
- Attendre une valeur de retour de `L.append(x)`, qui ne renvoie rien.
- Utiliser une liste muable comme valeur par défaut d'un paramètre.
- Lire une clé absente d'un dictionnaire sans avoir prévu le cas.

## Ton entraînement

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

## Ton exercice, celui qui vient de ton positionnement

**Algorithmique — Évaluer le coût d'un algorithme de recherche.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Dans un tableau trié de 1 000 éléments, combien de comparaisons au pire pour une recherche dichotomique ? Et pour une recherche séquentielle ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Suppose que l'on divise une seule fois la taille par deux.

> **Méthode.** À chaque étape la taille est divisée par deux : le nombre d'étapes est de l'ordre de $\log_2(n)$. Retenir les repères : $2^{10} \approx 1 000$, $2^{20} \approx 1 000 000$.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

On veut compter les mots d'un texte. Deux structures sont possibles :
une liste de couples `(mot, effectif)` ou un dictionnaire `mot -> effectif`. a) Écris
l'ajout d'un mot dans chacune. b) Laquelle est la plus rapide pour savoir si un mot est déjà
présent ? Pourquoi ? c) Laquelle choisirais-tu, et dans quel cas l'autre serait-elle
préférable ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

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

## Prendre du recul

- Comment savoir si une opération a modifié la structure ou en a créé une nouvelle ?

....................................................................................................

- Quel test simple révèle qu'une liste a été copiée par référence ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** `L = [1, 2, 3]` puis `M = L` puis `M.append(4)`. Que contient `L` ?

....................................................................................................

**2.** Comment tester qu'une clé existe dans un dictionnaire `d` ?

....................................................................................................

**3.** Cite une structure muable et une structure immuable.

....................................................................................................

### D'ici la prochaine séance — quinze minutes, pas davantage

Note deux ou trois réflexes que tu utilises en algorithmique : les écrire permettra de voir lequel bifurque.

Fait : $\square$oui $\square$non    Ce que j'ai noté : ..................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 3 — Programmation : fonctions, retour, portée, boucles

**Le thème du groupe aujourd'hui :** Programmation : fonctions, retour, portée, boucles.  
**Ton point personnel pendant le temps différencié :** Types construits.  
**Ta piste :** Confronter. Écris d'abord ce que tu croyais, puis ce qui l'a mis en défaut. C'est cette trace-là qui empêche l'erreur de revenir.

## Aujourd'hui, tu vas…

Reconstruire une notion tenue pour acquise sur les types construits.

L'entraînement collectif porte sur programmation ; ton exercice personnel, plus bas, porte sur types construits. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Types construits (CONFRONTER). Sur ce domaine, tu as réussi 50 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Booléens et logique — réponses justes, données avec assurance : c'est un vrai point d'appui pour la suite.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. Quelle est la différence entre `return` et `print` ?  ....................
2. Que renvoie une fonction sans `return` ?  ....................
3. `def f(x): return x + 1` : que vaut `f(f(1))` ?  ....................
4. Combien de tours fait `for i in range(3)` ? Quelles valeurs prend `i` ?  ....................
5. Que vaut `i` après `for i in range(5)` ?  ....................
6. Une variable définie dans une fonction est-elle visible en dehors ?  ....................
7. Que fait `while` si la condition est fausse dès le départ ?  ....................
8. Écrire l'en-tête d'une fonction `moyenne` prenant une liste.  ....................

> **Reprise.** Tu as travaillé **Données en tables** en séance 1. Avant de commencer, écris en une phrase la règle que tu en as retenue — sans regarder tes notes. Si elle ne vient pas, c'est le moment de le dire.

## L'essentiel à retenir

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

## La méthode, dans l'ordre

1. J'écris la spécification avant le corps : ce que la fonction prend, ce qu'elle renvoie.
2. Je traite le cas général, puis je reviens sur le cas limite — liste vide, valeur unique.
3. Je déroule une table de trace sur trois tours avant d'exécuter.
4. J'écris au moins deux tests, dont un cas limite.
5. Je vérifie que chaque branche du code se termine par un `return`.

## Un exemple mené jusqu'au bout

> **Exemple.** Somme des carrés de 1 à n.
> ```python
> def somme_carres(n):
>     """Prend un entier n >= 0, renvoie 1^2 + 2^2 + ... + n^2."""
>     total = 0
>     for i in range(1, n + 1):
>         total = total + i * i
>     return total
>
> assert somme_carres(3) == 14   # 1 + 4 + 9
> assert somme_carres(0) == 0    # cas limite
> ```
> Trois points clés : l'accumulateur est initialisé **avant** la boucle ; la borne est
> `n + 1` pour inclure n ; il y a **deux** tests, dont un cas limite.
>
> **À toi de transposer**, en gardant ces trois points.

---

## Les pièges de ce domaine

- Écrire `print` là où l'on attend `return` : la fonction affiche mais ne renvoie rien.
- Réinitialiser un accumulateur à l'intérieur de la boucle au lieu de l'initialiser avant.
- Affecter une variable globale dans une fonction sans la déclarer : Python la rend locale.
- Oublier le cas de la liste vide, qui fait échouer la fonction à l'exécution.

## Ton entraînement

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

## Tes exercices, ceux qui viennent de ton positionnement

**1. Types construits — Accéder à une valeur par sa clé dans un dictionnaire.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Soit $d =$ {'x': 10, 'y': 20}. Que vaut d['y'] ? Que se passe-t-il si on écrit d['z'] ? Comment obtenir 0 dans ce cas sans erreur ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Suppose à tort que la clé 'b' n'existe pas.

> **Méthode.** Un dictionnaire s'indexe par clé, pas par position. L'accès à une clé absente lève une erreur.

**2. Types construits — Créer, modifier et supprimer une entrée de dictionnaire.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Écrire les instructions qui ajoutent à d la clé 'z' de valeur 30, puis suppriment la clé 'x', puis parcourent d en affichant chaque couple clé-valeur.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** == est un test d'égalité, il n'affecte aucune valeur.

> **Méthode.** Une affectation d[clé] $=$ valeur crée l'entrée si elle n'existe pas et la remplace sinon ; del d[clé] la supprime.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Écris une fonction `est_croissante(L)` qui renvoie `True` si la liste est
triée par ordre croissant. a) La fonction. b) Sa spécification. c) Que doit-elle renvoyer sur
une liste vide ? sur une liste d'un seul élément ? Justifie ton choix — il n'y a pas une seule
réponse acceptable, mais il faut le dire dans la spécification.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

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

## Prendre du recul

- Comment savoir si une fonction renvoie bien quelque chose dans tous les cas ?

....................................................................................................

- Quelle question poser à un programme qui « marche » sur un exemple ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** Quelle est la différence entre `return` et `print` ?

....................................................................................................

**2.** Combien de tours fait `for i in range(1, 7, 2)` ?

....................................................................................................

**3.** Une variable affectée dans une fonction est-elle visible en dehors ?

....................................................................................................

### D'ici la prochaine séance — quinze minutes, pas davantage

Ne cherche pas à « réviser plus » sur les types construits : viens avec tes certitudes, ce sont elles qu'on va tester.

Fait : $\square$oui $\square$non    Ce que j'ai noté : ..................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 4 — Algorithmique : préconditions, recherche, tris, coût

**Le thème du groupe aujourd'hui :** Algorithmique : préconditions, recherche, tris, coût.  
**Ton point personnel pendant le temps différencié :** Représentation binaire.  
**Ta piste :** Installer. Écris la propriété ou la relation que tu utilises **avant** de calculer.

## Aujourd'hui, tu vas…

Installer les repères indispensables en représentation binaire.

L'entraînement collectif porte sur algorithmique ; ton exercice personnel, plus bas, porte sur représentation binaire. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Représentation binaire (INSTALLER). Sur ce domaine, tu as réussi 0 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Tu peux t'appuyer sur l'architecture des ordinateurs : les réponses sont justes et assumées, rien à reprendre pour l'instant.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. La recherche dichotomique exige quoi du tableau ?  ....................
2. Sur 1 000 éléments triés, combien de comparaisons au pire en dichotomie ?  ....................
3. Et en recherche séquentielle ?  ....................
4. Qu'est-ce qu'une précondition ?  ....................
5. Que fait `assert` quand la condition est fausse ?  ....................
6. Le tri par insertion sur une liste déjà triée : combien de comparaisons ?  ....................
7. Que compare-t-on pour juger deux algorithmes : le temps mesuré ou le nombre d'opérations ?  ....................
8. Qu'est-ce qu'un invariant de boucle ?  ....................

> **Reprise.** Tu as travaillé **Algorithmique** en séance 2. Avant de commencer, écris en une phrase la règle que tu en as retenue — sans regarder tes notes. Si elle ne vient pas, c'est le moment de le dire.

## L'essentiel à retenir

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

## La méthode, dans l'ordre

1. J'écris la précondition, puis l'`assert` qui la vérifie.
2. Je déroule l'algorithme à la main sur un exemple de quatre éléments.
3. Je compte les comparaisons, pas les secondes.
4. Je cherche le cas le plus favorable et le cas le pire, séparément.
5. Je vérifie que la boucle se termine : quelle quantité décroît à chaque tour ?

## Un exemple mené jusqu'au bout

> **Exemple.** Recherche de 5 dans `[1, 3, 5, 7, 9]`.
>
> | tour | gauche | droite | milieu | tableau[milieu] | décision |
> |---:|---:|---:|---:|---:|---|
> | 1 | 0 | 4 | 2 | 5 | trouvé, on renvoie 2 |
>
> **Exemple.** Recherche de 9 dans `[1, 3, 5, 7, 9]`.
>
> | tour | gauche | droite | milieu | tableau[milieu] | décision |
> |---:|---:|---:|---:|---:|---|
> | 1 | 0 | 4 | 2 | 5 | $5 < 9 \to$ gauche = 3 |
> | 2 | 3 | 4 | 3 | 7 | $7 < 9 \to$ gauche = 4 |
> | 3 | 4 | 4 | 4 | 9 | trouvé, on renvoie 4 |
>
> **À toi de transposer**, en remplissant une ligne par tour et en n'oubliant aucune colonne.

---

## Les pièges de ce domaine

- Appliquer la dichotomie à un tableau non trié : le résultat est faux sans être détecté.
- Confondre le coût dans le pire des cas et le coût moyen.
- Juger un algorithme au chronomètre sur un seul jeu de données.
- Écrire une boucle dont rien ne garantit qu'elle s'arrête.

## Ton entraînement

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

## Tes exercices, ceux qui viennent de ton positionnement

**1. Représentation binaire — Convertir un entier de la base 10 vers la base 2.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Écrire 22 en binaire, puis vérifier en recalculant la valeur décimale.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Vaut 14 : décale d'une unité.

> **Méthode.** Décomposer en somme de puissances de 2 décroissantes, ou diviser successivement par 2 et lire les restes de bas en haut.

**2. Représentation binaire — Convertir entre base 16 et base 10.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Convertir 0x2A en base 10, puis convertir 60 en hexadécimal.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Traite F comme s'il valait 9.

> **Méthode.** En hexadécimal, $A = 10$, $B = 11$, $C = 12$, $D = 13$, $E = 14$, $F = 15$. Chaque position vaut une puissance de 16.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Un site conserve les identifiants de ses membres. On doit décider entre
garder la liste triée et faire une dichotomie, ou la laisser en désordre et faire une
recherche séquentielle. Le site compte $\SI{100000}{}$ membres, avec 10 inscriptions et
$\SI{50000}{}$ recherches par jour. Quelle solution choisis-tu ? Justifie par un ordre de
grandeur du nombre d'opérations, pas par une impression.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

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

## Prendre du recul

- Comment être sûr qu'une boucle s'arrête ?

....................................................................................................

- Pourquoi chronométrer un algorithme ne suffit-il pas à le juger ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** Que faut-il vérifier avant d'appliquer une recherche dichotomique ?

....................................................................................................

**2.** Sur 1000 éléments triés, combien de comparaisons au pire ?

....................................................................................................

**3.** Le tri par insertion sur une liste déjà triée : combien de comparaisons ?

....................................................................................................

### D'ici la prochaine séance — quinze minutes, pas davantage

Et pendant tout le stage, garde le réflexe du bilan : avant de valider une réponse, demande-toi « j'en suis sûr, ou je crois l'être ? ».

Fait : $\square$oui $\square$non    Ce que j'ai noté : ..................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 5 — Données en tables, bases de données, systèmes, évaluation

**Le thème du groupe aujourd'hui :** Données en tables, bases de données, systèmes, évaluation.  
**Ton point personnel pendant le temps différencié :** Programmation.  
**Ta piste :** Installer. Écris la propriété ou la relation que tu utilises **avant** de calculer.

## Aujourd'hui, tu vas…

Poser les définitions et les gestes de base en programmation.

L'entraînement collectif porte sur données en tables, bases de données, systèmes, évaluation ; ton exercice personnel, plus bas, porte sur programmation. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Programmation (INSTALLER). Sur ce domaine, tu as réussi 67 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Booléens et logique — réponses justes, données avec assurance : c'est un vrai point d'appui pour la suite.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. Dans un fichier CSV avec en-tête, combien d'enregistrements pour 501 lignes ?  ....................
2. Qu'est-ce qu'un descripteur ?  ....................
3. Écrire en SQL : afficher tous les champs de la table `eleves`.  ....................
4. Ajouter à cette requête la condition « classe vaut TG3 ».  ....................
5. Comment s'appelle l'opération qui garde certaines lignes ? Certaines colonnes ?  ....................
6. Qu'est-ce qu'une clé primaire ?  ....................
7. Citer les quatre éléments du modèle de von Neumann.  ....................
8. Citer deux ressources gérées par un système d'exploitation.  ....................

> **Reprise.** Tu as travaillé **Types construits** en séance 3. Avant de commencer, écris en une phrase la règle que tu en as retenue — sans regarder tes notes. Si elle ne vient pas, c'est le moment de le dire.

## L'essentiel à retenir

> **Une table.** Une **ligne** est un enregistrement (un individu, un objet). Une **colonne**
> est un descripteur (un attribut). La première ligne d'un CSV contient les noms des
> descripteurs : ce **n'est pas** une donnée.
>
> **Trois opérations.**
>
> | Opération | Ce qu'on garde |
> |---|---|
> | **Sélection** | des **lignes**, selon une condition |
> | **Projection** | des **colonnes** |
> | **Jointure** | on rapproche deux tables par un attribut commun |
>
> **En SQL.**
> ```sql
> SELECT nom, note FROM eleves ;                    -- projection
> SELECT * FROM eleves WHERE note > 12 ;            -- selection
> SELECT nom, note FROM eleves WHERE note > 12 ;    -- les deux
> SELECT eleves.nom, classes.professeur
> FROM eleves JOIN classes ON eleves.classe = classes.code ;   -- jointure
> ```

---

## La méthode, dans l'ordre

1. J'identifie d'abord les tables concernées, puis les colonnes voulues.
2. J'écris `SELECT`, puis `FROM`, puis `WHERE` : dans cet ordre, même si l'exécution diffère.
3. Pour un rapprochement entre deux tables, je repère la clé étrangère avant d'écrire la jointure.
4. Je contrôle le résultat sur trois lignes à la main.
5. En Python, je nomme chaque étape par l'opération relationnelle qu'elle réalise.

## Un exemple mené jusqu'au bout

> **Exemple.** « Afficher le nom et la salle des élèves ayant plus de 12. »
>
> ```sql
> SELECT eleves.nom, classes.salle
> FROM eleves
> JOIN classes ON eleves.classe = classes.code
> WHERE eleves.note > 12 ;
> ```
>
> Trois éléments : la **projection** dans le `SELECT`, la **jointure** dans le `JOIN ... ON`,
> la **sélection** dans le `WHERE`. La condition de jointure dit toujours quel attribut
> correspond à quel autre.
>
> **À toi de transposer**, en identifiant d'abord laquelle des trois opérations tu dois écrire.

---

## Les pièges de ce domaine

- Compter la ligne d'en-tête d'un CSV comme un enregistrement.
- Confondre sélection, qui porte sur les lignes, et projection, qui porte sur les colonnes.
- Écrire une jointure sans condition de rapprochement : le résultat croise tout avec tout.
- Supposer qu'un CSV garantit l'unicité des identifiants.

## Ton entraînement

**Exercice 1.** Un fichier CSV décrit 500 élèves par 6 attributs, avec une ligne d'en-tête.
Combien de lignes ? Combien d'enregistrements ? Combien de descripteurs ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Pour chaque opération, écris son nom.

| Ce qu'on fait | Nom de l'opération |
|---|---|
| Ne garder que les élèves dont la note dépasse 12 | |
| Ne garder que les colonnes « nom » et « note » | |
| Rapprocher la table des élèves et celle des classes | |

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Écris en SQL : « afficher le nom et la note des élèves de la classe TG3 ».

```sql




```

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 4.** Sur l'extrait de la partie 1, applique une sélection `note > 12` **puis** une
projection sur `nom` et `note`. Écris la table obtenue.

| | |
|---|---|
| | |
| | |

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Tes exercices, ceux qui viennent de ton positionnement

**1. Programmation — Distinguer effet de bord et valeur renvoyée.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Soit def $h(L)$: L.append(0). Que vaut r après $r = h([1$, 2]) ? Si on écrit $M = [1$, 2] puis $h(M)$, que contient M ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Confond l'absence de valeur avec une chaîne vide.

> **Méthode.** Sans return, une fonction renvoie None. Une fonction peut modifier un objet mutable reçu en paramètre tout en renvoyant None : ce sont deux choses distinctes.

**2. Programmation — Construire un accumulateur dans une boucle.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réussi avec une certitude de 2/4.

Soit $s = 0$ puis « for i in range(1, 6): $s = s + i$*i ». Que vaut s ? Dresser la table de trace.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Méthode.** Initialiser l'accumulateur avant la boucle, écrire la valeur des variables à chaque tour dans une table de trace pour vérifier.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Une association gère ses adhérents dans un fichier CSV de 4000 lignes.
Elle veut savoir quels adhérents n'ont pas payé leur cotisation cette année, en croisant avec
un second fichier des paiements. a) Écris la requête SQL si les deux fichiers étaient des
tables. b) Décris l'algorithme Python à partir des deux fichiers. c) Que gagne-t-elle à passer
à une base de données ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

> **Bases de données.** Le chapitre reprend les trois opérations sous leurs noms SQL, et ajoute
> le modèle relationnel, les clés primaires et étrangères, les contraintes d'intégrité et le
> système de gestion de bases de données.
>
> **Processus et ordonnancement.** Un système exécute plusieurs programmes « en même temps »
> alors qu'un cœur n'en exécute qu'un : il partage le temps du processeur. Quand deux
> processus s'attendent mutuellement, il y a **interblocage**.
>
> **Réseaux.** Les protocoles de routage (RIP, OSPF) déterminent le chemin d'un message : ce
> sont des **algorithmes de plus court chemin sur un graphe** — le bloc algorithmique de
> l'année.
>
> **Sécurisation des communications.** Le chiffrement repose sur l'arithmétique des entiers,
> donc sur la représentation binaire de la séance 1.
>
> Remarque : les trois dernières ouvertures renvoient à des séances que tu as déjà faites.

---

## Prendre du recul

- Comment vérifier qu'une requête SQL renvoie bien ce qu'on voulait ? (SQL est au programme de Terminale : on l'ouvre ici, on ne l'exige pas.)

....................................................................................................

- Qu'est-ce qui, dans un CSV, peut casser silencieusement un traitement ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** Sélection ou projection : laquelle porte sur les colonnes ?

....................................................................................................

**2.** À quoi sert une clé étrangère ?

....................................................................................................

**3.** Cite deux ressources gérées par le système d'exploitation.

....................................................................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

## Bilan personnel — à remplir à la fin du stage

Rien n'est prérempli ici : ce sont des constats, et ils n'existent qu'après les cinq séances.

| Séance | 1 | 2 | 3 | 4 | 5 |
|---|:---:|:---:|:---:|:---:|:---:|
| Aide maximale utilisée | | | | | |
| Certitude déclarée | | | | | |

**Ce que je consolide vraiment, et que je saurais refaire seul**

....................................................................................................

....................................................................................................

**Le point que je dois encore surveiller à la rentrée**

....................................................................................................

....................................................................................................

**Une méthode que je retiens, écrite avec mes mots**

....................................................................................................

....................................................................................................

**La première notion de Terminale que je me sens prêt à aborder**

....................................................................................................

....................................................................................................
