"""Canonical nominative student registry: single source of truth for PII detection,
nominative pack generation and private-link generation. Replaces the previous
hardcoded student name tuple in tools/build.py."""

from __future__ import annotations

import json
import unicodedata
from dataclasses import dataclass
from pathlib import Path

REGISTRY_RELATIVE_PATH = "content/students.json"
LEVELS = ("4e", "3e", "2nde", "1ere_spe")
EXPECTED_MARKDOWN_SUFFIXES = ("Dossier_Individuel", "Remediation_Ciblee")


class RegistryError(ValueError):
    """Raised when content/students.json fails validation."""


@dataclass(frozen=True)
class Student:
    id: str
    display_name: str
    aliases: tuple[str, ...]
    level: str
    directory: str
    active: bool
    source_student_report: str
    source_parent_report: str

    @property
    def names(self) -> tuple[str, ...]:
        """Every name form (display name + aliases) that must be treated as PII."""
        return (self.display_name, *self.aliases)


def normalize_name(value: str) -> str:
    """Casefold and Unicode-normalize a name for alias-insensitive comparison."""
    return unicodedata.normalize("NFC", value).casefold()


def normalize_text(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


def text_contains_name(text: str, name: str) -> bool:
    return normalize_name(name) in normalize_text(text)


def load_registry_raw(root: Path) -> dict[str, object]:
    path = root / REGISTRY_RELATIVE_PATH
    if not path.exists():
        raise RegistryError(f"Registre introuvable : {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise RegistryError(f"Registre JSON invalide : {error}") from error
    if data.get("schemaVersion") != "nexus-students-v1":
        raise RegistryError("schemaVersion inattendu dans content/students.json")
    if data.get("scope") != "stages_maths_2026":
        raise RegistryError("scope inattendu ou manquant dans content/students.json (attendu: 'stages_maths_2026')")
    if "students" not in data or not isinstance(data["students"], list):
        raise RegistryError("Clé 'students' manquante ou invalide")
    return data


def load_students(root: Path, *, validate_filesystem: bool = True) -> list[Student]:
    """Load and strictly validate the student registry.

    Raises RegistryError listing every problem found (not just the first one) so a
    broken registry fails the build with an actionable message.
    """
    data = load_registry_raw(root)
    errors: list[str] = []
    students: list[Student] = []
    seen_ids: set[str] = set()
    seen_display_names: set[str] = set()
    seen_directories: set[str] = set()
    all_alias_owners: dict[str, str] = {}

    for index, raw in enumerate(data["students"]):
        where = f"students[{index}]"
        required_fields = (
            "id", "displayName", "aliases", "level", "directory", "active",
            "sourceStudentReport", "sourceParentReport",
        )
        missing = [field for field in required_fields if field not in raw]
        if missing:
            errors.append(f"{where} : champs manquants {missing}")
            continue

        student_id = str(raw["id"])
        display_name = str(raw["displayName"])
        aliases = tuple(str(alias) for alias in raw["aliases"])
        level = str(raw["level"])
        directory = str(raw["directory"])
        active = bool(raw["active"])
        source_student_report = str(raw["sourceStudentReport"])
        source_parent_report = str(raw["sourceParentReport"])

        if student_id in seen_ids:
            errors.append(f"{where} : identifiant dupliqué '{student_id}'")
        seen_ids.add(student_id)

        display_key = normalize_name(display_name)
        if display_key in seen_display_names:
            errors.append(f"{where} : nom d'affichage dupliqué '{display_name}'")
        seen_display_names.add(display_key)

        if level not in LEVELS:
            errors.append(f"{where} : niveau invalide '{level}'")

        if directory in seen_directories:
            errors.append(f"{where} : répertoire dupliqué '{directory}'")
        seen_directories.add(directory)

        for alias in (display_name, *aliases):
            alias_key = normalize_name(alias)
            owner = all_alias_owners.get(alias_key)
            if owner is not None and owner != student_id:
                errors.append(
                    f"{where} : alias '{alias}' ambigu, déjà utilisé par '{owner}'"
                )
            all_alias_owners[alias_key] = student_id

        directory_path = root / directory
        if validate_filesystem:
            resolved_root = root.resolve()
            try:
                resolved_directory = directory_path.resolve(strict=False)
            except OSError:
                resolved_directory = directory_path
            if resolved_root not in resolved_directory.parents and resolved_directory != resolved_root:
                errors.append(f"{where} : répertoire hors racine du dépôt '{directory}'")
            if directory_path.is_symlink():
                errors.append(f"{where} : le répertoire est un lien symbolique '{directory}'")
            elif not directory_path.is_dir():
                errors.append(f"{where} : répertoire introuvable '{directory}'")
            else:
                markdown_files = sorted(p for p in directory_path.glob("*.md"))
                pdf_files = sorted(p for p in directory_path.glob("*.pdf"))
                symlinked = [p for p in (*markdown_files, *pdf_files) if p.is_symlink()]
                if symlinked:
                    errors.append(f"{where} : fichier(s) lien symbolique dans '{directory}'")
                if len(markdown_files) != 3:
                    errors.append(
                        f"{where} : {len(markdown_files)} fichier(s) Markdown au lieu de 3 exactement dans '{directory}'"
                    )
                if len(pdf_files) != 2:
                    errors.append(
                        f"{where} : {len(pdf_files)} PDF au lieu de 2 exactement dans '{directory}'"
                    )
                expected_pdfs = {source_student_report, source_parent_report}
                actual_pdf_names = {p.name for p in pdf_files}
                if expected_pdfs != actual_pdf_names:
                    errors.append(
                        f"{where} : PDF source déclarés {sorted(expected_pdfs)} "
                        f"différents des PDF présents {sorted(actual_pdf_names)}"
                    )

        students.append(Student(
            id=student_id, display_name=display_name, aliases=aliases, level=level,
            directory=directory, active=active,
            source_student_report=source_student_report,
            source_parent_report=source_parent_report,
        ))

    if validate_filesystem:
        declared_directories = {str(student.directory) for student in students}
        for level in LEVELS:
            level_nominatifs = root / level / "04_NOMINATIFS"
            if not level_nominatifs.exists():
                continue
            for entry in sorted(level_nominatifs.iterdir()):
                if not entry.is_dir():
                    continue
                relative = entry.relative_to(root).as_posix()
                if relative not in declared_directories:
                    errors.append(
                        f"Dossier nominatif non déclaré dans le registre : '{relative}'"
                    )

    if errors:
        raise RegistryError("Registre des élèves invalide :\n- " + "\n- ".join(errors))

    return students


def all_names(students: list[Student]) -> list[str]:
    """Every display name and alias across all students, for PII scanning."""
    names: list[str] = []
    for student in students:
        names.extend(student.names)
    return names
