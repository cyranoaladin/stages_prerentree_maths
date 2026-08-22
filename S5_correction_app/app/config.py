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
# Copies réelles des élèves. Elles sont des pièces probantes : recopiées ici en
# lecture seule, jamais modifiées en place, et incluses dans la sauvegarde.
SOURCE_COPIES_DIR = RUNTIME_DIR / "source_copies"
# Résultats OCR mis en cache par (page, modèle, prompt, schéma) : relire une page
# déjà lue ne doit pas être refacturé.
OCR_CACHE_DIR = RUNTIME_DIR / "ocr_cache"
# Secret local, hors Git, permissions restreintes. L'environnement reste prioritaire.
SECRETS_DIR = RUNTIME_DIR / "secrets"
OPENROUTER_KEY_FILE = SECRETS_DIR / "openrouter.key"

LATEX_DIR = PROJECT_DIR / "latex"
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"

# ----------------------------------------------------- mode de données
# REAL : le poste manipule des copies d'élèves réelles. L'authentification est exigée,
#        y compris sur la boucle locale, et le transport en clair hors boucle locale
#        est refusé. C'est le défaut : un déploiement qui oublie de se déclarer est
#        protégé, pas exposé.
# SYNTHETIC : fixtures uniquement. L'absence d'authentification y est explicitement
#        autorisée, parce qu'il n'y a rien à protéger.
DATA_MODE = (os.environ.get("S5_DATA_MODE") or "REAL").strip().upper()
DATA_MODES = ("REAL", "SYNTHETIC")

# Le proxy inverse qui termine TLS doit être déclaré : « X-Forwarded-Proto » envoyé
# par n'importe quel client ne prouve rien.
TRUSTED_PROXY_TLS = os.environ.get("NEXUS_S5_TRUSTED_PROXY_TLS", "0") == "1"
TRUSTED_PROXY_HOSTS = tuple(
    h.strip() for h in (os.environ.get("NEXUS_S5_TRUSTED_PROXY_HOSTS")
                        or "127.0.0.1,::1").split(",") if h.strip())

# --------------------------------------------------------------- réseau
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765

# ------------------------------------------------- téléversement des copies
# Une copie scannée de plusieurs dizaines de pages en 300 dpi reste volumineuse ;
# la limite doit laisser passer un PDF scolaire normal sans ouvrir la porte à un
# fichier arbitraire. Les deux bornes sont configurables.
UPLOAD_MAX_BYTES = int(os.environ.get("NEXUS_S5_UPLOAD_MAX_BYTES", str(120 * 1024 * 1024)))
UPLOAD_MAX_PAGES = int(os.environ.get("NEXUS_S5_UPLOAD_MAX_PAGES", "60"))
UPLOAD_MAX_FILES = int(os.environ.get("NEXUS_S5_UPLOAD_MAX_FILES", "60"))

# ------------------------------------------------------------- rastérisation
# Résolution des pages dérivées destinées à la lecture assistée. 300 dpi est le
# point de départ mesuré : en dessous, les exposants, les indices et la barre de
# fraction deviennent difficiles à distinguer d'un signe moins.
RASTER_DPI = int(os.environ.get("NEXUS_S5_RASTER_DPI", "300"))
RASTER_MAX_PIXELS = int(os.environ.get("NEXUS_S5_RASTER_MAX_PIXELS", str(40_000_000)))
# Le rastériseur traite un fichier fourni par l'utilisateur : un délai d'attente ne
# borne que la durée, pas la consommation. Ces limites sont posées par le noyau dans
# le processus enfant.
RASTER_CPU_SECONDS = int(os.environ.get("NEXUS_S5_RASTER_CPU_SECONDS", "300"))
RASTER_MEMORY_BYTES = int(os.environ.get("NEXUS_S5_RASTER_MEMORY_BYTES",
                                         str(3 * 1024 * 1024 * 1024)))
RASTER_OUTPUT_MAX_BYTES = int(os.environ.get("NEXUS_S5_RASTER_OUTPUT_MAX_BYTES",
                                             str(2 * 1024 * 1024 * 1024)))

# --------------------------------------------------------------- OpenRouter
OPENROUTER_BASE_URL = os.environ.get("OPENROUTER_BASE_URL",
                                     "https://openrouter.ai/api/v1")
# Modèles configurables : le catalogue OpenRouter évolue, et figer un modèle dans
# le code condamnerait l'application à vieillir avec lui.
OCR_MODEL_PRIMARY = os.environ.get("OCR_MODEL_PRIMARY", "google/gemini-3.1-pro-preview")
OCR_MODEL_VERIFY = os.environ.get("OCR_MODEL_VERIFY", "meta-llama/llama-4-maverick")
OCR_MODEL_BASELINE = os.environ.get("OCR_MODEL_BASELINE", "mistralai/mistral-medium-3.1")

# Hôtes autorisés pour l'API. Un endpoint personnalisé exfiltrerait les copies :
# il exige NEXUS_S5_ALLOW_CUSTOM_ENDPOINT=1, jamais un simple réglage silencieux.
OPENROUTER_ALLOWED_HOSTS = ("openrouter.ai",)
ALLOW_CUSTOM_OPENROUTER_ENDPOINT = os.environ.get(
    "NEXUS_S5_ALLOW_CUSTOM_ENDPOINT", "0") == "1"

# Garde-fou d'envoi distant. Une pièce REAL_STUDENT_COPY ne part chez un fournisseur
# que si l'opérateur l'a explicitement autorisé. Les fixtures synthétiques du smoke
# test n'en dépendent pas : elles ne contiennent aucune donnée d'élève.
ALLOW_REAL_STUDENT_REMOTE_OCR = os.environ.get(
    "ALLOW_REAL_STUDENT_REMOTE_OCR", "0") == "1"

# Ce que l'application peut réellement savoir de la politique du compte OpenRouter :
# rien, tant qu'aucune API ne l'expose. « OPERATOR_ATTESTED » se déclare à la main et
# ne vaut que ce que vaut la déclaration ; UNKNOWN ne devient jamais VERIFIED.
ACCOUNT_PRIVACY_POLICY = (os.environ.get("NEXUS_S5_ACCOUNT_PRIVACY_POLICY")
                          or "UNKNOWN").strip().upper()

# Bornes de sortie : un modèle défaillant ne doit pas remplir la base.
OCR_MAX_RESPONSE_BYTES = int(os.environ.get("NEXUS_S5_OCR_MAX_RESPONSE_BYTES",
                                            str(2 * 1024 * 1024)))
OCR_MAX_BLOCKS_PER_PAGE = int(os.environ.get("NEXUS_S5_OCR_MAX_BLOCKS", "400"))
OCR_MAX_VERBATIM_CHARS = int(os.environ.get("NEXUS_S5_OCR_MAX_VERBATIM", "8000"))
OCR_MAX_LATEX_CHARS = int(os.environ.get("NEXUS_S5_OCR_MAX_LATEX", "8000"))
OCR_MAX_ALTERNATIVES = int(os.environ.get("NEXUS_S5_OCR_MAX_ALTERNATIVES", "12"))
OCR_MAX_NOTES_CHARS = int(os.environ.get("NEXUS_S5_OCR_MAX_NOTES", "2000"))

OPENROUTER_TIMEOUT_SECONDS = int(os.environ.get("OPENROUTER_TIMEOUT", "180"))
OPENROUTER_MAX_RETRIES = int(os.environ.get("OPENROUTER_MAX_RETRIES", "4"))
# Plafond de dépense par copie. Une boucle accidentelle coûte de l'argent réel ;
# au-delà, la campagne s'arrête et le dit.
OCR_MAX_COST_PER_COPY_USD = float(os.environ.get("OCR_MAX_COST_PER_COPY_USD", "3.00"))

# --------------------------------------------------------------- LaTeX
LATEX_ENGINE = os.environ.get("NEXUS_S5_LATEX_ENGINE", "pdflatex")
LATEX_TIMEOUT_SECONDS = int(os.environ.get("NEXUS_S5_LATEX_TIMEOUT", "180"))

# --------------------------------------------------------------- divers
# Identité de l'opérateur. L'application est mono-utilisateur et locale : elle n'a
# pas d'authentification, et ne peut donc pas prouver qui agit. Cette valeur est une
# **déclaration**, pas une identité authentifiée, et l'audit la présente comme telle.
OPERATOR_IDENTITY = (os.environ.get("NEXUS_S5_OPERATOR") or "poste-local").strip()[:96]
OPERATOR_ROLE = (os.environ.get("NEXUS_S5_OPERATOR_ROLE") or "enseignant").strip()[:32]

TIMEZONE = "Africa/Tunis"
SCORE_SCALE = 100          # les points sont stockés en centièmes entiers
SCORE_STEP = 5             # tout montant du barème est un multiple de 0,05 point


def ensure_runtime() -> None:
    """Crée les répertoires d'écriture. N'écrit rien d'autre."""
    for d in (RUNTIME_DIR, EXPORTS_DIR, REPORTS_DIR, BACKUPS_DIR, BUILD_DIR,
              SOURCE_COPIES_DIR, OCR_CACHE_DIR):
        d.mkdir(parents=True, exist_ok=True)
    SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    # Copies d'élèves, transcriptions, sauvegardes et secrets : réservés au
    # propriétaire. Sur un poste partagé, un mode par défaut laisserait ces données
    # lisibles par les autres comptes ; l'intégrité (hachage) ne dit rien de la
    # confidentialité.
    for d in (SECRETS_DIR, SOURCE_COPIES_DIR, OCR_CACHE_DIR, BACKUPS_DIR,
              EXPORTS_DIR, REPORTS_DIR):
        try:
            d.chmod(0o700)
        except OSError:
            pass


class Settings:
    """État mutable du processus : ce que la ligne de commande a décidé."""

    def __init__(self):
        self.readonly = False
        self.readonly_reason = ""
        self.allow_network = False
        self.host = DEFAULT_HOST
        self.port = DEFAULT_PORT
        self.pilot_mode = True          # tant que le premier cas réel n'est pas validé
        # « human » : l'enseignant a la copie papier sous les yeux ; aucune pièce
        # jointe n'est exigée, et c'est le mode historique. « digital » : la
        # correction s'appuie sur une copie numérisée, qui doit alors être
        # rattachée et vérifiée avant toute saisie.
        self.correction_mode = (os.environ.get("NEXUS_S5_CORRECTION_MODE")
                                or "human").strip().lower()
        self.data_mode = DATA_MODE if DATA_MODE in DATA_MODES else "REAL"
        self.tls_active = False        # posé par la ligne de commande
        self.tls_by_proxy = False

    @property
    def real_data(self) -> bool:
        return self.data_mode == "REAL"

    @property
    def auth_required(self) -> bool:
        """Des copies d'élèves réelles ne s'ouvrent pas sans s'authentifier.

        Y compris sur la boucle locale : tout processus du poste capable d'ouvrir un
        navigateur pourrait sinon les lire.
        """
        return self.real_data

    def set_readonly(self, reason: str) -> None:
        self.readonly = True
        self.readonly_reason = reason


settings = Settings()
