# -*- coding: utf-8 -*-
"""Règles de correction équitable des questions déjà imprimées.

Le sujet n'est pas modifié. Ce module ne touche que le corrigé enseignant et le
barème interne : ce qui est accepté, ce qui ne peut pas être exigé, et ce que la
réussite ou la non-réussite autorise à conclure.

Ordre appliqué à toute question ambiguë (règle A) :

    1. retenir l'interprétation la plus favorable compatible avec la consigne
       réellement imprimée ;
    2. accepter toute méthode mathématiquement correcte ;
    3. n'exiger aucune justification que la consigne ne demande pas explicitement ;
    4. neutraliser le sous-critère si aucune correction équitable n'est possible ;
    5. marquer « evidence_quality »: « limited_by_prompt ».

Une ambiguïté de sujet est un défaut du sujet. Elle ne devient jamais une
faiblesse attribuée à l'élève.
"""

# Règle générale, applicable à tous les critères sans exception.
GENERAL_RULES = [
    "une méthode mathématiquement correcte n'est jamais un code d'erreur, même si une "
    "autre méthode aurait été plus rapide : le fait est consigné en observation de "
    "stratégie, avec accepted_alternative_method = true",
    "développer une équation-produit avant de la résoudre reste licite ; le code CONCEPT "
    "est interdit tant que le raisonnement de l'élève est valide",
    "un code d'erreur n'est porté que sur le ou les critères effectivement échoués ; il "
    "n'est jamais propagé aux autres critères du même item",
    "aucune justification non explicitement demandée par la consigne imprimée ne peut être "
    "exigée pour accorder les points",
]

# ---------------------------------------------------------------------------
# Cas documentés. Clé : (portée, ref, rang du critère) — même convention que
# scope_rules. Chaque entrée cite le libellé réellement imprimé.
# ---------------------------------------------------------------------------
CASES = {

    # --- Sinda CHIKHAOUI — 4e — C2 : justification de l'aire du triangle ---
    ("sinda-chikhaoui", "C2", 2): {
        "printed_prompt": "Expliquer pourquoi l'aire d'un triangle vaut la moitié du produit "
                          "de sa base par sa hauteur.",
        "accepted_methods": [
            "duplication du triangle par symétrie centrale autour du milieu d'un côté : les deux "
            "triangles congruents forment un parallélogramme de même base et de même hauteur, "
            "d'aire base x hauteur ; l'aire du triangle en est la moitié",
            "découpage-recollement aboutissant à un rectangle de même base et de même hauteur, "
            "à condition que la conservation des aires soit effectivement argumentée",
            "toute démonstration correcte reposant sur deux triangles congruents",
        ],
        "rejected_as_general_justification": [
            "« un triangle est la moitié d'un rectangle obtenu par duplication autour du milieu » "
            "employé comme justification générale : la duplication d'un triangle quelconque "
            "produit un parallélogramme, non un rectangle. L'argument n'est exact que pour un "
            "triangle rectangle et ne peut pas fonder le cas général.",
        ],
        "teacher_correction": "le corrigé enseignant et le barème interne retiennent le "
                              "parallélogramme construit à partir de deux triangles congruents. "
                              "La question posée à l'élève reste inchangée.",
        "grading_rule": "un élève qui produit la justification par le rectangle sans restriction "
                        "obtient les points s'il traite un triangle rectangle ou s'il argumente "
                        "correctement le découpage-recollement ; sinon le critère est crédité "
                        "partiellement et l'écart est consigné en observation, sans code CONCEPT "
                        "si le raisonnement reste cohérent.",
        "interpretation_limits": [
            "cet item ne suffit pas à conclure sur la compétence générale de démonstration "
            "géométrique",
        ],
    },

    # --- Elyes KEFI — 3e — B4 : contrôle capable de détecter une donnée oubliée ---
    ("elyes-kefi", "B4", 2): {
        "printed_prompt": "Indiquer un contrôle qui aurait détecté cet oubli.",
        "accepted_methods": [
            "recomptage de l'effectif : cinq valeurs annoncées, quatre utilisées",
            "recalcul de la somme et confrontation à la liste source",
            "confrontation terme à terme de la série employée et de la série donnée",
        ],
        "rejected_as_detection": [
            "l'encadrement de la moyenne entre la plus petite et la plus grande valeur : c'est un "
            "contrôle de vraisemblance parfaitement légitime, mais 11,25 appartient à "
            "l'intervalle [5 ; 15]. Dans ce cas précis, il ne détecte pas l'omission.",
        ],
        "grading_rule": "l'encadrement ne peut jamais être exigé comme preuve qu'une omission a "
                        "été détectée. Un élève qui le propose comme unique contrôle n'obtient "
                        "pas ce critère, mais aucun code d'erreur de méthode n'est porté : le "
                        "contrôle proposé est correct, il est seulement insuffisant ici.",
        "interpretation_limits": [
            "la distinction entre contrôle de vraisemblance et contrôle détecteur est fine ; la "
            "non-réussite ne documente pas une absence de pratique du contrôle",
        ],
    },
    ("elyes-kefi", "B4", 3): {
        "printed_prompt": "Expliquer pourquoi l'encadrement de la moyenne entre la plus petite "
                          "et la plus grande valeur ne l'aurait pas détecté.",
        "accepted_methods": [
            "toute formulation établissant que 11,25 reste compris entre 5 et 15, donc que "
            "l'encadrement est vérifié malgré l'erreur",
        ],
        "grading_rule": "la réponse attendue est une explication, pas un calcul ; toute "
                        "formulation correcte est créditée intégralement.",
    },

    # --- Ahmad BELDI — 1re spé — B4 : comparaison de x^3 et x^2 sur ]0 ; 1[ ---
    ("ahmad-beldi-maths", "B4", 1): {
        "printed_prompt": "Soit x un réel tel que 0 < x < 1. Comparer x^3 et x^2 : donner d'abord "
                          "un argument valable pour tout x de cet intervalle, puis illustrer par "
                          "un exemple numérique.",
        "proof_levels": {
            "niveau_demande": "comparaison correcte (x^3 < x^2) assortie d'un argument valable "
                              "pour tout x de l'intervalle. Tout argument général correct "
                              "convient : signe de x^2(x-1), multiplication de 0 < x < 1 par "
                              "x^2 > 0, ou comparaison des facteurs.",
            "preuve_renforcee": "rédaction formelle du signe de x^2(x-1) sur ]0 ; 1[. Elle est "
                                "valorisée qualitativement en observation, jamais exigée pour "
                                "accorder les points promis par la consigne imprimée.",
        },
        "grading_rule": "la consigne imprimée demande « un argument valable pour tout x », non "
                        "une démonstration formelle. Aucun élève n'est pénalisé pour l'absence "
                        "d'un formalisme que la consigne ne réclame pas. L'exemple numérique est "
                        "rétribué par son propre critère et ne peut pas tenir lieu d'argument "
                        "général.",
        "interpretation_limits": [
            "cet item, seul, ne prouve pas une compétence de démonstration universelle : il "
            "porte sur un intervalle donné et sur deux puissances voisines",
        ],
    },
    ("ahmad-beldi-maths", "B4", 2): {
        "printed_prompt": "…puis illustrer par un exemple numérique.",
        "grading_rule": "tout exemple numérique cohérent appartenant à ]0 ; 1[ est crédité. Sa "
                        "présentation comme illustration et non comme preuve est attendue mais "
                        "n'est pas une condition d'attribution des points.",
    },
    # Le même couple de critères existe sur l'item commun B2 des trois élèves de 1re spé.
    ("1ere_spe", "B2", 2): {
        "printed_prompt": "Soit x un réel tel que 0 < x < 1. Comparer x^2 et x, puis justifier la "
                          "réponse par un exemple numérique et par un argument valable pour tout "
                          "x de cet intervalle.",
        "proof_levels": {
            "niveau_demande": "comparaison correcte (x^2 < x) et argument valable pour tout x : "
                              "signe de x(x-1), ou multiplication de 0 < x < 1 par x > 0.",
            "preuve_renforcee": "rédaction formelle du tableau de signes de x(x-1). Valorisée, "
                                "jamais exigée.",
        },
        "grading_rule": "aucun formalisme non demandé par la consigne imprimée ne conditionne "
                        "l'attribution des points.",
        "interpretation_limits": [
            "cet item, seul, ne prouve pas une compétence de démonstration universelle",
        ],
    },

    # --- Malek KHADHRANI — 1re spé — C2 : réfutation de la croissance de 1/x ---
    ("malek-khadhrani", "C2", 2): {
        "printed_prompt": "L'affirmation « la fonction inverse f(x) = 1/x est croissante sur "
                          "]0 ; +infini[ » est-elle exacte ? Répondre par oui ou non, en "
                          "justifiant à l'aide de deux valeurs bien choisies.",
        "accepted_methods": [
            "un contre-exemple explicite : 1 < 2 et f(1) = 1 > f(2) = 0,5 ; la totalité des "
            "points du critère est acquise",
            "tout autre couple de valeurs correctement choisi et correctement comparé",
        ],
        "grading_rule": "un contre-exemple suffit à réfuter une affirmation universelle. La "
                        "consigne imprimée demande deux valeurs bien choisies : rien de plus ne "
                        "peut être exigé. L'ajout spontané « donc la fonction est décroissante » "
                        "n'est pas pénalisé, et la décroissance sur tout l'intervalle n'est pas "
                        "à démontrer.",
        "interpretation_limits": [
            "cette question ne permet pas de conclure que l'élève sait établir la monotonie "
            "d'une fonction sur un intervalle : elle mesure l'usage d'un contre-exemple",
        ],
    },
}

# ---------------------------------------------------------------------------
# Observations enseignantes explicitement NON scorées : présentes dans le corrigé
# mais absentes de la question imprimée et du barème. Elles ne peuvent influencer
# ni le score, ni le profil d'erreurs, ni les priorités, ni le bilan.
# ---------------------------------------------------------------------------
NON_SCORED_OBSERVATIONS = {
    ("ahmad-beldi-nsi", "B2"): [
        {
            "observation": "le corrigé mentionne que moyenne([]) provoque une division par zéro.",
            "raison": "la question imprimée ne demande ni le cas de la liste vide ni son "
                      "traitement, et aucun critère du barème ne le rétribue.",
            "consequence": "cette remarque peut être dite oralement à l'élève ; elle ne produit "
                           "aucun code d'erreur scoré et n'entre dans aucun décompte.",
        },
    ],
    ("ahmed-benhadj-salem", "B2"): [
        {
            "observation": "le corrigé mentionne que moyenne([]) provoque une division par zéro.",
            "raison": "la question imprimée ne demande ni le cas de la liste vide ni son "
                      "traitement, et aucun critère du barème ne le rétribue.",
            "consequence": "remarque orale seulement, hors score et hors profil d'erreurs.",
        },
    ],
}


def case_for(student_id, level_key, item_kind, ref, rank):
    key = (level_key if item_kind == "commun" else student_id, ref, rank)
    return CASES.get(key)


def non_scored_for(student_id, ref):
    return NON_SCORED_OBSERVATIONS.get((student_id, ref), [])
