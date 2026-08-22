# -*- coding: utf-8 -*-
"""Hiérarchie des niveaux de preuve, et vocabulaire de trajectoire.

Le défaut que cette couche existe pour empêcher est le glissement silencieux de

    « la notion figure dans le livret de la séance 2 »

vers

    « la notion est acquise ».

Ce sont deux affirmations de nature différente, appuyées sur des preuves de forces
très inégales. Chaque fait porte donc explicitement son niveau, et les règles de
rédaction refusent de transformer un niveau faible en affirmation forte.
"""

# --------------------------------------------------------------- niveaux de preuve
#
# A  preuve directe forte      un critère de l'évaluation de clôture a été noté sur
#                              une copie réelle, et l'item est rattaché à la compétence.
# B  preuve directe pédagogique une observation écrite de l'enseignant, ou une
#                              production de séance documentée.
# C  preuve de parcours        la compétence a été ciblée : elle figure au programme
#                              d'une séance ou d'une remédiation prescrite. Cela
#                              établit le travail proposé, pas la réussite.
# D  inférence                 aucune preuve directe suffisante ; déduction plausible.
LEVELS = ("A", "B", "C", "D")

LEVEL_LABELS = {
    "A": "critère évalué sur la copie de clôture",
    "B": "observation écrite de l'enseignant",
    "C": "compétence ciblée pendant le stage",
    "D": "inférence, sans preuve directe",
}

# Ce qu'un niveau autorise à écrire dans un document destiné aux familles.
LEVEL_MAY_ASSERT_MASTERY = {"A": True, "B": False, "C": False, "D": False}

_ORDER = {level: rank for rank, level in enumerate(LEVELS)}


def strongest(levels) -> str:
    """Retourne le niveau le plus fort d'un ensemble ; « D » si l'ensemble est vide."""
    retenus = [lv for lv in levels if lv in _ORDER]
    if not retenus:
        return "D"
    return min(retenus, key=lambda lv: _ORDER[lv])


def may_assert_mastery(level: str) -> bool:
    """Seule une preuve directe forte autorise une affirmation de maîtrise."""
    return LEVEL_MAY_ASSERT_MASTERY.get(level, False)


# ------------------------------------------------------- statuts de trajectoire N−1
#
# Vocabulaire qualitatif. Aucun de ces statuts n'est une mesure : ils décrivent la
# relation entre un point de départ documenté et ce que l'évaluation finale établit.
TRAJECTORY_STATUSES = (
    "FRAGILITE_INITIALE_CONFIRMEE",
    "FRAGILITE_INITIALE_EN_VOIE_DE_RESOLUTION",
    "CONSOLIDATION_OBSERVEE",
    "ACQUIS_ACTUELLEMENT_DISPONIBLE",
    "REUSSITE_A_CONFIRMER",
    "FRAGILITE_PERSISTANTE",
    "PREUVE_FINALE_INSUFFISANTE",
    "BRIDGE_FIRST_EXPOSURE",
    "BRIDGE_PROMISING",
)

TRAJECTORY_LABELS = {
    "FRAGILITE_INITIALE_CONFIRMEE":
        "la fragilité signalée au diagnostic se retrouve dans l'évaluation de clôture",
    "FRAGILITE_INITIALE_EN_VOIE_DE_RESOLUTION":
        "le point signalé au diagnostic présente des indicateurs positifs, encore partiels",
    "CONSOLIDATION_OBSERVEE":
        "plusieurs indicateurs positifs concordants sur un point signalé au diagnostic",
    "ACQUIS_ACTUELLEMENT_DISPONIBLE":
        "l'appui constaté au diagnostic est de nouveau disponible en fin de stage",
    "REUSSITE_A_CONFIRMER":
        "réussite obtenue juste après un travail sur la notion, à revérifier à distance",
    "FRAGILITE_PERSISTANTE":
        "la difficulté reste installée malgré le travail conduit",
    "PREUVE_FINALE_INSUFFISANTE":
        "l'évaluation n'apporte pas assez d'éléments pour conclure",
    "BRIDGE_FIRST_EXPOSURE":
        "première rencontre avec une notion de l'année à venir",
    "BRIDGE_PROMISING":
        "première aisance encourageante sur une notion de l'année à venir",
}

# Lecture grossière, exigée par les tests de trajectoire : elle répond à la seule
# question « le dossier va-t-il globalement dans le bon sens ? », sans chiffrer quoi
# que ce soit.
QUALITATIVE_TRAJECTORIES = ("positive_evidence", "mixed_evidence",
                            "persistent_difficulty", "no_final_evidence")

_TRAJECTORY_TO_QUALITATIVE = {
    "CONSOLIDATION_OBSERVEE": "positive_evidence",
    "FRAGILITE_INITIALE_EN_VOIE_DE_RESOLUTION": "positive_evidence",
    "ACQUIS_ACTUELLEMENT_DISPONIBLE": "positive_evidence",
    "BRIDGE_PROMISING": "positive_evidence",
    "REUSSITE_A_CONFIRMER": "mixed_evidence",
    "BRIDGE_FIRST_EXPOSURE": "mixed_evidence",
    "FRAGILITE_INITIALE_CONFIRMEE": "persistent_difficulty",
    "FRAGILITE_PERSISTANTE": "persistent_difficulty",
    "PREUVE_FINALE_INSUFFISANTE": "no_final_evidence",
}


def qualitative_of(trajectory_status: str) -> str:
    return _TRAJECTORY_TO_QUALITATIVE.get(trajectory_status, "no_final_evidence")


# ------------------------------------------------------------------- couverture
#
# La couverture décrit le TRAVAIL FOURNI pendant le stage. Elle ne dit rien de la
# réussite. Les deux sont affichées côte à côte, jamais fusionnées, précisément pour
# empêcher la lecture « beaucoup travaillé, donc acquis ».
COVERAGE_LEVELS = ("NONE", "LIGHT", "MODERATE", "STRONG")

COVERAGE_LABELS = {
    "NONE": "non travaillée pendant le stage",
    "LIGHT": "abordée",
    "MODERATE": "travaillée",
    "STRONG": "travaillée à plusieurs reprises",
}


def coverage_of(sessions, targeted_in_s5=False, remediation=False) -> str:
    """Couverture d'une compétence pendant le stage.

    Trois signaux, tous issus de documents et non d'observations : le nombre de
    séances où la compétence figure au programme, sa reprise dans la séance de
    clôture, et l'existence d'exercices de remédiation nominatifs.
    """
    poids = len(sessions or [])
    if targeted_in_s5:
        poids += 1
    if remediation:
        poids += 1
    if poids <= 0:
        return "NONE"
    if poids == 1:
        return "LIGHT"
    if poids == 2:
        return "MODERATE"
    return "STRONG"
