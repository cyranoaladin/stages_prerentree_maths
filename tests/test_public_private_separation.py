"""No nominative alias -- for any of the 13 students -- may ever reach a document
that the catalog classifies as public. This is the confidentiality gate that keeps
the public portal free of student PII, checked directly against real repo content."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.build import ROOT, build_catalog, public_documents
from tools.student_registry import all_names, load_students, text_contains_name


def test_no_public_document_mentions_any_student_alias():
    students = load_students(ROOT, validate_filesystem=True)
    names = all_names(students)
    catalog = build_catalog(ROOT)

    offenders = []
    for document in public_documents(catalog):
        source = ROOT / str(document["source"])
        text = source.read_text(encoding="utf-8", errors="replace")
        for name in names:
            if text_contains_name(text, name):
                offenders.append((document["source"], name))

    assert offenders == []


def test_nominatif_directories_are_never_classified_public():
    catalog = build_catalog(ROOT)
    for document in catalog:
        if "04_NOMINATIFS" in Path(str(document["source"])).parts:
            assert document["confidential"] is True
            assert document not in public_documents(catalog)


def test_ines_and_elyes_are_absent_from_every_public_document():
    catalog = build_catalog(ROOT)
    public_sources = {str(document["source"]) for document in public_documents(catalog)}
    for source in public_sources:
        text = (ROOT / source).read_text(encoding="utf-8", errors="replace")
        assert not text_contains_name(text, "Ines KEFI")
        assert not text_contains_name(text, "Elyes KEFI")
