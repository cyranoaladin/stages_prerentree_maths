# -*- coding: utf-8 -*-
"""Configuration : chemins, réseau, garde-fous.

Deux principes tenus ici. D'abord, l'application n'écoute que sur la boucle locale tant
qu'un drapeau explicite n'a pas été posé. Ensuite, aucun chemin d'écriture ne sort de
``runtime/`` : les répertoires sources sont ouverts en lecture, et seulement en lecture.
"""

import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
REPO_ROOT = PROJECT_DIR.parent

# --------------------------------------------------------------- sources en lecture
V3_ROOT = Path(os.environ.get("NEXUS_S5_V3_ROOT", REPO_ROOT / "S5_post_distribution_v3"))
CLOTURE_ROOT = Path(os.environ.get("NEXUS_S5_CLOTURE_ROOT", REPO_ROOT / "S5_cloture"))

IMMUTABLE_MANIFEST = V3_ROOT / "IMMUTABLE_STUDENT_ARTIFACTS.json"
CRITERIA_SCOPE = V3_ROOT / "curriculum_scope" / "criteria_scope.json"
ANALYSIS_SKILLS = V3_ROOT / "curriculum_scope" / "analysis_skills.json"
CURRICULUM_REFS = V3_ROOT / "curriculum_scope" / "curriculum_references.json"
OVERLAYS_DIR = V3_ROOT / "correction_overlays"
DELAYED_CHECKS = V3_ROOT / "teacher_guidance" / "mini_test_differe_s2.json"

# Racines dans lesquelles un document peut être servi. Toute demande résolue hors de
# cette liste est refusée, quel que soit le chemin demandé.
DOCUMENT_ROOTS = (CLOTURE_ROOT.resolve(), V3_ROOT.resolve())

# --------------------------------------------------------------- écritures
RUNTIME_DIR = Path(os.environ.get("NEXUS_S5_RUNTIME", PROJECT_DIR / "runtime"))
DB_PATH = Path(os.environ.get("NEXUS_S5_DB", RUNTIME_DIR / "corrections.sqlite3"))
EXPORTS_DIR = RUNTIME_DIR / "exports"
REPORTS_DIR = RUNTIME_DIR / "reports"
BACKUPS_DIR = RUNTIME_DIR / "backups"
BUILD_DIR = RUNTIME_DIR / "build"

LATEX_DIR = PROJECT_DIR / "latex"
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"

# --------------------------------------------------------------- réseau
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765

# --------------------------------------------------------------- LaTeX
LATEX_ENGINE = os.environ.get("NEXUS_S5_LATEX_ENGINE", "pdflatex")
LATEX_TIMEOUT_SECONDS = int(os.environ.get("NEXUS_S5_LATEX_TIMEOUT", "180"))

# --------------------------------------------------------------- divers
TIMEZONE = "Africa/Tunis"
SCORE_SCALE = 100          # les points sont stockés en centièmes entiers
SCORE_STEP = 5             # tout montant du barème est un multiple de 0,05 point


def ensure_runtime() -> None:
    """Crée les répertoires d'écriture. N'écrit rien d'autre."""
    for d in (RUNTIME_DIR, EXPORTS_DIR, REPORTS_DIR, BACKUPS_DIR, BUILD_DIR):
        d.mkdir(parents=True, exist_ok=True)


class Settings:
    """État mutable du processus : ce que la ligne de commande a décidé."""

    def __init__(self):
        self.readonly = False
        self.readonly_reason = ""
        self.allow_network = False
        self.host = DEFAULT_HOST
        self.port = DEFAULT_PORT
        self.pilot_mode = True          # tant que le premier cas réel n'est pas validé

    def set_readonly(self, reason: str) -> None:
        self.readonly = True
        self.readonly_reason = reason


settings = Settings()
