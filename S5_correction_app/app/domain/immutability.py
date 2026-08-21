# -*- coding: utf-8 -*-
"""Contrôle des documents distribués : ils ne bougent pas, et on le vérifie.

Au démarrage, les 60 empreintes du manifeste V3 sont recalculées. Si l'une d'elles a
changé, l'application ne continue pas comme si de rien n'était : elle bascule en lecture
seule et le dit sur chaque page. Un document dont l'empreinte a changé est en outre
refusé individuellement à la correction.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from .. import config
from ..security import sha256_file


@dataclass
class ImmutabilityReport:
    total: int = 0
    verified: int = 0
    changed: List[dict] = field(default_factory=list)
    missing: List[str] = field(default_factory=list)
    by_path: Dict[str, str] = field(default_factory=dict)
    manifest_present: bool = True

    @property
    def ok(self) -> bool:
        return self.manifest_present and not self.changed and not self.missing

    @property
    def verdict(self) -> str:
        if not self.manifest_present:
            return "MANIFESTE ABSENT"
        return "PASS" if self.ok else "IMMUTABILITY FAILURE"

    def summary(self) -> dict:
        return {"immutable_artifacts_total": self.total,
                "immutable_artifacts_verified": self.verified,
                "immutable_artifacts_changed": len(self.changed),
                "immutable_artifacts_missing": len(self.missing),
                "verdict": self.verdict}


def load_manifest(path: Path = None) -> dict:
    path = Path(path or config.IMMUTABLE_MANIFEST)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def verify(path: Path = None, repo_root: Path = None) -> ImmutabilityReport:
    path = Path(path or config.IMMUTABLE_MANIFEST)
    repo_root = Path(repo_root or config.REPO_ROOT)
    report = ImmutabilityReport()
    if not path.exists():
        report.manifest_present = False
        return report
    manifest = load_manifest(path)
    for art in manifest.get("artifacts", []):
        report.total += 1
        full = repo_root / art["path"]
        if not full.exists():
            report.missing.append(art["path"])
            continue
        got = sha256_file(full)
        report.by_path[art["path"]] = got
        if got != art["sha256"]:
            report.changed.append({"path": art["path"], "expected": art["sha256"],
                                   "observed": got, "student_id": art.get("student_id")})
            continue
        report.verified += 1
    return report


def changed_student_ids(report: ImmutabilityReport) -> set:
    return {c.get("student_id") for c in report.changed if c.get("student_id")}


def check_assessment(assessment, repo_root: Path = None) -> List[str]:
    """Recontrôle les deux PDF d'une évaluation juste avant une action sensible."""
    repo_root = Path(repo_root or config.REPO_ROOT)
    problems = []
    for label, rel, expected in (
            ("évaluation", assessment.evaluation_pdf_path, assessment.evaluation_pdf_sha256),
            ("livret", assessment.travail_pdf_path, assessment.travail_pdf_sha256)):
        full = repo_root / rel
        if not full.exists():
            problems.append("le PDF %s est introuvable : %s" % (label, rel))
            continue
        if sha256_file(full) != expected:
            problems.append("le PDF %s a changé depuis l'import : %s" % (label, rel))
    return problems
