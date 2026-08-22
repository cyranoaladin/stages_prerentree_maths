#!/usr/bin/env python3
"""Dossier de remise — qui reçoit quoi, quand, et en combien d'exemplaires.

Le corpus est complet et vérifié ; il reste à le remettre. C'est là que se produisent les
fautes qui coûtent le plus cher, et elles n'ont rien de pédagogique : un cahier donné au
mauvais élève, un corrigé glissé dans une pochette élève, une liasse photocopiée en trop
peu d'exemplaires le matin de la séance 1.

Ce module produit la note de remise — une page par personne qui distribue — et vérifie que
ce qui a été produit correspond exactement à ce que le registre annonce. Il tourne sans
distribution TeX : le registre suffit à établir ce qui est attendu. Quand les PDF existent,
l'inventaire réel est confronté à cette attente.

    python3 tools/build_dossier_livraison.py          écrit la note et vérifie
    python3 tools/build_dossier_livraison.py --check  vérifie seulement
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "dist" / "terminale"
MANIFESTE = SORTIE / "MANIFEST_TERMINALE.csv"
NOTE = SORTIE / "NOTE_DE_REMISE.md"

PREFIXE = {"tle_spe": "Tle_SPE", "tle_nsi": "Tle_NSI", "tle_pc": "Tle_PC"}
LIBELLE = {"tle_spe": "Mathématiques", "tle_nsi": "NSI", "tle_pc": "Physique-chimie"}

echecs: list[str] = []


def exige(condition: bool, message: str) -> None:
    if not condition:
        echecs.append(message)


def registre() -> dict:
    return json.loads((RACINE / "content/students_terminale.json").read_text(encoding="utf-8"))


def inscriptions(reg: dict) -> list[tuple[dict, str]]:
    """Les couples (élève, module) réellement accompagnés, dans l'ordre des groupes."""
    couples = []
    for eleve in reg["students"]:
        if not eleve.get("active", True):
            continue
        for matiere in list(eleve.get("matieres", [])) + list(eleve.get("matieresSansDiagnostic", [])):
            couples.append((eleve, matiere["module"]))
    return couples


def attendus(reg: dict) -> dict[str, dict]:
    """Ce que chaque fichier produit doit être, indexé par son chemin dans dist/terminale."""
    prevu: dict[str, dict] = {}
    for eleve, module in inscriptions(reg):
        slug, nom = eleve["slug"], eleve["displayName"]
        base = f"{PREFIXE[module]}_{slug}"
        prevu[f"eleves/{base}_CAHIER_SEANCES_ELEVE.pdf"] = {
            "eleve": nom, "confidentiel": "oui", "destinataire": "eleve"}
        prevu[f"eleves/{base}_DOSSIER_ELEVE_PERSONNALISE.pdf"] = {
            "eleve": nom, "confidentiel": "oui", "destinataire": "eleve"}
        # Un élève sans bilan n'a pas de plan de remédiation : il n'y a rien à corriger.
        a_un_bilan = any(m["module"] == module for m in eleve.get("matieres", []))
        if a_un_bilan:
            prevu[f"enseignant/{base}_REMEDIATION_CORRIGE_ENSEIGNANT.pdf"] = {
                "eleve": nom, "confidentiel": "oui", "destinataire": "enseignant"}

    for module, prefixe in PREFIXE.items():
        for seance in range(1, 6):
            prevu[f"seances/{prefixe}_S{seance}_FICHE_ELEVE.pdf"] = {
                "eleve": "", "confidentiel": "non", "destinataire": "eleve"}
            prevu[f"enseignant/seances/{prefixe}_S{seance}_PREPARATION_ENSEIGNANT.pdf"] = {
                "eleve": "", "confidentiel": "non", "destinataire": "enseignant"}
        prevu[f"seances/{prefixe}_PACK_ELEVE_SEANCES.pdf"] = {
            "eleve": "", "confidentiel": "non", "destinataire": "eleve"}
        prevu[f"enseignant/{prefixe}_PACK_ENSEIGNANT_COMPLET.pdf"] = {
            "eleve": "", "confidentiel": "oui", "destinataire": "enseignant"}
    return prevu


def inventaire() -> list[dict] | None:
    if not MANIFESTE.exists():
        return None
    return list(csv.DictReader(MANIFESTE.open(encoding="utf-8")))


def verifie(reg: dict, prevu: dict[str, dict], produit: list[dict] | None) -> None:
    effectifs = {}
    for _eleve, module in inscriptions(reg):
        effectifs[module] = effectifs.get(module, 0) + 1
    for module, nombre in effectifs.items():
        exige(nombre > 0, f"{module} : aucun élève inscrit, le module ne devrait pas exister.")

    if produit is None:
        return

    reel = {ligne["fichier"]: ligne for ligne in produit}

    for chemin, attendu in prevu.items():
        exige(chemin in reel, f"Document attendu et non produit : {chemin}")
        if chemin not in reel:
            continue
        ligne = reel[chemin]
        for champ in ("eleve", "confidentiel", "destinataire"):
            exige(ligne[champ] == attendu[champ],
                  f"{chemin} : {champ} vaut « {ligne[champ] } », attendu « {attendu[champ]} ».")

    for chemin in reel:
        exige(chemin in prevu, f"Document produit et non attendu par le registre : {chemin}")

    # La règle qui protège les mineurs : rien de nominatif dans la liasse collective.
    noms = {eleve["displayName"] for eleve in reg["students"]}
    slugs = {eleve["slug"] for eleve in reg["students"]}
    for ligne in produit:
        dossier = ligne["fichier"].split("/")[0]
        if dossier == "seances":
            exige(ligne["confidentiel"] == "non",
                  f"{ligne['fichier']} est confidentiel et se trouve dans la liasse "
                  f"collective à photocopier.")
            exige(not ligne["eleve"],
                  f"{ligne['fichier']} porte le nom de {ligne['eleve']} et se trouve dans "
                  f"la liasse collective à photocopier.")
            exige(not any(slug in ligne["fichier"] for slug in slugs),
                  f"{ligne['fichier']} porte un nom d'élève dans son nom de fichier alors "
                  f"qu'il est dans la liasse collective.")
        if ligne["eleve"]:
            exige(ligne["eleve"] in noms,
                  f"{ligne['fichier']} est attribué à « {ligne['eleve']} », qui n'est pas "
                  f"au registre.")
            autres = [nom for nom in noms
                      if nom != ligne["eleve"]
                      and nom.replace(" ", "_") in ligne["fichier"]]
            exige(not autres,
                  f"{ligne['fichier']} est attribué à {ligne['eleve']} mais porte aussi "
                  f"le nom de {autres}.")


def pages(produit: list[dict] | None, chemin: str) -> str:
    if produit is None:
        return "—"
    for ligne in produit:
        if ligne["fichier"] == chemin:
            return ligne["pages"]
    return "—"


def note(reg: dict, prevu: dict[str, dict], produit: list[dict] | None) -> str:
    cadre = reg["cadre"]
    groupes = {g["id"]: g["libelle"] for g in reg["groupes"]}
    out: list[str] = []
    add = out.append

    add("# Note de remise — stages de pré-rentrée Terminale")
    add(f"## {cadre['organisme']} — {cadre['dates']}")
    add("")
    add(f"{cadre['natureOrganisme']}. {cadre['dureeParSpecialite']} par enseignement de "
        f"spécialité, {cadre['rythme']}. {cadre['note']}")
    add("")
    add("Cette note est **produite** par `tools/build_dossier_livraison.py` à partir du "
        "registre de la cohorte : elle ne peut pas décrire une remise différente de ce qui "
        "a été fabriqué. Elle se régénère à chaque build.")
    add("")
    add("---")
    add("")

    add("## 1. Ce que chaque élève reçoit, et quand")
    add("")
    add("| Élève | Groupe | Matière | Le 24 août, en main propre | Pages | À conserver après le stage | Pages |")
    add("|---|---|---|---|---:|---|---:|")
    for eleve, module in sorted(inscriptions(reg),
                                key=lambda c: (c[0]["groupe"], c[0]["displayName"], c[1])):
        base = f"{PREFIXE[module]}_{eleve['slug']}"
        cahier = f"eleves/{base}_CAHIER_SEANCES_ELEVE.pdf"
        dossier = f"eleves/{base}_DOSSIER_ELEVE_PERSONNALISE.pdf"
        add(f"| {eleve['displayName']} | {groupes[eleve['groupe']].split('—')[0].strip()} | "
            f"{LIBELLE[module]} | cahier des cinq séances | {pages(produit, cahier)} | "
            f"dossier individuel | {pages(produit, dossier)} |")
    add("")
    add("**Le cahier est le document de travail.** Il est remis le premier jour et suit "
        "l'élève pendant les dix heures. Il ne porte que les exercices de sa piste : le "
        "cahier d'un camarade ne lui conviendrait pas, et le sien ne conviendrait pas à un "
        "camarade. C'est la seule chose qu'il ait besoin d'apporter chaque jour.")
    add("")
    add("**Le dossier individuel se conserve.** Il restitue le positionnement, porte la page "
        "de signature et sert d'appui à l'entretien avec la famille. On l'imprime une fois.")
    add("")

    add("## 2. Ce qui se photocopie pour le groupe")
    add("")
    effectifs: dict[str, int] = {}
    for _eleve, module in inscriptions(reg):
        effectifs[module] = effectifs.get(module, 0) + 1
    add("| Matière | Élèves | Document | Exemplaires | Pages | Total feuilles (recto-verso) |")
    add("|---|---:|---|---:|---:|---:|")
    for module in ("tle_spe", "tle_nsi", "tle_pc"):
        if module not in effectifs:
            continue
        for seance in range(1, 6):
            chemin = f"seances/{PREFIXE[module]}_S{seance}_FICHE_ELEVE.pdf"
            p = pages(produit, chemin)
            total = (str(-(-int(p) // 2) * effectifs[module]) if p.isdigit() else "—")
            add(f"| {LIBELLE[module]} | {effectifs[module]} | fiche élève S{seance} | "
                f"{effectifs[module]} | {p} | {total} |")
    add("")
    add("Ces fiches ne portent aucun nom : elles sont identiques pour tout le groupe. "
        "**Photocopier séance par séance**, la veille — pas les cinq d'un coup : une séance "
        "qui se déroule autrement que prévu rend la liasse suivante caduque.")
    add("")

    add("## 3. Ce qui reste entre les mains de l'enseignant")
    add("")
    add("| Matière | Document | Contenu | Pages |")
    add("|---|---|---|---:|")
    for module in ("tle_spe", "tle_nsi", "tle_pc"):
        if module not in effectifs:
            continue
        for seance in range(1, 6):
            chemin = f"enseignant/seances/{PREFIXE[module]}_S{seance}_PREPARATION_ENSEIGNANT.pdf"
            add(f"| {LIBELLE[module]} | préparation S{seance} | fiche professeur, supports, "
                f"cartes d'aide | {pages(produit, chemin)} |")
        chemin = f"enseignant/{PREFIXE[module]}_PACK_ENSEIGNANT_COMPLET.pdf"
        add(f"| {LIBELLE[module]} | pack complet | tout le module, corrigés compris | "
            f"{pages(produit, chemin)} |")
    add("")
    add("| Élève concerné | Matière | Corrigé du plan de remédiation | Pages |")
    add("|---|---|---|---:|")
    for chemin in sorted(c for c in prevu if c.endswith("_REMEDIATION_CORRIGE_ENSEIGNANT.pdf")):
        info = prevu[chemin]
        module = next(m for m, p in PREFIXE.items() if chemin.split("/")[1].startswith(p + "_"))
        add(f"| {info['eleve']} | {LIBELLE[module]} | `{chemin.split('/')[-1]}` | "
            f"{pages(produit, chemin)} |")
    add("")
    add("**Aucun de ces documents ne sort du dossier pédagogique.** Les packs et les tableaux "
        "de bord portent les diagnostics de plusieurs élèves : les remettre à une famille, "
        "même la sienne, expose ceux des autres.")
    add("")

    add("## 4. Les quatre règles qui n'ont pas d'exception")
    add("")
    add("1. **Un document nominatif ne va qu'à l'élève dont il porte le nom, ou à sa "
        "famille.** Jamais dans une liasse collective, jamais à un camarade. Vérifier le nom "
        "sur la couverture avant de tendre le document.")
    add("2. **Aucun corrigé dans une pochette élève**, même à la demande d'une famille : le "
        "plan de remédiation est fait pour être tenté avant d'être corrigé. "
        "`tools/build_terminale_pdf.py` refuse d'assembler un pack élève contenant un "
        "document marqué `PROF`, `Corrige`, `Tableau_Bord` ou `Guide_Formateur` — "
        "l'assemblage échoue plutôt que de produire un fichier douteux.")
    add("3. **Le mémento de formules de physique-chimie part avec l'élève en septembre.** "
        "C'est le seul document du corpus destiné à servir après le stage : le glisser dans "
        "le portfolio, pas dans la liasse du jour.")
    add("4. **Les fichiers Markdown font foi, pas les PDF.** Un PDF n'est pas reproductible "
        "d'une machine à l'autre : il n'est pas versionné. En cas de doute sur un contenu, "
        "c'est la source qu'on relit.")
    add("")

    add("## 5. À cocher avant le 24 août")
    add("")
    for etape in (
        "`make terminale` puis `make terminale-pdf` ont été relancés sur la dernière version.",
        "`make terminale-test`, `make terminale-qa` et `make terminale-check` passent.",
        "Le nombre de dossiers imprimés correspond au tableau 1, élève par élève.",
        "Chaque dossier élève a été ouvert et le nom vérifié sur la couverture.",
        "Les fiches de la séance 1 sont photocopiées, dans le nombre du tableau 2.",
        "Les corrigés nominatifs sont dans la pochette de l'enseignant, pas dans les liasses.",
        "Un jeu du positionnement papier est prévu pour l'élève qui ne l'a pas passé.",
    ):
        add(f"- [ ] {etape}")
    add("")

    add("## 6. Ce que cette cohorte a de particulier")
    add("")
    for eleve in reg["students"]:
        if not eleve.get("active", True):
            continue
        particularites = []
        if eleve.get("optionAnnuelle"):
            particularites.append(
                f"suit l'option **{eleve['optionAnnuelle']['intitule']}** — elle ne fait "
                f"l'objet d'aucun dossier séparé : elle figure dans le dossier de "
                f"mathématiques, section « Option annuelle », et ses exercices sont à la fin "
                f"de la feuille de remédiation. Le dossier est donc plus épais")
        if eleve.get("matieresSansDiagnostic"):
            particularites.append(
                "n'a **pas passé le positionnement** : son cahier porte l'étayage le plus "
                "complet et n'annonce aucun résultat, et son dossier organise la passation "
                "en séance 1 au lieu de restituer un bilan. Prévoir un jeu papier")
        if eleve.get("noteGroupe"):
            particularites.append(eleve["noteGroupe"].rstrip("."))
        if particularites:
            add(f"- **{eleve['displayName']}** " + " ; ".join(particularites) + ".")
    add("")
    add("**Ne pas se fier au nom du groupe pour savoir quoi remettre.** Le tableau 1 fait "
        "foi : il est produit à partir des spécialités réelles de chaque élève.")
    add("")
    add("---")
    add("_Note produite par `tools/build_dossier_livraison.py`. Ne pas la modifier à la "
        "main : elle est réécrite à chaque build._")
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="vérifier sans écrire la note")
    options = parser.parse_args(argv)

    reg = registre()
    prevu = attendus(reg)
    produit = inventaire()
    verifie(reg, prevu, produit)

    if echecs:
        for message in echecs:
            print("  ÉCHEC", message)
        print(f"\n{len(echecs)} anomalies de remise.")
        return 1

    couples = len(inscriptions(reg))
    if produit is None:
        print(f"OK : {couples} inscriptions, {len(prevu)} documents attendus. "
              f"Les PDF n'ont pas été produits — inventaire réel non confronté.")
    else:
        print(f"OK : {couples} inscriptions, {len(produit)} documents produits, "
              f"conformes au registre. Aucun document nominatif dans la liasse collective.")

    if not options.check:
        SORTIE.mkdir(parents=True, exist_ok=True)
        NOTE.write_text(note(reg, prevu, produit), encoding="utf-8")
        print(f"Note de remise écrite : {NOTE.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
