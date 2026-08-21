# Contre-résolution scientifique des items — après correction

**Date :** 21 août 2026. **Périmètre :** les 100 couples énoncé/réponse uniques des 15 évaluations.

## Méthode

Chaque item a été **re-résolu indépendamment**, à partir de son énoncé, sans lire la réponse déclarée dans la banque. Le résultat recalculé est ensuite confronté à cette réponse : c'est cette confrontation qui produit le verdict, et non une relecture.

| Méthode | Items | Ce qui tranche le verdict |
|---|:--:|---|
| `calcul` | 93 | recalcul exécutable en Python ; tous les fragments recalculés doivent se retrouver dans la réponse déclarée |
| `revue` | 7 | item portant sur une définition ou un raisonnement qu'aucun calcul ne tranche ; la justification est consignée mot pour mot |

Vingt et une valeurs supplémentaires sont recalculées par une voie différente de celle de la banque (racines entières, arccos/arcsin, produits de coefficients multiplicateurs, arithmétique exacte sur les fractions) et doivent également apparaître dans la réponse.

## Résultat

| Verdict | Items |
|---|:--:|
| **PASS** | 100 |
| **WARN** | 0 |
| **FAIL** | 0 |

## Détail item par item

| # | Portée | Réf. | Compétence | Pts | Méthode | Verdict | Contrôle effectué |
|---:|---|---|---|:--:|---|:--:|---|
| 1 | 1ere_spe | A1 | `M1RE_ALG_02` | 1 | `calcul` | **PASS** | 16x^2-49 factorisé |
| 2 | 1ere_spe | A2 | `M1RE_INEQ_01` | 1 | `calcul` | **PASS** | -3x+12>0 recalculé |
| 3 | 1ere_spe | A3 | `M1RE_FONC_01` | 1 | `calcul` | **PASS** | g(-3) pour 2x^2+x |
| 4 | 1ere_spe | A4 | `M1RE_VECT_01` | 1 | `calcul` | **PASS** | coordonnées de AB |
| 5 | 1ere_spe | B1 | `M1RE_INEQ_02` | 2 | `calcul` | **PASS** | racines de (3x+6)(2-x) et signe |
| 6 | 1ere_spe | B2 | `M1RE_FONC_02` | 2 | `calcul` | **PASS** | image, antécédent et comparaison sur ]0;1[ |
| 7 | 1ere_spe | B3 | `M1RE_POURC_02` | 2 | `calcul` | **PASS** | évolutions successives recalculées |
| 8 | 1ere_spe | C1 | `M1RE_DROIT_01` | 4 | `calcul` | **PASS** | droite, probabilités et suite |
| 9 | 1re_nsi | A1 | `NSI1_LIST_01` | 1 | `calcul` | **PASS** | L[2], L[-1], len(L) et dernier indice |
| 10 | 1re_nsi | A2 | `NSI1_LOG_01` | 1 | `calcul` | **PASS** | négations recalculées |
| 11 | 1re_nsi | A3 | `NSI1_BOUCLE_01` | 1 | `calcul` | **PASS** | range(3,12,4) recalculé |
| 12 | 1re_nsi | A4 | `NSI1_AFF_01` | 1 | `calcul` | **PASS** | a=6, b=a, a=a+4 |
| 13 | 1re_nsi | B1 | `NSI1_ACC_01` | 2 | `calcul` | **PASS** | accumulateur tracé |
| 14 | 1re_nsi | B2 | `NSI1_FONC_01` | 2 | `calcul` | **PASS** | fonction sans return |
| 15 | 1re_nsi | B3 | `NSI1_CSV_01` | 2 | `revue` | **PASS** | types de conversion float/int conformes aux colonnes ; la concaténation de deux chaînes par + est le comportement documenté de Python ; l'exemple de métadonnée proposé (date de production, capteur, unité, encodage) décrit bien le fichier et non un enregistrement. |
| 16 | 1re_nsi | C1 | `NSI1_ALGO_01` | 4 | `calcul` | **PASS** | recherche séquentielle sur liste de dictionnaires |
| 17 | 2nde | A1 | `M2DE_CALC_01` | 1 | `calcul` | **PASS** | -4+5(-3)-(-6) recalculé |
| 18 | 2nde | A2 | `M2DE_FRAC_01` | 1 | `calcul` | **PASS** | 3/8 + 5/12 recalculé |
| 19 | 2nde | A3 | `M2DE_PUIS_01` | 1 | `calcul` | **PASS** | 10^5 x 10^-2 / 10^4 |
| 20 | 2nde | A4 | `M2DE_ALG_01` | 1 | `calcul` | **PASS** | (x-5)^2 développé |
| 21 | 2nde | B1 | `M2DE_EQ_01` | 2 | `calcul` | **PASS** | équation, produit nul et vérification |
| 22 | 2nde | B2 | `M2DE_POURC_01` | 2 | `calcul` | **PASS** | évolutions successives recalculées |
| 23 | 2nde | B3 | `M2DE_GEO_01` | 2 | `calcul` | **PASS** | Pythagore, Thalès et périmètre |
| 24 | 2nde | C1 | `M2DE_ALG_01` | 4 | `calcul` | **PASS** | aire, diagonale et coefficient global |
| 25 | 3e | A1 | `M3E_REL_01` | 1 | `calcul` | **PASS** | (-15)/3 + (-2)(-6) recalculé |
| 26 | 3e | A2 | `M3E_FRAC_02` | 1 | `calcul` | **PASS** | 4/5 x 15/8 recalculé |
| 27 | 3e | A3 | `M3E_LIT_02` | 1 | `calcul` | **PASS** | 9x-4-5x-7 recalculé |
| 28 | 3e | A4 | `M3E_EQ_01` | 1 | `calcul` | **PASS** | 4x-3=2x+9 recalculé |
| 29 | 3e | B1 | `M3E_GEO_01` | 2 | `calcul` | **PASS** | AC = racine(20^2-12^2) |
| 30 | 3e | B2 | `M3E_TRIG_01` | 2 | `calcul` | **PASS** | cos B = 5/13 et angle arrondi |
| 31 | 3e | B3 | `M3E_PROP_01` | 2 | `calcul` | **PASS** | vitesse et moyenne pondérée recalculées |
| 32 | 3e | C1 | `M3E_GEO_01` | 4 | `calcul` | **PASS** | hypoténuse, angle, pente et coût |
| 33 | 4e | A1 | `M4E_REL_01` | 1 | `calcul` | **PASS** | (-8)+3-(-5) recalculé |
| 34 | 4e | A2 | `M4E_FRAC_02` | 1 | `calcul` | **PASS** | 5/8 - 1/4 recalculé |
| 35 | 4e | A3 | `M4E_LIT_02` | 1 | `calcul` | **PASS** | 7x+4-3x-9 : coefficients recalculés |
| 36 | 4e | A4 | `M4E_GEO_01` | 1 | `calcul` | **PASS** | angles aigus complémentaires |
| 37 | 4e | B1 | `M4E_AIRE_01` | 2 | `calcul` | **PASS** | aire, périmètre et prix recalculés |
| 38 | 4e | B2 | `M4E_LIT_01` | 2 | `calcul` | **PASS** | développement, réduction et contrôle en x=2 |
| 39 | 4e | B3 | `M4E_STAT_01` | 2 | `calcul` | **PASS** | fréquence, somme, moyenne et encadrement |
| 40 | 4e | C1 | `M4E_AIRE_01` | 4 | `calcul` | **PASS** | aires, expression, C(6) et décision |
| 41 | ahmad-beldi-maths | A5 | `M1RE_ALG_02` | 1 | `calcul` | **PASS** | 49x^2-16 factorisé |
| 42 | ahmad-beldi-maths | A6 | `M1RE_FONC_02` | 1 | `revue` | **PASS** | un point de coordonnées (-4 ; 1) sur la courbe se traduit par f(-4)=1 ; -4 est donc un antécédent de 1, ce que la réponse énonce correctement. |
| 43 | ahmad-beldi-maths | B4 | `M1RE_FREF_02` | 2 | `calcul` | **PASS** | argument général sur le signe de x^2(x-1), illustration numérique et P(A u B) |
| 44 | ahmad-beldi-maths | C2 | `M1RE_POURC_02` | 2 | `calcul` | **PASS** | suite géométrique de raison 1,05 |
| 45 | ahmad-beldi-nsi | A5 | `NSI1_FONC_01` | 1 | `calcul` | **PASS** | fonction qui affiche sans renvoyer |
| 46 | ahmad-beldi-nsi | A6 | `NSI1_BOUCLE_01` | 1 | `calcul` | **PASS** | range(6) et range(2,9) recalculés |
| 47 | ahmad-beldi-nsi | B4 | `NSI1_LIST_01` | 2 | `calcul` | **PASS** | indexation et alias de liste |
| 48 | ahmad-beldi-nsi | C2 | `NSI1_ALGO_01` | 2 | `calcul` | **PASS** | première valeur négative |
| 49 | ahmed-bakir | A5 | `M2DE_CALC_01` | 1 | `calcul` | **PASS** | (-3)^3 + 2(-4) recalculé |
| 50 | ahmed-bakir | A6 | `M2DE_PUIS_01` | 1 | `calcul` | **PASS** | notation scientifique de 0,000205 |
| 51 | ahmed-bakir | B4 | `M2DE_ALG_01` | 2 | `calcul` | **PASS** | (2x-3)(x+5) développé et contrôlé en x=1 |
| 52 | ahmed-bakir | C2 | `M2DE_POURC_01` | 2 | `calcul` | **PASS** | hausse de 15 % puis baisse de 15 % |
| 53 | ahmed-benhadj-salem | A5 | `NSI1_ACC_01` | 1 | `calcul` | **PASS** | accumulateur sur range(2,6) |
| 54 | ahmed-benhadj-salem | A6 | `NSI1_BOUCLE_02` | 1 | `revue` | **PASS** | le critère de choix entre for et while est bien la connaissance préalable du nombre de répétitions ; les deux situations sont classées conformément à ce critère. |
| 55 | ahmed-benhadj-salem | B4 | `NSI1_TEST_01` | 2 | `revue` | **PASS** | les trois tests proposés sont cohérents avec le contrat annoncé, dont le cas limite de la liste vide qui doit lever une erreur ; l'explication du problème des flottants est exacte et la solution proposée, math.isclose, est la solution usuelle. |
| 56 | ahmed-benhadj-salem | C2 | `NSI1_ALGO_01` | 2 | `calcul` | **PASS** | coût séquentiel maximal et ordre de grandeur dichotomique : 2^10 = 1024 >= 1000 |
| 57 | amine-mansouri | A5 | `M3E_LIT_02` | 1 | `calcul` | **PASS** | 6x+5-9x-8 recalculé |
| 58 | amine-mansouri | A6 | `M3E_TRIG_01` | 1 | `revue` | **PASS** | AB est bien le côté adjacent à l'angle B et BC l'hypoténuse dans un triangle rectangle en A : le rapport AB/BC est le cosinus de B. |
| 59 | amine-mansouri | B4 | `M3E_GEO_01` | 2 | `calcul` | **PASS** | AC = racine(17^2-15^2) et contrôle de vraisemblance |
| 60 | amine-mansouri | C2 | `M3E_FRAC_02` | 2 | `calcul` | **PASS** | 4/9 x 3/8 recalculé |
| 61 | donia-khadhrani | A5 | `M1RE_FONC_02` | 1 | `calcul` | **PASS** | 4x-3=13 recalculé |
| 62 | donia-khadhrani | A6 | `M1RE_INEQ_01` | 1 | `calcul` | **PASS** | -5x+20>=0 recalculé |
| 63 | donia-khadhrani | B4 | `M1RE_DROIT_01` | 2 | `calcul` | **PASS** | coefficient directeur, ordonnée à l'origine, parallélisme |
| 64 | donia-khadhrani | C2 | `M1RE_PROBA_01` | 2 | `calcul` | **PASS** | P(A u B) et P(non A) recalculées |
| 65 | elyes-kefi | A5 | `M3E_FRAC_02` | 1 | `calcul` | **PASS** | 7/9 x 3/14 recalculé |
| 66 | elyes-kefi | A6 | `M3E_LIT_02` | 1 | `calcul` | **PASS** | 8x-9+3x+4 recalculé |
| 67 | elyes-kefi | B4 | `M3E_STAT_01` | 2 | `calcul` | **PASS** | somme, effectif, moyenne, et démonstration que l'encadrement ne détecte pas l'omission |
| 68 | elyes-kefi | C2 | `M3E_LIT_01` | 2 | `calcul` | **PASS** | (x+4)(x+3) développé et contrôlé en x=2 |
| 69 | fares-darghouth | A5 | `M4E_AIRE_01` | 1 | `calcul` | **PASS** | aire du triangle 16 x 5 / 2 |
| 70 | fares-darghouth | A6 | `M4E_FRAC_02` | 1 | `calcul` | **PASS** | fraction équivalente et différence |
| 71 | fares-darghouth | B4 | `M4E_GEO_01` | 2 | `calcul` | **PASS** | somme des angles du triangle |
| 72 | fares-darghouth | C2 | `M4E_LIT_01` | 2 | `calcul` | **PASS** | substitution, développement, réduction |
| 73 | fares-laajili | A5 | `M3E_FRAC_02` | 1 | `calcul` | **PASS** | 6/25 : 3/10 recalculé |
| 74 | fares-laajili | A6 | `M3E_TRIG_01` | 1 | `revue` | **PASS** | connaissant le côté opposé à C et l'hypoténuse, le rapport qui les met en jeu est bien le sinus ; la définition donnée est exacte. |
| 75 | fares-laajili | B4 | `M3E_GEO_01` | 2 | `calcul` | **PASS** | BC = racine(20^2+21^2) et analyse de l'erreur |
| 76 | fares-laajili | C2 | `M3E_TRIG_01` | 2 | `calcul` | **PASS** | sin B = 10/26 et angle arrondi |
| 77 | ines-kefi | A5 | `M4E_REL_02` | 1 | `calcul` | **PASS** | ordre croissant recalculé |
| 78 | ines-kefi | A6 | `M4E_FRAC_02` | 1 | `calcul` | **PASS** | 2/3 = 10/15, facteur 5 |
| 79 | ines-kefi | B4 | `M4E_GEO_02` | 2 | `revue` | **PASS** | des diagonales de même milieu caractérisent le parallélogramme ; le contre-exemple du rectangle non carré réfute correctement la conclusion « carré ». |
| 80 | ines-kefi | C2 | `M4E_REL_01` | 2 | `calcul` | **PASS** | déplacements et produit de relatifs |
| 81 | malek-khadhrani | A5 | `M1RE_FONC_01` | 1 | `calcul` | **PASS** | f(-4) pour x^2-6x |
| 82 | malek-khadhrani | A6 | `M1RE_VECT_02` | 1 | `calcul` | **PASS** | déterminant de (6;-4) et (-9;6) |
| 83 | malek-khadhrani | B4 | `M1RE_VECT_01` | 2 | `calcul` | **PASS** | vecteurs, alignement, coefficient directeur |
| 84 | malek-khadhrani | C2 | `M1RE_NUM_01` | 2 | `calcul` | **PASS** | puissance et contre-exemple sur 1/x |
| 85 | noa-maniaci | A5 | `M2DE_EQ_02` | 1 | `calcul` | **PASS** | (4x-12)(x+6)=0 recalculé |
| 86 | noa-maniaci | A6 | `M2DE_PUIS_01` | 1 | `calcul` | **PASS** | 10^-4 x 10^7 recalculé |
| 87 | noa-maniaci | B4 | `M2DE_POURC_01` | 2 | `calcul` | **PASS** | évolutions successives recalculées |
| 88 | noa-maniaci | C2 | `M2DE_EQ_02` | 2 | `calcul` | **PASS** | factorisation et équation produit nul |
| 89 | sarah-bargaoui | A5 | `M3E_LIT_02` | 1 | `calcul` | **PASS** | 8x+6-3x-13 recalculé |
| 90 | sarah-bargaoui | A6 | `M3E_EQ_01` | 1 | `calcul` | **PASS** | 5x-8=17 recalculé |
| 91 | sarah-bargaoui | B4 | `M3E_PROP_01` | 2 | `calcul` | **PASS** | proportionnalité et Pythagore recalculés |
| 92 | sarah-bargaoui | C2 | `M3E_LIT_01` | 2 | `calcul` | **PASS** | développement, réduction et contrôle en x=1 |
| 93 | selim-mansouri | A5 | `M3E_REL_01` | 1 | `calcul` | **PASS** | (-7)(-4)+(-20)/5 recalculé |
| 94 | selim-mansouri | A6 | `M3E_LIT_01` | 1 | `calcul` | **PASS** | -5(3x-2) développé |
| 95 | selim-mansouri | B4 | `M3E_PROP_01` | 2 | `calcul` | **PASS** | retour à l'unité et Pythagore |
| 96 | selim-mansouri | C2 | `M3E_LIT_01` | 2 | `calcul` | **PASS** | (x+2)(x+5) développé et contrôlé en x=1 |
| 97 | sinda-chikhaoui | A5 | `M4E_REL_01` | 1 | `calcul` | **PASS** | 7-(-6)-4 recalculé |
| 98 | sinda-chikhaoui | A6 | `M4E_FRAC_02` | 1 | `calcul` | **PASS** | 3/4 - 5/12 recalculé |
| 99 | sinda-chikhaoui | B4 | `M4E_LIT_01` | 2 | `calcul` | **PASS** | développement, réduction, contrôle en x=0 |
| 100 | sinda-chikhaoui | C2 | `M4E_AIRE_01` | 2 | `calcul` | **PASS** | base du triangle et justification par duplication |

## Traitement des quatre FAIL et des huit WARN de la revue du 21 août

| Réf. audit | Item | Défaut relevé | Correction apportée |
|---|---|---|---|
| FAIL 20 | Sinda CHIKHAOUI C2 | la duplication d'un triangle produit un parallélogramme, pas un rectangle | la justification passe par un parallélogramme de même base et même hauteur ; la question demande désormais « la moitié du produit de la base par la hauteur » ; l'explication par découpage-recollement reste acceptée |
| FAIL 35 | Elyes KEFI B4 | l'encadrement [5 ; 15] ne détecte pas l'omission qui donne 11,25 | le contrôle détecteur devient le recomptage de l'effectif ou le recalcul de la somme ; la question demande en plus d'expliquer pourquoi l'encadrement ne détecte rien |
| FAIL 74 | Ahmad BELDI (maths) B4 | un exemple ne démontre pas une propriété universelle | l'énoncé exige d'abord un argument valable pour tout x, puis une illustration ; le barème sépare les deux, 0,75 pt pour l'argument, 0,25 pt pour l'exemple |
| FAIL 84 | Malek KHADHRANI C2 | deux valeurs réfutent la croissance mais ne démontrent pas la décroissance | la question demande de statuer sur l'exactitude d'une affirmation ; la réponse se limite à la réfutation et précise explicitement que la décroissance globale n'est pas établie |
| WARN 24, 42, 63, 73 | Amine A4, Sarah A6, Noa B4, Ahmad B3 | code `CONTROLE` alors qu'aucun contrôle n'est demandé | ces codes sont remplacés par `CALCUL` ; un contrôle automatique vérifie désormais qu'un code `CONTROLE` suppose un contrôle explicitement demandé dans l'énoncé ou dans le barème |
| WARN 55, 61 | Ahmed BAKIR B1, Noa MANIACI A5 | développer une équation-produit est une méthode valide, codée comme erreur | ces entrées quittent la liste des erreurs ; un champ `methodes_alternatives_acceptees` déclare que la méthode reçoit la totalité des points, et il est imprimé dans le dossier enseignant |
| WARN 99 | Ahmed BENHADJ SALEM B4 | le cas de la liste vide n'a pas de contrat de sortie | l'énoncé annonce désormais le contrat : pour une liste vide, la fonction doit lever une erreur explicite |
| WARN 100 | Ahmed BENHADJ SALEM C2 | code `TRANSFERT` pour une précondition non demandée | remplacé par `METHODE`, portant sur l'explicitation de la division répétée |

## Défauts de phase 4 corrigés

| Niveau | Défaut | Correction |
|---|---|---|
| 4e | « aucune connaissance nouvelle » alors que le produit de relatifs et l'équation sont annoncés comme nouveautés | la phase est présentée comme une découverte guidée, et un bandeau exclut explicitement ce qui y est produit de toute mesure de progression |
| 3e | même contradiction sur le double produit et le vocabulaire des fonctions | distinction explicite entre ce qui est réinvesti et ce qui est nouveau, plus le bandeau |
| 2nde | même formulation, non relevée par l'audit mais identique | corrigée de la même manière, par cohérence |
| 1re spé | « la suite n'est qu'une évolution répétée » | remplacé par une définition exacte, précisant que seules certaines suites, dont les suites géométriques, modélisent une évolution répétée |
| 1re spé | le programme annoncé affichait u1 à u5 sous le nom de « cinq premiers termes » | `print(0, u)` ajouté avant la boucle, énoncé reformulé en « u0 puis les cinq termes suivants », et une question demande ce que le programme afficherait sans cette ligne |
| 1re NSI | milieu de dichotomie « 19 ou 25 selon la convention », puis décompte affirmé | la convention `m = (g + d) // 2` est fixée dans l'énoncé ; le corrigé déroule les trois tours et indique que l'autre convention donnerait deux comparaisons |
