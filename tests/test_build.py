from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.build import build_catalog, classify_document, is_a4_page, output_pdf_name, public_documents


def test_nominative_document_is_private_and_never_public():
    document = classify_document(
        Path("4e/04_NOMINATIFS/Sinda_Chikhaoui/4e_Dossier_Individuel_Sinda_Chikhaoui.md")
    )

    assert document["confidential"] is True
    assert document["audience"] == "nominatif_prive"
    assert public_documents([document]) == []


def test_student_and_teacher_documents_have_safe_pdf_names():
    student = classify_document(Path("3e/02_SEANCES/S2/3e_S2_ELEVE_Activite.md"))
    teacher = classify_document(Path("3e/02_SEANCES/S2/3e_S2_PROF_Fiche.md"))

    assert student["audience"] == "eleve"
    assert teacher["audience"] == "enseignant"
    assert student["type"] == "fiche_eleve"
    assert teacher["type"] == "fiche_professeur"
    assert output_pdf_name(student) == "3e_S2_ELEVE_Activite.pdf"
    assert output_pdf_name(teacher) == "3e_S2_PROF_Fiche.pdf"


def test_catalog_excludes_canonical_sources_and_private_names_from_public_site(tmp_path):
    (tmp_path / "4e/02_SEANCES/S1").mkdir(parents=True)
    (tmp_path / "4e/05_SOURCES").mkdir(parents=True)
    (tmp_path / "4e/02_SEANCES/S1/4e_S1_ELEVE_Activite.md").write_text("# Activité")
    (tmp_path / "4e/05_SOURCES/stage_prerentree_quatrieme_maths.md").write_text("# Source")
    (tmp_path / "4e/01_ENSEIGNANT").mkdir(parents=True)
    (tmp_path / "4e/01_ENSEIGNANT/4e_Guide_Formateur.md").write_text("Sinda Chikhaoui")

    catalog = build_catalog(tmp_path)

    assert len(catalog) == 2
    assert all("05_SOURCES" not in document["source"] for document in catalog)
    assert [document["source"] for document in public_documents(catalog)] == [
        "4e/02_SEANCES/S1/4e_S1_ELEVE_Activite.md"
    ]


def test_evaluations_keep_their_own_document_type():
    student = classify_document(Path("2nde/03_EVALUATIONS/2nde_Evaluation_Finale_ELEVE.md"))
    correction = classify_document(Path("2nde/03_EVALUATIONS/2nde_Evaluation_Finale_PROF_Corrige_Bareme.md"))

    assert student["type"] == "evaluation"
    assert correction["type"] == "evaluation"


def test_a4_tolerance_accepts_portrait_and_rejects_other_sizes():
    assert is_a4_page(595.28, 841.89)
    assert not is_a4_page(612, 792)
