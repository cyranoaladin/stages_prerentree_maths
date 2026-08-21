# Audit scientifique post-distribution — séance 5

**Les documents élèves ne sont pas modifiés.** Cet audit dit ce qui a été vérifié, par
quel moyen, et ce qui ne l'a pas été. Rien n'y est présenté comme contrôlé plus
rigoureusement qu'il ne l'a été.

## 1. Ce que couvrait l'audit précédent, et ce qui manquait

L'audit livré avec le paquet de clôture portait sur les cent items uniques de
l'évaluation. C'est le cœur, mais ce n'est pas tout ce que l'élève a eu entre les mains :
les vingt-cinq modules de remédiation, les activités de réactivation de la phase 1, les
blocs de découverte de la phase 4, les rappels, les exemples guidés et les corrigés
enseignants n'étaient pas soumis au même contrôle. Cet audit-ci étend le périmètre.

## 2. Les cent items d'évaluation — énoncé exact du contrôle

Le décompte qui suit remplace la formule « 93 items recalculés indépendamment », qui
mélangeait trois choses différentes.

| ce qui a été fait | nombre |
| --- | ---: |
| items uniques soumis à un contrôle scientifique | 100 |
| items dont des points de contrôle chiffrés sont recalculés en Python, puis confrontés à la réponse déclarée | 93 |
| items vérifiés par revue argumentative documentée, sans calcul possible | 7 |
| items disposant **en outre** d'un recalcul secondaire, par une voie différente de la première | 21 |

Les sept items de revue sont : `1re_nsi/B3`, `ines-kefi/B4`, `amine-mansouri/A6`,
`fares-laajili/A6`, `ahmad-beldi-maths/A6`, `ahmed-benhadj-salem/A6` et
`ahmed-benhadj-salem/B4`. Aucun ne porte sur une réponse chiffrée : ce sont des
définitions, des explications ou des choix de rapport à nommer.

Ce qu'il ne faut pas écrire : que les 93 items sont « re-résolus indépendamment ». Les
points de contrôle sont écrits à la main dans la table de vérification, puis recalculés
par le programme ; c'est une confrontation sérieuse, ce n'est pas une seconde résolution
aveugle. Les 21 items à recalcul secondaire, eux, sont recalculés par une voie
réellement distincte — par exemple `arccos(4,8/5)` pour l'angle de la rampe d'accès.

## 3. Les vingt-cinq modules de remédiation

Périmètre : 25 modules, 150 exercices, 150 corrigés, plus les rappels et les exemples
guidés.

| méthode | exercices | verdict |
| --- | ---: | --- |
| recalcul exécuté par le vérificateur, valeur exigée dans le corrigé | 20 | 0 échec |
| revue de lecture, classée par nature et consignée | 130 | 0 écart relevé |

Le détail exercice par exercice figure dans `reports/pedagogical_audit.json`, produit par
`tools/audit_pedagogical_modules.py`.

Limite à énoncer clairement : les 130 exercices classés « revue » portent sur des
définitions, des explications, du code ou des propriétés géométriques. Leur verdict est
une lecture, pas un recalcul, et il est présenté comme tel. Aucun décompte de recalcul
ne les inclut.

## 4. Les imprécisions relevées, et ce qui en a été fait

Six formulations de support et une métadonnée curriculaire ont été relevées. Aucune ne
figure dans un énoncé posé à l'élève : elles sont dans les rappels de méthode, dans un
corrigé, ou dans un encadré de phase 4. Aucune n'affecte un score, sauf la première,
déjà traitée dans les overlays de correction.

| # | support | ce qui est écrit | statut |
| --- | --- | --- | --- |
| 1 | module `M2DE_EQ_02`, rappel | « une équation sous forme factorisée ne doit **jamais** être développée » | trop absolu — développer est licite, seulement moins pertinent |
| 2 | module `M1RE_ALG_02`, rappel | « une **somme** de deux carrés ne se factorise pas dans ℝ » | **faux tel qu'écrit** — `x⁴+4 = (x²−2x+2)(x²+2x+2)` |
| 3 | corrigé d'un item de Première | « les deux droites ont le même coefficient directeur » | à préciser — vrai pour des droites non verticales ; non défini pour une verticale |
| 4 | module `NSI1_BOUCLE_01`, rappel | « `range(a, b, p)` avance de `p` en `p` en s'arrêtant avant `b` » | incomplet — `p ≠ 0`, et le cas `p < 0` n'est pas dit |
| 5 | module `NSI1_ACC_01`, rappel | « variant : quantité entière positive qui décroît » | imprécis — il faut « strictement décroissante » et « minorée » |
| 6 | module `NSI1_TEST_01`, corrigé | « `assert f(2) is not None` » | à limiter — repère un `print` conservé, ne teste pas le contrat |
| 7 | livret de phase 4, entrée en Seconde | « ce qui est nouveau : […] le vocabulaire fonctionnel » | inexact — image, antécédent et `f(x)` relèvent déjà de la Troisième |

Le point 2 mérite d'être souligné : ce n'est pas une approximation pédagogique, c'est un
énoncé faux. L'identité de Sophie Germain fournit un contre-exemple immédiat. La
reformulation exacte — « il n'existe pas d'identité réelle analogue à la différence de
deux carrés permettant de transformer directement `a²+b²` en un produit de deux facteurs
linéaires réels non constants » — est celle qui doit être dite.

Le point 7 est une contradiction interne du dossier : le livret des élèves entrant en
Troisième présente le statut de fonction comme une nouveauté de Troisième, et celui des
élèves entrant en Seconde présente le même vocabulaire comme une nouveauté de Seconde.
Les deux ne peuvent pas être exacts. Le premier l'est.

Les sept points sont traités dans `teacher_guidance/CLARIFICATIONS_ORALES_S5.md`, avec
pour chacun la phrase exacte à dire si la séance n'a pas encore eu lieu. Si elle a eu
lieu, aucune reprise n'est demandée à l'élève : la limite est portée dans l'analyse.

## 5. Les quatre questions à correction délicate

Ces quatre questions restent imprimées telles quelles. Seuls le corrigé enseignant et le
barème interne ont été précisés.

### Sinda CHIKHAOUI — 4e — C2 (b)

> « Expliquer pourquoi l'aire d'un triangle vaut la moitié du produit de sa base par sa
> hauteur. »

La justification retenue repose sur la duplication du triangle par symétrie centrale :
les deux triangles congruents forment un **parallélogramme** de même base et de même
hauteur. L'argument « moitié d'un rectangle obtenu par duplication » n'est pas recevable
comme justification générale — dupliquer un triangle quelconque ne donne pas un
rectangle. Il reste acceptable pour un triangle rectangle, ou dans un découpage-recollement
correctement argumenté.

### Elyes KEFI — 3e — B4 (b)

Le recomptage de l'effectif, le recalcul de la somme ou la confrontation à la liste
source détectent l'omission. L'encadrement de la moyenne entre la plus petite et la plus
grande valeur est un contrôle de vraisemblance légitime, mais 11,25 appartient à
[5 ; 15] : dans ce cas précis, il ne détecte rien. L'encadrement ne peut donc jamais être
exigé comme preuve de détection — et un élève qui le propose ne reçoit aucun code
d'erreur de méthode : son contrôle est correct, il est seulement insuffisant ici.

### Ahmad BELDI — 1re spé — B4 (a)

La consigne imprimée est : « donner d'abord un argument valable pour tout `x` de cet
intervalle, puis illustrer par un exemple numérique ». Elle demande donc bien un argument
général — mais un argument, pas un formalisme. Deux niveaux sont distingués : le niveau
demandé, qui est la comparaison correcte assortie de n'importe quel argument général
valable ; et la preuve renforcée, qui est la rédaction du signe de `x²(x−1)`. La seconde
est valorisée en observation, jamais exigée pour accorder les points.

> Remarque de fidélité : la note de mission décrivait cette consigne comme n'exigeant pas
> explicitement d'argument général. La lecture du PDF réellement distribué montre qu'elle
> en demande un. La règle d'équité retenue est donc légèrement différente de celle
> envisagée — ne pas exiger de formalisme — mais son effet est le même : aucun élève
> n'est pénalisé pour l'absence d'une preuve que la consigne ne réclamait pas.

Cet item, seul, ne prouve pas une compétence de démonstration universelle.

### Malek KHADHRANI — 1re spé — C2 (b)

> « […] est-elle exacte ? Répondre par oui ou non, en justifiant à l'aide de deux valeurs
> bien choisies. »

Un contre-exemple suffit à réfuter une affirmation universelle : `1 < 2` et `f(1) > f(2)`
donnent la totalité des points. La décroissance sur tout l'intervalle n'est pas
demandée et ne peut pas être exigée. L'ajout spontané « donc décroissante » n'est pas
pénalisé. Réciproquement, cette question ne permet pas de conclure que l'élève sait
établir la monotonie d'une fonction.

## 6. Une observation de corrigé qui ne doit rien scorer

Le corrigé enseignant de l'item B2 des deux élèves de NSI mentionne que `moyenne([])`
provoque une division par zéro. La question imprimée ne demande ni le cas de la liste
vide ni son traitement, et aucun critère du barème ne le rétribue. Cette remarque est
donc consignée en `teacher_observation_non_scored` : elle peut être dite oralement, et
elle n'entre ni dans le score, ni dans le profil d'erreurs, ni dans les priorités, ni
dans le bilan.

À distinguer de l'item C1, où le test sur liste vide **est** explicitement demandé par
l'énoncé imprimé — « puis écrire un test portant sur une liste vide, avec son résultat
attendu » — et où il constitue légitimement un critère de barème.

## 7. Le harnais de tests NSI

Le harnais exécute vingt-trois scénarios pour Ahmad BELDI. Sur la copie synthétique
volontairement fautive, il en valide quinze et en rejette huit.

Ce qu'il faut écrire : **23 scénarios attendus, 23 comportements attendus correctement
reconnus.** La copie synthétique contient quatre familles de fautes délibérées —
`somme` affiche au lieu de renvoyer, `moyenne` affiche au lieu de renvoyer, `chercher`
renvoie 0 au lieu de −1 en cas d'absence, `premier_negatif` accepte zéro — qui produisent
exactement les huit échecs observés. Le harnais les a tous localisés, et n'a produit
aucun faux positif sur les quinze cas corrects.

Ce qu'il ne faut plus écrire : « 15/23 », qui donne à croire à un taux de réussite du
harnais alors qu'il s'agit du score d'une copie fabriquée pour échouer.

L'isolation du mode conteneur a été durcie : plus aucun répertoire hôte inscriptible
n'est monté — le résultat sort par `stdout`, encadré par une sentinelle — le `chmod 0777`
a disparu, le swap est borné comme la mémoire, et des limites `fsize` et `nofile` ont été
ajoutées. Le mode « relu », sans isolation, reste explicitement signalé comme tel et
n'est pas le défaut.

Le durcissement a été éprouvé : le mode conteneur a été relancé sur la copie synthétique
après modification, avec l'image `python:3-slim`, et rend exactement le même résultat que
le mode relu — quinze cas validés, les huit mêmes échecs délibérés. Le passage du résultat
par `stdout` n'a donc rien cassé. Une seule image et un seul moteur de conteneurs ont été
essayés.

## 8. Ce que cet audit n'a pas fait

- Il n'a pas re-résolu les cent items à l'aveugle : il a confronté des points de contrôle
  recalculés à des réponses déclarées.
- Il n'a pas recalculé les 130 exercices de module classés « revue » : il les a relus.
- Il n'a conduit **aucune étude de fiabilité** : le terme `measurement_reliability` est
  proscrit de toutes les sorties. Ce qui est calculé est une force de preuve, c'est-à-dire
  un décompte explicite de ce qui étaye une conclusion sur douze items.
- Il n'a pas mesuré les durées réelles de passation : le champ
  `observed_duration_minutes` existe et vaut `null` tant qu'aucune mesure n'a été faite.
  Les deux estimateurs internes du modèle de durée partagent leurs entrées ; ils ne
  constituent pas deux mesures indépendantes, et rien ne le prétend plus.
