# -*- coding: utf-8 -*-
"""Schémas de sortie structurée, et leur validation locale.

Un paragraphe libre produit par un modèle n'est pas exploitable : il faudrait le
reparser, donc l'interpréter, donc risquer d'y lire autre chose que ce qu'il dit.
On impose un schéma JSON, et on revalide localement ce qui revient — le contrat
« strict » côté fournisseur ne dispense pas de vérifier.

``bbox`` est facultatif à dessein. Les modèles de vision généralistes ne fournissent
pas de coordonnées fiables ; prétendre le contraire donnerait une fausse précision
spatiale. Quand la boîte est absente, elle vaut null, et l'interface ne dessine rien.
"""

import json

from .. import config

SCHEMA_VERSION = "ocr-page-v1"
VERIFY_SCHEMA_VERSION = "ocr-verify-v1"

# Empreintes techniques des schémas : un caractère modifié sans changement
# de nom de version doit invalider le cache et se voir dans l'audit.
def schema_sha256(schema: dict) -> str:
    import hashlib
    return hashlib.sha256(
        json.dumps(schema, sort_keys=True, ensure_ascii=False).encode(
            "utf-8")).hexdigest()

BLOCK_ORIGINS = ("PRINTED", "HANDWRITTEN", "DIAGRAM_ANNOTATION")

# Toute preuve d'élève n'est pas du texte. Une figure, une droite graduée annotée,
# un tableau ou un programme peuvent constituer la réponse entière — et l'absence de
# texte transcrit ne vaut JAMAIS « non répondu ».
TEXTUAL_KINDS = ("TEXT", "MATH", "MIXED")
CODE_KINDS = ("CODE",)
NON_TEXT_KINDS = ("DIAGRAM", "GRAPH", "TABLE", "GEOMETRY", "OTHER_NON_TEXT")
BLOCK_KINDS = TEXTUAL_KINDS + CODE_KINDS + NON_TEXT_KINDS
BLOCK_STATUSES = ("ACTIVE", "CROSSED_OUT", "OVERWRITTEN", "AMBIGUOUS")
UNCERTAINTY_LEVELS = ("LOW", "MEDIUM", "HIGH")
VERDICTS = ("AGREE", "DISAGREE", "UNCERTAIN")

PAGE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["page_index", "orientation", "blocks"],
    "properties": {
        "page_index": {"type": "integer"},
        "orientation": {"type": "string",
                        "enum": ["UPRIGHT", "ROTATED_90", "ROTATED_180",
                                 "ROTATED_270", "UNKNOWN"]},
        "page_note": {"type": ["string", "null"]},
        "blocks": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["block_id", "origin", "kind", "status", "verbatim",
                             "uncertainty"],
                "properties": {
                    "block_id": {"type": "string"},
                    "item_ref": {"type": ["string", "null"]},
                    "origin": {"type": "string", "enum": list(BLOCK_ORIGINS)},
                    "kind": {"type": "string", "enum": list(BLOCK_KINDS)},
                    "status": {"type": "string", "enum": list(BLOCK_STATUSES)},
                    "verbatim": {"type": "string"},
                    "latex": {"type": ["string", "null"]},
                    "verbatim_code": {"type": ["string", "null"]},
                    "language_hint": {"type": ["string", "null"]},
                    "ai_description": {"type": ["string", "null"]},
                    "continues_from": {"type": ["string", "null"]},
                    "continues_to": {"type": ["string", "null"]},
                    "uncertainty": {"type": "string", "enum": list(UNCERTAINTY_LEVELS)},
                    "alternatives": {"type": "array", "items": {"type": "string"}},
                    "notes": {"type": ["string", "null"]},
                    "bbox": {
                        "type": ["object", "null"],
                        "additionalProperties": False,
                        "required": ["x", "y", "width", "height"],
                        "properties": {"x": {"type": "number"}, "y": {"type": "number"},
                                       "width": {"type": "number"},
                                       "height": {"type": "number"}},
                    },
                },
            },
        },
    },
}

VERIFY_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["page_index", "verdicts"],
    "properties": {
        "page_index": {"type": "integer"},
        "verdicts": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["block_id", "verdict"],
                "properties": {
                    "block_id": {"type": "string"},
                    "verdict": {"type": "string", "enum": list(VERDICTS)},
                    "verbatim": {"type": ["string", "null"]},
                    "latex": {"type": ["string", "null"]},
                    "note": {"type": ["string", "null"]},
                },
            },
        },
    },
}


def response_format(name: str, schema: dict) -> dict:
    return {"type": "json_schema",
            "json_schema": {"name": name, "strict": True, "schema": schema}}


PAGE_RESPONSE_FORMAT = response_format("page_transcription", PAGE_SCHEMA)
VERIFY_RESPONSE_FORMAT = response_format("page_verification", VERIFY_SCHEMA)

PAGE_SCHEMA_SHA256 = schema_sha256(PAGE_SCHEMA)
VERIFY_SCHEMA_SHA256 = schema_sha256(VERIFY_SCHEMA)


class SchemaError(ValueError):
    """Sortie non conforme. On refuse, on ne rafistole pas."""


def _require(condition, message):
    if not condition:
        raise SchemaError(message)


def validate_page(payload: dict) -> dict:
    """Revalide localement une transcription de page, et normalise ses valeurs.

    On ne fait confiance ni au fournisseur, ni au drapeau « strict » : c'est ici que
    l'on constate que le modèle a réellement honoré le contrat.
    """
    _require(isinstance(payload, dict), "la réponse n'est pas un objet JSON")
    _require(isinstance(payload.get("page_index"), int),
             "page_index manquant ou non entier")
    blocks = payload.get("blocks")
    _require(isinstance(blocks, list), "blocks manquant ou non liste")

    if len(blocks) > config.OCR_MAX_BLOCKS_PER_PAGE:
        raise SchemaError(
            "%d blocs pour une page, au-delà du plafond de %d : réponse écartée."
            % (len(blocks), config.OCR_MAX_BLOCKS_PER_PAGE))

    seen, normalised = set(), []
    for position, block in enumerate(blocks, start=1):
        _require(isinstance(block, dict), "bloc %d : ce n'est pas un objet" % position)
        block_id = str(block.get("block_id") or "").strip() or "b%03d" % position
        # Un identifiant dupliqué rendrait la revue humaine ambiguë.
        if block_id in seen:
            block_id = "%s_%03d" % (block_id, position)
        seen.add(block_id)

        origin = block.get("origin")
        kind = block.get("kind")
        status = block.get("status")
        uncertainty = block.get("uncertainty")
        _require(origin in BLOCK_ORIGINS, "bloc %s : origin « %s » hors valeurs admises"
                 % (block_id, origin))
        _require(kind in BLOCK_KINDS, "bloc %s : kind « %s » hors valeurs admises"
                 % (block_id, kind))
        _require(status in BLOCK_STATUSES, "bloc %s : status « %s » hors valeurs admises"
                 % (block_id, status))
        _require(uncertainty in UNCERTAINTY_LEVELS,
                 "bloc %s : uncertainty « %s » hors valeurs admises"
                 % (block_id, uncertainty))
        verbatim = block.get("verbatim")
        _require(isinstance(verbatim, str), "bloc %s : verbatim absent" % block_id)
        _require(len(verbatim) <= config.OCR_MAX_VERBATIM_CHARS,
                 "bloc %s : verbatim de %d caractères, au-delà du plafond de %d"
                 % (block_id, len(verbatim), config.OCR_MAX_VERBATIM_CHARS))
        # Un programme : la mise en forme EST la donnée. On ne « nettoie » rien,
        # on ne remplace aucune tabulation, on ne réindente pas.
        code = block.get("verbatim_code")
        if code is not None:
            _require(isinstance(code, str) and
                     len(code) <= config.OCR_MAX_VERBATIM_CHARS,
                     "bloc %s : verbatim_code trop long ou mal typé" % block_id)
        if kind in CODE_KINDS and not (code or "").strip() \
                and not (verbatim or "").strip():
            raise SchemaError("bloc %s : bloc CODE sans contenu" % block_id)

        description = block.get("ai_description") or None
        if description is not None:
            _require(isinstance(description, str) and
                     len(description) <= config.OCR_MAX_NOTES_CHARS,
                     "bloc %s : ai_description trop longue" % block_id)
        if kind in NON_TEXT_KINDS:
            # Une preuve non textuelle doit être décrite ou signalée, jamais rendue
            # invisible : c'est peut-être toute la réponse de l'élève.
            _require(description or (verbatim or "").strip() or block.get("notes"),
                     "bloc %s : preuve non textuelle sans description ni repère : "
                     "elle disparaîtrait de la revue" % block_id)

        latex = block.get("latex") or None
        if latex is not None:
            _require(isinstance(latex, str) and
                     len(latex) <= config.OCR_MAX_LATEX_CHARS,
                     "bloc %s : latex trop long ou mal typé" % block_id)
        notes = block.get("notes") or None
        if notes is not None:
            _require(isinstance(notes, str) and
                     len(notes) <= config.OCR_MAX_NOTES_CHARS,
                     "bloc %s : notes trop longues" % block_id)

        alternatives = block.get("alternatives") or []
        _require(isinstance(alternatives, list),
                 "bloc %s : alternatives n'est pas une liste" % block_id)
        _require(len(alternatives) <= config.OCR_MAX_ALTERNATIVES,
                 "bloc %s : %d alternatives, au-delà du plafond de %d"
                 % (block_id, len(alternatives), config.OCR_MAX_ALTERNATIVES))
        alternatives = [str(a)[:config.OCR_MAX_VERBATIM_CHARS] for a in alternatives]

        bbox = block.get("bbox")
        if bbox is not None:
            _require(isinstance(bbox, dict) and
                     all(isinstance(bbox.get(k), (int, float))
                         for k in ("x", "y", "width", "height")),
                     "bloc %s : bbox mal formée" % block_id)

        normalised.append({
            "block_id": block_id,
            "item_ref": (block.get("item_ref") or None),
            "origin": origin, "kind": kind, "status": status,
            "verbatim": verbatim,
            "latex": latex,
            "verbatim_code": code,
            "language_hint": (block.get("language_hint") or None),
            "ai_description": description,
            "continues_from": (block.get("continues_from") or None),
            "continues_to": (block.get("continues_to") or None),
            "uncertainty": uncertainty,
            "alternatives": alternatives,
            "notes": notes,
            "bbox": bbox,
        })

    orientation = payload.get("orientation")
    if orientation not in ("UPRIGHT", "ROTATED_90", "ROTATED_180", "ROTATED_270",
                           "UNKNOWN"):
        orientation = "UNKNOWN"
    return {"page_index": payload["page_index"], "orientation": orientation,
            "page_note": payload.get("page_note") or None, "blocks": normalised}


def validate_verification(payload: dict) -> dict:
    _require(isinstance(payload, dict), "la réponse n'est pas un objet JSON")
    verdicts = payload.get("verdicts")
    _require(isinstance(verdicts, list), "verdicts manquant ou non liste")
    out = []
    for position, entry in enumerate(verdicts, start=1):
        _require(isinstance(entry, dict), "verdict %d : ce n'est pas un objet" % position)
        block_id = str(entry.get("block_id") or "").strip()
        _require(block_id, "verdict %d : block_id absent" % position)
        verdict = entry.get("verdict")
        _require(verdict in VERDICTS,
                 "verdict %s : « %s » hors valeurs admises" % (block_id, verdict))
        out.append({"block_id": block_id, "verdict": verdict,
                    "verbatim": entry.get("verbatim") or None,
                    "latex": entry.get("latex") or None,
                    "note": entry.get("note") or None})
    return {"page_index": payload.get("page_index"), "verdicts": out}
