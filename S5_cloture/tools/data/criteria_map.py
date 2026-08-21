# -*- coding: utf-8 -*-
"""Barème au niveau du critère : chaque critère porte une compétence et un type de preuve.

Motif du changement : répartir également les points d'un item entre toutes ses
compétences peut créditer une compétence qui n'a pas été réussie. Un item de deux
points dont une sous-question relève de l'aire et l'autre de la proportionnalité
doit pouvoir attribuer un point à l'une et zéro à l'autre.

Règle appliquée : **un critère évalue exactement une compétence**. Lorsqu'un critère
en couvrait deux, il a été scindé. Les compétences déclarées d'un item sont, depuis
cette correction, exactement l'ensemble des compétences de ses critères ; c'est
vérifié par `validate_s5.py`.

Ce module contient la table explicite des items qui mobilisent plusieurs compétences.
Pour les items mono-compétence, la compétence du critère est celle de l'item — ce
n'est pas une supposition, c'est une identité.

Vocabulaire des types de preuve :
    automatisme    restitution ou calcul immédiat, sans choix de méthode
    procedure      choix et exécution corrects d'une méthode
    justification  propriété nommée, argument produit, contre-exemple
    controle       vérification explicitement demandée et effectivement conduite
    transfert      mobilisation dans une situation non standard
    communication  formulation exacte destinée à être lue par un tiers
"""

EVIDENCE_TYPES = ("automatisme", "procedure", "justification", "controle",
                  "transfert", "communication")

# Clé : (level_key, ref) pour un item du noyau commun, (student_id, ref) pour un
# item individualisé. Valeur : liste de critères (points, skill, evidence, subpart, desc).
CRITERIA = {
    # ------------------------------------------------------------------ 4e
    ("4e", "B1"): [
        (1.0, "M4E_AIRE_01", "procedure", "1", "aire et périmètre exacts, avec les unités correctes"),
        (1.0, "M4E_PROP_01", "procedure", "2", "prix exact, obtenu à partir de l'aire et non du périmètre"),
    ],
    ("4e", "B2"): [
        (0.5, "M4E_LIT_01", "procedure", "1", "développement $5(x-3)=5x-15$ exact"),
        (0.5, "M4E_LIT_02", "procedure", "2", "réduction en $7x-8$ exacte"),
        (1.0, "M4E_LIT_02", "controle", "3", "contrôle mené sur les deux écritures pour $x=2$, aboutissant à la même valeur"),
    ],
    ("4e", "B3"): [
        (1.0, "M4E_PROP_02", "procedure", "1", "fréquence exacte en pourcentage"),
        (0.7, "M4E_STAT_01", "procedure", "2", "moyenne exacte, somme et effectif visibles"),
        (0.3, "M4E_STAT_01", "controle", "2", "encadrement entre la plus petite et la plus grande valeur écrit"),
    ],
    ("4e", "C1"): [
        (1.0, "M4E_AIRE_01", "transfert", "1", "aire à peindre exacte, soustraction de la fenêtre visible"),
        (0.5, "M4E_FRAC_02", "procedure", "2", "aire de la sous-couche exacte, le tiers étant correctement pris"),
        (1.5, "M4E_LIT_01", "transfert", "3", "expression $C(n)=19n+25$ correcte, substitution écrite et $C(6)$ exact"),
        (1.0, "M4E_LIT_01", "transfert", "4", "décision justifiée par la comparaison de $C(10)$ au budget de 200 TND"),
    ],
    ("fares-darghouth", "B4"): [
        (1.0, "M4E_GEO_01", "justification", "1", "angle exact et rédaction en donnée-propriété-conclusion"),
        (1.0, "M4E_GEO_02", "justification", "2", "famille correcte et contre-exemple explicite"),
    ],
    ("fares-darghouth", "C2"): [
        (0.5, "M4E_LIT_01", "automatisme", "1", "substitution $3\\times 5+7=22$ exacte"),
        (0.5, "M4E_LIT_01", "procedure", "2", "développement $4(x+6)=4x+24$ exact"),
        (1.0, "M4E_LIT_02", "procedure", "3", "réduction en $6x+24$ exacte"),
    ],
    ("ines-kefi", "B4"): [
        (1.0, "M4E_GEO_02", "justification", "1", "raisonnement complet en donnée-propriété-conclusion"),
        (1.0, "M4E_GEO_02", "justification", "2", "réponse négative appuyée sur un contre-exemple explicite"),
    ],
    ("ines-kefi", "C2"): [
        (1.0, "M4E_REL_02", "procedure", "1", "abscisse finale exacte, les deux déplacements visibles"),
        (1.0, "M4E_REL_01", "justification", "2", "produit exact et signe justifié"),
    ],
    ("sinda-chikhaoui", "B4"): [
        (0.5, "M4E_LIT_01", "procedure", "1", "développement $6(x-2)=6x-12$ exact"),
        (0.5, "M4E_LIT_02", "procedure", "2", "réduction en $9x-7$ exacte"),
        (1.0, "M4E_LIT_02", "controle", "3", "contrôle pour $x=0$ mené sur les deux écritures"),
    ],
    # ------------------------------------------------------------------ 3e
    ("3e", "B3"): [
        (1.0, "M3E_PROP_01", "procedure", "1", "vitesse exacte, conversion de 1 h 30 en 1,5 h visible"),
        (0.7, "M3E_STAT_01", "procedure", "2", "moyenne pondérée exacte, somme des coefficients correcte"),
        (0.3, "M3E_STAT_01", "controle", "2", "encadrement entre 9 et 14 écrit"),
    ],
    ("3e", "C1"): [
        (1.0, "M3E_GEO_01", "transfert", "1", "longueur exacte, théorème cité"),
        (1.0, "M3E_TRIG_01", "transfert", "2", "angle exact au degré près, rapport correctement choisi"),
        (1.0, "M3E_PROP_01", "transfert", "3", "pente exprimée en pourcentage et conclusion explicite"),
        (1.0, "M3E_LIT_01", "transfert", "4", "$C(5)$ exact et rôle du terme constant correctement expliqué"),
    ],
    ("sarah-bargaoui", "B4"): [
        (1.0, "M3E_PROP_01", "procedure", "1", "nombre de pages exact, relation écrite avant les nombres"),
        (1.0, "M3E_GEO_01", "procedure", "2", "$AB = 7$ cm, relation de Pythagore écrite"),
    ],
    ("sarah-bargaoui", "C2"): [
        (0.5, "M3E_LIT_01", "procedure", "1", "développement $5(2x-3)=10x-15$ exact"),
        (0.5, "M3E_LIT_02", "procedure", "1", "réduction en $14x-4$ exacte"),
        (1.0, "M3E_LIT_02", "controle", "2", "contrôle pour $x=1$ mené sur les deux écritures"),
    ],
    ("selim-mansouri", "B4"): [
        (1.0, "M3E_PROP_01", "procedure", "1", "prix exact, prix unitaire explicité"),
        (1.0, "M3E_GEO_01", "procedure", "2", "$BC = 20$ cm avec la relation écrite"),
    ],
    # ---------------------------------------------------------------- 2nde
    ("2nde", "B1"): [
        (0.75, "M2DE_EQ_01", "procedure", "1", "$x=5$ et vérification écrite"),
        (0.75, "M2DE_EQ_02", "procedure", "2", "les deux solutions exactes et propriété nommée, quelle que soit la méthode"),
        (0.5, "M2DE_EQ_02", "controle", "3", "vérification de la solution entière conduite jusqu'au produit nul"),
    ],
    ("2nde", "B3"): [
        (0.75, "M2DE_GEO_01", "procedure", "1", "$BC=15$ cm avec la relation écrite"),
        (0.75, "M2DE_GEO_02", "procedure", "2", "$AN$ et $MN$ exacts, théorème de Thalès cité"),
        (0.5, "M2DE_GEO_02", "procedure", "3", "périmètre exact, avec l'unité"),
    ],
    ("2nde", "C1"): [
        (1.0, "M2DE_ALG_01", "transfert", "1", "expression développée et réduite exacte"),
        (0.5, "M2DE_ALG_01", "controle", "2", "$A(4)$ exact et vérifié par les deux voies"),
        (1.0, "M2DE_GEO_01", "transfert", "3", "diagonale exacte, théorème cité"),
        (1.5, "M2DE_POURC_01", "transfert", "4", "prix final exact, coefficient global et conclusion argumentée"),
    ],
    ("noa-maniaci", "C2"): [
        (0.5, "M2DE_ALG_01", "procedure", "1", "factorisation $x(x-7)$ exacte"),
        (0.5, "M2DE_EQ_02", "procedure", "2", "les deux solutions exactes"),
        (1.0, "M2DE_EQ_02", "controle", "3", "vérification des deux solutions"),
    ],
    # ------------------------------------------------------------ 1ere_spe
    ("1ere_spe", "B2"): [
        (1.0, "M1RE_FONC_02", "communication", "1", "vocabulaire correct dans les deux sens : image et antécédent"),
        (0.6, "M1RE_FREF_02", "justification", "2", "argument valable pour tout $x$ de l'intervalle"),
        (0.4, "M1RE_FREF_02", "procedure", "2", "exemple numérique cohérent"),
    ],
    ("1ere_spe", "B3"): [
        (1.0, "M1RE_POURC_02", "procedure", "1", "les deux prix exacts"),
        (1.0, "M1RE_POURC_01", "procedure", "2", "coefficient global et taux global exacts"),
    ],
    ("ahmad-beldi-maths", "B4"): [
        (0.75, "M1RE_FREF_02", "justification", "1", "argument valable pour tout $x$ de l'intervalle : signe de $x^2(x-1)$, ou tout raisonnement général équivalent"),
        (0.25, "M1RE_FREF_02", "procedure", "1", "exemple numérique cohérent, présenté comme une illustration et non comme une preuve"),
        (1.0, "M1RE_PROBA_01", "procedure", "2", "$P(A\\cup B)$ exacte, formule visible"),
    ],
    ("1ere_spe", "C1"): [
        (1.0, "M1RE_DROIT_01", "transfert", "1", "coefficient directeur et équation réduite exacts"),
        (1.0, "M1RE_VECT_02", "justification", "2", "appartenance justifiée par un calcul explicite"),
        (1.0, "M1RE_PROBA_01", "transfert", "3", "les deux probabilités exactes, intersection correctement retirée"),
        (1.0, "M1RE_POURC_02", "transfert", "4", "relation de récurrence correcte et $u_2$ exact"),
    ],
    ("donia-khadhrani", "B4"): [
        (1.0, "M1RE_DROIT_01", "procedure", "1", "coefficient directeur exact"),
        (0.6, "M1RE_DROIT_01", "procedure", "2", "équation réduite exacte"),
        (0.4, "M1RE_DROIT_02", "justification", "3", "parallélisme justifié par l'égalité des coefficients directeurs"),
    ],
    ("donia-khadhrani", "C2"): [
        (1.0, "M1RE_PROBA_01", "procedure", "1", "$P(A\\cup B)$ exacte, formule visible"),
        (1.0, "M1RE_PROBA_02", "procedure", "2", "probabilité de l'événement contraire exacte"),
    ],
    ("malek-khadhrani", "B4"): [
        (0.7, "M1RE_VECT_01", "automatisme", "1", "les deux vecteurs exacts"),
        (0.7, "M1RE_VECT_02", "justification", "2", "alignement justifié par le calcul du déterminant"),
        (0.6, "M1RE_DROIT_01", "procedure", "3", "coefficient directeur de $(AB)$ exact"),
    ],
    ("malek-khadhrani", "C2"): [
        (1.0, "M1RE_NUM_01", "automatisme", "1", "puissance exacte"),
        (1.0, "M1RE_FREF_01", "justification", "2", "affirmation réfutée par un contre-exemple explicite $f(1)>f(2)$ avec $1<2$ ; l'ajout « donc décroissante » n'est pas pénalisé, mais la décroissance globale n'est pas exigée"),
    ],
    # ------------------------------------------------------------- 1re_nsi
    ("1re_nsi", "B3"): [
        (0.75, "NSI1_CSV_01", "procedure", "1", "colonnes et types de conversion exacts"),
        (0.5, "NSI1_CSV_01", "justification", "2", "concaténation correctement expliquée par le type des opérandes"),
        (0.75, "NSI1_TAB_01", "communication", "3", "métadonnée pertinente et distinction avec une donnée du tableau"),
    ],
    ("ahmad-beldi-nsi", "B4"): [
        (1.0, "NSI1_LIST_01", "automatisme", "1", "les trois valeurs exactes, dont le dernier indice valide"),
        (1.0, "NSI1_MUT_01", "justification", "2", "contenu de \\code{L} exact et alias correctement expliqué"),
    ],
    ("1re_nsi", "C1"): [
        (1.5, "NSI1_ALGO_01", "transfert", "1", "les deux trous complétés correctement"),
        (0.75, "NSI1_ALGO_01", "procedure", "2", "les deux résultats exacts, dont la valeur d'absence"),
        (0.75, "NSI1_TEST_01", "transfert", "2", "test sur liste vide, avec son résultat attendu"),
        (1.0, "NSI1_ALGO_01", "communication", "3", "gain et précondition de la dichotomie correctement énoncés"),
    ],
}

# Règle de classement des critères des items mono-compétence, appliquée dans l'ordre.
# Chaque motif est explicite ; aucun classement par défaut silencieux n'est autorisé.
EVIDENCE_RULES = [
    ("controle", ("contrôle", "vérification", "vérifié", "encadrement", "vérifier")),
    ("justification", ("justifi", "cité", "citée", "nommée", "expliqu", "argument",
                       "contre-exemple", "réfut", "propriété", "raisonnement", "démarche")),
    ("communication", ("phrase", "rédaction", "rédigé", "conclusion", "formulation",
                       "vocabulaire", "énoncé")),
    ("transfert", ("décision", "transfert", "situation")),
    ("procedure", ("relation", "méthode", "étape", "substitution", "développement",
                   "factorisation", "tableau", "intervalle", "conversion", "unité",
                   "somme", "effectif", "solutions", "test", "assertion", "trous",
                   "complet", "complète", "complétés", "état", "type", "types")),
    ("automatisme", ("exact", "exacte", "exacts", "exactes", "réponses", "valeurs",
                     "résultat", "coordonnées")),
]


# Critères que la règle par mots-clés ne classe pas : attribution explicite.
EVIDENCE_OVERRIDES = {
    "$\\frac{3}{8}$ ou une écriture équivalente correcte": "automatisme",
    "$\\frac{4}{12}$ ou $\\frac13$": "automatisme",
    "les cinq nombres dans le bon ordre": "automatisme",
    "$x=4$ avec l'équation écrite": "procedure",
    "côtés correctement nommés et rapport correct": "procedure",
    "rapport nommé et défini correctement": "procedure",
    "sinus identifié à la question 3": "procedure",
    "exemple numérique cohérent, présenté comme une illustration et non comme une preuve": "procedure",
    "\\code{None} et explication correcte": "justification",
    "explication correcte de la différence de procédure": "justification",
    ("explication géométrique correcte : duplication en parallélogramme de même base et même "
     "hauteur. Une explication par découpage-recollement aboutissant à un rectangle de même base "
     "et même hauteur est également acceptée si elle est correctement conduite"): "justification",
}


def evidence_for(desc):
    """Type de preuve d'un critère. Ne renvoie jamais de valeur par défaut."""
    if desc in EVIDENCE_OVERRIDES:
        return EVIDENCE_OVERRIDES[desc]
    low = desc.lower()
    for kind, keys in EVIDENCE_RULES:
        if any(k in low for k in keys):
            return kind
    raise ValueError("aucun type de preuve ne correspond au critère : %r" % desc)
