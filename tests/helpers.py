"""Shared test fixtures for building a minimal content/students.json registry."""

from __future__ import annotations

import json
from pathlib import Path


def write_minimal_registry(root: Path, students: list[dict]) -> None:
    """Write content/students.json under `root`, filling any field a caller
    doesn't care about with an innocuous default so tests stay short."""
    entries = []
    for student in students:
        student_id = student["id"]
        entries.append({
            "id": student_id,
            "displayName": student["displayName"],
            "aliases": student.get("aliases", []),
            "level": student.get("level", "4e"),
            "directory": student.get("directory", f"4e/04_NOMINATIFS/{student_id}"),
            "active": student.get("active", True),
            "sourceStudentReport": student.get("sourceStudentReport", "bilan-nexus-eleve.pdf"),
            "sourceParentReport": student.get("sourceParentReport", "bilan-nexus-parents.pdf"),
        })
    content_dir = root / "content"
    content_dir.mkdir(parents=True, exist_ok=True)
    (content_dir / "students.json").write_text(
        json.dumps({
            "schemaVersion": "nexus-students-v1",
            "scope": "stages_maths_2026",
            "students": entries,
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
