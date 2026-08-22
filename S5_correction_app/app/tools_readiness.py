# -*- coding: utf-8 -*-
"""Assemblage de l'état de mise en service, pour la page d'administration.

Le calcul vit ici plutôt que dans la route : il est ainsi appelable depuis un
test ou depuis un outil en ligne de commande, sans passer par HTTP.
"""

from . import APP_VERSION, config
from .domain import immutability
from .domain.longitudinal import readiness as long_readiness
from .models import Assessment, Student


def etat_mise_en_service(session) -> dict:
    rapport = immutability.verify()
    etats = long_readiness.evaluate_all(session, config)
    resume = long_readiness.summary(etats)

    reelles = _corrections_reelles()

    return {
        "app_version": APP_VERSION,
        "immutability": {"total": rapport.total, "changed": len(rapport.changed),
                         "missing": len(rapport.missing), "verdict": rapport.verdict,
                         "ok": rapport.ok},
        "referentiel": {"students": session.query(Student).count(),
                        "assessments": session.query(Assessment).count()},
        "readiness": resume,
        "readiness_rows": etats,
        "real_corrections": reelles,
        "readonly": config.settings.readonly,
        "readonly_reason": config.settings.readonly_reason,
    }


def _corrections_reelles():
    """Nombre de corrections non synthétiques portant des données saisies."""
    import sys
    from pathlib import Path
    outils = Path(__file__).resolve().parent.parent / "tools"
    if str(outils.parent) not in sys.path:
        sys.path.insert(0, str(outils.parent))
    from tools.init_database import real_corrections
    return len(real_corrections(config.DB_PATH))
