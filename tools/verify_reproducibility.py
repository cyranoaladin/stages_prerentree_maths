#!/usr/bin/env python3
"""Preuve déterministe de reproductibilité du build Nexus Réussite (Build A vs Build B bit-for-bit)."""

import hashlib
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

def collect_hashes():
    hashes = {}
    # Target deterministic files: HTML, manifests, catalog
    targets = list((ROOT / "dist").rglob("*.html")) + [
        ROOT / "content" / "catalog.json",
        ROOT / "MANIFEST_PUBLIC.csv",
        ROOT / "MANIFEST_PRIVATE.csv"
    ]
    for p in sorted(targets):
        if p.exists() and p.is_file():
            rel = p.relative_to(ROOT).as_posix()
            hashes[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return hashes

def main():
    print("=== PREUVE DE REPRODUCTIBILITÉ DE BUILD ===")

    print("1. Exécution du Build A...")
    res_a = subprocess.run(["make", "clean-generated"], cwd=ROOT, capture_output=True)
    res_a2 = subprocess.run(["python3", "tools/build.py", "all"], cwd=ROOT, capture_output=True, text=True)
    if res_a2.returncode != 0:
        print("Échec du Build A:", res_a2.stderr)
        sys.exit(1)
    hashes_a = collect_hashes()
    print(f"Build A terminé : {len(hashes_a)} fichiers capturés.")

    print("2. Exécution du Build B...")
    res_b = subprocess.run(["make", "clean-generated"], cwd=ROOT, capture_output=True)
    res_b2 = subprocess.run(["python3", "tools/build.py", "all"], cwd=ROOT, capture_output=True, text=True)
    if res_b2.returncode != 0:
        print("Échec du Build B:", res_b2.stderr)
        sys.exit(1)
    hashes_b = collect_hashes()
    print(f"Build B terminé : {len(hashes_b)} fichiers capturés.")

    print("3. Comparaison des SHA-256 (Build A vs Build B)...")
    diffs = 0
    all_keys = sorted(set(hashes_a.keys()) | set(hashes_b.keys()))
    for k in all_keys:
        ha = hashes_a.get(k)
        hb = hashes_b.get(k)
        if ha != hb:
            print(f"DIFFÉRENCE trouvée dans {k}:\n  A: {ha}\n  B: {hb}")
            diffs += 1

    print(f"\nRésultat final : {len(all_keys)} fichiers comparés, {diffs} différence(s).")
    if diffs == 0:
        print("=== REPRODUCTIBILITÉ POUVÉE À 100% (0 DIFFÉRENCE) ===")
    else:
        print("=== ÉCHEC DE REPRODUCTIBILITÉ ===")
        sys.exit(1)

if __name__ == "__main__":
    main()
