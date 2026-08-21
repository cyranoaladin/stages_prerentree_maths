#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sépare le paquet d'exploitation du paquet d'audit, et empreinte les deux.

    S5_release/   ce qui sert réellement à conduire les séances et à exploiter
                  les résultats : PDF, JSON, gabarits, scripts, index, manifeste
                  canonique. Aucun log, aucun test, aucun cache.
    S5_audit/     les preuves : sources LaTeX, journaux de compilation, rapports
                  d'audit, jeu de tests synthétique, contrôle visuel page à page.

Produit également RELEASE_MANIFEST.json (empreinte SHA-256 de chaque fichier livré).
"""

import sys
sys.dont_write_bytecode = True
import hashlib
import json
import os
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core

ROOT = core.S5_ROOT
PARENT = core.REPO_ROOT
DATE = "2026-08-21"

RELEASE_DIR = os.path.join(PARENT, "S5_release")
AUDIT_DIR = os.path.join(PARENT, "S5_audit")

# Ce qui n'a sa place dans aucun paquet.
EXCLUS = ("__pycache__", ".pyc", ".aux", ".fls", ".fdb_latexmk", ".out", ".synctex.gz")

# Ce qui relève du paquet d'audit et non du paquet d'exploitation.
AUDIT_ONLY_DIRS = ("_build_logs", "_audit", os.path.join("tools", "tests"))
AUDIT_ONLY_SUFFIX = (".tex", ".log")
AUDIT_ONLY_FILES = ()   # SCIENTIFIC_AUDIT.md accompagne aussi le paquet d'exploitation


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()


def iter_files():
    for dp, dn, fns in os.walk(ROOT):
        dn[:] = [d for d in dn if d != "__pycache__"]
        for fn in fns:
            if fn.endswith(EXCLUS[1:]):
                continue
            full = os.path.join(dp, fn)
            yield full, os.path.relpath(full, ROOT)


def destination(rel):
    """Retourne 'release', 'audit' ou 'both'."""
    if any(rel.startswith(d + os.sep) or rel == d for d in AUDIT_ONLY_DIRS):
        return "audit"
    if rel.endswith(AUDIT_ONLY_SUFFIX):
        return "audit"
    if os.path.basename(rel) in AUDIT_ONLY_FILES:
        return "audit"
    return "both"


def copy(rel, src, base):
    dst = os.path.join(base, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    return dst


def main():
    for d in (RELEASE_DIR, AUDIT_DIR):
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)

    rel_files, aud_files = [], []
    for src, rel in iter_files():
        where = destination(rel)
        if where in ("both",):
            copy(rel, src, RELEASE_DIR)
            rel_files.append(rel)
        copy(rel, src, AUDIT_DIR)          # le paquet d'audit contient tout
        aud_files.append(rel)

    manifest = {
        "schema": "nexus-s5-release-manifest-v1",
        "genere_le": DATE,
        "paquets": {
            "S5_release": {"objet": "exploitation des séances et des résultats",
                           "fichiers": len(rel_files)},
            "S5_audit": {"objet": "preuves, sources et journaux", "fichiers": len(aud_files)},
        },
        "regles_de_separation": {
            "exclus_des_deux": ["caches Python", "fichiers auxiliaires LaTeX"],
            "reserves_a_l_audit": ["sources .tex", "journaux .log", "_build_logs/", "_audit/",
                                   "tools/tests/", "SCIENTIFIC_AUDIT.md"],
        },
        "fichiers_release": [{"chemin": r, "sha256": sha256(os.path.join(RELEASE_DIR, r)),
                              "octets": os.path.getsize(os.path.join(RELEASE_DIR, r))}
                             for r in sorted(rel_files)],
    }
    for base in (RELEASE_DIR, AUDIT_DIR):
        with open(os.path.join(base, "RELEASE_MANIFEST.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
            f.write("\n")

    def count(base, ext):
        return sum(1 for dp, dn, fns in os.walk(base) for f in fns if f.endswith(ext))

    print("S5_release : %d fichiers  (pdf %d, json %d, tex %d, log %d, pyc %d)"
          % (sum(1 for dp, dn, fns in os.walk(RELEASE_DIR) for _ in fns),
             count(RELEASE_DIR, ".pdf"), count(RELEASE_DIR, ".json"),
             count(RELEASE_DIR, ".tex"), count(RELEASE_DIR, ".log"), count(RELEASE_DIR, ".pyc")))
    print("S5_audit   : %d fichiers  (pdf %d, json %d, tex %d, log %d, pyc %d)"
          % (sum(1 for dp, dn, fns in os.walk(AUDIT_DIR) for _ in fns),
             count(AUDIT_DIR, ".pdf"), count(AUDIT_DIR, ".json"),
             count(AUDIT_DIR, ".tex"), count(AUDIT_DIR, ".log"), count(AUDIT_DIR, ".pyc")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
