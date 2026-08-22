#!/usr/bin/env python3
"""CI-only gates: secret scanning and public/private confidentiality checks.

Run after `make all` so the checks operate on freshly generated output.
Exits non-zero (and prints every violation) on the first category that fails.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.student_registry import all_names, load_students, text_contains_name

ROOT = Path(__file__).resolve().parents[1]

SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN(?: RSA| OPENSSH| EC| DSA)? PRIVATE KEY-----"), "private key"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}"), "Slack token"),
    (re.compile(r"\bghp_[0-9A-Za-z]{36}\b"), "GitHub personal access token"),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"), "API secret key"),
]
SECRET_SCAN_DIRS = (
    "4e", "3e", "2nde", "1ere_spe", "1re_nsi", "tle_spe", "tle_nsi", "tle_pc",
    "content", "tools", "tests", "reports", "assets",
)
SECRET_SCAN_EXTENSIONS = {".md", ".py", ".json", ".csv", ".yml", ".yaml", ".css", ".js", ".html"}

PUBLIC_SCAN_ROOTS = (
    ROOT / "dist" / "site-public",
    ROOT / "dist" / "pdf",
    ROOT / "dist" / "packs" / "eleves",
    ROOT / "dist" / "packs" / "enseignants",
    ROOT / "MANIFEST_PUBLIC.csv",
)


def scan_secrets() -> list[str]:
    violations = []
    for directory in SECRET_SCAN_DIRS:
        base = ROOT / directory
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in SECRET_SCAN_EXTENSIONS:
                continue
            if "_archive" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern, label in SECRET_PATTERNS:
                if pattern.search(text):
                    violations.append(f"{path.relative_to(ROOT)}: motif '{label}' détecté")
    for name in (".env", ".env.local", ".env.production"):
        if (ROOT / name).exists():
            violations.append(f"Fichier interdit présent : {name}")
    return violations


def scan_public_confidentiality() -> list[str]:
    students = load_students(ROOT, validate_filesystem=False)
    names = all_names(students)
    violations = []
    for root in PUBLIC_SCAN_ROOTS:
        if not root.exists():
            continue
        paths = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
        for path in paths:
            if path.suffix.lower() not in {".html", ".csv"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for name in names:
                if text_contains_name(text, name):
                    violations.append(f"{path.relative_to(ROOT)}: alias élève '{name}' trouvé côté public")
    # 04_NOMINATIFS directories must never appear in the public site.
    site_public = ROOT / "dist" / "site-public"
    if site_public.exists():
        for path in site_public.rglob("*NOMINATIFS*"):
            violations.append(f"{path.relative_to(ROOT)}: chemin nominatif exposé côté public")
    return violations


def main() -> int:
    failures = 0

    secret_violations = scan_secrets()
    if secret_violations:
        failures += 1
        print("=== ÉCHEC : scan de secrets ===")
        for violation in secret_violations:
            print(f"  - {violation}")
    else:
        print("OK : aucun secret détecté.")

    public_violations = scan_public_confidentiality()
    if public_violations:
        failures += 1
        print("=== ÉCHEC : gate de confidentialité logique publique ===")
        for violation in public_violations:
            print(f"  - {violation}")
    else:
        print("OK : aucune fuite nominative côté public.")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
