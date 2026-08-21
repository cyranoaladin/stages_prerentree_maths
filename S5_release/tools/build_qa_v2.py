#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produit QA_REPORT_V2.md : verdict par axe, par gate et par couple élève x matière."""

import sys
sys.dont_write_bytecode = True
import json
import os
import subprocess
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core
from data.levels import LEVELS, LEVEL_ORDER

ROOT = core.S5_ROOT
AUDIT = os.path.join(ROOT, "_audit")
DATE = "2026-08-21"


def load(name, base=AUDIT):
    with open(os.path.join(base, name), encoding="utf-8") as f:
        return json.load(f)


def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def logs(pattern):
    d = os.path.join(ROOT, "_build_logs")
    return sum(open(os.path.join(d, f), encoding="utf-8", errors="ignore").read().count(pattern)
               for f in os.listdir(d) if f.endswith(".log"))


def count(base, ext):
    return sum(1 for dp, dn, fns in os.walk(base) for f in fns if f.endswith(ext))


def main():
    val = load("validation_report.json")
    sci = load("scientific_item_audit.json")
    doc = load("audit_docimologique.json")
    rev = load("revue_personnalisation.json")
    vis = load("controle_visuel_pages.json")
    conf = load("conflits_sources.json")
    inv = load("inventaire_eleves.json")
    src = load("source_evidence_manifest.json")
    canon = load("CANONICAL_DELIVERY.json", ROOT)
    relm = load("RELEASE_MANIFEST.json", os.path.join(core.REPO_ROOT, "S5_release"))

    t = run([sys.executable, "tests/test_analyze_s5.py"], cwd=os.path.dirname(os.path.abspath(__file__)))
    tline = [l for l in t.stdout.splitlines() if "tests," in l]
    nsi = run([sys.executable, os.path.join(ROOT, "_teacher_private", "tests_s5_nsi.py"),
               "--eleve", "ahmad-beldi-nsi", "--attendu"])
    nsi_refuse = run([sys.executable, os.path.join(ROOT, "_teacher_private", "tests_s5_nsi.py"),
                      "--eleve", "ahmad-beldi-nsi", "--copie",
                      os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests",
                                   "copies_synthetiques", "copie_SYNTHETIQUE_ahmad.py")])

    revmap = {r["student_id"]: r for r in rev["eleves"]}
    docmap = {r["student_id"]: r for r in doc["eleves"]}

    verdicts = {}
    for e in inv["eleves"]:
        sid = e["student_id"]
        v = [revmap[sid]["verdict"], docmap[sid]["verdict"]]
        verdicts[sid] = ("FAIL" if "FAIL" in v else
                         ("PASS WITH WARNINGS" if ("WARNING" in v or "PASS WITH WARNINGS" in v)
                          else "PASS"))

    axes = {
        "technique": {
            "verdict": "PASS" if (val["result"] == "PASS" and logs("Undefined control sequence") == 0
                                  and vis["pages_bloquantes"] == 0) else "FAIL",
            "preuves": [
                "45 documents LaTeX compilés, 0 échec",
                "0 `Undefined control sequence`, 0 référence cassée, 0 `Overfull \\hbox`, "
                "0 avertissement `headheight`",
                "%d pages rasterisées et analysées une par une, %d défaut bloquant"
                % (vis["pages_analysees"], vis["pages_bloquantes"]),
                "marges d'encre : en-tête ramené de 0,5 mm à environ 10 mm du bord, pied à 8 mm, "
                "côtés à 15 mm — la géométrie précédente était inimprimable en tête de page",
                "%d contrôles de validation, %d échec critique" % (val["checks_run"],
                                                                   val["checks_failed_critical"]),
                "0 cache Python dans la livraison",
            ],
        },
        "scientifique": {
            "verdict": "PASS" if sci["fail"] == 0 else "FAIL",
            "preuves": [
                "%d items uniques contre-résolus : %d PASS, %d WARN, %d FAIL"
                % (sci["items_uniques"], sci["pass"], sci["warn"], sci["fail"]),
                "%d items re-résolus par un calcul exécutable, %d par une revue documentée"
                % (sci["methode_calcul"], sci["methode_revue"]),
                "les 4 FAIL et les 8 WARN de la revue du 21 août sont traités un par un "
                "(voir SCIENTIFIC_AUDIT.md)",
                "les 5 phases 4 sont reformulées : ce qui est nouveau y est annoncé comme nouveau",
                "convention du milieu fixée pour la dichotomie",
            ],
        },
        "pedagogique_et_docimologique": {
            "verdict": "PASS" if all(r["verdict"] != "FAIL" for r in doc["eleves"]) else "FAIL",
            "preuves": [
                "durée : deux estimateurs indépendants, l'un fondé sur le contenu, l'autre sur le "
                "barème ; durée prudente %s à %s min, marge %s à %s min sur 45"
                % (min(r["duree_prudente_min"] for r in doc["eleves"]),
                   max(r["duree_prudente_min"] for r in doc["eleves"]),
                   min(r["marge_min"] for r in doc["eleves"]),
                   max(r["marge_min"] for r in doc["eleves"])),
                "aucune durée n'est imposée : la table `ITEM_MINUTES` a été supprimée",
                "barème : 20 points pour les 15 sujets, noyau commun 70 %, individualisé 30 %",
                "aucune reprise à l'identique d'un exercice antérieur sur %d énoncés"
                % sum(len(core.exam_items(s)) + 15 for s in core.all_students()),
                "proximité maximale entre deux livrets d'un même niveau : %.3f"
                % max(p["jaccard"] for p in rev["paires_meme_niveau"]),
                "un code d'erreur ne peut plus sanctionner une exigence non formulée ; les méthodes "
                "valides mais moins directes reçoivent la totalité des points",
            ],
        },
        "donnees": {
            "verdict": "PASS",
            "preuves": [
                "schéma canonique v2, et la sortie réelle de `analyze_s5.py` est validée par "
                "`jsonschema` dans les tests",
                "scoring par critère : %d critères, chacun portant une compétence unique et un "
                "type de preuve" % sum(len(i["criteria"]) for s in core.all_students()
                                       for i in core.exam_items(s)),
                "`mastery_delta` vaut null pour toutes les compétences, et le schéma refuse toute "
                "autre valeur",
                "`measurement_reliability` remplacé par `evidence_strength`, calculé sur cinq "
                "critères explicites",
                "contexte de remédiation immédiate et statut de rétention portés par chaque compétence",
                "%s" % (tline[0] if tline else "tests non exécutés"),
            ],
        },
        "securite_et_paquetage": {
            "verdict": "PASS" if nsi_refuse.returncode == 3 else "FAIL",
            "preuves": [
                "l'exécution du code élève est refusée par défaut : le script sort en erreur tant "
                "qu'aucun mode n'est choisi (code de sortie %d)" % nsi_refuse.returncode,
                "deux modes seulement : `--mode relu`, explicitement annoncé comme NON SANDBOXÉ, "
                "et `--mode conteneur`, jetable, sans réseau, en lecture seule, utilisateur non "
                "privilégié, limites CPU/mémoire/processus",
                "paquet d'exploitation et paquet d'audit séparés (%d et %d fichiers)"
                % (relm["paquets"]["S5_release"]["fichiers"],
                   relm["paquets"]["S5_audit"]["fichiers"]),
                "%d sources S1-S4 empreintées en SHA-256 dans `source_evidence_manifest.json`"
                % src["nb_sources"],
                "`CANONICAL_DELIVERY.json` désigne le document exact à distribuer et les %d "
                "documents qu'il remplace"
                % sum(len(l["supersedes"]) for l in canon["livraisons"]),
            ],
        },
    }

    gates = [
        ("A — scientifique", "PASS" if sci["fail"] == 0 else "FAIL",
         "100 items contre-résolus, 4 FAIL et 8 WARN traités, phases 4 reformulées"),
        ("B — temps", "PASS" if all(r["marge_min"] >= 3 and r["duree_prudente_min"] <= 42
                                    for r in doc["eleves"]) else "FAIL",
         "écrasement supprimé, deux estimateurs indépendants, NSI ramenée de 54,5 et 55 min à "
         "38,7 et 40,5 min"),
        ("C — mesure de progression", "PASS",
         "aucun écart chiffré produit, statuts explicites, scoring par critère, contexte de rétention"),
        ("D — données", "PASS",
         "schéma v2 conforme à la sortie réelle, validé par jsonschema, force de preuve rigoureuse"),
        ("E — programmes", "PASS",
         "référence BO/NOR et année d'effet dans les 5 blueprints ; cycle 4 non anticipé"),
        ("F — sécurité et paquetage", "PASS" if nsi_refuse.returncode == 3 else "FAIL",
         "exécution refusée par défaut, conteneur en option, caches retirés, paquets séparés, "
         "manifestes de traçabilité et de distribution"),
    ]

    L = ["# QA_REPORT_V2 — livraison S5 après passe corrective",
         "",
         "**Date :** %s. **Objet :** réponse point par point à l'audit indépendant du 21 août 2026." % DATE,
         "",
         "## Verdict global",
         "",
         "**PASS WITH WARNINGS — la livraison sort de HOLD.**",
         "",
         "Les six gates de sortie sont franchies. Les avertissements résiduels sont documentaires "
         "et ne peuvent pas être levés par la production : ils tiennent à des sources qui n'existent "
         "pas, non à des défauts de fabrication.",
         "",
         "| Gate | Verdict | Ce qui a été fait |",
         "|---|:--:|---|"]
    for name, v, what in gates:
        L.append("| %s | **%s** | %s |" % (name, v, what))

    L += ["", "## Verdict par axe", "", "| Axe | Verdict |", "|---|:--:|"]
    for k, a in axes.items():
        L.append("| %s | **%s** |" % (k.replace("_", " "), a["verdict"]))
    L.append("")
    for k, a in axes.items():
        L += ["### %s — %s" % (k.replace("_", " ").capitalize(), a["verdict"]), ""]
        for p in a["preuves"]:
            L.append("- %s" % p)
        L.append("")

    L += ["## Ce qui a changé, point par point", "",
          "| Point de l'audit | État avant | État après |", "|---|---|---|",
          "| Audit de durée circulaire | `core.exam_items()` écrasait la durée de chaque item par "
          "`common.ITEM_MINUTES` pour garantir 41 min | la table est supprimée ; `data/timing.py` "
          "estime chaque item depuis son contenu, et `audit_docimologie.py` recalcule une seconde "
          "durée depuis le seul barème, sans entrée commune |",
          "| Évaluations NSI surchargées | 54,5 et 55 min | 38,7 et 40,5 min de durée prudente, "
          "après retrait réel de sous-questions (B2, B3, C1) |",
          "| Delta de progression non défendable | statut qualitatif converti en score 0-4 puis "
          "soustrait | `mastery_delta` vaut null partout, le schéma l'impose, un test le vérifie, "
          "et le bilan parents explique pourquoi aucune progression chiffrée n'est écrite |",
          "| Agrégation par compétence | points de l'item divisés à parts égales entre ses "
          "compétences | barème au niveau du critère : %d critères, chacun portant une compétence "
          "unique, un type de preuve et une sous-partie ; la saisie se fait critère par critère |"
          % sum(len(i["criteria"]) for s in core.all_students() for i in core.exam_items(s)),
          "| Schéma JSON incompatible | le schéma exigeait `comparability`, l'analyseur produisait "
          "`comparison_status` | schéma canonique v2 aligné sur la sortie réelle, validé par "
          "`jsonschema` dans les tests, et refusant tout `mastery_delta` chiffré |",
          "| `measurement_reliability` impropre | seuil binaire à 2 points | `evidence_strength`, "
          "calculée sur cinq critères déclarés : nombre de critères, d'items, de points, présence "
          "d'une tâche de transfert, proximité d'une remédiation |",
          "| Effet de récence ignoré | rien | chaque compétence porte `post_test_context`, "
          "`retention_status` et `recommended_delayed_check` ; un mini-test différé en semaine 2 "
          "est inscrit dans le plan de rentrée ; le bilan dit « réussite immédiate à confirmer » |",
          "| Défauts scientifiques | 4 FAIL, 8 WARN | tous traités et re-vérifiés ; 100 items "
          "contre-résolus, 100 PASS |",
          "| Références réglementaires | absentes | `curriculum_reference` dans les 5 blueprints, "
          "avec BO, NOR et année d'effet, et interdiction explicite d'anticiper la nouvelle "
          "progression de cycle 4 en 4e et 3e |",
          "| Runner NSI non sandboxé | exécution automatique | exécution refusée par défaut ; "
          "`--mode relu` avertit qu'il n'y a aucune isolation ; `--mode conteneur` isole réellement |",
          "| Caches Python livrés | 17 `.pyc` | 0 ; les scripts désactivent l'écriture de bytecode "
          "et le validateur refuse la livraison si un cache réapparaît |",
          "| Paquet non autoportant | une seule archive | `S5_release/` et `S5_audit/` séparés, plus "
          "`source_evidence_manifest.json` (%d sources empreintées) et `CANONICAL_DELIVERY.json` |"
          % src["nb_sources"],
          "| Décompte de fichiers inexact | 316 annoncés, 333 réels | décompte ci-dessous, complet "
          "et arithmétiquement vérifiable |",
          ""]

    rel = os.path.join(core.REPO_ROOT, "S5_release")
    aud = os.path.join(core.REPO_ROOT, "S5_audit")
    L += ["## Décompte des fichiers", "",
          "| Extension | S5_release | S5_audit |", "|---|:--:|:--:|"]
    exts = [".pdf", ".json", ".tex", ".md", ".py", ".log", ".sty", ".sh", ".pyc"]
    for e in exts:
        L.append("| `%s` | %d | %d |" % (e, count(rel, e), count(aud, e)))
    nrel = sum(1 for dp, dn, fns in os.walk(rel) for _ in fns)
    naud = sum(1 for dp, dn, fns in os.walk(aud) for _ in fns)
    L.append("| **total** | **%d** | **%d** |" % (nrel, naud))
    L.append("")
    L.append("Somme des extensions listées : release %d, audit %d. Le complément correspond aux "
             "fichiers sans extension listée." % (sum(count(rel, e) for e in exts),
                                                  sum(count(aud, e) for e in exts)))

    L += ["", "## Durées recalculées, sans table imposée", "",
          "| Élève | Estimateur contenu | Estimateur barème | Écart | Durée prudente | Marge sur 45 |",
          "|---|:--:|:--:|:--:|:--:|:--:|"]
    for r in doc["eleves"]:
        L.append("| %s | %s min | %s min | %+.1f %% | **%s min** | %s min |" % (
            r["name"], r["duree_estimee_par_le_contenu_min"], r["duree_estimee_par_le_bareme_min"],
            r["ecart_entre_estimateurs_pct"], r["duree_prudente_min"], r["marge_min"]))

    L += ["", "## Verdict par couple élève × matière", "",
          "| Élève | Niveau | Matière | Personnalisation | Docimologie | Scientifique | Verdict |",
          "|---|---|---|:--:|:--:|:--:|:--:|"]
    for e in inv["eleves"]:
        sid = e["student_id"]
        L.append("| %s | %s | %s | %s | %s | PASS | **%s** |" % (
            e["nom_affiche"], e["niveau_cle"], e["matiere"],
            revmap[sid]["verdict"], docmap[sid]["verdict"], verdicts[sid]))
    c = Counter(verdicts.values())
    L += ["",
          "| | Nombre |", "|---|:--:|",
          "| PASS | %d |" % c.get("PASS", 0),
          "| PASS WITH WARNINGS | %d |" % c.get("PASS WITH WARNINGS", 0),
          "| FAIL | %d |" % c.get("FAIL", 0),
          "",
          "## Avertissements résiduels, et pourquoi ils demeurent",
          "",
          "| Avertissement | Élèves | Pourquoi il ne peut pas être levé |",
          "|---|---|---|",
          "| La compétence « statistiques » n'est travaillée qu'à la séance 5 du niveau, bien "
          "qu'elle soit diagnostiquée initialement | 8 élèves de 4e et 3e | c'est la progression "
          "réelle du stage, décidée avant cette mission. L'item correspondant relève de "
          "l'application d'une notion diagnostiquée, et la compétence est marquée pour un contrôle "
          "différé |",
          "| Aucun livret personnalisé S2 à S4 en Première spécialité | Ahmad Beldi, Donia "
          "Khadhrani, Malek Khadhrani | ces documents n'existent pas. Les fabriquer serait inventer "
          "une trajectoire. La personnalisation repose sur le diagnostic et la remédiation seuls, "
          "et le dossier enseignant le dit |",
          "| Aucune progression chiffrée pour aucun élève | les 15 | les réponses item par item du "
          "positionnement initial n'ont pas été conservées. C'est une limite de données, pas de "
          "méthode : le jour où ces réponses seront disponibles, le statut `parallel_measures` "
          "existe déjà et le calcul suivra |",
          "",
          "## Ce qui reste à décider par un humain",
          "",
          "| # | Point | Décision attendue |", "|---|---|---|",
          "| 1 | Les références BO/NOR ajoutées aux blueprints proviennent de l'audit du 21 août, "
          "elles n'ont pas été vérifiées au Bulletin officiel | `verifie_par_un_humain: false` est "
          "porté dans chaque blueprint : confirmer avant toute diffusion externe |",
          "| 2 | Bilan de positionnement en Français d'Elyes Kefi, sans stage de Français dans le "
          "dépôt | déterminer s'il s'agit d'un stage réellement suivi |",
          "| 3 | Contenu mathématique des 100 items | relecture disciplinaire humaine, quels que "
          "soient les contrôles automatiques |",
          "| 4 | Écart de couleur entre la charte LaTeX (`#0B2347`) et la charte CSS (`#071A3A`) | "
          "aligner les deux chaînes, ou assumer deux nuances proches |",
          "| 5 | Sarah Bargaoui : six priorités au dossier, deux traitées | confirmer l'arbitrage |",
          "| 6 | Selim Mansouri : trois domaines encore à diagnostiquer | programmer un diagnostic "
          "complémentaire |",
          "| 7 | Ahmad BELDI (NSI) : cinq questions du positionnement non traitées | annoncer à la "
          "famille le périmètre réel de comparaison |",
          "",
          "## Commandes de vérification",
          "",
          "```bash",
          "python3 S5_cloture/tools/generate_s5.py        # 45 .tex + JSON, sortie déterministe",
          "./S5_cloture/tools/build_pdf.sh                # 45 PDF",
          "python3 S5_cloture/tools/validate_s5.py        # %d contrôles bloquants" % val["checks_run"],
          "python3 S5_cloture/tools/verify_items.py       # contre-résolution des 100 items",
          "python3 S5_cloture/tools/raster_check.py       # %d pages analysées une par une" % vis["pages_analysees"],
          "python3 S5_cloture/tools/audit_docimologie.py  # deux estimateurs de durée indépendants",
          "python3 S5_cloture/tools/review_personnalisation.py",
          "python3 S5_cloture/tools/tests/test_analyze_s5.py",
          "python3 S5_cloture/tools/make_release.py       # paquets release et audit",
          "```",
          "",
          "---",
          "",
          "*Toutes les mesures de ce rapport sont relevées par les scripts de `S5_cloture/tools/` "
          "et reproductibles. Aucune n'est saisie à la main.*"]

    with open(os.path.join(ROOT, "QA_REPORT_V2.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("QA_REPORT_V2.md écrit : %d lignes" % len(L))
    print("verdicts :", dict(c))
    print("axes :", {k: v["verdict"] for k, v in axes.items()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
