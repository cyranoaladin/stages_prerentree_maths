# Terminale NSI — Cahier des cinq séances — Sara Bsiri
## NSI — Stage de pré-rentrée 2026-2027

> **DOCUMENT CONFIDENTIEL — DONNÉES NOMINATIVES**  
> À conserver dans le dossier pédagogique de l'élève. Ne pas diffuser hors de Nexus Réussite et de la famille concernée.

**Élève :** Sara Bsiri  
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
| 1 | Représentation des données et booléens | Installer les repères indispensables sur les types construits. Stabiliser l'acquis encore fragile en représentation binaire. | Installer |
| 2 | Types construits : tableaux, dictionnaires, mutabilité | Transformer la réussite hésitante sur les booléens en réflexe. Ancrer durablement ce qui est déjà compris en programmation. | Consolider |
| 3 | Programmation : fonctions, retour, portée, boucles | Stabiliser l'acquis encore fragile en algorithmique. | Consolider |
| 4 | Algorithmique : préconditions, recherche, tris, coût | Transformer la réussite hésitante sur les données en tables en réflexe. | Consolider |
| 5 | Données en tables, bases de données, systèmes, évaluation | Ancrer durablement ce qui est déjà compris sur l'architecture et les systèmes. | Consolider |

## Comment utiliser ce cahier

- Chaque séance suit le même ordre : réactivation, essentiel, méthode, entraînement, transfert, ouverture, bilan.
- Tu ne traites que les exercices de ta piste. Ils sont déjà sélectionnés ici : ce cahier ne contient pas ceux des autres.
- Écris la propriété ou la relation **avant** de calculer. C'est la seule habitude que ce stage cherche à installer partout.
- Note à chaque fois la lettre de l'aide utilisée. Ce n'est pas un aveu : c'est la mesure de ton autonomie, et on veut la voir baisser d'ici la séance 5.

---

<div class="page-break"></div>

# Séance 1 — Représentation des données et booléens

**Le thème du groupe aujourd'hui :** Représentation des données et booléens.  
**Ton point personnel pendant le temps différencié :** Types construits.  
**Ta piste :** Installer. Écris la propriété ou la relation que tu utilises **avant** de calculer.

## Aujourd'hui, tu vas…

Installer les repères indispensables sur les types construits. Stabiliser l'acquis encore fragile en représentation binaire.

L'entraînement collectif porte sur représentation des données et booléens ; ton exercice personnel, plus bas, porte sur types construits. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Types construits (INSTALLER) · Représentation binaire (CONSOLIDER). Sur ce domaine, tu as réussi 83 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Aucun domaine n'est encore complètement stabilisé — c'est exactement ce que le stage vient faire. Ton point d'appui le plus proche est la représentation binaire : la réussite y est déjà réelle, il reste à l'affermir.

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

## Ton exercice, celui qui vient de ton positionnement

**Types construits — Accéder à une valeur par sa clé dans un dictionnaire.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Soit $d =$ {'x': 10, 'y': 20}. Que vaut d['y'] ? Que se passe-t-il si on écrit d['z'] ? Comment obtenir 0 dans ce cas sans erreur ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Suppose à tort que la clé 'b' n'existe pas.

> **Méthode.** Un dictionnaire s'indexe par clé, pas par position. L'accès à une clé absente lève une erreur.

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

Relis la fiche de cours sur les types construits et note ce qui reste flou : tes questions feront gagner du temps à tout le monde.

Fait : $\square$oui $\square$non    Ce que j'ai noté : ..................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 2 — Types construits : tableaux, dictionnaires, mutabilité

**Le thème du groupe aujourd'hui :** Types construits : tableaux, dictionnaires, mutabilité.  
**Ton point personnel pendant le temps différencié :** Booléens et logique.  
**Ta piste :** Consolider. Justifie par écrit, et sans carte d'aide. Tu sais faire ; il reste à le faire sans hésiter.

## Aujourd'hui, tu vas…

Transformer la réussite hésitante sur les booléens en réflexe. Ancrer durablement ce qui est déjà compris en programmation.

L'entraînement collectif porte sur types construits ; ton exercice personnel, plus bas, porte sur booléens et logique. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Booléens et logique (CONSOLIDER) · Programmation (CONSOLIDER). Sur ce domaine, tu as réussi 100 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Aucun domaine n'est encore complètement stabilisé — c'est exactement ce que le stage vient faire. Ton point d'appui le plus proche est la représentation binaire : la réussite y est déjà réelle, il reste à l'affermir.

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

> **Méthode.** Aucun exemple résolu ne t'est donné ici : sur ce domaine, tu réussis. Ce qui est attendu de toi aujourd'hui, c'est la **rédaction** — la propriété écrite avant le calcul, la conclusion qui répond à la question posée.

## Les pièges de ce domaine

- Croire que `M = L` recopie la liste : les deux noms désignent le même objet.
- Attendre une valeur de retour de `L.append(x)`, qui ne renvoie rien.
- Utiliser une liste muable comme valeur par défaut d'un paramètre.
- Lire une clé absente d'un dictionnaire sans avoir prévu le cas.

## Ton entraînement

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

## Tes exercices, ceux qui viennent de ton positionnement

**1. Booléens et logique — Évaluer une expression booléenne.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réussi, domaine classé en réussite hésitante.

Que vaut l'expression (not True) or (False and True) ? Détailler l'ordre d'évaluation.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Méthode.** Évaluer de l'intérieur vers l'extérieur, en respectant la priorité : not, puis and, puis or.

**2. Booléens et logique — Maîtriser les tables de vérité de la conjonction et de la disjonction.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réussi, domaine classé en réussite hésitante.

L'expression « A ET B » est vraie uniquement lorsque… ? Écrire la table de vérité complète de A ET B, puis celle de non(A ET B).

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Méthode.** Une disjonction n'est fausse que si les deux opérandes sont faux ; une conjonction n'est vraie que si les deux sont vrais. Écrire la table de vérité plutôt que se fier à l'intuition.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Ici, on attend une rédaction complète : la propriété citée, le calcul mené, la conclusion écrite en français.

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

Refais régulièrement un exercice court en représentation binaire, même réussi : c'est la répétition espacée qui transforme « je crois » en « je sais ».

Fait : $\square$oui $\square$non    Ce que j'ai noté : ..................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 3 — Programmation : fonctions, retour, portée, boucles

**Le thème du groupe aujourd'hui :** Programmation : fonctions, retour, portée, boucles.  
**Ton point personnel pendant le temps différencié :** Algorithmique.  
**Ta piste :** Consolider. Justifie par écrit, et sans carte d'aide. Tu sais faire ; il reste à le faire sans hésiter.

## Aujourd'hui, tu vas…

Stabiliser l'acquis encore fragile en algorithmique.

L'entraînement collectif porte sur programmation ; ton exercice personnel, plus bas, porte sur algorithmique. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Algorithmique (CONSOLIDER). Sur ce domaine, tu as réussi 100 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Aucun domaine n'est encore complètement stabilisé — c'est exactement ce que le stage vient faire. Ton point d'appui le plus proche est la représentation binaire : la réussite y est déjà réelle, il reste à l'affermir.

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

> **Reprise.** Tu as travaillé **Types construits** en séance 1. Avant de commencer, écris en une phrase la règle que tu en as retenue — sans regarder tes notes. Si elle ne vient pas, c'est le moment de le dire.

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

> **Méthode.** Aucun exemple résolu ne t'est donné ici : sur ce domaine, tu réussis. Ce qui est attendu de toi aujourd'hui, c'est la **rédaction** — la propriété écrite avant le calcul, la conclusion qui répond à la question posée.

## Les pièges de ce domaine

- Écrire `print` là où l'on attend `return` : la fonction affiche mais ne renvoie rien.
- Réinitialiser un accumulateur à l'intérieur de la boucle au lieu de l'initialiser avant.
- Affecter une variable globale dans une fonction sans la déclarer : Python la rend locale.
- Oublier le cas de la liste vide, qui fait échouer la fonction à l'exécution.

## Ton entraînement

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

## Tes exercices, ceux qui viennent de ton positionnement

**1. Algorithmique — Connaître la précondition de la recherche dichotomique.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réussi, domaine classé en réussite hésitante.

Peut-on appliquer directement la recherche dichotomique au tableau [4, 1, 9, 3] ? Que faut-il faire avant ? Quel est alors le coût total ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Méthode.** La dichotomie compare à l'élément central pour éliminer une moitié : cette élimination n'est valide que sur un tableau trié. La précondition fait partie de la spécification.

**2. Algorithmique — Évaluer le coût d'un algorithme de recherche.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réussi, domaine classé en réussite hésitante.

Dans un tableau trié de 1 000 éléments, combien de comparaisons au pire pour une recherche dichotomique ? Et pour une recherche séquentielle ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Méthode.** À chaque étape la taille est divisée par deux : le nombre d'étapes est de l'ordre de $\log_2(n)$. Retenir les repères : $2^{10} \approx 1 000$, $2^{20} \approx 1 000 000$.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Ici, on attend une rédaction complète : la propriété citée, le calcul mené, la conclusion écrite en français.

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

Chronomètre-toi sur un exercice simple sur les booléens : l'aisance, pas seulement la justesse, est l'objectif.

Fait : $\square$oui $\square$non    Ce que j'ai noté : ..................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 4 — Algorithmique : préconditions, recherche, tris, coût

**Le thème du groupe aujourd'hui :** Algorithmique : préconditions, recherche, tris, coût.  
**Ton point personnel pendant le temps différencié :** Données en tables.  
**Ta piste :** Consolider. Justifie par écrit, et sans carte d'aide. Tu sais faire ; il reste à le faire sans hésiter.

## Aujourd'hui, tu vas…

Transformer la réussite hésitante sur les données en tables en réflexe.

L'entraînement collectif porte sur algorithmique ; ton exercice personnel, plus bas, porte sur données en tables. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Données en tables (CONSOLIDER). Sur ce domaine, tu as réussi 100 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Aucun domaine n'est encore complètement stabilisé — c'est exactement ce que le stage vient faire. Ton point d'appui le plus proche est la représentation binaire : la réussite y est déjà réelle, il reste à l'affermir.

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

> **Reprise.** Tu as travaillé **Booléens et logique** en séance 2. Avant de commencer, écris en une phrase la règle que tu en as retenue — sans regarder tes notes. Si elle ne vient pas, c'est le moment de le dire.

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

> **Méthode.** Aucun exemple résolu ne t'est donné ici : sur ce domaine, tu réussis. Ce qui est attendu de toi aujourd'hui, c'est la **rédaction** — la propriété écrite avant le calcul, la conclusion qui répond à la question posée.

## Les pièges de ce domaine

- Appliquer la dichotomie à un tableau non trié : le résultat est faux sans être détecté.
- Confondre le coût dans le pire des cas et le coût moyen.
- Juger un algorithme au chronomètre sur un seul jeu de données.
- Écrire une boucle dont rien ne garantit qu'elle s'arrête.

## Ton entraînement

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

## Tes exercices, ceux qui viennent de ton positionnement

**1. Données en tables — Distinguer enregistrement et descripteur.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réussi, domaine classé en réussite hésitante.

Un fichier CSV décrit 500 élèves par 6 attributs, avec une ligne d'en-tête. Combien de lignes contient le fichier ? Combien d'enregistrements ? Combien de descripteurs ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Méthode.** Une ligne est un enregistrement (un individu, un objet) ; une colonne est un descripteur (un attribut). La première ligne du fichier contient en général les noms des descripteurs.

**2. Données en tables — Nommer les opérations sur une table.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réussi, domaine classé en réussite hésitante.

Ne garder que les colonnes « nom » et « note » d'une table : de quelle opération s'agit-il ? Et rapprocher une table « élèves » d'une table « classes » par l'identifiant de classe ? Écrire la première en SQL.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Méthode.** Sélection : on choisit des lignes selon une condition. Projection : on choisit des colonnes. Jointure : on rapproche deux tables par un attribut commun.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Ici, on attend une rédaction complète : la propriété citée, le calcul mené, la conclusion écrite en français.

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
**Ton point personnel pendant le temps différencié :** Architecture et systèmes.  
**Ta piste :** Consolider. Justifie par écrit, et sans carte d'aide. Tu sais faire ; il reste à le faire sans hésiter.

## Aujourd'hui, tu vas…

Ancrer durablement ce qui est déjà compris sur l'architecture et les systèmes.

L'entraînement collectif porte sur données en tables, bases de données, systèmes, évaluation ; ton exercice personnel, plus bas, porte sur architecture et systèmes. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Architecture et systèmes (CONSOLIDER). Sur ce domaine, tu as réussi 100 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Aucun domaine n'est encore complètement stabilisé — c'est exactement ce que le stage vient faire. Ton point d'appui le plus proche est la représentation binaire : la réussite y est déjà réelle, il reste à l'affermir.

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

> **Reprise.** Tu as travaillé **Algorithmique** en séance 3. Avant de commencer, écris en une phrase la règle que tu en as retenue — sans regarder tes notes. Si elle ne vient pas, c'est le moment de le dire.

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

> **Méthode.** Aucun exemple résolu ne t'est donné ici : sur ce domaine, tu réussis. Ce qui est attendu de toi aujourd'hui, c'est la **rédaction** — la propriété écrite avant le calcul, la conclusion qui répond à la question posée.

## Les pièges de ce domaine

- Compter la ligne d'en-tête d'un CSV comme un enregistrement.
- Confondre sélection, qui porte sur les lignes, et projection, qui porte sur les colonnes.
- Écrire une jointure sans condition de rapprochement : le résultat croise tout avec tout.
- Supposer qu'un CSV garantit l'unicité des identifiants.

## Ton entraînement

**Exercice 5.** Écris en SQL : « afficher le nom des élèves dont la note est supérieure à 12
**et** qui sont en TG3 ». Puis écris la requête qui donne exactement les élèves **exclus** par
cette condition.

```sql




```

*Indication : pour la seconde, souviens-toi de De Morgan (séance 1).*

**Exercice 6.** Deux tables :

```
eleves(id, nom, classe)
classes(code, professeur, salle)
```

Écris la requête qui affiche, pour chaque élève, son nom et le nom de son professeur.

```sql




```

Quel attribut sert au rapprochement ? ....................

## Tes exercices, ceux qui viennent de ton positionnement

**1. Architecture et systèmes — Identifier les composants du modèle de von Neumann.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réussi, domaine classé en réussite hésitante.

Dans le modèle de von Neumann, quel élément stocke les instructions du programme en cours d'exécution ? Quel élément séquence leur exécution ? Quel est le rôle des bus ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Méthode.** Le processeur contient l'unité arithmétique et logique (les calculs) et l'unité de commande (le séquencement) ; la mémoire contient données et instructions ; les bus les relient.

**2. Architecture et systèmes — Décrire le rôle d'un système d'exploitation.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réussi, domaine classé en réussite hésitante.

Citer trois ressources gérées par un système d'exploitation, puis deux commandes du shell agissant sur le système de fichiers en précisant leur effet.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Méthode.** Le système d'exploitation est l'intermédiaire entre les programmes et le matériel : il gère mémoire, processeur, périphériques, fichiers et processus.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Ici, on attend une rédaction complète : la propriété citée, le calcul mené, la conclusion écrite en français.

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
