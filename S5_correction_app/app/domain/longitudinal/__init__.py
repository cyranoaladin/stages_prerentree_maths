# -*- coding: utf-8 -*-
"""Pipeline de bilan longitudinal de fin de stage.

Le bilan répond à sept questions, dans cet ordre : d'où partait l'élève, pourquoi ce
parcours a été choisi, ce qui a été travaillé avec lui, ce qu'il montre aujourd'hui,
ce qui reste fragile, ce qui est déjà prometteur pour l'année suivante, et ce qu'il
doit faire pendant les quatre premières semaines.

Il ne répond pas à « combien a-t-il eu ? ». Le score y figure, mais comme une donnée
parmi d'autres, jamais comme la conclusion.
"""

from .service import LongitudinalError, LongitudinalReportService   # noqa: F401

__all__ = ["LongitudinalReportService", "LongitudinalError"]
