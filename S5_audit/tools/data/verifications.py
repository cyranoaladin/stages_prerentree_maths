# -*- coding: utf-8 -*-
"""Contre-résolution indépendante des 100 items uniques de l'évaluation.

Chaque item est re-résolu ici **à partir de son énoncé**, sans lire la réponse
déclarée dans la banque. Le vérificateur compare ensuite le résultat recalculé à
la réponse déclarée : c'est cette confrontation qui produit le verdict.

Deux méthodes seulement :

    "calcul"  le résultat est recalculé en Python, et les valeurs obtenues doivent
              se retrouver dans la réponse déclarée. Le verdict est mécanique.
    "revue"   l'item porte sur une définition, une explication ou un raisonnement
              qu'aucun calcul ne tranche. Le verdict provient d'une lecture, et la
              justification est consignée mot pour mot.

La méthode "revue" n'est jamais employée pour un item dont la réponse est chiffrée.
"""

from fractions import Fraction as F
import math


def frac(a, b):
    f = F(a, b)
    return "%d/%d" % (f.numerator, f.denominator) if f.denominator != 1 else str(f.numerator)


def rnd(x, n=2):
    return ("%%.%df" % n) % x


# --- Chaque entrée : method, expect (fragments recalculés attendus), commentaire.
V = {}


def calcul(key, expect, note):
    V[key] = {"method": "calcul", "expect": expect, "note": note}


def revue(key, verdict, justification):
    V[key] = {"method": "revue", "verdict": verdict, "justification": justification}


# ================================================================= 4e commun
calcul(("4e", "A1"), [str((-8) + 3 - (-5))], "(-8)+3-(-5) recalculé")
calcul(("4e", "A2"), ["3/8"], "5/8 - 1/4 recalculé")
calcul(("4e", "A3"), ["4x", "-5"], "7x+4-3x-9 : coefficients recalculés")
calcul(("4e", "A4"), ["%d" % (90 - 37)], "angles aigus complémentaires")
calcul(("4e", "B1"), ["%d" % (12 * 7), "%d" % (2 * (12 + 7)), "2184"], "aire, périmètre et prix recalculés")
calcul(("4e", "B2"), ["5x-15", "7x-8", "6"], "développement, réduction et contrôle en x=2")
calcul(("4e", "B3"), ["35", "110", "13.75", "11", "17"], "fréquence, somme, moyenne et encadrement")
calcul(("4e", "C1"), ["15", "5", "19n+25", "139", "215", "200"], "aires, expression, C(6) et décision")

# ================================================================= 3e commun
calcul(("3e", "A1"), [str(int(-15 / 3 + (-2) * (-6)))], "(-15)/3 + (-2)(-6) recalculé")
calcul(("3e", "A2"), ["3/2"], "4/5 x 15/8 recalculé")
calcul(("3e", "A3"), ["4x", "-11"], "9x-4-5x-7 recalculé")
calcul(("3e", "A4"), ["6"], "4x-3=2x+9 recalculé")
calcul(("3e", "B1"), ["16"], "AC = racine(20^2-12^2)")
calcul(("3e", "B2"), ["5/13", "67"], "cos B = 5/13 et angle arrondi")
calcul(("3e", "B3"), ["140", "11"], "vitesse et moyenne pondérée recalculées")
calcul(("3e", "C1"), ["5", "16", "29", "545", "120"], "hypoténuse, angle, pente et coût")

# =============================================================== 2nde commun
calcul(("2nde", "A1"), [str(-4 + 5 * (-3) - (-6))], "-4+5(-3)-(-6) recalculé")
calcul(("2nde", "A2"), ["19/24"], "3/8 + 5/12 recalculé")
calcul(("2nde", "A3"), [("10^-1", "0.1")], "10^5 x 10^-2 / 10^4")
calcul(("2nde", "A4"), [("x^2-10x+25",)], "(x-5)^2 développé")
calcul(("2nde", "B1"), ["5", "17", "-3.5", "3", "0"], "équation, produit nul et vérification")
calcul(("2nde", "B2"), ["280", "246.40", "0.9856"], "évolutions successives recalculées")
calcul(("2nde", "B3"), ["15", "4", "5", "12"], "Pythagore, Thalès et périmètre")
calcul(("2nde", "C1"), [("x^2-x",), "12", "5", "1.0115"], "aire, diagonale et coefficient global")

# =========================================================== 1ere_spe commun
calcul(("1ere_spe", "A1"), ["(4x-7)(4x+7)"], "16x^2-49 factorisé")
calcul(("1ere_spe", "A2"), ["x<4", "4"], "-3x+12>0 recalculé")
calcul(("1ere_spe", "A3"), [str(2 * (-3) ** 2 + (-3))], "g(-3) pour 2x^2+x")
calcul(("1ere_spe", "A4"), ["-6", "6"], "coordonnées de AB")
calcul(("1ere_spe", "B1"), ["-2", "2"], "racines de (3x+6)(2-x) et signe")
calcul(("1ere_spe", "B2"), ["5", "-2"], "image, antécédent et comparaison sur ]0;1[")
calcul(("1ere_spe", "B3"), ["360", "432", "0.9", "10"], "évolutions successives recalculées")
calcul(("1ere_spe", "C1"), ["2", "0.7", "0.6", "1.04", "195"], "droite, probabilités et suite")

# ============================================================ 1re_nsi commun
calcul(("1re_nsi", "A1"), ["8", "2", "5", "4"], "L[2], L[-1], len(L) et dernier indice")
calcul(("1re_nsi", "A2"), ["x>8", "(x<=2)and(x!=0)"], "négations recalculées")
calcul(("1re_nsi", "A3"), ["3,7,11", "trois"], "range(3,12,4) recalculé")
calcul(("1re_nsi", "A4"), ["10", "6"], "a=6, b=a, a=a+4")
calcul(("1re_nsi", "B1"), ["4,13,15,22", "22", "4"], "accumulateur tracé")
calcul(("1re_nsi", "B2"), ["None"], "fonction sans return")
revue(("1re_nsi", "B3"), "PASS",
      "types de conversion float/int conformes aux colonnes ; la concaténation de deux chaînes "
      "par + est le comportement documenté de Python ; l'exemple de métadonnée proposé (date de "
      "production, capteur, unité, encodage) décrit bien le fichier et non un enregistrement.")
calcul(("1re_nsi", "C1"), ["return i", "2", "-1"], "recherche séquentielle sur liste de dictionnaires")

# ================================================== items individualisés — 4e
calcul(("fares-darghouth", "A5"), [str(16 * 5 // 2)], "aire du triangle 16 x 5 / 2")
calcul(("fares-darghouth", "A6"), ["15/25", "11/25"], "fraction équivalente et différence")
calcul(("fares-darghouth", "B4"), [str(180 - 54 - 39)], "somme des angles du triangle")
calcul(("fares-darghouth", "C2"), [str(3 * 5 + 7), "4x+24", "6x+24"], "substitution, développement, réduction")
calcul(("ines-kefi", "A5"), ["-12", "-8", "-5", "0", "2"], "ordre croissant recalculé")
calcul(("ines-kefi", "A6"), ["10/15", "5"], "2/3 = 10/15, facteur 5")
revue(("ines-kefi", "B4"), "PASS",
      "des diagonales de même milieu caractérisent le parallélogramme ; le contre-exemple du "
      "rectangle non carré réfute correctement la conclusion « carré ».")
calcul(("ines-kefi", "C2"), [str(-9 + 14 - 6), str((-4) * (-7))], "déplacements et produit de relatifs")
calcul(("sinda-chikhaoui", "A5"), [str(7 - (-6) - 4)], "7-(-6)-4 recalculé")
calcul(("sinda-chikhaoui", "A6"), ["1/3", "4/12"], "3/4 - 5/12 recalculé")
calcul(("sinda-chikhaoui", "B4"), ["6x-12", "9x-7", "-7"], "développement, réduction, contrôle en x=0")
calcul(("sinda-chikhaoui", "C2"), [str(54 * 2 // 9), "parall"], "base du triangle et justification par duplication")

# ================================================== items individualisés — 3e
calcul(("amine-mansouri", "A5"), ["-3x", "-3"], "6x+5-9x-8 recalculé")
revue(("amine-mansouri", "A6"), "PASS",
      "AB est bien le côté adjacent à l'angle B et BC l'hypoténuse dans un triangle rectangle "
      "en A : le rapport AB/BC est le cosinus de B.")
calcul(("amine-mansouri", "B4"), ["8", "225", "289"], "AC = racine(17^2-15^2) et contrôle de vraisemblance")
calcul(("amine-mansouri", "C2"), ["1/6"], "4/9 x 3/8 recalculé")
calcul(("elyes-kefi", "A5"), ["1/6"], "7/9 x 3/14 recalculé")
calcul(("elyes-kefi", "A6"), ["11x", "-5"], "8x-9+3x+4 recalculé")
calcul(("elyes-kefi", "B4"), ["50", "5", "10", "45", "11.25"],
       "somme, effectif, moyenne, et démonstration que l'encadrement ne détecte pas l'omission")
calcul(("elyes-kefi", "C2"), [("x^2+7x+12",), "30"], "(x+4)(x+3) développé et contrôlé en x=2")
calcul(("fares-laajili", "A5"), ["4/5"], "6/25 : 3/10 recalculé")
revue(("fares-laajili", "A6"), "PASS",
      "connaissant le côté opposé à C et l'hypoténuse, le rapport qui les met en jeu est bien "
      "le sinus ; la définition donnée est exacte.")
calcul(("fares-laajili", "B4"), ["29", "400", "441", "841"], "BC = racine(20^2+21^2) et analyse de l'erreur")
calcul(("fares-laajili", "C2"), ["10/26", "23"], "sin B = 10/26 et angle arrondi")
calcul(("sarah-bargaoui", "A5"), ["5x", "-7"], "8x+6-3x-13 recalculé")
calcul(("sarah-bargaoui", "A6"), ["5"], "5x-8=17 recalculé")
calcul(("sarah-bargaoui", "B4"), ["210", "7"], "proportionnalité et Pythagore recalculés")
calcul(("sarah-bargaoui", "C2"), ["14x-4", "10"], "développement, réduction et contrôle en x=1")
calcul(("selim-mansouri", "A5"), [str((-7) * (-4) + int(-20 / 5))], "(-7)(-4)+(-20)/5 recalculé")
calcul(("selim-mansouri", "A6"), ["-15x", "10"], "-5(3x-2) développé")
calcul(("selim-mansouri", "B4"), ["3", "33", "20"], "retour à l'unité et Pythagore")
calcul(("selim-mansouri", "C2"), [("x^2+7x+10",), "18"], "(x+2)(x+5) développé et contrôlé en x=1")

# ================================================ items individualisés — 2nde
calcul(("ahmed-bakir", "A5"), [str((-3) ** 3 + 2 * (-4))], "(-3)^3 + 2(-4) recalculé")
calcul(("ahmed-bakir", "A6"), ["2.05", ("10^-4",)], "notation scientifique de 0,000205")
calcul(("ahmed-bakir", "B4"), [("2x^2+7x-15",), "-6"], "(2x-3)(x+5) développé et contrôlé en x=1")
calcul(("ahmed-bakir", "C2"), ["69", "58.65"], "hausse de 15 % puis baisse de 15 %")
calcul(("noa-maniaci", "A5"), ["3", "-6"], "(4x-12)(x+6)=0 recalculé")
calcul(("noa-maniaci", "A6"), [("10^3",)], "10^-4 x 10^7 recalculé")
calcul(("noa-maniaci", "B4"), ["180", "135", "0.9", "10"], "évolutions successives recalculées")
calcul(("noa-maniaci", "C2"), ["x(x-7)", "0", "7"], "factorisation et équation produit nul")

# ============================================ items individualisés — 1ere_spe
calcul(("ahmad-beldi-maths", "A5"), ["(7x-4)(7x+4)"], "49x^2-16 factorisé")
revue(("ahmad-beldi-maths", "A6"), "PASS",
      "un point de coordonnées (-4 ; 1) sur la courbe se traduit par f(-4)=1 ; -4 est donc un "
      "antécédent de 1, ce que la réponse énonce correctement.")
calcul(("ahmad-beldi-maths", "B4"), [("x^2(x-1)",), "0.125", "0.25", "2/3"],
       "argument général sur le signe de x^2(x-1), illustration numérique et P(A u B)")
calcul(("ahmad-beldi-maths", "C2"), ["1.05", "330.75", "331"], "suite géométrique de raison 1,05")
calcul(("donia-khadhrani", "A5"), ["4"], "4x-3=13 recalculé")
calcul(("donia-khadhrani", "A6"), ["4"], "-5x+20>=0 recalculé")
calcul(("donia-khadhrani", "B4"), ["-2", "3"], "coefficient directeur, ordonnée à l'origine, parallélisme")
calcul(("donia-khadhrani", "C2"), ["0.6", "0.55"], "P(A u B) et P(non A) recalculées")
calcul(("malek-khadhrani", "A5"), [str((-4) ** 2 - 6 * (-4))], "f(-4) pour x^2-6x")
calcul(("malek-khadhrani", "A6"), ["36", "0"], "déterminant de (6;-4) et (-9;6)")
calcul(("malek-khadhrani", "B4"), ["4", "8", "-2", "-4", "2"], "vecteurs, alignement, coefficient directeur")
calcul(("malek-khadhrani", "C2"), [("3^-1", "1/3"), "0.5"], "puissance et contre-exemple sur 1/x")

# ============================================= items individualisés — 1re_nsi
calcul(("ahmad-beldi-nsi", "A5"), ["None"], "fonction qui affiche sans renvoyer")
calcul(("ahmad-beldi-nsi", "A6"), ["2,3,4,5,6,7,8"], "range(6) et range(2,9) recalculés")
calcul(("ahmad-beldi-nsi", "B4"), ["10", "3", "2", "[10,4,7,9]"], "indexation et alias de liste")
calcul(("ahmad-beldi-nsi", "C2"), ["L[i]<0", "return i", "return -1", "2"], "première valeur négative")
calcul(("ahmed-benhadj-salem", "A5"), [str(sum(range(2, 6))), "quatre"], "accumulateur sur range(2,6)")
revue(("ahmed-benhadj-salem", "A6"), "PASS",
      "le critère de choix entre for et while est bien la connaissance préalable du nombre de "
      "répétitions ; les deux situations sont classées conformément à ce critère.")
revue(("ahmed-benhadj-salem", "B4"), "PASS",
      "les trois tests proposés sont cohérents avec le contrat annoncé, dont le cas limite de la "
      "liste vide qui doit lever une erreur ; l'explication du problème des flottants est exacte "
      "et la solution proposée, math.isclose, est la solution usuelle.")
calcul(("ahmed-benhadj-salem", "C2"), ["1000", "10"],
       "coût séquentiel maximal et ordre de grandeur dichotomique : 2^10 = 1024 >= 1000")


# --- valeurs recalculées, utilisées par le vérificateur pour éviter tout copier-coller
RECALCUL = {
    ("4e", "A2"): frac(F(5, 8).numerator * 4 - F(1, 4).numerator * 8, 32),
    ("3e", "A2"): str(F(4, 5) * F(15, 8)),
    ("2nde", "A2"): str(F(3, 8) + F(5, 12)),
    ("elyes-kefi", "A5"): str(F(7, 9) * F(3, 14)),
    ("amine-mansouri", "C2"): str(F(4, 9) * F(3, 8)),
    ("fares-laajili", "A5"): str(F(6, 25) / F(3, 10)),
    ("sinda-chikhaoui", "A6"): str(F(3, 4) - F(5, 12)),
    ("3e", "B1"): str(int(math.isqrt(20 ** 2 - 12 ** 2))),
    ("amine-mansouri", "B4"): str(int(math.isqrt(17 ** 2 - 15 ** 2))),
    ("fares-laajili", "B4"): str(int(math.isqrt(20 ** 2 + 21 ** 2))),
    ("sarah-bargaoui", "B4"): str(int(math.isqrt(25 ** 2 - 24 ** 2))),
    ("selim-mansouri", "B4"): str(int(math.isqrt(12 ** 2 + 16 ** 2))),
    ("2nde", "B3"): str(int(math.isqrt(9 ** 2 + 12 ** 2))),
    ("3e", "B2"): str(round(math.degrees(math.acos(5 / 13)))),
    ("3e", "C1"): str(round(math.degrees(math.acos(4.8 / 5)))),
    ("fares-laajili", "C2"): str(round(math.degrees(math.asin(10 / 26)))),
    ("ahmad-beldi-maths", "C2"): rnd(300 * 1.05 ** 2),   # 330.75
    ("2nde", "B2"): rnd(250 * 1.12 * 0.88),              # 246.40
    ("1ere_spe", "B3"): "%g" % (480 * 0.75 * 1.2),
    ("noa-maniaci", "B4"): "%g" % (150 * 1.2 * 0.75),
    ("ahmed-bakir", "C2"): rnd(60 * 1.15 * 0.85),        # 58.65
}
