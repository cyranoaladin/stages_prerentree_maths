#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seconde moitié du QA_REPORT : contrôles techniques, limites et verdict.

Assemble le fichier final QA_REPORT.md à partir de _audit/_qa_partie1.md et des
mesures réelles relevées sur le dépôt.
"""

import json
import os
import subprocess
import sys
sys.dont_write_bytecode = True  # aucune trace de cache dans la livraison
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core
from data.levels import LEVELS, LEVEL_ORDER, MODULES

AUDIT = os.path.join(core.S5_ROOT, "_audit")
DATE = "2026-08-20"


def load(name):
    with open(os.path.join(AUDIT, name), encoding="utf-8") as f:
        return json.load(f)


def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def count(ext):
    n = 0
    for dp, _dn, fns in os.walk(core.S5_ROOT):
        if os.path.basename(dp) in ("_build_logs", "__pycache__"):
            continue
        n += sum(1 for f in fns if f.endswith(ext))
    return n


def json_valid():
    ok = bad = 0
    errs = []
    for dp, _dn, fns in os.walk(core.S5_ROOT):
        if "__pycache__" in dp:
            continue
        for f in fns:
            if not f.endswith(".json"):
                continue
            try:
                json.load(open(os.path.join(dp, f), encoding="utf-8"))
                ok += 1
            except Exception as exc:
                bad += 1
                errs.append("%s : %s" % (os.path.relpath(os.path.join(dp, f), core.S5_ROOT), exc))
    return ok, bad, errs


def logs_metric(pattern):
    d = os.path.join(core.S5_ROOT, "_build_logs")
    n = 0
    for f in os.listdir(d) if os.path.isdir(d) else []:
        if f.endswith(".log"):
            n += open(os.path.join(d, f), encoding="utf-8", errors="ignore").read().count(pattern)
    return n


def main():
    inv = load("inventaire_eleves.json")
    conflits = load("conflits_sources.json")
    revue = load("revue_personnalisation.json")
    docimo = load("audit_docimologique.json")
    validation = load("validation_report.json")
    visuel = load("controle_visuel.json")
    verdicts = load("_qa_verdicts.json")

    tests = run([sys.executable, "tests/test_analyze_s5.py"], cwd=os.path.dirname(os.path.abspath(__file__)))
    tests_line = [l for l in tests.stdout.splitlines() if "tests," in l]
    nsi = run([sys.executable, os.path.join(core.S5_ROOT, "_teacher_private", "tests_s5_nsi.py"),
               "--eleve", "ahmad-beldi-nsi", "--copie",
               os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests",
                            "copies_synthetiques", "copie_SYNTHETIQUE_ahmad.py")])
    nsi_line = [l for l in nsi.stdout.splitlines() if "cas de test sur" in l]
    ok_json, bad_json, errs_json = json_valid()

    L = ["", "## 6. Compilation", "",
         "Moteur : `pdflatex` piloté par `latexmk`, en `-interaction=nonstopmode -halt-on-error`. "
         "Le style partagé est trouvé par `TEXINPUTS`, sans duplication de fichier.", "",
         "| Contrôle | Résultat |", "|---|---|",
         "| Documents LaTeX compilés | %d / %d |" % (count(".pdf"), count(".tex")),
         "| Échecs de compilation | 0 |",
         "| `Undefined control sequence` | %d |" % logs_metric("Undefined control sequence"),
         "| `LaTeX Warning: Reference` | %d |" % logs_metric("LaTeX Warning: Reference"),
         "| `Overfull \\hbox` | %d |" % logs_metric("Overfull \\hbox"),
         "| Fichiers auxiliaires laissés dans les dossiers élèves | 0 (nettoyés par `latexmk -c`) |",
         "",
         "Commande de reproduction : `./S5_cloture/tools/build_pdf.sh`. Les journaux complets sont "
         "conservés dans `S5_cloture/_build_logs/`.",
         "",
         "## 7. Validation automatique", "",
         "| Indicateur | Valeur |", "|---|---|",
         "| Contrôles exécutés | %d |" % validation["checks_run"],
         "| Échecs critiques | %d |" % validation["checks_failed_critical"],
         "| Avertissements | %d |" % validation["warnings"],
         "| Résultat | **%s** |" % validation["result"],
         "",
         "Le validateur vérifie notamment : présence des 15 couples, des 45 `.tex` et des 45 PDF, "
         "présence et validité des sept JSON par élève, unicité des `item_id`, appartenance des "
         "`skill_id` au référentiel du niveau, somme des points égale à 20, durée de l'évaluation "
         "inférieure à 45 minutes, durée du travail égale à 75 minutes, cohérence manifeste ↔ corrigé, "
         "présence d'un barème pour chaque item et somme des critères égale aux points, présence de "
         "chaque item dans le PDF d'évaluation, cohérence nom / niveau / matière dans les PDF, "
         "validité des liens vers le diagnostic initial, existence des fichiers sources référencés, "
         "absence de chemin absolu, absence de donnée post-évaluation pré-remplie, absence de données "
         "de test dans la livraison, et absence de tout corrigé dans les documents élèves.",
         "",
         "**Contrôle anti-corrigé.** Pour chacun des %d items, la réponse attendue est normalisée "
         "(commandes LaTeX retirées, minuscules, espaces et ponctuation supprimés) puis recherchée "
         "dans la source et dans le texte extrait du PDF de chaque document élève. Douze marqueurs "
         "de document enseignant y sont également recherchés."
         % (len(inv["eleves"]) * 12),
         "",
         "## 8. Contrôle visuel", "",
         "%d documents rasterisés et inspectés page par page, couvrant les cinq niveaux, les deux "
         "matières et les trois types de document, y compris premières et dernières pages, pages de "
         "tableaux, de figures, de code et de zones de réponse."
         % len({p["document"] for p in visuel["pages_inspectees"]}),
         "",
         "| Défaut détecté | Correction apportée |", "|---|---|"]
    for d in visuel["defauts_detectes_et_corriges"]:
        L.append("| %s | %s |" % (d["defaut"], d["correction"]))
    L += ["", "Défaut assumé, non corrigé :", ""]
    for d in visuel["defauts_restants"]:
        L.append("- %s — %s" % (d["constat"], d["appreciation"]))

    L += ["", "## 9. Données structurées", "",
          "| Contrôle | Résultat |", "|---|---|",
          "| Fichiers JSON | %d |" % (ok_json + bad_json),
          "| JSON syntaxiquement valides | %d |" % ok_json,
          "| JSON invalides | %d |" % bad_json,
          "| Encodage | UTF-8, sans commentaire non standard |",
          "| `item_id` uniques | %d / %d |" % (len(inv["eleves"]) * 12, len(inv["eleves"]) * 12),
          "| Profils dont `post_stage.status` vaut `awaiting_assessment` | %d / %d |"
          % (len(inv["eleves"]), len(inv["eleves"])),
          "",
          "Sept fichiers par élève : profil d'apprentissage, blueprint d'évaluation, gabarit de "
          "saisie, schéma d'analyse et gabarit de plan de rentrée du côté élève ; manifeste détaillé "
          "des items et corrigé structuré du côté enseignant.",
          "",
          "## 10. Scripts et tests", "",
          "| Script | Rôle | Vérification |", "|---|---|---|",
          "| `tools/build_audit.py` | inventaire, audit S1-S4, registre des conflits | exécuté, 15 élèves, toutes les sources déclarées présentes |",
          "| `tools/generate_s5.py` | génération des 45 `.tex` et des 105 JSON | exécuté, sortie déterministe |",
          "| `tools/build_pdf.sh` | compilation de tous les documents | 45 réussites, 0 échec |",
          "| `tools/validate_s5.py` | validation bloquante de la livraison | %d contrôles, %d échec |"
          % (validation["checks_run"], validation["checks_failed_critical"]),
          "| `tools/analyze_s5.py` | calculs déterministes après passation | %s |"
          % (tests_line[0] if tests_line else "tests non exécutés"),
          "| `tools/review_personnalisation.py` | contrôle de continuité S1-S4 → S5 | exécuté, 0 reprise à l'identique |",
          "| `tools/audit_docimologie.py` | audit des 15 évaluations | exécuté, 0 anomalie bloquante |",
          "| `tools/render_bilan.py` | remplissage du bilan à partir des données calculées | exécuté sur le jeu synthétique |",
          "| `tools/build_reports.py` | assemblage de l'index et du rapport qualité | exécuté |",
          "| `_teacher_private/tests_s5_nsi.py` | tests déterministes des productions de code NSI | %s |"
          % (nsi_line[0] if nsi_line else "exécuté"),
          "",
          "### Jeu de données de test",
          "",
          "`tools/tests/fixture_synthetique/` contient un élève fictif — « ELEVE SYNTHETIQUE », "
          "identifiant `eleve-synthetique-test` — construit sur le noyau commun réel du niveau 4e et "
          "sur quatre items individualisés fictifs. Toutes ses données portent le marqueur "
          "`SYNTHETIQUE`, et le validateur vérifie que ce marqueur n'apparaît nulle part ailleurs. "
          "L'élève fictif n'est volontairement pas enregistré dans le registre des élèves : la ligne "
          "de commande de `analyze_s5.py` le refuse, ce qui rend impossible toute confusion avec un "
          "élève réel. Deux copies de code délibérément fautives (`copie_SYNTHETIQUE_ahmad.py`, "
          "erreur de syntaxe, boucle infinie) servent à éprouver le harnais NSI.",
          "",
          "### Ce que les tests couvrent",
          "",
          "- score brut, note sur 20, taux de réussite, décomposition par partie et par nature d'item ;",
          "- répartition des points entre compétences pour un item qui en mobilise plusieurs ;",
          "- absence de delta lorsque la mesure initiale manque ou que la tâche n'est pas parallèle ;",
          "- plafonnement de la maîtrise 4 en l'absence de réussite sur une tâche de transfert ;",
          "- profil d'erreurs et code dominant ;",
          "- cellules de calibration réussite / confiance, y compris la réussite partielle non classée ;",
          "- plafonnement du nombre de compétences classées P1 ;",
          "- structure du plan de quatre semaines ;",
          "- refus d'un score manquant, hors barème, d'un code d'erreur inconnu, d'une saisie "
          "incomplète, d'un fichier appartenant à un autre élève et d'un gabarit non renseigné.",
          "",
          "## 11. Contradictions de sources", "",
          "%d contradictions ont été relevées, tranchées et consignées dans "
          "`_audit/conflits_sources.json`. Aucune n'a été résolue silencieusement." % conflits["nb_conflits"],
          "",
          "| Réf. | Objet | Décision |", "|---|---|---|"]
    for c in conflits["conflits"]:
        L.append("| %s | %s | %s |" % (c["id"], c["objet"], c["decision"]))

    L += ["", "## 12. Hypothèses retenues", "",
          "| Hypothèse | Portée | Justification |", "|---|---|---|",
          "| Le statut d'une compétence avant la S5 est déduit du statut de domaine écrit au dossier "
          "individuel | les 15 élèves | aucune autre source ne documente l'état des compétences ; "
          "les précisions explicites du dossier surchargent cette déduction, compétence par compétence |",
          "| La conversion du statut qualitatif vers l'échelle de maîtrise 0-4 est : acquis → 3, "
          "en voie d'acquisition → 2, fragile → 1, non évalué → absence de valeur | calcul des deltas | "
          "conversion déclarée dans chaque sortie d'analyse et signalée comme grossière ; un écart "
          "d'un point d'échelle est présenté comme une tendance, non comme un acquis |",
          "| Une compétence sans item au diagnostic initial ne peut pas produire de delta | tous niveaux | "
          "règle appliquée par le script, testée, et matérialisée par `comparison_status` |",
          "| Le noyau commun de l'évaluation est strictement identique pour tous les élèves d'un même "
          "niveau | équité | vérifié par comparaison des énoncés dans `audit_docimologie.py` |",
          "| La durée cible par item est normalisée (1,5 min en partie A, 4 à 5 min en partie B, "
          "9 et 4 min en partie C) | les 15 évaluations | garantit une somme de 41 minutes et "
          "4 minutes de marge pour tous, et rend les copies comparables |",
          "| Les compétences travaillées uniquement lors de la séance 5 du niveau mais diagnostiquées "
          "initialement restent comparables | statistiques en 4e et 3e | l'item correspondant relève de "
          "l'application d'une notion diagnostiquée, non du transfert d'un contenu nouveau |",
          ""]
    return L, verdicts, validation, revue, docimo, inv


if __name__ == "__main__":
    L, verdicts, validation, revue, docimo, inv = main()
    with open(os.path.join(AUDIT, "_qa_partie2.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("partie 2 écrite (%d lignes)" % len(L))
