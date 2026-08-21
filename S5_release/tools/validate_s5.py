#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validation de la livraison S5.

Exécute des contrôles bloquants (ERREUR) et non bloquants (AVERTISSEMENT) sur
l'ensemble de S5_cloture, puis retourne :

    0  si aucun contrôle critique n'échoue
    1  si au moins un contrôle critique échoue

Usage :
    python3 S5_cloture/tools/validate_s5.py
    python3 S5_cloture/tools/validate_s5.py --json rapport.json
    python3 S5_cloture/tools/validate_s5.py --quiet
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
from data import criteria_map
from data.levels import LEVELS

STUDENT_JSON = ["student_learning_profile.json", "evaluation_blueprint.json",
                "responses_TEMPLATE.json", "post_stage_analysis_schema.json",
                "four_week_action_plan_TEMPLATE.json"]
TEACHER_JSON = ["evaluation_manifest.json", "answer_key.json"]

# Marqueurs qui ne doivent jamais apparaître dans un document remis à l'élève.
FORBIDDEN_IN_STUDENT = [
    "Réponse attendue", "Barème", "Corrigé de", "Corrigé :", "CORRIGÉ",
    "Critère de correction", "Erreurs probables", "Étapes significatives",
    "usage enseignant", "CONFIDENTIEL", "answer_key", "expected_answer",
    "skill_id", "grading_criteria", "baseline_item",
]

ERRORS = []
WARNINGS = []
CHECKS = []


def check(ok, label, detail="", critical=True):
    CHECKS.append({"label": label, "ok": bool(ok), "detail": detail,
                   "critical": critical})
    if not ok:
        (ERRORS if critical else WARNINGS).append("%s — %s" % (label, detail))
    return bool(ok)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def norm_tex(txt):
    """Normalise un fragment LaTeX pour une comparaison de contenu."""
    txt = re.sub(r"\\[a-zA-Z]+\s*", " ", txt)
    txt = re.sub(r"[${}\\~^_&%#\[\]]", " ", txt)
    txt = txt.replace("\u2212", "-").replace("\u00a0", " ")
    return re.sub(r"\s+", "", txt).lower()


def pdf_text(path):
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"],
                              capture_output=True, text=True, check=True).stdout
    except Exception as exc:  # pragma: no cover - dépend de l'environnement
        WARNINGS.append("pdftotext indisponible pour %s (%s)" % (path, exc))
        return ""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", metavar="FICHIER", help="écrit le rapport détaillé en JSON")
    ap.add_argument("--quiet", action="store_true", help="n'affiche que la conclusion")
    ap.add_argument("--skip-pdf", action="store_true",
                    help="saute les contrôles qui lisent le contenu des PDF")
    args = ap.parse_args()

    students = core.all_students()
    root = core.S5_ROOT

    # ---------------------------------------------------------------- 1. périmètre
    check(len(students) == 15, "périmètre", "%d couples élève x matière détectés (15 attendus)" % len(students))

    tex_files = sorted(f for f in _walk(root, ".tex"))
    pdf_files = sorted(f for f in _walk(root, ".pdf"))
    check(len(tex_files) == 45, "nombre de fichiers .tex", "%d trouvés, 45 attendus" % len(tex_files))
    check(len(pdf_files) == 45, "nombre de fichiers .pdf", "%d trouvés, 45 attendus" % len(pdf_files))

    # ------------------------------------------------------ 2. audit et blueprints
    for rel in ("_audit/inventaire_eleves.json", "_audit/AUDIT_S1_S4.md",
                "_audit/conflits_sources.json", "_common/nexusS5.sty"):
        check(os.path.exists(os.path.join(root, rel)), "présence %s" % rel, "fichier absent")
    for key in LEVELS:
        p = os.path.join(root, "_common", "blueprints", "blueprint_%s.json" % key)
        if not check(os.path.exists(p), "blueprint de niveau %s" % key, "fichier absent"):
            continue
        bp = load_json(p)
        cr = bp.get("curriculum_reference") or {}
        check(bool(cr.get("transition")), "programme de référence du niveau %s" % key,
              "curriculum_reference absent ou incomplet")
        prog = cr.get("programme_applique_a_l_eleve") or {}
        check("nouvelle_progression_applicable" in prog,
              "applicabilité du programme 2026 pour %s" % key, "non précisée")
        if key in ("4e", "3e"):
            check(prog.get("nouvelle_progression_applicable") is False,
                  "cycle 4 : nouvelle progression non appliquée prématurément à %s" % key,
                  "la nouvelle progression de cycle 4 est appliquée à tort")

    caches = [os.path.join(dp, f) for dp, dn, fns in os.walk(root)
              for f in fns if f.endswith(".pyc")] + \
             [os.path.join(dp, d) for dp, dn, fns in os.walk(root) for d in dn
              if d == "__pycache__"]
    check(not caches, "absence de cache Python dans la livraison",
          "%d élément(s) : %s" % (len(caches), ", ".join(os.path.relpath(c, root) for c in caches[:5])))

    seen_item_ids = set()
    seen_criterion_ids = set()

    for st in students:
        who = "%s (%s)" % (st["name"], st["level"])
        d = core.student_output_dir(st)
        td = os.path.join(d, "_ENSEIGNANT")
        lv = core.level_of(st)

        # ------------------------------------------------ 3. présence des livrables
        docs = {
            "travail": os.path.join(d, core.doc_basename("TRAVAIL", st)),
            "evaluation": os.path.join(d, core.doc_basename("EVALUATION", st)),
            "enseignant": os.path.join(td, core.doc_basename("ENSEIGNANT", st)),
        }
        for kind, base in docs.items():
            check(os.path.exists(base + ".tex"), "%s : source %s" % (who, kind), base + ".tex absent")
            check(os.path.exists(base + ".pdf"), "%s : PDF %s" % (who, kind), base + ".pdf absent")
        for name in STUDENT_JSON:
            check(os.path.exists(os.path.join(d, name)), "%s : %s" % (who, name), "absent")
        for name in TEACHER_JSON:
            check(os.path.exists(os.path.join(td, name)), "%s : _ENSEIGNANT/%s" % (who, name), "absent")

        # ------------------------------- 4. séparation des documents sensibles
        for name in TEACHER_JSON:
            check(not os.path.exists(os.path.join(d, name)),
                  "%s : %s hors du dossier enseignant" % (who, name),
                  "le fichier sensible ne doit pas se trouver à la racine du dossier élève")

        # -------------------------------------------------- 5. validité des JSON
        try:
            profile = load_json(os.path.join(d, "student_learning_profile.json"))
            blueprint = load_json(os.path.join(d, "evaluation_blueprint.json"))
            responses = load_json(os.path.join(d, "responses_TEMPLATE.json"))
            plan = load_json(os.path.join(d, "four_week_action_plan_TEMPLATE.json"))
            schema = load_json(os.path.join(d, "post_stage_analysis_schema.json"))
            manifest = load_json(os.path.join(td, "evaluation_manifest.json"))
            key = load_json(os.path.join(td, "answer_key.json"))
        except Exception as exc:
            check(False, "%s : JSON illisible" % who, str(exc))
            continue
        check(True, "%s : sept JSON valides" % who)

        # ------------------------------------------ 6. cohérence élève / niveau
        check(profile["student"]["name"] == st["name"], "%s : nom du profil" % who, profile["student"]["name"])
        check(profile["student"]["level_key"] == st["level"], "%s : niveau du profil" % who, profile["student"]["level_key"])
        check(profile["student"]["subject"] == lv["subject"], "%s : matière du profil" % who, profile["student"]["subject"])
        for obj, name in ((blueprint, "blueprint"), (manifest, "manifeste"),
                          (key, "corrigé"), (responses, "saisie"), (plan, "plan 4 semaines")):
            check(obj.get("student_id") == st["id"], "%s : student_id du %s" % (who, name), str(obj.get("student_id")))

        # ------------------------------------------------ 7. items et identifiants
        m_items = {i["ref"]: i for i in manifest["items"]}
        k_items = {a["ref"]: a for a in key["answers"]}
        p_items = {i["ref"]: i for i in profile["assessment"]["items"]}
        r_items = {r["ref"]: r for r in responses["responses"]}
        check(sorted(m_items) == sorted(common.EXAM_ITEM_ORDER), "%s : 12 items au manifeste" % who, str(sorted(m_items)))
        check(sorted(k_items) == sorted(m_items), "%s : manifeste <-> corrigé" % who, "références divergentes")
        check(sorted(p_items) == sorted(m_items), "%s : manifeste <-> profil" % who, "références divergentes")
        check(sorted(r_items) == sorted(m_items), "%s : manifeste <-> saisie" % who, "références divergentes")

        for ref, it in m_items.items():
            iid = it["item_id"]
            check(iid not in seen_item_ids, "unicité de item_id %s" % iid, "identifiant déjà rencontré")
            seen_item_ids.add(iid)
            check(it["skill_id"] in lv["skills"], "%s : skill_id de %s" % (who, ref), it["skill_id"])
            for extra in it.get("skills_extra", []):
                check(extra in lv["skills"], "%s : skill_id secondaire de %s" % (who, ref), extra)
            check(k_items[ref]["points"] == it["points"], "%s : points de %s" % (who, ref),
                  "manifeste %s, corrigé %s" % (it["points"], k_items[ref]["points"]))
            check(k_items[ref]["expected_answer"] == it["expected_answer"],
                  "%s : réponse attendue de %s" % (who, ref), "manifeste et corrigé divergent")
            crit = it["grading_criteria"]
            check(bool(crit), "%s : barème de %s" % (who, ref), "aucun critère de correction")
            check(abs(sum(c["points"] for c in crit) - it["points"]) < 1e-9,
                  "%s : somme du barème de %s" % (who, ref),
                  "%s critères pour %s points" % (sum(c["points"] for c in crit), it["points"]))
            for c in crit:
                cid = c.get("criterion_id")
                check(bool(cid), "%s : identifiant de critère sur %s" % (who, ref), "absent")
                check(cid not in seen_criterion_ids, "unicité de criterion_id %s" % cid, "déjà vu")
                seen_criterion_ids.add(cid)
                check(c.get("skill_id") in lv["skills"],
                      "%s : compétence du critère %s" % (who, cid), str(c.get("skill_id")))
                check(c.get("evidence_type") in criteria_map.EVIDENCE_TYPES,
                      "%s : type de preuve du critère %s" % (who, cid), str(c.get("evidence_type")))
                check(bool(c.get("subpart")), "%s : sous-partie du critère %s" % (who, cid), "absente")
                check(c["points"] > 0, "%s : points du critère %s" % (who, cid), str(c["points"]))
            crit_skills = {c["skill_id"] for c in crit}
            item_skills = {it["skill_id"]} | set(it.get("skills_extra", []))
            check(crit_skills == item_skills,
                  "%s : compétences de %s = compétences de ses critères" % (who, ref),
                  "item %s, critères %s" % (sorted(item_skills), sorted(crit_skills)))
            # un code CONTROLE suppose qu'un contrôle soit explicitement demandé
            if any(e["code"] == "CONTROLE" for e in it["likely_errors"]):
                demande = re.search(r"contrôl|vérifi|Contrôl|Vérifi", it.get("statement", "") or "")
                check(bool(demande) or bool(re.search(
                    r"contrôl|vérifi", " ".join(c["desc"] for c in crit), re.I)),
                    "%s : code CONTROLE justifié sur %s" % (who, ref),
                    "aucun contrôle explicitement demandé dans l'énoncé ni dans le barème")
            # rétention
            ret = it.get("retention") or {}
            for sid in item_skills:
                check(sid in ret, "%s : contexte de rétention de %s pour %s" % (who, ref, sid), "absent")
            check(len(it["likely_errors"]) >= 1, "%s : erreurs probables de %s" % (who, ref), "aucune")
            check(all(e["code"] in common.ERROR_CODES for e in it["likely_errors"]),
                  "%s : codes d'erreur de %s" % (who, ref), "code hors nomenclature")
            check(it["comparability"] in common.COMPARABILITY,
                  "%s : comparabilité de %s" % (who, ref), it["comparability"])
            cs = it["comparison_status"]
            check(cs in core.COMPARISON_VALUES, "%s : comparison_status de %s" % (who, ref), cs)
            check(cs != "parallel_measures",
                  "%s : %s ne prétend pas à des mesures appariées" % (who, ref),
                  "parallel_measures exige deux mesures nominatives réelles, indisponibles")
            if cs == "indicative_skill_comparison":
                # un énoncé parallèle existe, mais la réponse initiale n'a pas été conservée :
                # la confrontation reste qualitative.
                refs = it["baseline_skill_refs"]
                check(bool(it["baseline_item_id"]) or bool(refs),
                      "%s : rattachement initial de %s" % (who, ref),
                      "aucun énoncé initial ni compétence diagnostiquée")
                if it["baseline_item_id"]:
                    check(it["baseline_item_id"] in lv["baseline_items"],
                          "%s : énoncé initial connu pour %s" % (who, ref), str(it["baseline_item_id"]))
                for r in refs:
                    check(all(b in lv["baseline_items"] for b in r["baseline_items"]),
                          "%s : références initiales de %s" % (who, ref), str(r))
            else:
                check(it["baseline_item_id"] is None,
                      "%s : absence de rattachement initial pour %s" % (who, ref),
                      "item %s mais rattaché à %s" % (cs, it["baseline_item_id"]))

        # ------------------------------------------------ 8. barème global et durée
        total = sum(i["points"] for i in m_items.values())
        minutes = round(sum(i["target_minutes"] for i in m_items.values()), 2)
        check(abs(total - common.EXAM_TOTAL_POINTS) < 1e-9, "%s : total de points" % who, "%s / 20" % total)
        check(minutes <= common.EXAM_MAX_ESTIMATED_MINUTES,
              "%s : durée estimée de l'évaluation" % who,
              "%s min, plafond %s" % (minutes, common.EXAM_MAX_ESTIMATED_MINUTES))
        check(common.EXAM_MINUTES - minutes >= common.EXAM_MIN_MARGIN_MINUTES,
              "%s : marge sur les 45 minutes" % who,
              "%.2f min de marge, minimum %s" % (common.EXAM_MINUTES - minutes,
                                                 common.EXAM_MIN_MARGIN_MINUTES))
        # la durée doit provenir du contenu, pas d'une table imposée
        for ref, it in m_items.items():
            te = it.get("time_estimate") or {}
            check(bool(te.get("breakdown")), "%s : durée de %s estimée depuis le contenu" % (who, ref),
                  "aucune décomposition lecture/traitement/rédaction")
        commun = sum(i["points"] for i in m_items.values() if i["kind"] == "commun")
        share = 100.0 * commun / total
        check(60 <= share <= 80, "%s : part du noyau commun" % who, "%.1f %%" % share)
        maxskill = max(blueprint["points_per_skill"].values())
        top = max(blueprint["points_per_skill"], key=blueprint["points_per_skill"].get)
        check(100.0 * maxskill / total <= 30, "%s : surpondération d'une compétence" % who,
              "%.1f %% des points sur %s" % (100.0 * maxskill / total, top))
        check(len(blueprint["points_per_skill"]) >= 6, "%s : couverture des compétences" % who,
              "%d compétences seulement" % len(blueprint["points_per_skill"]))
        work = sum(a["minutes"] for a in profile["session5"]["activities"])
        check(work == common.WORK_MINUTES, "%s : durée du travail" % who, "%s min" % work)

        # Progression de la difficulté, contrôlée partie par partie et non item par item :
        # A = automatismes de socle, B = application, C = transfert avec au moins une
        # tâche complexe. Exiger une croissance stricte entre C1 et C2 n'aurait pas de
        # sens : l'item C2 est individualisé et peut viser une compétence plus élémentaire.
        diff = {r: m_items[r]["difficulty"] for r in common.EXAM_ITEM_ORDER}
        dA = [diff[r] for r in ("A1", "A2", "A3", "A4", "A5", "A6")]
        dB = [diff[r] for r in ("B1", "B2", "B3", "B4")]
        dC = [diff[r] for r in ("C1", "C2")]
        check(all(x == "socle" for x in dA), "%s : partie A entièrement de niveau socle" % who, str(dA))
        check(all(x in ("standard", "transfert") for x in dB),
              "%s : partie B au niveau application" % who, str(dB))
        check(all(x != "socle" for x in dC) and "transfert" in dC,
              "%s : partie C au niveau transfert" % who, str(dC))
        # équilibre des types de tâches
        tasks = [m_items[r]["task_type"] for r in common.EXAM_ITEM_ORDER]
        check(tasks.count("automatisme") == 6 and tasks.count("application") == 4
              and tasks.count("transfert") == 2,
              "%s : équilibre automatismes / application / transfert" % who, str(tasks))

        # ------------------------------------- 9. aucune donnée finale fabriquée
        check(profile["post_stage"]["status"] == "awaiting_assessment",
              "%s : statut post-stage" % who, profile["post_stage"]["status"])
        check(responses["status"] == "awaiting_assessment", "%s : statut de la saisie" % who, responses["status"])
        check(all("criteria" in r and r["criteria"] for r in responses["responses"]),
              "%s : saisie prévue critère par critère" % who, "un item sans critères")
        check(all(c["score"] is None for r in responses["responses"] for c in r["criteria"]),
              "%s : aucun score pré-rempli" % who, "des scores sont déjà renseignés")
        check(all(c["criterion_id"] == cc["criterion_id"]
                  for r in responses["responses"]
                  for c, cc in zip(r["criteria"], m_items[r["ref"]]["grading_criteria"])),
              "%s : critères de saisie alignés sur le barème" % who, "désalignement")
        check(all(r["confidence"] is None for r in responses["responses"]),
              "%s : aucune certitude pré-remplie" % who, "des certitudes sont déjà renseignées")
        check(plan["status"] == "awaiting_assessment", "%s : statut du plan 4 semaines" % who, plan["status"])
        check(all(w["skills"] == [] and w["objective"] is None for w in plan["weeks"]),
              "%s : plan 4 semaines non pré-rempli" % who, "des semaines sont déjà renseignées")
        check(len(plan["weeks"]) == 4, "%s : quatre semaines au plan" % who, str(len(plan["weeks"])))
        check(schema["$id"].endswith("post-stage-analysis-v2"), "%s : schéma de sortie v2" % who,
              schema["$id"])
        sk_props = schema["properties"]["skills"]["items"]["properties"]
        check(sk_props["mastery_delta"]["type"] == "null",
              "%s : le schéma interdit tout écart chiffré" % who, str(sk_props["mastery_delta"]))
        check(sk_props["baseline_mastery"]["type"] == "null",
              "%s : le schéma interdit une maîtrise initiale chiffrée" % who, "")
        check("evidence_strength" in sk_props and "measurement_reliability" not in sk_props,
              "%s : force de preuve substituée à la fiabilité de mesure" % who, "")
        check(profile["baseline"]["mesure_initiale_nominative_disponible"] is False,
              "%s : absence de mesure initiale nominative déclarée" % who, "")

        # ------------------------------------------------- 10. sources référencées
        missing = [s["path"] for s in profile["sources"] if not core.source_exists(s["path"])]
        check(not missing, "%s : sources référencées existantes" % who, ", ".join(missing))

        # -------------------------------- 11. pas de chemin absolu dans les livrables
        for f in [os.path.join(d, n) for n in STUDENT_JSON] + \
                 [os.path.join(td, n) for n in TEACHER_JSON] + \
                 [docs["travail"] + ".tex", docs["evaluation"] + ".tex", docs["enseignant"] + ".tex"]:
            with open(f, encoding="utf-8") as fh:
                body = fh.read()
            check("/home/" not in body and "/Users/" not in body,
                  "%s : absence de chemin absolu dans %s" % (who, os.path.basename(f)),
                  "chemin absolu détecté")

        # ---------------------- 12. aucun corrigé dans les documents remis à l'élève
        for kind in ("travail", "evaluation"):
            with open(docs[kind] + ".tex", encoding="utf-8") as fh:
                src = fh.read()
            for ref, a in k_items.items():
                na = norm_tex(a["expected_answer"])
                if len(na) >= 10:
                    check(na not in norm_tex(src),
                          "%s : réponse de %s absente du livret %s" % (who, ref, kind),
                          "la réponse attendue apparaît dans un document élève")
            for crit in ("grading_criteria", "expected_answer"):
                check(crit not in src, "%s : champ %s absent du .tex %s" % (who, crit, kind), "présent")

        if not args.skip_pdf:
            for kind in ("travail", "evaluation"):
                txt = pdf_text(docs[kind] + ".pdf")
                low = txt.lower()
                for marker in FORBIDDEN_IN_STUDENT:
                    check(marker.lower() not in low,
                          "%s : marqueur « %s » absent du PDF %s" % (who, marker, kind),
                          "marqueur trouvé dans un document élève")
                nt = norm_tex(txt)
                for ref, a in k_items.items():
                    na = norm_tex(a["expected_answer"])
                    if len(na) >= 12:
                        check(na not in nt,
                              "%s : réponse de %s absente du PDF %s" % (who, ref, kind),
                              "la réponse attendue est lisible dans un document élève")
                check(st["name"].split()[0] in txt, "%s : nom présent dans le PDF %s" % (who, kind),
                      "prénom introuvable")
                check(lv["label"].split("—")[0].strip()[:18] in txt,
                      "%s : niveau présent dans le PDF %s" % (who, kind), "libellé de niveau introuvable")
                for ref in common.EXAM_ITEM_ORDER if kind == "evaluation" else []:
                    check(re.search(r"\b%s\b" % ref, txt) is not None,
                          "%s : item %s présent dans le PDF d'évaluation" % (who, ref), "item introuvable")

    # ------------------------------------ 13. aucune donnée de test dans la livraison
    for path in _walk(root, ".json"):
        if os.sep + "tests" + os.sep in path:
            continue
        with open(path, encoding="utf-8") as fh:
            body = fh.read()
        check("SYNTHETIQUE" not in body and "synthetic_fixture" not in body,
              "absence de données de test dans %s" % os.path.relpath(path, root),
              "marqueur de jeu de test détecté")

    ok = not ERRORS
    report = {
        "schema": "nexus-s5-validation-v1",
        "checks_run": len(CHECKS),
        "checks_failed_critical": len(ERRORS),
        "warnings": len(WARNINGS),
        "errors": ERRORS,
        "warning_list": WARNINGS,
        "result": "PASS" if ok else "FAIL",
    }
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            f.write("\n")
    if not args.quiet:
        print("contrôles exécutés : %d" % len(CHECKS))
        print("échecs critiques  : %d" % len(ERRORS))
        print("avertissements    : %d" % len(WARNINGS))
        for e in ERRORS[:40]:
            print("  ERREUR       %s" % e)
        for w in WARNINGS[:40]:
            print("  AVERTISSEMENT %s" % w)
    print("RESULTAT : %s" % report["result"])
    return 0 if ok else 1


def _walk(root, ext):
    for dirpath, _dirnames, filenames in os.walk(root):
        if os.path.basename(dirpath) in ("_build_logs", "__pycache__"):
            continue
        for fn in filenames:
            if fn.endswith(ext):
                yield os.path.join(dirpath, fn)


if __name__ == "__main__":
    sys.exit(main())
