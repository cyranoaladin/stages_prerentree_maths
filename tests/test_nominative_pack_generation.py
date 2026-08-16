"""End-to-end pack generation for a nominative student, run against the real Ines
KEFI / Elyes KEFI source documents but redirected to a throwaway dist/ directory so
running the test suite never mutates the committed build output."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import build as build_module
from tools.build import ROOT, build_catalog, build_html, build_pdf, build_packs, is_individual_student_doc


def test_ines_and_elyes_produce_complete_nominative_packs(tmp_path, monkeypatch):
    monkeypatch.setattr(build_module, "DIST", tmp_path / "dist")
    monkeypatch.setattr(build_module, "write_catalog", lambda catalog: None)

    full_catalog = build_catalog(ROOT)
    reduced = [
        document for document in full_catalog
        if is_individual_student_doc(document)
        and ("Ines_Kefi" in str(document["source"]) or "Elyes_Kefi" in str(document["source"]))
    ]
    assert len(reduced) == 6

    build_html(reduced, clean=True)
    build_pdf(reduced, clean=True)
    packs = build_packs(reduced, clean=True)

    pack_names = {pack.name for pack in packs}
    for level, slug in (("4e", "Ines_Kefi"), ("3e", "Elyes_Kefi")):
        work_pack = f"{level}_{slug}_PACK_TRAVAIL_PERSONNALISE.pdf"
        teacher_pack = f"{level}_{slug}_DOSSIER_ENSEIGNANT_CONFIDENTIEL.pdf"
        assert work_pack in pack_names
        assert teacher_pack in pack_names

    nominatifs_dir = (tmp_path / "dist" / "packs" / "nominatifs-prives")
    assert nominatifs_dir.is_dir()
    for pack in packs:
        assert pack.parent == nominatifs_dir
        assert pack.stat().st_size > 0
