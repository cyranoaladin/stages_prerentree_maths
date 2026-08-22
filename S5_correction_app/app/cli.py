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
    mode = config.settings.data_mode
    password = os.environ.get("NEXUS_S5_PASSWORD", "")
    tls = bool(args.ssl_certfile and args.ssl_keyfile)
    config.settings.tls_active = tls
    config.settings.tls_by_proxy = bool(config.TRUSTED_PROXY_TLS)

    # Un mot de passe est exigé dans deux cas, et l'un ne remplace pas l'autre :
    #
    #  * mode REAL — aucune copie ne s'ouvre sans authentification, y compris sur la
    #    boucle locale : tout processus du poste sait ouvrir un navigateur ;
    #  * exposition réseau — quel que soit le mode déclaré. « S5_DATA_MODE » est une
    #    déclaration d'opérateur : une erreur de déclaration ne doit pas suffire à
    #    ouvrir un serveur sans authentification sur toutes les interfaces.
    if (mode == "REAL" or args.allow_network) and len(password) < 12:
        raison = ("S5_DATA_MODE=REAL" if mode == "REAL" else "--allow-network")
        print("REFUS : %s exige NEXUS_S5_PASSWORD, d'au moins 12 caractères.\n"
              "Aucun mot de passe par défaut n'est fourni. Pour travailler sur des "
              "fixtures\nen local sans authentification, déclarez explicitement "
              "S5_DATA_MODE=SYNTHETIC\net n'exposez pas le réseau." % raison,
              file=sys.stderr)
        return 2

    if args.allow_network:
        # HTTP Basic ne chiffre rien : sur un réseau, le mot de passe ET les copies
        # circuleraient en clair. On refuse plutôt que de donner le change.
        if mode == "REAL" and not tls and not config.TRUSTED_PROXY_TLS:
            print("REFUS : données réelles + réseau + HTTP en clair.\n"
                  "HTTP Basic n'apporte aucune confidentialité sur un transport en "
                  "clair : le mot de passe\net les copies d'élèves seraient "
                  "interceptables. Deux issues :\n"
                  "  --ssl-certfile CERT --ssl-keyfile CLE      (TLS direct)\n"
                  "  NEXUS_S5_TRUSTED_PROXY_TLS=1 + NEXUS_S5_TRUSTED_PROXY_HOSTS=…\n"
                  "                                             (TLS terminé par un "
                  "proxy déclaré)\n"
                  "Aucun certificat n'est généré automatiquement : un certificat non "
                  "maîtrisé\nne résout rien.", file=sys.stderr)
            return 2
        print("AVERTISSEMENT : l'application va écouter sur toutes les interfaces "
              "réseau.\nLes corrections et les bilans sont des données personnelles "
              "d'élèves.", file=sys.stderr)
        host = "0.0.0.0"          # noqa: S104 — choix explicite de l'opérateur
        config.settings.allow_network = True
    config.settings.host, config.settings.port = host, args.port
    print("%s %s" % (APP_NAME, APP_VERSION))
    print("  http://%s:%d" % ("127.0.0.1" if host == "127.0.0.1" else host, args.port))
    print("  base : %s" % config.DB_PATH)
    print("  pour arrêter : Ctrl+C")
    print("  mode de données : %s%s" % (mode, "" if mode == "REAL"
                                        else "  (fixtures — aucune donnée réelle)"))
    print("  transport : %s" % ("TLS direct" if tls else
                                "TLS par proxy déclaré" if config.TRUSTED_PROXY_TLS
                                else "clair (boucle locale uniquement)"))
    options = {}
    if tls:
        options = {"ssl_certfile": args.ssl_certfile, "ssl_keyfile": args.ssl_keyfile}
    uvicorn.run("app.main:app", host=host, port=args.port, log_level="info",
                reload=False, access_log=False, **options)
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
    serve.add_argument("--ssl-certfile", default=None,
                       help="certificat TLS ; exigé pour exposer des données réelles")
    serve.add_argument("--ssl-keyfile", default=None, help="clé privée TLS")
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
