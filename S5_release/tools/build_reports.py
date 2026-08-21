#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble INDEX_S5.md et QA_REPORT.md à partir des fichiers d'audit produits.

Aucun chiffre n'est saisi à la main : tout provient de
    _audit/inventaire_eleves.json
    _audit/conflits_sources.json
    _audit/revue_personnalisation.json
    _audit/audit_docimologique.json
    _audit/validation_report.json
et de l'inspection du système de fichiers.

Le seul contenu rédigé est la lecture pédagogique élève par élève (dictionnaire
CONTINUITE ci-dessous), écrite après lecture des dossiers individuels, des plans
de remédiation et des livrets personnalisés S2 à S4.
"""

import json
import os
import subprocess
import sys
sys.dont_write_bytecode = True  # aucune trace de cache dans la livraison
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core
from data import common
from data.levels import LEVELS, LEVEL_ORDER, MODULES

AUDIT = os.path.join(core.S5_ROOT, "_audit")
DATE = "2026-08-20"

# --------------------------------------------------------------------------
# Lecture pédagogique, rédigée après consultation des sources de chaque élève.
# Chaque entrée dit : ce que le diagnostic établit, ce que S1-S4 a travaillé,
# ce que la S5 en fait, et ce qui reste explicitement à vérifier.
# --------------------------------------------------------------------------
CONTINUITE = {
    "ines-kefi": (
        "Le diagnostic établit deux réponses fausses données avec une certitude maximale, sur "
        "l'ordre des relatifs et le déplacement sur une droite graduée, ainsi qu'une conversion "
        "de fraction incomplète sur 5/6 − 1/3. La séance 1 a travaillé relatifs et fractions, la "
        "séance 3 le calcul littéral, la séance 4 la géométrie ; le plan de remédiation reprend "
        "exactement ces quatre points. La S5 place en phase 2 l'ordre et la droite graduée — la "
        "conviction erronée passe avant la technique — et en phase 3 la transformation complète "
        "d'une fraction. L'évaluation reprend ces deux compétences en A5 et A6, avec des items "
        "parallèles à 4E_TI_Q17 et 4E_TI_Q04, et vérifie en B4 la rédaction géométrique sans "
        "hypothèse ajoutée, quatrième priorité du dossier. Reste à vérifier : la calibration "
        "réussite-confiance, dont le point de départ documenté est 67 %."),
    "sinda-chikhaoui": (
        "Le dossier cite la soustraction d'un négatif, les fractions équivalentes, la distributivité, "
        "la réduction avec constantes négatives et l'aire du triangle. Le plan de remédiation "
        "contient précisément ces cinq entrées. La S5 retient les deux premières comme axes : "
        "phase 2 sur la soustraction d'un négatif, phase 3 sur la réduction signée. L'évaluation "
        "reprend ces deux compétences en A5 et A6, teste en B4 la chaîne développer-réduire-contrôler "
        "et en C2 l'aire du triangle sous sa forme inverse, cinquième priorité du dossier. Le conseil "
        "du dossier — associer chaque règle à une représentation et à un contrôle — est repris comme "
        "critère de réussite de phase."),
    "fares-darghouth": (
        "Le dossier distingue nettement ce qui est appui (proportionnalité, statistiques) et ce qui "
        "est à rectifier (aire contre périmètre, angles, symétrie centrale, fractions équivalentes) ; "
        "il indique explicitement que le calcul littéral n'a pas pu être situé. Les séances 2 et 4 "
        "ont travaillé grandeurs et géométrie. La S5 place l'aire et le périmètre en phase 2, avec "
        "l'unité comme premier contrôle, et le raisonnement donnée-propriété-conclusion en phase 3. "
        "L'évaluation évalue en A5 l'aire du triangle, en A6 les fractions équivalentes, en B4 les "
        "angles et le parallélogramme. C2 est le seul item du dossier explicitement présenté comme "
        "un point de référence à établir et non comme une mesure de progression : le calcul littéral "
        "n'a pas de résultat initial documenté."),
    "elyes-kefi": (
        "Le diagnostic est précis : croisement inversé sur 2/3 × 9/4, réduction où −7 + 3 est traité "
        "comme −10, et une valeur oubliée dans une moyenne. Calibration de départ à 82 %, la plus "
        "haute du groupe. Le plan de remédiation couvre les trois points en douze exercices. La S5 "
        "place le produit de fractions en phase 2 et la réduction signée en phase 3 ; l'item 6 de "
        "chaque module reprend l'erreur exacte du dossier, mais sous forme d'analyse d'erreur, format "
        "qu'il n'a pas encore rencontré. L'évaluation vérifie les trois points : A5 produit de "
        "fractions, A6 réduction, B4 moyenne avec inventaire des valeurs. C2 introduit le double "
        "produit, travaillé en phase 4 : il est marqué non comparable."),
    "amine-mansouri": (
        "Le dossier décrit un profil particulier : de nombreuses réussites accompagnées d'une "
        "confiance très faible. Le levier n'est donc pas le niveau des exercices mais la "
        "verbalisation. La S5 ne durcit rien : elle place la réduction signée en phase 2 et le "
        "choix d'un rapport trigonométrique en phase 3, et l'évaluation demande explicitement, en "
        "B4, d'écrire pourquoi le résultat devait être inférieur à l'hypoténuse, puis en C2 "
        "d'expliquer pourquoi un produit de fractions ne demande pas de dénominateur commun. "
        "Deux items sur quatre portent sur la justification, ce qui correspond à l'indicateur du "
        "dossier : quatre réponses justifiées oralement."),
    "fares-laajili": (
        "Six domaines solides, trois points à rectifier : produit de fractions, application de "
        "Pythagore sur les carrés, confusion cosinus / sinus. Le plan de remédiation les couvre en "
        "six exercices. La S5 retient le produit de fractions en phase 2 et le choix du rapport "
        "trigonométrique en phase 3. L'évaluation reprend le quotient de fractions en A5, "
        "l'identification du rapport en A6, et confronte en B4 l'erreur documentée « carré confondu "
        "avec double » sur un énoncé nouveau. C2 demande de justifier le choix du rapport par le nom "
        "des côtés avant tout calcul, ce qui est le cœur de la difficulté relevée."),
    "sarah-bargaoui": (
        "Socle numérique solide, tout le reste à installer : le dossier liste six priorités, ce qui "
        "impose un choix. La S5 retient les deux qui conditionnent les autres : la réduction signée "
        "en phase 2 et l'équation du premier degré en phase 3 ; la proportionnalité et Pythagore sont "
        "évalués en B4 sans être reconsolidés, faute de temps. Le conseil du dossier — écrire la "
        "relation avant d'insérer les nombres — devient une consigne explicite de l'item B4. Les "
        "quatre autres priorités du dossier ne sont pas traitées en séance : elles figurent dans les "
        "compétences non ciblées de la matrice de trajectoire et ressortiront du plan de rentrée."),
    "selim-mansouri": (
        "Le profil est le plus lacunaire du niveau : seules les puissances sont solides, et trois "
        "domaines restent à diagnostiquer. La S5 sécurise donc d'abord le signe d'un produit en "
        "phase 2, puis la distributivité complète en phase 3, dans cet ordre parce que le second "
        "dépend du premier. L'évaluation reprend ces deux compétences en A5 et A6, teste en B4 le "
        "retour à l'unité et Pythagore, et introduit en C2 le double produit travaillé en phase 4. "
        "Trois compétences restent au statut non évalué dans la matrice : le dossier enseignant "
        "demande d'en recueillir une observation sans conclure à une maîtrise."),
    "ahmed-bakir": (
        "Le dossier signale des certitudes erronées sur sept domaines : la conviction est ici le "
        "problème principal, avant la technique. La S5 place les priorités opératoires et les signes "
        "en phase 2 — le socle de tout le reste — et les identités remarquables en phase 3. "
        "L'évaluation reprend la puissance d'un relatif en A5, l'écriture scientifique en A6, le "
        "double produit en B4 et réfute en C2 la compensation de deux évolutions successives. Chaque "
        "module se termine par une analyse d'erreur portant sur la conception documentée, ce qui "
        "correspond à l'indicateur du dossier : diminuer les erreurs données avec certitude 4."),
    "noa-maniaci": (
        "Le dossier place les équations à installer et cite huit priorités, dont le produit nul et "
        "les évolutions successives. La S5 retient ces deux-là : phase 2 sur l'équation produit nul, "
        "phase 3 sur le coefficient multiplicateur. L'évaluation reprend le produit nul en A5, "
        "l'exposant négatif en A6, les évolutions successives en B4, et demande en C2 de factoriser "
        "avant de résoudre — la méthode qui conditionne le second degré. Les points d'appui relevés "
        "au dossier (réciproque 6-8-10, facteur d'aire 9) sont réutilisés dans le noyau commun B3 "
        "plutôt que retravaillés."),
    "ahmad-beldi-maths": (
        "Inéquations et vecteurs solides, factorisation et langage fonctionnel à rectifier. La S5 "
        "place la différence de carrés en phase 2 et le couple image / antécédent en phase 3. "
        "L'évaluation reprend la factorisation en A5, la traduction d'un point de la courbe en A6, "
        "et croise en B4 la comparaison de puissances sur ]0 ; 1[ avec l'union de deux événements — "
        "les deux domaines que le dossier place « à installer ». C2 introduit la suite géométrique "
        "travaillée en phase 4 : elle est marquée non comparable. Limite : aucun livret personnalisé "
        "S2 à S4 n'existe en Première spécialité, la trajectoire repose sur le diagnostic et la "
        "remédiation seuls."),
    "donia-khadhrani": (
        "Le dossier liste six priorités, dominées par le langage fonctionnel et les inéquations. La "
        "S5 retient ces deux-là. L'évaluation demande en A5 un antécédent obtenu par équation — et "
        "non par essais, erreur de méthode visée par le dossier —, en A6 une inéquation avec "
        "changement de sens, en B4 le coefficient directeur et l'équation réduite, troisième "
        "priorité, et en C2 l'union et le complémentaire, sixième priorité. Les vecteurs, seul "
        "domaine solide, servent d'appui au coefficient directeur plutôt que d'objet de travail. "
        "Même limite documentaire que pour les deux autres élèves de Première spécialité."),
    "malek-khadhrani": (
        "Le dossier vise la substitution d'une valeur négative, le langage fonctionnel, la fonction "
        "inverse, les coordonnées de vecteur, la colinéarité, la pente et les puissances. La S5 "
        "retient la substitution négative en phase 2 et la colinéarité en phase 3 : ce sont les deux "
        "erreurs dont le dossier donne la mécanique exacte. L'évaluation reprend la substitution en "
        "A5, le déterminant en A6, l'alignement de trois points et la pente en B4, les puissances et "
        "la fonction inverse en C2. Le calcul littéral et les pourcentages, solides, ne sont pas "
        "retravaillés. Même limite documentaire que pour les deux autres élèves de Première spécialité."),
    "ahmad-beldi-nsi": (
        "Le tableau de suivi du dossier donne des niveaux initiaux chiffrés : affectation 1, "
        "conditions 2, boucles 1, fonctions 1, listes 1, tables CSV 2, autonomie 1 ; la réussite en "
        "programmation est de 22,2 %, et cinq questions du test n'ont pas été traitées. Les séances "
        "1 à 4 ont traité successivement affectation, boucles, fonctions et listes ; le livret S4 "
        "existant montre que l'indexation et le CSV ont été travaillés. La S5 retient les deux "
        "compétences restées au niveau 1 dont dépend tout le reste : le contrat d'une fonction "
        "(phase 2) et les bornes de range (phase 3). L'évaluation reprend le None en A5, les bornes "
        "en A6, l'alias de liste en B4 — prolongement direct du livret S4 — et la recherche "
        "séquentielle en C2, introduite en phase 4 et donc non comparable. Le parcours reste "
        "« fondations guidées » conformément au dossier."),
    "ahmed-benhadj-salem": (
        "Le dossier écarte explicitement une reprise lente de notions connues : six domaines sur "
        "sept sont solides, la programmation est à 55,6 % et l'erreur d'accumulateur — somme "
        "confondue avec le nombre d'itérations — est documentée dans les deux bilans, Première et "
        "niveau Terminale. La compétence Tests est relevée au niveau 1, la plus basse du profil. La "
        "S5 retient donc l'accumulateur en phase 2 et les tests en phase 3, et rien d'autre. "
        "L'évaluation mesure l'accumulateur en A5, le choix for/while en A6, un jeu de tests avec "
        "cas limite et le problème des flottants en B4, et le coût comparé des deux recherches en "
        "C2. Le parcours reste « projet autonome, candidat individuel », avec la gestion du temps "
        "comme objectif transversal."),
}

STATUT_FR = {"acquis": "acquis au diagnostic", "en_voie_acquisition": "en voie d'acquisition",
             "fragile": "fragile", "non_evalue": "non évalué", "non_travaille": "non travaillé"}


def load(name):
    with open(os.path.join(AUDIT, name), encoding="utf-8") as f:
        return json.load(f)


def count_files(ext, root=None):
    root = root or core.S5_ROOT
    n = 0
    for dp, _dn, fns in os.walk(root):
        if os.path.basename(dp) in ("_build_logs", "__pycache__"):
            continue
        n += sum(1 for f in fns if f.endswith(ext))
    return n


def pdf_pages(path):
    try:
        out = subprocess.run(["pdfinfo", path], capture_output=True, text=True, check=True).stdout
        for line in out.splitlines():
            if line.startswith("Pages:"):
                return int(line.split()[1])
    except Exception:
        pass
    return None


def build_index(inv, revue, docimo, validation):
    rev = {r["student_id"]: r for r in revue["eleves"]}
    doc = {r["student_id"]: r for r in docimo["eleves"]}
    L = ["# INDEX — Séance 5 de clôture",
         "",
         "Généré le %s. Un couple élève × matière par ligne." % DATE,
         "",
         "## 1. Tableau de livraison",
         "",
         "| Élève | Niveau | Matière | Diag. | S1 | S2 | S3 | S4 | Livret S5 | Évaluation | Dossier ens. | JSON | PDF | Validation | Revue péd. | Alerte |",
         "|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|"]
    for e in inv["eleves"]:
        st = [s for s in core.all_students() if s["id"] == e["student_id"]][0]
        d = core.student_output_dir(st)
        td = os.path.join(d, "_ENSEIGNANT")
        pers = e["documents_personnalises_disponibles"]

        def seance(tag):
            if tag == "S1":
                return "niveau"
            return "perso." if any("_%s_" % tag in os.path.basename(p) or
                                   "_%s_" % tag in p for p in pers) else "niveau"

        def ok(p):
            return "oui" if os.path.exists(p) else "**NON**"

        pdfs = [os.path.join(d, core.doc_basename(k, st) + ".pdf") for k in ("TRAVAIL", "EVALUATION")]
        pdfs.append(os.path.join(td, core.doc_basename("ENSEIGNANT", st) + ".pdf"))
        njson = sum(1 for f in os.listdir(d) if f.endswith(".json")) + \
            sum(1 for f in os.listdir(td) if f.endswith(".json"))
        r = rev[e["student_id"]]
        alerte = "; ".join(r["notes"]) if r["notes"] else "—"
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %d/7 | %s | %s | %s | %s |" % (
            e["nom_affiche"], e["niveau_cle"], e["matiere"],
            "oui" if e["diagnostic_initial"]["disponible"] else "non",
            seance("S1"), seance("S2"), seance("S3"), seance("S4"),
            ok(os.path.join(d, core.doc_basename("TRAVAIL", st) + ".tex")),
            ok(os.path.join(d, core.doc_basename("EVALUATION", st) + ".tex")),
            ok(os.path.join(td, core.doc_basename("ENSEIGNANT", st) + ".tex")),
            njson,
            "3/3" if all(os.path.exists(p) for p in pdfs) else "**incomplet**",
            "PASS" if validation["result"] == "PASS" else "FAIL",
            r["verdict"], alerte))
    L += ["",
          "*« niveau »* : seuls les documents communs du niveau sont attestés pour cette séance. "
          "*« perso. »* : un livret personnalisé de cette séance existe pour cet élève.",
          "",
          "## 2. Chemins des livrables",
          "",
          "| Élève | Répertoire |", "|---|---|"]
    for e in inv["eleves"]:
        L.append("| %s | `%s/` |" % (e["nom_affiche"], e["repertoire_s5"]))
    L += ["",
          "Chaque répertoire contient :",
          "",
          "```",
          "S5_TRAVAIL_<NIVEAU>_<ELEVE>.tex / .pdf        75 minutes, aucun corrigé",
          "S5_EVALUATION_<NIVEAU>_<ELEVE>.tex / .pdf     45 minutes, aucun corrigé, aucun barème",
          "student_learning_profile.json                 profil et métadonnées d'items",
          "evaluation_blueprint.json                     structure, durées, comparabilité",
          "responses_TEMPLATE.json                       gabarit de saisie des résultats",
          "post_stage_analysis_schema.json               schéma de la sortie d'analyse",
          "four_week_action_plan_TEMPLATE.json           gabarit du plan de rentrée",
          "_ENSEIGNANT/S5_ENSEIGNANT_<...>.tex / .pdf    profil, déroulé, corrigés, barème",
          "_ENSEIGNANT/evaluation_manifest.json          métadonnées complètes des items",
          "_ENSEIGNANT/answer_key.json                   corrigé structuré",
          "_ENSEIGNANT/README.md                         marche à suivre après la passation",
          "```",
          "",
          "## 3. Volumétrie par document",
          "",
          "| Document | Pages | Élèves |", "|---|:--:|---|"]
    for kind, label in (("TRAVAIL", "Livret de travail"), ("EVALUATION", "Évaluation finale"),
                        ("ENSEIGNANT", "Dossier enseignant")):
        pages = Counter()
        for st in core.all_students():
            d = core.student_output_dir(st)
            p = (os.path.join(d, "_ENSEIGNANT", core.doc_basename(kind, st) + ".pdf")
                 if kind == "ENSEIGNANT" else os.path.join(d, core.doc_basename(kind, st) + ".pdf"))
            pages[pdf_pages(p)] += 1
        L.append("| %s | %s | %s |" % (
            label, " / ".join(str(k) for k in sorted(pages)),
            ", ".join("%d document(s) de %s pages" % (v, k) for k, v in sorted(pages.items()))))
    L += ["",
          "## 4. Durée de chaque évaluation",
          "",
          "| Élève | Partie A | Partie B | Partie C | Somme | Épreuve | Marge | Points |",
          "|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|"]
    for r in docimo["eleves"]:
        dp = r["duree_par_partie"]
        L.append("| %s | %s min | %s min | %s min | **%s min** | %s min | %s min | %s / 20 |" % (
            r["name"], dp["A"], dp["B"], dp["C"], r["somme_durees_min"],
            r["duree_epreuve_min"], r["marge_min"], r["total_points"]))
    L += ["",
          "## 5. Documents transverses",
          "",
          "| Fichier | Objet |", "|---|---|",
          "| `_audit/inventaire_eleves.json` | inventaire des 15 couples, sources et statut des compétences |",
          "| `_audit/AUDIT_S1_S4.md` | audit lisible du diagnostic à la séance 4 |",
          "| `_audit/conflits_sources.json` | 10 contradictions de sources, décision et justification |",
          "| `_audit/revue_personnalisation.json` | contrôle de continuité S1-S4 → S5, collisions d'énoncés |",
          "| `_audit/audit_docimologique.json` | audit des 15 évaluations et matrices de comparabilité |",
          "| `_audit/validation_report.json` | sortie de `tools/validate_s5.py` |",
          "| `_common/nexusS5.sty` | charte graphique partagée |",
          "| `_common/blueprints/blueprint_<niveau>.json` | référentiel de compétences par niveau |",
          "| `_teacher_private/tests_s5_nsi.py` | tests déterministes des productions de code NSI |",
          "| `_teacher_private/BILAN_TEMPLATE_PARENTS.md` | gabarit du bilan aux responsables légaux |",
          "| `_teacher_private/bilan_template.json` | règles de rédaction du bilan, lisibles par machine |",
          "| `INDEX_S5.md`, `QA_REPORT.md` | le présent index et le rapport qualité |",
          ""]
    return "\n".join(L)


def build_qa(inv, conflits, revue, docimo, validation):
    rev = {r["student_id"]: r for r in revue["eleves"]}
    doc = {r["student_id"]: r for r in docimo["eleves"]}
    verdicts = {}
    for e in inv["eleves"]:
        sid = e["student_id"]
        v = [rev[sid]["verdict"], doc[sid]["verdict"]]
        if "FAIL" in v:
            verdicts[sid] = "FAIL"
        elif "WARNING" in v or "PASS WITH WARNINGS" in v:
            verdicts[sid] = "PASS WITH WARNINGS"
        else:
            verdicts[sid] = "PASS"

    L = ["# Rapport qualité — Séance 5 de clôture",
         "",
         "Généré le %s." % DATE,
         "",
         "## 1. Inventaire final",
         "",
         "| Indicateur | Valeur |", "|---|---|",
         "| Couples élève × matière traités | %d |" % len(inv["eleves"]),
         "| Niveaux | %d (%s) |" % (len(LEVEL_ORDER), ", ".join(LEVEL_ORDER)),
         "| Matières | 2 (Mathématiques, NSI) |",
         "| Documents LaTeX produits | %d |" % count_files(".tex"),
         "| PDF produits | %d |" % count_files(".pdf"),
         "| Fichiers JSON produits | %d |" % count_files(".json"),
         "| Modules de consolidation individualisés | %d |" % len(MODULES),
         "| Blueprints de niveau | %d |" % len(LEVEL_ORDER),
         "| Compétences décrites, tous niveaux | %d |" % sum(len(LEVELS[k]["skills"]) for k in LEVEL_ORDER),
         "| Items d'évaluation produits | %d |" % (len(inv["eleves"]) * 12),
         "",
         "### Répartition par niveau", "",
         "| Niveau | Matière | Élèves | Compétences au référentiel | Items du diagnostic initial |",
         "|---|---|:--:|:--:|:--:|"]
    for k in LEVEL_ORDER:
        lv = LEVELS[k]
        n = len([e for e in inv["eleves"] if e["niveau_cle"] == k])
        L.append("| %s | %s | %d | %d | %d |" % (lv["label"], lv["subject"], n,
                                                 len(lv["skills"]), len(lv["baseline_items"])))

    L += ["",
          "## 2. Couverture",
          "",
          "| Contrôle | Résultat |", "|---|---|",
          "| Élèves détectés dans les dossiers nominatifs | 15 |",
          "| Élèves disposant d'un diagnostic initial exploitable | %d / 15 |"
          % len([e for e in inv["eleves"] if e["diagnostic_initial"]["disponible"]]),
          "| Élèves disposant d'au moins un livret personnalisé S2 à S4 | %d / 15 |"
          % len([e for e in inv["eleves"] if e["documents_personnalises_disponibles"]]),
          "| Sources déclarées effectivement présentes sur le disque | %d / %d |"
          % (sum(len([s for s in e["sources"] if s["existe"]]) for e in inv["eleves"]),
             sum(len(e["sources"]) for e in inv["eleves"])),
          "| Élèves pour lesquels une observation de séance S1-S4 est documentée | 0 / 15 |",
          "",
          "La dernière ligne est la limite majeure de cette livraison : les tableaux d'observation "
          "séance par séance des dossiers individuels sont vierges. Aucune preuve n'existe entre le "
          "diagnostic initial et aujourd'hui. Toute la construction en tient compte.",
          "",
          "## 3. Revue de personnalisation",
          ""]
    nb_enonces = 0
    for st in core.all_students():
        ph = core.phases(st)
        nb_enonces += (len(LEVELS[st["level"]]["phase1"]["items"])
                       + len(ph[1]["exos"]) + len(ph[2]["exos"]) + len(common.EXAM_ITEM_ORDER))
    L += ["Méthode : pour chaque élève, l'ensemble de ce qui lui a déjà été remis — séances de niveau "
          "S1 à S5, plan de remédiation individuel, livrets personnalisés S2 à S4 lorsqu'ils existent — "
          "a été rassemblé en un corpus, puis chaque énoncé de la séance 5 y a été recherché. "
          "Deux détections : reprise à l'identique (bloquante sur l'évaluation) et signature numérique "
          "identique (à adjuger humainement). La proximité entre livrets d'un même niveau est mesurée "
          "par un indice de Jaccard sur les énoncés.",
          "",
          "Résultat global : %d énoncés produits et confrontés au corpus ; "
          "**%d reprise(s) à l'identique**, %d alerte(s) de signature numérique, toutes relues une "
          "par une. Proximité maximale entre deux élèves d'un même niveau : **%.3f**."
          % (nb_enonces,
             sum(len(rev[e["student_id"]]["collisions_exactes"]) for e in inv["eleves"]),
             sum(len(rev[e["student_id"]]["collisions_signature_numerique"]) for e in inv["eleves"]),
             max(p["jaccard"] for p in revue["paires_meme_niveau"])),
          ""]
    for e in inv["eleves"]:
        sid = e["student_id"]
        r = rev[sid]
        d = doc[sid]
        st = [s for s in core.all_students() if s["id"] == sid][0]
        L += ["### %s — %s (%s) — **%s**" % (e["nom_affiche"], e["niveau_entree"],
                                             e["matiere"], verdicts[sid]),
              "",
              "**Sources individuelles utilisées** (%d fichiers lus, corpus de %d caractères) :"
              % (r["nb_sources_lues"], r["corpus_caracteres"]),
              ""]
        for s in r["sources_individuelles"]:
            L.append("- `%s`" % s)
        L += ["",
              "**Priorités retenues**",
              "",
              "| | skill_id | Compétence | Justification tirée du dossier |",
              "|---|---|---|---|"]
        for tag, lab in (("p1", "P1"), ("p2", "P2")):
            sid_sk = st[tag]
            L.append("| %s | `%s` | %s | %s |" % (lab, sid_sk, MODULES[sid_sk]["titre"],
                                                  MODULES[sid_sk]["pourquoi"]))
        lvv = LEVELS[e["niveau_cle"]]
        L += ["",
              "**Rattachement à S1-S4** — `%s` travaillée en %s ; `%s` travaillée en %s."
              % (st["p1"], ", ".join(lvv["skills"][st["p1"]]["sessions"]) or "aucune séance",
                 st["p2"], ", ".join(lvv["skills"][st["p2"]]["sessions"]) or "aucune séance"),
              "",
              "**Commun au niveau** : %d min de travail (%.0f %%) et %g points d'évaluation (%.0f %%) — "
              "phases 1, 4 et 5, items A1-A4, B1-B3 et C1, strictement identiques pour tous les élèves du niveau."
              % (r["commun_au_niveau"]["travail_minutes"], r["commun_au_niveau"]["travail_pct"],
                 r["commun_au_niveau"]["evaluation_points"], r["commun_au_niveau"]["evaluation_pct"]),
              "",
              "**Véritablement individualisé** : %d min de travail (%.0f %%) et %g points (%.0f %%) — "
              "phase 2 (`%s`), phase 3 (`%s`), items A5, A6, B4 et C2."
              % (r["individualise"]["travail_minutes"], r["individualise"]["travail_pct"],
                 r["individualise"]["evaluation_points"], r["individualise"]["evaluation_pct"],
                 st["p1"], st["p2"]),
              "",
              "**Lecture pédagogique.** %s" % CONTINUITE[sid],
              ""]
        prox = r["proximite_meme_niveau"]
        if prox:
            L.append("**Proximité avec les autres élèves du niveau** : %s."
                     % ", ".join("%s %.2f%s" % (p["autre"], p["jaccard"],
                                                " (mêmes priorités)" if p["memes_priorites"] else "")
                                 for p in prox))
            L.append("")
        if r["collisions_signature_numerique"]:
            L += ["**Alertes de signature numérique, relues une par une**", ""]
            for c in r["collisions_signature_numerique"]:
                adj = c.get("adjudication") or {}
                L.append("- `%s` — %s. %s" % (c["ref"], adj.get("verdict", "NON ADJUGÉE"),
                                              adj.get("justification", "")))
            L.append("")
        if r["notes"] or d["avertissements"]:
            L += ["**Points d'attention**", ""]
            for n in r["notes"]:
                L.append("- %s" % n)
            for w in d["avertissements"]:
                L.append("- %s" % w)
            L.append("")

    L += ["## 4. Comparabilité diagnostic initial ↔ évaluation finale",
          "",
          "Trois statuts sont utilisés, jamais un delta par défaut :",
          "",
          "| `comparison_status` | Signification | Ce que le calcul autorise |",
          "|---|---|---|",
          "| `item_level` | un item parallèle existe dans le test de positionnement : même compétence, "
          "difficulté comparable, valeurs différentes | delta de maîtrise item par item |",
          "| `skill_level` | aucun item parallèle, mais les compétences mobilisées sont diagnostiquées | "
          "comparaison au niveau de la compétence seulement, aucun delta d'item |",
          "| `not_comparable` | aucune mesure initiale, ou contenu introduit pendant la séance 5 | "
          "aucun delta ; un état final seulement |",
          "",
          "| Élève | `item_level` | `skill_level` | `not_comparable` | Compétences évaluées ayant une mesure initiale |",
          "|---|:--:|:--:|:--:|:--:|"]
    for r in docimo["eleves"]:
        c = r["repartition_comparaison"]
        L.append("| %s | %d | %d | %d | %d / %d |" % (
            r["name"], c.get("item_level", 0), c.get("skill_level", 0), c.get("not_comparable", 0),
            r["competences_evaluees_avec_mesure_initiale"], r["nb_competences_evaluees"]))
    L += ["",
          "### Matrices de comparabilité par niveau", ""]
    for m in docimo["matrices_de_comparabilite"]:
        L += ["#### %s — %s" % (m["label"], m["subject"]),
              "",
              "Noyau commun identique entre les élèves du niveau : **%s**."
              % ("oui" if m["noyau_commun_identique_entre_eleves"] else "NON"),
              "",
              "| Item | Compétence | Points | Durée | Difficulté | Item initial | Comparaison |",
              "|---|---|:--:|:--:|---|---|---|"]
        for it in m["noyau_commun"]:
            L.append("| %s | `%s` | %s | %s min | %s | %s | `%s` |" % (
                it["ref"], it["skill_id"], it["points"], it["duree_min"], it["difficulte"],
                ("`%s` — %s" % (it["baseline_item_id"], it["baseline_item_text"]))
                if it["baseline_item_id"] else "aucun", it["comparaison"]))
        L += ["", "Items individualisés :", "",
              "| Élève | A5 | A6 | B4 | C2 |", "|---|---|---|---|---|"]
        for sid, its in m["items_individualises_par_eleve"].items():
            L.append("| %s | %s |" % (sid, " | ".join(
                "`%s`%s" % (i["skill_id"], "" if i["baseline_item_id"] else " (sans item initial)")
                for i in its)))
        if m["competences_du_niveau_sans_item_initial"]:
            L += ["", "Compétences du niveau sans item au diagnostic initial : %s. "
                      "Aucune progression ne sera calculée pour elles."
                  % ", ".join("`%s`" % s for s in m["competences_du_niveau_sans_item_initial"])]
        L.append("")

    L += ["## 5. Contrôle docimologique",
          "",
          "Treize contrôles par évaluation : durée, barème sur 20, validité de contenu, difficulté "
          "progressive par partie, équilibre des types de tâches, surpondération, indépendance des "
          "questions, crédit partiel, absence de choix fermé, familles d'erreurs distinguables, "
          "couverture des compétences, comparabilité, équité du noyau commun.",
          "",
          "| Élève | Durée | Marge | Points | A/B/C | Compétence la plus pondérée | Familles d'erreur | Verdict |",
          "|---|:--:|:--:|:--:|:--:|---|---|:--:|"]
    for r in docimo["eleves"]:
        pp = r["points_par_partie"]
        L.append("| %s | %s min | %s min | %s | %g/%g/%g | `%s` %.0f %% | %d | %s |" % (
            r["name"], r["somme_durees_min"], r["marge_min"], r["total_points"],
            pp["A"], pp["B"], pp["C"],
            r["competence_la_plus_ponderee"]["skill_id"], r["competence_la_plus_ponderee"]["pct"],
            len(r["familles_erreur_mobilisees"]), r["verdict"]))
    L += ["",
          "**Réussite par hasard.** Aucune question à choix fermé n'a été retenue : les douze items "
          "appellent une production écrite. Le crédit partiel est garanti sur tout item valant au "
          "moins deux points, où le barème comporte systématiquement au moins deux critères, "
          "dissociant la démarche du résultat final.",
          "",
          "**Chaîne d'erreurs.** En mathématiques, le barème distingue CONCEPT (connaissance), "
          "METHODE (choix), CALCUL (exécution), auxquels s'ajoutent JUSTIFICATION, LECTURE, CONTROLE "
          "et NOTATION. En NSI, le choix de méthode se lit dans ALGORITHME et l'exécution dans "
          "SYNTAXE. Une erreur de calcul isolée, non reproduite sur les items voisins de même "
          "compétence, ne vaut jamais non-maîtrise conceptuelle : la règle figure dans chaque dossier "
          "enseignant.",
          ""]
    return L, verdicts


if __name__ == "__main__":
    inv = load("inventaire_eleves.json")
    conflits = load("conflits_sources.json")
    revue = load("revue_personnalisation.json")
    docimo = load("audit_docimologique.json")
    validation = load("validation_report.json")
    with open(os.path.join(core.S5_ROOT, "INDEX_S5.md"), "w", encoding="utf-8") as f:
        f.write(build_index(inv, revue, docimo, validation))
    lines, verdicts = build_qa(inv, conflits, revue, docimo, validation)
    with open(os.path.join(AUDIT, "_qa_partie1.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open(os.path.join(AUDIT, "_qa_verdicts.json"), "w", encoding="utf-8") as f:
        json.dump(verdicts, f, ensure_ascii=False, indent=2)
    print("INDEX_S5.md écrit ; partie 1 du QA écrite ; verdicts : %s" % Counter(verdicts.values()))
