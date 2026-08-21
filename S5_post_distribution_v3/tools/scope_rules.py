# -*- coding: utf-8 -*-
"""Classement curriculaire des critères déjà imprimés : N-1, passerelle vers N, mixte.

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
"""

SCOPES = ("n_minus_1", "bridge_n", "mixed")

# Statuts d'interprétation. Les statuts de passerelle ne contiennent volontairement
# aucun terme de déficit : on ne peut pas manquer ce qui n'a pas encore été enseigné.
N1_STATUSES = ("acquis_observe", "en_cours_de_consolidation", "fragile", "non_conclusif")
BRIDGE_STATUSES = ("first_exposure", "not_yet_installed", "bridge_to_revisit", "no_conclusion")

# Ce que le livret distribué déclare lui-même nouveau en phase 4, niveau par niveau.
# Citations relevées dans les PDF réellement remis aux élèves.
BRIDGE_DECLARED_IN_LIVRET = {
    "4e": {
        "citation": ("« Découverte guidée : construire, à partir d'acquis de Cinquième, deux "
                     "notions nouvelles de Quatrième — le signe d'un produit de relatifs et "
                     "l'équation du premier degré. »"),
        "notions": ["produit et quotient de relatifs, signe du produit",
                    "mise en équation et résolution d'une équation du premier degré"],
    },
    "3e": {
        "citation": ("« Ce qui est nouveau — et qui appartient au programme de Troisième : le "
                     "double produit (a+b)(c+d), et le statut de fonction donné à une expression "
                     "littérale, avec le vocabulaire « image » et « antécédent ». »"),
        "notions": ["double distributivité (a+b)(c+d)",
                    "entrée dans le langage des fonctions",
                    "sinus et tangente (programme de Troisième ; le cosinus relève de la Quatrième)"],
    },
    "2nde": {
        "citation": ("« Ce qui est nouveau : la notation en intervalle et le vocabulaire "
                     "fonctionnel. »"),
        "notions": ["notation en intervalle",
                    "notations et approfondissements fonctionnels propres à la Seconde"],
    },
    "1ere_spe": {
        "citation": ("« Découverte guidée : […] deux notions nouvelles de Première — la suite "
                     "géométrique définie par récurrence et le taux de variation moyen. »"),
        "notions": ["suite définie par récurrence, notation u_(n+1)",
                    "taux de variation moyen"],
    },
    "1re_nsi": {
        "citation": ("« Ce qui est nouveau : les algorithmes de recherche eux-mêmes, leur "
                     "précondition et leur coût, qui appartiennent au programme de Première. »"),
        "notions": ["recherche séquentielle", "recherche dichotomique",
                    "précondition et coût d'un algorithme", "invariant de boucle"],
    },
}

# ---------------------------------------------------------------------------
# Exceptions au classement par défaut.
#
# Clé : (portée, ref, rang du critère dans l'item). La portée vaut le niveau pour
# un item du noyau commun, l'identifiant de l'élève pour un item individualisé —
# exactement la convention déjà employée par le barème de S5_cloture.
#
# Champs : scope, analysis_skill_id (alias analytique, ou None pour conserver le
# skill_id d'origine), label de l'alias, justification, et éventuellement
# accepted_methods / interpretation_limits / virtual (pour un critère mixte).
# ---------------------------------------------------------------------------
EXCEPTIONS = {

    # ------------------------------------------------------------------ 4e
    # Le livret annonce le produit de relatifs comme une découverte de Quatrième.
    # La question imprimée reste rigoureusement inchangée ; seule sa lecture change.
    ("ines-kefi", "C2", 2): {
        "scope": "bridge_n",
        "analysis_skill_id": "M4E_REL_PROD_BRIDGE",
        "analysis_skill_label": "Produit de deux relatifs et justification du signe "
                                "(découverte de Quatrième)",
        "rationale": ("(-4) x (-7) et la justification du signe relèvent du produit de relatifs, "
                      "introduit en phase 4 de la séance comme notion nouvelle de Quatrième. Le "
                      "skill_id d'origine M4E_REL_01 ne porte que la somme et la différence de "
                      "relatifs, acquis de Cinquième : le confondre avec le produit fusionnerait "
                      "un acquis N-1 et une découverte N."),
        "interpretation_limits": [
            "une non-réussite ici ne documente aucune fragilité sur la somme et la différence "
            "de relatifs, mesurées séparément en A1 et A5",
        ],
    },

    # ------------------------------------------------------------------ 3e
    # Trigonométrie : le cosinus est un acquis de Quatrième, le sinus et la tangente
    # appartiennent au programme de Troisième. Un skill_id unique les fusionnait.
    ("3e", "B2", 1): {
        "scope": "n_minus_1",
        "analysis_skill_id": "M3_TRIGO_COS_NM1",
        "analysis_skill_label": "Nommer les côtés d'un triangle rectangle et employer le cosinus "
                                "(acquis de Quatrième)",
        "rationale": ("nommer le côté adjacent et l'hypoténuse puis choisir le cosinus est un "
                      "attendu de Quatrième."),
    },
    ("3e", "B2", 2): {
        "scope": "n_minus_1",
        "analysis_skill_id": "M3_TRIGO_COS_NM1",
        "analysis_skill_label": "Nommer les côtés d'un triangle rectangle et employer le cosinus "
                                "(acquis de Quatrième)",
        "rationale": "calcul d'un angle à partir du cosinus : attendu de Quatrième.",
    },
    ("3e", "B2", 3): {
        "scope": "bridge_n",
        "analysis_skill_id": "M3_TRIGO_SIN_BRIDGE",
        "analysis_skill_label": "Sinus et tangente : identification du rapport "
                                "(programme de Troisième)",
        "rationale": ("la question 3 demande le rapport liant le côté opposé et l'hypoténuse : "
                      "le sinus, qui appartient au programme de Troisième et non à celui de "
                      "Quatrième."),
        "interpretation_limits": [
            "une non-réussite ne documente aucune fragilité sur la trigonométrie de Quatrième, "
            "mesurée aux critères 1 et 2 du même item",
        ],
    },
    ("3e", "C1", 2): {
        "scope": "n_minus_1",
        "analysis_skill_id": "M3_TRIGO_COS_NM1",
        "analysis_skill_label": "Nommer les côtés d'un triangle rectangle et employer le cosinus "
                                "(acquis de Quatrième)",
        "rationale": ("la longueur de la rampe, c'est-à-dire l'hypoténuse, a été calculée à la "
                      "question précédente : l'angle au sol s'obtient donc par le cosinus, "
                      "acquis de Quatrième. Le contre-calcul de référence du dossier emploie "
                      "lui-même arccos(4,8/5)."),
        "accepted_methods": [
            "cosinus de l'angle au sol, à partir de la longueur au sol et de la rampe",
            "tangente, à partir de la hauteur et de la longueur au sol",
            "sinus, à partir de la hauteur et de la rampe",
        ],
    },
    ("amine-mansouri", "A6", 1): {
        "scope": "n_minus_1",
        "analysis_skill_id": "M3_TRIGO_COS_NM1",
        "analysis_skill_label": "Nommer les côtés d'un triangle rectangle et employer le cosinus "
                                "(acquis de Quatrième)",
        "rationale": "le rapport demandé lie le côté adjacent et l'hypoténuse : c'est le cosinus.",
    },
    ("fares-laajili", "A6", 1): {
        "scope": "bridge_n",
        "analysis_skill_id": "M3_TRIGO_SIN_BRIDGE",
        "analysis_skill_label": "Sinus et tangente : identification du rapport "
                                "(programme de Troisième)",
        "rationale": ("le rapport demandé lie le côté opposé et l'hypoténuse : c'est le sinus, "
                      "notion de Troisième."),
    },
    ("fares-laajili", "C2", 1): {
        "scope": "bridge_n",
        "analysis_skill_id": "M3_TRIGO_SIN_BRIDGE",
        "analysis_skill_label": "Sinus et tangente : identification du rapport "
                                "(programme de Troisième)",
        "rationale": ("les données fournies sont le côté opposé à l'angle et l'hypoténuse : la "
                      "voie directe est le sinus. Le contre-calcul de référence du dossier "
                      "emploie arcsin(10/26)."),
        "accepted_methods": [
            "sinus, directement à partir des données",
            "calcul préalable du troisième côté par le théorème de Pythagore, puis cosinus : "
            "voie entièrement N-1, mathématiquement correcte, à créditer intégralement",
        ],
        "interpretation_limits": [
            "si l'élève emprunte la voie Pythagore puis cosinus, la réussite documente un acquis "
            "de Quatrième et doit être signalée comme telle en observation, sans être reversée "
            "automatiquement au décompte N-1",
        ],
    },
    ("fares-laajili", "C2", 2): {
        "scope": "bridge_n",
        "analysis_skill_id": "M3_TRIGO_SIN_BRIDGE",
        "analysis_skill_label": "Sinus et tangente : identification du rapport "
                                "(programme de Troisième)",
        "rationale": "la mesure de l'angle découle du rapport choisi à la question précédente.",
        "accepted_methods": [
            "arcsin appliqué au rapport 10/26",
            "arccos appliqué au rapport obtenu après calcul du troisième côté",
        ],
    },
    # Double distributivité : le livret l'annonce comme nouveauté de Troisième, et le
    # manifeste marque déjà ces deux items « not_comparable ».
    ("elyes-kefi", "C2", 1): {
        "scope": "bridge_n",
        "analysis_skill_id": "M3_LIT_DOUBLE_DISTRIB_BRIDGE",
        "analysis_skill_label": "Double distributivité (a+b)(c+d) — découverte de Troisième",
        "rationale": ("(x+4)(x+3) relève du double produit, introduit en phase 4 de la séance. "
                      "Le skill_id d'origine M3E_LIT_01 porte la distributivité simple k(ax+b), "
                      "acquis de Quatrième."),
    },
    ("elyes-kefi", "C2", 2): {
        "scope": "n_minus_1",
        "analysis_skill_id": None,
        "rationale": ("conduire un contrôle numérique sur les deux écritures est une compétence "
                      "de Quatrième, indépendante de la nouveauté du développement."),
        "fairness_rules": [
            "le contrôle est crédité dès lors qu'il est effectivement conduit sur les deux "
            "écritures, même si le développement (passerelle) est erroné",
            "un élève qui détecte et signale le désaccord entre les deux écritures obtient la "
            "totalité du critère : c'est exactement ce que le contrôle sert à produire",
        ],
        "interpretation_limits": [
            "la réussite s'appuie sur un développement relevant d'une notion nouvelle ; ce "
            "critère ne doit pas être lu isolément comme une mesure du contrôle numérique",
        ],
    },
    ("selim-mansouri", "C2", 1): {
        "scope": "bridge_n",
        "analysis_skill_id": "M3_LIT_DOUBLE_DISTRIB_BRIDGE",
        "analysis_skill_label": "Double distributivité (a+b)(c+d) — découverte de Troisième",
        "rationale": "(x+2)(x+5) relève du double produit, introduit en phase 4 de la séance.",
    },
    ("selim-mansouri", "C2", 2): {
        "scope": "n_minus_1",
        "analysis_skill_id": None,
        "rationale": ("conduire un contrôle numérique sur les deux écritures est une compétence "
                      "de Quatrième, indépendante de la nouveauté du développement."),
        "fairness_rules": [
            "le contrôle est crédité dès lors qu'il est effectivement conduit sur les deux "
            "écritures, même si le développement (passerelle) est erroné",
            "un élève qui détecte et signale le désaccord entre les deux écritures obtient la "
            "totalité du critère",
        ],
        "interpretation_limits": [
            "la réussite s'appuie sur un développement relevant d'une notion nouvelle ; ce "
            "critère ne doit pas être lu isolément comme une mesure du contrôle numérique",
        ],
    },

    # ------------------------------------------------------------ 1ere_spe
    # Suites définies par récurrence : nouveauté de Première annoncée par le livret.
    # Le critère C1 c4 rétribue en un seul point deux choses séparables : l'écriture
    # de la relation de récurrence (Première) et l'application répétée d'un
    # coefficient multiplicateur (Seconde). Il est donc déclaré mixte et éclaté.
    ("1ere_spe", "C1", 4): {
        "scope": "mixed",
        "analysis_skill_id": None,
        "rationale": ("« Écrire la relation liant u_(n+1) et u_n, puis calculer u_2 » agrège en un "
                      "seul critère une notation de Première et un calcul d'évolution successive "
                      "de Seconde. Le critère imprimé est indivisible ; il est donc éclaté en "
                      "sous-critères analytiques virtuels, à somme de points strictement égale."),
        "virtual": [
            {"suffix": "v1", "share": 0.5, "scope": "bridge_n",
             "analysis_skill_id": "M1RE_SUITES_RECURRENCE_BRIDGE",
             "analysis_skill_label": "Suite définie par récurrence, notation u_(n+1) "
                                     "(découverte de Première)",
             "desc": "relation de récurrence u_(n+1) = 1,04 x u_n correctement écrite"},
            {"suffix": "v2", "share": 0.5, "scope": "n_minus_1",
             "analysis_skill_id": None,
             "desc": "u_2 obtenu par application répétée du coefficient multiplicateur, "
                     "évalué à partir de la relation écrite par l'élève"},
        ],
        "fairness_rules": [
            "le sous-critère de calcul est évalué à partir de la relation que l'élève a "
            "effectivement écrite : une relation fausse ne doit pas être pénalisée deux fois",
        ],
    },
    ("ahmad-beldi-maths", "C2", 1): {
        "scope": "bridge_n",
        "analysis_skill_id": "M1RE_SUITES_RECURRENCE_BRIDGE",
        "analysis_skill_label": "Suite définie par récurrence, notation u_(n+1) "
                                "(découverte de Première)",
        "rationale": ("l'écriture de u_(n+1) en fonction de u_n est la notation de suite "
                      "introduite en phase 4 de la séance ; le manifeste marque déjà cet item "
                      "« not_comparable »."),
    },
    ("ahmad-beldi-maths", "C2", 2): {
        "scope": "bridge_n",
        "analysis_skill_id": "M1RE_SUITES_RECURRENCE_BRIDGE",
        "analysis_skill_label": "Suite définie par récurrence, notation u_(n+1) "
                                "(découverte de Première)",
        "rationale": ("u_2 est ici demandé dans le cadre de la suite ; le classer en N-1 ferait "
                      "retomber sur la consolidation de Seconde l'échec éventuel d'une notation "
                      "nouvelle. Le coefficient multiplicateur reste mesuré en N-1 par les deux "
                      "critères de l'item B3."),
        "fairness_rules": [
            "u_2 est évalué à partir de la relation que l'élève a écrite à la question précédente",
        ],
    },

    # ------------------------------------------------------------- 1re_nsi
    # Recherche séquentielle, dichotomie, précondition, coût, invariant : le livret
    # les déclare nouveaux et le manifeste marque les items C1 et C2 « not_comparable ».
    ("1re_nsi", "C1", 1): {
        "scope": "bridge_n",
        "analysis_skill_id": "NSI1_ALGO_RECHERCHE_BRIDGE",
        "analysis_skill_label": "Algorithmes de recherche : séquentielle et dichotomique "
                                "(programme de Première NSI)",
        "rationale": "complétion de la boucle de recherche séquentielle, introduite en phase 4.",
    },
    ("1re_nsi", "C1", 2): {
        "scope": "bridge_n",
        "analysis_skill_id": "NSI1_ALGO_RECHERCHE_BRIDGE",
        "analysis_skill_label": "Algorithmes de recherche : séquentielle et dichotomique "
                                "(programme de Première NSI)",
        "rationale": "lecture du contrat de la recherche séquentielle, dont la valeur d'absence.",
    },
    ("1re_nsi", "C1", 3): {
        "scope": "n_minus_1",
        "analysis_skill_id": None,
        "rationale": ("écrire un test avec son résultat attendu sur un cas limite est une "
                      "compétence de test, travaillée en séances 3 et 4 et indépendante de "
                      "l'algorithme support : la valeur attendue se lit directement dans le code "
                      "imprimé, qui contient « return -1 »."),
        "interpretation_limits": [
            "le support du test est un algorithme de passerelle ; ce critère mesure la pratique "
            "de test, pas la maîtrise de la recherche séquentielle",
        ],
    },
    ("1re_nsi", "C1", 4): {
        "scope": "bridge_n",
        "analysis_skill_id": "NSI1_ALGO_RECHERCHE_BRIDGE",
        "analysis_skill_label": "Algorithmes de recherche : séquentielle et dichotomique "
                                "(programme de Première NSI)",
        "rationale": "gain et précondition de la dichotomie : attendus explicites de Première.",
    },
    ("ahmad-beldi-nsi", "C2", 1): {
        "scope": "bridge_n",
        "analysis_skill_id": "NSI1_ALGO_RECHERCHE_BRIDGE",
        "analysis_skill_label": "Algorithmes de recherche : séquentielle et dichotomique "
                                "(programme de Première NSI)",
        "rationale": "écriture d'une recherche séquentielle avec valeur sentinelle.",
    },
    ("ahmad-beldi-nsi", "C2", 2): {
        "scope": "bridge_n",
        "analysis_skill_id": "NSI1_ALGO_RECHERCHE_BRIDGE",
        "analysis_skill_label": "Algorithmes de recherche : séquentielle et dichotomique "
                                "(programme de Première NSI)",
        "rationale": "résultat de l'appel : lecture du contrat de l'algorithme écrit.",
    },
    ("ahmed-benhadj-salem", "C2", 1): {
        "scope": "bridge_n",
        "analysis_skill_id": "NSI1_ALGO_RECHERCHE_BRIDGE",
        "analysis_skill_label": "Algorithmes de recherche : séquentielle et dichotomique "
                                "(programme de Première NSI)",
        "rationale": "coût comparé de la recherche séquentielle et de la dichotomie.",
    },
    ("ahmed-benhadj-salem", "C2", 2): {
        "scope": "bridge_n",
        "analysis_skill_id": "NSI1_ALGO_RECHERCHE_BRIDGE",
        "analysis_skill_label": "Algorithmes de recherche : séquentielle et dichotomique "
                                "(programme de Première NSI)",
        "rationale": "énoncé d'un invariant de boucle : attendu de Première.",
    },
}


def key_for(student_id, level_key, item_kind, ref, rank):
    """Clé d'exception : niveau pour un item commun, élève pour un item individualisé."""
    scope_key = level_key if item_kind == "commun" else student_id
    return (scope_key, ref, rank)


def lookup(student_id, level_key, item_kind, ref, rank):
    return EXCEPTIONS.get(key_for(student_id, level_key, item_kind, ref, rank))
