# -*- coding: utf-8 -*-
"""Parcours d'interface dans un vrai navigateur, contre un serveur réellement démarré.

Les fonctions les plus critiques de cette application sont côté navigateur : le choix
et l'ordre des pages avant envoi, les miniatures, l'annulation, la navigation
multipage, le rendu mathématique, la revue bloc par bloc et l'attestation de
complétude. Aucune de ces fonctions n'est éprouvée par un client HTTP : elles vivent
dans le JavaScript et dans le rendu du document.

Le test précédent visait un port sur lequel rien n'écoutait, et son « skip » masquait
l'absence totale de couverture navigateur. Celui-ci démarre un serveur, ouvre
Chromium, et agit comme un opérateur.

Playwright est une dépendance de **développement** : l'application de production n'en
dépend pas. Installation : voir ``docs/OCR_TRANSCRIPTION_PIPELINE.md``.
"""

import importlib.util
import socket
import threading
import time
from pathlib import Path

import pytest

PLAYWRIGHT = importlib.util.find_spec("playwright") is not None
pytestmark = pytest.mark.skipif(
    not PLAYWRIGHT,
    reason="playwright absent : installer le profil de développement "
           "(pip install playwright && playwright install chromium)")

ELEVE = "sinda-chikhaoui"


def _port_libre() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def serveur(runtime):
    """Un serveur uvicorn réel, sur la boucle locale, en mode fixtures."""
    import uvicorn
    from app import config
    from app.main import app

    config.settings.data_mode = "SYNTHETIC"     # aucune donnée réelle en jeu
    port = _port_libre()
    serveur = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port,
                                            log_level="error", access_log=False))
    fil = threading.Thread(target=serveur.run, daemon=True)
    fil.start()
    limite = time.monotonic() + 30
    while not serveur.started and time.monotonic() < limite:
        time.sleep(0.05)
    if not serveur.started:
        pytest.fail("le serveur de test n'a pas démarré")
    yield "http://127.0.0.1:%d" % port
    serveur.should_exit = True
    fil.join(timeout=10)


@pytest.fixture(scope="module")
def navigateur():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        chromium = p.chromium.launch()
        yield chromium
        chromium.close()


@pytest.fixture()
def page(navigateur, serveur):
    contexte = navigateur.new_context(viewport={"width": 1400, "height": 900})
    onglet = contexte.new_page()
    erreurs = []

    def _console(message):
        # Un refus HTTP attendu — un fichier invalide rejeté, par exemple — est
        # journalisé par le navigateur comme « Failed to load resource ». Ce n'est
        # pas une erreur de l'interface : c'est le serveur qui fait son travail, et
        # le script le rattrape. On ne retient que les vraies fautes de script.
        if message.type != "error":
            return
        if "Failed to load resource" in message.text:
            return
        erreurs.append(message.text)

    onglet.on("pageerror", lambda e: erreurs.append("exception : %s" % e))
    onglet.on("console", _console)
    yield onglet
    contexte.close()
    # Une exception JavaScript non rattrapée, ou une violation de la politique de
    # sécurité du contenu, casse silencieusement l'interface : elle doit faire échouer.
    assert not erreurs, "erreurs JavaScript : %s" % erreurs[:3]


def _fabrique_pdf(chemin: Path, pages: int = 3) -> Path:
    from test_ocr_pipeline import fabrique_pdf
    return fabrique_pdf(chemin, pages=pages)


def _fabrique_png(chemin: Path, gris: int = 120) -> Path:
    from PIL import Image, ImageDraw
    image = Image.new("RGB", (420, 594), "white")
    dessin = ImageDraw.Draw(image)
    dessin.rectangle([20, 20, 400, 574], outline="black", width=3)
    dessin.text((60, 260), "page %d" % gris, fill="black")
    image.save(chemin, format="PNG")
    return chemin


def _remise_a_zero():
    from app import database
    from test_ocr_pipeline import _remise_a_zero, _vider_cache
    with database.session_scope() as session:
        _remise_a_zero(session)
    _vider_cache()


def _ouvrir_correction(page, base):
    page.goto("%s/eleve/%s" % (base, ELEVE), wait_until="networkidle")
    page.click("summary:has-text('Téléverser')")
    page.wait_for_selector("[data-zone-depot]", state="visible")


# ============================================================ A. PDF multipage
def test_a_televersement_d_un_pdf_de_trois_pages(page, serveur, tmp_path):
    """A — sélection, résumé, confirmation, ingestion, manifeste."""
    _remise_a_zero()
    pdf = _fabrique_pdf(tmp_path / "copie_trois_pages.pdf", pages=3)
    _ouvrir_correction(page, serveur)

    page.set_input_files("[data-input-fichiers]", str(pdf))
    page.wait_for_selector(".page-a-envoyer")
    resume = page.text_content("[data-resume-selection]")
    assert "1 PDF" in resume
    assert "pagination interne du PDF fait foi" in resume
    assert page.locator(".vignette-pdf").count() == 1

    page.once("dialog", lambda d: d.accept())
    page.click("[data-envoyer]")
    page.wait_for_url("**/eleve/%s" % ELEVE, timeout=30000)
    page.wait_for_selector("#copie-eleve:has-text('EMPREINTE VÉRIFIÉE')", timeout=30000)

    panneau = page.text_content("#copie-eleve")
    assert "3 page(s)" in panneau
    assert "copie_trois_pages.pdf" in panneau


# ========================================================= B. lot d'images
def test_b_lot_d_images_ordre_retrait_et_confirmation(page, serveur, tmp_path):
    """B — ordre initial, réordonnancement, retrait, réajout, confirmation."""
    _remise_a_zero()
    images = [_fabrique_png(tmp_path / ("p%d.png" % n), gris=n) for n in (1, 2, 3)]
    _ouvrir_correction(page, serveur)

    page.set_input_files("[data-input-fichiers]", [str(i) for i in images])
    page.wait_for_selector(".page-a-envoyer")
    assert page.locator(".page-a-envoyer").count() == 3
    assert page.locator(".vignette img").count() == 3, "miniatures réellement rendues"

    lignes = lambda: [page.locator(".infos-page").nth(i).text_content()
                      for i in range(page.locator(".page-a-envoyer").count())]
    assert "p1.png" in lignes()[0] and "p3.png" in lignes()[2]

    # descendre la première page
    page.locator(".page-a-envoyer").nth(0).locator("button[title='Descendre']").click()
    assert "p2.png" in lignes()[0] and "p1.png" in lignes()[1]

    # retirer la dernière, puis la réajouter
    page.locator(".page-a-envoyer").nth(2).locator("button:has-text('retirer')").click()
    assert page.locator(".page-a-envoyer").count() == 2
    page.set_input_files("[data-input-fichiers]", str(images[2]))
    assert page.locator(".page-a-envoyer").count() == 3
    assert "p3.png" in lignes()[2]

    # la numérotation affichée suit l'ordre courant
    assert page.locator(".infos-page strong").nth(0).text_content() == "page 1"

    page.once("dialog", lambda d: d.accept())
    page.click("[data-envoyer]")
    page.wait_for_selector("#copie-eleve:has-text('EMPREINTE VÉRIFIÉE')", timeout=30000)

    import json as _json
    manifeste = _json.loads(page.evaluate(
        "fetch('/eleve/%s/copie/manifeste').then(r => r.text())" % ELEVE))
    assert [f["original_name"] for f in manifeste["files"]] == \
        ["p2.png", "p1.png", "p3.png"], "l'ordre confirmé est l'ordre enregistré"


# ======================================================== C. annulation
def test_c_annulation_avant_envoi_ne_persiste_rien(page, serveur, tmp_path):
    """C — tant que « Confirmer » n'est pas cliqué, rien n'a quitté le poste."""
    _remise_a_zero()
    images = [_fabrique_png(tmp_path / ("a%d.png" % n), gris=n) for n in (1, 2)]
    _ouvrir_correction(page, serveur)
    page.set_input_files("[data-input-fichiers]", [str(i) for i in images])
    page.wait_for_selector(".page-a-envoyer")
    page.click("[data-annuler]")
    assert page.locator(".page-a-envoyer").count() == 0
    assert "Rien n'a été envoyé" in page.text_content("[data-etat-upload]")

    from app import database
    from app.domain import source_copy as sc
    from app.models import Assessment
    with database.session_scope() as session:
        a = session.query(Assessment).filter_by(student_id=ELEVE).one()
        assert sc.current_copy(session, a.assessment_id) is None


# ======================================================== G. erreurs
def test_g_un_fichier_invalide_est_refuse_avec_un_message(page, serveur, tmp_path):
    """G — le refus arrive jusqu'à l'écran, sans page blanche ni erreur muette."""
    _remise_a_zero()
    faux = tmp_path / "deguise.pdf"
    faux.write_bytes(b"MZ\x90\x00 ceci est un executable")
    _ouvrir_correction(page, serveur)
    page.set_input_files("[data-input-fichiers]", str(faux))
    page.wait_for_selector(".page-a-envoyer")
    page.once("dialog", lambda d: d.accept())
    page.click("[data-envoyer]")
    page.wait_for_selector("[data-etat-upload].erreur-upload", timeout=20000)
    message = page.text_content("[data-etat-upload]")
    assert "format accepté" in message


def test_g_le_melange_pdf_et_images_est_refuse_avant_l_envoi(page, serveur, tmp_path):
    """Le refus est immédiat, côté navigateur : rien n'est même tenté."""
    _remise_a_zero()
    _ouvrir_correction(page, serveur)
    page.set_input_files("[data-input-fichiers]",
                         str(_fabrique_pdf(tmp_path / "m.pdf", pages=1)))
    page.wait_for_selector(".page-a-envoyer")
    page.set_input_files("[data-input-fichiers]",
                         str(_fabrique_png(tmp_path / "m.png")))
    assert "soit un PDF, soit des images" in page.text_content("[data-etat-upload]")


# ======================================================== H. clavier
def test_h_le_parcours_de_televersement_est_accessible_au_clavier(page, serveur,
                                                                  tmp_path):
    """H — les actions importantes sont atteignables sans souris."""
    _remise_a_zero()
    images = [_fabrique_png(tmp_path / ("k%d.png" % n), gris=n) for n in (1, 2)]
    _ouvrir_correction(page, serveur)
    page.set_input_files("[data-input-fichiers]", [str(i) for i in images])
    page.wait_for_selector(".page-a-envoyer")

    # Les commandes d'ordre sont de vrais boutons, donc focusables et activables
    # à la barre d'espace ou à Entrée.
    bouton = page.locator(".page-a-envoyer").nth(0).locator("button[title='Descendre']")
    bouton.focus()
    assert page.evaluate("document.activeElement.tagName") == "BUTTON"
    page.keyboard.press("Enter")
    premier = page.locator(".infos-page").nth(0).text_content()
    assert "k2.png" in premier

    # Le champ de fichiers est lui-même focusable, et chaque commande porte un
    # intitulé lisible par une synthèse vocale.
    page.focus("[data-input-fichiers]")
    assert page.evaluate("document.activeElement.type") == "file"
    for titre in ("Monter", "Descendre"):
        assert page.locator("button[title='%s']" % titre).count() >= 1


def _copie_et_transcription(serveur, tmp_path, avec_desaccord=False):
    """Prépare une copie lue par deux modèles simulés, sans aucun appel réseau."""
    from app import database
    from app.domain import source_copy as sc
    from app.domain import transcription
    from app.models import Assessment
    from test_ocr_pipeline import FauxClient, page_blind, page_primary
    from test_ocr_pipeline import _remise_a_zero as raz, _vider_cache
    pdf = _fabrique_pdf(tmp_path / "revue.pdf", pages=2)
    with database.session_scope() as session:
        raz(session)
        a = session.query(Assessment).filter_by(student_id=ELEVE).one()
        sc.attach(session, a, [pdf], is_synthetic=True, label="fixture navigateur")
    _vider_cache()
    with database.session_scope() as session:
        a = session.query(Assessment).filter_by(student_id=ELEVE).one()
        transcription.run_primary(session, a, model="nav/primaire",
                                  client=FauxClient([page_primary(1), page_primary(2)]))
        divergence = "b002" if avec_desaccord else None
        transcription.run_blind(
            session, a, model="nav/aveugle",
            client=FauxClient([page_blind(1, divergence=divergence),
                               page_blind(2, divergence=divergence)]))


# ==================================================== D. revue de transcription
def test_d_navigation_pages_rendu_math_et_actions_de_revue(page, serveur, tmp_path):
    """D — navigation multipage, rendu KaTeX, modification puis acceptation."""
    _copie_et_transcription(serveur, tmp_path)
    page.goto("%s/eleve/%s/transcription?page=1" % (serveur, ELEVE),
              wait_until="networkidle")

    # La page rendue est bien affichée, et la pagination fonctionne.
    assert page.locator("[data-image-page]").count() == 1
    assert page.locator(".pagination-pages a").count() == 2
    page.click(".pagination-pages a:has-text('2')")
    page.wait_for_url("**page=2")
    assert "Page 2 / 2" in page.text_content(".pane-page .pane-head")
    page.go_back(wait_until="networkidle")

    # KaTeX a réellement rendu le LaTeX proposé : la source reste lisible à côté.
    page.wait_for_selector(".latex-rendu .katex", timeout=15000)
    assert page.locator(".latex-source").count() >= 1

    # Zoom et rotation d'affichage n'altèrent pas l'image stockée.
    avant = page.get_attribute("[data-image-page]", "src")
    page.click("[data-zoom='+']")
    page.click("[data-rotation]")
    transforme = page.evaluate(
        "document.querySelector('[data-image-page]').style.transform")
    assert "scale" in transforme and "rotate(90deg)" in transforme
    assert page.get_attribute("[data-image-page]", "src") == avant

    # Modifier un bloc, puis vérifier que la proposition de l'IA reste visible.
    bloc = page.locator(".bloc").first
    bloc.locator("button:has-text('Modifier')").click()
    zone = bloc.locator("[data-edition-verbatim]")
    zone.fill("lecture retenue par l'enseignant")
    bloc.locator("[data-valider-edition]").click()
    page.wait_for_selector(".bloc-humain", timeout=20000)
    texte = page.text_content(".bloc:has(.bloc-humain)")
    assert "lecture retenue par l'enseignant" in texte
    assert "PRIMARY" in texte, "la proposition de l'IA reste affichée"


# ============================================= E. attestation de complétude
def test_e_la_revue_n_est_pas_finalisable_sans_attestation(page, serveur, tmp_path):
    """E — tous les blocs acceptés ne suffisent pas : la complétude s'atteste."""
    from app import database
    from app.domain import transcription
    from app.models import Assessment, TranscriptionBlock
    _copie_et_transcription(serveur, tmp_path)
    with database.session_scope() as session:
        a = session.query(Assessment).filter_by(student_id=ELEVE).one()
        for bloc in session.query(TranscriptionBlock).all():
            transcription.review_block(session, a, bloc.id, "accepter")

    page.goto("%s/eleve/%s/transcription?page=1" % (serveur, ELEVE),
              wait_until="networkidle")
    bandeau = page.text_content(".banner.banner-warning")
    assert "complétude" in bandeau.lower()
    assert page.locator("[data-attester]").count() == 1

    # On atteste les deux pages, et l'empêchement disparaît.
    for numero in (1, 2):
        page.goto("%s/eleve/%s/transcription?page=%d" % (serveur, ELEVE, numero),
                  wait_until="networkidle")
        page.once("dialog", lambda d: d.accept())
        page.click("[data-attester]")
        page.wait_for_selector("text=COMPLÉTUDE ATTESTÉE", timeout=20000)

    page.goto("%s/eleve/%s/transcription?page=1" % (serveur, ELEVE),
              wait_until="networkidle")
    assert page.locator(".banner.banner-warning").count() == 0
    assert "HUMAN_VERIFIED" in page.text_content(".sticky-bar")


# ================================================== F. rotation réelle
def test_f_la_rotation_change_reellement_les_pixels_envoyes(page, serveur, tmp_path):
    """F — une rotation d'affichage ne suffirait pas : le modèle verrait la page couchée."""
    from app import database
    from app.domain import rasterize
    from app.domain import source_copy as sc
    from app.models import Assessment
    _copie_et_transcription(serveur, tmp_path)

    with database.session_scope() as session:
        a = session.query(Assessment).filter_by(student_id=ELEVE).one()
        original = sc.current_copy(session, a.assessment_id)
        avant = {r.page_index: (r.sha256, r.width_px, r.height_px)
                 for r in sc.pages_for_reading(session, original)}
        rasterize.rotate_page(session, a, 1, 90)
        apres = {r.page_index: (r.sha256, r.width_px, r.height_px, r.rotation)
                 for r in sc.pages_for_reading(session, original)}

    assert apres[1][0] != avant[1][0], "les octets de la page tournée changent"
    assert apres[1][3] == 90
    # 90 degrés : la page devient plus large que haute.
    assert apres[1][1] == avant[1][2] and apres[1][2] == avant[1][1]

    page.goto("%s/eleve/%s/transcription?page=1" % (serveur, ELEVE),
              wait_until="networkidle")
    dimensions = page.evaluate(
        "() => { const i = document.querySelector('[data-image-page]');"
        " return [i.naturalWidth, i.naturalHeight]; }")
    assert dimensions[0] > dimensions[1], "le navigateur reçoit bien la page tournée"
