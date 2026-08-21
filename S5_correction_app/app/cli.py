#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ligne de commande.

    python3 -m app.cli serve                 démarre sur 127.0.0.1:8765
    python3 -m app.cli serve --readonly      démarre sans autoriser la moindre écriture
    python3 -m app.cli check                 contrôle l'immutabilité et sort

L'application n'écoute que la boucle locale. ``--allow-network`` existe, mais il exige un
mot de passe fourni par variable d'environnement : il n'y a pas de valeur par défaut, et
il n'y en aura pas.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import APP_NAME, APP_VERSION, config          # noqa: E402


def _serve(args) -> int:
    import uvicorn
    if args.db:
        config.DB_PATH = Path(args.db)
    if args.readonly:
        config.settings.set_readonly("démarré avec --readonly : aucune écriture n'est acceptée.")
    host = config.DEFAULT_HOST
    if args.allow_network:
        password = os.environ.get("NEXUS_S5_PASSWORD", "")
        if len(password) < 12:
            print("REFUS : --allow-network exige NEXUS_S5_PASSWORD, d'au moins 12 caractères.\n"
                  "Aucun mot de passe par défaut n'est fourni, et l'application ne s'expose "
                  "pas sans authentification.", file=sys.stderr)
            return 2
        print("AVERTISSEMENT : l'application va écouter sur toutes les interfaces réseau.\n"
              "Les corrections et les bilans sont des données personnelles d'élèves.",
              file=sys.stderr)
        host = "0.0.0.0"          # noqa: S104 — choix explicite de l'opérateur
        config.settings.allow_network = True
    config.settings.host, config.settings.port = host, args.port
    print("%s %s" % (APP_NAME, APP_VERSION))
    print("  http://%s:%d" % ("127.0.0.1" if host == "127.0.0.1" else host, args.port))
    print("  base : %s" % config.DB_PATH)
    print("  pour arrêter : Ctrl+C")
    uvicorn.run("app.main:app", host=host, port=args.port, log_level="info",
                reload=False, access_log=False)
    return 0


def _check(args) -> int:
    from app.domain import immutability
    report = immutability.verify()
    summary = report.summary()
    for key, value in summary.items():
        print("%-32s %s" % (key, value))
    for changed in report.changed:
        print("  modifié : %s" % changed["path"])
    for missing in report.missing:
        print("  manquant : %s" % missing)
    return 0 if report.ok else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="nexus-s5-correction",
                                     description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command")

    serve = sub.add_parser("serve", help="démarre l'application web locale")
    serve.add_argument("--host", default=config.DEFAULT_HOST,
                       help="ignoré sans --allow-network : la boucle locale est le défaut")
    serve.add_argument("--port", type=int, default=config.DEFAULT_PORT)
    serve.add_argument("--db", help="chemin d'une autre base SQLite")
    serve.add_argument("--readonly", action="store_true")
    serve.add_argument("--allow-network", action="store_true",
                       help="expose l'application au réseau ; exige NEXUS_S5_PASSWORD")
    serve.set_defaults(func=_serve)

    check = sub.add_parser("check", help="contrôle l'immutabilité des documents distribués")
    check.set_defaults(func=_check)

    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
