# -*- coding: utf-8 -*-
"""Application FastAPI.

Au démarrage, trois choses se passent, dans cet ordre : la base est créée si elle
n'existe pas, le référentiel V3 est importé si la base est vide, et les soixante
empreintes des documents distribués sont recalculées. Si l'une d'elles a changé,
l'application démarre en lecture seule et l'affiche sur toutes les pages.
"""

import datetime as dt
import json
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import APP_NAME, APP_VERSION, config, database
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
    return {"fresh": fresh, "immutability": report.summary()}


def create_app() -> FastAPI:
    app = FastAPI(title=APP_NAME, version=APP_VERSION, docs_url=None, redoc_url=None)
    app.mount("/static", StaticFiles(directory=str(config.STATIC_DIR)), name="static")

    from .routes import admin, analysis, correction as correction_routes, dashboard
    from .routes import documents, reports as report_routes
    app.include_router(dashboard.router)
    app.include_router(correction_routes.router)
    app.include_router(analysis.router)
    app.include_router(report_routes.router)
    app.include_router(documents.router)
    app.include_router(admin.router)

    @app.on_event("startup")
    def _startup():
        bootstrap()

    @app.middleware("http")
    async def _context(request: Request, call_next):
        request.state.readonly = config.settings.readonly
        return await call_next(request)

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
