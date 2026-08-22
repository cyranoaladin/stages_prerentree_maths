# -*- coding: utf-8 -*-
"""Fermeture des réserves : rotation, preuves non textuelles, code, continuation, échelle.

Chacune de ces réserves correspondait à une fonction **annoncée** par le produit —
téléversement multipage, OCR mathématique, NSI, revue humaine — dont un invariant
indispensable n'était ni implémenté ni éprouvé. Une réserve documentée ne remplace pas
un test.

Aucun appel réseau. Aucune donnée d'Inès.
"""

import json
import time
from pathlib import Path

import pytest

from test_ocr_pipeline import (FauxClient, fabrique_pdf, page_blind, page_primary,
                               _assessment, _remise_a_zero, _vider_cache)

ELEVE = "sinda-chikhaoui"


@pytest.fixture()
def copie(client, tmp_path):
    from app import database
    from app.domain import source_copy as sc
    source = fabrique_pdf(tmp_path / "zero_dette.pdf", pages=2)
    with database.session_scope() as session:
        _remise_a_zero(session)
        sc.attach(session, _assessment(session, ELEVE), [source], is_synthetic=True)
    _vider_cache()
    yield source
    with database.session_scope() as session:
        _remise_a_zero(session)
    _vider_cache()


# ==================================================== §2 rotation réelle
def test_la_rotation_produit_une_piece_derivee_distincte(client, copie):
    """Une rotation d'affichage ne change pas ce que voit le modèle. Celle-ci, si."""
    from app import database
    from app.domain import rasterize
    from app.domain import source_copy as sc
    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        original = sc.current_copy(session, assessment.assessment_id)
        rasterize.render_pages(session, assessment, original)
        base = {r.page_index: r for r in sc.pages_for_reading(session, original)}

        tournees = rasterize.rotate_page(session, assessment, 1, 90)
        assert tournees.source_kind == sc.DERIVED_ROTATED_PAGES
        assert tournees.origin == "DERIVED"
        # Traçable jusqu'au rendu de base, lui-même traçable jusqu'à l'original.
        rendu_base = sc.derived_pages(session, original)
        assert tournees.derived_from_id == rendu_base.source_copy_id
        assert rendu_base.derived_from_id == original.source_copy_id

        effectives = {r.page_index: r for r in sc.pages_for_reading(session, original)}
        assert effectives[1].sha256 != base[1].sha256
        assert effectives[1].rotation == 90
        assert effectives[1].width_px == base[1].height_px
        assert effectives[1].height_px == base[1].width_px
        # La page non tournée reste celle du rendu de base.
        assert effectives[2].sha256 == base[2].sha256

        # L'original et le rendu de base sont intacts.
        assert sc.verify(session, original)["ok"] is True
        assert sc.verify(session, rendu_base)["ok"] is True


@pytest.mark.parametrize("angle", [45, 360, -90, "90"])
def test_une_rotation_non_admise_est_refusee(client, copie, angle):
    from app import database
    from app.domain import rasterize
    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        rasterize.render_pages(session, assessment)
        with pytest.raises(rasterize.RasterError):
            rasterize.rotate_page(session, assessment, 1, angle)


def test_une_rotation_differente_invalide_le_cache_de_lecture(client, copie):
    """Deux orientations, deux empreintes de page, donc deux clés de cache."""
    from app import database
    from app.domain import rasterize, transcription
    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        transcription.run_primary(session, assessment, model="t/p",
                                  client=FauxClient([page_primary(1),
                                                     page_primary(2)]))

    # Relecture sans rien changer : tout vient du cache.
    with database.session_scope() as session:
        rejoue = transcription.run_primary(session, _assessment(session, ELEVE),
                                           model="t/p", client=FauxClient([]))
        assert rejoue.calls == 0 and rejoue.cached_calls == 2

    # Une page tournée est une autre image : elle doit être relue.
    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        rasterize.rotate_page(session, assessment, 1, 180)
    with database.session_scope() as session:
        apres = transcription.run_primary(session, _assessment(session, ELEVE),
                                          model="t/p",
                                          client=FauxClient([page_primary(1)]))
        assert apres.calls == 1, "la page tournée doit être relue"
        assert apres.cached_calls == 1, "l'autre page reste en cache"


def test_la_lecture_emploie_bien_la_page_tournee(client, copie):
    from app import database
    from app.domain import rasterize, transcription
    from app.domain import source_copy as sc
    from app.security import sha256_file
    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        rasterize.render_pages(session, assessment)
        rasterize.rotate_page(session, assessment, 1, 270)
        original = sc.current_copy(session, assessment.assessment_id)
        attendue = next(r for r in sc.pages_for_reading(session, original)
                        if r.page_index == 1)
        empreinte_attendue = sha256_file(sc.stored_path(attendue))

        faux = FauxClient([page_primary(1), page_primary(2)])
        transcription.run_primary(session, assessment, model="t/p", client=faux)

    import base64
    charge = faux.appels[0]["messages"][1]["content"]
    url = next(p["image_url"]["url"] for p in charge if p.get("type") == "image_url")
    octets = base64.b64decode(url.split(",", 1)[1])
    import hashlib
    assert hashlib.sha256(octets).hexdigest() == empreinte_attendue, \
        "c'est bien la page tournée qui part au modèle"


# ============================================ §3 preuves non textuelles
def test_une_figure_est_une_reponse_pas_une_absence_de_reponse(client, copie):
    """L'absence de texte transcrit ne vaut JAMAIS « non répondu »."""
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    charge = page_primary(1)
    charge["blocks"].append({
        "block_id": "fig1", "item_ref": "A5", "origin": "HANDWRITTEN",
        "kind": "GEOMETRY", "status": "ACTIVE", "verbatim": "",
        "latex": None, "uncertainty": "MEDIUM", "alternatives": [],
        "notes": None, "bbox": None,
        "ai_description": "droite graduée avec cinq points placés et étiquetés"})
    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        transcription.run_primary(session, assessment, model="t/p",
                                  client=FauxClient([charge, page_primary(2)]))
        figure = (session.query(TranscriptionBlock)
                  .filter_by(page_index=1, block_id="fig1", reading="PRIMARY").one())
        assert figure.kind == "GEOMETRY"
        assert figure.verbatim == ""
        assert "droite graduée" in figure.ai_description

        # Tant qu'un humain ne s'est pas prononcé, rien n'est exploitable : une
        # figure peut constituer toute la réponse.
        empechements = transcription.transcription_is_usable(session, assessment)
        assert any("non textuelle" in m for m in empechements)

        transcription.review_block(session, assessment, figure.id, "decrire",
                                   note="segment [AB] tracé, milieu marqué")
        session.refresh(figure)
        assert figure.human_description == "segment [AB] tracé, milieu marqué"
        assert figure.review_state == "HUMAN_VERIFIED"
        assert not any("non textuelle" in m for m in
                       transcription.transcription_is_usable(session, assessment))


def test_le_resume_distingue_les_preuves_non_textuelles(client, copie):
    from app import database
    from app.domain import transcription
    charge = page_primary(1)
    charge["blocks"].append({
        "block_id": "tab1", "item_ref": "B3", "origin": "HANDWRITTEN",
        "kind": "TABLE", "status": "ACTIVE", "verbatim": "", "latex": None,
        "uncertainty": "LOW", "alternatives": [], "notes": None, "bbox": None,
        "ai_description": "tableau d'effectifs à trois colonnes"})
    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        transcription.run_primary(session, assessment, model="t/p",
                                  client=FauxClient([charge, page_primary(2)]))
        resume = transcription.summary(session, assessment)
        assert resume["non_text"] == 1


# ==================================================== §4 code NSI
def test_un_programme_conserve_exactement_sa_mise_en_forme(client, copie):
    """La mise en forme EST la donnée : une indentation fausse est l'information."""
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    programme = ("def somme(n):\n"
                 "    total = 0\n"
                 "  for i in range(n):\n"          # indentation fautive, conservée
                 "        total = total + i\n"
                 "    if total = 10:\n"            # « = » au lieu de « == »
                 "        print('dix')\n"
                 "\n"
                 "    return total\n")
    charge = page_primary(1)
    charge["blocks"].append({
        "block_id": "code1", "item_ref": "C2", "origin": "HANDWRITTEN",
        "kind": "CODE", "status": "ACTIVE", "verbatim": programme, "latex": None,
        "uncertainty": "LOW", "alternatives": [], "notes": None, "bbox": None,
        "verbatim_code": programme, "language_hint": "python"})
    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        transcription.run_primary(session, assessment, model="t/p",
                                  client=FauxClient([charge, page_primary(2)]))
        bloc = (session.query(TranscriptionBlock)
                .filter_by(page_index=1, block_id="code1", reading="PRIMARY").one())
        assert bloc.kind == "CODE"
        assert bloc.language_hint == "python"
        # Octet pour octet : ni réindentation, ni correction, ni normalisation.
        assert bloc.verbatim_code == programme
        assert "  for i in range(n):" in bloc.verbatim_code
        assert "if total = 10:" in bloc.verbatim_code, "l'erreur reste l'erreur"
        assert bloc.verbatim_code.count("\n\n") == 1, "la ligne vide est conservée"


def test_un_bloc_code_vide_est_refuse(client):
    from app.domain import ocr_schema
    charge = page_primary(1)
    charge["blocks"][0].update({"kind": "CODE", "verbatim": "  ",
                                "verbatim_code": "   "})
    with pytest.raises(ocr_schema.SchemaError) as exc:
        ocr_schema.validate_page(charge)
    assert "CODE sans contenu" in str(exc.value)


def test_la_consigne_interdit_de_reparer_un_programme():
    from app.domain import ocr_prompts
    consigne = ocr_prompts.transcription_system_prompt()
    for exigence in ("indentation", "N'indente pas", "verbatim_code",
                    "language_hint", "Markdown"):
        assert exigence in consigne, exigence


# ============================================ §5 continuation entre pages
def test_une_reponse_qui_se_poursuit_page_suivante(client, copie):
    """Deux preuves physiques, un seul ensemble logique — et aucune duplication."""
    from app import database
    from app.domain import transcription
    from app.models import TranscriptionBlock
    debut = page_primary(1)
    debut["blocks"][1].update({"item_ref": "C1", "continues_to": "C1"})
    suite = page_primary(2)
    suite["blocks"][1].update({"item_ref": "C1", "continues_from": "C1",
                               "verbatim": "… suite du calcul, page suivante"})
    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        transcription.run_primary(session, assessment, model="t/p",
                                  client=FauxClient([debut, suite]))
        blocs = (session.query(TranscriptionBlock)
                 .filter_by(reading="PRIMARY", item_ref="C1").all())
        assert len(blocs) == 2, "deux preuves physiques, pas une réponse dupliquée"
        assert {b.page_index for b in blocs} == {1, 2}
        vue = transcription.page_view(session, assessment, 2)
        lien = next(b for b in vue["blocks"] if b["block_id"] == "b002")
        assert lien["continues_from"] == "C1"

        # La liaison proposée est révisable : le système ne rattache jamais une suite
        # à la question dont elle est physiquement la plus proche.
        cible = next(b for b in blocs if b.page_index == 2)
        transcription.review_block(session, assessment, cible.id, "chainer",
                                   verbatim="C2", note="c'est la suite de C2")
        session.refresh(cible)
        assert cible.continues_from == "C1", "la proposition IA reste lisible"
        assert cible.human_continues_from == "C2"
        vue = transcription.page_view(session, assessment, 2)
        lien = next(b for b in vue["blocks"] if b["block_id"] == "b002")
        assert lien["continues_from"] == "C2"
        assert lien["ai_continues_from"] == "C1"


# ============================================== §6 échelle : 60 pages
@pytest.mark.slow
def test_une_copie_de_soixante_pages(client, tmp_path):
    """§6 — la limite annoncée est éprouvée, hors ligne et sans appel distant."""
    from app import config, database
    from app.domain import rasterize, transcription
    from app.domain import source_copy as sc
    from app.models import OcrPage, TranscriptionBlock
    from tools import backup, fsck

    mesures = {}
    source = fabrique_pdf(tmp_path / "soixante.pdf", pages=60)
    mesures["pdf_octets"] = source.stat().st_size

    debut = time.monotonic()
    with database.session_scope() as session:
        _remise_a_zero(session)
        sc.attach(session, _assessment(session, ELEVE), [source], is_synthetic=True)
    mesures["ingestion_s"] = round(time.monotonic() - debut, 2)
    _vider_cache()

    debut = time.monotonic()
    with database.session_scope() as session:
        derived = rasterize.render_pages(session, _assessment(session, ELEVE))
        assert derived.page_count == 60
    mesures["rasterisation_s"] = round(time.monotonic() - debut, 2)

    # Campagne complète : 60 pages, deux lectures. Client simulé — la latence
    # distante ne s'extrapole pas depuis un bouchon, et on ne prétend pas la mesurer.
    debut = time.monotonic()
    with database.session_scope() as session:
        assessment = _assessment(session, ELEVE)
        transcription.run_primary(
            session, assessment, model="t/p",
            client=FauxClient([page_primary(n) for n in range(1, 61)]))
        transcription.run_blind(
            session, assessment, model="t/b",
            client=FauxClient([page_blind(n) for n in range(1, 61)]))
    mesures["campagne_120_appels_s"] = round(time.monotonic() - debut, 2)

    with database.session_scope() as session:
        mesures["blocs"] = session.query(TranscriptionBlock).count()
        mesures["pages_ocr"] = session.query(OcrPage).count()
    # SQLite est en mode WAL : les données récentes vivent dans « -wal ». Mesurer le
    # seul fichier principal donnerait un chiffre faux et rassurant.
    mesures["base_octets"] = sum(
        chemin.stat().st_size for chemin in
        (Path(config.DB_PATH), Path(str(config.DB_PATH) + "-wal"),
         Path(str(config.DB_PATH) + "-shm")) if chemin.exists())
    mesures["fichiers_octets"] = sum(
        f.stat().st_size for f in Path(config.SOURCE_COPIES_DIR).rglob("*")
        if f.is_file())

    assert mesures["pages_ocr"] == 120, "60 pages × 2 lectures"
    assert mesures["blocs"] == 60 * 4 * 2, "4 blocs par page et par lecture"

    # Interruption à mi-parcours, puis reprise : rien n'est refacturé.
    with database.session_scope() as session:
        from app.models import OcrRun
        run = session.query(OcrRun).order_by(OcrRun.run_id.desc()).first()
        run.status = "RUNNING"
    with database.session_scope() as session:
        assert transcription.resume_interrupted(session) == 1
    debut = time.monotonic()
    with database.session_scope() as session:
        reprise = transcription.run_blind(session, _assessment(session, ELEVE),
                                          model="t/b", client=FauxClient([]))
        assert reprise.calls == 0 and reprise.cached_calls == 60
    mesures["reprise_depuis_cache_s"] = round(time.monotonic() - debut, 2)

    debut = time.monotonic()
    archive = backup.create_backup(tmp_path / "soixante.zip")
    assert backup.verify_backup(archive["archive"])["ok"] is True
    mesures["backup_restore_s"] = round(time.monotonic() - debut, 2)
    mesures["archive_octets"] = Path(archive["archive"]).stat().st_size

    debut = time.monotonic()
    with database.session_scope() as session:
        constat = fsck.controler(session)
    mesures["fsck_s"] = round(time.monotonic() - debut, 2)
    assert not constat.par_gravite("P0") and not constat.par_gravite("P1"), \
        [p["message"] for p in constat.problemes][:3]

    # L'écran de revue ne charge jamais les 60 pages en pleine résolution : il en
    # affiche une, et la pagination pointe les autres.
    ecran = client.get("/eleve/%s/transcription?page=1" % ELEVE)
    assert ecran.status_code == 200
    assert ecran.text.count("data-image-page") == 1
    assert ecran.text.count('class="btn btn-sm ') >= 1

    # Croissance linéaire : le temps par page reste du même ordre d'un bout à l'autre.
    debut = time.monotonic()
    client.get("/eleve/%s/transcription/page/1" % ELEVE)
    premiere = time.monotonic() - debut
    debut = time.monotonic()
    client.get("/eleve/%s/transcription/page/60" % ELEVE)
    derniere = time.monotonic() - debut
    mesures["page_1_ms"] = round(premiere * 1000)
    mesures["page_60_ms"] = round(derniere * 1000)
    assert derniere < max(0.5, premiere * 8), \
        "la dernière page ne doit pas coûter un ordre de grandeur de plus que la première"

    print("\nMESURES 60 PAGES : %s" % json.dumps(mesures, ensure_ascii=False))
    with database.session_scope() as session:
        _remise_a_zero(session)
    _vider_cache()


# ================================================ §7 isolation du rastériseur
def test_un_enfant_qui_deborde_ne_tue_pas_le_parent(client, tmp_path):
    """§7 — un délai d'attente ne borne que la durée, pas la consommation.

    Un analyseur de PDF hostile peut, dans le délai imparti, saturer le processeur,
    allouer plusieurs gigaoctets ou écrire un fichier de la taille du disque. Ces
    limites-là sont posées par le noyau, dans le processus enfant, avant ``exec``.
    """
    from app.security import run_command

    # Dépassement processeur : boucle infinie, une seconde de temps CPU accordée.
    cpu = run_command(["python3", "-c", "while True: pass"], cwd=tmp_path, timeout=30,
                      cpu_secondes=1)
    assert cpu.returncode < 0, "le noyau doit interrompre l'enfant (SIGXCPU)"

    # Dépassement mémoire : allocation d'un gigaoctet, 64 Mio accordés.
    memoire = run_command(["python3", "-c", "b = bytearray(1024*1024*1024)"],
                          cwd=tmp_path, timeout=30, cpu_secondes=60,
                          memoire_octets=64 * 1024 * 1024)
    assert memoire.returncode != 0
    assert "MemoryError" in (memoire.stderr or "")

    # Dépassement de taille de sortie : 50 Mio écrits, 1 Mio accordé.
    fichier = run_command(
        ["python3", "-c", "open('gros', 'wb').write(b'x' * 50 * 1024 * 1024)"],
        cwd=tmp_path, timeout=30, cpu_secondes=60,
        taille_fichier_octets=1024 * 1024)
    assert fichier.returncode != 0
    produit = tmp_path / "gros"
    assert produit.exists() and produit.stat().st_size <= 1024 * 1024

    # Dépassement du délai : l'appelant reprend la main.
    import subprocess
    with pytest.raises(subprocess.TimeoutExpired):
        run_command(["python3", "-c", "import time; time.sleep(30)"],
                    cwd=tmp_path, timeout=2, cpu_secondes=60)

    # Et le parent est toujours là pour l'affirmer.
    assert run_command(["python3", "-c", "print('vivant')"], cwd=tmp_path,
                       timeout=30, cpu_secondes=10).stdout.strip() == "vivant"


def test_le_rasterisseur_applique_bien_ces_limites():
    """Les limites ne sont pas seulement disponibles : elles sont employées."""
    import ast
    source = Path("app/domain/rasterize.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    appels = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
              and getattr(n.func, "id", "") == "run_command"]
    assert appels, "le rendu doit passer par run_command"
    for appel in appels:
        noms = {kw.arg for kw in appel.keywords}
        assert "timeout" in noms
        assert "cpu_secondes" in noms, "délai seul : insuffisant"
        assert "memoire_octets" in noms
        assert "taille_fichier_octets" in noms


def test_le_temporaire_de_rendu_est_prive():
    source = Path("app/domain/rasterize.py").read_text(encoding="utf-8")
    assert "out_dir.chmod(0o700)" in source


# ================================================ §16 migration avec données
# Définitions telles qu'elles existaient au schéma 6 : sans lecture aveugle, sans
# attestation, sans rotation, sans code. Les reconstituer explicitement vaut mieux
# que de maquiller une base courante en base ancienne — ce qui ne testerait rien.
SCHEMA_6 = [
    "CREATE TABLE app_meta (key VARCHAR(64) PRIMARY KEY, value VARCHAR(255) NOT NULL)",
    """CREATE TABLE source_copy (
        source_copy_id INTEGER NOT NULL PRIMARY KEY,
        assessment_id VARCHAR(64) NOT NULL,
        source_kind VARCHAR(32) NOT NULL DEFAULT 'REAL_STUDENT_COPY',
        origin VARCHAR(16) NOT NULL DEFAULT 'ORIGINAL',
        derived_from_id INTEGER,
        label VARCHAR(255), page_count INTEGER,
        file_count INTEGER NOT NULL DEFAULT 0,
        status VARCHAR(16) NOT NULL DEFAULT 'ATTACHED',
        is_immutable BOOLEAN NOT NULL DEFAULT 1,
        note TEXT, ingested_at DATETIME NOT NULL)""",
    """CREATE TABLE source_copy_file (
        id INTEGER NOT NULL PRIMARY KEY,
        source_copy_id INTEGER NOT NULL,
        page_index INTEGER NOT NULL,
        original_name VARCHAR(255) NOT NULL,
        media_type VARCHAR(64) NOT NULL,
        byte_size INTEGER NOT NULL,
        sha256 VARCHAR(64) NOT NULL,
        stored_path VARCHAR(512) NOT NULL,
        width_px INTEGER, height_px INTEGER, dpi INTEGER)""",
    """CREATE TABLE ocr_run (
        run_id INTEGER NOT NULL PRIMARY KEY,
        assessment_id VARCHAR(64) NOT NULL,
        source_copy_id INTEGER NOT NULL,
        derived_copy_id INTEGER,
        role VARCHAR(16) NOT NULL, model_id VARCHAR(128) NOT NULL,
        provider_name VARCHAR(96),
        prompt_version VARCHAR(64) NOT NULL, schema_version VARCHAR(64) NOT NULL,
        params_json TEXT, status VARCHAR(16) NOT NULL DEFAULT 'RUNNING',
        pages_total INTEGER NOT NULL DEFAULT 0, calls INTEGER NOT NULL DEFAULT 0,
        cached_calls INTEGER NOT NULL DEFAULT 0,
        tokens_in INTEGER NOT NULL DEFAULT 0, tokens_out INTEGER NOT NULL DEFAULT 0,
        cost_usd VARCHAR(32), error TEXT,
        started_at DATETIME NOT NULL, finished_at DATETIME)""",
    """CREATE TABLE transcription_block (
        id INTEGER NOT NULL PRIMARY KEY,
        assessment_id VARCHAR(64) NOT NULL,
        source_copy_id INTEGER NOT NULL,
        page_index INTEGER NOT NULL, block_id VARCHAR(64) NOT NULL,
        item_ref VARCHAR(16), origin VARCHAR(24) NOT NULL,
        kind VARCHAR(8) NOT NULL, status VARCHAR(16) NOT NULL,
        verbatim TEXT NOT NULL, latex TEXT,
        uncertainty VARCHAR(8) NOT NULL DEFAULT 'LOW',
        alternatives_json TEXT, notes TEXT, bbox_json TEXT,
        primary_run_id INTEGER, verify_run_id INTEGER,
        verify_verdict VARCHAR(16), verify_verbatim TEXT, verify_latex TEXT,
        verify_note TEXT, reconciliation VARCHAR(24),
        review_state VARCHAR(24) NOT NULL DEFAULT 'AI_PROPOSED',
        human_verbatim TEXT, human_latex TEXT, human_note TEXT,
        reviewed_at DATETIME, reviewed_by_role VARCHAR(32),
        created_at DATETIME NOT NULL)""",
    """CREATE TABLE transcription_state (
        id INTEGER NOT NULL PRIMARY KEY,
        assessment_id VARCHAR(64) NOT NULL, source_copy_id INTEGER NOT NULL,
        state VARCHAR(24) NOT NULL DEFAULT 'NOT_STARTED', detail TEXT,
        updated_at DATETIME NOT NULL)""",
]

DONNEES_6 = [
    ("INSERT INTO app_meta VALUES ('domain_schema_version','6')", ()),
    ("INSERT INTO app_meta VALUES ('app_version','1.4.0')", ()),
    ("""INSERT INTO source_copy (assessment_id, source_kind, origin, label,
        page_count, file_count, status, is_immutable, ingested_at)
        VALUES ('asm-x','REAL_STUDENT_COPY','ORIGINAL','pièce v6',2,1,'ATTACHED',1,
                '2026-08-20 10:00:00')""", ()),
    ("""INSERT INTO source_copy_file (source_copy_id, page_index, original_name,
        media_type, byte_size, sha256, stored_path, width_px, height_px, dpi)
        VALUES (1,1,'v6.pdf','application/pdf',123,'abc','x/v6.pdf',2480,3509,300)""", ()),
    ("""INSERT INTO ocr_run (assessment_id, source_copy_id, role, model_id,
        prompt_version, schema_version, status, pages_total, calls, cached_calls,
        tokens_in, tokens_out, started_at)
        VALUES ('asm-x',1,'PRIMARY','ancien/modele','v1','v1','DONE',2,2,0,10,20,
                '2026-08-20 10:05:00')""", ()),
    ("""INSERT INTO transcription_block (assessment_id, source_copy_id, page_index,
        block_id, item_ref, origin, kind, status, verbatim, uncertainty,
        review_state, human_verbatim, primary_run_id, created_at)
        VALUES ('asm-x',1,1,'v6b1','A1','HANDWRITTEN','MATH','ACTIVE',
                '-8 + 3 - (-5) = -10','LOW','HUMAN_VERIFIED','lecture humaine v6',1,
                '2026-08-20 10:06:00')""", ()),
]


def test_une_base_ancienne_avec_donnees_migre_sans_perte(client, tmp_path):
    """§16 — migrer une base vide ne prouve rien : on migre une base peuplée.

    La base de départ est un **vrai** schéma 6, reconstitué colonne par colonne, et
    non une base courante déguisée. On y met une pièce, une campagne et une décision
    humaine, puis on migre. Rien ne doit disparaître, et la décision humaine de la
    version 6 doit se retrouver intacte.
    """
    import sqlite3
    import migrations
    from sqlalchemy import create_engine

    ancienne = tmp_path / "v6.sqlite3"
    conn = sqlite3.connect(str(ancienne))
    for instruction in SCHEMA_6:
        conn.execute(instruction)
    for instruction, params in DONNEES_6:
        conn.execute(instruction, params)
    conn.commit()
    avant = {t: conn.execute("SELECT count(*) FROM %s" % t).fetchone()[0]
             for t in ("source_copy", "source_copy_file", "ocr_run",
                       "transcription_block")}
    # Les colonnes de la version 8 n'existent pas encore : c'est bien une base v6.
    colonnes = [r[1] for r in conn.execute("pragma table_info(transcription_block)")]
    assert "reading" not in colonnes and "verbatim_code" not in colonnes
    conn.close()

    moteur = create_engine("sqlite:///%s" % ancienne, future=True)
    rapport = migrations.apply(moteur, ancienne, tmp_path / "sauvegardes")
    assert rapport["version_avant"] == 6
    assert rapport["version_apres"] == migrations.CURRENT_VERSION
    assert rapport["sauvegarde"], "une sauvegarde précède toute migration"
    assert Path(rapport["sauvegarde"]).exists()

    conn = sqlite3.connect(str(ancienne))
    apres = {t: conn.execute("SELECT count(*) FROM %s" % t).fetchone()[0]
             for t in avant}
    assert apres == avant, "aucune ligne perdue : %s → %s" % (avant, apres)
    assert conn.execute("pragma foreign_key_check").fetchall() == []
    assert conn.execute("pragma integrity_check").fetchone()[0] == "ok"

    bloc = conn.execute("SELECT human_verbatim, reading, verbatim_code, "
                        "human_continues_from FROM transcription_block "
                        "WHERE block_id='v6b1'").fetchone()
    assert bloc[0] == "lecture humaine v6", "la décision humaine survit à la migration"
    assert bloc[1] == "PRIMARY", "les blocs existants deviennent la lecture primaire"
    assert bloc[2] is None and bloc[3] is None
    assert conn.execute("SELECT rotation FROM source_copy_file").fetchone()[0] == 0
    assert conn.execute("SELECT is_synthetic FROM source_copy").fetchone()[0] == 0
    for table in ("page_attestation", "transcription_block_history"):
        assert conn.execute("SELECT count(*) FROM %s" % table).fetchone()[0] == 0

    # Idempotence : rejouer la migration ne change rien.
    migrations.apply(moteur, ancienne, tmp_path / "sauvegardes")
    apres_bis = {t: conn.execute("SELECT count(*) FROM %s" % t).fetchone()[0]
                 for t in avant}
    assert apres_bis == avant
    conn.close()
    moteur.dispose()


def test_une_sauvegarde_capture_les_transactions_recentes(client, tmp_path):
    """La base est en mode WAL : copier le fichier principal ne suffit pas.

    Défaut trouvé pendant cet audit : ``shutil.copy2`` d'une base WAL produit une
    sauvegarde incomplète — jusqu'à l'absence pure et simple des tables récentes.
    Les deux chemins de sauvegarde employaient cette copie.
    """
    import shutil
    import sqlite3
    from app import config, database
    from app.domain import source_copy as sc
    import migrations

    # Une pièce vient d'être écrite : elle est committée, mais encore dans le WAL.
    source = fabrique_pdf(tmp_path / "recente.pdf", pages=1)
    with database.session_scope() as session:
        _remise_a_zero(session)
        sc.attach(session, _assessment(session, ELEVE), [source], is_synthetic=True,
                  label="pièce très récente")

    # La copie de fichier ne la voit pas forcément ; l'instantané, si — toujours.
    naive = tmp_path / "naive.sqlite3"
    shutil.copy2(config.DB_PATH, naive)
    instantane = migrations.backup_database(config.DB_PATH, tmp_path / "sauvegardes")

    def compte(chemin):
        try:
            conn = sqlite3.connect(str(chemin))
            valeur = conn.execute(
                "SELECT count(*) FROM source_copy WHERE label='pièce très récente'"
            ).fetchone()[0]
            conn.close()
            return valeur
        except sqlite3.OperationalError:
            return "TABLE ABSENTE"

    assert compte(instantane) == 1, "l'instantané doit contenir la pièce récente"

    # Et l'archive complète la contient aussi.
    from tools import backup
    import zipfile
    archive = backup.create_backup(tmp_path / "archive.zip")["archive"]
    with zipfile.ZipFile(archive) as zf:
        extrait = tmp_path / "extrait.sqlite3"
        extrait.write_bytes(zf.read("corrections.sqlite3"))
    assert compte(extrait) == 1, "l'archive doit contenir la pièce récente"

    with database.session_scope() as session:
        _remise_a_zero(session)
