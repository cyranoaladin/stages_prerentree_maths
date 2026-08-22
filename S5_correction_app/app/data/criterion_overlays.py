# -*- coding: utf-8 -*-
"""Overlays de correction, critère par critère.

Ce module ajoute à un critère ce que le référentiel V3 ne porte pas :

* un **libellé neutre**, qui dit ce que le critère mesure sans livrer la réponse ;
* une **rubrique de score**, qui associe chaque valeur proposée à une règle observable ;
* des **suggestions d'erreur propres au critère**, et non celles de tout l'item ;
* le cas échéant, une **correction de classement curriculaire**, adossée à une source
  officielle citée.

Rien ici ne modifie un document distribué, ni le total de 20 points, ni un identifiant.
Les valeurs proposées par l'interface sont exactement celles que la rubrique décrit :
un score partiel qu'on ne sait pas justifier ne doit pas être proposé.

Portée actuelle : les 22 critères d'Inès KEFI. Les autres élèves conservent le
classement V3 tant qu'une revue équivalente n'a pas été conduite pour eux — voir
``docs/FUTURE_CURRICULUM_REVIEW.md``.
"""

# --------------------------------------------------------------------- sources
# Références réellement consultées. Aucune n'est inventée ; chacune est citée telle
# qu'elle apparaît dans le document officiel.
SOURCES = {
    "ATT5": ("Attendus de fin d'année de cinquième — mathématiques, éduscol "
             "(14-maths-5e-attendus-eduscol1114744)"),
    "ATT4": ("Attendus de fin d'année de quatrième — mathématiques, éduscol "
             "(16-maths-4e-attendus-eduscol1114746)"),
    "PROG": ("Programme de mathématiques du cycle 4, arrêté MENE2018714A, "
             "BO n° 31 du 30 juillet 2020 — applicable à la Quatrième en 2026-2027"),
    "DIAG": ("Positionnement de pré-rentrée — mathématiques, entrée en Quatrième "
             "(4e_Test_Initial, 18 items), instrument ayant établi le diagnostic "
             "de fin de Cinquième d'Inès KEFI"),
    "REPO": ("Tableau N-1 → N du dossier de stage, "
             "4e/05_SOURCES/stage_prerentree_quatrieme_maths.md § 3.1"),
}

CERTAINTY = ("haute", "moyenne", "faible")

# Codes d'erreur employés ici ; ils appartiennent tous à la nomenclature S5.
# ---------------------------------------------------------------------------

OVERLAYS = {

    # ================================================================= A1
    "4E_INES_KEFI_A1_c1": {
        "neutral_label": "Somme algébrique de relatifs, avec soustraction d'un négatif",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième : « Il additionne et soustrait des "
                      "nombres décimaux relatifs » et « Il sait que soustraire revient à "
                      "additionner l'opposé ». Le produit de relatifs, lui, relève de la "
                      "Quatrième et n'intervient pas ici."),
        "rubric": [
            (100, "résultat exact"),
            (50, "l'opposé est correctement pris — la soustraction du négatif est "
                 "traitée — mais le calcul aboutit à une valeur fausse"),
            (0, "aucun élément exploitable, ou la soustraction du négatif est traitée "
                "comme une soustraction ordinaire"),
        ],
        "errors": [
            ("CONCEPT", "soustraire un négatif traité comme une soustraction ordinaire "
                        "(résultat −10)"),
            ("CALCUL", "erreur isolée sur la première somme (−8 + 3)"),
        ],
    },

    # ================================================================= A2
    "4E_INES_KEFI_A2_c1": {
        "neutral_label": "Différence de deux fractions dont un dénominateur est multiple "
                         "de l'autre",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième : « Il additionne ou soustrait des "
                      "fractions dont les dénominateurs sont égaux ou multiples l'un de "
                      "l'autre ». Ici 8 est un multiple de 4 : la question tombe "
                      "exactement dans cet attendu. Le cas général des dénominateurs "
                      "quelconques, lui, relève de la Quatrième."),
        "rubric": [
            (100, "résultat exact, sous forme réduite ou non"),
            (50, "mise au même dénominateur correcte, soustraction des numérateurs fausse"),
            (0, "aucun élément exploitable"),
        ],
        "errors": [
            ("CONCEPT", "numérateurs et dénominateurs soustraits séparément"),
            ("METHODE", "aucune mise au même dénominateur"),
        ],
    },

    # ================================================================= A3
    "4E_INES_KEFI_A3_c1": {
        "neutral_label": "Réduction d'une expression mêlant termes en x et constantes signées",
        "scope": "mixed",
        "certainty": "moyenne",
        "source": "ATT5",
        "rationale": ("Les attendus de fin de cinquième bornent explicitement la "
                      "réduction à la forme « ax + bx » — leurs exemples sont "
                      "« 5,2x + 3,4x » et « 2,4x − 2,1x », sans constante. Les attendus "
                      "de quatrième énoncent la réduction sans restriction. L'expression "
                      "posée mêle les deux : le regroupement des termes en x est un "
                      "acquis de Cinquième, l'écriture réduite complète avec constantes "
                      "signées relève de la formulation de Quatrième. Le critère est "
                      "donc déclaré mixte plutôt que tranché arbitrairement."),
        "virtual_split": [
            {"suffix": "v1", "points": 50, "scope": "n_minus_1",
             "analysis_skill_id": "M4E_LIT_02",
             "label": "Regroupement des termes en x",
             "rubric": [
                 (50, "les termes en x sont correctement regroupés"),
                 (0, "les termes en x ne sont pas regroupés, ou le sont faussement"),
             ],
             "errors": [
                 ("CONCEPT", "termes en x et constantes additionnés ensemble"),
                 ("CALCUL", "erreur sur la soustraction des coefficients"),
             ]},
            {"suffix": "v2", "points": 50, "scope": "bridge_n",
             "analysis_skill_id": "M4E_LIT_02_REDUCTION_COMPLETE",
             "label": "Écriture réduite complète, constantes signées comprises",
             "rubric": [
                 (50, "les constantes signées sont correctement regroupées et "
                      "l'expression est écrite sous la forme ax + b"),
                 (0, "constantes non regroupées, ou signe mal traité"),
             ],
             "errors": [
                 ("CALCUL", "erreur de signe sur la somme des constantes"),
                 ("NOTATION", "expression laissée sous une forme non réduite"),
             ]},
        ],
    },

    # ================================================================= A4
    "4E_INES_KEFI_A4_c1": {
        "neutral_label": "Second angle aigu d'un triangle rectangle",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième, connaissances mobilisables dans un "
                      "raisonnement : « la somme des angles d'un triangle »."),
        "rubric": [
            (100, "mesure exacte"),
            (50, "méthode correcte — l'angle droit est bien retiré — mais le calcul "
                 "aboutit à une valeur fausse"),
            (0, "aucun élément exploitable"),
        ],
        "errors": [
            ("METHODE", "180° − 37° calculé sans retirer l'angle droit"),
            ("LECTURE", "le caractère rectangle du triangle n'est pas exploité"),
        ],
    },

    # ================================================================= A5
    "4E_INES_KEFI_A5_c1": {
        "neutral_label": "Ordre croissant de cinq nombres relatifs",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième : « Il repère sur une droite graduée "
                      "les nombres décimaux relatifs » et « Il compare, range et "
                      "encadre »."),
        "rubric": [
            (100, "les cinq nombres dans le bon ordre"),
            (50, "les positifs et le zéro sont correctement placés, les négatifs sont "
                 "ordonnés entre eux à l'envers"),
            (0, "ordre non exploitable"),
        ],
        "errors": [
            ("CONCEPT", "relatifs ordonnés comme des distances : −5 placé avant −8 "
                        "et −12"),
        ],
    },

    # ================================================================= A6
    "4E_INES_KEFI_A6_c1": {
        "neutral_label": "Fraction égale et facteur employé",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième : « Il reconnaît et produit des "
                      "fractions égales »."),
        "rubric": [
            (100, "numérateur exact et facteur explicitement écrit"),
            (50, "numérateur exact mais facteur non écrit, ou facteur correct sans "
                 "numérateur juste"),
            (0, "aucun élément exploitable"),
        ],
        "errors": [
            ("CONCEPT", "facteur appliqué au seul dénominateur"),
            ("NOTATION", "facteur non écrit alors qu'il est demandé"),
        ],
    },

    # ================================================================= B1
    "4E_INES_KEFI_B1_c1": {
        "neutral_label": "Aire et périmètre d'un rectangle, unités comprises",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième : « Il calcule le périmètre et l'aire "
                      "des figures usuelles (rectangle, parallélogramme, triangle…) », et "
                      "contrôle la cohérence d'une unité."),
        "rubric": [
            (100, "aire et périmètre exacts, avec les unités correctes (m² et m)"),
            (75, "les deux calculs exacts, une unité manquante ou erronée"),
            (50, "un des deux calculs exact, avec son unité"),
            (25, "formule pertinente engagée, aucun résultat abouti"),
            (0, "aucun élément mathématiquement exploitable"),
        ],
        "errors": [
            ("CONCEPT", "aire et périmètre confondus"),
            ("NOTATION", "unité m employée pour une aire, ou unité absente"),
            ("CALCUL", "erreur sur 12 × 7 ou sur 2 × (12 + 7)"),
        ],
    },
    "4E_INES_KEFI_B1_c2": {
        "neutral_label": "Prix du carrelage, obtenu à partir de la grandeur pertinente",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième : « Il résout des problèmes de "
                      "proportionnalité […] passage à l'unité, coefficient de "
                      "proportionnalité ». Le prix au mètre carré est un coefficient "
                      "appliqué directement ; ce n'est pas la recherche d'une quatrième "
                      "proportionnelle, qui relève de la Quatrième — malgré le libellé "
                      "de la compétence d'origine."),
        "rubric": [
            (100, "prix exact, calculé à partir de l'aire"),
            (50, "démarche correcte — prix unitaire multiplié par une grandeur — mais "
                 "grandeur inadaptée ou erreur de calcul"),
            (0, "aucun élément exploitable"),
        ],
        "errors": [
            ("METHODE", "prix calculé à partir du périmètre au lieu de l'aire"),
            ("CALCUL", "erreur sur le produit 84 × 26"),
        ],
    },

    # ================================================================= B2
    "4E_INES_KEFI_B2_c1": {
        "neutral_label": "Développement d'un produit du type k(a − b)",
        "scope": "bridge_n",
        "certainty": "haute",
        "source": "ATT4",
        "rationale": ("Les attendus de fin de cinquième ne mentionnent la distributivité "
                      "que pour « réduire une expression littérale de la forme ax + bx » ; "
                      "leurs exemples ne comportent aucune parenthèse à développer. Les "
                      "attendus de fin de quatrième énoncent au contraire : « Il utilise "
                      "la propriété de distributivité simple pour développer un produit », "
                      "avec pour exemple « 3(4x − 2) », de forme identique à la question "
                      "posée. Le développement est donc une passerelle vers la Quatrième, "
                      "et non un acquis de Cinquième."),
        "interpretation_limits": [
            "une non-réussite ici ne documente aucune fragilité de calcul littéral de "
            "Cinquième : le regroupement de termes semblables est mesuré séparément en A3",
        ],
        "rubric": [
            (50, "développement exact, signe compris"),
            (25, "la distributivité est appliquée aux deux termes, mais le signe du "
                 "second est faux"),
            (0, "distributivité appliquée à un seul terme, ou aucun élément exploitable"),
        ],
        "errors": [
            ("CONCEPT", "distributivité appliquée au seul premier terme (5x − 3)"),
            ("CALCUL", "erreur de signe sur le second terme (5x + 15)"),
        ],
    },
    "4E_INES_KEFI_B2_c2": {
        "neutral_label": "Réduction de l'expression obtenue après développement",
        "scope": "bridge_n",
        "certainty": "moyenne",
        "source": "ATT4",
        "rationale": ("Cette réduction porte sur une expression issue d'un développement "
                      "qui relève lui-même de la Quatrième : elle en est conditionnée. "
                      "Les attendus de cinquième ne couvrent la réduction que pour la "
                      "forme ax + bx, sans terme constant issu d'un développement."),
        "fairness_rules": [
            "la réduction est appréciée sur l'expression que l'élève a effectivement "
            "obtenue au développement : une erreur de développement ne doit pas être "
            "sanctionnée deux fois",
        ],
        "rubric": [
            (50, "réduction exacte, termes en x et constantes correctement regroupés"),
            (25, "les termes en x sont correctement regroupés mais les constantes ne le "
                 "sont pas, ou l'inverse"),
            (0, "aucune réduction exploitable"),
        ],
        "errors": [
            ("CONCEPT", "termes en x et constantes additionnés ensemble"),
            ("CALCUL", "erreur de signe sur la somme des constantes"),
        ],
    },
    "4E_INES_KEFI_B2_c3": {
        "neutral_label": "Contrôle du résultat par substitution d'une valeur",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième, explicitement : « Il substitue une "
                      "valeur numérique à une lettre pour […] contrôler son résultat ». "
                      "Le contrôle est donc un acquis de Cinquième, même lorsqu'il porte "
                      "sur une expression dont la production relève de la Quatrième."),
        "fairness_rules": [
            "le contrôle est crédité dès lors qu'il est effectivement conduit sur les "
            "deux écritures, même si le développement — qui est une passerelle — est "
            "erroné",
            "un élève qui détecte et signale le désaccord entre les deux écritures "
            "obtient la totalité du critère : c'est précisément ce que le contrôle sert "
            "à produire",
        ],
        "interpretation_limits": [
            "la réussite s'appuie sur une expression issue d'un développement de "
            "Quatrième ; ce critère mesure la pratique du contrôle, pas le développement",
        ],
        "rubric": [
            (100, "substitution menée sur les deux écritures et comparaison conclue"),
            (50, "substitution menée sur une seule écriture, ou sur les deux sans "
                 "conclusion écrite"),
            (0, "aucun contrôle mené"),
        ],
        "errors": [
            ("CONTROLE", "aucun contrôle mené alors qu'il est demandé"),
            ("CALCUL", "erreur dans la substitution numérique"),
        ],
    },

    # ================================================================= B3
    "4E_INES_KEFI_B3_c1": {
        "neutral_label": "Fréquence exprimée en pourcentage",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième : « Il calcule des effectifs et des "
                      "fréquences » et « Il relie fractions, proportions et "
                      "pourcentages »."),
        "rubric": [
            (100, "fréquence exacte, exprimée en pourcentage"),
            (50, "quotient correct mais laissé sous forme décimale ou fractionnaire, "
                 "sans conversion en pourcentage"),
            (0, "aucun élément exploitable"),
        ],
        "errors": [
            ("LECTURE", "effectif total mal lu"),
            ("METHODE", "quotient inversé (40 divisé par 14)"),
        ],
    },
    "4E_INES_KEFI_B3_c2": {
        "neutral_label": "Moyenne d'une série, somme et effectif apparents",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième : « Il calcule et interprète la "
                      "moyenne d'une série de données ». La médiane, elle, relève de la "
                      "Quatrième et n'est pas demandée ici."),
        "rubric": [
            (70, "moyenne exacte, somme et effectif visibles"),
            (35, "somme exacte mais division fausse, ou effectif erroné"),
            (0, "aucun élément exploitable"),
        ],
        "errors": [
            ("CALCUL", "erreur sur la somme des valeurs"),
            ("METHODE", "division par une valeur autre que l'effectif"),
        ],
    },
    "4E_INES_KEFI_B3_c3": {
        "neutral_label": "Contrôle de vraisemblance par encadrement",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Le contrôle de la cohérence d'un résultat est un attendu "
                      "transversal de fin de cinquième, associé au calcul de la moyenne."),
        "rubric": [
            (30, "l'encadrement entre la plus petite et la plus grande valeur est écrit"),
            (0, "aucun encadrement écrit"),
        ],
        "errors": [
            ("CONTROLE", "aucun encadrement écrit alors qu'il est demandé"),
        ],
    },

    # ================================================================= B4
    "4E_INES_KEFI_B4_c1": {
        "neutral_label": "Raisonnement rédigé en donnée – propriété – conclusion",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième : « Il mène des raisonnements en "
                      "utilisant des propriétés des figures » et connaît « une définition "
                      "et une propriété caractéristique du parallélogramme »."),
        "rubric": [
            (100, "les trois temps sont présents, la propriété est nommée, la conclusion "
                  "est exacte"),
            (75, "conclusion exacte et propriété nommée, rédaction incomplète"),
            (50, "conclusion exacte, sans propriété nommée"),
            (25, "propriété évoquée sans conclusion"),
            (0, "aucun élément exploitable"),
        ],
        "errors": [
            ("JUSTIFICATION", "conclusion exacte mais propriété non nommée"),
            ("CONCEPT", "propriété caractéristique du parallélogramme mal identifiée"),
        ],
    },
    "4E_INES_KEFI_B4_c2": {
        "neutral_label": "Réfutation appuyée sur un contre-exemple",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième : raisonner à partir des propriétés "
                      "des figures. Un contre-exemple suffit à réfuter une affirmation ; "
                      "aucune démonstration générale n'est demandée."),
        "rubric": [
            (100, "réponse négative et contre-exemple explicite"),
            (50, "réponse négative correcte, sans contre-exemple"),
            (0, "réponse affirmative, ou aucun élément exploitable"),
        ],
        "errors": [
            ("JUSTIFICATION", "réponse correcte mais aucun contre-exemple produit"),
            ("CONCEPT", "carré et parallélogramme confondus"),
        ],
    },

    # ================================================================= C1
    "4E_INES_KEFI_C1_c1": {
        "neutral_label": "Aire d'une surface obtenue par soustraction",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième : calcul de l'aire des figures "
                      "usuelles et résolution de problèmes de grandeurs."),
        "rubric": [
            (100, "aire exacte, soustraction de la fenêtre visible"),
            (50, "les deux aires sont calculées mais non soustraites, ou erreur de calcul "
                 "sur la différence"),
            (0, "aucun élément exploitable"),
        ],
        "errors": [
            ("LECTURE", "la fenêtre n'est pas déduite de la surface du mur"),
            ("CALCUL", "erreur sur la différence des aires"),
            ("NOTATION", "unité absente ou incorrecte"),
        ],
    },
    "4E_INES_KEFI_C1_c2": {
        "neutral_label": "Fraction d'une grandeur",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Prendre le tiers d'une grandeur relève de l'usage des fractions "
                      "comme opérateurs, acquis de Cinquième."),
        "rubric": [
            (50, "aire exacte, le tiers étant pris sur la bonne surface"),
            (25, "division par 3 correctement conduite, mais sur la mauvaise surface"),
            (0, "aucun élément exploitable"),
        ],
        "errors": [
            ("CONCEPT", "tiers pris sur l'aire totale du mur au lieu de la surface à "
                        "peindre"),
            ("CALCUL", "erreur sur la division par 3"),
        ],
    },
    "4E_INES_KEFI_C1_c3": {
        "neutral_label": "Expression littérale d'un coût, puis calcul pour une valeur",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième : « Il produit une expression "
                      "littérale pour élaborer une formule ou traduire un programme de "
                      "calcul » et « Il substitue une valeur numérique à une lettre pour "
                      "calculer la valeur d'une expression littérale ». Aucune "
                      "transformation d'expression n'est demandée ici."),
        "rubric": [
            (150, "expression correcte, substitution écrite et valeur exacte"),
            (100, "expression correcte, mais substitution non écrite ou valeur fausse"),
            (50, "un seul des deux termes de l'expression est correct — le terme "
                 "variable ou le terme constant"),
            (0, "aucune expression exploitable"),
        ],
        "errors": [
            ("TRANSFERT", "aucune expression littérale produite malgré la demande"),
            ("CONCEPT", "frais fixes intégrés au terme variable"),
            ("CALCUL", "erreur dans le calcul de la valeur demandée"),
        ],
    },
    "4E_INES_KEFI_C1_c4": {
        "neutral_label": "Décision justifiée par comparaison à un budget",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Substituer une valeur puis comparer deux nombres pour décider "
                      "relève des attendus de fin de cinquième ; aucune mise en équation "
                      "n'est requise."),
        "rubric": [
            (100, "valeur calculée et conclusion explicitement écrite"),
            (50, "calcul correct sans conclusion écrite, ou conclusion sans calcul"),
            (0, "aucun élément exploitable"),
        ],
        "errors": [
            ("TRANSFERT", "comparaison au budget non effectuée"),
            ("JUSTIFICATION", "décision annoncée sans être appuyée sur le calcul"),
        ],
    },

    # ================================================================= C2
    "4E_INES_KEFI_C2_c1": {
        "neutral_label": "Abscisse finale après deux déplacements sur une droite graduée",
        "scope": "n_minus_1",
        "certainty": "haute",
        "source": "ATT5",
        "rationale": ("Attendus de fin de cinquième : « Il repère sur une droite graduée "
                      "les nombres décimaux relatifs » ; les déplacements se traduisent "
                      "par des additions et soustractions de relatifs, également au "
                      "programme de Cinquième."),
        "rubric": [
            (100, "abscisse finale exacte, les deux déplacements visibles"),
            (50, "un seul des deux déplacements correctement traité"),
            (0, "aucun élément exploitable"),
        ],
        "errors": [
            ("CONCEPT", "sens des déplacements inversé"),
            ("CALCUL", "erreur sur l'une des deux opérations"),
        ],
    },
    "4E_INES_KEFI_C2_c2": {
        "neutral_label": "Produit de deux relatifs et justification du signe",
        "scope": "bridge_n",
        "certainty": "haute",
        "source": "ATT4",
        "rationale": ("Attendus de fin de quatrième : « Il effectue avec des nombres "
                      "décimaux relatifs, des produits et des quotients ». Les attendus "
                      "de cinquième s'arrêtent à l'addition et à la soustraction. Le "
                      "livret de la séance annonce d'ailleurs cette notion comme une "
                      "découverte de Quatrième."),
        "interpretation_limits": [
            "une non-réussite ici ne documente aucune fragilité sur la somme et la "
            "différence de relatifs, mesurées séparément en A1, A5 et C2 question 1",
        ],
        # La couche V3 pose la même mise en garde, mais sans « et C2 question 1 » :
        # la question 1 de C2 mesure justement la somme et la différence de relatifs,
        # et c'est ce qui rend la limite complète. Les deux formulations affichées
        # côte à côte donnaient deux phrases quasi identiques ; celle-ci les remplace.
        "interpretation_limits_mode": "replace",
        "rubric": [
            (100, "produit exact et signe justifié par une phrase"),
            (50, "produit exact sans justification du signe, ou justification correcte "
                 "assortie d'une erreur de calcul"),
            (0, "aucun élément exploitable"),
        ],
        "errors": [
            ("CONCEPT", "règle des signes non disponible (résultat −28)"),
            ("JUSTIFICATION", "résultat exact mais aucune phrase de justification"),
        ],
    },
}


def for_criterion(criterion_id):
    return OVERLAYS.get(criterion_id)


def covered_criteria():
    return sorted(OVERLAYS)
