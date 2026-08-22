# -*- coding: utf-8 -*-
"""Schémas d'entrée et de sortie de l'API.

Le rôle de ces modèles est de refuser tôt ce qui n'a pas de sens : un score négatif, un
code d'erreur inventé, une certitude hors échelle. Les règles métier — invariant erreur /
réussite, cohérence d'un critère mixte — restent dans le domaine, où elles sont testées.
"""

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from .domain.correction import ERROR_CODES, SCORING_STATUSES


class ResponseIn(BaseModel):
    score_centi: Optional[int] = Field(default=None, ge=0, le=10000)
    error_codes: List[str] = Field(default_factory=list)
    observation: Optional[str] = Field(default=None, max_length=4000)
    accepted_alternative_method: bool = False
    scoring_status: Optional[str] = None

    @field_validator("error_codes")
    @classmethod
    def _codes(cls, value):
        for code in value:
            if code not in ERROR_CODES:
                raise ValueError("code d'erreur inconnu : %s" % code)
        return sorted(set(value))

    @field_validator("scoring_status")
    @classmethod
    def _status(cls, value):
        if value in (None, ""):
            return None
        if value not in SCORING_STATUSES:
            raise ValueError("statut de saisie inconnu : %s" % value)
        return value


class ItemObservationIn(BaseModel):
    confidence: Optional[int] = Field(default=None, ge=1, le=4)
    observation: Optional[str] = Field(default=None, max_length=4000)


class GeneralObservationsIn(BaseModel):
    """Un choix structuré et un commentaire facultatif par rubrique.

    Les champs restent optionnels : ces observations sont un appui pour le bilan, pas
    une case à remplir, et elles n'entrent dans aucun calcul de points.
    """

    model_config = {"extra": "forbid"}

    autonomie_choix: Optional[str] = Field(default=None, max_length=120)
    autonomie_commentaire: Optional[str] = Field(default=None, max_length=2000)
    methode_choix: Optional[str] = Field(default=None, max_length=120)
    methode_commentaire: Optional[str] = Field(default=None, max_length=2000)
    rythme_choix: Optional[str] = Field(default=None, max_length=120)
    rythme_commentaire: Optional[str] = Field(default=None, max_length=2000)
    redaction_choix: Optional[str] = Field(default=None, max_length=120)
    redaction_commentaire: Optional[str] = Field(default=None, max_length=2000)
    controle_choix: Optional[str] = Field(default=None, max_length=120)
    controle_commentaire: Optional[str] = Field(default=None, max_length=2000)
    erreur_choix: Optional[str] = Field(default=None, max_length=120)
    erreur_commentaire: Optional[str] = Field(default=None, max_length=2000)
    libre_commentaire: Optional[str] = Field(default=None, max_length=4000)
    observed_duration_minutes: Optional[int] = Field(default=None, ge=0, le=600)


class ReopenIn(BaseModel):
    reason: str = Field(min_length=5, max_length=2000)


class BlockEditIn(BaseModel):
    content: str = Field(max_length=20000)
    approve: bool = True
