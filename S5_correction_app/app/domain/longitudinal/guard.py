# -*- coding: utf-8 -*-
"""Contrôle du texte avant compilation. Le dernier filet, pas le premier.

Ce module ne rend pas un texte correct : il refuse d'en laisser passer un qui ne
l'est pas. Il attrape trois familles de fautes, qui n'ont pas la même origine :

* **fuite technique** — un identifiant de compétence ou de critère dans un document
  destiné à une famille. Ce sont des clés internes, illisibles et anxiogènes ;
* **surinterprétation** — une progression chiffrée, une maîtrise déclarée
  définitive, un écart de maîtrise présenté comme mesuré alors qu'aucune mesure
  initiale nominative n'existe ;
* **disqualification** — « lacune », « élève faible », « n'a pas le niveau ». Ces
  mots ne décrivent pas un résultat : ils qualifient une personne. Sur une notion
  de passerelle, « lacune » est de surcroît faux, puisque la notion relève du
  programme de l'année suivante.

Chaque règle porte la raison de son existence : un contrôle dont on ignore le motif
finit par être désactivé.
"""

import re

# ------------------------------------------------------------------ identifiants
# Les identifiants de compétence du corpus (M4E_..., M3_..., NSI1_...) et les
# identifiants de critère (4E_INES_KEFI_B2_c1, y compris les sous-critères _v1).
RE_SKILL_ID = re.compile(r"\b(?:M\d?[A-Z]{1,4}\d?_[A-Z0-9_]{2,}|NSI\d_[A-Z0-9_]{2,})\b")
RE_CRITERION_ID = re.compile(r"\b\d?[A-Z]{1,4}_[A-Z_]+_[A-Z]\d+_c\d+(?:_v\d+)?\b")
RE_SCOPE_KEY = re.compile(r"\b(?:n_minus_1|bridge_n|curriculum_scope|mastery_delta|"
                          r"evidence_strength|scoring_id)\b")

# ------------------------------------------------------------- progression chiffrée
# « +35 % de progression », « progression de 2 points », « a progressé de 15 % ».
RE_PROGRESSION = re.compile(
    r"(?:progress(?:ion|é|e)\w*[^.]{0,40}?[+-]?\s*\d+([.,]\d+)?\s*(?:%|points?|niveaux?)"
    r"|[+-]\s*\d+([.,]\d+)?\s*%\s*(?:de\s+)?progression)", re.IGNORECASE)
RE_NIVEAUX = re.compile(r"[+-]\s*\d+\s*niveaux?\b", re.IGNORECASE)

# ------------------------------------------------------------------ affirmations
PHRASES_INTERDITES = (
    ("définitivement acquis", "aucune preuve ponctuelle n'établit une acquisition définitive"),
    ("definitivement acquis", "aucune preuve ponctuelle n'établit une acquisition définitive"),
    ("élève faible", "qualifie la personne et non le résultat"),
    ("eleve faible", "qualifie la personne et non le résultat"),
    ("n'a pas le niveau", "jugement global, non soutenu par une évaluation de 45 minutes"),
    ("na pas le niveau", "jugement global, non soutenu par une évaluation de 45 minutes"),
    ("est indispensable", "aucune recommandation commerciale ne doit être automatique"),
)

# « lacune » est proscrit partout dans le document parents : sur un prérequis il
# disqualifie, sur une passerelle il est faux.
MOT_LACUNE = re.compile(r"\blacunes?\b", re.IGNORECASE)


def _lignes(texte):
    for numero, ligne in enumerate(texte.splitlines(), start=1):
        yield numero, ligne


def check_parent_text(texte: str) -> list:
    """Contrôles applicables à un document destiné aux familles.

    Retourne la liste des manquements ; une liste vide vaut acceptation.
    """
    manquements = []

    def signaler(ligne, regle, extrait, raison):
        manquements.append({"line": ligne, "rule": regle,
                            "excerpt": extrait.strip()[:160], "reason": raison})

    for numero, ligne in _lignes(texte):
        for motif, regle, raison in (
                (RE_CRITERION_ID, "criterion_id",
                 "un identifiant de critère est une clé interne"),
                (RE_SKILL_ID, "skill_id",
                 "un identifiant de compétence est une clé interne"),
                (RE_SCOPE_KEY, "cle_technique",
                 "vocabulaire technique du moteur d'analyse"),
                (RE_PROGRESSION, "progression_chiffree",
                 "aucune mesure initiale nominative n'existe : un écart chiffré serait fabriqué"),
                (RE_NIVEAUX, "progression_chiffree",
                 "les niveaux ne sont pas une échelle mesurée"),
                (MOT_LACUNE, "lacune",
                 "disqualifie l'élève ; sur une notion de l'année à venir, c'est de "
                 "surcroît inexact")):
            trouve = motif.search(ligne)
            if trouve:
                signaler(numero, regle, trouve.group(0), raison)

        minuscule = ligne.lower()
        for phrase, raison in PHRASES_INTERDITES:
            if phrase in minuscule:
                signaler(numero, "phrase_interdite", phrase, raison)

    return manquements


def check_mastery_claims(trajectoire, texte: str) -> list:
    """Refuse d'annoncer maîtrisée une compétence sans preuve finale directe.

    C'est le contrôle qui empêche le glissement « figure au livret » → « acquise ».
    Une compétence dont l'évaluation ne dit rien ne peut pas voir son intitulé
    précédé d'un verbe de maîtrise dans le document.
    """
    manquements = []
    verbes = ("maîtrise", "maitrise", "acquis", "acquise", "sait faire", "réussit")
    minuscule = texte.lower()
    for ligne in trajectoire:
        if ligne.get("has_final_evidence"):
            continue
        label = (ligne.get("label") or "").lower().rstrip(".")
        if not label or label not in minuscule:
            continue
        position = minuscule.index(label)
        fenetre = minuscule[max(0, position - 140):position + len(label) + 60]
        for verbe in verbes:
            if verbe in fenetre:
                manquements.append({
                    "line": None, "rule": "maitrise_sans_preuve",
                    "excerpt": fenetre.strip()[:160],
                    "reason": "« %s » n'est évaluée par aucun critère de la copie de "
                              "clôture : le stage l'a ciblée, l'évaluation ne la "
                              "documente pas" % (ligne.get("label") or ""),
                })
                break
    return manquements


def validate(texte: str, trajectoire=None, audience: str = "parents") -> dict:
    """Point d'entrée unique. ``audience`` vaut « parents », « eleve » ou « enseignant ».

    La synthèse enseignant a le droit — et le besoin — de porter les identifiants
    techniques : elle n'est pas soumise aux règles de fuite. Les règles de
    surinterprétation, elles, s'appliquent à tout le monde.
    """
    if audience == "enseignant":
        manquements = [m for m in check_parent_text(texte)
                       if m["rule"] in ("progression_chiffree", "phrase_interdite")]
    else:
        manquements = check_parent_text(texte)
    if trajectoire and audience != "enseignant":
        manquements += check_mastery_claims(trajectoire, texte)
    return {"ok": not manquements, "violations": manquements,
            "checked_rules": ["criterion_id", "skill_id", "cle_technique",
                              "progression_chiffree", "lacune", "phrase_interdite",
                              "maitrise_sans_preuve"]}
