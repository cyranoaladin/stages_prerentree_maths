#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Traçabilité des sources S1-S4 : dire ce qui est réellement vérifiable, et depuis où.

Le paquet d'audit précédent se présentait comme autonome alors que son validateur
dépendait de documents S1-S4 situés hors du bundle. Cette confusion cesse ici : le
mode de vérification est explicite, et le verdict le dit.

    --source-mode live       les fichiers sources sont présents autour du projet ;
                             chacun est relu et son empreinte recalculée.
                             Verdict possible : PASS ou FAIL.

    --source-mode manifest   seules les empreintes et les références du manifeste sont
                             disponibles ; leur cohérence interne est contrôlée, mais
                             aucune source n'est relue.
                             Verdict : PASS WITH LIMITATION — sources originales non
                             réauditables depuis ce bundle seul.

Aucune source manquante n'est fabriquée, en aucun mode.
"""

import argparse
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd

MANIFEST = os.path.join(pd.S5_ROOT, "_audit", "source_evidence_manifest.json")
OUT = os.path.join(pd.V3_ROOT, "source_evidence", "SOURCE_VERIFICATION.json")


def verify(mode, manifest_path=None, root=None):
    man = pd.read_json(manifest_path or MANIFEST, "manifeste de traçabilité des sources")
    root = root or pd.REPO_ROOT
    sources = man["sources"]
    rows = {"ok": 0, "missing": [], "mismatch": [], "malformed": []}
    for s in sources:
        for field in ("chemin_canonique", "sha256", "taille_octets"):
            if not s.get(field):
                rows["malformed"].append(s.get("chemin_canonique", "?"))
                break
        else:
            if len(s["sha256"]) != 64 or any(c not in "0123456789abcdef" for c in s["sha256"]):
                rows["malformed"].append(s["chemin_canonique"])
                continue
            if mode == "manifest":
                rows["ok"] += 1
                continue
            full = os.path.join(root, s["chemin_canonique"])
            if not os.path.exists(full):
                rows["missing"].append(s["chemin_canonique"])
                continue
            if pd.sha256(full) != s["sha256"]:
                rows["mismatch"].append(s["chemin_canonique"])
                continue
            rows["ok"] += 1
    if mode == "manifest":
        verdict = ("PASS WITH LIMITATION" if not rows["malformed"] else "FAIL")
        limitation = ("sources originales non réauditables depuis ce bundle seul : seules les "
                      "empreintes et les références du manifeste ont été contrôlées.")
    else:
        verdict = "PASS" if not (rows["missing"] or rows["mismatch"] or rows["malformed"]) \
            else "FAIL"
        limitation = None
    return {
        "schema": "nexus-s5-source-verification-v3",
        "generated_on": pd.GENERATED_ON,
        "source_mode": mode,
        "manifest": os.path.relpath(manifest_path or MANIFEST, pd.REPO_ROOT),
        "reference_root": os.path.relpath(root, os.path.dirname(pd.REPO_ROOT)),
        "sources_declared": len(sources),
        "sources_verified": rows["ok"],
        "sources_missing": rows["missing"],
        "sources_hash_mismatch": rows["mismatch"],
        "sources_malformed": rows["malformed"],
        "standalone_bundle": mode == "manifest",
        "limitation": limitation,
        "verdict": verdict,
        "regle": "aucune source manquante n'est fabriquée ; une absence est déclarée.",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--source-mode", choices=("live", "manifest"), default="live")
    ap.add_argument("--manifest")
    ap.add_argument("--root")
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args(argv)
    res = verify(args.source_mode, args.manifest, args.root)
    print("mode              : %s" % res["source_mode"])
    print("sources déclarées : %d" % res["sources_declared"])
    print("sources vérifiées : %d" % res["sources_verified"])
    for k in ("sources_missing", "sources_hash_mismatch", "sources_malformed"):
        if res[k]:
            print("%-18s: %d  %s" % (k, len(res[k]), res[k][:5]))
    if res["limitation"]:
        print("limitation        : %s" % res["limitation"])
    print("verdict           : %s" % res["verdict"])
    if not args.no_write:
        pd.write_json(OUT, res)
    return 0 if res["verdict"].startswith("PASS") else 1


if __name__ == "__main__":
    sys.exit(main())
