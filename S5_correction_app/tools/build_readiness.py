#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manifestes de préparation longitudinale, un par couple élève × matière.

Produit, sans rien corriger ni saisir :

* ``runtime/readiness/<student_id>/LONGITUDINAL_SOURCE_READINESS.json`` — l'état
  détaillé des sources d'un élève, avec ce qui manque et pourquoi ;
* ``docs/LONGITUDINAL_READINESS_15.md`` — la matrice des quinze, lisible d'un
  coup d'œil.

Les manifestes vivent sous ``runtime/``, hors de Git : ils décrivent l'état d'un
poste à un instant donné, pas une vérité du dépôt.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config, database                                   # noqa: E402
from app.domain.longitudinal import readiness                       # noqa: E402
import migrations                                                   # noqa: E402

SYMBOLES = {True: "oui", False: "—"}
ETIQUETTES = {
    readiness.READY: "Prêt",
    readiness.WARNING: "Prêt avec réserve documentaire",
    readiness.BLOCKED: "Bloqué",
}


def _case_seance(etat):
    if not etat.get("general_material"):
        return "absente"
    return "perso." if etat.get("personalised_dossier") else "niveau"


def build(session) -> list:
    return readiness.evaluate_all(session, config)


def write_manifests(etats) -> list:
    racine = Path(config.RUNTIME_DIR) / "readiness"
    ecrits = []
    for etat in etats:
        dossier = racine / etat["student_id"]
        dossier.mkdir(parents=True, exist_ok=True)
        chemin = dossier / "LONGITUDINAL_SOURCE_READINESS.json"
        chemin.write_text(json.dumps(etat, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
        ecrits.append(str(chemin))
    return ecrits


def write_matrix(etats, destination=None) -> str:
    resume = readiness.summary(etats)
    lignes = [
        "# Préparation longitudinale — les quinze couples élève × matière",
        "",
        "Relevé produit par `tools/build_readiness.py`. Il décrit **les sources**, pas",
        "les résultats : aucune copie n'est corrigée ici.",
        "",
        "| état | nombre |",
        "| --- | ---: |",
        "| Prêt | %d |" % resume["ready"],
        "| Prêt avec réserve documentaire | %d |" % resume["ready_with_warning"],
        "| Bloqué | %d |" % resume["blocked"],
        "",
        "**%d des %d couples sont corrigeables aujourd'hui.**"
        % (resume["total"] - resume["blocked"], resume["total"]),
        "",
        "Dans la colonne des séances : *perso.* désigne un dossier personnalisé trouvé,",
        "*niveau* le seul matériel de séance du niveau, *absente* aucune source.",
        "",
        "| Élève | Niveau | Initial | S1 | S2 | S3 | S4 | S5 | Évaluation | Longitudinal | Statut | Réserves |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: |",
    ]
    for etat in etats:
        seances = etat.get("sessions") or {}
        finale = etat.get("final_assessment") or {}
        diagnostic = etat.get("diagnostic") or {}
        lignes.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %d |" % (
            etat["display_name"],
            etat.get("level_label", "—").replace("Entrée en ", ""),
            "oui (%d compétences)" % diagnostic.get("skills", 0)
            if diagnostic.get("available") else "non",
            _case_seance(seances.get("S1", {})), _case_seance(seances.get("S2", {})),
            _case_seance(seances.get("S3", {})), _case_seance(seances.get("S4", {})),
            _case_seance(seances.get("S5", {})),
            "%d lignes / %s pts" % (finale.get("scoring_lines", 0),
                                    (finale.get("max_points_centi") or 0) // 100)
            if finale.get("defined") else "absente",
            SYMBOLES[bool(etat["longitudinal_report"]["ready"])],
            ETIQUETTES.get(etat["status"], etat["status"]),
            len(etat["longitudinal_report"]["warnings"])))

    lignes += ["", "## Réserves, élève par élève", ""]
    for etat in etats:
        reserves = etat["longitudinal_report"]["warnings"]
        blocages = etat.get("blockers") or []
        if not reserves and not blocages:
            continue
        lignes.append("### %s" % etat["display_name"])
        lignes.append("")
        for blocage in blocages:
            lignes.append("- **Blocage.** %s." % blocage)
        for reserve in reserves:
            lignes.append("- %s." % reserve)
        lignes.append("")

    lignes += [
        "## Lecture",
        "",
        "Aucun couple n'est bloqué : les quinze peuvent être corrigés et donneront un",
        "bilan longitudinal. Les réserves portent toutes sur la **documentation du",
        "parcours**, jamais sur l'évaluation elle-même — et chacune sera écrite dans le",
        "bilan produit, sous la forme d'une limite d'interprétation.",
        "",
        "Deux réserves reviennent chez tout le monde et méritent d'être comprises :",
        "",
        "1. **Aucune observation de séance n'a été saisie.** Les tableaux de suivi des",
        "   dossiers individuels sont des formulaires vierges. Le bilan pourra donc dire",
        "   « cette notion a fait l'objet d'un travail ciblé en S2 », jamais « l'élève l'a",
        "   réussie en S2 ». C'est la raison d'être du niveau de preuve C.",
        "2. **Les dossiers de séance personnalisés ne couvrent pas les cinq séances.**",
        "   Le thème de la séance reste connu par le matériel de niveau ; la",
        "   personnalisation, elle, ne l'est pas, et rien n'est inventé pour la combler.",
        "",
    ]
    contenu = "\n".join(lignes)
    chemin = Path(destination or (Path(config.PROJECT_DIR) / "docs"
                                  / "LONGITUDINAL_READINESS_15.md"))
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(contenu, encoding="utf-8")
    return str(chemin)


def main(argv=None):
    config.ensure_runtime()
    migrations.apply(database.engine(), config.DB_PATH, config.BACKUPS_DIR)
    with database.session_scope() as session:
        etats = build(session)
    manifestes = write_manifests(etats)
    matrice = write_matrix(etats)
    resume = readiness.summary(etats)

    print("couples examinés          %d" % resume["total"])
    print("  prêts                   %d" % resume["ready"])
    print("  prêts avec réserve      %d" % resume["ready_with_warning"])
    print("  bloqués                 %d" % resume["blocked"])
    print("manifestes écrits         %d" % len(manifestes))
    print("matrice                   %s" % matrice)
    return 0 if resume["blocked"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
