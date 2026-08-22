#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Catalogue OpenRouter : quels modèles peuvent réellement lire nos copies.

Le catalogue évolue. Figer un modèle dans le code condamnerait l'application à
vieillir avec lui ; cet outil interroge le catalogue **du jour** et rend la liste des
candidats qui satisfont nos contraintes techniques :

* entrée image — sans quoi il ne voit pas la page ;
* sorties structurées — sans quoi la transcription n'est pas exploitable.

Ce que l'outil ne fait pas, et ne peut pas faire : dire lequel lit le mieux une
écriture manuscrite. Cela se mesure, avec ``tools/ocr_benchmark.py``, sur de vraies
pages manuscrites et une transcription humaine de référence.

    python3 tools/openrouter_models.py                 # candidats, du moins cher au plus cher
    python3 tools/openrouter_models.py --contient qwen # filtre sur l'identifiant
    python3 tools/openrouter_models.py --json          # sortie machine

L'endpoint du catalogue est public : aucune clé n'est nécessaire, et aucune n'est lue.
La compatibilité ZDR, elle, n'est pas exposée par le catalogue : elle est appliquée
par OpenRouter au moment du routage. Un modèle listé ici peut donc échouer à
l'exécution faute d'endpoint conforme — et c'est le comportement voulu : l'appel
échoue plutôt que d'être rerouté vers un fournisseur qui conserverait les données.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config                                     # noqa: E402


def fetch(base_url=None, timeout=30) -> list:
    import httpx
    url = "%s/models" % (base_url or config.OPENROUTER_BASE_URL).rstrip("/")
    with httpx.Client(timeout=timeout) as client:
        response = client.get(url)
    response.raise_for_status()
    return response.json().get("data", [])


def candidates(models) -> list:
    out = []
    for model in models:
        architecture = model.get("architecture") or {}
        entrees = architecture.get("input_modalities") or []
        parametres = model.get("supported_parameters") or []
        if "image" not in entrees or "structured_outputs" not in parametres:
            continue
        pricing = model.get("pricing") or {}

        def prix(cle):
            try:
                valeur = float(pricing.get(cle) or 0)
            except (TypeError, ValueError):
                return 0.0
            # « openrouter/auto » annonce des prix sentinelles négatifs.
            return valeur if valeur >= 0 else None

        out.append({
            "id": model.get("id"),
            "nom": model.get("name"),
            "contexte": model.get("context_length"),
            "prompt_usd_par_mtok": (prix("prompt") or 0) * 1e6,
            "completion_usd_par_mtok": (prix("completion") or 0) * 1e6,
            "image_usd_par_millier": (prix("image") or 0) * 1000,
            "raisonnement": bool(model.get("reasoning")),
        })
    out.sort(key=lambda m: (m["prompt_usd_par_mtok"], m["id"]))
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--contient", default=None,
                        help="ne garder que les identifiants contenant ce fragment")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--limite", type=int, default=40)
    args = parser.parse_args(argv)

    try:
        modeles = fetch()
    except Exception as exc:
        print("catalogue inaccessible : %s" % type(exc).__name__, file=sys.stderr)
        return 1

    liste = candidates(modeles)
    if args.contient:
        fragment = args.contient.lower()
        liste = [m for m in liste if fragment in (m["id"] or "").lower()]

    if args.json:
        print(json.dumps(liste, ensure_ascii=False, indent=2))
        return 0

    print("%d modèle(s) au catalogue, %d acceptent image + sorties structurées."
          % (len(modeles), len(liste)))
    print()
    print("Réglages actuels de l'application :")
    print("  PRIMARY  %s" % config.OCR_MODEL_PRIMARY)
    print("  VERIFY   %s" % config.OCR_MODEL_VERIFY)
    print("  BASELINE %s" % config.OCR_MODEL_BASELINE)
    print()
    print("%-52s %12s %12s %10s" % ("identifiant", "prompt $/Mt", "sortie $/Mt",
                                    "image $/k"))
    for modele in liste[:args.limite]:
        print("%-52s %12.3f %12.3f %10.4f"
              % (modele["id"], modele["prompt_usd_par_mtok"],
                 modele["completion_usd_par_mtok"], modele["image_usd_par_millier"]))
    if len(liste) > args.limite:
        print("… %d autres. Utilisez --limite ou --contient."
              % (len(liste) - args.limite))
    print()
    print("Le catalogue n'indique pas la compatibilité ZDR : elle est appliquée au "
          "routage.\nUn modèle listé peut donc échouer à l'exécution — l'appel est "
          "alors refusé,\njamais rerouté vers un fournisseur qui conserverait les "
          "données.")
    print("La qualité de lecture manuscrite ne se déduit pas de ce tableau : "
          "mesurez-la\navec tools/ocr_benchmark.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
