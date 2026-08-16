"""Ines KEFI (4e) and Elyes KEFI (3e) must be fully wired into the real repository
catalog: correctly classified, private-only, bucketed as nominatifs-prives, and
present in the canonical student registry."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.build import ROOT, build_catalog, document_bucket, document_pdf_path
from tools.student_registry import load_students

NEW_STUDENTS = {
    "ines-kefi": {
        "level": "4e",
        "directory": "4e/04_NOMINATIFS/Ines_Kefi",
        "stems": {
            "4e_Dossier_Individuel_Ines_Kefi",
            "4e_Remediation_Ciblee_Ines_Kefi_ELEVE",
            "4e_Remediation_Ciblee_Ines_Kefi_PROF_Corrige",
        },
    },
    "elyes-kefi": {
        "level": "3e",
        "directory": "3e/04_NOMINATIFS/Elyes_Kefi",
        "stems": {
            "3e_Dossier_Individuel_Elyes_Kefi",
            "3e_Remediation_Ciblee_Elyes_Kefi_ELEVE",
            "3e_Remediation_Ciblee_Elyes_Kefi_PROF_Corrige",
        },
    },
}


def test_new_students_are_declared_in_the_registry():
    students = {student.id: student for student in load_students(ROOT, validate_filesystem=True)}
    for student_id, expected in NEW_STUDENTS.items():
        assert student_id in students
        assert students[student_id].level == expected["level"]
        assert students[student_id].directory == expected["directory"]


def test_new_students_documents_are_private_nominative_and_bucketed():
    catalog = build_catalog(ROOT)
    for student_id, expected in NEW_STUDENTS.items():
        documents = [
            document for document in catalog
            if Path(str(document["source"])).stem in expected["stems"]
        ]
        assert len(documents) == 3, f"{student_id}: expected 3 operational Markdown, found {len(documents)}"
        for document in documents:
            assert document["level"] == expected["level"]
            assert document["confidential"] is True
            assert document["audience"] == "nominatif_prive"
            assert document["contains_pii"] is True
            assert document["session"] is None
            assert document_bucket(document) == "nominatifs-prives"
            assert document_pdf_path(document).parts[-2] == "nominatifs-prives"


def test_new_students_eleve_remediation_has_no_teacher_correction_leak():
    for student_id, expected in NEW_STUDENTS.items():
        eleve_path = ROOT / expected["directory"]
        candidates = list(eleve_path.glob("*_Remediation_Ciblee_*_ELEVE.md"))
        assert len(candidates) == 1
        text = candidates[0].read_text(encoding="utf-8")
        assert "Réponse attendue" not in text
        assert "VERSION ELEVE SANS CORRIGE" in text
