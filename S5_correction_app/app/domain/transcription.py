# -*- coding: utf-8 -*-
"""Lecture assistée : double lecture aveugle, réconciliation locale, revue humaine.

    copie originale immuable
      → pages rendues (DERIVED, empreintes propres)
      → lecture PRIMARY  (modèle vision, sortie structurée)
      → lecture BLIND    (second modèle, MÊME image, qui n'a PAS vu la première)
      → réconciliation   (comparaison locale et déterministe des deux lectures)
      → revue humaine    (la seule chose qui fasse foi)
      → attestation de complétude, page par page

**Pourquoi la seconde lecture est aveugle.** Montrer la transcription candidate à un
second modèle produit un biais de confirmation : acquiescer lui coûte moins que
relire. Deux lectures indépendantes de la même image, comparées *localement*, sont la
seule construction qui mérite d'être appelée « deux lectures ».

**Ce que deux lectures identiques ne prouvent pas.** Elles ne prouvent pas que la
lecture est juste : deux modèles peuvent se tromper de la même manière. Le statut
s'appelle donc ``AI_TWO_BLIND_READINGS_IDENTICAL``, jamais « consensus ».

**Angle mort assumé, et traité.** Une interface qui n'affiche que les blocs trouvés
ne peut pas révéler une zone que les deux modèles auraient omise. Seul un humain,
comparant la page et la transcription, peut l'attester : sans attestation de
complétude, une page n'est jamais vérifiée.

Cette couche ne touche jamais ``criterion_response``. Un score reste une décision
humaine ; la transcription dit seulement ce qui est écrit.
"""

import datetime as dt
import json
from pathlib import Path

from .. import config
from ..models import (ItemDefinition, OcrPage, OcrRun, PageAttestation,
                      TranscriptionBlock, TranscriptionBlockHistory,
                      TranscriptionState)
from ..security import sha256_text
from . import ocr_prompts, ocr_schema, openrouter, rasterize
from . import source_copy as sc
from .correction import audit

ROLE_PRIMARY = "PRIMARY"
ROLE_BLIND = "BLIND"
ROLE_SECOND_LOOK = "SECOND_LOOK"
ROLE_BASELINE = "BASELINE"
# Compatibilité de nommage : l'ancien « VERIFY » désigne désormais la lecture aveugle.
ROLE_VERIFY = ROLE_BLIND

READING_PRIMARY = "PRIMARY"
READING_BLIND = "BLIND"

VERDICT_IDENTICAL = "IDENTICAL"
VERDICT_DIFFERENT = "DIFFERENT"
VERDICT_UNMATCHED = "UNMATCHED"

STATE_NOT_STARTED = "NOT_STARTED"
STATE_RUNNING = "RUNNING"
STATE_AI_PROPOSED = "AI_PROPOSED"
STATE_REVIEW_REQUIRED = "REVIEW_REQUIRED"
STATE_HUMAN_VERIFIED = "HUMAN_VERIFIED"
STATE_FAILED = "FAILED"
STATE_INTERRUPTED = "INTERRUPTED"

# Une seule lecture n'est pas un consensus, et le dire autrement serait mentir sur la
# force de la preuve.
RECONCILE_SINGLE = "AI_SINGLE_READING"
# Deux lectures aveugles qui coïncident. Ce n'est pas une preuve de justesse : deux
# modèles peuvent se tromper identiquement. Le nom le dit, « consensus » ne le disait pas.
RECONCILE_BLIND_IDENTICAL = "AI_TWO_BLIND_READINGS_IDENTICAL"
RECONCILE_SECOND_LOOK_AGREED = "AI_SECOND_LOOK_AGREED"
RECONCILE_REVIEW = "HUMAN_REVIEW_REQUIRED"

REVIEW_AI_PROPOSED = "AI_PROPOSED"
REVIEW_HUMAN_VERIFIED = "HUMAN_VERIFIED"
REVIEW_ILLEGIBLE = "HUMAN_ILLEGIBLE"
REVIEW_REJECTED = "HUMAN_REJECTED"


class TranscriptionError(Exception):
    pass


class RemoteOcrForbiddenError(TranscriptionError):
    """Envoi distant d'une copie réelle non autorisé sur ce poste."""


def actor() -> dict:
    """Qui agit, tel que l'application peut honnêtement le dire.

    L'application est locale et sans authentification : cette identité est une
    **déclaration** de l'opérateur, jamais une identité prouvée. L'audit l'expose
    comme telle, et ne fabrique pas une identité qui n'existe pas.
    """
    return {"identity": config.OPERATOR_IDENTITY, "role": config.OPERATOR_ROLE,
            "authenticated": False}


def guard_remote_send(original):
    """Une copie réelle ne part chez un fournisseur que sur autorisation explicite.

    OpenRouter peut conserver prompts et réponses si une fonction de journalisation
    est activée côté compte — ce que l'application ne sait ni lire ni empêcher. La
    décision d'envoyer malgré tout la copie d'un élève est donc une décision
    d'opérateur, prise hors interface, et pas un clic.
    """
    if original.source_kind != sc.REAL_STUDENT_COPY or original.is_synthetic:
        # Une fixture synthétique ne contient aucune donnée d'élève : le contrôle de
        # chaîne peut donc l'envoyer sans cette autorisation.
        return
    if not config.ALLOW_REAL_STUDENT_REMOTE_OCR:
        raise RemoteOcrForbiddenError(
            "l'envoi distant d'une copie d'élève réelle n'est pas autorisé sur ce "
            "poste. Cette autorisation se donne hors interface, en connaissance de "
            "cause : ALLOW_REAL_STUDENT_REMOTE_OCR=1. Le contrôle de chaîne sur "
            "fixture synthétique n'en a pas besoin.")


# ----------------------------------------------------------------------- état
def state_of(session, assessment) -> TranscriptionState:
    original = sc.current_copy(session, assessment.assessment_id)
    if original is None:
        return None
    return (session.query(TranscriptionState)
            .filter_by(source_copy_id=original.source_copy_id).one_or_none())


def _set_state(session, assessment, original, value, detail=None):
    row = (session.query(TranscriptionState)
           .filter_by(source_copy_id=original.source_copy_id).one_or_none())
    if row is None:
        row = TranscriptionState(assessment_id=assessment.assessment_id,
                                 source_copy_id=original.source_copy_id)
        session.add(row)
    row.state = value
    row.detail = detail
    session.flush()
    return row


# ---------------------------------------------------------------------- cache
def cache_key(page_sha256, model, prompt_sha, schema_sha, params) -> str:
    """Même page, même modèle, même consigne, même schéma : même résultat attendu.

    Relire une page déjà lue ne doit pas être refacturé. Une relecture délibérée
    passe par ``force``, qui contourne le cache explicitement.

Ce sont les **empreintes** du prompt et du schéma qui entrent ici, jamais leurs
    noms : un nom de version est déclaratif et peut rester identique alors que le
    texte a changé d'un caractère. ``params`` porte tout le reste de ce qui distingue
    la requête — rang de page, total, présence des indices d'items, résolution,
    politique de routage —, de sorte que deux requêtes différentes ne partagent
    jamais un résultat.
    """
    material = json.dumps({"page": page_sha256, "model": model,
                           "prompt_sha256": prompt_sha, "schema_sha256": schema_sha,
                           "params": params or {}},
                          sort_keys=True, ensure_ascii=False)
    return sha256_text(material)


def _cache_path(key) -> Path:
    return Path(config.OCR_CACHE_DIR) / ("%s.json" % key)


def cache_get(key):
    path = _cache_path(key)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return None


def cache_put(key, payload):
    root = Path(config.OCR_CACHE_DIR)
    root.mkdir(parents=True, exist_ok=True)
    path = _cache_path(key)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    # Le cache contient des transcriptions de copies : lisible par son propriétaire
    # seulement, comme les copies elles-mêmes.
    try:
        path.chmod(0o600)
    except OSError:
        pass


# -------------------------------------------------------------------- budget
class Budget:
    """Plafond de dépense par copie.

    Il **ne remplace pas** un plafond de dépense côté fournisseur : il ne connaît que
    les coûts que l'API lui rend, et un appel dont le coût n'est pas communiqué est
    compté ``UNKNOWN_COST``, pas gratuit. Un délai d'attente côté client peut par
    ailleurs survenir *après* que le fournisseur a facturé l'appel : une reprise n'est
    donc pas gratuite, et ce plafond ne prétend pas le contraire.

    Le pipeline est strictement séquentiel — une campagne à la fois par copie et par
    rôle, garantie par un index unique partiel en base — donc aucune course entre deux
    consommateurs du même budget.
    """

    def __init__(self, maximum=None):
        self.maximum = config.OCR_MAX_COST_PER_COPY_USD if maximum is None else maximum
        self.spent = 0.0
        self.unknown_calls = 0

    def add(self, cost):
        if cost is None:
            self.unknown_calls += 1
            return
        self.spent += float(cost)

    def as_dict(self):
        return {"maximum_usd": self.maximum, "spent_usd": round(self.spent, 6),
                "unknown_cost_calls": self.unknown_calls}

    def check(self):
        if self.maximum and self.spent > self.maximum:
            raise openrouter.BudgetExceededError(
                "budget de lecture dépassé pour cette copie : %.4f $ engagés pour un "
                "plafond de %.2f $. La campagne s'arrête ici."
                % (self.spent, self.maximum))


# ------------------------------------------------------------- contexte sujet
def item_hints(session, assessment):
    """Références et énoncés imprimés, pour aider au rattachement des réponses.

    Uniquement ``ref`` et ``statement``. Jamais ``expected_answer``, jamais le barème,
    jamais le profil de l'élève : un modèle à qui l'on montre la bonne réponse
    normalise l'écriture vers elle, et transcrirait une copie fausse en copie juste.
    """
    items = (session.query(ItemDefinition)
             .filter_by(assessment_id=assessment.assessment_id)
             .order_by(ItemDefinition.position).all())
    hints = []
    for item in items:
        statement = " ".join((item.statement or "").split())
        hints.append((item.ref, statement[:280]))
    return hints




# ----------------------------------------------------- configuration figée
def freeze_config(session, assessment, original, derived, pages, role, model,
                  system_prompt, schema_sha, budget=None, scope=None) -> dict:
    """Fige tout ce qui définit une campagne, au moment où elle démarre.

    Une variable d'environnement modifiée à la page 7 ne doit pas produire une
    campagne hétérogène : les six premières pages auraient été lues autrement, et le
    rapport ne pourrait plus dire avec quoi la copie a été lue.
    """
    from .. import APP_VERSION
    return {
        "assessment_id": assessment.assessment_id,
        "source_copy_id": original.source_copy_id,
        "source_files_sha256": [r.sha256 for r in sc.files_of(session, original)],
        "derived_copy_id": derived.source_copy_id,
        "page_sha256": [r.sha256 for r in pages],
        "page_count": len(pages),
        "raster_dpi": pages[0].dpi if pages else None,
        "role": role, "model": model, "scope": scope,
        "prompt_version": ocr_prompts.TRANSCRIPTION_PROMPT_VERSION,
        "prompt_sha256": ocr_prompts.prompt_sha256(system_prompt),
        "schema_version": ocr_schema.SCHEMA_VERSION,
        "schema_sha256": schema_sha,
        "temperature": 0, "max_tokens": 8000,
        "privacy_provider": dict(openrouter.PRIVACY_PROVIDER_BLOCK),
        "no_response_cache": dict(openrouter.NO_RESPONSE_CACHE_HEADER),
        "account_privacy_policy": openrouter.account_privacy_policy(),
        "base_url": config.OPENROUTER_BASE_URL,
        "cost_cap_usd": (budget or Budget()).maximum,
        "app_version": APP_VERSION,
    }


def _open_run(session, assessment, original, derived, role, model, gelee, pages_total):
    """Ouvre une campagne. Deux campagnes simultanées du même rôle sont impossibles.

    La garantie est **en base** — index unique partiel sur les campagnes ``RUNNING``
    — et non dans le code applicatif : un double clic ne peut pas la contourner.
    """
    en_cours = (session.query(OcrRun)
                .filter_by(source_copy_id=original.source_copy_id, role=role,
                           status="RUNNING").first())
    if en_cours is not None:
        raise TranscriptionError(
            "une campagne %s est déjà en cours sur cette copie (n° %d). Attendez sa "
            "fin, ou reprenez-la." % (role, en_cours.run_id))
    run = OcrRun(assessment_id=assessment.assessment_id,
                 source_copy_id=original.source_copy_id,
                 derived_copy_id=derived.source_copy_id,
                 role=role, model_id=model,
                 prompt_version=gelee["prompt_version"],
                 schema_version=gelee["schema_version"],
                 prompt_sha256=gelee["prompt_sha256"],
                 schema_sha256=gelee["schema_sha256"],
                 params_json=json.dumps({"temperature": gelee["temperature"]}),
                 frozen_config_json=json.dumps(gelee, ensure_ascii=False),
                 verify_mode=(ROLE_BLIND if role == ROLE_BLIND else None),
                 pages_total=pages_total, status="RUNNING")
    session.add(run)
    session.flush()
    return run


def is_stale(session, assessment, run) -> bool:
    """Campagne menée sur une pièce qui n'est plus la pièce courante.

    Remplacer une copie pendant une campagne ne l'invalide pas — elle reste vraie de
    la pièce qu'elle a lue — mais elle ne peut plus servir la correction courante
    sans reprise humaine explicite.
    """
    courante = sc.current_copy(session, assessment.assessment_id)
    return courante is None or run.source_copy_id != courante.source_copy_id


# ------------------------------------------------------------------ lectures
def _page_messages(page_row, page_index, page_total, hints):
    return [
        {"role": "system", "content": ocr_prompts.transcription_system_prompt()},
        {"role": "user", "content": [
            {"type": "text",
             "text": ocr_prompts.transcription_user_prompt(page_index, page_total,
                                                           hints)},
            {"type": "image_url",
             "image_url": {"url": openrouter.image_data_url(
                 sc.stored_path(page_row), page_row.media_type)}},
        ]},
    ]


def run_reading(session, assessment, role=ROLE_PRIMARY, model=None, force=False,
                client=None, budget=None, with_item_hints=True):
    """Une lecture complète de la copie, page par page.

    ``role`` vaut ``PRIMARY`` ou ``BLIND``. Les deux emploient exactement la même
    consigne et le même schéma sur la même image ; une lecture ``BLIND`` ne reçoit
    **jamais** la transcription produite par ``PRIMARY``. C'est ce qui la rend
    indépendante, et la seule construction qui autorise à parler de deux lectures.
    """
    # Deux rôles de lecture, et deux seulement. Un rôle inconnu tombait auparavant
    # dans la branche « sinon » et lisait la copie avec le modèle de vérification,
    # sous une étiquette qui ne correspondait à rien. BASELINE, en particulier, est un
    # repère de comparaison : il n'a pas passé de porte live sous la politique
    # imposée, et ne doit jamais lire une copie.
    if role not in (ROLE_PRIMARY, ROLE_BLIND):
        raise TranscriptionError(
            "rôle de lecture « %s » non admis : une lecture est PRIMARY ou BLIND. "
            "BASELINE est un repère de benchmark, pas un lecteur de copies — il n'a "
            "pas de porte live validée sous la politique de routage imposée." % role)
    client = client or openrouter
    budget = budget or Budget()
    model = model or (config.OCR_MODEL_PRIMARY if role == ROLE_PRIMARY
                      else config.OCR_MODEL_VERIFY)

    original = sc.current_copy(session, assessment.assessment_id)
    if original is None:
        raise TranscriptionError("aucune copie rattachée : rien à lire.")
    guard_remote_send(original)

    derived = rasterize.render_pages(session, assessment, original)
    # Les pages réellement montrées au modèle : la version tournée quand elle existe.
    # Une rotation d'affichage ne suffirait pas — le modèle recevrait la page couchée.
    pages = sc.pages_for_reading(session, original)
    if not pages:
        raise TranscriptionError("aucune page rendue.")
    hints = item_hints(session, assessment) if with_item_hints else None

    gelee = freeze_config(session, assessment, original, derived, pages, role, model,
                          ocr_prompts.transcription_system_prompt(),
                          ocr_schema.PAGE_SCHEMA_SHA256, budget=budget)
    run = _open_run(session, assessment, original, derived, role, model, gelee,
                    len(pages))
    _set_state(session, assessment, original, STATE_RUNNING,
               "lecture %s en cours (%d page(s))" % (role, len(pages)))

    reading = READING_PRIMARY if role == ROLE_PRIMARY else READING_BLIND
    try:
        for page_row in pages:
            # Tout ce qui distingue la requête entre dans la clé, et provient de la
            # configuration figée — pas de l'environnement courant.
            params = {"temperature": gelee["temperature"],
                      "page_index": page_row.page_index,
                      "page_total": len(pages), "hints": bool(hints),
                      "dpi": page_row.dpi,
                      "rotation": page_row.rotation or 0,
                      "reading": reading,
                      "privacy": gelee["privacy_provider"]}
            key = cache_key(page_row.sha256, model, gelee["prompt_sha256"],
                            gelee["schema_sha256"], params)
            cached = None if force else cache_get(key)
            if cached is not None:
                valide = ocr_schema.validate_page(cached["parsed"])
                valide["page_index"] = page_row.page_index
                _record_page(session, run, page_row, valide, cached, cached_call=True)
                run.cached_calls += 1
            else:
                completion = client.chat(
                    _page_messages(page_row, page_row.page_index, len(pages), hints),
                    model=model, response_format=ocr_schema.PAGE_RESPONSE_FORMAT,
                    temperature=gelee["temperature"])
                valide = ocr_schema.validate_page(completion.parsed)
                valide["page_index"] = page_row.page_index
                record = {"parsed": completion.parsed,
                          "model_id": completion.model_id,
                          "provider_name": completion.provider_name,
                          "generation_id": completion.generation_id,
                          "request_id": completion.request_id,
                          "latency_ms": completion.latency_ms,
                          "usage": completion.usage.as_dict()}
                cache_put(key, record)
                _record_page(session, run, page_row, valide, record)
                run.calls += 1
                run.provider_name = run.provider_name or completion.provider_name
                run.tokens_in += completion.usage.tokens_in
                run.tokens_out += completion.usage.tokens_out
                budget.add(completion.usage.cost_usd)
                budget.check()
            _store_blocks(session, assessment, original, run, page_row.page_index,
                          valide, reading)
    except Exception as exc:
        run.status = "FAILED"
        # Ni clé, ni image, ni copie dans un journal applicatif.
        run.error = openrouter.redact(str(exc), limite=1000)
        run.finished_at = dt.datetime.now(dt.timezone.utc)
        _set_state(session, assessment, original, STATE_FAILED, run.error)
        session.flush()
        raise

    run.status = "DONE"
    run.cost_usd = "%.6f" % budget.spent if budget.spent else None
    run.finished_at = dt.datetime.now(dt.timezone.utc)
    session.flush()
    reconcile(session, assessment)
    audit(session, "transcription.%s" % role.lower(), "ocr_run", run.run_id,
          assessment.assessment_id,
          new_value="%s · %d page(s) · %d appel(s) · %d en cache"
                    % (model, run.pages_total, run.calls, run.cached_calls))
    session.flush()
    return run


def run_primary(session, assessment, **kwargs):
    return run_reading(session, assessment, role=ROLE_PRIMARY, **kwargs)


def run_blind(session, assessment, **kwargs):
    """Seconde lecture, indépendante. Elle ne voit pas la première."""
    return run_reading(session, assessment, role=ROLE_BLIND, **kwargs)


# Nom historique conservé pour les appelants existants. La sémantique a changé : ce
# n'est plus une relecture d'une transcription candidate, mais une lecture aveugle.
def run_verify(session, assessment, model=None, scope=None, client=None, budget=None,
               force=False):
    return run_reading(session, assessment, role=ROLE_BLIND, model=model,
                       client=client, budget=budget, force=force)


def _record_page(session, run, page_row, validated, record, cached_call=False):
    usage = (record or {}).get("usage") or {}
    session.add(OcrPage(
        run_id=run.run_id, page_index=page_row.page_index,
        page_sha256=page_row.sha256,
        status="CACHED" if cached_call else "OK",
        request_id=(record or {}).get("request_id"),
        generation_id=(record or {}).get("generation_id"),
        raw_json=json.dumps(validated, ensure_ascii=False),
        latency_ms=(record or {}).get("latency_ms"),
        tokens_in=usage.get("tokens_in"), tokens_out=usage.get("tokens_out"),
        cost_usd=("%.6f" % usage["cost_usd"]) if usage.get("cost_usd") else None))


def _store_blocks(session, assessment, original, run, page_index, validated, reading):
    for block in validated["blocks"]:
        existing = (session.query(TranscriptionBlock)
                    .filter_by(source_copy_id=original.source_copy_id,
                               page_index=page_index, block_id=block["block_id"],
                               reading=reading).one_or_none())
        if existing is not None and existing.review_state != REVIEW_AI_PROPOSED:
            continue              # un humain s'est prononcé : sa décision prime
        row = existing or TranscriptionBlock(
            assessment_id=assessment.assessment_id,
            source_copy_id=original.source_copy_id,
            page_index=page_index, block_id=block["block_id"], reading=reading)
        row.item_ref = block["item_ref"]
        row.origin = block["origin"]
        row.kind = block["kind"]
        row.status = block["status"]
        row.verbatim = block["verbatim"]
        row.latex = block["latex"]
        row.uncertainty = block["uncertainty"]
        row.alternatives_json = json.dumps(block["alternatives"], ensure_ascii=False)
        row.notes = block["notes"]
        row.bbox_json = json.dumps(block["bbox"], ensure_ascii=False) \
            if block["bbox"] else None
        row.verbatim_code = block.get("verbatim_code")
        row.language_hint = block.get("language_hint")
        row.ai_description = block.get("ai_description")
        row.continues_from = block.get("continues_from")
        row.continues_to = block.get("continues_to")
        if reading == READING_PRIMARY:
            row.primary_run_id = run.run_id
            row.reconciliation = RECONCILE_SINGLE
        else:
            row.verify_run_id = run.run_id
        row.review_state = REVIEW_AI_PROPOSED
        if existing is None:
            session.add(row)
    session.flush()


# ------------------------------------------------------------- réconciliation
def normalise(texte) -> str:
    """Indulgente sur la mise en forme, stricte sur le contenu."""
    return " ".join((texte or "").split()).replace("−", "-").lower()


def _same_reading(a, b):
    return normalise(a) == normalise(b)


def _appariement(primaires, aveugles):
    """Apparie deux lectures d'une même page, localement et sans modèle.

    Deux passes, de la plus sûre à la moins sûre : texte identique, puis même item et
    même nature. Ce qui ne s'apparie pas est déclaré ``UNMATCHED`` — jamais rapproché
    de force, parce qu'un faux appariement masquerait précisément le désaccord.
    """
    restants = list(aveugles)
    couples = []
    for bloc in primaires:
        cible = next((b for b in restants if _same_reading(b.verbatim, bloc.verbatim)),
                     None)
        if cible is not None:
            restants.remove(cible)
        couples.append([bloc, cible])
    for couple in couples:
        if couple[1] is not None:
            continue
        cible = next((b for b in restants
                      if b.item_ref == couple[0].item_ref
                      and b.kind == couple[0].kind), None)
        if cible is not None:
            restants.remove(cible)
            couple[1] = cible
    return couples, restants


def reconcile(session, assessment) -> dict:
    """Confronte les deux lectures, localement. Aucune machine n'arbitre.

    Aucun troisième modèle n'est appelé pour départager : un désaccord entre deux
    lecteurs indépendants est précisément l'information qui doit remonter à l'humain.
    """
    original = sc.current_copy(session, assessment.assessment_id)
    if original is None:
        return {}
    blocs = (session.query(TranscriptionBlock)
             .filter_by(source_copy_id=original.source_copy_id).all())
    primaires = [b for b in blocs if b.reading == READING_PRIMARY]
    aveugles = [b for b in blocs if b.reading == READING_BLIND]
    comptes = {}

    if not aveugles:
        for bloc in primaires:
            if bloc.review_state == REVIEW_AI_PROPOSED:
                bloc.reconciliation = RECONCILE_SINGLE
                comptes[RECONCILE_SINGLE] = comptes.get(RECONCILE_SINGLE, 0) + 1
        session.flush()
        refresh_state(session, assessment)
        return comptes

    run_aveugle = (session.query(OcrRun)
                   .filter_by(source_copy_id=original.source_copy_id, role=ROLE_BLIND)
                   .order_by(OcrRun.run_id.desc()).first())
    for page in sorted({b.page_index for b in primaires} |
                       {b.page_index for b in aveugles}):
        pp = [b for b in primaires if b.page_index == page]
        pa = [b for b in aveugles if b.page_index == page]
        couples, orphelins = _appariement(pp, pa)
        for bloc, jumeau in couples:
            if bloc.review_state != REVIEW_AI_PROPOSED:
                continue
            bloc.verify_mode = ROLE_BLIND
            # Provenance : quelle campagne a produit la lecture confrontée.
            bloc.verify_run_id = run_aveugle.run_id if run_aveugle else None
            if jumeau is None:
                # Vu par la seule première lecture : à trancher.
                bloc.verify_verdict = VERDICT_UNMATCHED
                bloc.verify_block_id = None
                bloc.verify_verbatim = None
                bloc.verify_latex = None
                bloc.reconciliation = RECONCILE_REVIEW
            else:
                bloc.verify_block_id = jumeau.block_id
                bloc.verify_verbatim = jumeau.verbatim
                bloc.verify_latex = jumeau.latex
                identique = _same_reading(bloc.verbatim, jumeau.verbatim)
                bloc.verify_verdict = (VERDICT_IDENTICAL if identique
                                       else VERDICT_DIFFERENT)
                if not identique:
                    bloc.reconciliation = RECONCILE_REVIEW
                elif "HIGH" in (bloc.uncertainty, jumeau.uncertainty):
                    # Deux lecteurs peuvent s'accorder sur « je ne sais pas ». Ce
                    # n'est pas une lecture exploitable.
                    bloc.reconciliation = RECONCILE_REVIEW
                elif bloc.item_ref != jumeau.item_ref:
                    # Même texte, question différente : une réponse rattachée au
                    # mauvais item est aussi fausse qu'un caractère mal lu.
                    bloc.reconciliation = RECONCILE_REVIEW
                else:
                    bloc.reconciliation = RECONCILE_BLIND_IDENTICAL
            comptes[bloc.reconciliation] = comptes.get(bloc.reconciliation, 0) + 1
        # Zones vues par la seule lecture aveugle : signal d'omission de la première.
        for orphelin in orphelins:
            if orphelin.review_state != REVIEW_AI_PROPOSED:
                continue
            orphelin.verify_mode = ROLE_BLIND
            orphelin.verify_verdict = VERDICT_UNMATCHED
            orphelin.reconciliation = RECONCILE_REVIEW
            comptes[RECONCILE_REVIEW] = comptes.get(RECONCILE_REVIEW, 0) + 1
    session.flush()
    refresh_state(session, assessment)
    return comptes


# --------------------------------------------------------------- revue humaine
def _history(session, row, action, avant, reason=None):
    who = actor()
    session.add(TranscriptionBlockHistory(
        block_pk=row.id, action=action,
        before_verbatim=avant.get("human_verbatim"), after_verbatim=row.human_verbatim,
        before_latex=avant.get("human_latex"), after_latex=row.human_latex,
        before_item_ref=avant.get("human_item_ref"), after_item_ref=row.human_item_ref,
        before_state=avant.get("review_state"), after_state=row.review_state,
        reason=reason, actor_identity=who["identity"], actor_role=who["role"]))
    session.flush()


def review_block(session, assessment, block_id_pk, action, verbatim=None, latex=None,
                 note=None, item_ref=None, role=None):
    """Décision humaine sur un bloc. La proposition de l'IA n'est jamais écrasée.

    Chaque révision — y compris la deuxième sur le même bloc — est conservée dans
    ``transcription_block_history`` : avant, après, quand, qui, quelle action, pourquoi.
    """
    row = session.get(TranscriptionBlock, block_id_pk)
    if row is None:
        raise TranscriptionError("bloc de transcription inconnu.")
    if row.assessment_id != assessment.assessment_id:
        raise TranscriptionError("ce bloc n'appartient pas à cette évaluation.")

    avant = {"human_verbatim": row.human_verbatim, "human_latex": row.human_latex,
             "human_item_ref": row.human_item_ref, "review_state": row.review_state}

    if action == "accepter":
        row.review_state = REVIEW_HUMAN_VERIFIED
        row.human_verbatim = row.verbatim
        row.human_latex = row.latex
    elif action == "modifier":
        if verbatim is None or not str(verbatim).strip():
            raise TranscriptionError("une correction humaine demande un texte.")
        row.review_state = REVIEW_HUMAN_VERIFIED
        row.human_verbatim = verbatim
        row.human_latex = latex or None
    elif action == "illisible":
        row.review_state = REVIEW_ILLEGIBLE
        row.human_verbatim = "[illisible]"
        row.human_latex = None
    elif action == "rejeter":
        row.review_state = REVIEW_REJECTED
        row.human_verbatim = None
        row.human_latex = None
    elif action == "decrire":
        # Preuve non textuelle : l'humain décrit ce que l'image montre. La
        # description ne remplace jamais l'image, elle la situe.
        if not (note or verbatim):
            raise TranscriptionError("une description demande un texte.")
        row.human_description = note or verbatim
        row.review_state = REVIEW_HUMAN_VERIFIED
    elif action == "chainer":
        # Liaison entre pages, décidée par l'humain. Le système ne rattache jamais
        # une suite à la question dont elle est physiquement la plus proche.
        row.human_continues_from = verbatim or None
        row.human_continues_to = latex or None
    elif action == "rattacher":
        # Corriger le rattachement sans toucher à la lecture : l'OCR peut lire
        # parfaitement et se tromper de question, ce qui est aussi grave.
        if not item_ref:
            raise TranscriptionError("un rattachement demande une référence d'item.")
        row.human_item_ref = item_ref
    else:
        raise TranscriptionError("action de revue inconnue : %s" % action)

    if item_ref and action != "rattacher":
        row.human_item_ref = item_ref
    who = actor()
    if note:
        row.human_note = note
    row.reviewed_at = dt.datetime.now(dt.timezone.utc)
    row.reviewed_by_role = role or who["role"]
    row.reviewed_by_identity = who["identity"]
    session.flush()
    _history(session, row, action, avant, note)

    audit(session, "transcription.review", "transcription_block", row.id,
          assessment.assessment_id,
          old_value=(avant.get("review_state") or "")[:200],
          new_value="%s → %s" % (action, row.review_state), reason=note)
    refresh_state(session, assessment)
    return row


def attest_page(session, assessment, page_index, attested=True, note=None):
    """Attestation humaine de complétude pour une page.

    C'est la seule réponse à l'angle mort majeur de la revue par blocs : l'interface
    ne montre que ce que les modèles ont vu, et ne peut donc pas signaler une zone
    qu'ils auraient **tous deux** omise. Seul un humain, comparant la page et la
    transcription, peut attester que rien de pertinent ne manque.

    L'attestation porte sur des octets précis : si la page est re-rendue ensuite,
    l'empreinte change et l'attestation devient périmée.
    """
    original = sc.current_copy(session, assessment.assessment_id)
    if original is None:
        raise TranscriptionError("aucune copie rattachée.")
    derived = sc.derived_pages(session, original)
    page = next((r for r in sc.files_of(session, derived)
                 if r.page_index == page_index), None) if derived else None
    if page is None:
        raise TranscriptionError("page %s inconnue." % page_index)

    row = (session.query(PageAttestation)
           .filter_by(source_copy_id=original.source_copy_id,
                      page_index=page_index).one_or_none())
    if row is None:
        row = PageAttestation(source_copy_id=original.source_copy_id,
                              page_index=page_index, page_sha256=page.sha256)
        session.add(row)
    who = actor()
    row.page_sha256 = page.sha256
    row.attested = bool(attested)
    row.note = note
    row.actor_identity = who["identity"]
    row.actor_role = who["role"]
    row.attested_at = dt.datetime.now(dt.timezone.utc)
    session.flush()
    audit(session, "transcription.page_attested", "page_attestation", row.id,
          assessment.assessment_id,
          new_value="page %d : %s" % (page_index,
                                      "complète" if attested else "réservée"),
          reason=note)
    refresh_state(session, assessment)
    return row


def attestation_status(session, original) -> dict:
    derived = sc.derived_pages(session, original)
    pages = sc.files_of(session, derived) if derived else []
    rows = {r.page_index: r for r in session.query(PageAttestation)
            .filter_by(source_copy_id=original.source_copy_id).all()}
    detail, manquantes, perimees = [], [], []
    for page in pages:
        row = rows.get(page.page_index)
        ok = bool(row and row.attested and row.page_sha256 == page.sha256)
        if row is None or not row.attested:
            manquantes.append(page.page_index)
        elif row.page_sha256 != page.sha256:
            perimees.append(page.page_index)
        detail.append({"page_index": page.page_index, "attested": ok,
                       "actor_identity": row.actor_identity if row else None,
                       "attested_at": row.attested_at.isoformat()
                       if row and row.attested_at else None,
                       "note": row.note if row else None})
    return {"pages": len(pages), "attested": sum(1 for d in detail if d["attested"]),
            "missing": manquantes, "stale": perimees, "detail": detail}


# ------------------------------------------------------------------ invariant
def refresh_state(session, assessment):
    """Recalcule l'état d'après l'avancement de la revue **et** des attestations."""
    original = sc.current_copy(session, assessment.assessment_id)
    if original is None:
        return None
    blocs = (session.query(TranscriptionBlock)
             .filter_by(source_copy_id=original.source_copy_id).all())
    if not blocs:
        return _set_state(session, assessment, original, STATE_NOT_STARTED, None)

    pending = [b for b in blocs if b.review_state == REVIEW_AI_PROPOSED]
    attestation = attestation_status(session, original)
    if pending:
        a_trancher = [b for b in pending if b.reconciliation == RECONCILE_REVIEW]
        if a_trancher:
            return _set_state(session, assessment, original, STATE_REVIEW_REQUIRED,
                              "%d bloc(s) à trancher" % len(a_trancher))
        return _set_state(session, assessment, original, STATE_AI_PROPOSED,
                          "%d bloc(s) proposés, non encore vérifiés" % len(pending))
    if attestation["missing"] or attestation["stale"]:
        return _set_state(
            session, assessment, original, STATE_REVIEW_REQUIRED,
            "blocs tranchés, mais complétude non attestée pour %d page(s)"
            % (len(attestation["missing"]) + len(attestation["stale"])))
    return _set_state(session, assessment, original, STATE_HUMAN_VERIFIED,
                      "%d bloc(s) vérifiés, %d page(s) attestées complètes"
                      % (len(blocs), attestation["attested"]))


def transcription_is_usable(session, assessment) -> list:
    """L'invariant unique : ce qui interdit d'exploiter une transcription.

    Toute voie d'exploitation — route, service de domaine, ligne de commande,
    analyse, génération de bilan — passe par cette fonction. Une garde posée sur une
    seule route ne protégerait rien : un autre chemin appellerait le moteur
    directement. Retourne la liste des empêchements ; vide signifie exploitable.
    """
    problemes = []
    original = sc.current_copy(session, assessment.assessment_id)
    if original is None:
        return ["aucune copie rattachée."]
    if original.status != sc.STATUS_ATTACHED:
        problemes.append("la pièce source n'est plus la pièce courante.")
    if not sc.verify(session, original)["ok"]:
        problemes.append("l'empreinte de la pièce source ne se vérifie plus.")

    etat = state_of(session, assessment)
    if etat is None:
        return problemes + ["aucune transcription."]
    if etat.state != STATE_HUMAN_VERIFIED:
        problemes.append("transcription à l'état %s : elle n'a pas été entièrement "
                         "vérifiée par un humain." % etat.state)

    derived = sc.derived_pages(session, original)
    if derived is None:
        problemes.append("les pages rendues sont absentes.")
    elif not sc.verify(session, derived)["ok"]:
        problemes.append("l'empreinte des pages rendues ne se vérifie plus.")

    # Une preuve non textuelle non traitée par un humain n'est pas exploitable : sa
    # description automatique ne vaut pas lecture, et son absence de texte ne vaut
    # surtout pas « non répondu ».
    non_traitees = (session.query(TranscriptionBlock)
                    .filter(TranscriptionBlock.source_copy_id == original.source_copy_id,
                            TranscriptionBlock.reading == READING_PRIMARY,
                            TranscriptionBlock.kind.in_(ocr_schema.NON_TEXT_KINDS),
                            TranscriptionBlock.review_state == REVIEW_AI_PROPOSED)
                    .count())
    if non_traitees:
        problemes.append("%d preuve(s) non textuelle(s) n'ont pas été traitées par un "
                         "humain : une figure peut constituer toute la réponse."
                         % non_traitees)

    attestation = attestation_status(session, original)
    if attestation["missing"]:
        problemes.append("complétude non attestée pour la ou les pages %s."
                         % ", ".join(str(p) for p in attestation["missing"]))
    if attestation["stale"]:
        problemes.append("attestation périmée pour la ou les pages %s : la page a "
                         "été re-rendue depuis."
                         % ", ".join(str(p) for p in attestation["stale"]))

    for run in (session.query(OcrRun)
                .filter_by(source_copy_id=original.source_copy_id).all()):
        if run.status == "RUNNING":
            problemes.append("une campagne de lecture est encore en cours (n° %d)."
                             % run.run_id)
        if is_stale(session, assessment, run):
            problemes.append("la campagne n° %d porte sur une pièce qui n'est plus la "
                             "pièce courante." % run.run_id)
    return problemes


def guard_automated_use(session, assessment) -> list:
    """Nom historique de l'invariant, conservé pour les appelants existants."""
    return transcription_is_usable(session, assessment)


def resume_interrupted(session) -> int:
    """Au démarrage, une campagne restée RUNNING n'a pas survécu au processus.

    Elle ne peut pas être « en cours » : le processus qui la menait n'existe plus. On
    la marque INTERRUPTED, ce qui la rend reprenable — les pages déjà lues sont en
    cache et ne seront pas refacturées — et libère l'index d'unicité.
    """
    en_cours = session.query(OcrRun).filter_by(status="RUNNING").all()
    for run in en_cours:
        run.status = STATE_INTERRUPTED
        run.error = ("campagne interrompue : le processus qui la menait s'est arrêté. "
                     "Elle est reprenable ; les pages déjà lues sont en cache.")
        run.finished_at = dt.datetime.now(dt.timezone.utc)
    session.flush()
    return len(en_cours)


# ------------------------------------------------------------------ synthèse
def summary(session, assessment) -> dict:
    original = sc.current_copy(session, assessment.assessment_id)
    if original is None:
        return {"attached": False, "state": STATE_NOT_STARTED, "blocks": 0}
    derived = sc.derived_pages(session, original)
    rows = (session.query(TranscriptionBlock)
            .filter_by(source_copy_id=original.source_copy_id,
                       reading=READING_PRIMARY)
            .order_by(TranscriptionBlock.page_index,
                      TranscriptionBlock.block_id).all())
    aveugles = (session.query(TranscriptionBlock)
                .filter_by(source_copy_id=original.source_copy_id,
                           reading=READING_BLIND).all())
    runs = (session.query(OcrRun)
            .filter_by(source_copy_id=original.source_copy_id)
            .order_by(OcrRun.run_id).all())
    etat = state_of(session, assessment)

    def count(predicate, source=None):
        return sum(1 for r in (rows if source is None else source) if predicate(r))

    cout, cout_connu = 0.0, False
    for run in runs:
        if run.cost_usd:
            cout += float(run.cost_usd)
            cout_connu = True

    empechements = transcription_is_usable(session, assessment)
    return {
        "attached": True,
        "source_copy_id": original.source_copy_id,
        "derived_copy_id": derived.source_copy_id if derived else None,
        "pages": derived.page_count if derived else None,
        "state": etat.state if etat else STATE_NOT_STARTED,
        "state_detail": etat.detail if etat else None,
        "blocks": len(rows),
        "blind_blocks": len(aveugles),
        "handwritten": count(lambda r: r.origin == "HANDWRITTEN"),
        "math": count(lambda r: r.kind in ("MATH", "MIXED")),
        "crossed_out": count(lambda r: r.status == "CROSSED_OUT"),
        "uncertain": count(lambda r: r.uncertainty != "LOW"),
        "illegible": count(lambda r: "[illisible]" in (r.verbatim or "")),
        "code": count(lambda r: r.kind in ocr_schema.CODE_KINDS),
        "non_text": count(lambda r: r.kind in ocr_schema.NON_TEXT_KINDS),
        "chained": count(lambda r: (r.human_continues_from or r.continues_from
                                    or r.human_continues_to or r.continues_to)),
        "blind_identical": count(
            lambda r: r.reconciliation == RECONCILE_BLIND_IDENTICAL),
        "disagreement": count(lambda r: r.reconciliation == RECONCILE_REVIEW),
        "single_reading": count(lambda r: r.reconciliation == RECONCILE_SINGLE),
        "unmatched": count(lambda r: r.verify_verdict == VERDICT_UNMATCHED),
        "blind_only": count(lambda r: r.verify_verdict == VERDICT_UNMATCHED, aveugles),
        "human_verified": count(lambda r: r.review_state == REVIEW_HUMAN_VERIFIED),
        "human_edited": count(lambda r: r.review_state == REVIEW_HUMAN_VERIFIED
                              and not _same_reading(r.verbatim, r.human_verbatim)),
        "human_illegible": count(lambda r: r.review_state == REVIEW_ILLEGIBLE),
        "human_rejected": count(lambda r: r.review_state == REVIEW_REJECTED),
        "human_realigned": count(lambda r: r.human_item_ref is not None
                                 and r.human_item_ref != r.item_ref),
        "pending_review": count(lambda r: r.review_state == REVIEW_AI_PROPOSED),
        "attestation": attestation_status(session, original),
        "usable": not empechements,
        "blocking": empechements,
        "runs": [{"run_id": r.run_id, "role": r.role, "model_id": r.model_id,
                  "provider_name": r.provider_name, "status": r.status,
                  "verify_mode": r.verify_mode,
                  "prompt_version": r.prompt_version,
                  "prompt_sha256": (r.prompt_sha256 or "")[:16],
                  "schema_version": r.schema_version,
                  "schema_sha256": (r.schema_sha256 or "")[:16],
                  "pages": r.pages_total, "calls": r.calls,
                  "cached_calls": r.cached_calls,
                  "tokens_in": r.tokens_in, "tokens_out": r.tokens_out,
                  "cost_usd": r.cost_usd, "error": r.error,
                  "stale": is_stale(session, assessment, r),
                  "started_at": r.started_at.isoformat() if r.started_at else None}
                 for r in runs],
        "cost_usd": round(cout, 6) if cout_connu else None,
        "openrouter": openrouter.configuration_status(),
    }


def page_view(session, assessment, page_index: int) -> dict:
    original = sc.current_copy(session, assessment.assessment_id)
    if original is None:
        return {"attached": False}
    rows = (session.query(TranscriptionBlock)
            .filter_by(source_copy_id=original.source_copy_id, page_index=page_index,
                       reading=READING_PRIMARY)
            .order_by(TranscriptionBlock.block_id).all())
    orphelins = (session.query(TranscriptionBlock)
                 .filter_by(source_copy_id=original.source_copy_id,
                            page_index=page_index, reading=READING_BLIND,
                            verify_verdict=VERDICT_UNMATCHED).all())
    attestation = (session.query(PageAttestation)
                   .filter_by(source_copy_id=original.source_copy_id,
                              page_index=page_index).one_or_none())
    return {"attached": True, "page_index": page_index,
            "blocks": [_block_dict(r) for r in rows],
            # Zones vues par la seule lecture aveugle : signal d'omission possible de
            # la première lecture, que la revue par blocs ne montrerait pas sinon.
            "blind_only": [_block_dict(r) for r in orphelins],
            "attestation": {
                "attested": bool(attestation and attestation.attested),
                "actor_identity": attestation.actor_identity if attestation else None,
                "attested_at": attestation.attested_at.isoformat()
                if attestation and attestation.attested_at else None,
                "note": attestation.note if attestation else None}}


def _block_dict(row) -> dict:
    return {
        "id": row.id, "block_id": row.block_id, "page_index": row.page_index,
        "reading": row.reading,
        "item_ref": row.item_ref, "human_item_ref": row.human_item_ref,
        "origin": row.origin, "kind": row.kind,
        "status": row.status, "verbatim": row.verbatim, "latex": row.latex,
        "verbatim_code": row.verbatim_code, "language_hint": row.language_hint,
        "ai_description": row.ai_description,
        "human_description": row.human_description,
        "continues_from": row.human_continues_from or row.continues_from,
        "continues_to": row.human_continues_to or row.continues_to,
        "ai_continues_from": row.continues_from, "ai_continues_to": row.continues_to,
        "uncertainty": row.uncertainty,
        "alternatives": json.loads(row.alternatives_json or "[]"),
        "notes": row.notes,
        "verify_mode": row.verify_mode, "verify_verdict": row.verify_verdict,
        "verify_block_id": row.verify_block_id,
        "verify_verbatim": row.verify_verbatim, "verify_latex": row.verify_latex,
        "verify_note": row.verify_note,
        "reconciliation": row.reconciliation, "review_state": row.review_state,
        "human_verbatim": row.human_verbatim, "human_latex": row.human_latex,
        "human_note": row.human_note,
        "reviewed_at": row.reviewed_at.isoformat() if row.reviewed_at else None,
        "reviewed_by_role": row.reviewed_by_role,
        "reviewed_by_identity": row.reviewed_by_identity,
        "retenu": row.human_verbatim if row.review_state != REVIEW_AI_PROPOSED
        else row.verbatim,
    }


def block_history(session, block_pk) -> list:
    rows = (session.query(TranscriptionBlockHistory)
            .filter_by(block_pk=block_pk)
            .order_by(TranscriptionBlockHistory.id).all())
    return [{"action": r.action, "before": r.before_verbatim,
             "after": r.after_verbatim, "before_state": r.before_state,
             "after_state": r.after_state, "reason": r.reason,
             "actor_identity": r.actor_identity, "actor_role": r.actor_role,
             "at": r.created_at.isoformat() if r.created_at else None}
            for r in rows]
