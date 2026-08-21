# -*- coding: utf-8 -*-
"""Estimation de la durée d'un item à partir de son contenu réel.

Aucune durée cible n'est imposée : la durée d'un item est calculée à partir de ce
que l'item demande effectivement. Le total d'une épreuve est donc une *mesure*,
pas une contrainte. Si ce total dépasse la durée de l'épreuve, c'est le contenu
qui doit être allégé, jamais l'estimation.

Modèle en trois postes, appliqué à chaque item :

    lecture     = caractères de l'énoncé / vitesse de lecture du niveau
                  + lignes de code à lire × temps de lecture d'une ligne de code
    traitement  = nombre de sous-questions × temps de traitement d'une
                  sous-question, selon le type de tâche et la difficulté
    rédaction   = nombre de lignes effectivement écrites × temps par ligne

Les lignes effectivement écrites sont plafonnées : l'espace de réponse est
volontairement généreux dans les livrets, et un élève n'écrit pas nécessairement
sur toutes les lignes offertes.

Toutes les constantes sont déclarées ici et justifiées. Elles n'ont pas été
ajustées pour atteindre un total : elles proviennent d'ordres de grandeur usuels
de lecture et de rédaction manuscrite, différenciés par niveau.
"""

import re

# Caractères d'énoncé lus par minute. Un énoncé mathématique se lit nettement plus
# lentement qu'un texte courant (symboles, fractions, retours en arrière).
READ_RATE = {"4e": 550, "3e": 650, "2nde": 750, "1ere_spe": 800, "1re_nsi": 700}

# Minutes de lecture par ligne de code ou de données à interpréter.
CODE_LINE_READ = 0.12

# Minutes de traitement par sous-question, selon (type de tâche, difficulté).
THINK = {
    ("automatisme", "socle"): 0.60,
    ("automatisme", "standard"): 0.80,
    ("application", "standard"): 1.15,
    ("application", "transfert"): 1.35,
    ("transfert", "standard"): 1.25,
    ("transfert", "transfert"): 1.45,
}

# Minutes par ligne manuscrite effectivement rédigée.
WRITE_LINE = {"4e": 0.42, "3e": 0.38, "2nde": 0.35, "1ere_spe": 0.33, "1re_nsi": 0.38}

# Plafond de lignes réellement écrites : une ligne d'amorce, puis environ une
# ligne et quart par sous-question.
def _effective_lines(offered, n_sub):
    return min(offered, 1.0 + 1.25 * n_sub)


def _plain(tex):
    """Énoncé débarrassé du balisage LaTeX, pour compter la charge de lecture."""
    t = re.sub(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", " ", tex, flags=re.S)
    t = re.sub(r"\\begin\{[^}]*\}(\[[^\]]*\])?|\\end\{[^}]*\}", " ", t)
    t = re.sub(r"\\rule\{[^}]*\}\{[^}]*\}", " ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    t = re.sub(r"[{}$&%#_^~\\]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def _code_lines(tex):
    n = 0
    for block in re.findall(r"\\begin\{lstlisting\}(?:\[[^\]]*\])?(.*?)\\end\{lstlisting\}", tex, flags=re.S):
        n += len([l for l in block.splitlines() if l.strip()])
    return n


def _sub_questions(tex):
    n = len(re.findall(r"\\item\b", tex))
    return max(1, n)


def _offered_lines(space):
    if not space or space == "short":
        return 1
    if space.startswith("lines:"):
        return int(space.split(":")[1])
    return 1


def estimate(item, level_key):
    """Retourne la durée estimée et sa décomposition, en minutes."""
    tex = item["tex"]
    chars = len(_plain(tex))
    code = _code_lines(tex)
    n_sub = _sub_questions(tex)
    offered = _offered_lines(item.get("space"))
    eff = _effective_lines(offered, n_sub)

    lecture = chars / READ_RATE[level_key] + code * CODE_LINE_READ
    key = (item["task"], item["difficulty"])
    if key not in THINK:
        raise KeyError("couple (tâche, difficulté) non prévu : %s" % (key,))
    traitement = n_sub * THINK[key]
    redaction = eff * WRITE_LINE[level_key]
    total = lecture + traitement + redaction
    return {
        "minutes": round(total * 4) / 4.0,          # arrondi au quart de minute
        "breakdown": {
            "lecture": round(lecture, 2),
            "traitement": round(traitement, 2),
            "redaction": round(redaction, 2),
        },
        "features": {
            "caracteres_enonce": chars,
            "lignes_de_code": code,
            "sous_questions": n_sub,
            "lignes_offertes": offered,
            "lignes_retenues": round(eff, 2),
        },
        "model": "contenu-v2",
    }
