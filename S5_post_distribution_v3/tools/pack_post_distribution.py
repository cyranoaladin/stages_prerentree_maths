#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Packager sûr. Il construit à côté, puis bascule ; il ne supprime jamais à l'aveugle.

Ce que refuse ce script, catégoriquement :

    * une destination égale à la source ;
    * la racine du système, le répertoire personnel, le dépôt lui-même ou l'un de
      ses parents ;
    * une destination existante qui ne porte pas la sentinelle de ce packager ;
    * toute écriture à l'intérieur de S5_cloture.

Ce qu'il fait :

    * il construit le paquet dans un répertoire de travail voisin, jamais en place ;
    * il empreinte chaque fichier livré ;
    * il bascule par renommage atomique, et conserve l'ancien paquet sous un suffixe
      .previous que l'opérateur supprime lui-même s'il le souhaite ;
    * il propose --dry-run, qui n'écrit rien du tout.

Les artefacts élèves figés ne sont jamais touchés : ils ne font pas partie de ce
paquet, qui ne contient que la couche post-distribution.
"""

import argparse
import hashlib
import os
import shutil
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd

SENTINEL = ".nexus-post-distribution-package"
EXCLUDED = ("__pycache__", ".pyc", ".tmp", ".pytest_cache")


def _refuse(msg):
    raise pd.PostDistributionError("destination refusée : " + msg)


def check_destination(dest, source):
    dest = os.path.abspath(dest)
    source = os.path.abspath(source)
    home = os.path.abspath(os.path.expanduser("~"))
    forbidden = {os.path.abspath(os.sep), home, pd.REPO_ROOT,
                 os.path.dirname(pd.REPO_ROOT), source, pd.S5_ROOT}
    if dest in forbidden:
        _refuse("%s est la racine, le répertoire personnel, le dépôt, son parent, la source ou "
                "le dossier figé S5_cloture" % dest)
    if source == dest:
        _refuse("source et destination identiques")
    if dest.startswith(source + os.sep):
        _refuse("la destination est à l'intérieur de la source")
    if dest.startswith(pd.S5_ROOT + os.sep):
        _refuse("aucune écriture n'est autorisée dans S5_cloture")
    if os.path.exists(dest):
        if not os.path.isdir(dest):
            _refuse("%s existe et n'est pas un répertoire" % dest)
        if not os.path.exists(os.path.join(dest, SENTINEL)):
            _refuse("%s existe déjà et ne porte pas la sentinelle %s. Ce packager ne remplace "
                    "que des paquets qu'il a lui-même produits." % (dest, SENTINEL))
    return dest


def iter_files(source):
    for dp, dn, fns in os.walk(source):
        dn[:] = [d for d in dn if d not in ("__pycache__", ".pytest_cache")]
        for fn in fns:
            if fn.endswith(EXCLUDED[1:]) or fn == SENTINEL:
                continue
            full = os.path.join(dp, fn)
            yield full, os.path.relpath(full, source)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()


def build(source, dest, dry_run=False):
    dest = check_destination(dest, source)
    files = sorted(iter_files(source), key=lambda t: t[1])
    if dry_run:
        print("--dry-run : rien n'est écrit.")
        print("source      : %s" % source)
        print("destination : %s" % dest)
        print("fichiers    : %d" % len(files))
        if os.path.exists(dest):
            print("le paquet existant porte la sentinelle : il serait remplacé après bascule, "
                  "et conservé sous %s.previous" % os.path.basename(dest))
        return 0
    staging = dest + ".staging"
    if os.path.exists(staging):
        if not os.path.exists(os.path.join(staging, SENTINEL)):
            _refuse("%s existe et ne porte pas la sentinelle" % staging)
        shutil.rmtree(staging)
    os.makedirs(staging)
    with open(os.path.join(staging, SENTINEL), "w", encoding="utf-8") as f:
        f.write("paquet produit par S5_post_distribution_v3/tools/pack_post_distribution.py\n")
    manifest = []
    for full, rel in files:
        target = os.path.join(staging, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copy2(full, target)
        manifest.append({"chemin": rel, "sha256": sha256(target),
                         "octets": os.path.getsize(target)})
    pd_manifest = {
        "schema": "nexus-s5-post-distribution-package-v3",
        "genere_le": pd.GENERATED_ON,
        "source": os.path.relpath(source, pd.REPO_ROOT),
        "fichiers": len(manifest),
        "contenu": manifest,
        "avertissement": ("ce paquet ne contient aucun document élève distribué : ceux-ci restent "
                          "dans S5_cloture et ne sont jamais recopiés ni modifiés par ce script."),
    }
    import json
    with open(os.path.join(staging, "PACKAGE_MANIFEST.json"), "w", encoding="utf-8") as f:
        json.dump(pd_manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")
    previous = dest + ".previous"
    if os.path.exists(dest):
        if os.path.exists(previous):
            if not os.path.exists(os.path.join(previous, SENTINEL)):
                _refuse("%s existe et ne porte pas la sentinelle" % previous)
            shutil.rmtree(previous)
        os.rename(dest, previous)
    os.rename(staging, dest)
    print("paquet écrit : %s (%d fichiers)" % (dest, len(manifest)))
    if os.path.exists(previous):
        print("ancien paquet conservé : %s — à supprimer manuellement si vous le souhaitez"
              % previous)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--source", default=pd.V3_ROOT)
    ap.add_argument("--dest", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    try:
        return build(os.path.abspath(args.source), args.dest, args.dry_run)
    except pd.PostDistributionError as exc:
        print("REFUS : %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
