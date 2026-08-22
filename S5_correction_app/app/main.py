# -*- coding: utf-8 -*-
"""Application FastAPI.

Au démarrage, trois choses se passent, dans cet ordre : la base est créée si elle
n'existe pas, le référentiel V3 est importé si la base est vide, et les soixante
empreintes des documents distribués sont recalculées. Si l'une d'elles a changé,
l'application démarre en lecture seule et l'affiche sur toutes les pages.
"""

import contextlib
import datetime as dt
import json

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import APP_NAME, APP_VERSION, config, database, latex_html
from .domain import correction as corr
from .domain import immutability, importer, points

templates = Jinja2Templates(directory=str(config.TEMPLATES_DIR))

STATE = {"immutability": None, "started_at": None, "drift": []}


def _fr_number(value):
    if value is None:
        return "—"
    if isinstance(value, (int,)):
        return str(value)
    return ("%.1f" % float(value)).replace(".", ",").replace(",0", "")


def _fr_datetime(value):
    if value is None:
        return "—"
    if value.tzinfo is None:
        value = value.replace(tzinfo=dt.timezone.utc)
    return value.astimezone().strftime("%d/%m/%Y à %H:%M")


templates.env.filters["points"] = points.format_fr
templates.env.filters["nombre"] = _fr_number
templates.env.filters["datetime_fr"] = _fr_datetime
templates.env.filters["fromjson"] = lambda s: json.loads(s or "[]")
# « enonce » ne s'applique qu'au contenu du référentiel interne : il rend les
# structures LaTeX documentaires (enumerate, item, textbf) après échappement
# intégral. Les saisies enseignant restent hors de son chemin.
templates.env.filters["enonce"] = latex_html.render_statement
# Variante texte, pour les attributs HTML : le rendu principal produit des
# balises, qui n'ont rien à faire dans un « title ».
templates.env.filters["enonce_texte"] = latex_html.render_plain
templates.env.globals["APP_NAME"] = APP_NAME
templates.env.globals["APP_VERSION"] = APP_VERSION
templates.env.globals["STATUS_LABELS"] = corr.STATUS_LABELS
templates.env.globals["ERROR_CODES"] = corr.ERROR_CODES


def bootstrap() -> dict:
    """Prépare la base et contrôle l'immutabilité. Ne fabrique aucune donnée."""
    import migrations
    config.ensure_runtime()
    fresh = not config.DB_PATH.exists()
    migrations.apply(database.engine(), config.DB_PATH, config.BACKUPS_DIR)
    report = immutability.verify()
    STATE["immutability"] = report
    STATE["started_at"] = dt.datetime.now().astimezone()
    if not report.ok:
        config.settings.set_readonly(
            "IMMUTABILITY FAILURE — %d document(s) distribué(s) ne correspondent plus à leur "
            "empreinte. La correction est suspendue." % (len(report.changed) + len(report.missing)))
    if fresh and report.ok:
        with database.session_scope() as session:
            importer.run_import(session)
    with database.session_scope() as session:
        STATE["drift"] = importer.check_sources_unchanged(session)
        # Une campagne de lecture restée « en cours » n'a pas survécu au processus
        # précédent : elle est marquée interrompue, donc reprenable, et libère
        # l'index qui interdit deux campagnes simultanées.
        from .domain import transcription
        STATE["interrupted_runs"] = transcription.resume_interrupted(session)
    return {"fresh": fresh, "immutability": report.summary()}


@contextlib.asynccontextmanager
async def _cycle_de_vie(app: FastAPI):
    """Démarrage et arrêt de l'application.

    ``@app.on_event`` est déprécié par FastAPI et disparaîtra : le seul avertissement
    de dépréciation provenant de notre code venait de là. Le comportement est
    identique — ``bootstrap()`` au démarrage, rien de particulier à l'arrêt.
    """
    bootstrap()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title=APP_NAME, version=APP_VERSION, docs_url=None, redoc_url=None,
                  lifespan=_cycle_de_vie)
    app.mount("/static", StaticFiles(directory=str(config.STATIC_DIR)), name="static")

    from .routes import admin, analysis, correction as correction_routes, dashboard
    from .routes import documents, longitudinal as longitudinal_routes
    from .routes import reports as report_routes
    from .routes import source_copy as source_copy_routes
    app.include_router(dashboard.router)
    app.include_router(correction_routes.router)
    app.include_router(analysis.router)
    app.include_router(report_routes.router)
    app.include_router(longitudinal_routes.router)
    app.include_router(source_copy_routes.router)
    app.include_router(documents.router)
    app.include_router(admin.router)

    # Chemins dont la réponse ne doit jamais être conservée par un navigateur, un
    # cache intermédiaire ou un mandataire : ce sont des copies d'élèves.
    SENSIBLE = ("/eleve/", "/rapport/", "/document/", "/admin")

    @app.middleware("http")
    async def _context(request: Request, call_next):
        from .security import (check_basic_auth, check_token, issue_token,
                               same_origin, transport_is_secure)
        request.state.readonly = config.settings.readonly

        # 1. Transport. Des copies d'élèves ne transitent pas en clair hors de la
        #    boucle locale. « X-Forwarded-Proto » n'est cru que d'un proxy déclaré.
        if config.settings.real_data and not transport_is_secure(request):
            return JSONResponse(
                {"detail": "Refus : en mode REAL, les copies d'élèves ne transitent "
                           "pas en clair hors de la boucle locale. Configurez TLS, "
                           "ou déclarez le proxy qui le termine."},
                status_code=421)

        # 2. Authentification. En mode REAL, elle est exigée même sur la boucle
        #    locale : tout processus du poste capable d'ouvrir un navigateur pourrait
        #    sinon lire les copies.
        if config.settings.auth_required:
            if not check_basic_auth(request.headers.get("authorization", "")):
                return JSONResponse(
                    {"detail": "Authentification requise : ce poste manipule des "
                               "copies d'élèves réelles."},
                    status_code=401,
                    headers={"WWW-Authenticate": 'Basic realm="Nexus S5"'})

        # 3. CSRF. Deux barrières indépendantes : un jeton signé, lié à la session du
        #    processus, et un contrôle d'origine. Un site tiers ne peut ni lire le
        #    cookie du jeton, ni falsifier « Origin ».
        if request.method not in ("GET", "HEAD", "OPTIONS"):
            jeton = (request.headers.get("x-csrf-token")
                     or request.cookies.get("nexus_csrf", ""))
            if not check_token(jeton, scope="csrf"):
                return JSONResponse(
                    {"detail": "Requête refusée : jeton anti-CSRF absent ou invalide."},
                    status_code=403)
            origine_sure = same_origin(request.headers.get("origin"),
                                       request.headers.get("referer"),
                                       request.headers.get("host", ""))
            if not origine_sure:
                return JSONResponse(
                    {"detail": "Requête refusée : origine non reconnue."},
                    status_code=403)

        response = await call_next(request)

        # Le jeton anti-CSRF accompagne toute page : il est lisible par le script de
        # l'application (il doit l'être pour être renvoyé en en-tête) mais reste
        # inaccessible à une autre origine, et « Secure » dès que le transport l'est.
        if request.method in ("GET", "HEAD") and "nexus_csrf" not in request.cookies:
            response.set_cookie(
                "nexus_csrf", issue_token("csrf"), samesite="strict",
                secure=bool(config.settings.tls_active or config.settings.tls_by_proxy),
                httponly=False, max_age=12 * 3600, path="/")

        # 3. Rien de sensible ne doit rester dans un cache.
        if request.url.path.startswith(SENSIBLE):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
            response.headers["Pragma"] = "no-cache"
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        # Tout est servi localement : aucune origine distante n'a à être jointe, et
        # aucun cadre étranger n'a à nous inclure.
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data: blob:; style-src 'self' "
            "'unsafe-inline'; script-src 'self'; font-src 'self'; connect-src 'self'; "
            "object-src 'none'; base-uri 'none'; frame-ancestors 'self'; "
            "form-action 'self'")
        return response

    def _wants_json(request: Request) -> bool:
        """Une requête de l'interface attend du JSON ; un lien de navigation attend une page."""
        headers = request.headers
        return bool(headers.get("HX-Request") or headers.get("X-Requested-With")
                    or headers.get("content-type", "").startswith("application/json")
                    or "application/json" in headers.get("accept", ""))

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(request: Request, exc: StarletteHTTPException):
        if _wants_json(request):
            return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
        return templates.TemplateResponse(
            request, "error.html",
            {"code": exc.status_code, "detail": exc.detail,
             "readonly": config.settings.readonly,
             "readonly_reason": config.settings.readonly_reason,
             "drift": [], "immutability": None, "pilot_mode": config.settings.pilot_mode},
            status_code=exc.status_code)

    return app


app = create_app()
