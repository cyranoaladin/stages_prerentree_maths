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

import argparse
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


SENTINEL = ".nexus-s5-generated-package"


def _refuse(msg):
    raise SystemExit("REFUS : %s" % msg)


def prepare(d, dry_run):
    """Prépare un répertoire de sortie sans jamais supprimer à l'aveugle.

    Ce script a effacé, dans une version antérieure, tout répertoire portant le nom
    attendu. Il ne le fait plus : une destination n'est remplacée que si elle porte
    la sentinelle de ce packager, la construction se fait dans un répertoire de
    travail voisin, et la bascule est un renommage atomique. L'ancien paquet est
    conservé sous le suffixe .previous, à charge de l'opérateur de le supprimer.
    """
    d = os.path.abspath(d)
    home = os.path.abspath(os.path.expanduser("~"))
    interdits = {os.path.abspath(os.sep), home, PARENT, os.path.dirname(PARENT),
                 os.path.abspath(ROOT)}
    if d in interdits:
        _refuse("%s est la racine, le répertoire personnel, le dépôt, son parent, ou le "
                "dossier source S5_cloture" % d)
    if d.startswith(os.path.abspath(ROOT) + os.sep):
        _refuse("aucune écriture n'est autorisée dans le dossier source %s" % ROOT)
    if os.path.exists(d):
        if not os.path.isdir(d):
            _refuse("%s existe et n'est pas un répertoire" % d)
        if not os.path.exists(os.path.join(d, SENTINEL)):
            _refuse("%s existe déjà et ne porte pas la sentinelle %s. Ce script ne remplace "
                    "que des paquets qu'il a lui-même produits ; déplacez ou renommez ce "
                    "répertoire vous-même." % (d, SENTINEL))
    staging = d + ".staging"
    if dry_run:
        return d, None
    if os.path.exists(staging):
        if not os.path.exists(os.path.join(staging, SENTINEL)):
            _refuse("%s existe et ne porte pas la sentinelle" % staging)
        shutil.rmtree(staging)
    os.makedirs(staging)
    with open(os.path.join(staging, SENTINEL), "w", encoding="utf-8") as f:
        f.write("paquet produit par S5_cloture/tools/make_release.py\n")
    return d, staging


def commit(final, staging):
    previous = final + ".previous"
    if os.path.exists(final):
        if os.path.exists(previous):
            if not os.path.exists(os.path.join(previous, SENTINEL)):
                _refuse("%s existe et ne porte pas la sentinelle" % previous)
            shutil.rmtree(previous)
        os.rename(final, previous)
    os.rename(staging, final)
    return previous if os.path.exists(previous) else None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="n'écrit rien ; affiche ce qui serait produit")
    args = ap.parse_args(argv)

    release_final, release_dir = prepare(RELEASE_DIR, args.dry_run)
    audit_final, audit_dir = prepare(AUDIT_DIR, args.dry_run)
    if args.dry_run:
        rel, aud = 0, 0
        for src, rel_path in iter_files():
            if destination(rel_path) == "both":
                rel += 1
            aud += 1
        print("--dry-run : rien n'est écrit.")
        print("S5_release : %d fichiers seraient produits dans %s" % (rel, release_final))
        print("S5_audit   : %d fichiers seraient produits dans %s" % (aud, audit_final))
        return 0

    rel_files, aud_files = [], []
    for src, rel in iter_files():
        where = destination(rel)
        if where in ("both",):
            copy(rel, src, release_dir)
            rel_files.append(rel)
        copy(rel, src, audit_dir)          # le paquet d'audit contient tout
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
        "fichiers_release": [{"chemin": r, "sha256": sha256(os.path.join(release_dir, r)),
                              "octets": os.path.getsize(os.path.join(release_dir, r))}
                             for r in sorted(rel_files)],
    }
    for base in (release_dir, audit_dir):
        with open(os.path.join(base, "RELEASE_MANIFEST.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
            f.write("\n")

    def count(base, ext):
        return sum(1 for dp, dn, fns in os.walk(base) for f in fns if f.endswith(ext))

    for label, staging in (("S5_release", release_dir), ("S5_audit", audit_dir)):
        print("%s : %d fichiers  (pdf %d, json %d, tex %d, log %d, pyc %d)"
              % (label, sum(1 for dp, dn, fns in os.walk(staging) for _ in fns),
                 count(staging, ".pdf"), count(staging, ".json"),
                 count(staging, ".tex"), count(staging, ".log"), count(staging, ".pyc")))

    for final, staging in ((release_final, release_dir), (audit_final, audit_dir)):
        previous = commit(final, staging)
        if previous:
            print("ancien paquet conservé : %s — à supprimer manuellement si vous le souhaitez"
                  % previous)
    return 0


if __name__ == "__main__":
    sys.exit(main())
