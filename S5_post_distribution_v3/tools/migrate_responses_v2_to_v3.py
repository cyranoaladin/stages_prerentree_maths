#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Migration d'une saisie V2 vers le format V3, sans jamais inventer de ventilation.

État constaté au 21 août 2026 : aucune saisie V2 réelle n'existe dans le dossier.
Les quinze gabarits V2 sont vierges. Ce migrateur n'est donc pas nécessaire
aujourd'hui ; il existe pour le cas où une correction aurait été commencée sur un
poste qui ne serait pas remonté au dépôt.

Ce qu'il fait :

    * il reprend tel quel tout score déjà saisi au niveau du critère ;
    * il reporte les codes d'erreur d'un item UNIQUEMENT sur les critères de cet
      item qui ne sont pas intégralement réussis, et marque le report ;
    * lorsqu'un score existe sans ventilation exploitable — critère mixte à éclater,
      ou codes d'erreur impossibles à attribuer sans ambiguïté — il écrit
      « criterion_scoring_status »: « requires_human_allocation » plutôt que de
      répartir les points lui-même.

L'analyseur V3 refuse ensuite d'analyser tant qu'un critère porte ce statut. C'est
voulu : une ventilation inventée serait pire qu'une ventilation absente.
"""

import argparse
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd


def migrate(v2, student_id):
    tpl = pd.read_json(os.path.join(pd.V3_ROOT, "responses",
                                    "responses_v3_TEMPLATE_%s.json" % student_id),
                       "gabarit V3")
    if v2.get("student_id") != student_id:
        raise pd.PostDistributionError(
            "la saisie V2 porte student_id=%r, l'élève demandé est %r"
            % (v2.get("student_id"), student_id))
    old_items = {r["ref"]: r for r in v2.get("responses", [])}
    report = {"criteria_reprises": 0, "criteria_sans_saisie": 0,
              "criteria_requires_human_allocation": 0, "error_codes_reportes": 0,
              "error_codes_non_attribuables": 0, "details": []}

    def note(kind, cid, msg):
        report["details"].append({"type": kind, "criterion_id": cid, "message": msg})

    for item in tpl["responses"]:
        old = old_items.get(item["ref"])
        if old is None:
            for c in item["criteria"]:
                c["criterion_scoring_status"] = "requires_human_allocation"
                report["criteria_requires_human_allocation"] += 1
                note("item_absent", c["criterion_id"],
                     "item %s absent de la saisie V2" % item["ref"])
            continue
        item["confidence"] = old.get("confidence")
        old_crits = {c["criterion_id"]: c for c in (old.get("criteria") or [])}
        item_codes = list(old.get("error_codes") or [])
        failing = []
        for c in item["criteria"]:
            src = old_crits.get(c["criterion_id"])
            if c["curriculum_scope"] == "mixed":
                # Le critère V2 était global : sa ventilation entre une compétence N-1
                # et une notion N n'existe pas dans la source. Elle ne s'invente pas.
                c["criterion_scoring_status"] = "requires_human_allocation"
                for v in c["virtual_subcriteria"]:
                    v["criterion_scoring_status"] = "requires_human_allocation"
                    report["criteria_requires_human_allocation"] += 1
                if src is not None and src.get("score") is not None:
                    c["observation"] = ("score V2 global conservé pour mémoire : %s ; la "
                                        "ventilation entre le sous-critère N-1 et le "
                                        "sous-critère de passerelle doit être établie par le "
                                        "correcteur." % src["score"])
                note("mixte", c["criterion_id"], "ventilation à établir par un correcteur humain")
                continue
            if src is None or src.get("score") is None:
                c["criterion_scoring_status"] = "requires_human_allocation"
                report["criteria_requires_human_allocation"] += 1
                report["criteria_sans_saisie"] += 1
                note("sans_saisie", c["criterion_id"], "aucun score V2 pour ce critère")
                continue
            c["score"] = src["score"]
            c["observation"] = src.get("observation")
            c["criterion_scoring_status"] = "scored"
            report["criteria_reprises"] += 1
            if float(src["score"]) < float(c["max_points"]) - 1e-9:
                failing.append(c)
        if item_codes:
            if len(failing) == 1:
                failing[0]["error_codes"] = list(item_codes)
                failing[0]["observation"] = ((failing[0].get("observation") or "")
                                             + " [codes d'erreur reportés depuis l'item V2 : "
                                               "un seul critère échoué]").strip()
                report["error_codes_reportes"] += len(item_codes)
                note("codes_reportes", failing[0]["criterion_id"],
                     "codes %s reportés : un seul critère non réussi" % item_codes)
            elif failing:
                for c in failing:
                    c["criterion_scoring_status"] = "requires_human_allocation"
                    report["criteria_requires_human_allocation"] += 1
                report["error_codes_non_attribuables"] += len(item_codes)
                note("codes_ambigus", item["ref"],
                     "codes %s portés sur l'item V2 alors que %d critères sont non réussis : "
                     "l'attribution ne peut pas être devinée" % (item_codes, len(failing)))
            else:
                report["error_codes_non_attribuables"] += len(item_codes)
                note("codes_orphelins", item["ref"],
                     "codes %s portés sur l'item V2 alors qu'aucun critère n'est échoué : "
                     "codes abandonnés, aucun critère réussi ne doit porter d'erreur" % item_codes)
    tpl["status"] = "migrated_from_v2"
    tpl["assessed_on"] = v2.get("assessed_on")
    tpl["migration"] = {
        "from_schema": v2.get("schema"),
        "regle": "aucune ventilation par critère n'est inventée ; ce qui manque est signalé",
        "report": report,
    }
    return tpl, report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--student", required=True)
    ap.add_argument("--v2", required=True, help="fichier de saisie V2 renseigné")
    ap.add_argument("--out", required=True, help="fichier V3 à écrire (sous responses/)")
    args = ap.parse_args(argv)
    v2 = pd.read_json(args.v2, "saisie V2")
    doc, report = migrate(v2, args.student)
    pd.write_json(args.out, doc)
    print("migré : %s" % args.out)
    print("  critères repris                        : %d" % report["criteria_reprises"])
    print("  critères sans saisie V2                : %d" % report["criteria_sans_saisie"])
    print("  critères à ventiler par un humain      : %d"
          % report["criteria_requires_human_allocation"])
    print("  codes d'erreur reportés sans ambiguïté : %d" % report["error_codes_reportes"])
    print("  codes d'erreur non attribuables        : %d" % report["error_codes_non_attribuables"])
    if report["criteria_requires_human_allocation"]:
        print("  l'analyse V3 restera bloquée tant que ces critères ne seront pas tranchés.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
