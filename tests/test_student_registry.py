from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from tests.helpers import write_minimal_registry
from tools.student_registry import RegistryError, load_students, normalize_name, text_contains_name


def make_student_dir(root: Path, directory: str, base_name: str) -> None:
    student_dir = root / directory
    student_dir.mkdir(parents=True)
    for suffix in ("Dossier_Individuel", "Remediation_Ciblee_ELEVE", "Remediation_Ciblee_PROF_Corrige"):
        (student_dir / f"{base_name}_{suffix}.md").write_text("# Document")
    (student_dir / "bilan-nexus-eleve.pdf").write_bytes(b"%PDF-1.4 fake")
    (student_dir / "bilan-nexus-parents.pdf").write_bytes(b"%PDF-1.4 fake")


def test_real_repository_registry_is_valid():
    students = load_students(Path(__file__).resolve().parents[1], validate_filesystem=True)
    assert len(students) == 13
    assert {student.id for student in students} >= {"ines-kefi", "elyes-kefi"}


def test_duplicate_id_is_rejected(tmp_path):
    write_minimal_registry(tmp_path, [
        {"id": "dup", "displayName": "A One", "directory": "4e/04_NOMINATIFS/A_One"},
        {"id": "dup", "displayName": "A Two", "directory": "4e/04_NOMINATIFS/A_Two"},
    ])
    with pytest.raises(RegistryError, match="dupliqué"):
        load_students(tmp_path, validate_filesystem=False)


def test_ambiguous_alias_across_students_is_rejected(tmp_path):
    write_minimal_registry(tmp_path, [
        {"id": "a", "displayName": "Student A", "aliases": ["Shared Name"]},
        {"id": "b", "displayName": "Student B", "aliases": ["Shared Name"]},
    ])
    with pytest.raises(RegistryError, match="ambigu"):
        load_students(tmp_path, validate_filesystem=False)


def test_invalid_level_is_rejected(tmp_path):
    write_minimal_registry(tmp_path, [{"id": "a", "displayName": "A", "level": "6e"}])
    with pytest.raises(RegistryError, match="niveau invalide"):
        load_students(tmp_path, validate_filesystem=False)


def test_missing_directory_fails_filesystem_validation(tmp_path):
    write_minimal_registry(tmp_path, [{
        "id": "a", "displayName": "A", "directory": "4e/04_NOMINATIFS/A",
    }])
    with pytest.raises(RegistryError, match="introuvable"):
        load_students(tmp_path, validate_filesystem=True)


def test_incomplete_student_directory_fails_validation(tmp_path):
    directory = "4e/04_NOMINATIFS/A_One"
    (tmp_path / directory).mkdir(parents=True)
    (tmp_path / directory / "only_one.md").write_text("# Doc")
    write_minimal_registry(tmp_path, [{
        "id": "a-one", "displayName": "A One", "directory": directory,
        "sourceStudentReport": "bilan-nexus-eleve.pdf", "sourceParentReport": "bilan-nexus-parents.pdf",
    }])
    with pytest.raises(RegistryError, match="Markdown"):
        load_students(tmp_path, validate_filesystem=True)


def test_undeclared_nominatif_directory_fails_validation(tmp_path):
    directory = "4e/04_NOMINATIFS/Declared_Student"
    make_student_dir(tmp_path, directory, "4e")
    write_minimal_registry(tmp_path, [{
        "id": "declared-student", "displayName": "Declared Student", "directory": directory,
        "sourceStudentReport": "bilan-nexus-eleve.pdf", "sourceParentReport": "bilan-nexus-parents.pdf",
    }])
    # An orphan directory nobody declared in the registry.
    make_student_dir(tmp_path, "4e/04_NOMINATIFS/Orphan_Student", "4e")

    with pytest.raises(RegistryError, match="non déclaré"):
        load_students(tmp_path, validate_filesystem=True)


def test_valid_registry_with_matching_filesystem_passes(tmp_path):
    directory = "4e/04_NOMINATIFS/Clean_Student"
    make_student_dir(tmp_path, directory, "4e")
    write_minimal_registry(tmp_path, [{
        "id": "clean-student", "displayName": "Clean Student", "directory": directory,
        "sourceStudentReport": "bilan-nexus-eleve.pdf", "sourceParentReport": "bilan-nexus-parents.pdf",
    }])

    students = load_students(tmp_path, validate_filesystem=True)

    assert len(students) == 1
    assert students[0].id == "clean-student"


def test_name_matching_is_case_and_unicode_insensitive():
    assert text_contains_name("Bilan de INES KEFI", "Ines Kefi")
    assert text_contains_name("bilan de ines kefi", "Ines KEFI")
    assert normalize_name("Ines KEFI") == normalize_name("ines kefi")
