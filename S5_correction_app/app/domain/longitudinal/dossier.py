# -*- coding: utf-8 -*-
"""Lecture du dossier individuel : objectifs personnalisés et suivi de séance.

Le dossier individuel contient deux choses que le profil d'apprentissage ne porte
pas : l'**objectif personnel** écrit pour chaque séance, et les **tableaux de suivi**
que l'enseignant remplit pendant le stage.

Les seconds sont, dans le corpus actuel, des formulaires vierges : cases non cochées,
cellules vides, auto-bilan en pointillés. C'est une information en soi, et cette
lecture la produit explicitement (``observations_available = False``) plutôt que de
laisser croire qu'aucune observation n'a été cherchée.

L'extraction est volontairement littérale : on lit ce qui est écrit, on ne complète
jamais. Un dossier absent ou d'une autre forme donne un résultat vide, pas une
reconstitution.
"""

import re

# « | 1 | Calculer avec du sens | Fractions équivalentes, puis ordre ... | | | »
_LIGNE_PARCOURS = re.compile(r"^\|\s*(\d)\s*\|([^|]*)\|([^|]*)\|(.*)$")

# Une cellule est vide si elle ne contient que des espaces, des points de conduite
# ou des cases à cocher non cochées.
_VIDE = re.compile(r"^[\s.·☐_\-]*$")


def _cellules(ligne):
    return [c.strip() for c in ligne.strip().strip("|").split("|")]


def parse(texte: str) -> dict:
    """Extrait le parcours personnalisé et l'état du suivi de séance."""
    parcours, suivi = {}, {}
    section = None
    seance_courante = None

    for ligne in texte.splitlines():
        depouillee = ligne.strip()

        if depouillee.startswith("## "):
            section = depouillee[3:].strip().lower()
            seance_courante = None
            continue
        if depouillee.startswith("### Séance") or depouillee.startswith("### Seance"):
            trouve = re.search(r"(\d)", depouillee)
            seance_courante = "S%s" % trouve.group(1) if trouve else None
            continue

        if section and "parcours personnalis" in section:
            trouve = _LIGNE_PARCOURS.match(depouillee)
            if trouve:
                numero, theme, focus = trouve.group(1), trouve.group(2), trouve.group(3)
                parcours["S%s" % numero] = {
                    "theme": theme.strip() or None,
                    "personal_focus": focus.strip() or None,
                }
            continue

        if section and "suivi des cinq" in section and seance_courante:
            if depouillee.startswith("**Objectif personnel"):
                valeur = depouillee.split(":", 1)[-1].strip().strip("*").strip()
                suivi.setdefault(seance_courante, {})["personal_focus"] = valeur or None
            elif depouillee.startswith("|") and depouillee.count("|") >= 4:
                cellules = _cellules(depouillee)
                if len(cellules) >= 4 and cellules[0] not in ("Observation", "---"):
                    renseignee = any(not _VIDE.match(c) for c in cellules[1:])
                    etat = suivi.setdefault(seance_courante, {})
                    etat["has_filled_row"] = etat.get("has_filled_row", False) or renseignee

    seances = {}
    for cle in ("S1", "S2", "S3", "S4", "S5"):
        depuis_parcours = parcours.get(cle) or {}
        depuis_suivi = suivi.get(cle) or {}
        seances[cle] = {
            "theme": depuis_parcours.get("theme"),
            # L'objectif du tableau de suivi fait foi : c'est celui qui a été
            # imprimé en tête de la séance.
            "personal_focus": (depuis_suivi.get("personal_focus")
                               or depuis_parcours.get("personal_focus")),
            "observations_available": bool(depuis_suivi.get("has_filled_row")),
        }
    return {
        "sessions": seances,
        "observations_available_anywhere":
            any(s["observations_available"] for s in seances.values()),
        "personalised_objectives_found":
            sum(1 for s in seances.values() if s["personal_focus"]),
    }


def read(path) -> dict:
    """Lit un dossier individuel. Un fichier absent donne un résultat vide et honnête."""
    try:
        texte = open(str(path), encoding="utf-8").read()
    except (OSError, UnicodeDecodeError):
        return {"sessions": {}, "observations_available_anywhere": False,
                "personalised_objectives_found": 0, "unreadable": True}
    resultat = parse(texte)
    resultat["unreadable"] = False
    return resultat
