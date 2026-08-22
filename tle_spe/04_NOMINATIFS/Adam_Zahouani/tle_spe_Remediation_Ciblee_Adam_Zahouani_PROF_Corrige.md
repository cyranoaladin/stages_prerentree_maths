# Terminale Spécialité Mathématiques — Plan de remédiation ciblée — Adam Zahouani (Corrigé enseignant)
## Mathématiques — Parcours personnalisé

> **DOCUMENT CONFIDENTIEL — DONNÉES NOMINATIVES**  
> À conserver dans le dossier pédagogique de l'élève. Ne pas diffuser hors de Nexus Réussite et de la famille concernée.

**Élève :** Adam Zahouani  
**Matière :** Mathématiques  
**Diagnostic du :** 2026-08-13  
**Source :** `Bilans/bilan-nexus-eleve_adam_zahouani_maths.pdf`

## Profil de l'élève, en une page

| Domaine | Réussite | Situation | Posture de travail |
|---|---:|---|---|
| Second degré | 100 % | Acquis disponible | **ENTRETENIR** |
| Dérivation | 72,7 % | Difficulté repérée, sans fausse certitude | **INSTALLER** |
| Fonction exponentielle | 0 % | Certitude à revoir | **CONFRONTER** |
| Suites numériques | 42,9 % | Difficulté repérée, sans fausse certitude | **INSTALLER** |
| Produit scalaire | 100 % | Acquis disponible | **ENTRETENIR** |

**Ordre de traitement.** Fonction exponentielle (CONFRONTER) $\to$ Dérivation (INSTALLER) $\to$ Suites numériques (INSTALLER)

**Calibration de la confiance.** Point fort : ton auto-évaluation est fiable — tu sais globalement ce que tu sais. C'est un vrai atout pour réviser juste, sans perdre de temps.

## Composition de la feuille

| # | Item du positionnement | Domaine | Compétence | Motif de sélection |
|---:|---:|---|---|---|
| 1 | item 11 | Fonction exponentielle | Appliquer les règles de calcul sur les exposants | réponse fausse |
| 2 | item 12 | Fonction exponentielle | Utiliser la stricte positivité de la fonction exponentielle | réponse fausse |
| 3 | item 7 | Dérivation | Déduire les variations du signe de la dérivée | réponse fausse |
| 4 | item 8 | Dérivation | Distinguer le signe de la dérivée et le signe de la fonction | réponse fausse |
| 5 | item 15 | Suites numériques | Déterminer le sens de variation d'une suite géométrique par sa raison | réponse fausse |
| 6 | item 16 | Suites numériques | Étudier le sens de variation d'une suite définie par récurrence | réponse fausse |

Chaque exercice est la **variante** de l'item que l'élève a manqué ou réussi sans assurance : même compétence, énoncé différent. La feuille d'un autre élève n'a donc pas la même composition.

<div class="page-break"></div>

## Corrigé

### Exercice 1 — Fonction exponentielle

**Énoncé.** Simplifier l'expression $e^{3x} \times e^{1 - x} / e^{x}$ et donner le résultat sous la forme $e^{ax+b}$.

**Corrigé.** On additionne les exposants du produit puis on soustrait celui du dénominateur : $3x + (1 - x) - x = x + 1$. L'expression vaut donc $e^{x+1}$.

**Geste à installer.** Diviser deux exponentielles revient à soustraire les exposants, en gardant la parenthèse autour de l'exposant soustrait.

**Erreur à surveiller chez cet élève.** Additionne les exposants au lieu de les soustraire lors de la division. (constatée à l'item 11 du positionnement, donné avec une certitude de 2/4.)

### Exercice 2 — Fonction exponentielle

**Énoncé.** Résoudre dans $\mathbb{R}$ l'équation $e^{x^2 - 1} = 0$, puis l'inéquation $e^x > 0$.

**Corrigé.** La fonction exponentielle est strictement positive sur $\mathbb{R}$ : elle ne s'annule jamais, donc l'équation $e^{x^2 - 1} = 0$ n'a aucune solution. Pour la même raison, l'inéquation $e^x > 0$ est vraie pour tout réel x : son ensemble de solutions est $\mathbb{R}$.

**Geste à installer.** Pour tout réel x, $e^x > 0$. Toute équation de la forme $e^{quelque chose} = 0$ ou = nombre négatif n'a aucune solution.

**Erreur à surveiller chez cet élève.** Associe l'équation à la valeur remarquable $e^1 = e$ sans traiter la question posée. (constatée à l'item 12 du positionnement, donné avec une certitude de 4/4.)

### Exercice 3 — Dérivation

**Énoncé.** Soit $f(x) = x^3 - 12x$. Déterminer l'intervalle sur lequel f est décroissante.

**Corrigé.** $f'(x) = 3x^2 - 12 = 3(x - 2)(x + 2)$, qui s'annule en $- 2$ et 2 et est négatif entre ces valeurs. La fonction f est donc décroissante sur $[ - 2 ; 2]$.

**Geste à installer.** Calculer f', la factoriser, dresser le tableau de signes, puis lire les variations. f décroît là où $f' \leqslant 0$.

**Erreur à surveiller chez cet élève.** Inverse le lien entre le signe de f' et le sens de variation. (constatée à l'item 7 du positionnement, donné avec une certitude de 2/4.)

### Exercice 4 — Dérivation

**Énoncé.** On sait que g' est strictement positive sur ]0 ; 5[. Que peut-on affirmer sur les variations de g ? Peut-on en déduire le signe de g sur cet intervalle ?

**Corrigé.** g est strictement croissante sur ]0 ; 5[. En revanche, on ne peut rien affirmer sur le signe de g : la fonction $g(x) = x - 10$ a une dérivée strictement positive et reste négative sur ]0 ; 5[.

**Geste à installer.** Le signe de f' renseigne sur le sens de variation de f, jamais sur le signe de f. Ce sont deux informations indépendantes.

**Erreur à surveiller chez cet élève.** Confond le signe de la dérivée avec le signe de la fonction elle-même. (constatée à l'item 8 du positionnement, donné avec une certitude de 2/4.)

### Exercice 5 — Suites numériques

**Énoncé.** Les suites $(w_n)$ et $(t_n)$ sont définies par $w_n = 1{,}2^n$ et $t_n = 3 \times 0{,}8^n$. Donner le sens de variation de chacune, en justifiant.

**Corrigé.** Les deux suites sont géométriques de premier terme strictement positif. Pour $(w_n)$, la raison 1,2 est strictement supérieure à 1 : la suite est strictement croissante. Pour $(t_n)$, la raison 0,8 vérifie $0 < 0{,}8 < 1$ : la suite est strictement décroissante.

**Geste à installer.** Comparer la raison à 1, et non à 0 : pour un premier terme positif, $0 < r < 1$ donne une suite décroissante, $r > 1$ une suite croissante.

**Erreur à surveiller chez cet élève.** Croit qu'une raison strictement positive entraîne une suite croissante, sans comparer la raison à 1. (constatée à l'item 15 du positionnement, donné avec une certitude de 3/4.)

### Exercice 6 — Suites numériques

**Énoncé.** La suite $(u_n)$ est définie par $u_0 = 2$ et, pour tout entier naturel n, $u_{n+1} = u_n - n^2$. Étudier son sens de variation. Est-elle arithmétique ?

**Corrigé.** $u_{n+1} - u_n = - n^2$, qui est négatif ou nul pour tout entier naturel n : la suite est décroissante (au sens large). Elle n'est pas arithmétique, car l'écart entre deux termes consécutifs dépend de n et n'est donc pas constant.

**Geste à installer.** Calculer la différence $u_{n+1} - u_n$ et étudier son signe : c'est la seule méthode fiable pour une suite définie par récurrence.

**Erreur à surveiller chez cet élève.** Ne calcule pas le signe de $u_{n+1} - u_n$ avant de conclure. (constatée à l'item 16 du positionnement, donné avec une certitude de 2/4.)

## Relevé de maîtrise

| Exercice | Juste sans aide | Juste avec aide | Erreur de procédure | Erreur de calcul | À reprendre |
|---:|:---:|:---:|:---:|:---:|:---:|
| 1 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 2 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 3 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 4 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 5 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 6 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |

## Conduite recommandée

### Fonction exponentielle — CONFRONTER

Une réponse fausse a été donnée avec assurance. On part d'un cas qui met la conviction en défaut, on fait verbaliser le raisonnement, puis on reconstruit la notion avant tout entraînement.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** La fonction logarithme népérien est introduite en Terminale comme réciproque de l'exponentielle : toute erreur sur les règles d'exposants se propage aux règles sur ln. L'exponentielle est aussi la solution de référence des équations différentielles $y' =$ ay + b et le support des croissances comparées.

### Dérivation — INSTALLER

La difficulté est repérée et assumée : il n'y a aucune fausse certitude à défaire. On pose les définitions utiles, on montre des exemples résolus, puis on entraîne court et souvent.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** Toute l'analyse de Terminale s'appuie dessus : dérivée d'une fonction composée, dérivée seconde et convexité, étude des fonctions comportant exp et ln, recherche de primitives, équations différentielles.

### Suites numériques — INSTALLER

La difficulté est repérée et assumée : il n'y a aucune fausse certitude à défaire. On pose les définitions utiles, on montre des exemples résolus, puis on entraîne court et souvent.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** C'est le chapitre d'ouverture de la Terminale : raisonnement par récurrence, limite d'une suite, suites majorées, minorées, bornées, théorèmes de comparaison et théorème de convergence monotone. On ne démontre pas une limite sans savoir d'abord établir un sens de variation.

## Décision de fin de parcours

| Domaine | Situation initiale | Situation finale | Décision pour septembre |
|---|---|---|---|
| Second degré | Acquis disponible | | |
| Dérivation | Difficulté repérée, sans fausse certitude | | |
| Fonction exponentielle | Certitude à revoir | | |
| Suites numériques | Difficulté repérée, sans fausse certitude | | |
| Produit scalaire | Acquis disponible | | |

---
_Document enseignant. Source pédagogique unique : `stage_prerentree_terminale_maths.md`._
