# -*- coding: utf-8 -*-
"""Bilans : génération, provenance des textes, contenu, compilation PDF."""

import re
import shutil
import subprocess
from pathlib import Path

import pytest

from app import config, database
from app.models import Assessment, Report
from app.domain import correction as corr
from app.domain import reports as rep
from conftest import fill

STUDENT = "noa-maniaci"
LATEX_AVAILABLE = shutil.which(config.LATEX_ENGINE) is not None


@pytest.fixture(scope="module")
def prepared(client):
    fill(client, STUDENT)
    client.post("/eleve/%s/valider" % STUDENT, follow_redirects=False)
    client.get("/eleve/%s/bilan" % STUDENT)
    return STUDENT


def test_les_quatre_documents_existent():
    assert set(rep.REPORT_TYPES) == {"BILAN_PARENTS", "SYNTHESE_ENSEIGNANT",
                                     "PLAN_RENTREE", "FICHE_ELEVE"}
    for spec in rep.REPORT_TYPES.values():
        assert (config.LATEX_DIR / spec["template"]).exists()


def test_l_echappement_latex_neutralise_les_caracteres_speciaux():
    escaped = rep.latex_escape(r"100 % & $x^2$ #1 _test_ \commande {}")
    for dangereux in ("&", "%", "#", "_", "$"):
        assert ("\\" + dangereux) in escaped
    assert r"\textbackslash{}" in escaped


def test_un_bilan_ne_se_genere_pas_sans_correction_validee(client):
    student = "sinda-chikhaoui"
    client.get("/eleve/%s" % student)
    response = client.post("/eleve/%s/bilan/BILAN_PARENTS/generer" % student, json={})
    assert response.status_code == 409


def test_les_blocs_portent_leur_provenance(client, prepared):
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        report = (s.query(Report).filter_by(assessment_id=assessment.assessment_id,
                                            report_type="BILAN_PARENTS")
                  .order_by(Report.version.desc()).first())
        assert report is not None
        assert all(b.source == "deterministic" for b in report.blocks)
        assert not any(b.approved for b in report.blocks)


def test_une_modification_humaine_survit_a_une_regeneration(client, prepared):
    texte = "Formulation revue par l'enseignant, à conserver telle quelle."
    assert client.post("/eleve/%s/bilan/BILAN_PARENTS/bloc/points_forts" % STUDENT,
                       json={"content": texte, "approve": True}).status_code == 200
    body = client.post("/eleve/%s/bilan/BILAN_PARENTS/regenerer" % STUDENT, json={}).json()
    assert "points_forts" in body["blocs_conserves"]
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        report = (s.query(Report).filter_by(assessment_id=assessment.assessment_id,
                                            report_type="BILAN_PARENTS")
                  .order_by(Report.version.desc()).first())
        block = next(b for b in report.blocks if b.block_key == "points_forts")
        assert block.content == texte
        assert block.source == "human" and block.approved


def test_le_generateur_deterministe_suffit():
    from app.domain import narrative
    generator = narrative.get_generator("deterministic")
    assert generator.name == "deterministic"
    llm = narrative.LLMNarrativeGenerator()
    assert not llm.enabled()
    with pytest.raises(RuntimeError):
        llm.blocks("bilan_parents", {})


def test_la_pseudonymisation_retire_le_nom():
    from app.domain import narrative
    safe = narrative.LLMNarrativeGenerator.pseudonymise(
        {"first_name": "Ines", "display_name": "Ines KEFI",
         "analysis": {"student_name": "Ines KEFI", "student_id": "ines-kefi", "x": 1}})
    assert safe["display_name"] == "ÉLÈVE_01"
    assert "student_name" not in safe["analysis"]
    assert "student_id" not in safe["analysis"]


def test_la_compilation_n_utilise_jamais_un_shell():
    """Contrôle sur l'arbre syntaxique, pas sur le texte : un commentaire ne compte pas."""
    import ast
    for path in sorted(Path(config.APP_DIR).rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                nom = ast.unparse(node.func)
                assert nom not in ("os.system", "os.popen", "subprocess.getoutput"), path
                for kw in node.keywords:
                    if kw.arg == "shell":
                        assert isinstance(kw.value, ast.Constant) and kw.value.value is False, \
                            path
    source = (Path(config.APP_DIR) / "security.py").read_text(encoding="utf-8")
    assert "shell=False" in source


def test_le_nom_de_fichier_est_assaini():
    from app.security import safe_slug
    assert safe_slug("Ahmed BAKIR") == "AHMED_BAKIR"
    assert safe_slug("../../etc/passwd") == "ETC_PASSWD"
    assert safe_slug("") == "SANS_NOM"
    assert ";" not in safe_slug("rm -rf /; echo")


@pytest.mark.skipif(not LATEX_AVAILABLE, reason="moteur LaTeX absent de cette machine")
def test_les_quatre_pdf_compilent_et_ne_fuient_rien(client, prepared):
    produits = {}
    for kind in rep.REPORT_TYPES:
        client.get("/eleve/%s/bilan?type=%s" % (STUDENT, kind))
        response = client.post("/eleve/%s/bilan/%s/generer" % (STUDENT, kind), json={})
        assert response.status_code == 200, response.text
        produits[kind] = response.json()["report_id"]

    with database.session_scope() as s:
        for kind, report_id in produits.items():
            report = s.get(Report, report_id)
            assert report.pdf_path and Path(report.pdf_path).exists()
            assert report.pdf_sha256 and report.manifest_path
            assert Path(report.manifest_path).exists()

    if shutil.which("pdftotext") is None:
        pytest.skip("pdftotext absent : le contenu n'est pas relu")

    with database.session_scope() as s:
        parents = s.get(Report, produits["BILAN_PARENTS"])
        texte = subprocess.run(["pdftotext", "-layout", parents.pdf_path, "-"],
                               capture_output=True, text=True, check=True).stdout
    interdits = ["mastery_delta", "criterion_id", "skill_id", "analysis_sha256",
                 "n_minus_1", "bridge_n", "{", "}", "lacune", "non acquis"]
    for mot in interdits:
        assert mot not in texte, mot
    assert not re.search(r"progression de \d", texte, re.I)
    assert not re.search(r"\+\s?\d+\s?%", texte)
    assert "score brut au sujet de clôture" in texte.lower()
    assert "aucune progression chiffrée" in texte.lower()


@pytest.mark.skipif(not LATEX_AVAILABLE, reason="moteur LaTeX absent de cette machine")
def test_un_bilan_approuve_n_est_pas_ecrase_silencieusement(client, prepared):
    assert client.post("/eleve/%s/bilan/BILAN_PARENTS/approuver" % STUDENT,
                       json={}).status_code == 200
    refus = client.post("/eleve/%s/bilan/BILAN_PARENTS/bloc/points_forts" % STUDENT,
                        json={"content": "autre texte"})
    assert refus.status_code == 409
    body = client.post("/eleve/%s/bilan/BILAN_PARENTS/regenerer" % STUDENT, json={}).json()
    assert body["version"] == 2
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        versions = (s.query(Report)
                    .filter_by(assessment_id=assessment.assessment_id,
                               report_type="BILAN_PARENTS").all())
        assert len(versions) == 2
        approuve = next(r for r in versions if r.version == 1)
        assert approuve.status == "APPROVED"
        nouvelle = next(r for r in versions if r.version == 2)
        conserve = next(b for b in nouvelle.blocks if b.block_key == "points_forts")
        assert conserve.source == "human"


def test_la_fiche_eleve_parle_a_un_eleve(client, prepared):
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        report = (s.query(Report).filter_by(assessment_id=assessment.assessment_id,
                                            report_type="FICHE_ELEVE")
                  .order_by(Report.version.desc()).first())
        if report is None:
            pytest.skip("fiche non générée")
        contenu = " ".join(b.content for b in report.blocks)
        titres = " ".join(b.title for b in report.blocks)
    for jargon in ("evidence_strength", "curriculum_scope", "skill_id", "n_minus_1",
                   "docimolog", "criterion"):
        assert jargon not in contenu
    assert "objectif" in titres.lower()
    assert "Ce que je sais bien faire" in titres
    assert "Ma méthode" in titres
