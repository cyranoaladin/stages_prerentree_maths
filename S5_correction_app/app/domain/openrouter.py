# -*- coding: utf-8 -*-
"""Client OpenRouter : appels vision, sous contraintes de confidentialité non négociables.

Ce sont des copies d'élèves mineurs. Toute requête portant une page de copie impose,
sans exception et sans repli silencieux :

* ``provider.data_collection = "deny"`` — aucun fournisseur susceptible de conserver
  les données ;
* ``provider.zdr = true`` — routage restreint aux endpoints Zero Data Retention ;
* ``provider.require_parameters = true`` — seuls les fournisseurs qui honorent tous
  les paramètres envoyés, sorties structurées comprises ;
* ``provider.allow_fallbacks = false`` — pas de report vers un endpoint non contrôlé.

Si aucun endpoint conforme n'existe pour le modèle demandé, l'appel **échoue**. Il ne
se rabat jamais sur un fournisseur moins protecteur : c'est le seul comportement
acceptable quand la donnée est la copie d'un enfant.

La clé n'est jamais journalisée, jamais mise en base, jamais envoyée au navigateur.
Le seul renseignement que l'interface obtient est « configuré » ou « clé absente ».
"""

import base64
import json
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from .. import config

# Valeur d'en-tête HTTP : elle doit être encodable en ASCII. Un tiret cadratin ici
# faisait échouer l'appel **avant même de sortir du poste**, avec un
# « UnicodeEncodeError » qui ne désignait pas l'en-tête fautif. Les en-têtes ne sont
# pas de la prose : le tiret simple ne coûte rien et supprime la classe de panne.
PROMPT_ATTRIBUTION = "Nexus S5 - Correction & Bilans"

# Trois caches existent, et les confondre serait une faute de raisonnement :
#
# 1. le *prompt caching* du fournisseur — mécanisme d'optimisation côté modèle ;
# 2. le *response caching* d'OpenRouter — susceptible de conserver une réponse
#    côté passerelle, et qu'un préréglage de compte peut activer sans que la
#    requête ne le demande ;
# 3. notre cache applicatif local, sous ``runtime/ocr_cache/``, qui ne quitte
#    jamais le poste et relève de notre seule politique.
#
# ``provider.zdr`` porte sur le routage, pas sur le point 2. On désactive donc le
# response caching explicitement, à chaque appel, quel que soit le préréglage du
# compte : c'est le seul levier dont l'application dispose réellement.
NO_RESPONSE_CACHE_HEADER = {"X-OpenRouter-Cache": "false"}

# Contraintes de routage. Elles ne sont pas paramétrables depuis l'interface : les
# assouplir demanderait de modifier ce fichier, ce qui laisse une trace dans Git.
PRIVACY_PROVIDER_BLOCK = {
    "data_collection": "deny",
    "zdr": True,
    "require_parameters": True,
    "allow_fallbacks": False,
}

RETRYABLE_STATUS = {408, 409, 429, 500, 502, 503, 504, 520, 522, 524}
FATAL_STATUS = {400, 401, 402, 403, 404, 413, 422}


class OpenRouterError(Exception):
    """Erreur d'appel. Le message ne contient jamais la clé."""

    def __init__(self, message, status=None, retryable=False, payload=None):
        super().__init__(message)
        self.status = status
        self.retryable = retryable
        self.payload = payload


class MissingKeyError(OpenRouterError):
    pass


class NoCompliantEndpointError(OpenRouterError):
    """Aucun endpoint ne satisfait ZDR + data_collection=deny pour ce modèle."""


class StructuredOutputError(OpenRouterError):
    """Le modèle n'a pas rendu un JSON conforme au schéma demandé."""


class BudgetExceededError(OpenRouterError):
    pass


# ------------------------------------------------------------------ endpoint
def validated_base_url(url: str = None) -> str:
    """L'URL de l'API, contrôlée. Un mauvais endpoint exfiltrerait les copies.

    Seul HTTPS vers un hôte connu est accepté. Un endpoint personnalisé — utile en
    développement pour un bouchon local — exige ``NEXUS_S5_ALLOW_CUSTOM_ENDPOINT=1``,
    et ne s'active donc jamais par un simple réglage passé inaperçu.
    """
    raw = (url or config.OPENROUTER_BASE_URL or "").strip()
    parsed = urlparse(raw)
    if config.ALLOW_CUSTOM_OPENROUTER_ENDPOINT:
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise OpenRouterError("endpoint personnalisé invalide : %s" % raw)
        return raw
    if parsed.scheme != "https":
        raise OpenRouterError(
            "l'API doit être appelée en HTTPS (endpoint refusé : %s). Un endpoint "
            "personnalisé exige NEXUS_S5_ALLOW_CUSTOM_ENDPOINT=1." % raw)
    hote = (parsed.hostname or "").lower()
    if hote not in config.OPENROUTER_ALLOWED_HOSTS:
        raise OpenRouterError(
            "hôte non autorisé pour l'API : « %s ». Les copies d'élèves ne partent "
            "que vers %s. Un endpoint personnalisé exige "
            "NEXUS_S5_ALLOW_CUSTOM_ENDPOINT=1."
            % (hote or "?", ", ".join(config.OPENROUTER_ALLOWED_HOSTS)))
    return raw


# --------------------------------------------------------------------- secret
def _read_key_file() -> str:
    path = Path(config.OPENROUTER_KEY_FILE)
    if not path.exists():
        return ""
    mode = path.stat().st_mode & 0o777
    if mode & 0o077:
        raise MissingKeyError(
            "le fichier de clé %s est lisible par d'autres utilisateurs (mode %o) : "
            "corrigez avec « chmod 600 %s » avant de l'utiliser."
            % (path, mode, path))
    return path.read_text(encoding="utf-8").strip()


def api_key() -> str:
    """La clé, depuis l'environnement puis depuis le fichier local. Jamais journalisée."""
    key = (os.environ.get("OPENROUTER_API_KEY") or "").strip()
    return key or _read_key_file()


def is_configured() -> bool:
    try:
        return bool(api_key())
    except MissingKeyError:
        return False


def configuration_status() -> dict:
    """Ce que l'interface a le droit de savoir. Ni la clé, ni un préfixe, ni sa longueur."""
    try:
        configured = bool(api_key())
        problem = None
    except MissingKeyError as exc:
        configured, problem = False, str(exc)
    return {
        "configured": configured,
        "label": "OpenRouter : configuré" if configured else "OpenRouter : clé absente",
        "problem": problem,
        "base_url": config.OPENROUTER_BASE_URL,
        "model_primary": config.OCR_MODEL_PRIMARY,
        "model_verify": config.OCR_MODEL_VERIFY,
        "privacy": dict(PRIVACY_PROVIDER_BLOCK),
        "no_response_cache": dict(NO_RESPONSE_CACHE_HEADER),
        # L'application ne sait pas lire la configuration du compte OpenRouter.
        # Elle ne prétend donc jamais l'avoir vérifiée.
        "account_privacy_policy": account_privacy_policy(),
        "remote_ocr_allowed_for_real_copies": bool(
            config.ALLOW_REAL_STUDENT_REMOTE_OCR),
    }


def account_privacy_policy() -> str:
    """Ce que l'on sait de la politique du compte : VERIFIED, OPERATOR_ATTESTED, UNKNOWN.

    Aucune API n'expose aujourd'hui la configuration de confidentialité d'un compte
    OpenRouter — journalisation, préréglages, cache de réponse. Le code ne peut donc
    pas la vérifier, et ``UNKNOWN`` ne devient jamais ``VERIFIED`` : au mieux
    ``OPERATOR_ATTESTED``, qui n'est qu'une déclaration humaine et se lit comme telle.
    """
    valeur = config.ACCOUNT_PRIVACY_POLICY
    if valeur == "OPERATOR_ATTESTED":
        return "OPERATOR_ATTESTED"
    # « VERIFIED » ne peut pas être obtenu : le code ne sait pas le démontrer.
    return "UNKNOWN"


_DATA_URL = re.compile(r"data:image/[a-z.+-]+;base64,[A-Za-z0-9+/=]{40,}")
_KEY_LIKE = re.compile(r"sk-or-[A-Za-z0-9\-_]{8,}")
_LONG_B64 = re.compile(r"[A-Za-z0-9+/]{400,}={0,2}")

MAX_REDACTED_CHARS = 2000


def check_header_values(headers: dict) -> None:
    """Refuse un en-tête non transportable, en désignant lequel.

    Les valeurs d'en-tête HTTP sont encodées en ASCII par le client : un caractère
    hors de cette plage lève une ``UnicodeEncodeError`` brute, qui ne dit ni quel
    en-tête est en cause, ni pourquoi. C'est arrivé — un tiret cadratin dans le titre
    d'attribution — et la panne survenait avant tout appel réseau.

    Le cas le plus insidieux reste la clé : collée avec un caractère accentué, elle
    produirait exactement la même panne, et le message ne mentionnerait jamais la clé.
    On la nomme donc, sans jamais l'afficher.
    """
    for nom, valeur in headers.items():
        try:
            str(nom).encode("ascii")
            str(valeur).encode("ascii")
        except UnicodeEncodeError as exc:
            if nom.lower() == "authorization":
                raise MissingKeyError(
                    "la clé OpenRouter contient un caractère non ASCII (position %d) : "
                    "elle n'est pas transportable dans un en-tête HTTP. Vérifiez le "
                    "copier-coller — espace insécable, tiret typographique, accent."
                    % exc.start)
            raise OpenRouterError(
                "l'en-tête « %s » contient un caractère non ASCII : il n'est pas "
                "transportable en HTTP. Les en-têtes ne sont pas de la prose."
                % nom)


def redact(text: str, limite: int = MAX_REDACTED_CHARS) -> str:
    """Nettoie un message avant qu'il ne sorte d'ici.

    Masquer la clé ne suffit pas : une exception peut charrier l'image de la copie
    encodée en base64, un extrait de transcription, ou la réponse brute du
    fournisseur. Un journal applicatif n'a pas à contenir la copie d'un élève.
    """
    try:
        key = api_key()
    except MissingKeyError:
        key = ""
    out = str(text)
    if key:
        out = out.replace(key, "«clé masquée»")
    out = _KEY_LIKE.sub("«clé masquée»", out)
    out = _DATA_URL.sub("«image de copie masquée»", out)
    out = _LONG_B64.sub("«données masquées»", out)
    if len(out) > limite:
        out = out[:limite] + " …(message tronqué : %d caractères)" % len(out)
    return out


# ------------------------------------------------------------------- résultat
@dataclass
class Usage:
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = None

    def as_dict(self):
        return {"tokens_in": self.tokens_in, "tokens_out": self.tokens_out,
                "cost_usd": self.cost_usd}


CACHE_STATUS_HEADER = "x-openrouter-cache-status"


@dataclass
class Completion:
    content: str
    parsed: dict = None
    model_id: str = None
    provider_name: str = None
    generation_id: str = None
    request_id: str = None
    latency_ms: int = 0
    usage: Usage = field(default_factory=Usage)
    # État de cache rapporté par la passerelle. « HIT » sur un appel portant une copie
    # réelle signifierait que notre en-tête n'a pas été honoré.
    cache_status: str = None
    raw: dict = None


# --------------------------------------------------------------------- images
def image_data_url(path, media_type: str = None) -> str:
    """Image encodée en base64, transmise le temps de l'appel.

    L'original probant reste le fichier local : rien n'est déposé dans un stockage
    distant, et aucune copie ne survit à la requête côté client.
    """
    path = Path(path)
    media_type = media_type or ("image/png" if path.suffix.lower() == ".png"
                                else "image/jpeg")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return "data:%s;base64,%s" % (media_type, encoded)


# ---------------------------------------------------------------------- appel
def _client(timeout):
    import httpx
    return httpx.Client(timeout=timeout)


def _sleep(seconds):
    time.sleep(seconds)


def _extract_usage(payload: dict) -> Usage:
    usage = (payload or {}).get("usage") or {}
    cost = usage.get("cost")
    if cost is None:
        cost = (usage.get("cost_details") or {}).get("upstream_inference_cost")
    try:
        cost = float(cost) if cost is not None else None
    except (TypeError, ValueError):
        cost = None
    return Usage(tokens_in=int(usage.get("prompt_tokens") or 0),
                 tokens_out=int(usage.get("completion_tokens") or 0),
                 cost_usd=cost)


def _is_no_endpoint(status: int, body: str) -> bool:
    """OpenRouter refuse la requête quand aucun endpoint ne satisfait les contraintes.

    Le message exact a varié ; on reconnaît la situation sur plusieurs formulations
    plutôt que sur une seule, et on ne la confond jamais avec une panne passagère.
    """
    lowered = (body or "").lower()
    marks = ("no endpoints found", "no allowed providers", "no providers available",
             "zdr", "data policy", "no endpoints match")
    return status in (404, 403, 400) and any(m in lowered for m in marks)


def chat(messages, model: str, response_format: dict = None, temperature: float = 0,
         max_tokens: int = 8000, extra_body: dict = None, timeout: int = None,
         max_retries: int = None) -> Completion:
    """Un appel de complétion, contraintes de confidentialité comprises.

    Les erreurs transitoires sont réessayées avec un recul croissant et borné. Les
    erreurs d'authentification, de charge utile ou d'absence d'endpoint conforme ne
    sont **jamais** réessayées, et ne déclenchent aucun repli vers un autre modèle.
    """
    import httpx

    key = api_key()
    if not key:
        raise MissingKeyError(
            "OPENROUTER_API_KEY n'est pas configurée. Renseignez la variable "
            "d'environnement, ou déposez la clé dans %s avec le mode 600."
            % config.OPENROUTER_KEY_FILE)

    timeout = timeout or config.OPENROUTER_TIMEOUT_SECONDS
    max_retries = config.OPENROUTER_MAX_RETRIES if max_retries is None else max_retries

    body = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "provider": dict(PRIVACY_PROVIDER_BLOCK),
        # Le coût réel de l'appel, quand le fournisseur le remonte.
        "usage": {"include": True},
    }
    if response_format:
        body["response_format"] = response_format
    if extra_body:
        body.update(extra_body)

    headers = {
        "Authorization": "Bearer %s" % key,
        "Content-Type": "application/json",
        "X-Title": PROMPT_ATTRIBUTION,
    }
    # Jamais optionnel, jamais paramétrable depuis l'interface.
    headers.update(NO_RESPONSE_CACHE_HEADER)
    # Contrôlés avant tout appel : une panne d'encodage doit dire ce qui la cause.
    check_header_values(headers)
    url = "%s/chat/completions" % validated_base_url().rstrip("/")

    attempt, delay, last = 0, 1.0, None
    while attempt <= max_retries:
        attempt += 1
        started = time.monotonic()
        try:
            with _client(timeout) as client:
                response = client.post(url, headers=headers, json=body)
            elapsed = int((time.monotonic() - started) * 1000)
            text = response.text
            # Un modèle défaillant ne doit pas pouvoir remplir la base : la réponse
            # est bornée avant même d'être analysée.
            if len(text) > config.OCR_MAX_RESPONSE_BYTES:
                raise OpenRouterError(
                    "réponse de %d octets, au-delà du plafond de %d : le modèle « %s » "
                    "est écarté plutôt que de laisser grossir la base."
                    % (len(text), config.OCR_MAX_RESPONSE_BYTES, model),
                    status=response.status_code, retryable=False)
            if response.status_code == 200:
                try:
                    payload = response.json()
                except ValueError:
                    raise OpenRouterError("réponse OpenRouter illisible (JSON invalide)",
                                          status=200, retryable=True)
                # Une erreur peut arriver dans un corps 200.
                if isinstance(payload, dict) and payload.get("error"):
                    detail = json.dumps(payload["error"], ensure_ascii=False)
                    if _is_no_endpoint(404, detail):
                        raise NoCompliantEndpointError(
                            "aucun endpoint ZDR sans conservation de données pour « %s » : "
                            "l'appel est refusé plutôt que rerouté. %s"
                            % (model, redact(detail)), status=404)
                    raise OpenRouterError("OpenRouter a renvoyé une erreur : %s"
                                          % redact(detail), status=200, retryable=True)
                return _build_completion(payload, response, elapsed, response_format, model)

            if _is_no_endpoint(response.status_code, text):
                raise NoCompliantEndpointError(
                    "aucun endpoint ZDR sans conservation de données pour « %s » : "
                    "l'appel est refusé plutôt que rerouté. %s"
                    % (model, redact(text)[:400]), status=response.status_code)
            if response.status_code in FATAL_STATUS:
                raise OpenRouterError("OpenRouter a refusé la requête (HTTP %d) : %s"
                                      % (response.status_code, redact(text)[:400]),
                                      status=response.status_code, retryable=False)
            if response.status_code in RETRYABLE_STATUS:
                last = OpenRouterError("OpenRouter indisponible (HTTP %d)"
                                       % response.status_code,
                                       status=response.status_code, retryable=True)
                # Respecte Retry-After lorsqu'il est fourni.
                wait = response.headers.get("retry-after")
                pause = float(wait) if (wait or "").replace(".", "", 1).isdigit() else delay
            else:
                raise OpenRouterError("réponse OpenRouter inattendue (HTTP %d) : %s"
                                      % (response.status_code, redact(text)[:300]),
                                      status=response.status_code, retryable=False)
        except (httpx.TimeoutException, httpx.TransportError) as exc:
            last = OpenRouterError("échec réseau vers OpenRouter : %s"
                                   % redact(type(exc).__name__), retryable=True)
            pause = delay
        except (NoCompliantEndpointError, MissingKeyError, StructuredOutputError):
            raise
        except OpenRouterError as exc:
            if not exc.retryable:
                raise
            last, pause = exc, delay

        if attempt > max_retries:
            break
        _sleep(min(pause, 30.0))
        delay = min(delay * 2, 30.0)

    raise last or OpenRouterError("appel OpenRouter impossible après %d tentative(s)"
                                  % attempt)


def _build_completion(payload, response, elapsed, response_format, model) -> Completion:
    choices = payload.get("choices") or []
    if not choices:
        raise OpenRouterError("réponse OpenRouter sans contenu", status=200, retryable=True)
    message = choices[0].get("message") or {}
    content = message.get("content")
    if isinstance(content, list):      # certains fournisseurs renvoient des segments
        content = "".join(part.get("text", "") for part in content
                          if isinstance(part, dict))
    content = content or ""

    parsed = None
    if response_format:
        parsed = _parse_structured(content, model)

    return Completion(
        content=content, parsed=parsed,
        model_id=payload.get("model") or model,
        provider_name=payload.get("provider"),
        generation_id=payload.get("id"),
        request_id=response.headers.get("x-request-id"),
        cache_status=response.headers.get(CACHE_STATUS_HEADER),
        latency_ms=elapsed,
        usage=_extract_usage(payload),
        raw=payload)


def _parse_structured(content: str, model: str) -> dict:
    """Le contenu doit être un objet JSON. On ne « répare » pas une sortie non conforme.

    Un modèle qui n'honore pas le schéma est un modèle inadapté à cet usage : le
    signaler vaut mieux que rafistoler un JSON approximatif et faire croire à une
    transcription structurée.
    """
    text = (content or "").strip()
    if text.startswith("```"):
        # Certains modèles encadrent malgré tout leur JSON. On retire l'enveloppe,
        # ce qui reste une lecture du contenu, pas une réparation de sa structure.
        text = text.split("\n", 1)[-1] if "\n" in text else text
        if text.endswith("```"):
            text = text[: text.rfind("```")]
        text = text.strip()
    try:
        parsed = json.loads(text)
    except ValueError as exc:
        raise StructuredOutputError(
            "le modèle « %s » n'a pas rendu un JSON exploitable (%s). Ce modèle ne "
            "convient pas à la lecture structurée." % (model, exc), status=200)
    if not isinstance(parsed, dict):
        raise StructuredOutputError(
            "le modèle « %s » a rendu un JSON qui n'est pas un objet." % model, status=200)
    return parsed
