# Terminale Spécialité Mathématiques — Cahier des cinq séances — Inès Darghouth
## Mathématiques — Stage de pré-rentrée 2026-2027

> **DOCUMENT CONFIDENTIEL — DONNÉES NOMINATIVES**  
> À conserver dans le dossier pédagogique de l'élève. Ne pas diffuser hors de Nexus Réussite et de la famille concernée.

**Élève :** Inès Darghouth  
**Groupe :** Groupe 2 — Stage de mathématiques  
**Matière :** Mathématiques  
**Organisme :** Nexus Réussite  
**Stage :** 10 heures, 2 heures par jour, 5 jours consécutifs  
**Dates :** du 24 au 28 août 2026

---

## Ton parcours de pré-rentrée

Le thème de chaque séance est commun au groupe. L'objectif, la piste et les exercices sont les tiens : ils viennent de ton positionnement.

| Séance | Thème | Ton objectif | Ta piste |
|---:|---|---|:---:|
| 1 | Suites numériques : du sens de variation à la récurrence | Rectifier une certitude erronée sur les suites numériques. | Confronter |
| 2 | Fonction exponentielle : exposants, équations, vers le logarithme | Faire apparaître, puis lever, l'idée fausse installée sur le second degré. | Confronter |
| 3 | Second degré : discriminant, signe du trinôme, tableau de signes | Installer les repères indispensables sur le produit scalaire. | Installer |
| 4 | Dérivation : du nombre dérivé aux variations, ouverture sur la convexité | Poser les définitions et les gestes de base sur la fonction exponentielle. | Installer |
| 5 | Produit scalaire vers l'espace, probabilités, Python, évaluation | Construire les premiers automatismes en dérivation. | Installer |

## Comment utiliser ce cahier

- Chaque séance suit le même ordre : réactivation, essentiel, méthode, entraînement, transfert, ouverture, bilan.
- Tu ne traites que les exercices de ta piste. Ils sont déjà sélectionnés ici : ce cahier ne contient pas ceux des autres.
- Écris la propriété ou la relation **avant** de calculer. C'est la seule habitude que ce stage cherche à installer partout.
- Note à chaque fois la lettre de l'aide utilisée. Ce n'est pas un aveu : c'est la mesure de ton autonomie, et on veut la voir baisser d'ici la séance 5.

---

<div class="page-break"></div>

# Séance 1 — Suites numériques : du sens de variation à la récurrence

**Le thème du groupe aujourd'hui :** Suites numériques : du sens de variation à la récurrence.  
**Ta piste :** Confronter. Écris d'abord ce que tu croyais, puis ce qui l'a mis en défaut. C'est cette trace-là qui empêche l'erreur de revenir.

## Aujourd'hui, tu vas…

Rectifier une certitude erronée sur les suites numériques.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Suites numériques (CONFRONTER). Sur ce domaine, tu as réussi 14 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Pas encore de domaine stabilisé, mais un vrai atout : tu sais dire où ça coince, notamment en dérivation. Cette lucidité est le meilleur point de départ pour progresser vite.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. $(u_n)$ arithmétique, $u_0 = 3$, raison 5. Que vaut $u_4$ ?  ....................
2. $(v_n)$ géométrique, $v_0 = 2$, raison 3. Que vaut $v_3$ ?  ....................
3. Calculer $0{,}5^3$, puis $0{,}5^4$. Laquelle est la plus grande ?  ....................
4. $(w_n)$ géométrique de raison $0{,}9$ et de premier terme positif : croissante ou décroissante ?  ....................
5. Écrire $u_{n+1} - u_n$ pour $u_n = 3n + 1$. Que vaut cette différence ?  ....................
6. Une suite dont la différence $u_{n+1} - u_n$ vaut $- 2$ : que peut-on dire d'elle ?  ....................
7. $u_{n+1}$ et $u_n + 1$ désignent-ils la même chose ?  ....................

## Avant tout : ta réponse spontanée

> **Remarque.** Réponds **avant** de lire la suite, et note ta certitude honnêtement. Sur ce domaine, ton positionnement a donné une réponse fausse assurée : c'est cette réponse-là qu'il faut voir apparaître pour pouvoir la reprendre.

**Question 0.** La suite $(u_n)$ est définie pour tout entier naturel n par $u_n = 0{,}5^n$.
Est-elle croissante ou décroissante ?

Ma réponse : ..................................................  Ma certitude : $\square$1 $\square$2 $\square$3 $\square$4

Maintenant, calcule :

$u_0 =$ ................  $u_1 =$ ................  $u_2 =$ ................  $u_3 =$ ................

Ce que je constate : .....................................................................

....................................................................................................

---

## L'essentiel à retenir

> **Sens de variation d'une suite — méthode générale.**
> On étudie le signe de $u_{n+1} - u_n$.
> Si $u_{n+1} - u_n \geqslant 0$ pour tout n, la suite est croissante.
> Si $u_{n+1} - u_n \leqslant 0$ pour tout n, la suite est décroissante.
>
> **Cas d'une suite géométrique** de premier terme $v_0 > 0$ et de raison $q > 0$ :
> $v_{n+1} - v_n = v_0 q^n (q - 1)$. Comme $v_0 > 0$ et $q^n > 0$, le signe est celui de $q - 1$.
> Donc : $q > 1$ croissante ; $q = 1$ constante ; $0 < q < 1$ décroissante.
> **On compare la raison à 1, pas à 0.**
>
> **Formules explicites.**
> Suite arithmétique : $u_n = u_0 + n \times r$.
> Suite géométrique : $v_n = v_0 \times r^n$.

---

## La méthode, dans l'ordre

1. J'écris la relation qui définit la suite, telle qu'elle est donnée.
2. Je calcule la différence $u_{n+1} - u_n$, sans la simplifier tout de suite.
3. J'étudie le signe de cette différence pour tout entier naturel n.
4. Je conclus sur le sens de variation, en une phrase complète.
5. Je contrôle en calculant les trois premiers termes.

## Un exemple mené jusqu'au bout

> **Exemple.** $(u_n)$ définie par $u_0 = 4$ et $u_{n+1} = u_n + 2n + 1$.
> $u_{n+1} - u_n = 2n + 1$.
> Pour tout entier naturel n, $2n + 1 > 0$.
> Donc la suite est strictement croissante.
> Elle n'est pas arithmétique : l'écart 2n + 1 dépend de n, il n'est pas constant.
>
> **À toi de transposer** à ta suite, en gardant les trois étapes : différence, signe,
> conclusion.

---

## Les pièges de ce domaine

- Comparer la raison à 0 au lieu de la comparer à 1. Une raison de $0{,}9$ est positive, et pourtant la suite décroît.
- Conclure sur les variations sans avoir écrit la différence : l'erreur de méthode devient invisible dans un calcul faux.
- Confondre $u_{n+1}$, le terme suivant, et $u_n + 1$, le terme augmenté de 1.
- Écrire $v_n = v_0 \times n \times r$ au lieu de $v_0 \times r^n$ pour une suite géométrique.

## Ton entraînement

**Exercice 1.** La suite $(u_n)$ est arithmétique, de premier terme $u_0 = - 4$ et de raison 3.
Calculer $u_{12}$.

Propriété utilisée : ......................................................................

Calcul : ...........................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** La suite $(v_n)$ est géométrique, de premier terme $v_0 = 5$ et de raison 1/2.
Calculer $v_3$.

Propriété utilisée : ......................................................................

Calcul : ...........................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Les suites $(w_n)$ et $(t_n)$ sont définies par $w_n = 1{,}2^n$ et $t_n = 3 \times 0{,}8^n$.
Donner le sens de variation de chacune, en justifiant.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 4.** La suite $(u_n)$ est définie par $u_0 = 2$ et, pour tout entier naturel n,
$u_{n+1} = u_n - n^2$. Étudier son sens de variation. Est-elle arithmétique ?

Différence $u_{n+1} - u_n =$ ...........................  Signe : ...........................

Conclusion : ......................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

## Tes exercices, ceux qui viennent de ton positionnement

**1. Suites numériques — Calculer un terme d'une suite géométrique.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

La suite $(v_n)$ est géométrique de premier terme $v_0 = 5$ et de raison 1/2. Calculer $v_3$.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Applique la formule d'une suite arithmétique : calcule $2 + 4 \times 3$.

> **Méthode.** Formule explicite $v_n = v_0 \times r^n$ : la raison est élevée à la puissance n, elle n'est pas multipliée par n.

**2. Suites numériques — Déterminer le sens de variation d'une suite géométrique par sa raison.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Les suites $(w_n)$ et $(t_n)$ sont définies par $w_n = 1{,}2^n$ et $t_n = 3 \times 0{,}8^n$. Donner le sens de variation de chacune, en justifiant.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Croit qu'une raison strictement positive entraîne une suite croissante, sans comparer la raison à 1.

> **Méthode.** Comparer la raison à 1, et non à 0 : pour un premier terme positif, $0 < r < 1$ donne une suite décroissante, $r > 1$ une suite croissante.

**3. Suites numériques — Étudier le sens de variation d'une suite définie par récurrence.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

La suite $(u_n)$ est définie par $u_0 = 2$ et, pour tout entier naturel n, $u_{n+1} = u_n - n^2$. Étudier son sens de variation. Est-elle arithmétique ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Lit $u_{n+1} = u_n + 3n$ comme $u_{n+1} = u_n + 3$ : ne voit pas que l'écart dépend de n.

> **Méthode.** Calculer la différence $u_{n+1} - u_n$ et étudier son signe : c'est la seule méthode fiable pour une suite définie par récurrence.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Une entreprise compte $\SI{1200}{}$ abonnés et en perd $\SI{5}{\percent}$
par mois, mais en gagne 30 nouveaux chaque mois. On note $a_n$ le nombre d'abonnés après n
mois. Écris la relation qui lie $a_{n+1}$ à $a_n$. Cette suite est-elle arithmétique ?
géométrique ? Ni l'une ni l'autre ? Calcule $a_1$ et $a_2$, puis dis si le nombre d'abonnés
augmente ou diminue au début.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

> Une suite **croissante et majorée** converge : elle se rapproche d'une valeur limite sans
> jamais la dépasser. C'est le premier grand résultat de l'année.
>
> Pour démontrer qu'une suite est majorée, on utilise le **raisonnement par récurrence** :
> on vérifie la propriété au rang 0, puis on démontre que si elle est vraie au rang n, elle
> l'est au rang n+1.
>
> Tout cela part du sens de variation. C'est pourquoi il devait être sûr aujourd'hui.

---

## Prendre du recul

- Comment vérifier, sans refaire le calcul, qu'une suite annoncée décroissante l'est bien ?

....................................................................................................

- Quelle donnée de l'énoncé aurais-tu pu ignorer sans changer ta réponse ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** Écris la différence $u_{n+1} - u_n$ pour $u_n = 2 \times 3^n$, sans la calculer.

....................................................................................................

**2.** Une suite géométrique de raison $0{,}95$ et de premier terme 100 : croissante ou décroissante ? Pourquoi ?

....................................................................................................

**3.** En une phrase : à quoi le sens de variation va-t-il servir en Terminale ?

....................................................................................................

### D'ici la prochaine séance — quinze minutes, pas davantage

D'ici la première séance, repère une question sur les suites numériques dont la réponse te paraît évidente : on la mettra à l'épreuve ensemble.

Fait : $\square$oui $\square$non    Ce que j'ai noté : ..................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 2 — Fonction exponentielle : exposants, équations, vers le logarithme

**Le thème du groupe aujourd'hui :** Fonction exponentielle : exposants, équations, vers le logarithme.  
**Ton point personnel pendant le temps différencié :** Second degré.  
**Ta piste :** Confronter. Écris d'abord ce que tu croyais, puis ce qui l'a mis en défaut. C'est cette trace-là qui empêche l'erreur de revenir.

## Aujourd'hui, tu vas…

Faire apparaître, puis lever, l'idée fausse installée sur le second degré.

L'entraînement collectif porte sur fonction exponentielle ; ton exercice personnel, plus bas, porte sur second degré. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Second degré (CONFRONTER). Sur ce domaine, tu as réussi 67 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Pas encore de domaine stabilisé, mais un vrai atout : tu sais dire où ça coince, notamment en dérivation. Cette lucidité est le meilleur point de départ pour progresser vite.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. Que vaut $e^0$ ?  ....................
2. Simplifier $e^3 \times e^{-3}$.  ....................
3. Écrire $e^{2x} \times e^{x}$ sous la forme $e^{ax}$.  ....................
4. Écrire $1/e^{x}$ avec un exposant négatif.  ....................
5. $(e^x)^3$ vaut-il $e^{3x}$ ou $3e^x$ ?  ....................
6. L'équation $e^x = 0$ a-t-elle une solution ?  ....................
7. $e^x$ est-il parfois négatif ?  ....................
8. Résoudre $e^x = e^5$.  ....................

## Avant tout : ta réponse spontanée

> **Remarque.** Réponds **avant** de lire la suite, et note ta certitude honnêtement. Sur ce domaine, ton positionnement a donné une réponse fausse assurée : c'est cette réponse-là qu'il faut voir apparaître pour pouvoir la reprendre.

**Question 0.** Simplifier l'expression $e^{2x} / e^{x - 1}$.

Ma réponse : ..................................................  Ma certitude : $\square$1 $\square$2 $\square$3 $\square$4

Test en $x = 2$ :
- valeur de $e^{2x} / e^{x - 1}$ : ...........................................................
- valeur de ma réponse : .................................................................

Ce que je constate : .....................................................................

---

## L'essentiel à retenir

> **Les quatre règles.** Pour tous réels a et b :
> $\exp(a) \times \exp(b) = \exp(a + b)$
> $\exp(a) / \exp(b) = \exp(a - b)$
> $\exp( - a) = 1 / \exp(a)$
> $(\exp(a))^n = \exp$(na)
>
> **Dans une division, on soustrait — et on garde la parenthèse :**
> $\exp(2x) / \exp(x - 1) = \exp(2x - (x - 1)) = \exp(2x - x + 1) = \exp(x + 1)$.
>
> **Stricte positivité.** Pour tout réel x, $\exp(x) > 0$.
> Conséquences : $\exp(u(x)) = 0$ n'a jamais de solution ; $\exp(u(x)) > 0$ est toujours vraie ;
> on peut simplifier une équation par $\exp(x)$ sans perdre de solution.
>
> **Attention.** $\exp(a + b)$ n'est pas $\exp(a) + \exp(b)$.

---

## La méthode, dans l'ordre

1. Je ramène chaque membre à une seule exponentielle, en additionnant les exposants.
2. Si l'équation est de la forme $e^A = e^B$, j'utilise la stricte croissance : $A = B$.
3. Si un facteur $e^x$ apparaît partout, je le factorise — il ne s'annule jamais.
4. Je résous l'équation restante, qui ne contient plus d'exponentielle.
5. Je vérifie la solution en la remplaçant dans l'énoncé de départ.

## Un exemple mené jusqu'au bout

> **Exemple.** Simplifier $e^{4x} / e^{x - 2}$.
> Division : on soustrait les exposants, avec la parenthèse.
> $4x - (x - 2) = 4x - x + 2 = 3x + 2$.
> Donc $e^{4x} / e^{x - 2} = e^{3x+2}$.
> **Contrôle en $x = 1$ :** $e^4/e^{ - 1} = e^5 \approx 148{,}4 ; e^{3+2} = e^5 \approx 148{,}4$. $\checkmark$
>
> **À toi de transposer**, en gardant les trois étapes : règle, parenthèse, contrôle.

---

## Les pièges de ce domaine

- Écrire $e^{2x} = 2e^x$. Un exposant n'est pas un facteur : $e^{2x} = (e^x)^2$.
- Chercher les valeurs qui annulent $e^x$ : il n'y en a pas, l'exponentielle est strictement positive.
- Simplifier $e^{a} + e^{b}$ en $e^{a+b}$. La règle vaut pour le produit, pas pour la somme.
- Oublier que $e^{-x} = 1/e^{x}$ et traiter le signe moins comme un facteur.

## Ton entraînement

**Exercice 1.** Simplifier $e^{3x} \times e^{1 - x} / e^{x}$ et donner le résultat sous la forme
$e^{ax+b}$.

Règle utilisée : ...........................................................................

Calcul : ...........................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Résoudre dans $\mathbb{R}$ l'équation $e^{x^2 - 1} = 0$, puis l'inéquation $e^x > 0$.

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Simplifier $e^{5x} / e^{2x+3}$.

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 4.** Écrire $1 / e^{3x}$ sous la forme $e^{ax}$.

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

## Ton exercice, celui qui vient de ton positionnement

**Second degré — Tenir compte du signe du coefficient dominant dans le tableau de signes.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Sur quel intervalle le trinôme $- 2x^2 + 8x - 6$ est-il strictement positif ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Applique la règle « positif à l'extérieur des racines » sans tenir compte du signe négatif de a.

> **Méthode.** Quand $a < 0$, le trinôme est positif entre les racines. Écrire le tableau de signes plutôt que retenir une formule.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Une population de bactéries suit $N(t) = 500 e^{0{,}3t}$, où t est en
heures. Au bout de combien d'heures la population dépasse-t-elle 2000 ? Tu ne disposes pas
encore du logarithme : procède par encadrement, en calculant $N(4)$ et $N(5)$. Que faudrait-il
pour répondre exactement ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

> La **fonction logarithme népérien** est introduite comme la fonction qui défait
> l'exponentielle : $\ln(\exp(x)) = x$, et $\exp(\ln x) = x$ pour $x > 0$.
>
> Chaque règle sur exp devient une règle sur ln :
>
> | exp | ln |
> |---|---|
> | $\exp(a + b) = \exp(a) \times \exp(b)$ | ln(ab) $= \ln a + \ln b$ |
> | $\exp(a - b) = \exp(a) / \exp(b)$ | $\ln(a/b) = \ln a - \ln b$ |
> | exp(na) $= (\exp(a))^n$ | $\ln(a^n) = n \ln$ a |
>
> Une erreur sur exp aujourd'hui deviendra la même erreur sur ln en octobre. C'est la raison
> d'être de cette séance.

---

## Prendre du recul

- Comment vérifier qu'une solution d'équation avec exponentielle est correcte ?

....................................................................................................

- Pourquoi l'équation $e^x = k$ n'a-t-elle pas toujours de solution ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** Simplifie $e^{4x} / e^{x-2}$.

....................................................................................................

**2.** Résous $e^{3x} = e^{x+4}$.

....................................................................................................

**3.** Vrai ou faux : $e^{x}$ peut valoir 0. Justifie en une ligne.

....................................................................................................

### D'ici la prochaine séance — quinze minutes, pas davantage

Note deux ou trois réflexes que tu utilises sur le second degré : les écrire permettra de voir lequel bifurque.

Fait : $\square$oui $\square$non    Ce que j'ai noté : ..................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 3 — Second degré : discriminant, signe du trinôme, tableau de signes

**Le thème du groupe aujourd'hui :** Second degré : discriminant, signe du trinôme, tableau de signes.  
**Ton point personnel pendant le temps différencié :** Produit scalaire.  
**Ta piste :** Installer. Écris la propriété ou la relation que tu utilises **avant** de calculer.

## Aujourd'hui, tu vas…

Installer les repères indispensables sur le produit scalaire.

L'entraînement collectif porte sur second degré ; ton exercice personnel, plus bas, porte sur produit scalaire. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Produit scalaire (INSTALLER). Sur ce domaine, tu as réussi 0 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Pas encore de domaine stabilisé, mais un vrai atout : tu sais dire où ça coince, notamment en dérivation. Cette lucidité est le meilleur point de départ pour progresser vite.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. Que vaut le discriminant de $x^2 - 5x + 6$ ?  ....................
2. Combien de racines si $\Delta < 0$ ?  ....................
3. Racines de $x^2 - 4 = 0$.  ....................
4. Le trinôme $x^2 + 1$ s'annule-t-il sur $\mathbb{R}$ ?  ....................
5. Somme et produit des racines de $x^2 - 7x + 12$.  ....................
6. Signe de $- 2x^2 + 3$ quand x est très grand.  ....................
7. Un trinôme de coefficient dominant positif et de discriminant négatif : quel est son signe ?  ....................

> **Reprise.** Tu as travaillé **Suites numériques** en séance 1. Avant de commencer, écris en une phrase la règle que tu en as retenue — sans regarder tes notes. Si elle ne vient pas, c'est le moment de le dire.

## L'essentiel à retenir

> **Résolution.** $\Delta = b^2 - 4$ac.
> $\Delta > 0$ : deux racines $( - b \pm \surd \Delta )/(2a)$. $\Delta = 0$ : une racine double $- b/(2a)$. $\Delta < 0$ : aucune
> racine réelle.
> **Contrôle :** somme des racines = $- b/a$, produit = c/a.
>
> **Signe du trinôme ax^2 + bx + c :**
> il est **du signe de a à l'extérieur des racines**, et **du signe contraire entre les
> racines**.
> Si $\Delta < 0$, il garde le signe de a sur $\mathbb{R}$ tout entier.
>
> **Ensemble solution.** Crochets ouverts pour une inégalité stricte, fermés pour une
> inégalité large. Deux intervalles disjoints se relient par le symbole $\cup$.

---

## La méthode, dans l'ordre

1. J'identifie a, b et c, en respectant les signes.
2. Je calcule $\Delta = b^2 - 4ac$.
3. Je discute : deux racines si $\Delta > 0$, une racine double si $\Delta = 0$, aucune si $\Delta < 0$.
4. Je place les racines dans un tableau de signes, et j'écris d'abord le signe de a.
5. Le trinôme est du signe de a partout, sauf entre les racines.

## Un exemple mené jusqu'au bout

> **Exemple.** Sur quel intervalle $- x^2 + 4x - 3$ est-il strictement positif ?
> $\Delta = 16 - 12 = 4$, $\surd \Delta = 2$. Racines : $( - 4 + 2)/( - 2) = 1$ et $( - 4 - 2)/( - 2) = 3$.
> Ici **$a = - 1 < 0$** : le trinôme est négatif à l'extérieur des racines, positif entre elles.
>
> | | $- \infty$ | | 1 | | 3 | | +$\infty$ |
> |---|---|---|---|---|---|---|---|
> | signe | | $-$ | 0 | + | 0 | $-$ | |
>
> Réponse : le trinôme est strictement positif sur ]1 ; 3[.
> **Contrôle** en $x = 2$ : $- 4 + 8 - 3 = 1 > 0 \checkmark$
>
> **À toi de transposer**, en gardant les quatre étapes : $\Delta$, racines, signe de a, contrôle.

---

## Les pièges de ce domaine

- Dresser un tableau de signes sans y faire figurer le signe de a : le tableau est alors faux une fois sur deux.
- Oublier le signe de b dans $b^2$ : le carré rend positif, mais $- 4ac$ garde le sien.
- Conclure « pas de solution » quand $\Delta < 0$ sans préciser « dans $\mathbb{R}$ ».
- Résoudre une inéquation en gardant le sens de l'inégalité après multiplication par un nombre négatif.

## Ton entraînement

> **Remarque.** Les 1 premier(s) exercice(s) d'application directe ne figurent pas ici : ton positionnement montre que ce geste-là est acquis. On commence donc plus loin dans la série. Si tu bloques malgré tout, demande-les : ils existent.

**Exercice 2.** Combien de solutions réelles l'équation $3x^2 - 6x + 4 = 0$ admet-elle ?
Justifier.

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Résoudre dans $\mathbb{R}$ l'inéquation $x^2 - 9 \geqslant 0$. Compléter le tableau.

| | $- \infty$ | | ....... | | ....... | | +$\infty$ |
|---|---|---|---|---|---|---|---|
| signe de $x^2 - 9$ | | | 0 | | 0 | | |

Ensemble solution : ......................................................................

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 4.** Sur quel intervalle le trinôme $- 2x^2 + 8x - 6$ est-il strictement positif ?

Signe de a : ..........  Racines : ..........

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

## Tes exercices, ceux qui viennent de ton positionnement

**1. Produit scalaire — Calculer un produit scalaire par les coordonnées.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Dans un repère orthonormé, $u( - 2 ; 5)$ et $v(4 ; 1)$. Calculer u·v, puis dire si les vecteurs sont orthogonaux.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Additionne les produits en valeur absolue : ignore le signe de la seconde coordonnée.

> **Méthode.** En repère orthonormé, $u \cdot v = x_u x_v + y_u y_v$. Le résultat est un nombre réel, jamais un vecteur.

**2. Produit scalaire — Utiliser le critère d'orthogonalité.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Déterminer le réel m pour que les vecteurs $u(3 ; m)$ et $v( - 2 ; 6)$ soient orthogonaux.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Confond l'orthogonalité avec l'égalité des normes.

> **Méthode.** $u \cdot v = 0$ est une équivalence : elle sert aussi bien à démontrer une orthogonalité qu'à déterminer un paramètre inconnu.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Un objet lancé vers le haut a pour altitude $h(t) = - 5t^2 + 20t + 1$,
en mètres, t étant en secondes. Pendant combien de temps l'objet est-il au-dessus de
$\SI{16}{\metre}$ ? Rien dans l'énoncé ne dit d'utiliser le second degré : c'est à toi de le
reconnaître.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

> La dérivée d'une fonction polynôme du troisième degré est **un trinôme**. Le tableau de
> signes que tu viens de faire est donc exactement celui dont tu auras besoin pour trouver
> les variations d'une fonction.
>
> En Terminale, on dérive une deuxième fois : le signe de f'' donne les variations de f',
> donc la **convexité** de f. Le même tableau, deux fois par exercice.
>
> Le **théorème des valeurs intermédiaires** s'appuie aussi dessus : si une fonction
> continue est strictement monotone sur un intervalle et y change de signe, l'équation
> $f(x) = 0 y$ a une solution, et une seule.

---

## Prendre du recul

- Comment vérifier deux racines trouvées sans refaire le discriminant ?

....................................................................................................

- Un tableau de signes sans le signe de a : pourquoi est-ce faux une fois sur deux ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** Que vaut le discriminant de $2x^2 - 4x + 5$ ? Combien de racines ?

....................................................................................................

**2.** Signe de $- x^2 + 4$ sur $\mathbb{R}$, en une ligne.

....................................................................................................

**3.** Somme et produit des racines de $x^2 - 9x + 20$, sans les calculer.

....................................................................................................

### D'ici la prochaine séance — quinze minutes, pas davantage

Relis la fiche de cours sur le produit scalaire et note ce qui reste flou : tes questions feront gagner du temps à tout le monde.

Fait : $\square$oui $\square$non    Ce que j'ai noté : ..................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 4 — Dérivation : du nombre dérivé aux variations, ouverture sur la convexité

**Le thème du groupe aujourd'hui :** Dérivation : du nombre dérivé aux variations, ouverture sur la convexité.  
**Ton point personnel pendant le temps différencié :** Fonction exponentielle.  
**Ta piste :** Installer. Écris la propriété ou la relation que tu utilises **avant** de calculer.

## Aujourd'hui, tu vas…

Poser les définitions et les gestes de base sur la fonction exponentielle.

L'entraînement collectif porte sur dérivation ; ton exercice personnel, plus bas, porte sur fonction exponentielle. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Fonction exponentielle (INSTALLER). Sur ce domaine, tu as réussi 50 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Pas encore de domaine stabilisé, mais un vrai atout : tu sais dire où ça coince, notamment en dérivation. Cette lucidité est le meilleur point de départ pour progresser vite.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. Dérivée de $x^3$.  ....................
2. Dérivée de $5x$.  ....................
3. Dérivée d'une constante.  ....................
4. Formule de $(uv)'$.  ....................
5. Formule de $(u/v)'$.  ....................
6. Si $f'$ est négative sur un intervalle, que fait f ?  ....................
7. $f'(2) = 0$ : que peut-on affirmer, et que ne peut-on pas affirmer ?  ....................
8. Que représente $f'(a)$ pour la courbe de f au point d'abscisse a ?  ....................

> **Reprise.** Tu as travaillé **Second degré** en séance 2. Avant de commencer, écris en une phrase la règle que tu en as retenue — sans regarder tes notes. Si elle ne vient pas, c'est le moment de le dire.

## L'essentiel à retenir

> **Nombre dérivé.** $f'(a)$ est le coefficient directeur de la tangente à la courbe au point
> d'abscisse a.
> Équation de la tangente : **$y = f'(a)(x - a) + f(a)$**.
>
> **Formules.**
> (u + v)' = u' + v' · (ku)' = ku' · (uv)' = u'v + uv' · (u/v)' = (u'$v -$ uv')$/v^2$
>
> **Signe et variations.**
> Là où $f' > 0$, f est strictement **croissante**.
> Là où $f' < 0$, f est strictement **décroissante**.
> Le signe de f' ne dit **rien** du signe de f.

---

## La méthode, dans l'ordre

1. Je repère la forme de l'expression : produit, quotient, ou somme de termes simples.
2. Je pose u et v à part, puis j'écris $u'$ et $v'$ avant toute chose.
3. J'applique la formule correspondante, sans développer tout de suite.
4. Je factorise la dérivée : le signe se lit sur une forme factorisée, jamais sur une forme développée.
5. Je dresse le tableau de signes de la dérivée, puis celui des variations.

## Un exemple mené jusqu'au bout

> **Exemple.** $f(x) = (x + 4)/(x - 1)$ sur $]1 ; + \infty [$.
> $u = x + 4$, $u' = 1 ; v = x - 1$, $v' = 1$.
> (u/v)' = (u'$v -$ uv')$/v^2 = (1 \times (x - 1) - (x + 4) \times 1)/(x - 1)^2$
> = $(x - 1 - x - 4)/(x - 1)^2 =$ **$- 5/(x - 1)^2$**.
> Le numérateur est constant négatif, le dénominateur est un carré : $f' < 0$, donc f est
> strictement décroissante sur $]1 ; + \infty [$.
>
> **À toi de transposer**, en gardant les quatre étapes : u, v, u', v' ; formule ;
> simplification du numérateur ; signe.

---

## Les pièges de ce domaine

- Écrire $(uv)' = u'v'$. La dérivée d'un produit n'est pas le produit des dérivées.
- Conclure sur les variations à partir d'une dérivée développée, dont le signe ne se lit pas.
- Déduire de $f'(a) = 0$ qu'il y a un extremum : il faut que $f'$ change de signe.
- Confondre $f(a)$, l'ordonnée, et $f'(a)$, la pente de la tangente.

## Ton entraînement

> **Remarque.** Les 2 premier(s) exercice(s) d'application directe ne figurent pas ici : ton positionnement montre que ce geste-là est acquis. On commence donc plus loin dans la série. Si tu bloques malgré tout, demande-les : ils existent.

**Exercice 3.** Soit $f(x) = x^3 - 12x$. Déterminer l'intervalle sur lequel f est décroissante.

$f'(x) =$ ....................  Forme factorisée : ....................

| | $- \infty$ | | ....... | | ....... | | +$\infty$ |
|---|---|---|---|---|---|---|---|
| signe de $f'(x)$ | | | 0 | | 0 | | |
| variations de f | | | | | | | |

Conclusion : ......................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 4.** On sait que g' est strictement positive sur ]0 ; 5[. Que peut-on affirmer
sur les variations de g ? Peut-on en déduire le signe de g ? Justifier par un exemple.

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

## Ton exercice, celui qui vient de ton positionnement

**Fonction exponentielle — Utiliser la stricte positivité de la fonction exponentielle.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Résoudre dans $\mathbb{R}$ l'équation $e^{x^2 - 1} = 0$, puis l'inéquation $e^x > 0$.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Confond la limite nulle en $- \infty$ avec l'atteinte effective de la valeur 0.

> **Méthode.** Pour tout réel x, $e^x > 0$. Toute équation de la forme $e^{quelque chose} = 0$ ou = nombre négatif n'a aucune solution.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Une boîte sans couvercle est fabriquée dans un carré de carton de
$\SI{20}{\centi\metre}$ de côté, en découpant un carré de côté x à chaque coin. Son volume
vaut $V(x) = x(20 - 2x)^2$. Pour quelle valeur de x le volume est-il maximal ? L'énoncé ne
dit pas de dériver : à toi de décider.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

> En Terminale, on dérive **une deuxième fois**.
>
> Le signe de f'' donne les variations de f'. Là où f'' $\geqslant 0$, f' croît : la courbe de f
> tourne vers le haut, on dit que f est **convexe**. Là où f'' $\leqslant 0$, f est **concave**. Le
> point où f'' change de signe est un **point d'inflexion**.
>
> C'est exactement le geste d'aujourd'hui, fait une fois de plus. Pour qu'il fonctionne au
> deuxième étage, il doit être sûr au premier.

---

## Prendre du recul

- Comment savoir si un extremum trouvé est un maximum et non un minimum ?

....................................................................................................

- Pourquoi factoriser la dérivée avant d'étudier son signe ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** Dérive $f(x) = (2x + 1)(x - 3)$.

....................................................................................................

**2.** $f'$ est négative sur $]0 ; 3[$ : que fait f sur cet intervalle ?

....................................................................................................

**3.** $f'(2) = 0$ : peut-on affirmer qu'il y a un extremum en 2 ? Justifie.

....................................................................................................

### D'ici la prochaine séance — quinze minutes, pas davantage

Et pendant tout le stage, garde le réflexe du bilan : avant de valider une réponse, demande-toi « j'en suis sûr, ou je crois l'être ? ».

Fait : $\square$oui $\square$non    Ce que j'ai noté : ..................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 5 — Produit scalaire vers l'espace, probabilités, Python, évaluation

**Le thème du groupe aujourd'hui :** Produit scalaire vers l'espace, probabilités, Python, évaluation.  
**Ton point personnel pendant le temps différencié :** Dérivation.  
**Ta piste :** Installer. Écris la propriété ou la relation que tu utilises **avant** de calculer.

## Aujourd'hui, tu vas…

Construire les premiers automatismes en dérivation.

L'entraînement collectif porte sur produit scalaire vers l'espace, probabilités, python, évaluation ; ton exercice personnel, plus bas, porte sur dérivation. Les deux sont à traiter : le premier avec le groupe, le second pendant le temps différencié.

> **Remarque.** Ce que ton positionnement a montré sur ce point : Dérivation (INSTALLER). Sur ce domaine, tu as réussi 82 % des questions du positionnement. C'est de là que part ta séance.

> **Point d'appui.** Pas encore de domaine stabilisé, mais un vrai atout : tu sais dire où ça coince, notamment en dérivation. Cette lucidité est le meilleur point de départ pour progresser vite.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. $u(3 ; - 1)$ et $v(2 ; 6)$ : calculer $u \cdot v$.  ....................
2. Le produit scalaire est-il un nombre ou un vecteur ?  ....................
3. Deux vecteurs non nuls orthogonaux : que vaut leur produit scalaire ?  ....................
4. $P(A) = 0{,}3$ : que vaut $P(\bar{A})$ ?  ....................
5. A et B incompatibles : que vaut $P(A \cap B)$ ?  ....................
6. Formule de $P(A \cup B)$.  ....................
7. Que renvoie `range(2, 10, 3)` ?  ....................
8. Une variable aléatoire prend les valeurs 0 et 2 avec les probabilités $0{,}4$ et $0{,}6$ : que vaut son espérance ?  ....................

> **Reprise.** Tu as travaillé **Produit scalaire** en séance 3. Avant de commencer, écris en une phrase la règle que tu en as retenue — sans regarder tes notes. Si elle ne vient pas, c'est le moment de le dire.

## La méthode, dans l'ordre

1. Pour le produit scalaire : j'écris les coordonnées des deux vecteurs, puis j'applique la formule.
2. Pour l'orthogonalité : je pose le produit scalaire égal à zéro et je résous.
3. Pour une probabilité : je décris l'expérience, puis je choisis entre arbre et tableau.
4. Pour une espérance : je dresse la loi de probabilité complète avant de sommer.
5. Pour un programme : je déroule une table de trace sur trois tours avant d'exécuter.

## Un exemple mené jusqu'au bout

> **Exemple — détermination d'un paramètre.**
> Pour quel réel k les vecteurs $u(4 ; k)$ et $v(3 ; - 6)$ sont-ils orthogonaux ?
> Le critère $u \cdot v = 0$ s'écrit : $4 \times 3 + k \times ( - 6) = 0$, soit $12 - 6k = 0$, donc **$k = 2$**.
> Contrôle : $u(4 ; 2)$ et $v(3 ; - 6)$ donnent $12 - 12 = 0 \checkmark$
>
> **À toi de transposer** en gardant les trois étapes : écrire le critère comme une équation,
> résoudre, contrôler.

---

## Les pièges de ce domaine

- Annoncer un vecteur comme résultat d'un produit scalaire : c'est un nombre.
- Confondre événements incompatibles et événements indépendants.
- Oublier que la somme des probabilités d'une loi vaut 1, et ne pas s'en servir pour contrôler.
- Dans une boucle `for`, confondre le nombre d'itérations et la dernière valeur prise.

## Ton entraînement

### Partie 1 — Produit scalaire

> **Rappel.** En repère orthonormé : $u \cdot v = x_u x_v + y_u y_v$. **Le résultat est un nombre.**
> Deux vecteurs non nuls sont orthogonaux **si et seulement si** $u \cdot v = 0$.

**Exercice 1.** $u( - 2 ; 5)$ et $v(4 ; 1)$. Calculer u·v, puis dire si les vecteurs sont
orthogonaux.

$u \cdot v =$ ...........................................  Conclusion : ...........................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Déterminer le réel m pour que $u(3 ; m)$ et $v( - 2 ; 6)$ soient orthogonaux.

Équation posée : ..........................................................................

$m =$ ...........................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** ABC est un triangle avec $A(1 ; 2)$, $B(4 ; 3)$ et $C(2 ; 8)$. Le triangle est-il
rectangle en A ?

Vecteurs à utiliser : ....................................................................

Calcul : ...........................................................................................

Conclusion : ......................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

### Partie 2 — Probabilités

> **Rappels.**
> $P(A \cap B) = P(A) \times P_A(B)$.
> Probabilités totales : $P(B) = P(A) \times P_A(B) + P(\overline{A}) \times P_{\overline{A}}(B)$.
> A et B sont **indépendants** lorsque $P_A(B) = P(B)$.
> Espérance d'une variable aléatoire : $E(X) = \sum x_i \times P(X = x_i)$.

**Exercice 4.** Une urne contient 3 boules rouges et 2 boules noires. On tire deux boules
successivement, **sans remise**. Construire l'arbre pondéré, puis calculer la probabilité de
tirer deux boules rouges.

Arbre :

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

P(deux rouges) $=$ ...........................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 5.** Deux événements A et B de probabilités non nulles sont **incompatibles**.
Peuvent-ils être indépendants ? Justifier en calculant $P_A(B)$.

....................................................................................................

....................................................................................................

**Exercice 6.** Une variable aléatoire X prend les valeurs 0, 1 et 3 avec les probabilités
0,5 ; 0,3 et 0,2. Calculer $E(X)$ et interpréter le résultat.

$E(X) =$ ...........................  Interprétation : ...........................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

### Partie 3 — Python

**Exercice 7.** Compléter le programme suivant pour qu'il renvoie le terme de rang n d'une
suite géométrique de premier terme v0 et de raison q.

```python
def terme_geometrique(v0, q, n):
    v = ..........
    for _ in range(..........):
        v = ..........
    return v
```

Tester avec `terme_geometrique(2, 3, 4)`. Le résultat doit valoir : ...........................

**Exercice 8.** Ce programme cherche le premier rang à partir duquel la suite dépasse un
seuil.

```python
def premier_rang_depassement(v0, q, seuil):
    v = v0
    n = 0
    while v <= seuil:
        v = q * v
        n = n + 1
    return n
```

a) Que renvoie `premier_rang_depassement(2, 3, 100)` ? ...........................

b) Que se passe-t-il si $q = 0{,}5$ et seuil = 100, avec $v0 = 2$ ? Pourquoi ?

....................................................................................................

....................................................................................................

c) Quel lien avec le sens de variation vu en séance 1 ?

....................................................................................................

....................................................................................................

## Tes exercices, ceux qui viennent de ton positionnement

**1. Dérivation — Déduire les variations du signe de la dérivée.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réponse fausse.

Soit $f(x) = x^3 - 12x$. Déterminer l'intervalle sur lequel f est décroissante.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Piège.** Suppose une fonction polynomiale de degré 3 monotone sur $\mathbb{R}$, sans étude de signe.

> **Méthode.** Calculer f', la factoriser, dresser le tableau de signes, puis lire les variations. f décroît là où $f' \leqslant 0$.

**2. Dérivation — Dériver un quotient.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réussi avec une certitude de 1/4.

Soit $f(x) = (2x - 1)/(x + 3)$, définie sur $] - 3 ; + \infty [$. Calculer $f'(x)$ et donner son signe.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Méthode.** Appliquer (u/v)' = (u'$v -$ uv')$/v^2$. L'ordre du numérateur n'est pas commutatif : u'v vient en premier.

**3. Dérivation — Interpréter le nombre dérivé.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réussi avec une certitude de 2/4.

Une fonction h vérifie $h(3) = - 2$ et $h'(3) = 5$. Que représente le nombre 5 ? Donner l'équation de la tangente à la courbe de h au point d'abscisse 3.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Méthode.** $f'(a)$ est la limite du taux de variation en a : c'est un coefficient directeur, pas une valeur de la fonction.

### Si tu bloques — ouvre les indices dans l'ordre

N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne se traitent pas de la même façon.

- **Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. Écris le nom de la propriété avant toute chose.
- **Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et applique la première à ton énoncé.
- **Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y arrives, la suite t'appartient.

Indice qui m'a débloqué : $\square$1 $\square$2 $\square$3 $\square$aucun, j'ai trouvé seul

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Un jeu propose de tirer une carte dans un jeu de 32. Tu gagnes 5 euros si
c'est un cœur, 10 euros si c'est l'as de pique, et tu perds 2 euros sinon. Le jeu
est-il favorable au joueur ? Décide quelle notion utiliser, puis conclus.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

> Dans l'espace, le produit scalaire s'écrit avec trois coordonnées :
> $u \cdot v = x_u x_v + y_u y_v + z_u z_v$.
>
> Un vecteur **normal** à un plan est orthogonal à deux vecteurs directeurs de ce plan. Si
> $n(a ; b ; c)$ est normal au plan P et si $A(x_0 ; y_0 ; z_0)$ appartient à P, alors P a pour
> équation cartésienne :
> $a(x - x_0) + b(y - y_0) + c(z - z_0) = 0$.
>
> Autrement dit : **l'équation d'un plan est un produit scalaire nul.** Le critère que tu
> viens d'utiliser est l'outil principal de toute la géométrie de Terminale.

---

## Prendre du recul

- Comment contrôler qu'une loi de probabilité est complète ?

....................................................................................................

- Un produit scalaire nul : que peux-tu affirmer, et que ne peux-tu pas affirmer ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** $u(2 ; - 3)$ et $v(6 ; 4)$ : ces vecteurs sont-ils orthogonaux ?

....................................................................................................

**2.** $P(A) = 0{,}4$, $P(B) = 0{,}5$, A et B incompatibles : que vaut $P(A \cup B)$ ?

....................................................................................................

**3.** Une espérance négative : qu'est-ce que cela signifie pour un jeu ?

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
