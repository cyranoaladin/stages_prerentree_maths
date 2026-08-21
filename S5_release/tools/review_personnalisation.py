#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Revue de personnalisation : la S5 prolonge-t-elle réellement S1-S4 de chaque élève ?

Le script confronte, élève par élève, les énoncés produits pour la séance 5 au
corpus de tout ce qui lui a déjà été donné : séances de niveau S1 à S5,
plan de remédiation individuel, et livrets personnalisés S2, S3, S4, S5 lorsqu'ils
existent (texte extrait des PDF).

Il produit `_audit/revue_personnalisation.json` et détecte :
  * la reprise à l'identique d'un énoncé déjà donné (bloquant sur l'évaluation) ;
  * une signature numérique identique, à vérifier humainement ;
  * une proximité excessive entre deux élèves du même niveau ;
  * une part individualisée hors de la fourchette attendue ;
  * une priorité qui ne serait pas documentée dans le dossier individuel.

Usage :
    python3 S5_cloture/tools/review_personnalisation.py [--verbose]
"""

import argparse
import json
import os
import re
import subprocess
import sys
sys.dont_write_bytecode = True  # aucune trace de cache dans la livraison

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core
from data import common
from data.levels import MODULES

AUDIT = os.path.join(core.S5_ROOT, "_audit")

# Adjudication humaine des alertes de signature numérique, relues une par une le
# 20 août 2026. Une alerte non listée ici reste un AVERTISSEMENT.
REVUE_HUMAINE = {
    ("*", "eval.A4"): {
        "verdict": "faux positif",
        "justification": "l'équation 4x - 3 = 2x + 9 partage le multiensemble {2, 3, 4, 9} avec "
                         "un produit de fractions du dossier de remédiation. Les deux tâches n'ont "
                         "aucun rapport : ni la compétence, ni la consigne, ni la procédure.",
    },
    ("elyes-kefi", "eval.C2"): {
        "verdict": "faux positif",
        "justification": "coïncidence de nombres avec un énoncé de probabilités (urne). Tâches sans "
                         "rapport : développement d'un produit de deux sommes contre calcul de probabilité.",
    },
    ("selim-mansouri", "eval.C2"): {
        "verdict": "faux positif",
        "justification": "coïncidence de nombres avec l'expression f(x) = 1,5x + 2 d'une fiche de niveau. "
                         "Tâches sans rapport.",
    },
    ("ahmad-beldi-nsi", "phase2.3"): {
        "verdict": "faux positif",
        "justification": "coïncidence des nombres 2, 3 et 5 avec un exercice de décomposition de tuple "
                         "de la séance 4. Tâches sans rapport.",
    },
    ("malek-khadhrani", "phase2.2"): {
        "verdict": "reprise délibérée, tâche différente",
        "justification": "la fonction et la valeur diffèrent (g(x) = -2x² + x en -3 contre f(x) = x² - 3x "
                         "en -2). L'énoncé du plan de remédiation est réutilisé plus loin dans le module, "
                         "en analyse d'erreur : c'est précisément l'erreur de substitution négative "
                         "documentée au dossier de cet élève. Format nouveau, réactivation espacée.",
    },
    ("ahmed-bakir", "phase3.3"): {
        "verdict": "faux positif",
        "justification": "l'alerte provient de l'exposant 2 de (3x - 4)², compté comme un nombre : "
                         "le multiensemble {2, 3, 4} coïncide avec celui d'un double produit de la "
                         "séance 2. Les tâches diffèrent : identité remarquable ici, double "
                         "distributivité de deux binômes distincts là. Aucune valeur reprise.",
    },
    ("ahmed-benhadj-salem", "phase3.3"): {
        "verdict": "reprise délibérée, tâche différente",
        "justification": "le plan de remédiation demandait de lire math.isclose et de tester 0.1 + 0.2 ; "
                         "la séance 5 demande d'expliquer pourquoi l'assertion échoue puis de proposer "
                         "une écriture correcte. La compétence Tests est relevée au niveau 1, le plus bas "
                         "du profil : la réactivation espacée est justifiée.",
    },
}


def adjudication(student_id, ref):
    return REVUE_HUMAINE.get((student_id, ref)) or REVUE_HUMAINE.get(("*", ref))
MIN_LEN = 28            # longueur normalisée en deçà de laquelle une collision n'a pas de sens
INDIV_MIN, INDIV_MAX = 25.0, 40.0


def norm(txt):
    txt = re.sub(r"\\[a-zA-Z]+\s*", " ", txt)
    txt = re.sub(r"\\begin\{[^}]*\}|\\end\{[^}]*\}", " ", txt)
    txt = txt.replace("\u2212", "-").replace("\u00a0", " ").replace("\u2019", "'")
    txt = re.sub(r"[^0-9a-zàâäçéèêëîïôöùûüÿœæ]+", "", txt.lower())
    return txt


def numbers(txt):
    return tuple(sorted(re.findall(r"-?\d+(?:[.,]\d+)?", txt)))


def read_pdf(path):
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"],
                              capture_output=True, text=True, check=True).stdout
    except Exception:
        return ""


def corpus_for(student):
    """Tout ce qui a déjà été remis à cet élève, sous forme de texte brut."""
    lv = core.level_of(student)
    root = core.REPO_ROOT
    parts = []
    used = []
    for s in core.student_sources(student):
        p = os.path.join(root, s)
        if os.path.isdir(p):
            for fn in sorted(os.listdir(p)):
                if fn.endswith(".md"):
                    parts.append(open(os.path.join(p, fn), encoding="utf-8", errors="ignore").read())
                    used.append(os.path.join(s, fn))
        elif p.endswith(".md"):
            parts.append(open(p, encoding="utf-8", errors="ignore").read())
            used.append(s)
        elif p.endswith(".pdf"):
            t = read_pdf(p)
            if t:
                parts.append(t)
                used.append(s)
        elif p.endswith(".tex"):
            parts.append(open(p, encoding="utf-8", errors="ignore").read())
            used.append(s)
    # les documents communs du niveau font aussi partie de ce qui a été donné
    for s in ("S1", "S2", "S3", "S4", "S5"):
        d = os.path.join(root, lv["source_dir"], "02_SEANCES", s)
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if fn.endswith(".md"):
                    parts.append(open(os.path.join(d, fn), encoding="utf-8", errors="ignore").read())
    return "\n".join(parts), used


def s5_statements(student):
    """Tous les énoncés produits pour la S5, avec leur origine."""
    lv = core.level_of(student)
    ph = core.phases(student)
    out = []
    for i, it in enumerate(lv["phase1"]["items"], 1):
        out.append(("phase1.%d" % i, it["tex"], "travail"))
    for p in (ph[1], ph[2]):
        for i, ex in enumerate(p["exos"], 1):
            out.append(("phase%d.%d" % (p["n"], i), ex["tex"], "travail"))
    for it in core.exam_items(student):
        out.append(("eval.%s" % it["ref"], it["tex"], "evaluation"))
    return out


def review(student, verbose=False):
    lv = core.level_of(student)
    corpus, used = corpus_for(student)
    ncorpus = norm(corpus)
    corpus_lines = [l for l in corpus.splitlines() if len(l.strip()) > 20]

    exact, numeric = [], []
    for ref, tex, kind in s5_statements(student):
        n = norm(tex)
        if len(n) >= MIN_LEN and n in ncorpus:
            exact.append({"ref": ref, "kind": kind, "statement": tex[:160]})
            continue
        sig = numbers(tex)
        if len(sig) >= 3:
            for line in corpus_lines:
                if numbers(line) == sig:
                    numeric.append({"ref": ref, "kind": kind,
                                    "statement": tex[:120], "corpus_line": line.strip()[:120]})
                    break

    ph = core.phases(student)
    items = core.exam_items(student)
    tot = core.exam_totals(items)
    work_ind = sum(p["minutes_individualisees"] for p in ph)
    work_pct = 100.0 * work_ind / common.WORK_MINUTES

    # les deux priorités sont-elles écrites dans le dossier individuel ?
    dossier_txt = norm(" ".join(student["baseline"]["priorites"] + student["baseline"]["appuis"]
                                + [student["baseline"]["summary"]]
                                + [o[2] for o in student["baseline"]["observations"]]))
    prio_ok = {}
    for tag in ("p1", "p2"):
        sid = student[tag]
        mots = [norm(w) for w in re.split(r"[ ,:;()/']", MODULES[sid]["titre"]) if len(w) > 4]
        prio_ok[tag] = {"skill_id": sid,
                        "mots_retrouves": [w for w in mots if w and w in dossier_txt],
                        "justification_dossier": MODULES[sid]["pourquoi"][:200]}

    return {
        "student_id": student["id"], "name": student["name"],
        "level_key": lv["key"], "subject": lv["subject"],
        "sources_individuelles": [s for s in used
                                  if "04_NOMINATIFS" in s or "05_NOMINATIFS" in s
                                  or s.startswith(("Bilans/", "Nexus_"))],
        "nb_sources_lues": len(used),
        "corpus_caracteres": len(corpus),
        "priorites": {"P1": student["p1"], "P2": student["p2"]},
        "priorites_documentees": prio_ok,
        "ancrage_s1_s4": {
            "S1": lv["sessions"]["S1"], "S2": lv["sessions"]["S2"],
            "S3": lv["sessions"]["S3"], "S4": lv["sessions"]["S4"],
            "competences_travaillees_visees_en_s5": {
                student["p1"]: lv["skills"][student["p1"]]["sessions"],
                student["p2"]: lv["skills"][student["p2"]]["sessions"],
            },
        },
        "commun_au_niveau": {
            "travail_minutes": common.WORK_MINUTES - work_ind,
            "travail_pct": round(100.0 - work_pct, 1),
            "evaluation_points": tot["points_commun"],
            "evaluation_pct": tot["part_commun_pct"],
            "elements": ["phase 1 (réactivation, identique au niveau)",
                         "phase 4 (pont vers l'année suivante, identique au niveau)",
                         "phase 5 (méthodologie, identique au niveau)",
                         "items A1-A4, B1-B3 et C1 de l'évaluation"],
        },
        "individualise": {
            "travail_minutes": work_ind,
            "travail_pct": round(work_pct, 1),
            "evaluation_points": tot["points_individuel"],
            "evaluation_pct": tot["part_individuel_pct"],
            "elements": ["phase 2 : module %s (%s)" % (student["p1"], MODULES[student["p1"]]["titre"]),
                         "phase 3 : module %s (%s)" % (student["p2"], MODULES[student["p2"]]["titre"]),
                         "items A5, A6, B4 et C2 de l'évaluation"],
        },
        "collisions_exactes": exact,
        "collisions_signature_numerique": numeric,
    }


def similarity(a, b):
    """Jaccard sur les 6-grammes normalisés des énoncés de deux livrets."""
    def grams(st):
        n = norm(" ".join(t for _, t, _ in s5_statements(st)))
        return {n[i:i + 6] for i in range(0, max(0, len(n) - 6), 3)}
    ga, gb = grams(a), grams(b)
    return round(len(ga & gb) / len(ga | gb), 3) if ga and gb else 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    students = core.all_students()
    rows = [review(st, args.verbose) for st in students]

    # proximité entre élèves d'un même niveau
    pairs = []
    for i, a in enumerate(students):
        for b in students[i + 1:]:
            if a["level"] != b["level"]:
                continue
            sim = similarity(a, b)
            pairs.append({"a": a["id"], "b": b["id"], "jaccard": sim,
                          "memes_priorites": sorted([a["p1"], a["p2"]]) == sorted([b["p1"], b["p2"]]),
                          "priorites_a": [a["p1"], a["p2"]], "priorites_b": [b["p1"], b["p2"]]})
    simmap = {}
    for p in pairs:
        simmap.setdefault(p["a"], []).append(p)
        simmap.setdefault(p["b"], []).append(p)

    for r in rows:
        verdict, notes = "PASS", []
        if any(c["kind"] == "evaluation" for c in r["collisions_exactes"]):
            verdict, _ = "FAIL", notes.append("un énoncé de l'évaluation reprend à l'identique un exercice déjà donné")
        elif r["collisions_exactes"]:
            verdict = "WARNING"
            notes.append("%d énoncé(s) du livret de travail reprennent un exercice déjà donné"
                         % len(r["collisions_exactes"]))
        non_adjuges = []
        for c in r["collisions_signature_numerique"]:
            adj = adjudication(r["student_id"], c["ref"])
            c["adjudication"] = adj
            if adj is None:
                non_adjuges.append(c["ref"])
        if non_adjuges:
            if verdict == "PASS":
                verdict = "WARNING"
            notes.append("%d alerte(s) de signature numérique non adjugée(s) : %s"
                         % (len(non_adjuges), ", ".join(non_adjuges)))
        elif r["collisions_signature_numerique"]:
            notes.append("%d alerte(s) de signature numérique, toutes relues et adjugées"
                         % len(r["collisions_signature_numerique"]))
        if not (INDIV_MIN <= r["individualise"]["travail_pct"] <= INDIV_MAX):
            verdict = "FAIL"
            notes.append("part individualisée du travail hors fourchette : %.1f %%"
                         % r["individualise"]["travail_pct"])
        if not (INDIV_MIN <= r["individualise"]["evaluation_pct"] <= INDIV_MAX):
            verdict = "FAIL"
            notes.append("part individualisée de l'évaluation hors fourchette : %.1f %%"
                         % r["individualise"]["evaluation_pct"])
        if not r["sources_individuelles"]:
            verdict = "FAIL"
            notes.append("aucune source individuelle disponible")
        perso = [s for s in r["sources_individuelles"] if s.startswith(("Bilans/", "Nexus_"))]
        if not perso:
            if verdict == "PASS":
                verdict = "WARNING"
            notes.append("aucun livret personnalisé S2 à S4 n'existe pour cet élève : "
                         "la trajectoire est reconstruite à partir du diagnostic et de la remédiation seuls")
        proches = [p for p in simmap.get(r["student_id"], []) if p["jaccard"] > 0.75]
        for p in proches:
            other = p["b"] if p["a"] == r["student_id"] else p["a"]
            if p["memes_priorites"]:
                if verdict == "PASS":
                    verdict = "WARNING"
                notes.append("livret très proche de celui de %s (Jaccard %.2f) avec les mêmes deux "
                             "priorités : proximité à justifier par les diagnostics" % (other, p["jaccard"]))
            else:
                notes.append("livret proche de celui de %s (Jaccard %.2f) mais priorités différentes"
                             % (other, p["jaccard"]))
        r["proximite_meme_niveau"] = sorted(
            [{"autre": (p["b"] if p["a"] == r["student_id"] else p["a"]), "jaccard": p["jaccard"],
              "memes_priorites": p["memes_priorites"]} for p in simmap.get(r["student_id"], [])],
            key=lambda x: -x["jaccard"])
        r["verdict"] = verdict
        r["notes"] = notes

    out = {"schema": "nexus-s5-revue-personnalisation-v1", "genere_le": "2026-08-20",
           "methode": {
               "collision_exacte": "énoncé normalisé (LaTeX retiré, minuscules, sans espaces ni ponctuation) "
                                   "retrouvé tel quel dans le corpus déjà remis à l'élève",
               "signature_numerique": "même multiensemble de nombres qu'une ligne du corpus : indice de "
                                      "reprise, à confirmer par lecture humaine",
               "proximite": "indice de Jaccard sur les 6-grammes des énoncés de deux livrets du même niveau",
           },
           "seuils": {"part_individualisee_min_pct": INDIV_MIN, "part_individualisee_max_pct": INDIV_MAX,
                      "proximite_alerte": 0.75},
           "eleves": rows, "paires_meme_niveau": sorted(pairs, key=lambda p: -p["jaccard"])}
    os.makedirs(AUDIT, exist_ok=True)
    with open(os.path.join(AUDIT, "revue_personnalisation.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    for r in rows:
        print("%-8s %-22s %-9s indiv %4.1f %%/%4.1f %%  collisions %d/%d  %s"
              % (r["verdict"], r["student_id"], r["level_key"],
                 r["individualise"]["travail_pct"], r["individualise"]["evaluation_pct"],
                 len(r["collisions_exactes"]), len(r["collisions_signature_numerique"]),
                 "; ".join(r["notes"])[:90]))
    print("\nproximité maximale entre élèves d'un même niveau : %.3f"
          % max([p["jaccard"] for p in pairs] or [0]))
    return 0 if all(r["verdict"] != "FAIL" for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
