# -*- coding: utf-8 -*-
"""Constantes partagées par tous les niveaux de la séance S5 de clôture.

Ce module ne contient aucune donnée nominative : uniquement l'architecture
commune imposée par le cahier des charges (75 min de travail + 45 min
d'évaluation, double lecture note/compétences, échelle de certitude).
"""

# --- architecture temporelle -------------------------------------------------
WORK_MINUTES = 75
EXAM_MINUTES = 45

PHASE_PLAN = [
    # (n, titre, minutes, minutes "objectifs communs du niveau", minutes individualisées)
    (1, "Réactivation et mise en route", 10, 10, 0),
    (2, "Consolidation ciblée — priorité 1", 25, 13, 12),
    (3, "Consolidation ciblée — priorité 2", 20, 10, 10),
    (4, "Réinvestissement et pont vers l'année suivante", 15, 13, 2),
    (5, "Préparation méthodologique à l'évaluation", 5, 5, 0),
]

# --- barème et blueprint de l'évaluation ------------------------------------
# 70 % de noyau commun (14 pts) / 30 % individualisé (6 pts) — cf. §8 et §25.
EXAM_TOTAL_POINTS = 20
EXAM_PARTS = [
    {"part": "A", "titre": "Automatismes et connaissances essentielles",
     "minutes": 10, "points": 6,
     "commun": ["A1", "A2", "A3", "A4"], "individuel": ["A5", "A6"]},
    {"part": "B", "titre": "Application et raisonnement",
     "minutes": 20, "points": 8,
     "commun": ["B1", "B2", "B3"], "individuel": ["B4"]},
    {"part": "C", "titre": "Transfert et synthèse",
     "minutes": 15, "points": 6,
     "commun": ["C1"], "individuel": ["C2"]},
]
EXAM_ITEM_ORDER = ["A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B3", "B4", "C1", "C2"]

# Aucune durée cible n'est imposée. La durée de chaque item est estimée à partir de
# son contenu réel par data/timing.py, et la somme est une mesure, non une consigne.
# Seuils de recevabilité appliqués par l'audit docimologique :
EXAM_MIN_MARGIN_MINUTES = 3      # marge minimale exigée sur les 45 minutes
EXAM_MAX_ESTIMATED_MINUTES = 42  # au-delà, le contenu doit être allégé

# --- échelles ----------------------------------------------------------------
# Échelle de certitude : identique au diagnostic initial (Test de positionnement,
# 18 items, certitude 1 à 4). Elle est donc directement comparable.
CONFIDENCE_SCALE = {
    "1": "Je devine.",
    "2": "Je ne suis pas sûr.",
    "3": "Je pense avoir juste.",
    "4": "J'en suis certain : je saurais expliquer pourquoi.",
}

MASTERY_SCALE = {
    "0": "non maîtrisé",
    "1": "très fragile",
    "2": "partiellement maîtrisé",
    "3": "maîtrisé",
    "4": "maîtrise solide / transfert réussi",
}

# Statut d'une compétence AVANT la passation de l'évaluation finale.
PRE_STATUS = ["acquis", "en_voie_acquisition", "fragile", "non_evalue", "non_travaille"]

ERROR_CODES = {
    "CONCEPT": "La notion elle-même n'est pas disponible ou est remplacée par une règle fausse.",
    "METHODE": "La méthode choisie ne convient pas à la tâche demandée.",
    "CALCUL": "La méthode est correcte, l'exécution numérique ne l'est pas.",
    "LECTURE": "Une donnée de l'énoncé est mal lue, oubliée ou ajoutée.",
    "NOTATION": "Écriture, unité ou symbole incorrect alors que le raisonnement tient.",
    "JUSTIFICATION": "Le résultat est exact mais la propriété ou la relation n'est pas nommée.",
    "CONTROLE": "Aucun contrôle de vraisemblance n'est effectué alors qu'il était demandé.",
    "ALGORITHME": "L'enchaînement des instructions ne produit pas l'effet attendu.",
    "SYNTAXE": "Erreur d'écriture du langage, sans erreur de raisonnement.",
    "TRANSFERT": "Les acquis existent mais ne sont pas mobilisés dans un contexte nouveau.",
    "ETOURDERIE": "Écart isolé, non reproduit sur les items voisins de même compétence.",
}

PRIORITY_CODES = {
    "P1": "indispensable à travailler immédiatement",
    "P2": "important à consolider dans les deux premières semaines",
    "P3": "à stabiliser progressivement",
    "OK": "suffisamment solide à ce stade",
}

COMPARABILITY = [
    "comparable",          # un item de référence existe dans le diagnostic initial
    "partiellement_comparable",
    "non_comparable_contenu_nouveau",
    "non_comparable_absence_baseline",
]

# --- textes communs ----------------------------------------------------------
PHASE5_TEX = r"""
\begin{methodbox}
\textbf{Cinq règles, et rien d'autre.} Ce cadrage ne porte sur aucun contenu de l'évaluation.
\begin{enumerate}
\item \textbf{Gérer le temps.} Trois parties : environ 10 min, 20 min et 15 min. Un regard sur l'horloge à la fin de chaque partie suffit.
\item \textbf{Justifier.} Écrire la relation, la propriété ou la règle avant le calcul. Un résultat seul ne montre pas ce que tu sais.
\item \textbf{Contrôler.} Avant de passer à la suite : ordre de grandeur, substitution, unité, ou vérification par une seconde voie.
\item \textbf{Lire jusqu'au bout.} Souligner la question réellement posée et les données effectivement fournies.
\item \textbf{Passer et revenir.} Une question laissée de côté puis reprise vaut mieux qu'une réponse écrite au hasard.
\end{enumerate}
\end{methodbox}

\begin{graybox}
\textbf{La certitude.} Elle est demandée à trois moments seulement, comme au test de positionnement de début de stage :
\conf\ . Elle n'entre pas dans la note. Elle sert à distinguer ce que tu sais de ce que tu crois savoir.
\end{graybox}

\subsectiontitle{Mon engagement d'avant-évaluation}
\par\vspace{1mm}
\noindent\textbf{Le contrôle que j'écrirai systématiquement :}\ \rule{\dimexpr\linewidth-76mm\relax}{0.32pt}
\par\vspace{3mm}
\noindent\textbf{La question que je traiterai en dernier :}\ \rule{\dimexpr\linewidth-68mm\relax}{0.32pt}
\par\vspace{1mm}
"""

EXAM_INSTRUCTIONS_TEX = r"""
\begin{goalbox}
\textbf{Ce document est un diagnostic de sortie, pas un classement.} Il mesure ce qui est
désormais installé, ce qui reste fragile, et il sert à écrire le plan des quatre premières
semaines de la rentrée.
\end{goalbox}

\begin{methodbox}
\textbf{Consignes}
\begin{itemize}
\item Durée : \textbf{45 minutes}. Partie A : environ 10 min. Partie B : environ 20 min. Partie C : environ 15 min.
\item Travailler seul, sans document et sans les cartes de rappel de la séance.
\item Écrire la relation ou la propriété utilisée avant le calcul.
\item Une question peut être laissée de côté puis reprise ; il vaut mieux la laisser vide que d'écrire au hasard.
\item Trois lignes « Certitude » seulement : \conf\ , sur la même échelle qu'en début de stage.
\end{itemize}
\end{methodbox}
"""
