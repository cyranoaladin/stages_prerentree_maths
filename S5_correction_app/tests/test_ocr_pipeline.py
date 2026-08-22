# -*- coding: utf-8 -*-
"""Téléversement, rastérisation et lecture assistée — hors ligne.

Aucun test de ce fichier n'appelle OpenRouter. Le client est simulé : ce qui est
éprouvé ici, c'est la plomberie — la charge utile envoyée, les contraintes de
confidentialité, la validation du schéma, la double lecture, la réconciliation, la
revue humaine, le cache, les erreurs d'API et la provenance.

La qualité réelle de la reconnaissance d'écriture manuscrite **ne peut pas** être
mesurée ici : les fixtures sont typographiques. Elle se mesurera sur des pages
manuscrites réelles comparées à une transcription humaine, et pas avant.

Aucune donnée d'Inès n'est touchée.
"""

import hashlib
import json
import struct
import zlib
from pathlib import Path

import pytest

ELEVE = "sinda-chikhaoui"


# ------------------------------------------------------------------ fixtures
def fabrique_pdf(chemin: Path, pages: int = 2) -> Path:
    objets = ["<< /Type /Catalog /Pages 2 0 R >>",
              "<< /Type /Pages /Kids [%s] /Count %d >>"
              % (" ".join("%d 0 R" % (3 + i) for i in range(pages)), pages)]
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


def fabrique_png(chemin: Path, gris: int = 128, largeur: int = 4) -> Path:
    def bloc(nom, donnees):
        return (struct.pack(">I", len(donnees)) + nom + donnees
                + struct.pack(">I", zlib.crc32(nom + donnees) & 0xFFFFFFFF))
    ihdr = struct.pack(">IIBBBBB", largeur, 1, 8, 0, 0, 0, 0)
    idat = zlib.compress(bytes([0] + [gris] * largeur))
    chemin.write_bytes(b"\x89PNG\r\n\x1a\n" + bloc(b"IHDR", ihdr)
                       + bloc(b"IDAT", idat) + bloc(b"IEND", b""))
    return chemin


class FauxFichier:
    """Ce que FastAPI passe à la couche d'ingestion, sans serveur HTTP."""

    def __init__(self, path):
        self.filename = Path(path).name
        self.file = open(path, "rb")

    def close(self):
        self.file.close()


# -------------------------------------------------- client OpenRouter simulé
class FauxClient:
    """Client de substitution. Enregistre tout ce qui lui est demandé.

    Il rejoue des réponses préparées : la plomberie est éprouvée sans appel réseau,
    et les tests restent déterministes.
    """

    def __init__(self, reponses=None):
        self.reponses = list(reponses or [])
        self.appels = []
        self.erreurs = []

    def chat(self, messages, model, response_format=None, temperature=0, **kwargs):
        from app.domain import openrouter
        self.appels.append({"messages": messages, "model": model,
                            "response_format": response_format,
                            "temperature": temperature, "kwargs": kwargs})
        if self.erreurs:
            raise self.erreurs.pop(0)
        if not self.reponses:
            raise AssertionError("le client simulé n'a plus de réponse préparée")
        parsed = self.reponses.pop(0)
        return openrouter.Completion(
            content=json.dumps(parsed, ensure_ascii=False), parsed=parsed,
            model_id=model, provider_name="FournisseurSimulé",
            generation_id="gen-test", request_id="req-test", latency_ms=42,
            usage=openrouter.Usage(tokens_in=1200, tokens_out=300, cost_usd=0.004),
            raw={"model": model})


def page_primary(page_index=1):
    """Une transcription plausible, avec une erreur d'élève délibérément conservée."""
    return {
        "page_index": page_index,
        "orientation": "UPRIGHT",
        "page_note": None,
        "blocks": [
            {"block_id": "b001", "item_ref": "A1", "origin": "PRINTED", "kind": "TEXT",
             "status": "ACTIVE", "verbatim": "Calculer (-8) + 3 - (-5).",
             "latex": None, "uncertainty": "LOW", "alternatives": [], "notes": None,
             "bbox": None},
            # L'élève a écrit un résultat faux. La transcription le conserve tel quel.
            {"block_id": "b002", "item_ref": "A1", "origin": "HANDWRITTEN",
             "kind": "MATH", "status": "ACTIVE",
             "verbatim": "-8 + 3 - (-5) = -10", "latex": "-8 + 3 - (-5) = -10",
             "uncertainty": "LOW", "alternatives": [], "notes": None, "bbox": None},
            {"block_id": "b003", "item_ref": "A2", "origin": "HANDWRITTEN",
             "kind": "MATH", "status": "CROSSED_OUT",
             "verbatim": "5/8 - 1/4 = 4/4", "latex": "\\frac{5}{8}-\\frac{1}{4}=\\frac{4}{4}",
             "uncertainty": "MEDIUM", "alternatives": ["4/4", "4/8"],
             "notes": "barré d'un trait", "bbox": None},
            {"block_id": "b004", "item_ref": "A2", "origin": "HANDWRITTEN",
             "kind": "MATH", "status": "ACTIVE",
             "verbatim": "3/8", "latex": "\\frac{3}{8}", "uncertainty": "HIGH",
             "alternatives": ["3/8", "5/8"], "notes": "chiffre du numérateur douteux",
             "bbox": None},
        ],
    }


def page_blind(page_index=1, divergence=None, omet=None):
    """Seconde lecture, indépendante : ses identifiants de bloc lui sont propres.

    Elle n'a pas vu la première ; le rapprochement se fait localement, sur le texte
    puis sur (item, nature). ``divergence`` fait lire autrement un bloc, ``omet`` le
    fait disparaître — deux situations qui doivent remonter à l'humain.
    """
    modele = page_primary(page_index)
    blocs = []
    for index, bloc in enumerate(modele["blocks"], start=1):
        copie = dict(bloc)
        copie["block_id"] = "z%03d" % index          # identifiants propres à cette lecture
        if omet and bloc["block_id"] == omet:
            continue
        if divergence and bloc["block_id"] == divergence:
            copie["verbatim"] = "-8 + 3 - (-5) = -1"
            copie["latex"] = "-8 + 3 - (-5) = -1"
        blocs.append(copie)
    modele["blocks"] = blocs
    return modele


# ------------------------------------------------------------------- outils
def _assessment(session, student_id=ELEVE):
    from app.models import Assessment
    return session.query(Assessment).filter_by(student_id=student_id).one()


def _remise_a_zero(session):
    from app.domain import source_copy as sc
    from app.models import (OcrPage, OcrRun, PageAttestation, SourceCopy,
                            SourceCopyFile, TranscriptionBlock,
                            TranscriptionBlockHistory, TranscriptionState)
    for row in session.query(SourceCopyFile).all():
        chemin = sc.stored_path(row)
        if chemin.exists():
            chemin.chmod(0o600)
            chemin.unlink()
    session.query(OcrPage).delete()
    session.query(TranscriptionBlockHistory).delete()
    session.query(PageAttestation).delete()
    session.query(TranscriptionBlock).delete()
    session.query(TranscriptionState).delete()
    session.query(OcrRun).delete()
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


def _vider_cache():
    from app import config
    for path in Path(config.OCR_CACHE_DIR).glob("*.json"):
        path.unlink()


@pytest.fixture()
def copie_pdf(client, tmp_path):
    """Une copie synthétique de deux pages, rattachée puis rendue."""
    from app import database
    from app.domain import source_copy as sc
    source = fabrique_pdf(tmp_path / "copie_synthetique.pdf", pages=2)
    with database.session_scope() as session:
        _remise_a_zero(session)
        sc.attach(session, _assessment(session), [source], label="fixture OCR",
                  is_synthetic=True)
    _vider_cache()
    yield source
    with database.session_scope() as session:
        _remise_a_zero(session)
    _vider_cache()


# =================================================== 1. téléversement web
def test_televersement_pdf_multipage(client, tmp_path):
    from app import database
    from app.domain import upload as up
    source = fabrique_pdf(tmp_path / "scan_complet.pdf", pages=5)
    with database.session_scope() as session:
        _remise_a_zero(session)
        assessment = _assessment(session)
        fichier = FauxFichier(source)
        try:
            resultat = up.ingest(session, assessment, [fichier], label="scan", is_synthetic=True)
        finally:
            fichier.close()
        assert resultat["file_count"] == 1
        assert resultat["page_count"] == 5
        assert resultat["files"][0]["media_type"] == "application/pdf"
        assert resultat["files"][0]["sha256"] == \
            hashlib.sha256(source.read_bytes()).hexdigest()
        _remise_a_zero(session)


def test_televersement_lot_d_images_conserve_l_ordre(client, tmp_path):
    """L'ordre reçu est l'ordre des pages : il n'est jamais retrié par le serveur."""
    from app import database
    from app.domain import upload as up
    from app.domain import source_copy as sc
    c = fabrique_png(tmp_path / "zzz_derniere.png", gris=10)
    a = fabrique_png(tmp_path / "aaa_premiere.png", gris=60)
    b = fabrique_png(tmp_path / "mmm_milieu.png", gris=120)
    fournis = [c, a, b]                     # volontairement contraire à l'ordre du nom
    with database.session_scope() as session:
        _remise_a_zero(session)
        assessment = _assessment(session)
        fichiers = [FauxFichier(p) for p in fournis]
        try:
            resultat = up.ingest(session, assessment, fichiers, is_synthetic=True)
        finally:
            for f in fichiers:
                f.close()
        assert resultat["page_count"] == 3
        assert [f["original_name"] for f in resultat["files"]] == [p.name for p in fournis]
        copy = sc.current_copy(session, assessment.assessment_id)
        assert [r.page_index for r in sc.files_of(session, copy)] == [1, 2, 3]
        _remise_a_zero(session)


def test_televersement_refuse_un_fichier_deguise(client, tmp_path):
    """Ni le nom, ni l'extension, ni le type annoncé ne font foi : seuls les octets."""
    from app import database
    from app.domain import upload as up
    faux = tmp_path / "copie.pdf"
    faux.write_bytes(b"MZ\x90\x00 ceci est un executable, pas un PDF")
    with database.session_scope() as session:
        _remise_a_zero(session)
        fichier = FauxFichier(faux)
        try:
            with pytest.raises(up.UploadError) as exc:
                up.ingest(session, _assessment(session), [fichier])
        finally:
            fichier.close()
        assert "format accepté" in str(exc.value)


def test_televersement_refuse_un_fichier_vide(client, tmp_path):
    from app import database
    from app.domain import upload as up
    vide = tmp_path / "vide.pdf"
    vide.write_bytes(b"")
    with database.session_scope() as session:
        fichier = FauxFichier(vide)
        try:
            with pytest.raises(up.UploadError) as exc:
                up.ingest(session, _assessment(session), [fichier])
        finally:
            fichier.close()
        assert "vide" in str(exc.value)


def test_televersement_respecte_le_plafond_de_taille(client, tmp_path, monkeypatch):
    from app import config, database
    from app.domain import upload as up
    monkeypatch.setattr(config, "UPLOAD_MAX_BYTES", 256)
    gros = fabrique_pdf(tmp_path / "gros.pdf", pages=40)
    assert gros.stat().st_size > 256
    with database.session_scope() as session:
        fichier = FauxFichier(gros)
        try:
            with pytest.raises(up.UploadError) as exc:
                up.ingest(session, _assessment(session), [fichier])
        finally:
            fichier.close()
        assert "limite" in str(exc.value)


def test_televersement_refuse_trop_de_pages(client, tmp_path, monkeypatch):
    from app import config, database
    from app.domain import upload as up
    monkeypatch.setattr(config, "UPLOAD_MAX_PAGES", 3)
    source = fabrique_pdf(tmp_path / "long.pdf", pages=9)
    with database.session_scope() as session:
        _remise_a_zero(session)
        fichier = FauxFichier(source)
        try:
            with pytest.raises(up.UploadError) as exc:
                up.ingest(session, _assessment(session), [fichier])
        finally:
            fichier.close()
        assert "au-delà de la limite" in str(exc.value)


def test_televersement_refuse_le_melange_pdf_et_images(client, tmp_path):
    from app import database
    from app.domain import upload as up
    pdf = fabrique_pdf(tmp_path / "melange.pdf")
    png = fabrique_png(tmp_path / "melange.png")
    with database.session_scope() as session:
        _remise_a_zero(session)
        fichiers = [FauxFichier(pdf), FauxFichier(png)]
        try:
            with pytest.raises(up.UploadError) as exc:
                up.ingest(session, _assessment(session), fichiers)
        finally:
            for f in fichiers:
                f.close()
        assert "soit un PDF, soit des images" in str(exc.value)


def test_un_echec_ne_laisse_aucune_ligne_derriere_lui(client, tmp_path):
    """Ingestion atomique : pas d'état intermédiaire à moitié rattaché."""
    from app import database
    from app.domain import upload as up
    from app.domain import source_copy as sc
    bon = fabrique_png(tmp_path / "page1.png")
    mauvais = tmp_path / "page2.txt"
    mauvais.write_bytes(b"du texte, pas une image")
    with database.session_scope() as session:
        _remise_a_zero(session)
        assessment = _assessment(session)
        fichiers = [FauxFichier(bon), FauxFichier(mauvais)]
        try:
            with pytest.raises(up.UploadError):
                up.ingest(session, assessment, fichiers)
        finally:
            for f in fichiers:
                f.close()
        assert sc.current_copy(session, assessment.assessment_id) is None
        from app.models import SourceCopyFile
        assert session.query(SourceCopyFile).count() == 0


def test_route_de_televersement(client, tmp_path):
    """Le chemin HTTP complet, multipart compris."""
    from app import database
    with database.session_scope() as session:
        _remise_a_zero(session)
    source = fabrique_pdf(tmp_path / "via_http.pdf", pages=3)
    with open(source, "rb") as f:
        reponse = client.post("/eleve/%s/copie/televerser" % ELEVE,
                              files=[("fichiers", ("via_http.pdf", f,
                                                   "application/pdf"))],
                              data={"libelle": "envoi web"})
    assert reponse.status_code == 200, reponse.text
    corps = reponse.json()
    assert corps["page_count"] == 3
    assert corps["manifeste"]["verification"]["ok"] is True
    assert corps["manifeste"]["label"] == "envoi web"

    manifeste = client.get("/eleve/%s/copie/manifeste" % ELEVE).json()
    assert manifeste["attached"] is True
    assert manifeste["limites"]["max_pages"] >= 1
    with database.session_scope() as session:
        _remise_a_zero(session)


# ======================================================= 2. rastérisation
def test_rasterisation_produit_des_pages_derivees(client, copie_pdf):
    from app import config, database
    from app.domain import rasterize
    from app.domain import source_copy as sc
    with database.session_scope() as session:
        assessment = _assessment(session)
        derived = rasterize.render_pages(session, assessment)
        assert derived.origin == "DERIVED"
        assert derived.source_kind == sc.DERIVED_PAGE_IMAGES
        original = sc.current_copy(session, assessment.assessment_id)
        assert derived.derived_from_id == original.source_copy_id
        rows = sc.files_of(session, derived)
        assert len(rows) == 2
        for row in rows:
            assert row.media_type == "image/png"
            assert row.dpi == config.RASTER_DPI
            assert row.width_px and row.height_px
            assert len(row.sha256) == 64
            assert oct(sc.stored_path(row).stat().st_mode & 0o777) == "0o400"
        # empreintes distinctes de l'original : ce sont d'autres octets
        assert {r.sha256 for r in rows}.isdisjoint(
            {r.sha256 for r in sc.files_of(session, original)})


def test_les_pages_derivees_n_eclipsent_pas_la_piece_probante(client, copie_pdf):
    """current_copy doit continuer de désigner l'original, jamais les rendus."""
    from app import database
    from app.domain import rasterize
    from app.domain import source_copy as sc
    with database.session_scope() as session:
        assessment = _assessment(session)
        avant = sc.current_copy(session, assessment.assessment_id)
        rasterize.render_pages(session, assessment)
        apres = sc.current_copy(session, assessment.assessment_id)
        assert apres.source_copy_id == avant.source_copy_id
        assert apres.source_kind == sc.REAL_STUDENT_COPY
        assert apres.origin == "ORIGINAL"


def test_rasterisation_idempotente_sauf_demande_explicite(client, copie_pdf):
    from app import database
    from app.domain import rasterize
    with database.session_scope() as session:
        assessment = _assessment(session)
        premier = rasterize.render_pages(session, assessment)
        second = rasterize.render_pages(session, assessment)
        assert second.source_copy_id == premier.source_copy_id
        refait = rasterize.render_pages(session, assessment, force=True)
        assert refait.source_copy_id != premier.source_copy_id
        from app.models import SourceCopy
        assert session.get(SourceCopy, premier.source_copy_id).status == "SUPERSEDED"


def test_l_original_reste_intact_apres_rasterisation(client, copie_pdf):
    from app import database
    from app.domain import rasterize
    from app.domain import source_copy as sc
    attendu = hashlib.sha256(copie_pdf.read_bytes()).hexdigest()
    with database.session_scope() as session:
        assessment = _assessment(session)
        original = sc.current_copy(session, assessment.assessment_id)
        rasterize.render_pages(session, assessment)
        assert sc.verify(session, original)["ok"] is True
        assert sc.files_of(session, original)[0].sha256 == attendu
        assert copie_pdf.read_bytes() and \
            hashlib.sha256(copie_pdf.read_bytes()).hexdigest() == attendu


# ============================================== 3. confidentialité OpenRouter
def test_la_cle_n_est_jamais_exposee(client, monkeypatch):
    from app.domain import openrouter
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-secret-de-test-0123456789")
    statut = openrouter.configuration_status()
    assert statut["configured"] is True
    assert statut["label"] == "OpenRouter : configuré"
    serialise = json.dumps(statut, ensure_ascii=False)
    assert "sk-or" not in serialise
    assert "secret-de-test" not in serialise
    # la rédaction masque la clé partout où elle pourrait fuiter
    assert "sk-or" not in openrouter.redact(
        "échec avec la clé sk-or-v1-secret-de-test-0123456789")


def test_cle_absente_signalee_sans_planter(client, monkeypatch):
    from app.domain import openrouter
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    statut = openrouter.configuration_status()
    assert statut["configured"] is False
    assert statut["label"] == "OpenRouter : clé absente"
    with pytest.raises(openrouter.MissingKeyError):
        openrouter.chat([{"role": "user", "content": "bonjour"}], model="test/modele")


def test_fichier_de_cle_trop_permissif_refuse(client, monkeypatch, tmp_path):
    from app import config
    from app.domain import openrouter
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    fichier = tmp_path / "openrouter.key"
    fichier.write_text("sk-or-v1-abcdef0123456789", encoding="utf-8")
    fichier.chmod(0o644)
    monkeypatch.setattr(config, "OPENROUTER_KEY_FILE", fichier)
    assert openrouter.is_configured() is False
    fichier.chmod(0o600)
    assert openrouter.is_configured() is True


def test_les_contraintes_de_confidentialite_sont_toujours_envoyees(client, copie_pdf,
                                                                   monkeypatch):
    """ZDR et data_collection=deny partent avec chaque appel, sans exception."""
    from app.domain import openrouter
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-test")

    captures = {}

    def faux_post(self, url, headers=None, json=None):
        captures["url"] = url
        captures["body"] = json
        captures["headers"] = headers
        raise RuntimeError("interception volontaire")

    import httpx
    monkeypatch.setattr(httpx.Client, "post", faux_post)
    with pytest.raises(Exception):
        openrouter.chat([{"role": "user", "content": "x"}], model="test/modele",
                        max_retries=0)

    assert captures["body"]["provider"] == {
        "data_collection": "deny", "zdr": True,
        "require_parameters": True, "allow_fallbacks": False}
    assert captures["body"]["usage"] == {"include": True}
    assert captures["headers"]["Authorization"].startswith("Bearer ")


def test_absence_d_endpoint_conforme_echoue_sans_repli(client, monkeypatch):
    """Aucun reroutage vers un fournisseur qui conserverait les données."""
    from app.domain import openrouter
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-test")

    class FausseReponse:
        status_code = 404
        text = '{"error":{"message":"No endpoints found matching your data policy (zdr)"}}'
        headers = {}

    def faux_post(self, url, headers=None, json=None):
        return FausseReponse()

    import httpx
    monkeypatch.setattr(httpx.Client, "post", faux_post)
    with pytest.raises(openrouter.NoCompliantEndpointError) as exc:
        openrouter.chat([{"role": "user", "content": "x"}], model="test/modele")
    assert "refusé plutôt que rerouté" in str(exc.value)


@pytest.mark.parametrize("statut,doit_reessayer", [
    (429, True), (500, True), (502, True), (503, True), (408, True),
    (401, False), (403, False), (413, False), (422, False)])
def test_politique_de_reprise_selon_le_code(client, monkeypatch, statut, doit_reessayer):
    from app.domain import openrouter
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-test")
    monkeypatch.setattr(openrouter, "_sleep", lambda s: None)
    appels = {"n": 0}

    class FausseReponse:
        def __init__(self, code):
            self.status_code = code
            self.text = '{"error":"panne simulée"}'
            self.headers = {}

    def faux_post(self, url, headers=None, json=None):
        appels["n"] += 1
        return FausseReponse(statut)

    import httpx
    monkeypatch.setattr(httpx.Client, "post", faux_post)
    with pytest.raises(openrouter.OpenRouterError):
        openrouter.chat([{"role": "user", "content": "x"}], model="test/modele",
                        max_retries=2)
    if doit_reessayer:
        assert appels["n"] == 3, "les erreurs transitoires doivent être réessayées"
    else:
        assert appels["n"] == 1, "une erreur fatale ne doit jamais être réessayée"


def test_timeout_reessaye_puis_abandonne(client, monkeypatch):
    from app.domain import openrouter
    import httpx
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-test")
    monkeypatch.setattr(openrouter, "_sleep", lambda s: None)
    appels = {"n": 0}

    def faux_post(self, url, headers=None, json=None):
        appels["n"] += 1
        raise httpx.TimeoutException("trop long")

    monkeypatch.setattr(httpx.Client, "post", faux_post)
    with pytest.raises(openrouter.OpenRouterError):
        openrouter.chat([{"role": "user", "content": "x"}], model="test/modele",
                        max_retries=2)
    assert appels["n"] == 3


def test_json_invalide_refuse_sans_rafistolage(client, monkeypatch):
    from app.domain import openrouter
    with pytest.raises(openrouter.StructuredOutputError):
        openrouter._parse_structured("je pense que la copie dit environ ceci",
                                     "test/modele")
    # une enveloppe ```json reste lisible : c'est du contenu, pas de la structure
    assert openrouter._parse_structured('```json\n{"a": 1}\n```', "m") == {"a": 1}


# ================================================= 4. schéma de sortie
def test_le_schema_refuse_une_sortie_non_conforme():
    from app.domain import ocr_schema
    valide = ocr_schema.validate_page(page_primary())
    assert len(valide["blocks"]) == 4
    assert valide["blocks"][1]["kind"] == "MATH"

    mauvais = page_primary()
    mauvais["blocks"][0]["origin"] = "INVENTÉ"
    with pytest.raises(ocr_schema.SchemaError) as exc:
        ocr_schema.validate_page(mauvais)
    assert "origin" in str(exc.value)

    sans_verbatim = page_primary()
    del sans_verbatim["blocks"][0]["verbatim"]
    with pytest.raises(ocr_schema.SchemaError):
        ocr_schema.validate_page(sans_verbatim)


def test_le_schema_deduplique_les_identifiants_de_bloc():
    from app.domain import ocr_schema
    charge = page_primary()
    charge["blocks"][1]["block_id"] = "b001"
    valide = ocr_schema.validate_page(charge)
    identifiants = [b["block_id"] for b in valide["blocks"]]
    assert len(set(identifiants)) == len(identifiants)


def test_le_schema_de_verification_est_contraint():
    """Le schéma de verdict reste défini pour un futur mode SECOND_LOOK assisté.

    Ce mode n'est pas la double lecture : on y montrerait la transcription candidate
    au modèle, ce qui est utile pour éclairer un humain mais ne produit pas une
    lecture indépendante. Le schéma est donc éprouvé, sans être utilisé par la
    réconciliation.
    """
    from app.domain import ocr_schema
    charge = {"page_index": 1, "verdicts": [
        {"block_id": "b002", "verdict": "AGREE", "verbatim": None, "latex": None,
         "note": None},
        {"block_id": "b003", "verdict": "DISAGREE", "verbatim": "5/8 - 1/4 = 4/8",
         "latex": None, "note": "le dénominateur se lit 8"}]}
    valide = ocr_schema.validate_verification(charge)
    assert len(valide["verdicts"]) == 2
    charge["verdicts"][0]["verdict"] = "PEUT-ÊTRE"
    with pytest.raises(ocr_schema.SchemaError):
        ocr_schema.validate_verification(charge)


# ================================================= 5. consignes de lecture
def test_la_consigne_interdit_de_corriger_et_ne_donne_aucune_solution():
    from app.domain import ocr_prompts
    systeme = ocr_prompts.transcription_system_prompt()
    assert "NE JAMAIS CORRIGER" in systeme
    assert "-5 - (-5) = -10" in systeme          # l'exemple canonique est présent
    for interdit in ("réponse attendue", "corrigé", "barème", "solution :"):
        assert interdit not in systeme.lower().replace("aucune solution", "")
    verif = ocr_prompts.verification_system_prompt()
    assert "on ne te demande pas si l'élève a juste" in verif


def test_le_contexte_ne_contient_que_les_enonces_jamais_les_reponses(client, copie_pdf):
    from app import database
    from app.domain import transcription
    from app.models import ItemDefinition
    with database.session_scope() as session:
        assessment = _assessment(session)
        items = (session.query(ItemDefinition)
                 .filter_by(assessment_id=assessment.assessment_id)
                 .order_by(ItemDefinition.position).all())
        hints = transcription.item_hints(session, assessment)
        assert hints and all(len(h) == 2 for h in hints)

        # Contrôle structurel, et non par recherche de sous-chaîne : chaque indice est
        # exactement la référence de l'item et le début de son énoncé imprimé. Une
        # réponse courte comme « $9$ » apparaît fortuitement dans un énoncé, ce qui
        # ferait échouer une recherche naïve sans qu'aucune solution n'ait fuité.
        assert [ref for ref, _ in hints] == [i.ref for i in items]
        for (ref, texte), item in zip(hints, items):
            enonce = " ".join((item.statement or "").split())
            assert enonce.startswith(texte) or texte == enonce[:280]

        # Et aucune réponse attendue non triviale ne s'y retrouve.
        attendus = [i.expected_answer for i in items
                    if i.expected_answer and len(i.expected_answer) >= 12]
        assert attendus, "le référentiel doit bien porter des réponses attendues"
        textes = " ".join(t for _, t in hints)
        for attendu in attendus:
            assert attendu not in textes, "une réponse attendue a fuité dans le contexte"


def test_aucune_donnee_personnelle_superflue_dans_la_charge(client, copie_pdf):
    """Le modèle n'a pas besoin de savoir qui est l'élève, ni son historique."""
    from app import database
    from app.domain import transcription
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, model="test/primaire",
                                  client=faux)
    charge = json.dumps(faux.appels[0]["messages"], ensure_ascii=False)
    # Recherche par mot entier : « parenthèses » contient « parent » sans être une
    # donnée personnelle, et une recherche de sous-chaîne mentirait.
    import re
    for interdit in ("Sinda", "CHIKHAOUI", "sinda-chikhaoui", "parents", "tuteur",
                     "diagnostic", "profil", "remédiation", "séance"):
        assert not re.search(r"\b%s\b" % re.escape(interdit), charge, re.I), \
            "donnée personnelle ou pédagogique superflue : %s" % interdit
    # L'identifiant technique de l'évaluation ne circule pas non plus.
    assert "asm-" not in charge


# ================================================= 6. lecture et double lecture
def test_lecture_primary_voit_chaque_page(client, copie_pdf):
    """Chaque page est réellement envoyée à un modèle vision : aucune n'est résumée."""
    from app import database
    from app.domain import transcription
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        run = transcription.run_primary(session, assessment, model="test/primaire",
                                        client=faux)
        assert run.status == "DONE"
        assert run.pages_total == 2
        assert run.calls == 2
        assert len(faux.appels) == 2
        for appel in faux.appels:
            contenu = appel["messages"][1]["content"]
            images = [p for p in contenu if p.get("type") == "image_url"]
            assert len(images) == 1
            assert images[0]["image_url"]["url"].startswith("data:image/png;base64,")
            assert appel["response_format"]["json_schema"]["strict"] is True
        etat = transcription.state_of(session, assessment)
        assert etat.state == transcription.STATE_AI_PROPOSED


def test_la_transcription_conserve_l_erreur_de_l_eleve(client, copie_pdf):
    """Règle absolue : ce qui est écrit, pas ce qui aurait dû l'être."""
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, model="test/primaire",
                                  client=faux)
        bloc = (session.query(TranscriptionBlock)
                .filter_by(page_index=1, block_id="b002",
                           reading="PRIMARY").one())
        assert bloc.verbatim == "-8 + 3 - (-5) = -10"
        assert "0" != bloc.verbatim, "le résultat exact ne doit pas remplacer l'erreur"
        assert bloc.kind == "MATH"
        assert bloc.latex == "-8 + 3 - (-5) = -10"


def test_les_ratures_sont_conservees(client, copie_pdf):
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, model="test/primaire",
                                  client=faux)
        barre = (session.query(TranscriptionBlock)
                 .filter_by(page_index=1, block_id="b003",
                            reading="PRIMARY").one())
        assert barre.status == "CROSSED_OUT"
        assert barre.verbatim == "5/8 - 1/4 = 4/4"
        assert barre.notes == "barré d'un trait"


def test_les_incertitudes_et_alternatives_sont_conservees(client, copie_pdf):
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, model="test/primaire",
                                  client=faux)
        doute = (session.query(TranscriptionBlock)
                 .filter_by(page_index=1, block_id="b004",
                            reading="PRIMARY").one())
        assert doute.uncertainty == "HIGH"
        assert json.loads(doute.alternatives_json) == ["3/8", "5/8"]


def test_la_lecture_aveugle_ne_voit_ni_la_premiere_ni_la_reponse_attendue(client, copie_pdf):
    from app import database
    from app.domain import transcription
    faux_p = FauxClient([page_primary(1), page_primary(2)])
    faux_v = FauxClient([page_blind(1), page_blind(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, model="test/primaire",
                                  client=faux_p)
        run = transcription.run_blind(session, assessment, model="test/aveugle",
                                      client=faux_v)
        assert run.role == "BLIND"
        assert run.model_id == "test/aveugle"
        charge = json.dumps(faux_v.appels[0]["messages"], ensure_ascii=False)
        # La lecture aveugle ne voit PAS la transcription de la première : c'est ce
        # qui la rend indépendante. Aucun verbatim produit par PRIMARY n'y figure.
        for propose in ("-8 + 3 - (-5) = -10", "5/8 - 1/4 = 4/4"):
            assert propose not in charge, \
                "la seconde lecture ne doit pas voir la première"
        assert "verdict" not in charge.lower()
        # ni, bien sûr, la moindre réponse attendue
        from app.models import ItemDefinition
        for item in (session.query(ItemDefinition)
                     .filter_by(assessment_id=assessment.assessment_id).all()):
            if item.expected_answer and len(item.expected_answer) >= 12:
                assert item.expected_answer not in charge


def test_deux_lectures_aveugles_identiques(client, copie_pdf):
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    faux_p = FauxClient([page_primary(1), page_primary(2)])
    faux_v = FauxClient([page_blind(1), page_blind(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, client=faux_p,
                                  model="test/primaire")
        transcription.run_blind(session, assessment, client=faux_v,
                                model="test/aveugle")
        accord = (session.query(TranscriptionBlock)
                  .filter_by(page_index=1, block_id="b002",
                           reading="PRIMARY").one())
        assert accord.verify_verdict == "IDENTICAL"
        assert accord.reconciliation == transcription.RECONCILE_BLIND_IDENTICAL


def test_desaccord_rend_la_main_a_l_humain_sans_troisieme_vote(client, copie_pdf):
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    faux_p = FauxClient([page_primary(1), page_primary(2)])
    faux_v = FauxClient([page_blind(1, divergence="b002"),
                         page_blind(2, divergence="b002")])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, client=faux_p,
                                  model="test/primaire")
        transcription.run_blind(session, assessment, client=faux_v,
                                model="test/aveugle")
        litige = (session.query(TranscriptionBlock)
                  .filter_by(page_index=1, block_id="b002",
                           reading="PRIMARY").one())
        assert litige.verify_verdict == "DIFFERENT"
        assert litige.verify_verbatim == "-8 + 3 - (-5) = -1"
        assert litige.reconciliation == transcription.RECONCILE_REVIEW
        etat = transcription.state_of(session, assessment)
        assert etat.state == transcription.STATE_REVIEW_REQUIRED
    # Deux appels : une lecture aveugle par page, sur deux pages. Aucun troisième
    # modèle n'a été convoqué pour départager le désaccord.
    assert len(faux_v.appels) == 2, "une lecture aveugle par page, et rien de plus"


def test_une_incertitude_haute_reste_a_trancher_meme_en_accord(client, copie_pdf):
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    faux_p = FauxClient([page_primary(1), page_primary(2)])
    faux_v = FauxClient([page_blind(1), page_blind(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, client=faux_p,
                                  model="test/primaire")
        transcription.run_blind(session, assessment, client=faux_v,
                                model="test/aveugle")
        doute = (session.query(TranscriptionBlock)
                 .filter_by(page_index=1, block_id="b004",
                            reading="PRIMARY").one())
        assert doute.verify_verdict == "IDENTICAL"
        assert doute.reconciliation == transcription.RECONCILE_REVIEW


def test_une_seule_lecture_ne_vaut_pas_deux(client, copie_pdf):
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, client=faux,
                                  model="test/primaire")
        blocs = session.query(TranscriptionBlock).filter_by(reading="PRIMARY").all()
        assert all(b.reconciliation == transcription.RECONCILE_SINGLE for b in blocs)


# ===================================================== 7. revue humaine
def test_la_revue_humaine_n_ecrase_pas_la_proposition_de_l_ia(client, copie_pdf):
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, client=faux,
                                  model="test/primaire")
        bloc = (session.query(TranscriptionBlock)
                .filter_by(page_index=1, block_id="b002",
                           reading="PRIMARY").one())
        propose = bloc.verbatim
        transcription.review_block(session, assessment, bloc.id, "modifier",
                                   verbatim="-8 + 3 - (-5) = -1",
                                   note="le 0 est un 1 mal fermé")
        session.refresh(bloc)
        assert bloc.verbatim == propose, "la proposition IA doit rester lisible"
        assert bloc.human_verbatim == "-8 + 3 - (-5) = -1"
        assert bloc.review_state == transcription.REVIEW_HUMAN_VERIFIED
        assert bloc.reviewed_at is not None
        assert bloc.reviewed_by_role == "enseignant"
        assert bloc.human_note == "le 0 est un 1 mal fermé"


@pytest.mark.parametrize("action,etat_attendu", [
    ("accepter", "HUMAN_VERIFIED"),
    ("illisible", "HUMAN_ILLEGIBLE"),
    ("rejeter", "HUMAN_REJECTED")])
def test_les_actions_de_revue(client, copie_pdf, action, etat_attendu):
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, client=faux,
                                  model="test/primaire")
        bloc = (session.query(TranscriptionBlock)
                .filter_by(page_index=1, block_id="b002",
                           reading="PRIMARY").one())
        transcription.review_block(session, assessment, bloc.id, action)
        session.refresh(bloc)
        assert bloc.review_state == etat_attendu


def test_une_relecture_ne_pietine_pas_une_decision_humaine(client, copie_pdf):
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, client=faux,
                                  model="test/primaire")
        bloc = (session.query(TranscriptionBlock)
                .filter_by(page_index=1, block_id="b002",
                           reading="PRIMARY").one())
        transcription.review_block(session, assessment, bloc.id, "modifier",
                                   verbatim="lecture humaine définitive")
    _vider_cache()
    autre = page_primary(1)
    autre["blocks"][1]["verbatim"] = "une relecture qui dirait autre chose"
    faux2 = FauxClient([autre, page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, client=faux2, force=True,
                                  model="test/primaire")
        bloc = (session.query(TranscriptionBlock)
                .filter_by(page_index=1, block_id="b002",
                           reading="PRIMARY").one())
        assert bloc.human_verbatim == "lecture humaine définitive"
        assert bloc.review_state == transcription.REVIEW_HUMAN_VERIFIED


def test_etat_human_verified_quand_tout_est_tranche(client, copie_pdf):
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, client=faux,
                                  model="test/primaire")
        assert transcription.guard_automated_use(session, assessment), \
            "une transcription non vérifiée ne doit pas pouvoir être exploitée"
        for bloc in session.query(TranscriptionBlock).all():
            transcription.review_block(session, assessment, bloc.id, "accepter")
        for page in (1, 2):
            transcription.attest_page(session, assessment, page,
                                      note="page comparée à la transcription")
        etat = transcription.state_of(session, assessment)
        assert etat.state == transcription.STATE_HUMAN_VERIFIED
        assert transcription.guard_automated_use(session, assessment) == []


def test_route_de_revue(client, copie_pdf):
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, client=faux,
                                  model="test/primaire")
        bloc_id = (session.query(TranscriptionBlock)
                   .filter_by(page_index=1, block_id="b002",
                           reading="PRIMARY").one().id)

    reponse = client.post("/eleve/%s/transcription/bloc/%d" % (ELEVE, bloc_id),
                          json={"action": "modifier", "verbatim": "corrigé à la main"})
    assert reponse.status_code == 200, reponse.text
    corps = reponse.json()
    assert corps["bloc"]["human_verbatim"] == "corrigé à la main"
    assert corps["bloc"]["verbatim"] == "-8 + 3 - (-5) = -10"
    assert corps["resume"]["human_verified"] >= 1

    ecran = client.get("/eleve/%s/transcription?page=1" % ELEVE)
    assert ecran.status_code == 200
    assert "lecture, pas une correction" in ecran.text
    assert "PRIMARY" in ecran.text


# ============================================================ 8. cache et coût
def test_le_cache_evite_de_refacturer_une_page_deja_lue(client, copie_pdf):
    from app import database
    from app.domain import transcription
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        premier = transcription.run_primary(session, assessment, client=faux,
                                            model="test/primaire")
        assert premier.calls == 2 and premier.cached_calls == 0

    faux2 = FauxClient([])          # aucune réponse préparée : tout doit venir du cache
    with database.session_scope() as session:
        assessment = _assessment(session)
        second = transcription.run_primary(session, assessment, client=faux2,
                                           model="test/primaire")
        assert second.calls == 0
        assert second.cached_calls == 2
        assert faux2.appels == []


def test_relancer_ignore_le_cache_explicitement(client, copie_pdf):
    from app import database
    from app.domain import transcription
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        transcription.run_primary(session, _assessment(session), client=faux,
                                  model="test/primaire")
    faux2 = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        run = transcription.run_primary(session, _assessment(session), client=faux2,
                                        model="test/primaire", force=True)
        assert run.calls == 2 and run.cached_calls == 0


def test_le_cache_distingue_modele_et_version_de_consigne(client):
    from app.domain import transcription
    base = ("abc123", "modele/a", "prompt_v1", "schema_v1", {"temperature": 0})
    assert transcription.cache_key(*base) == transcription.cache_key(*base)
    assert transcription.cache_key(*base) != \
        transcription.cache_key("abc123", "modele/b", "prompt_v1", "schema_v1",
                                {"temperature": 0})
    assert transcription.cache_key(*base) != \
        transcription.cache_key("abc123", "modele/a", "prompt_v2", "schema_v1",
                                {"temperature": 0})
    assert transcription.cache_key(*base) != \
        transcription.cache_key("autre", "modele/a", "prompt_v1", "schema_v1",
                                {"temperature": 0})


def test_le_cout_est_releve_et_le_budget_borne(client, copie_pdf, monkeypatch):
    from app import database
    from app.domain import openrouter, transcription
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        run = transcription.run_primary(session, assessment, client=faux,
                                        model="test/primaire")
        assert float(run.cost_usd) == pytest.approx(0.008, abs=1e-6)
        assert run.tokens_in == 2400 and run.tokens_out == 600
        resume = transcription.summary(session, assessment)
        assert resume["cost_usd"] == pytest.approx(0.008, abs=1e-6)

    _vider_cache()
    faux2 = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        with pytest.raises(openrouter.BudgetExceededError):
            transcription.run_primary(session, assessment, client=faux2,
                                      model="test/primaire", force=True,
                                      budget=transcription.Budget(maximum=0.001))


def test_un_echec_marque_la_campagne_et_l_etat(client, copie_pdf):
    from app import database
    from app.domain import openrouter, transcription
    from app.models import OcrRun
    faux = FauxClient([])
    faux.erreurs = [openrouter.OpenRouterError("panne simulée", status=503)]
    with database.session_scope() as session:
        assessment = _assessment(session)
        with pytest.raises(openrouter.OpenRouterError):
            transcription.run_primary(session, assessment, client=faux,
                                      model="test/primaire")
    with database.session_scope() as session:
        assessment = _assessment(session)
        run = session.query(OcrRun).order_by(OcrRun.run_id.desc()).first()
        assert run.status == "FAILED"
        assert "panne simulée" in run.error
        etat = transcription.state_of(session, assessment)
        assert etat.state == transcription.STATE_FAILED


# ============================================================ 9. provenance
def test_chaine_de_provenance_complete(client, copie_pdf):
    """De l'original jusqu'au bloc vérifié, chaque maillon doit être interrogeable."""
    from app import database
    from app.domain import transcription
    from app.domain import source_copy as sc
    from app.models import OcrPage, OcrRun, TranscriptionBlock
    faux_p = FauxClient([page_primary(1), page_primary(2)])
    faux_v = FauxClient([page_blind(1), page_blind(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        run_p = transcription.run_primary(session, assessment, client=faux_p,
                                          model="test/primaire")
        transcription.run_blind(session, assessment, client=faux_v,
                                model="test/aveugle")
        bloc = (session.query(TranscriptionBlock)
                .filter_by(page_index=1, block_id="b002",
                           reading="PRIMARY").one())
        transcription.review_block(session, assessment, bloc.id, "accepter")
        session.refresh(bloc)

        original = sc.current_copy(session, assessment.assessment_id)
        derived = sc.derived_pages(session, original)

        # QUELLE PAGE ? QUEL ORIGINAL ? QUEL SHA256 ?
        assert bloc.source_copy_id == original.source_copy_id
        assert derived.derived_from_id == original.source_copy_id
        page = next(r for r in sc.files_of(session, derived) if r.page_index == 1)
        ocr_page = (session.query(OcrPage)
                    .filter_by(run_id=run_p.run_id, page_index=1).one())
        assert ocr_page.page_sha256 == page.sha256

        # QUEL MODÈLE ? QUEL RUN ? QUELLE CONSIGNE ?
        run = session.get(OcrRun, bloc.primary_run_id)
        assert run.model_id == "test/primaire"
        assert run.prompt_version == "handwriting_transcription_v1"
        assert run.schema_version == "ocr-page-v1"
        assert run.provider_name == "FournisseurSimulé"
        assert session.get(OcrRun, bloc.verify_run_id).role == "BLIND"

        # MODIFIÉ PAR UN HUMAIN ? QUAND ? EN QUELLE QUALITÉ ?
        assert bloc.review_state == transcription.REVIEW_HUMAN_VERIFIED
        assert bloc.reviewed_at and bloc.reviewed_by_role == "enseignant"


def test_la_transcription_ne_touche_jamais_la_correction(client, copie_pdf):
    """La transcription est une couche séparée : aucun score n'en découle."""
    from app import database
    from app.domain import correction as corr
    from app.domain import transcription
    from app.models import CriterionResponse
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        correction = corr.get_or_create_correction(session, assessment)
        session.flush()
        avant = {r.scoring_id: (r.score_centi, r.scoring_status)
                 for r in session.query(CriterionResponse)
                 .filter_by(correction_id=correction.correction_id).all()}
        transcription.run_primary(session, assessment, client=faux,
                                  model="test/primaire")
        apres = {r.scoring_id: (r.score_centi, r.scoring_status)
                 for r in session.query(CriterionResponse)
                 .filter_by(correction_id=correction.correction_id).all()}
        assert avant == apres
        assert all(statut == "PENDING" for _, statut in apres.values())


def test_journal_d_audit_des_campagnes(client, copie_pdf):
    from app import database
    from app.domain import transcription
    from app.models import AuditEvent
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        transcription.run_primary(session, _assessment(session), client=faux,
                                  model="test/primaire")
    with database.session_scope() as session:
        actions = {e.action for e in session.query(AuditEvent).all()}
        assert "transcription.primary" in actions
        assert "source_copy.rasterised" in actions


# ============================================== 10. sauvegarde et restauration
def test_sauvegarde_et_restauration_avec_pages_rendues(client, copie_pdf, tmp_path):
    from app import database
    from app.domain import transcription
    from tools import backup
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        transcription.run_primary(session, _assessment(session), client=faux,
                                  model="test/primaire")

    archive = tmp_path / "backup_ocr.zip"
    resultat = backup.create_backup(archive)
    # l'original (1 PDF) + les 2 pages rendues
    assert resultat["copies_sources"] == 3
    assert resultat["cache_ocr"] == 2

    controle = backup.verify_backup(archive)
    assert controle["ok"] is True, controle
    assert controle["copies_verifiees"] == 3


def test_immutabilite_pendant_toute_la_lecture(client, copie_pdf):
    """Lire, vérifier et relire ne modifient aucun octet, ni original ni page rendue."""
    from app import database
    from app.domain import transcription
    from app.domain import source_copy as sc
    faux_p = FauxClient([page_primary(1), page_primary(2)])
    faux_v = FauxClient([page_blind(1), page_blind(2)])
    with database.session_scope() as session:
        assessment = _assessment(session)
        transcription.run_primary(session, assessment, client=faux_p,
                                  model="test/primaire")
        original = sc.current_copy(session, assessment.assessment_id)
        derived = sc.derived_pages(session, original)
        empreintes = {r.stored_path: r.sha256
                      for r in sc.files_of(session, original) + sc.files_of(session,
                                                                            derived)}
        transcription.run_blind(session, assessment, client=faux_v,
                                model="test/aveugle")
        assert sc.verify(session, original)["ok"] is True
        assert sc.verify(session, derived)["ok"] is True
        for row in sc.files_of(session, original) + sc.files_of(session, derived):
            assert row.sha256 == empreintes[row.stored_path]
            assert oct(sc.stored_path(row).stat().st_mode & 0o777) == "0o400"


# ================================================ 11. visionneuse multipage
def test_index_de_pages_pour_la_visionneuse(client, copie_pdf):
    from app import database
    from app.domain import transcription
    faux = FauxClient([page_primary(1), page_primary(2)])
    with database.session_scope() as session:
        transcription.run_primary(session, _assessment(session), client=faux,
                                  model="test/primaire")
    index = client.get("/eleve/%s/copie/pages" % ELEVE).json()
    assert index["attached"] is True
    assert len(index["rendered"]) == 2
    assert index["rendered"][0]["dpi"] >= 150
    assert index["rendered"][0]["url"].endswith("/copie/rendu/1")
    assert index["rendered"][0]["ocr"]["blocs"] == 4
    assert index["transcription"]["state"] in ("AI_PROPOSED", "REVIEW_REQUIRED")

    image = client.get("/eleve/%s/copie/rendu/1" % ELEVE)
    assert image.status_code == 200
    assert image.headers["content-type"].startswith("image/png")
    assert client.get("/eleve/%s/copie/rendu/99" % ELEVE).status_code == 404
