#!/usr/bin/env python3
"""Lancement d'un serveur HTTP local pour la tablette enseignant avec affichage de l'IP LAN."""

import sys
import socket
import http.server
import socketserver
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def run_server(mode="public", port=8000):
    directory = ROOT / "dist" / ("site-private" if mode == "private" else "site-public")
    if not directory.exists():
        directory = ROOT

    ip = get_lan_ip()

    print("=" * 60)
    if mode == "private":
        print("🔒 SERVEUR TABLETTE PRIVÉ NEXUS RÉUSSITE DÉMARRÉ")
        print("⚠️  AVERTISSEMENT DE SÉCURITÉ :")
        print("   Ce serveur diffuse les dossiers nominatifs et corrigés sur le réseau local (LAN).")
    else:
        print("🌐 SERVEUR TABLETTE PUBLIC NEXUS RÉUSSITE DÉMARRÉ")
        print("   Ce serveur diffuse la version publique (sans PII ni corrigés).")

    print("-" * 60)
    print(f"📍 Accès tablette sur le Wi-Fi local : http://{ip}:{port}")
    print(f"📍 Accès local sur la machine     : http://localhost:{port}")
    print(f"📂 Dossier servi                  : {directory}")
    print("🛑 Appuyez sur CTRL+C pour arrêter le serveur.")
    print("=" * 60)

    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServeur arrêté avec succès.")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "public"
    run_server(mode=mode)
