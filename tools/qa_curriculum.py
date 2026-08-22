#!/usr/bin/env python3
"""Audit curriculaire du corpus Terminale — chaque notion à sa place.

Le cahier des charges du stage distingue cinq statuts pour une notion : attendu de
Première, réactivation, approfondissement, passerelle Terminale, Terminale. La confusion
la plus coûteuse est celle qui présente une notion de Terminale comme un acquis supposé :
l'élève qui bute dessus est alors compté en déficit de Première, et on le fait travailler
sur ce qu'il maîtrise déjà.

Cette erreur est invisible dans un document fini — rien, dans un encadré « Rappel de
Première », ne signale que son contenu n'est pas de Première. Ce contrôle la rend visible.

Il ne remplace pas la lecture d'un enseignant : il tient ce qu'une relecture a établi.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

echecs: list[str] = []
controles = 0


def exige(condition: bool, message: str) -> None:
    global controles
    controles += 1
    if not condition:
        echecs.append(message)


# --- Ce qui relève de la Terminale, et de rien d'autre --------------------------------
# Ces listes sont tirées des sections « Contenus majeurs de Terminale » des documents
# sources du dépôt (tle_*/05_SOURCES/), et non d'un souvenir de programme. Une notion
# ajoutée ici doit l'être avec sa ligne de programme.
TERMINALE_SEULEMENT = {
    "tle_spe": [
        "raisonnement par récurrence", "démonstration par récurrence",
        "démontrer par récurrence", "hérédité",
        "limite d'une suite", "limite de la suite", "théorème des valeurs intermédiaires",
        "fonction logarithme", "logarithme népérien", "primitive", "primitives",
        "équation différentielle", "intégrale", "dérivée seconde", "convexité",
        "point d'inflexion", "loi des grands nombres", "représentation paramétrique",
        "vecteur normal", "produit scalaire dans l'espace",
    ],
    "tle_nsi": [
        "programmation orientée objet", "récursivité", "diviser pour régner",
        "programmation dynamique", "arbre binaire de recherche", "graphe pondéré",
        "ordonnancement",
        "base de données relationnelle", "requête sql", "interblocage",
        "routage", "protocole rip", "protocole ospf",
    ],
    "tle_pc": [
        "quotient de réaction", "constante d'équilibre", "taux d'avancement final",
        "diagramme de prédominance", "titrage", "vitesse volumique",
        "temps de demi-réaction", "catalyse", "vecteur accélération",
        "deuxième loi de newton", "lois de kepler", "premier principe",
        "énergie interne", "flux thermique", "résistance thermique",
        "loi de refroidissement", "condensateur", "constante de temps",
        "niveau d'intensité sonore", "décibel", "diffraction", "interférences",
        "effet doppler", "lunette astronomique", "photon",
    ],
}

# Les contextes qui affirment un acquis antérieur. Ce qu'ils contiennent doit être de
# Première — c'est tout leur propos.
CONTEXTE_ACQUIS = re.compile(
    r"^>\s*\*\*Rappel(?: de Première)?\.\*\*(?P<corps>.*?)(?=\n(?!>)|\Z)",
    re.M | re.S,
)


def module_de(chemin: Path) -> str | None:
    for module in TERMINALE_SEULEMENT:
        if chemin.is_relative_to(RACINE / module):
            return module
    return None


def documents() -> list[Path]:
    trouves: list[Path] = []
    for module in TERMINALE_SEULEMENT:
        trouves += sorted((RACINE / module).rglob("*.md"))
    return trouves


print("1. Aucune notion de Terminale dans un encadré qui affirme un acquis de Première")
for chemin in documents():
    module = module_de(chemin)
    if module is None:
        continue
    texte = chemin.read_text(encoding="utf-8")
    for bloc in CONTEXTE_ACQUIS.finditer(texte):
        corps = bloc.group("corps").lower()
        for notion in TERMINALE_SEULEMENT[module]:
            exige(
                notion not in corps,
                f"{chemin.relative_to(RACINE)} : « {notion} » est une notion de Terminale, "
                f"présentée dans un encadré « Rappel de Première ».",
            )

print("2. Le mémento de physique-chimie ne contient que des acquis de Première")
memento = (RACINE / "tle_pc/03_EVALUATIONS/tle_pc_Memento_Formules_Terminale_ELEVE.md")
corps = memento.read_text(encoding="utf-8").lower()
for notion in TERMINALE_SEULEMENT["tle_pc"]:
    exige(notion not in corps,
          f"Le mémento annonce « les acquis de Première » mais contient « {notion} ».")

print("3. Chaque domaine du positionnement porte son prérequis et son ouverture")
items = json.loads((RACINE / "content/items_terminale.json").read_text(encoding="utf-8"))
for matiere, corps_matiere in items["instruments"].items():
    for domaine, champ in corps_matiere["domaines"].items():
        for cle in ("prerequis_premiere", "ouverture_terminale", "reference_programme"):
            exige(bool(str(champ.get(cle, "")).strip()),
                  f"{matiere} / {domaine} : le champ « {cle} » est vide.")
        exige(any(classe in champ["prerequis_premiere"]
                  for classe in ("Première", "Seconde", "Collège")),
              f"{matiere} / {domaine} : le prérequis ne cite aucune classe antérieure "
              f"(Collège, Seconde ou Première).")
        exige("Terminale" in champ["reference_programme"],
              f"{matiere} / {domaine} : la référence ne cite pas le programme de Terminale.")

print("4. Aucun prérequis de Première ne décrit en réalité une notion de Terminale")
MODULE_DE_MATIERE = {"Mathématiques": "tle_spe", "Mathématiques expertes": "tle_spe",
                     "NSI": "tle_nsi", "Physique-chimie": "tle_pc"}
for matiere, corps_matiere in items["instruments"].items():
    module = MODULE_DE_MATIERE[matiere]
    for domaine, champ in corps_matiere["domaines"].items():
        prerequis = champ["prerequis_premiere"].lower()
        for notion in TERMINALE_SEULEMENT[module]:
            exige(notion not in prerequis,
                  f"{matiere} / {domaine} : le prérequis de Première annonce « {notion} », "
                  f"qui est au programme de Terminale.")

print("5. Le programme de mathématiques de 2026 n'est jamais présenté comme applicable")
# Il entre en vigueur en Terminale à la rentrée 2027-2028 : la cohorte accompagnée ici
# relève des textes de 2019. Un document qui s'appuierait sur l'arrêté de 2026 serait
# hors sujet, et rien dans son contenu ne le signalerait.
for chemin in documents():
    texte = chemin.read_text(encoding="utf-8")
    for marqueur in ("MENE2602919A", "2 avril 2026", "arrêté du 26 février 2026",
                     "BO n° 14"):
        if marqueur in texte:
            fenetre = texte[max(0, texte.find(marqueur) - 400):texte.find(marqueur) + 400]
            exige(
                "2027-2028" in fenetre or "ne s'applique" in fenetre
                or "non applicable" in fenetre or "pas à cette cohorte" in fenetre,
                f"{chemin.relative_to(RACINE)} : le programme de 2026 est cité sans dire "
                f"qu'il ne s'applique qu'à la rentrée 2027-2028.",
            )

print("6. Les passerelles vers la Terminale sont annoncées comme telles")
# Une notion de Terminale peut figurer dans une séance : c'est une ouverture volontaire.
# Elle doit alors être nommée comme telle, faute de quoi l'élève et le professeur la
# prendront pour un attendu. L'annonce porte le plus souvent sur toute une section — un
# titre « Ce que la Terminale en fera », une phrase d'ouverture — et non sur le paragraphe
# où la notion tombe : c'est donc la section entière qui fait foi.
ANNONCES = ("terminale", "passerelle", "ouverture", "excellence", "atelier",
            "pas attendu", "l'an prochain", "de demain", "cette année", "à venir",
            "plus tard", "expertes", "vers la ", "vers le ", "vers l'",
            "réutilisera", "verras", "verrez", "servira", "deviendra",
            "introduit", "exigera")
TITRE = re.compile(r"^#{1,6} .*$", re.M)
FIN_DE_PHRASE = re.compile(r"[.!?]\s")


def section_contenant(texte: str, position: int) -> str:
    """La section markdown qui contient cette position, titre compris."""
    titres = [m.start() for m in TITRE.finditer(texte)]
    debut = max((d for d in titres if d <= position), default=0)
    fin = min((d for d in titres if d > position), default=len(texte))
    return texte[debut:fin]


def phrase_contenant(texte: str, debut: int, fin: int) -> str:
    """La phrase qui porte la notion — une annonce au futur y suffit."""
    gauche = max((m.end() for m in FIN_DE_PHRASE.finditer(texte, 0, debut)), default=0)
    droite = FIN_DE_PHRASE.search(texte, fin)
    return texte[gauche:droite.end() if droite else len(texte)]


for chemin in documents():
    module = module_de(chemin)
    if module is None or "05_SOURCES" in str(chemin) or "01_ENSEIGNANT" in str(chemin):
        continue
    texte = chemin.read_text(encoding="utf-8")
    for notion in TERMINALE_SEULEMENT[module]:
        for occurrence in re.finditer(re.escape(notion), texte, re.I):
            fenetre = (section_contenant(texte, occurrence.start())
                       + phrase_contenant(texte, occurrence.start(), occurrence.end())).lower()
            exige(any(mot in fenetre for mot in ANNONCES),
                  f"{chemin.relative_to(RACINE)} : « {notion} » apparaît dans une section "
                  f"qui ne l'annonce pas comme une notion de Terminale (section "
                  f"« {section_contenant(texte, occurrence.start()).splitlines()[0][:60]} »).")

print()
if echecs:
    for message in echecs:
        print("  ÉCHEC", message)
    print(f"\n{controles - len(echecs)} contrôles passés, {len(echecs)} en échec.")
    sys.exit(1)
print(f"{controles} contrôles curriculaires passés, 0 en échec.")
