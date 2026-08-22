# Matrice curriculaire — les 22 critères d'Inès KEFI

Classement établi **contre les attendus officiels**, et non contre la phase 4 du livret. Inès a suivi sa Cinquième en 2025-2026 sous le programme du cycle 4 (arrêté `MENE2018714A`, BO n° 31 du 30 juillet 2020) ; elle entre en Quatrième en septembre 2026 sous ce même référentiel — le programme `MENE2602912A` ne s'applique à la Quatrième qu'ultérieurement et n'est pas anticipé.

## Sources consultées

- **ATT5** — Attendus de fin d'année de cinquième — mathématiques, éduscol (14-maths-5e-attendus-eduscol1114744)
- **ATT4** — Attendus de fin d'année de quatrième — mathématiques, éduscol (16-maths-4e-attendus-eduscol1114746)
- **PROG** — Programme de mathématiques du cycle 4, arrêté MENE2018714A, BO n° 31 du 30 juillet 2020 — applicable à la Quatrième en 2026-2027
- **DIAG** — Positionnement de pré-rentrée — mathématiques, entrée en Quatrième (4e_Test_Initial, 18 items), instrument ayant établi le diagnostic de fin de Cinquième d'Inès KEFI
- **REPO** — Tableau N-1 → N du dossier de stage, 4e/05_SOURCES/stage_prerentree_quatrieme_maths.md § 3.1

Les deux documents d'attendus ont été téléchargés depuis éduscol et lus intégralement. Aucune référence n'est inventée : lorsqu'un attendu ne dit rien d'une tâche, c'est écrit comme tel.

## La frontière déterminante

| tâche | attendus de fin de **5e** | attendus de fin de **4e** |
| --- | --- | --- |
| réduire `ax + bx` | ✅ explicite — exemples `5,2x + 3,4x`, `2,4x − 2,1x` | repris |
| **développer `k(a − b)`** | ❌ absent | ✅ explicite — exemple `3(4x − 2)` |
| substituer pour **contrôler** un résultat | ✅ explicite | — |
| produire une expression littérale | ✅ explicite | — |
| additionner/soustraire des fractions | ✅ si un dénominateur est multiple de l'autre | cas général |
| **produit** de relatifs | ❌ absent | ✅ explicite |

C'est cette frontière, et elle seule, qui a fait bouger le classement.

## Les 22 critères

| item | criterion_id | notion | max pts | scope avant | scope retenu | justification | source officielle | certitude |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| A1 | `A1_c1` | Somme et différence de relatifs, soustraction d'un négatif | 1 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième : « Il additionne et soustrait des nombres décimaux relatifs » et « Il sait que soustraire revient à additionner l'opposé ». Le produit … | Attendus 5e (éduscol) | haute |
| A2 | `A2_c1` | Différence de fractions, dénominateurs multiples l'un de l'autre | 1 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième : « Il additionne ou soustrait des fractions dont les dénominateurs sont égaux ou multiples l'un de l'autre ». Ici 8 est un multiple de … | Attendus 5e (éduscol) | haute |
| A3 | `A3_c1` | Réduction : termes en x et constantes signées | 1 | `n_minus_1` | `mixed` **←** | Les attendus de fin de cinquième bornent explicitement la réduction à la forme « ax + bx » — leurs exemples sont « 5,2x + 3,4x » et « 2,4x − 2,1x », sans constante. … | Attendus 5e (éduscol) | moyenne |
| A3 | ↳ `A3_c1_v1` | Regroupement des termes en x | 0,5 | — | `n_minus_1` | sous-critère analytique du critère mixte | Attendus 5e (éduscol) | moyenne |
| A3 | ↳ `A3_c1_v2` | Écriture réduite complète, constantes signées comprises | 0,5 | — | `bridge_n` | sous-critère analytique du critère mixte | Attendus 5e (éduscol) | moyenne |
| A4 | `A4_c1` | Somme des angles d'un triangle rectangle | 1 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième, connaissances mobilisables dans un raisonnement : « la somme des angles d'un triangle ». | Attendus 5e (éduscol) | haute |
| A5 | `A5_c1` | Ordre des relatifs | 1 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième : « Il repère sur une droite graduée les nombres décimaux relatifs » et « Il compare, range et encadre ». | Attendus 5e (éduscol) | haute |
| A6 | `A6_c1` | Fractions égales et facteur | 1 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième : « Il reconnaît et produit des fractions égales ». | Attendus 5e (éduscol) | haute |
| B1 | `B1_c1` | Aire et périmètre d'un rectangle, unités | 1 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième : « Il calcule le périmètre et l'aire des figures usuelles (rectangle, parallélogramme, triangle…) », et contrôle la cohérence d'une uni… | Attendus 5e (éduscol) | haute |
| B1 | `B1_c2` | Coefficient de proportionnalité (prix au m²) | 1 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième : « Il résout des problèmes de proportionnalité […] passage à l'unité, coefficient de proportionnalité ». Le prix au mètre carré est un … | Attendus 5e (éduscol) | haute |
| B2 | `B2_c1` | Développement de k(a − b) | 0,5 | `n_minus_1` | `bridge_n` **←** | Les attendus de fin de cinquième ne mentionnent la distributivité que pour « réduire une expression littérale de la forme ax + bx » ; leurs exemples ne comportent au… | Attendus 4e (éduscol) | haute |
| B2 | `B2_c2` | Réduction après développement | 0,5 | `n_minus_1` | `bridge_n` **←** | Cette réduction porte sur une expression issue d'un développement qui relève lui-même de la Quatrième : elle en est conditionnée. Les attendus de cinquième ne couvre… | Attendus 4e (éduscol) | moyenne |
| B2 | `B2_c3` | Contrôle par substitution | 1 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième, explicitement : « Il substitue une valeur numérique à une lettre pour […] contrôler son résultat ». Le contrôle est donc un acquis de C… | Attendus 5e (éduscol) | haute |
| B3 | `B3_c1` | Fréquence en pourcentage | 1 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième : « Il calcule des effectifs et des fréquences » et « Il relie fractions, proportions et pourcentages ». | Attendus 5e (éduscol) | haute |
| B3 | `B3_c2` | Moyenne d'une série | 0,7 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième : « Il calcule et interprète la moyenne d'une série de données ». La médiane, elle, relève de la Quatrième et n'est pas demandée ici. | Attendus 5e (éduscol) | haute |
| B3 | `B3_c3` | Contrôle de vraisemblance par encadrement | 0,3 | `n_minus_1` | `n_minus_1` | Le contrôle de la cohérence d'un résultat est un attendu transversal de fin de cinquième, associé au calcul de la moyenne. | Attendus 5e (éduscol) | haute |
| B4 | `B4_c1` | Raisonnement donnée–propriété–conclusion (parallélogramme) | 1 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième : « Il mène des raisonnements en utilisant des propriétés des figures » et connaît « une définition et une propriété caractéristique du … | Attendus 5e (éduscol) | haute |
| B4 | `B4_c2` | Réfutation par contre-exemple | 1 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième : raisonner à partir des propriétés des figures. Un contre-exemple suffit à réfuter une affirmation ; aucune démonstration générale n'es… | Attendus 5e (éduscol) | haute |
| C1 | `C1_c1` | Aire obtenue par soustraction | 1 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième : calcul de l'aire des figures usuelles et résolution de problèmes de grandeurs. | Attendus 5e (éduscol) | haute |
| C1 | `C1_c2` | Fraction d'une grandeur | 0,5 | `n_minus_1` | `n_minus_1` | Prendre le tiers d'une grandeur relève de l'usage des fractions comme opérateurs, acquis de Cinquième. | Attendus 5e (éduscol) | haute |
| C1 | `C1_c3` | Production d'une expression littérale et substitution | 1,5 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième : « Il produit une expression littérale pour élaborer une formule ou traduire un programme de calcul » et « Il substitue une valeur numé… | Attendus 5e (éduscol) | haute |
| C1 | `C1_c4` | Décision par comparaison à un budget | 1 | `n_minus_1` | `n_minus_1` | Substituer une valeur puis comparer deux nombres pour décider relève des attendus de fin de cinquième ; aucune mise en équation n'est requise. | Attendus 5e (éduscol) | haute |
| C2 | `C2_c1` | Déplacements sur une droite graduée | 1 | `n_minus_1` | `n_minus_1` | Attendus de fin de cinquième : « Il repère sur une droite graduée les nombres décimaux relatifs » ; les déplacements se traduisent par des additions et soustractions… | Attendus 5e (éduscol) | haute |
| C2 | `C2_c2` | Produit de deux relatifs et signe | 1 | `bridge_n` | `bridge_n` | Attendus de fin de quatrième : « Il effectue avec des nombres décimaux relatifs, des produits et des quotients ». Les attendus de cinquième s'arrêtent à l'addition e… | Attendus 4e (éduscol) | haute |

## Décompte

```
Ines KEFI
raw max            = 20
N−1 max            = 17,5   (avant : 19)
Bridge max         = 2,5   (avant : 1)
Mixed              = 1 critère (A3_c1, 1 pt) éclaté en 2 sous-critères de 0,5
criteria original  = 22
lignes notées      = 23   (21 critères simples + 2 sous-critères)
```

## Ce qui a changé, et pourquoi

| critère | avant | après | raison |
| --- | --- | --- | --- |
| `B2_c1` développer `5(x−3)` | `n_minus_1` | **`bridge_n`** | absent des attendus de 5e ; explicite en 4e avec l'exemple `3(4x−2)` |
| `B2_c2` réduire en `7x−8` | `n_minus_1` | **`bridge_n`** | conditionné par un développement de 4e |
| `A3_c1` réduire `7x+4−3x−9` | `n_minus_1` | **`mixed`** | le regroupement des termes en x est un attendu de 5e ; l'écriture réduite avec constantes signées relève de la formulation de 4e |

## Ce qui a été vérifié puis **confirmé sans changement**

| critère | vérification |
| --- | --- |
| `A2_c1` fractions | 8 est multiple de 4 : l'attendu de 5e couvre exactement ce cas. Aucune raison de reclasser. |
| `B2_c3` contrôle | « Il substitue une valeur numérique à une lettre pour […] contrôler son résultat » est un attendu de 5e, mot pour mot. |
| `C1_c3` / `C1_c4` | « produire une expression littérale » et « substituer » sont des attendus de 5e. Aucune transformation d'expression n'est demandée. |
| `C2_c2` produit de relatifs | attendu de 4e : le classement `bridge_n` d'origine est confirmé. |
| `C2_c1` déplacements | resté un critère distinct, en `n_minus_1`. |

## Une ambiguïté assumée plutôt qu'une fausse certitude

`A3_c1` est le seul critère dont le classement n'est pas tranché. Les attendus de 5e bornent la réduction à `ax + bx` ; ceux de 4e l'énoncent sans restriction ; et le diagnostic d'entrée d'Inès — instrument qui a mesuré ses acquis de fin de Cinquième — comportait pourtant un item de réduction avec constantes signées (`4E_TI_Q08`). Plutôt que de trancher arbitrairement, le critère est déclaré **mixte**, éclaté en deux sous-critères de 0,5 point, et sa certitude est notée **moyenne**. L'interface affiche ce niveau de certitude au correcteur.
