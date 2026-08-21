#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remplit un gabarit de saisie avec des scores SYNTHÉTIQUES, pour éprouver le moteur.

Aucune de ces valeurs ne provient d'une copie d'élève. Le fichier produit porte le
marqueur ``fixture_synthetique`` et n'a pas vocation à être analysé comme un
résultat réel : il sert uniquement au jeu de tests.
"""

import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "tools"))

import pd_core as pd


def fill(student_id, pattern=None, observed_minutes=42.0):
    """pattern : dict {criterion_or_virtual_id: (score, [codes])}. Le reste est réussi."""
    pattern = pattern or {}
    path = os.path.join(pd.V3_ROOT, "responses",
                        "responses_v3_TEMPLATE_%s.json" % student_id)
    doc = json.load(open(path, encoding="utf-8"))
    doc["fixture_synthetique"] = True
    doc["status"] = "assessed_SYNTHETIQUE"
    doc["assessed_on"] = "2026-08-28"
    doc["observed_duration_minutes"] = observed_minutes

    def apply(row, key):
        if key in pattern:
            score, codes = pattern[key]
            if score == "NEUTRALISE":
                row["criterion_scoring_status"] = "neutralised"
                row["score"] = None
                row["observation"] = "neutralisé par le jeu de tests"
                return
            if score == "REQUIRES_HUMAN":
                row["criterion_scoring_status"] = "requires_human_allocation"
                row["score"] = None
                return
            row["score"] = score
            row["error_codes"] = list(codes)
        else:
            row["score"] = row["max_points"]
            row["error_codes"] = []
        row["criterion_scoring_status"] = "scored"

    for item in doc["responses"]:
        if item["confidence_probe"]:
            item["confidence"] = 3
        for c in item["criteria"]:
            if c["curriculum_scope"] == "mixed":
                for v in c["virtual_subcriteria"]:
                    apply(v, v["virtual_criterion_id"])
                c["criterion_scoring_status"] = "scored"
                c["score"] = round(sum(v["score"] or 0 for v in c["virtual_subcriteria"]), 4)
            else:
                apply(c, c["criterion_id"])
    return doc


def main():
    sid = sys.argv[1] if len(sys.argv) > 1 else "ahmad-beldi-maths"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/fixture_%s.json" % sid
    doc = fill(sid)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(out)


if __name__ == "__main__":
    main()
