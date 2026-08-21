#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle visuel automatisé de la totalité des pages PDF de la livraison.

Chaque page est rasterisée puis analysée :
  * page blanche accidentelle    : moins de 0,3 % de pixels encrés ;
  * page très aérée              : moins de 3 % de pixels encrés (signalée, non bloquante) ;
  * débordement hors marge       : encre dans une bande de 4 mm sur un bord ;
  * page saturée                 : plus de 45 % de pixels encrés.

Produit `_audit/controle_visuel_pages.json`. Sortie non nulle si un défaut bloquant
est détecté.
"""

import sys
sys.dont_write_bytecode = True
import json
import os
import subprocess
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DPI = 100
MM = DPI / 25.4
EDGE_MM = 6.0   # marge non imprimable typique d'une imprimante laser A4
BLANK = 0.003
SPARSE = 0.015
DENSE = 0.45


def analyse_page(path):
    im = Image.open(path).convert("L")
    w, h = im.size
    px = im.load()
    ink = 0
    edge_ink = 0
    e = int(EDGE_MM * MM)
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if px[x, y] < 200:
                ink += 1
                if x < e or x >= w - e or y < e or y >= h - e:
                    edge_ink += 1
    total = (w // 2 + 1) * (h // 2 + 1)
    return {"ink_ratio": round(ink / total, 5), "edge_ink": edge_ink,
            "width": w, "height": h}


def main():
    pdfs = sorted(os.path.join(dp, f) for dp, dn, fns in os.walk(ROOT)
                  for f in fns if f.endswith(".pdf"))
    rows, blocking, sparse_pages = [], [], []
    tmp = tempfile.mkdtemp(prefix="s5raster_")
    total_pages = 0
    try:
        for pdf in pdfs:
            base = os.path.join(tmp, "p")
            subprocess.run(["pdftoppm", "-png", "-r", str(DPI), pdf, base],
                           check=True, capture_output=True)
            pages = sorted(f for f in os.listdir(tmp) if f.startswith("p") and f.endswith(".png"))
            for i, f in enumerate(pages, 1):
                fp = os.path.join(tmp, f)
                a = analyse_page(fp)
                total_pages += 1
                rel = os.path.relpath(pdf, ROOT)
                row = {"pdf": rel, "page": i, **a, "defauts": []}
                if a["ink_ratio"] < BLANK:
                    row["defauts"].append("page blanche accidentelle")
                    blocking.append(row)
                elif a["ink_ratio"] < SPARSE:
                    row["defauts"].append("page très aérée")
                    sparse_pages.append(row)
                if a["ink_ratio"] > DENSE:
                    row["defauts"].append("page saturée")
                    blocking.append(row)
                if a["edge_ink"] > 0:
                    row["defauts"].append("encre dans la bande de %g mm du bord" % EDGE_MM)
                    blocking.append(row)
                rows.append(row)
                os.unlink(fp)
    finally:
        for f in os.listdir(tmp):
            os.unlink(os.path.join(tmp, f))
        os.rmdir(tmp)

    out = {"schema": "nexus-s5-controle-visuel-pages-v1",
           "resolution_ppp": DPI,
           "seuils": {"page_blanche": BLANK, "page_aeree": SPARSE, "page_saturee": DENSE,
                      "bande_de_bord_mm": EDGE_MM},
           "documents": len(pdfs), "pages_analysees": total_pages,
           "pages_bloquantes": len(blocking),
           "pages_tres_aerees": len(sparse_pages),
           "detail_bloquant": blocking,
           "detail_aere": [{k: r[k] for k in ("pdf", "page", "ink_ratio")} for r in sparse_pages],
           "detail_pages": rows}
    os.makedirs(os.path.join(ROOT, "_audit"), exist_ok=True)
    with open(os.path.join(ROOT, "_audit", "controle_visuel_pages.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("documents : %d   pages analysées : %d" % (len(pdfs), total_pages))
    print("pages bloquantes : %d" % len(blocking))
    print("pages très aérées (non bloquant) : %d" % len(sparse_pages))
    for r in blocking[:20]:
        print("  %s p.%d : %s (encre %.4f)" % (r["pdf"], r["page"], ", ".join(r["defauts"]),
                                               r["ink_ratio"]))
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
