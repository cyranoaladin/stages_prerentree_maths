# -*- coding: utf-8 -*-
"""Provenance de la copie source : identité, immutabilité, rattachement, sauvegarde.

Toutes les pièces manipulées ici sont fabriquées dans un répertoire temporaire par
``fabrique_pdf`` et ``fabrique_png``. Aucune copie réelle d'élève n'est lue, écrite
ou imitée : ces tests portent sur la mécanique de provenance, pas sur une correction.
"""

import hashlib
import json
import os
import struct
import zlib
from pathlib import Path

import pytest

from conftest import fill

ELEVE = "sinda-chikhaoui"
AUTRE_ELEVE = "fares-darghouth"


# ------------------------------------------------------------------ fixtures
def fabrique_pdf(chemin: Path, pages: int = 2) -> Path:
    """Un PDF minimal mais réellement valide, pour que ``pdfinfo`` sache le lire."""
    objets = []
    kids = " ".join("%d 0 R" % (3 + i) for i in range(pages))
    objets.append("<< /Type /Catalog /Pages 2 0 R >>")
    objets.append("<< /Type /Pages /Kids [%s] /Count %d >>" % (kids, pages))
    for _ in range(pages):
        objets.append("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] >>")
    corps, offsets = b"%PDF-1.4\n", []
    for numero, contenu in enumerate(objets, start=1):
        offsets.append(len(corps))
        corps += ("%d 0 obj\n%s\nendobj\n" % (numero, contenu)).encode("ascii")
    depart = len(corps)
    corps += ("xref\n0 %d\n" % (len(objets) + 1)).encode("ascii")
    corps += b"0000000000 65535 f \n"
    for offset in offsets:
        corps += ("%010d 00000 n \n" % offset).encode("ascii")
    corps += ("trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n"
              % (len(objets) + 1, depart)).encode("ascii")
    chemin.write_bytes(corps)
    return chemin


def fabrique_png(chemin: Path, gris: int = 128) -> Path:
    """Un PNG 1×1 réellement décodable, pour ne pas tester sur un fichier factice."""
    def bloc(nom, donnees):
        entete = struct.pack(">I", len(donnees)) + nom
        return entete + donnees + struct.pack(">I", zlib.crc32(nom + donnees) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 0, 0, 0, 0)
    idat = zlib.compress(bytes([0, gris]))
    chemin.write_bytes(b"\x89PNG\r\n\x1a\n" + bloc(b"IHDR", ihdr)
                       + bloc(b"IDAT", idat) + bloc(b"IEND", b""))
    return chemin


@pytest.fixture()
def mode_humain():
    from app import config
    avant = config.settings.correction_mode
    config.settings.correction_mode = "human"
    yield
    config.settings.correction_mode = avant


@pytest.fixture()
def mode_numerique():
    from app import config
    avant = config.settings.correction_mode
    config.settings.correction_mode = "digital"
    yield
    config.settings.correction_mode = avant


def _assessment(session, student_id):
    from app.models import Assessment
    return session.query(Assessment).filter_by(student_id=student_id).one()


def _detache_tout(session):
    """Remet la base de test à « aucune copie rattachée ».

    L'application n'offre aucun chemin de suppression — une pièce probante ne
    s'efface pas — donc ce nettoyage n'existe que pour isoler les tests entre eux.
    Il retire aussi les fichiers stockés : sans cela, chaque test hériterait des
    pièces du précédent et les décomptes de sauvegarde ne voudraient plus rien dire.
    """
    from app.domain import source_copy as sc
    from app.models import SourceCopy, SourceCopyFile
    for row in session.query(SourceCopyFile).all():
        chemin = sc.stored_path(row)
        if chemin.exists():
            chemin.chmod(0o600)
            chemin.unlink()
    session.query(SourceCopyFile).delete()
    session.query(SourceCopy).delete()
    session.flush()
    # SQLite réattribue les identifiants supprimés : un résidu sur disque ferait
    # collision au test suivant. L'application, elle, ne supprime jamais rien.
    import shutil as _shutil
    from app import config as _config
    racine = Path(_config.SOURCE_COPIES_DIR)
    if racine.exists():
        for enfant in racine.iterdir():
            _shutil.rmtree(enfant, ignore_errors=True)


# --------------------------------------------------------- 1. PDF, 2. images
def test_rattachement_pdf_valide(client, tmp_path):
    """1. Un PDF multipage se rattache, et sa pagination est relevée."""
    from app import database
    from app.domain import source_copy as sc
    source = fabrique_pdf(tmp_path / "copie_synthetique.pdf", pages=3)
    with database.session_scope() as session:
        _detache_tout(session)
        copy = sc.attach(session, _assessment(session, ELEVE), [source],
                         label="fixture synthétique")
        assert copy.status == "ATTACHED"
        assert copy.origin == "ORIGINAL"
        assert copy.source_kind == "REAL_STUDENT_COPY"
        assert copy.file_count == 1
        rows = sc.files_of(session, copy)
        assert [r.media_type for r in rows] == ["application/pdf"]
        import shutil
        if shutil.which("pdfinfo"):
            assert copy.page_count == 3
        _detache_tout(session)


def test_rattachement_de_plusieurs_images(client, tmp_path):
    """2. Trois photographies forment une copie de trois pages."""
    from app import database
    from app.domain import source_copy as sc
    pages = [fabrique_png(tmp_path / ("page_%d.png" % n), gris=n * 40) for n in (1, 2, 3)]
    with database.session_scope() as session:
        _detache_tout(session)
        copy = sc.attach(session, _assessment(session, ELEVE), pages)
        assert copy.file_count == 3
        assert copy.page_count == 3
        rows = sc.files_of(session, copy)
        assert [r.page_index for r in rows] == [1, 2, 3]
        assert {r.media_type for r in rows} == {"image/png"}
        _detache_tout(session)


# ------------------------------------------------------------------ 3. SHA256
def test_sha256_calcule_correctement(client, tmp_path):
    """3. L'empreinte enregistrée est celle du fichier fourni, recalculée à part."""
    from app import database
    from app.domain import source_copy as sc
    source = fabrique_pdf(tmp_path / "empreinte.pdf")
    attendu = hashlib.sha256(source.read_bytes()).hexdigest()
    with database.session_scope() as session:
        _detache_tout(session)
        copy = sc.attach(session, _assessment(session, ELEVE), [source])
        row = sc.files_of(session, copy)[0]
        assert row.sha256 == attendu
        assert row.byte_size == source.stat().st_size
        # et le fichier stocké porte bien les mêmes octets
        assert hashlib.sha256(sc.stored_path(row).read_bytes()).hexdigest() == attendu
        assert sc.verify(session, copy)["ok"] is True
        _detache_tout(session)


# ------------------------------------------------------- 4. ordre des pages
def test_ordre_des_pages_stable(client, tmp_path):
    """4. L'ordre est celui qui a été fourni, jamais celui du tri alphabétique."""
    from app import database
    from app.domain import source_copy as sc
    c = fabrique_png(tmp_path / "c_derniere.png", gris=30)
    a = fabrique_png(tmp_path / "a_premiere.png", gris=60)
    b = fabrique_png(tmp_path / "b_milieu.png", gris=90)
    fournis = [c, a, b]                     # volontairement pas dans l'ordre du nom
    with database.session_scope() as session:
        _detache_tout(session)
        copy = sc.attach(session, _assessment(session, ELEVE), fournis)
        rows = sc.files_of(session, copy)
        assert [r.original_name for r in rows] == [p.name for p in fournis]
        # relu depuis la base, l'ordre est le même
        described = sc.describe(session, _assessment(session, ELEVE))
        assert [f["page_index"] for f in described["files"]] == [1, 2, 3]
        assert [f["original_name"] for f in described["files"]] == [p.name for p in fournis]
        _detache_tout(session)


# ------------------------------------------- 5. mauvais assessment, 6. source absente
def test_mauvais_assessment_rejete(client, tmp_path):
    """5. On ne rattache pas une copie à un élève qui n'existe pas."""
    from app import database
    from app.domain import source_copy as sc
    source = fabrique_pdf(tmp_path / "orpheline.pdf")
    with database.session_scope() as session:
        with pytest.raises(sc.SourceCopyError):
            sc.attach(session, None, [source])
    from tools import attach_source_copy
    with pytest.raises(SystemExit):
        attach_source_copy.main(["eleve-qui-nexiste-pas", str(source)])


def test_source_inexistante_rejetee(client, tmp_path):
    """6. Un chemin qui ne désigne aucun fichier est refusé, sans rien écrire."""
    from app import database
    from app.domain import source_copy as sc
    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        with pytest.raises(sc.SourceCopyError):
            sc.attach(session, assessment, [tmp_path / "absente.pdf"])
        with pytest.raises(sc.SourceCopyError):
            sc.attach(session, assessment, [])
        assert sc.current_copy(session, assessment.assessment_id) is None


def test_format_non_reconnu_rejete(client, tmp_path):
    """Un fichier renommé « .pdf » sans en être un ne passe pas : les octets font foi."""
    from app import database
    from app.domain import source_copy as sc
    faux = tmp_path / "renomme.pdf"
    faux.write_bytes(b"ceci n'est pas un PDF")
    with database.session_scope() as session:
        with pytest.raises(sc.SourceCopyError):
            sc.attach(session, _assessment(session, ELEVE), [faux])


# ----------------------------------------------- 7. original intact, 8. lecture seule
def test_original_non_modifie(client, tmp_path):
    """7. Le fichier fourni par l'utilisateur n'est ni déplacé, ni réécrit."""
    from app import database
    from app.domain import source_copy as sc
    source = fabrique_pdf(tmp_path / "intacte.pdf")
    avant_octets = source.read_bytes()
    avant_sha = hashlib.sha256(avant_octets).hexdigest()
    avant_mtime = source.stat().st_mtime
    with database.session_scope() as session:
        _detache_tout(session)
        copy = sc.attach(session, _assessment(session, ELEVE), [source])
        assert source.exists(), "l'original ne doit pas être déplacé"
        assert source.read_bytes() == avant_octets
        assert hashlib.sha256(source.read_bytes()).hexdigest() == avant_sha
        assert source.stat().st_mtime == avant_mtime
        # la pièce stockée est une copie distincte, pas un lien vers l'original
        stocke = sc.stored_path(sc.files_of(session, copy)[0])
        assert stocke.resolve() != source.resolve()
        _detache_tout(session)


def test_piece_stockee_en_lecture_seule(client, tmp_path):
    """8. La pièce rattachée est en lecture seule et se sert telle quelle."""
    from app import database
    from app.domain import source_copy as sc
    source = fabrique_png(tmp_path / "lecture_seule.png")
    with database.session_scope() as session:
        _detache_tout(session)
        copy = sc.attach(session, _assessment(session, ELEVE), [source])
        stocke = sc.stored_path(sc.files_of(session, copy)[0])
        assert oct(stocke.stat().st_mode & 0o777) == "0o400"
        if os.geteuid() != 0:      # root ignore les permissions, et le dirait à tort
            with pytest.raises(PermissionError):
                with open(stocke, "ab") as f:
                    f.write(b"alteration")

    reponse = client.get("/eleve/%s/copie/page/1" % ELEVE)
    assert reponse.status_code == 200
    assert reponse.headers["content-type"].startswith("image/png")
    assert client.get("/eleve/%s/copie/page/7" % ELEVE).status_code == 404

    manifeste = client.get("/eleve/%s/copie/manifeste" % ELEVE).json()
    assert manifeste["attached"] is True
    assert manifeste["verification"]["ok"] is True
    assert manifeste["files"][0]["sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()

    with database.session_scope() as session:
        _detache_tout(session)


# -------------------------------------------------- 9. sauvegarde, 10. restauration
def test_sauvegarde_contient_la_copie_et_restaure_le_meme_sha256(client, tmp_path):
    """9 et 10. Les octets de la copie sont dans l'archive, et en ressortent identiques."""
    import zipfile
    from app import database
    from app.domain import source_copy as sc
    from tools import backup
    source = fabrique_pdf(tmp_path / "sauvegardee.pdf", pages=2)
    attendu = hashlib.sha256(source.read_bytes()).hexdigest()
    with database.session_scope() as session:
        _detache_tout(session)
        sc.attach(session, _assessment(session, ELEVE), [source])

    archive = tmp_path / "backup_test.zip"
    resultat = backup.create_backup(archive)
    assert resultat["copies_sources"] == 1

    with zipfile.ZipFile(archive) as zf:
        noms = zf.namelist()
        manifeste = json.loads(zf.read("BACKUP_MANIFEST.json").decode("utf-8"))
        entrees = [n for n in noms if n.startswith("source_copies/")]
        assert len(entrees) == 1
        assert hashlib.sha256(zf.read(entrees[0])).hexdigest() == attendu
    assert manifeste["copies_sources_total"] == 1
    assert manifeste["copies_sources"][0]["sha256"] == attendu

    controle = backup.verify_backup(archive)
    assert controle["ok"] is True, controle
    assert controle["verdict"] == "RESTORE VERIFIED"
    assert controle["copies_verifiees"] == 1
    assert controle["differentes"] == [] and controle["absentes"] == []

    with database.session_scope() as session:
        _detache_tout(session)


def test_restauration_detecte_une_archive_alteree(client, tmp_path):
    """La vérification n'est pas décorative : une archive touchée est signalée."""
    import zipfile
    from app import database
    from app.domain import source_copy as sc
    from tools import backup
    source = fabrique_png(tmp_path / "alteree.png")
    with database.session_scope() as session:
        _detache_tout(session)
        sc.attach(session, _assessment(session, ELEVE), [source])
    archive = backup.create_backup(tmp_path / "backup_altere.zip")["archive"]

    with zipfile.ZipFile(archive) as zf:
        contenu = {n: zf.read(n) for n in zf.namelist()}
    cible = next(n for n in contenu if n.startswith("source_copies/"))
    contenu[cible] = contenu[cible] + b"octet en trop"
    with zipfile.ZipFile(archive, "w") as zf:
        for nom, octets in contenu.items():
            zf.writestr(nom, octets)

    controle = backup.verify_backup(archive)
    assert controle["ok"] is False
    assert controle["verdict"] == "RESTORE FAILURE"
    assert len(controle["differentes"]) == 1

    with database.session_scope() as session:
        _detache_tout(session)


# ------------------------------------------------- 11. mode humain, 12. mode numérique
def test_correction_sans_copie_possible_en_mode_humain(client, mode_humain):
    """11. Le mode historique reste ouvert : la copie papier n'est pas une pièce jointe."""
    from app import database
    from app.domain import source_copy as sc
    with database.session_scope() as session:
        _detache_tout(session)
        assessment = _assessment(session, ELEVE)
        assert sc.current_copy(session, assessment.assessment_id) is None
        assert sc.guard(session, assessment) == []

    assert client.get("/eleve/%s" % ELEVE).status_code == 200
    reponse = client.post("/eleve/%s/critere/%s" % (ELEVE, "4E_SINDA_CHIKHAOUI_A1_c1"),
                          json={"score_centi": 100, "error_codes": []})
    assert reponse.status_code == 200, reponse.text
    described = client.get("/eleve/%s/copie/manifeste" % ELEVE).json()
    assert described["attached"] is False
    assert described["message"] == "Aucune copie élève rattachée."


def test_correction_numerique_refuse_de_demarrer_sans_source(client, mode_numerique):
    """12. En mode copie numérisée, pas de saisie tant qu'aucune source n'est rattachée."""
    from app import database
    from app.domain import source_copy as sc
    from app.domain import validation
    from app.domain import correction as corr
    with database.session_scope() as session:
        _detache_tout(session)
        assessment = _assessment(session, ELEVE)
        blocking = sc.guard(session, assessment)
        assert len(blocking) == 1
        assert "aucune copie élève n'est rattachée" in blocking[0]

    reponse = client.post("/eleve/%s/critere/%s" % (ELEVE, "4E_SINDA_CHIKHAOUI_A1_c1"),
                          json={"score_centi": 100, "error_codes": []})
    assert reponse.status_code == 409
    assert "copie élève" in reponse.json()["detail"]

    # et la validation refuse également, avec un problème explicitement identifié
    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        correction = corr.current_correction(session, assessment.assessment_id)
        problems = validation.validate(session, correction, assessment)
        assert any(p.code == "copie_source" for p in problems)


def test_mode_numerique_accepte_une_fois_la_copie_rattachee(client, tmp_path,
                                                            mode_numerique):
    """La porte s'ouvre dès que la pièce est là et que son empreinte se vérifie."""
    from app import database
    from app.domain import source_copy as sc
    from app.domain import validation
    from app.domain import correction as corr
    source = fabrique_pdf(tmp_path / "mode_numerique.pdf")
    with database.session_scope() as session:
        _detache_tout(session)
        sc.attach(session, _assessment(session, ELEVE), [source])

    assert client.get("/eleve/%s" % ELEVE).status_code == 200
    reponse = client.post("/eleve/%s/critere/%s" % (ELEVE, "4E_SINDA_CHIKHAOUI_A1_c1"),
                          json={"score_centi": 100, "error_codes": []})
    assert reponse.status_code == 200, reponse.text

    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        correction = corr.current_correction(session, assessment.assessment_id)
        problems = validation.validate(session, correction, assessment)
        assert not any(p.code == "copie_source" for p in problems)
        _detache_tout(session)


def test_mode_numerique_refuse_une_empreinte_qui_ne_se_verifie_plus(client, tmp_path,
                                                                    mode_numerique):
    """Une pièce dont les octets ont changé n'est plus une pièce probante."""
    from app import database
    from app.domain import source_copy as sc
    source = fabrique_png(tmp_path / "corrompue.png")
    with database.session_scope() as session:
        _detache_tout(session)
        copy = sc.attach(session, _assessment(session, ELEVE), [source])
        stocke = sc.stored_path(sc.files_of(session, copy)[0])

    stocke.chmod(0o600)                       # simule une altération hors application
    stocke.write_bytes(stocke.read_bytes() + b"\x00")
    stocke.chmod(0o400)

    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        copy = sc.current_copy(session, assessment.assessment_id)
        rapport = sc.verify(session, copy)
        assert rapport["ok"] is False
        assert len(rapport["changed"]) == 1
        blocking = sc.guard(session, assessment)
        assert len(blocking) == 1
        assert "ne se vérifie plus" in blocking[0]
        _detache_tout(session)


# ---------------------------------------------------- rattachement sans ambiguïté
def test_un_fichier_ne_se_rattache_pas_a_deux_eleves_sans_controle(client, tmp_path):
    """§7 : le même fichier chez deux élèves différents exige une décision explicite."""
    from app import database
    from app.domain import source_copy as sc
    source = fabrique_pdf(tmp_path / "partagee.pdf")
    with database.session_scope() as session:
        _detache_tout(session)
        sc.attach(session, _assessment(session, ELEVE), [source])
    with database.session_scope() as session:
        with pytest.raises(sc.SourceCopyError) as exc:
            sc.attach(session, _assessment(session, AUTRE_ELEVE), [source])
        assert "déjà rattaché à une autre évaluation" in str(exc.value)
    # la décision explicite, elle, passe
    with database.session_scope() as session:
        copy = sc.attach(session, _assessment(session, AUTRE_ELEVE), [source],
                         allow_shared=True, note="fixture : partage volontaire")
        assert copy.assessment_id.endswith(AUTRE_ELEVE)
        _detache_tout(session)


def test_meme_fichier_deux_fois_avertit_avant_de_passer(client, tmp_path):
    """Doublon : avertissement et confirmation, plutôt que rejet définitif.

    La doctrine a changé au terme de l'audit de fermeture. Deux pages identiques ne
    sont pas nécessairement une erreur — deux pages blanches d'un même scan le sont
    légitimement — et la provenance doit reproduire ce qui a été fourni. Le rejet sec
    d'origine faisait trancher le système à la place de l'utilisateur.
    """
    from app import database
    from app.domain import source_copy as sc
    source = fabrique_png(tmp_path / "doublon.png")
    with database.session_scope() as session:
        _detache_tout(session)
        with pytest.raises(sc.SourceCopyError) as exc:
            sc.attach(session, _assessment(session, ELEVE), [source, source])
        assert "DOUBLON DÉTECTÉ" in str(exc.value)
        assert "--autoriser-doublons" in str(exc.value)
        copy = sc.attach(session, _assessment(session, ELEVE), [source, source],
                         allow_duplicates=True)
        assert [r.page_index for r in sc.files_of(session, copy)] == [1, 2]
        _detache_tout(session)


def test_pdf_et_images_ne_se_melangent_pas(client, tmp_path):
    """Un rattachement porte un PDF ou des images, pas les deux."""
    from app import database
    from app.domain import source_copy as sc
    pdf = fabrique_pdf(tmp_path / "melange.pdf")
    png = fabrique_png(tmp_path / "melange.png")
    with database.session_scope() as session:
        _detache_tout(session)
        with pytest.raises(sc.SourceCopyError):
            sc.attach(session, _assessment(session, ELEVE), [pdf, png])
        with pytest.raises(sc.SourceCopyError):
            sc.attach(session, _assessment(session, ELEVE),
                      [pdf, fabrique_pdf(tmp_path / "second.pdf", pages=1)])


def test_remplacement_conserve_l_ancienne_piece(client, tmp_path):
    """Rien n'est écrasé : l'ancienne copie devient SUPERSEDED et reste consultable."""
    from app import database
    from app.domain import source_copy as sc
    from app.models import SourceCopy
    premiere = fabrique_pdf(tmp_path / "premiere.pdf")
    seconde = fabrique_pdf(tmp_path / "seconde.pdf", pages=4)
    with database.session_scope() as session:
        _detache_tout(session)
        assessment = _assessment(session, ELEVE)
        ancienne = sc.attach(session, assessment, [premiere])
        with pytest.raises(sc.SourceCopyError) as exc:
            sc.attach(session, assessment, [seconde])
        assert "déjà rattachée" in str(exc.value)
        nouvelle = sc.attach(session, assessment, [seconde], replace=True)
        assert nouvelle.source_copy_id != ancienne.source_copy_id
        assert session.get(SourceCopy, ancienne.source_copy_id).status == "SUPERSEDED"
        assert sc.current_copy(session, assessment.assessment_id).source_copy_id \
            == nouvelle.source_copy_id
        # les octets de l'ancienne pièce sont toujours là
        assert sc.stored_path(sc.files_of(session, ancienne)[0]).exists()
        _detache_tout(session)


def test_piece_derivee_pointe_vers_son_original(client, tmp_path):
    """§5 : une normalisation produit une pièce distincte, jamais un remplacement muet."""
    from app import database
    from app.domain import source_copy as sc
    original = fabrique_pdf(tmp_path / "original.pdf")
    normalise = fabrique_pdf(tmp_path / "normalise.pdf", pages=2)
    normalise.write_bytes(normalise.read_bytes() + b"%% variante\n")
    with database.session_scope() as session:
        _detache_tout(session)
        assessment = _assessment(session, ELEVE)
        source = sc.attach(session, assessment, [original])
        derivee = sc.attach(session, assessment, [normalise], replace=True,
                            derived_from=source)
        assert derivee.origin == "DERIVED"
        assert derivee.derived_from_id == source.source_copy_id
        # empreintes distinctes, et l'original est toujours intact sur le disque
        sha_original = sc.files_of(session, source)[0].sha256
        sha_derivee = sc.files_of(session, derivee)[0].sha256
        assert sha_original != sha_derivee
        assert sc.verify(session, source)["ok"] is True
        _detache_tout(session)


# -------------------------------------------------- 10. immutabilité en usage réel
def test_aucune_operation_de_correction_ne_touche_la_piece(client, tmp_path,
                                                           mode_humain):
    """§10 : saisir, valider et analyser ne modifient pas un octet de la copie."""
    from app import database
    from app.domain import source_copy as sc
    source = fabrique_pdf(tmp_path / "pendant_correction.pdf", pages=2)
    attendu = hashlib.sha256(source.read_bytes()).hexdigest()
    with database.session_scope() as session:
        _detache_tout(session)
        copy = sc.attach(session, _assessment(session, ELEVE), [source])
        stocke = sc.stored_path(sc.files_of(session, copy)[0])
        copy_id = copy.source_copy_id

    fill(client, ELEVE)
    assert client.post("/eleve/%s/valider" % ELEVE).status_code in (200, 303)
    client.get("/eleve/%s/analyse" % ELEVE)

    # et la génération des bilans, qui écrit dans runtime/build et runtime/reports
    import shutil as _shutil
    if _shutil.which("pdflatex"):
        from app.domain import reports as rep
        for kind in rep.REPORT_TYPES:
            client.get("/eleve/%s/bilan?type=%s" % (ELEVE, kind))
            reponse = client.post("/eleve/%s/bilan/%s/generer" % (ELEVE, kind), json={})
            assert reponse.status_code == 200, reponse.text[:300]

    assert hashlib.sha256(stocke.read_bytes()).hexdigest() == attendu
    assert oct(stocke.stat().st_mode & 0o777) == "0o400"
    with database.session_scope() as session:
        from app.models import SourceCopy
        assert sc.verify(session, session.get(SourceCopy, copy_id))["ok"] is True


def test_manifeste_relie_la_copie_a_la_correction(client, tmp_path):
    """§7 : « quelle copie a servi à cette correction ? » a une réponse complète."""
    from app import database
    from app.domain import source_copy as sc
    source = fabrique_pdf(tmp_path / "manifeste.pdf", pages=2)
    with database.session_scope() as session:
        _detache_tout(session)
        sc.attach(session, _assessment(session, ELEVE), [source], label="pièce pilote")

    described = client.get("/eleve/%s/copie/manifeste" % ELEVE).json()
    assert described["assessment_id"] == "asm-%s" % ELEVE
    assert described["correction_id"] is not None
    assert described["correction_revision"] is not None
    assert described["source_kind"] == "REAL_STUDENT_COPY"
    assert described["label"] == "pièce pilote"
    assert described["files"][0]["page_index"] == 1
    assert len(described["files"][0]["sha256"]) == 64
    assert described["verification"]["verdict"] == "EMPREINTE VÉRIFIÉE"

    with database.session_scope() as session:
        _detache_tout(session)


def test_journal_d_audit_enregistre_le_rattachement(client, tmp_path):
    """Le rattachement est un événement daté, pas un effet de bord silencieux."""
    from app import database
    from app.domain import source_copy as sc
    from app.models import AuditEvent
    source = fabrique_png(tmp_path / "auditee.png")
    with database.session_scope() as session:
        _detache_tout(session)
        copy = sc.attach(session, _assessment(session, ELEVE), [source])
        copy_id = copy.source_copy_id
    with database.session_scope() as session:
        # SQLite réattribue l'identifiant d'une pièce que le nettoyage de test a
        # supprimée : on prend le dernier événement, pas « le » seul.
        evenement = (session.query(AuditEvent)
                     .filter(AuditEvent.action == "source_copy.attached",
                             AuditEvent.object_id == str(copy_id))
                     .order_by(AuditEvent.id.desc()).first())
        assert evenement.assessment_id == "asm-%s" % ELEVE
        assert "1 fichier(s)" in evenement.new_value
        _detache_tout(session)


def test_l_ecran_supporte_un_probleme_sans_reference_d_item(client, mode_humain):
    """Régression : un problème « hors item » mêlé à des problèmes d'item faisait
    tomber l'écran de correction.

    Le gabarit regroupe les problèmes par référence d'item et sait afficher « hors
    item » ; mais trier un mélange de ``None`` et de chaînes lève une ``TypeError``.
    Le défaut préexistait — une empreinte de document altérée l'aurait déclenché — et
    le problème « copie source absente » le rendait systématique.
    """
    from app import config, database
    from app.domain import validation
    from app.domain import correction as corr
    with database.session_scope() as session:
        _detache_tout(session)

    # la correction s'ouvre en mode humain : elle existe, et ses lignes sont PENDING
    assert client.get("/eleve/%s" % AUTRE_ELEVE).status_code == 200
    # puis le mode numérique ajoute un problème sans référence d'item, aux côtés des
    # problèmes d'item déjà présents — c'est ce mélange qui faisait tomber l'écran
    config.settings.correction_mode = "digital"
    reponse = client.get("/eleve/%s" % AUTRE_ELEVE)
    assert reponse.status_code == 200, reponse.text[:400]
    assert "hors item" in reponse.text
    assert "Correction suspendue" in reponse.text

    with database.session_scope() as session:
        assessment = _assessment(session, AUTRE_ELEVE)
        correction = corr.get_or_create_correction(session, assessment)
        problems = validation.validate(session, correction, assessment)
        refs = {p.group_ref for p in problems}
        assert "" in refs and any(r for r in refs), "les deux natures doivent coexister"
        # la clé de regroupement se trie sans exception
        assert sorted(refs) == sorted(refs)
