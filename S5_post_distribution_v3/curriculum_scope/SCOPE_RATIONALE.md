# Classement curriculaire des critères — justification

Ce document explique, critère par critère, pourquoi un point du sujet déjà distribué compte dans la consolidation des acquis de l'année N-1 ou dans la disponibilité sur les passerelles vers l'année N. Aucune question, aucune valeur, aucun identifiant du sujet n'a été modifié.

## La règle

```
Classement curriculaire des critères déjà imprimés : N-1, passerelle vers N, mixte.

Aucune question, aucune valeur, aucun identifiant du sujet distribué n'est modifié
ici. Ce module ajoute une métadonnée de lecture à des critères qui existent déjà.

PRINCIPE DE CLASSEMENT (règle P, appliquée sans exception)

    n_minus_1   la question imprimée peut être traitée entièrement avec des notions
                du programme de l'année N-1 ;
    bridge_n    la voie directe prévue par la question imprimée mobilise une notion
                qui appartient au programme de l'année N ;
    mixed       un même critère, indivisible tel qu'il a été imprimé, rétribue à la
                fois une compétence N-1 et une notion N. Le critère est alors éclaté
                en sous-critères analytiques VIRTUELS, dont la somme des points est
                strictement égale aux points du critère d'origine.

Le classement par défaut est n_minus_1 : c'est la vocation déclarée du sujet de
clôture. Toute exception est listée ci-dessous avec sa justification, et une seule
source la fonde : le livret de la séance 5 lui-même, qui énonce explicitement, en
phase 4, « ce qui est nouveau » pour chaque niveau.
```

## Ce que les livrets distribués déclarent eux-mêmes nouveau

La source du classement n'est pas une opinion : c'est le livret remis à l'élève, qui énonce en phase 4, niveau par niveau, ce qui est réinvesti et ce qui est nouveau.

### 4e

> « Découverte guidée : construire, à partir d'acquis de Cinquième, deux notions nouvelles de Quatrième — le signe d'un produit de relatifs et l'équation du premier degré. »

- produit et quotient de relatifs, signe du produit
- mise en équation et résolution d'une équation du premier degré

### 3e

> « Ce qui est nouveau — et qui appartient au programme de Troisième : le double produit (a+b)(c+d), et le statut de fonction donné à une expression littérale, avec le vocabulaire « image » et « antécédent ». »

- double distributivité (a+b)(c+d)
- entrée dans le langage des fonctions
- sinus et tangente (programme de Troisième ; le cosinus relève de la Quatrième)

### 2nde

> « Ce qui est nouveau : la notation en intervalle et le vocabulaire fonctionnel. »

- notation en intervalle
- notations et approfondissements fonctionnels propres à la Seconde

### 1ere_spe

> « Découverte guidée : […] deux notions nouvelles de Première — la suite géométrique définie par récurrence et le taux de variation moyen. »

- suite définie par récurrence, notation u_(n+1)
- taux de variation moyen

### 1re_nsi

> « Ce qui est nouveau : les algorithmes de recherche eux-mêmes, leur précondition et leur coût, qui appartiennent au programme de Première. »

- recherche séquentielle
- recherche dichotomique
- précondition et coût d'un algorithme
- invariant de boucle

## Règles générales de correction, applicables à tous les critères

- une méthode mathématiquement correcte n'est jamais un code d'erreur, même si une autre méthode aurait été plus rapide : le fait est consigné en observation de stratégie, avec accepted_alternative_method = true
- développer une équation-produit avant de la résoudre reste licite ; le code CONCEPT est interdit tant que le raisonnement de l'élève est valide
- un code d'erreur n'est porté que sur le ou les critères effectivement échoués ; il n'est jamais propagé aux autres critères du même item
- aucune justification non explicitement demandée par la consigne imprimée ne peut être exigée pour accorder les points

## Les exceptions au classement par défaut

Par défaut un critère est `n_minus_1` : c'est la vocation déclarée du sujet de clôture. 24 critères font exception, chacun pour une raison écrite.

### `1ere_spe` / C1 / critère 4 — **mixed**

« Écrire la relation liant u_(n+1) et u_n, puis calculer u_2 » agrège en un seul critère une notation de Première et un calcul d'évolution successive de Seconde. Le critère imprimé est indivisible ; il est donc éclaté en sous-critères analytiques virtuels, à somme de points strictement égale.

Critères concernés : `1ERE_SPE_AHMAD_BELDI_C1_c4` (1.00 pt), `1ERE_SPE_DONIA_KHADHRANI_C1_c4` (1.00 pt), `1ERE_SPE_MALEK_KHADHRANI_C1_c4` (1.00 pt)

- sous-critère virtuel `…_v1` : 50 % des points, bridge_n — relation de récurrence u_(n+1) = 1,04 x u_n correctement écrite
- sous-critère virtuel `…_v2` : 50 % des points, n_minus_1 — u_2 obtenu par application répétée du coefficient multiplicateur, évalué à partir de la relation écrite par l'élève

- règle d'équité : le sous-critère de calcul est évalué à partir de la relation que l'élève a effectivement écrite : une relation fausse ne doit pas être pénalisée deux fois

### `1re_nsi` / C1 / critère 1 — **bridge_n**

Alias analytique : `NSI1_ALGO_RECHERCHE_BRIDGE` — Algorithmes de recherche : séquentielle et dichotomique (programme de Première NSI)

complétion de la boucle de recherche séquentielle, introduite en phase 4.

Critères concernés : `1RE_NSI_AHMAD_BELDI_C1_c1` (1.50 pt), `1RE_NSI_AHMED_BENHADJ_SALEM_C1_c1` (1.50 pt)


### `1re_nsi` / C1 / critère 2 — **bridge_n**

Alias analytique : `NSI1_ALGO_RECHERCHE_BRIDGE` — Algorithmes de recherche : séquentielle et dichotomique (programme de Première NSI)

lecture du contrat de la recherche séquentielle, dont la valeur d'absence.

Critères concernés : `1RE_NSI_AHMAD_BELDI_C1_c2` (0.75 pt), `1RE_NSI_AHMED_BENHADJ_SALEM_C1_c2` (0.75 pt)


### `1re_nsi` / C1 / critère 3 — **n_minus_1**

écrire un test avec son résultat attendu sur un cas limite est une compétence de test, travaillée en séances 3 et 4 et indépendante de l'algorithme support : la valeur attendue se lit directement dans le code imprimé, qui contient « return -1 ».

Critères concernés : `1RE_NSI_AHMAD_BELDI_C1_c3` (0.75 pt), `1RE_NSI_AHMED_BENHADJ_SALEM_C1_c3` (0.75 pt)

- limite d'interprétation : le support du test est un algorithme de passerelle ; ce critère mesure la pratique de test, pas la maîtrise de la recherche séquentielle

### `1re_nsi` / C1 / critère 4 — **bridge_n**

Alias analytique : `NSI1_ALGO_RECHERCHE_BRIDGE` — Algorithmes de recherche : séquentielle et dichotomique (programme de Première NSI)

gain et précondition de la dichotomie : attendus explicites de Première.

Critères concernés : `1RE_NSI_AHMAD_BELDI_C1_c4` (1.00 pt), `1RE_NSI_AHMED_BENHADJ_SALEM_C1_c4` (1.00 pt)


### `3e` / B2 / critère 1 — **n_minus_1**

Alias analytique : `M3_TRIGO_COS_NM1` — Nommer les côtés d'un triangle rectangle et employer le cosinus (acquis de Quatrième)

nommer le côté adjacent et l'hypoténuse puis choisir le cosinus est un attendu de Quatrième.

Critères concernés : `3E_AMINE_MANSOURI_B2_c1` (1.00 pt), `3E_ELYES_KEFI_B2_c1` (1.00 pt), `3E_FARES_LAAJILI_B2_c1` (1.00 pt), `3E_SARAH_BARGAOUI_B2_c1` (1.00 pt), `3E_SELIM_MANSOURI_B2_c1` (1.00 pt)


### `3e` / B2 / critère 2 — **n_minus_1**

Alias analytique : `M3_TRIGO_COS_NM1` — Nommer les côtés d'un triangle rectangle et employer le cosinus (acquis de Quatrième)

calcul d'un angle à partir du cosinus : attendu de Quatrième.

Critères concernés : `3E_AMINE_MANSOURI_B2_c2` (0.50 pt), `3E_ELYES_KEFI_B2_c2` (0.50 pt), `3E_FARES_LAAJILI_B2_c2` (0.50 pt), `3E_SARAH_BARGAOUI_B2_c2` (0.50 pt), `3E_SELIM_MANSOURI_B2_c2` (0.50 pt)


### `3e` / B2 / critère 3 — **bridge_n**

Alias analytique : `M3_TRIGO_SIN_BRIDGE` — Sinus et tangente : identification du rapport (programme de Troisième)

la question 3 demande le rapport liant le côté opposé et l'hypoténuse : le sinus, qui appartient au programme de Troisième et non à celui de Quatrième.

Critères concernés : `3E_AMINE_MANSOURI_B2_c3` (0.50 pt), `3E_ELYES_KEFI_B2_c3` (0.50 pt), `3E_FARES_LAAJILI_B2_c3` (0.50 pt), `3E_SARAH_BARGAOUI_B2_c3` (0.50 pt), `3E_SELIM_MANSOURI_B2_c3` (0.50 pt)

- limite d'interprétation : une non-réussite ne documente aucune fragilité sur la trigonométrie de Quatrième, mesurée aux critères 1 et 2 du même item

### `3e` / C1 / critère 2 — **n_minus_1**

Alias analytique : `M3_TRIGO_COS_NM1` — Nommer les côtés d'un triangle rectangle et employer le cosinus (acquis de Quatrième)

la longueur de la rampe, c'est-à-dire l'hypoténuse, a été calculée à la question précédente : l'angle au sol s'obtient donc par le cosinus, acquis de Quatrième. Le contre-calcul de référence du dossier emploie lui-même arccos(4,8/5).

Critères concernés : `3E_AMINE_MANSOURI_C1_c2` (1.00 pt), `3E_ELYES_KEFI_C1_c2` (1.00 pt), `3E_FARES_LAAJILI_C1_c2` (1.00 pt), `3E_SARAH_BARGAOUI_C1_c2` (1.00 pt), `3E_SELIM_MANSOURI_C1_c2` (1.00 pt)

- méthode acceptée : cosinus de l'angle au sol, à partir de la longueur au sol et de la rampe
- méthode acceptée : tangente, à partir de la hauteur et de la longueur au sol
- méthode acceptée : sinus, à partir de la hauteur et de la rampe

### `ahmad-beldi-maths` / C2 / critère 1 — **bridge_n**

Alias analytique : `M1RE_SUITES_RECURRENCE_BRIDGE` — Suite définie par récurrence, notation u_(n+1) (découverte de Première)

l'écriture de u_(n+1) en fonction de u_n est la notation de suite introduite en phase 4 de la séance ; le manifeste marque déjà cet item « not_comparable ».

Critères concernés : `1ERE_SPE_AHMAD_BELDI_C2_c1` (1.00 pt)


### `ahmad-beldi-maths` / C2 / critère 2 — **bridge_n**

Alias analytique : `M1RE_SUITES_RECURRENCE_BRIDGE` — Suite définie par récurrence, notation u_(n+1) (découverte de Première)

u_2 est ici demandé dans le cadre de la suite ; le classer en N-1 ferait retomber sur la consolidation de Seconde l'échec éventuel d'une notation nouvelle. Le coefficient multiplicateur reste mesuré en N-1 par les deux critères de l'item B3.

Critères concernés : `1ERE_SPE_AHMAD_BELDI_C2_c2` (1.00 pt)

- règle d'équité : u_2 est évalué à partir de la relation que l'élève a écrite à la question précédente

### `ahmad-beldi-nsi` / C2 / critère 1 — **bridge_n**

Alias analytique : `NSI1_ALGO_RECHERCHE_BRIDGE` — Algorithmes de recherche : séquentielle et dichotomique (programme de Première NSI)

écriture d'une recherche séquentielle avec valeur sentinelle.

Critères concernés : `1RE_NSI_AHMAD_BELDI_C2_c1` (1.00 pt)


### `ahmad-beldi-nsi` / C2 / critère 2 — **bridge_n**

Alias analytique : `NSI1_ALGO_RECHERCHE_BRIDGE` — Algorithmes de recherche : séquentielle et dichotomique (programme de Première NSI)

résultat de l'appel : lecture du contrat de l'algorithme écrit.

Critères concernés : `1RE_NSI_AHMAD_BELDI_C2_c2` (1.00 pt)


### `ahmed-benhadj-salem` / C2 / critère 1 — **bridge_n**

Alias analytique : `NSI1_ALGO_RECHERCHE_BRIDGE` — Algorithmes de recherche : séquentielle et dichotomique (programme de Première NSI)

coût comparé de la recherche séquentielle et de la dichotomie.

Critères concernés : `1RE_NSI_AHMED_BENHADJ_SALEM_C2_c1` (1.00 pt)


### `ahmed-benhadj-salem` / C2 / critère 2 — **bridge_n**

Alias analytique : `NSI1_ALGO_RECHERCHE_BRIDGE` — Algorithmes de recherche : séquentielle et dichotomique (programme de Première NSI)

énoncé d'un invariant de boucle : attendu de Première.

Critères concernés : `1RE_NSI_AHMED_BENHADJ_SALEM_C2_c2` (1.00 pt)


### `amine-mansouri` / A6 / critère 1 — **n_minus_1**

Alias analytique : `M3_TRIGO_COS_NM1` — Nommer les côtés d'un triangle rectangle et employer le cosinus (acquis de Quatrième)

le rapport demandé lie le côté adjacent et l'hypoténuse : c'est le cosinus.

Critères concernés : `3E_AMINE_MANSOURI_A6_c1` (1.00 pt)


### `elyes-kefi` / C2 / critère 1 — **bridge_n**

Alias analytique : `M3_LIT_DOUBLE_DISTRIB_BRIDGE` — Double distributivité (a+b)(c+d) — découverte de Troisième

(x+4)(x+3) relève du double produit, introduit en phase 4 de la séance. Le skill_id d'origine M3E_LIT_01 porte la distributivité simple k(ax+b), acquis de Quatrième.

Critères concernés : `3E_ELYES_KEFI_C2_c1` (1.00 pt)


### `elyes-kefi` / C2 / critère 2 — **n_minus_1**

conduire un contrôle numérique sur les deux écritures est une compétence de Quatrième, indépendante de la nouveauté du développement.

Critères concernés : `3E_ELYES_KEFI_C2_c2` (1.00 pt)

- règle d'équité : le contrôle est crédité dès lors qu'il est effectivement conduit sur les deux écritures, même si le développement (passerelle) est erroné
- règle d'équité : un élève qui détecte et signale le désaccord entre les deux écritures obtient la totalité du critère : c'est exactement ce que le contrôle sert à produire
- limite d'interprétation : la réussite s'appuie sur un développement relevant d'une notion nouvelle ; ce critère ne doit pas être lu isolément comme une mesure du contrôle numérique

### `fares-laajili` / A6 / critère 1 — **bridge_n**

Alias analytique : `M3_TRIGO_SIN_BRIDGE` — Sinus et tangente : identification du rapport (programme de Troisième)

le rapport demandé lie le côté opposé et l'hypoténuse : c'est le sinus, notion de Troisième.

Critères concernés : `3E_FARES_LAAJILI_A6_c1` (1.00 pt)


### `fares-laajili` / C2 / critère 1 — **bridge_n**

Alias analytique : `M3_TRIGO_SIN_BRIDGE` — Sinus et tangente : identification du rapport (programme de Troisième)

les données fournies sont le côté opposé à l'angle et l'hypoténuse : la voie directe est le sinus. Le contre-calcul de référence du dossier emploie arcsin(10/26).

Critères concernés : `3E_FARES_LAAJILI_C2_c1` (1.00 pt)

- méthode acceptée : sinus, directement à partir des données
- méthode acceptée : calcul préalable du troisième côté par le théorème de Pythagore, puis cosinus : voie entièrement N-1, mathématiquement correcte, à créditer intégralement
- limite d'interprétation : si l'élève emprunte la voie Pythagore puis cosinus, la réussite documente un acquis de Quatrième et doit être signalée comme telle en observation, sans être reversée automatiquement au décompte N-1

### `fares-laajili` / C2 / critère 2 — **bridge_n**

Alias analytique : `M3_TRIGO_SIN_BRIDGE` — Sinus et tangente : identification du rapport (programme de Troisième)

la mesure de l'angle découle du rapport choisi à la question précédente.

Critères concernés : `3E_FARES_LAAJILI_C2_c2` (1.00 pt)

- méthode acceptée : arcsin appliqué au rapport 10/26
- méthode acceptée : arccos appliqué au rapport obtenu après calcul du troisième côté

### `ines-kefi` / C2 / critère 2 — **bridge_n**

Alias analytique : `M4E_REL_PROD_BRIDGE` — Produit de deux relatifs et justification du signe (découverte de Quatrième)

(-4) x (-7) et la justification du signe relèvent du produit de relatifs, introduit en phase 4 de la séance comme notion nouvelle de Quatrième. Le skill_id d'origine M4E_REL_01 ne porte que la somme et la différence de relatifs, acquis de Cinquième : le confondre avec le produit fusionnerait un acquis N-1 et une découverte N.

Critères concernés : `4E_INES_KEFI_C2_c2` (1.00 pt)

- limite d'interprétation : une non-réussite ici ne documente aucune fragilité sur la somme et la différence de relatifs, mesurées séparément en A1 et A5

### `selim-mansouri` / C2 / critère 1 — **bridge_n**

Alias analytique : `M3_LIT_DOUBLE_DISTRIB_BRIDGE` — Double distributivité (a+b)(c+d) — découverte de Troisième

(x+2)(x+5) relève du double produit, introduit en phase 4 de la séance.

Critères concernés : `3E_SELIM_MANSOURI_C2_c1` (1.00 pt)


### `selim-mansouri` / C2 / critère 2 — **n_minus_1**

conduire un contrôle numérique sur les deux écritures est une compétence de Quatrième, indépendante de la nouveauté du développement.

Critères concernés : `3E_SELIM_MANSOURI_C2_c2` (1.00 pt)

- règle d'équité : le contrôle est crédité dès lors qu'il est effectivement conduit sur les deux écritures, même si le développement (passerelle) est erroné
- règle d'équité : un élève qui détecte et signale le désaccord entre les deux écritures obtient la totalité du critère
- limite d'interprétation : la réussite s'appuie sur un développement relevant d'une notion nouvelle ; ce critère ne doit pas être lu isolément comme une mesure du contrôle numérique

## Ce que ce classement change, chiffres à l'appui

| élève | niveau | critères | points N-1 | points passerelle | critères mixtes |
| --- | --- | ---: | ---: | ---: | ---: |
| ahmad-beldi-maths | 1ere_spe | 23 | 17.50 | 2.50 | 1 |
| ahmad-beldi-nsi | 1re_nsi | 21 | 14.75 | 5.25 | 0 |
| ahmed-bakir | 2nde | 22 | 20.00 | 0.00 | 0 |
| ahmed-benhadj-salem | 1re_nsi | 22 | 14.75 | 5.25 | 0 |
| amine-mansouri | 3e | 22 | 19.50 | 0.50 | 0 |
| donia-khadhrani | 1ere_spe | 23 | 19.50 | 0.50 | 1 |
| elyes-kefi | 3e | 23 | 18.50 | 1.50 | 0 |
| fares-darghouth | 4e | 23 | 20.00 | 0.00 | 0 |
| fares-laajili | 3e | 22 | 16.50 | 3.50 | 0 |
| ines-kefi | 4e | 22 | 19.00 | 1.00 | 0 |
| malek-khadhrani | 1ere_spe | 23 | 19.50 | 0.50 | 1 |
| noa-maniaci | 2nde | 23 | 20.00 | 0.00 | 0 |
| sarah-bargaoui | 3e | 23 | 19.50 | 0.50 | 0 |
| selim-mansouri | 3e | 22 | 18.50 | 1.50 | 0 |
| sinda-chikhaoui | 4e | 23 | 20.00 | 0.00 | 0 |

Quatre élèves — Ahmed BAKIR, Noa MANIACI, Fares DARGHOUTH et Sinda CHIKHAOUI — n'ont aucun critère de passerelle : leur sujet de clôture porte intégralement sur des acquis de l'année N-1. Leur score brut reste néanmoins un score brut, et non un diagnostic complet : douze items ne mesurent pas une année.
