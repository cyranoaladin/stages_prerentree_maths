# -*- coding: utf-8 -*-
"""Défauts du test live : en-têtes transportables, modèles par défaut, autorité unique.

Deux corrections manuelles ont été faites pendant le premier appel réel. Elles sont
revalidées ici depuis le code, et couvertes par des tests qui **échouent** si on les
défait. Une correction sans test de régression n'est pas une correction : c'est un
répit.

Aucun appel réseau. Aucune donnée d'Inès.
"""

from pathlib import Path

import pytest


# ============================================ §7 en-têtes HTTP transportables
def test_tous_les_entetes_du_client_sont_transportables(monkeypatch):
    """Les en-têtes réellement construits, pas seulement la constante d'attribution.

    L'appel échouait **avant de quitter le poste** : le client encode les valeurs
    d'en-tête en ASCII, et un tiret cadratin dans le titre d'attribution levait une
    ``UnicodeEncodeError`` qui ne désignait pas l'en-tête fautif.
    """
    import httpx
    from app.domain import openrouter
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-cle-de-test-ascii")

    entetes = {
        "Authorization": "Bearer %s" % openrouter.api_key(),
        "Content-Type": "application/json",
        "X-Title": openrouter.PROMPT_ATTRIBUTION,
    }
    entetes.update(openrouter.NO_RESPONSE_CACHE_HEADER)

    # Aucun en-tête ne doit être refusé par le contrôle interne…
    openrouter.check_header_values(entetes)
    # …ni par le client HTTP lui-même, qui est l'autorité réelle.
    list(httpx.Headers(entetes).raw)

    for nom, valeur in entetes.items():
        nom.encode("ascii")
        valeur.encode("ascii")


def test_l_ancien_tiret_cadratin_reproduit_bien_la_panne():
    """Le test doit échouer avec l'ancienne valeur : sinon il ne prouve rien."""
    import httpx
    from app.domain import openrouter

    ancienne = "Nexus S5 — Correction & Bilans"      # tiret cadratin d'origine
    assert "—" not in openrouter.PROMPT_ATTRIBUTION

    # Le client HTTP refuse cette valeur — c'est exactement la panne observée.
    with pytest.raises(UnicodeEncodeError):
        list(httpx.Headers({"X-Title": ancienne}).raw)

    # Et notre contrôle la refuse d'abord, en nommant l'en-tête fautif.
    with pytest.raises(openrouter.OpenRouterError) as exc:
        openrouter.check_header_values({"X-Title": ancienne})
    assert "X-Title" in str(exc.value)
    assert "non ASCII" in str(exc.value)


def test_une_cle_non_ascii_est_signalee_comme_telle(monkeypatch):
    """Risque résiduel : une clé mal collée produisait la même panne, sans message.

    Espace insécable, tiret typographique, accent — le message brut ne mentionnait
    jamais la clé. Il la nomme désormais, sans jamais l'afficher.
    """
    from app.domain import openrouter
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-cle-accentuée")
    with pytest.raises(openrouter.MissingKeyError) as exc:
        openrouter.chat([{"role": "user", "content": "x"}], model="m", max_retries=0)
    message = str(exc.value)
    assert "clé OpenRouter" in message
    assert "non ASCII" in message
    assert "accentu" not in message, "la clé elle-même ne doit jamais apparaître"


def test_les_entetes_sont_controles_avant_tout_appel_reseau(monkeypatch):
    """La panne doit survenir au contrôle, pas dans la pile HTTP."""
    from app.domain import openrouter
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-test")
    monkeypatch.setattr(openrouter, "PROMPT_ATTRIBUTION",
                        "Nexus S5 — Correction")
    appels = {"n": 0}

    def faux_post(self, url, headers=None, json=None):
        appels["n"] += 1
        raise AssertionError("aucun appel réseau ne doit être tenté")

    import httpx
    monkeypatch.setattr(httpx.Client, "post", faux_post)
    with pytest.raises(openrouter.OpenRouterError):
        openrouter.chat([{"role": "user", "content": "x"}], model="m", max_retries=0)
    assert appels["n"] == 0


# ================================================ §5 autorité unique des modèles
def test_config_est_la_seule_autorite_des_modeles():
    """Aucun autre module ne doit inscrire un identifiant de modèle en dur.

    Un Makefile, un script ou une documentation qui porterait sa propre valeur
    deviendrait une autorité concurrente : le jour où l'une change, on ne saurait
    plus laquelle fait foi.
    """
    import re
    racine = Path(__file__).resolve().parents[1]
    # Un identifiant de modèle a la forme « fournisseur/modele ».
    motif = re.compile(r"\b(google|anthropic|openai|meta-llama|mistralai|qwen)/"
                       r"[a-z0-9][a-z0-9.\-]*\b", re.I)
    autorises = {racine / "app" / "config.py"}          # la seule autorité
    coupables = []
    for chemin in list((racine / "app").rglob("*.py")):
        if chemin in autorises or "__pycache__" in str(chemin):
            continue
        for numero, ligne in enumerate(
                chemin.read_text(encoding="utf-8").splitlines(), start=1):
            nu = ligne.strip()
            if nu.startswith("#") or nu.startswith('"""') or nu.startswith("*"):
                continue
            if motif.search(ligne):
                coupables.append("%s:%d %s" % (chemin.name, numero, nu[:70]))
    assert not coupables, "modèles inscrits hors de config.py : %s" % coupables


def test_les_outils_lisent_les_modeles_depuis_config():
    """Les outils affichent et emploient les valeurs de config, pas les leurs."""
    import ast
    racine = Path(__file__).resolve().parents[1]
    for nom in ("openrouter_models.py", "ocr_smoke.py", "ocr_benchmark.py"):
        source = (racine / "tools" / nom).read_text(encoding="utf-8")
        tree = ast.parse(source)
        lectures = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
        assert lectures & {"OCR_MODEL_PRIMARY", "OCR_MODEL_VERIFY",
                           "OCR_MODEL_BASELINE"}, nom


def test_les_defauts_inscrits_sont_ceux_qualifies_en_live():
    """Le couple retenu au test live est bien celui que le code emploie sans override.

    Ces valeurs sont des **défauts de pilote**, qualifiés à une date donnée sur une
    fixture synthétique. Elles ne sont pas une vérité durable : la compatibilité
    fournisseur change, et le benchmark reste l'arbitre.
    """
    import os
    from app import config
    # Aucun override d'environnement ne doit être nécessaire.
    assert "OCR_MODEL_PRIMARY" not in os.environ
    assert "OCR_MODEL_VERIFY" not in os.environ
    assert config.OCR_MODEL_PRIMARY == "google/gemini-3.1-pro-preview"
    assert config.OCR_MODEL_VERIFY == "meta-llama/llama-4-maverick"
    assert config.OCR_MODEL_PRIMARY != config.OCR_MODEL_VERIFY, \
        "deux lectures indépendantes exigent deux modèles distincts"


# ================================================ §12 rôle du modèle BASELINE
def test_le_modele_baseline_ne_lit_jamais_une_copie_reelle():
    """§12 — BASELINE est un repère de comparaison, pas un lecteur de copies.

    Il n'a pas passé de porte live sous la politique imposée. Aucun chemin de lecture
    ne doit pouvoir le sélectionner, et surtout pas par défaut.
    """
    import inspect
    from app.domain import transcription
    source = inspect.getsource(transcription.run_reading)
    assert "OCR_MODEL_BASELINE" not in source
    # Le choix du modèle ne connaît que deux rôles de lecture.
    assert "config.OCR_MODEL_PRIMARY" in source
    assert "config.OCR_MODEL_VERIFY" in source


def test_une_lecture_avec_un_role_inconnu_est_refusee(client, tmp_path):
    """Défense en profondeur : un rôle non prévu ne doit pas devenir une lecture."""
    from app import database
    from app.domain import source_copy as sc
    from app.domain import transcription
    from test_ocr_pipeline import (FauxClient, fabrique_pdf, page_primary,
                                   _assessment, _remise_a_zero, _vider_cache)
    source = fabrique_pdf(tmp_path / "roles.pdf", pages=1)
    with database.session_scope() as session:
        _remise_a_zero(session)
        sc.attach(session, _assessment(session, "sinda-chikhaoui"), [source],
                  is_synthetic=True)
    _vider_cache()
    with database.session_scope() as session:
        assessment = _assessment(session, "sinda-chikhaoui")
        with pytest.raises(transcription.TranscriptionError) as exc:
            transcription.run_reading(session, assessment,
                                      role=transcription.ROLE_BASELINE,
                                      client=FauxClient([page_primary(1)]))
        assert "BASELINE" in str(exc.value)
        _remise_a_zero(session)
    _vider_cache()


# ================================ §6 la seconde lecture reste réellement aveugle
def test_la_lecture_aveugle_emploie_la_meme_consigne_et_ne_voit_rien_de_plus(client,
                                                                             tmp_path):
    """§6 — revalidation avec le modèle réellement retenu comme VERIFY.

    Changer de modèle ne doit rien changer à la doctrine : la seconde lecture reçoit
    la même image et le même contexte, et **jamais** la transcription de la première.
    """
    import json
    from app import config, database
    from app.domain import source_copy as sc
    from app.domain import transcription
    from app.models import ItemDefinition
    from test_ocr_pipeline import (FauxClient, fabrique_pdf, page_blind, page_primary,
                                   _assessment, _remise_a_zero, _vider_cache)

    source = fabrique_pdf(tmp_path / "aveugle.pdf", pages=2)
    with database.session_scope() as session:
        _remise_a_zero(session)
        sc.attach(session, _assessment(session, "sinda-chikhaoui"), [source],
                  is_synthetic=True)
    _vider_cache()

    primaire = FauxClient([page_primary(1), page_primary(2)])
    aveugle = FauxClient([page_blind(1), page_blind(2)])
    with database.session_scope() as session:
        assessment = _assessment(session, "sinda-chikhaoui")
        transcription.run_primary(session, assessment, client=primaire)
        transcription.run_blind(session, assessment, client=aveugle)

        # Les modèles employés sont bien les défauts du code, sans override.
        from app.models import OcrRun
        roles = {r.role: r.model_id for r in session.query(OcrRun).all()}
        assert roles["PRIMARY"] == config.OCR_MODEL_PRIMARY
        assert roles["BLIND"] == config.OCR_MODEL_VERIFY

        interdits = [i.expected_answer for i in
                     session.query(ItemDefinition)
                     .filter_by(assessment_id=assessment.assessment_id).all()
                     if i.expected_answer and len(i.expected_answer) >= 12]
        _remise_a_zero(session)
    _vider_cache()

    # Même consigne système, même schéma, même image — et rien de la première lecture.
    assert len(aveugle.appels) == len(primaire.appels) == 2
    for rang, appel in enumerate(aveugle.appels):
        assert appel["messages"][0] == primaire.appels[rang]["messages"][0], \
            "la consigne système doit être identique"
        assert appel["response_format"] is primaire.appels[rang]["response_format"]
        charge = json.dumps(appel["messages"], ensure_ascii=False)
        for propose in ("-8 + 3 - (-5) = -10", "5/8 - 1/4 = 4/4", "3/8"):
            assert propose not in charge, \
                "la seconde lecture ne doit pas voir la transcription de la première"
        for mot in ("verdict", "AGREE", "DISAGREE", "candidate", "candidat"):
            assert mot.lower() not in charge.lower()
        for attendu in interdits:
            assert attendu not in charge, "aucune réponse attendue ne circule"


# ================================ §15 verdict de préparation, calculé
def test_la_preparation_pilote_exige_les_trois_portes(tmp_path, monkeypatch):
    """§15 — PILOT_SOFTWARE_READY se calcule ; il ne se déclare pas.

    Un résultat de porte live absent vaut « non exécutée », jamais « réussie ».
    """
    import json
    from tools import debt_gate

    etat = tmp_path / "live_gate_status.json"
    monkeypatch.setattr(debt_gate, "LIVE_ETAT", etat)

    # Aucun résultat enregistré : la préparation ne peut pas être acquise.
    verdict = debt_gate.preparation_pilote(full_gate_ok=True)
    assert verdict["PILOT_SOFTWARE_READY"] == "NO"
    assert verdict["live"]["connectivity"] == "NOT_RUN"

    # Porte live réussie, mais full gate en échec : toujours NON.
    etat.write_text(json.dumps({"connectivity": "PASS", "privacy_routing": "PASS"}),
                    encoding="utf-8")
    assert debt_gate.preparation_pilote(full_gate_ok=False)["PILOT_SOFTWARE_READY"] \
        == "NO"

    # Les trois portes : et seulement là.
    assert debt_gate.preparation_pilote(full_gate_ok=True)["PILOT_SOFTWARE_READY"] \
        == "YES"

    # La qualité manuscrite n'entre jamais dans ce calcul.
    assert debt_gate.preparation_pilote(True)["HANDWRITING_REAL_ACCURACY_GATE"] \
        == "NOT_RUN"


def test_un_refus_de_politique_fait_echouer_la_porte_de_routage(tmp_path, monkeypatch):
    """Un modèle refusé par la politique n'est pas une porte réussie."""
    import json
    from app import config
    from tools import ocr_smoke
    monkeypatch.setattr(config, "RUNTIME_DIR", tmp_path)

    reussite = [{"modele_demande": "a/b", "etat": ocr_smoke.ETAT_DISPONIBLE,
                 "cache_status": "NOT_REPORTED"}]
    chemin = ocr_smoke.enregistrer_resultat(reussite, 0)
    assert json.loads(chemin.read_text())["privacy_routing"] == "PASS"

    refus = [{"modele_demande": "a/b", "etat": ocr_smoke.ETAT_REFUSE_POLITIQUE}]
    chemin = ocr_smoke.enregistrer_resultat(refus, 3)
    resultat = json.loads(chemin.read_text())
    assert resultat["connectivity"] == "FAIL"
    assert resultat["privacy_routing"] == "FAIL"

    # §10 — un « HIT » de cache invalide la porte de confidentialité.
    avec_hit = [{"modele_demande": "a/b", "etat": ocr_smoke.ETAT_DISPONIBLE,
                 "cache_status": "HIT"}]
    resultat = json.loads(ocr_smoke.enregistrer_resultat(avec_hit, 0).read_text())
    assert resultat["privacy_routing"] == "FAIL"


def test_un_cache_status_absent_reste_non_rapporte():
    """§10 — l'absence d'information ne devient ni MISS ni « désactivé confirmé »."""
    from app.domain import openrouter

    class FausseReponse:
        status_code = 200
        headers = {}

        def json(self):
            return {"choices": [{"message": {"content": "{}"}}],
                    "model": "a/b", "usage": {}}

    completion = openrouter._build_completion(
        FausseReponse().json(), FausseReponse(), 10, None, "a/b")
    assert completion.cache_status is None, "rien n'est inventé au niveau du client"

    from tools import ocr_smoke
    assert (completion.cache_status or "NOT_REPORTED") == "NOT_REPORTED"
    assert ocr_smoke.ETAT_DISPONIBLE == "MODEL_AVAILABLE"


@pytest.mark.parametrize("exception,attendu", [
    ("NoCompliantEndpointError", "MODEL_REJECTED_BY_POLICY"),
    ("StructuredOutputError", "PARAMETER_UNSUPPORTED"),
])
def test_les_causes_de_refus_sont_distinguees(exception, attendu):
    """§9 — « le modèle n'existe pas » et « la politique le refuse » diffèrent."""
    from app.domain import openrouter
    from tools import ocr_smoke
    exc = getattr(openrouter, exception)("motif", status=404)
    assert ocr_smoke.classer_echec(exc) == attendu
    assert ocr_smoke.classer_echec(
        openrouter.OpenRouterError("model not found", status=404)) == "MODEL_UNAVAILABLE"
    assert ocr_smoke.classer_echec(
        openrouter.OpenRouterError("panne", status=503, retryable=True)) == "NETWORK_ERROR"
