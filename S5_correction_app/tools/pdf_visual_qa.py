#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit visuel des PDF de bilan : rastérisation, mesures, planches contact.

Un PDF qui compile n'est pas un PDF correct. Ce module ouvre réellement chaque
page, la rastérise, et mesure ce qu'un œil vérifierait : le format du papier, les
marges d'encre, la densité, les blancs injustifiés, le texte qui déborde.

Ce qu'il **ne fait pas** : juger l'esthétique. Aucun script ne dit si une page est
belle ou si une hiérarchie se lit bien. Il produit des mesures et des planches
contact ; le jugement reste humain, et le rapport final le dit.

Dépendances : ``pdftoppm`` et ``pdfinfo`` (poppler), Pillow. Toutes locales.
"""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# A4 en points PostScript, à la tolérance d'arrondi près.
A4_POINTS = (595.276, 841.89)
TOLERANCE_POINTS = 2.0

# Seuils. Ils ne condamnent rien : ils désignent les pages à regarder.
#
# Deux mesures distinctes, parce qu'elles ne disent pas la même chose :
#   « remplissage »  la hauteur réellement occupée par du contenu. C'est ce qui
#                    fait qu'une page paraît vide ou pleine ;
#   « encre »        la proportion de pixels encrés. Une page de texte courant en
#                    contient 5 à 12 % ; au-delà de 22 % elle est dense.
#
# Confondre les deux conduit à signaler toutes les pages comme creuses, ce qui
# revient à n'en signaler aucune.
REMPLISSAGE_FAIBLE = 0.45      # moins de la moitié de la hauteur occupée
DENSITE_FORTE = 0.22           # page saturée de texte
# Une page finale peu remplie est une page de clôture, pas un défaut : le
# contrôle de page creuse épargne donc la dernière page de chaque document.

# Marges d'encre : rien de critique ne doit approcher le bord.
MARGE_CRITIQUE_MM = 8.0
MARGE_CONFORTABLE_MM = 12.0
MM_PAR_POUCE = 25.4


def _executer(argv, **kwargs):
    return subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", shell=False, **kwargs)


def sha256(chemin) -> str:
    h = hashlib.sha256()
    with open(str(chemin), "rb") as f:
        for bloc in iter(lambda: f.read(1 << 16), b""):
            h.update(bloc)
    return h.hexdigest()


def infos_pdf(chemin) -> dict:
    """Format, pagination et métadonnées, lus par pdfinfo."""
    acheve = _executer(["pdfinfo", str(chemin)])
    donnees = {}
    for ligne in (acheve.stdout or "").splitlines():
        if ":" in ligne:
            cle, valeur = ligne.split(":", 1)
            donnees[cle.strip()] = valeur.strip()
    taille = donnees.get("Page size", "")
    trouve = re.match(r"([\d.]+) x ([\d.]+)", taille)
    largeur, hauteur = (float(trouve.group(1)), float(trouve.group(2))) if trouve \
        else (0.0, 0.0)
    return {
        "pages": int(donnees.get("Pages", 0) or 0),
        "width_pt": largeur, "height_pt": hauteur,
        "page_size": taille,
        "is_a4": (abs(largeur - A4_POINTS[0]) <= TOLERANCE_POINTS
                  and abs(hauteur - A4_POINTS[1]) <= TOLERANCE_POINTS),
        "title": donnees.get("Title", ""),
        "author": donnees.get("Author", ""),
        "subject": donnees.get("Subject", ""),
        "producer": donnees.get("Producer", ""),
        "creator": donnees.get("Creator", ""),
        "file_size": Path(chemin).stat().st_size,
    }


def texte_pdf(chemin) -> str:
    acheve = _executer(["pdftotext", "-layout", str(chemin), "-"])
    return acheve.stdout or ""


def rasteriser(chemin, destination, dpi=150, gris=False) -> list:
    """Produit une image par page. Retourne les chemins, dans l'ordre."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    prefixe = destination / Path(chemin).stem
    argv = ["pdftoppm", "-png", "-r", str(dpi)]
    if gris:
        argv.append("-gray")
    argv += [str(chemin), str(prefixe)]
    acheve = _executer(argv)
    if acheve.returncode != 0:
        return []
    return sorted(destination.glob("%s-*.png" % Path(chemin).stem))


def mesurer_page(image_path) -> dict:
    """Densité d'encre, marges occupées, grand blanc en pied de page.

    On travaille sur le seuil d'encre plutôt que sur la moyenne : un fond très clair
    ne doit pas compter comme du contenu, et un texte fin ne doit pas disparaître.
    """
    from PIL import Image
    image = Image.open(image_path).convert("L")
    largeur, hauteur = image.size
    pixels = image.load()

    # Colonnes et lignes contenant de l'encre (seuil à 200/255).
    lignes_encrees, colonnes_encrees = [], set()
    total_encre = 0
    pas = max(1, largeur // 400)          # échantillonnage horizontal, suffisant
    for y in range(hauteur):
        encre_ligne = 0
        for x in range(0, largeur, pas):
            if pixels[x, y] < 200:
                encre_ligne += 1
                colonnes_encrees.add(x)
        if encre_ligne:
            lignes_encrees.append(y)
            total_encre += encre_ligne

    if not lignes_encrees:
        return {"blank": True, "ink_ratio": 0.0, "fill_ratio": 0.0, "top_mm": None,
                "bottom_mm": None, "left_mm": None, "right_mm": None,
                "tail_white_ratio": 1.0, "width_px": largeur, "height_px": hauteur}

    dpi_effectif = largeur / (A4_POINTS[0] / 72.0)
    par_mm = dpi_effectif / MM_PAR_POUCE

    haut, bas = lignes_encrees[0], lignes_encrees[-1]
    gauche, droite = min(colonnes_encrees), max(colonnes_encrees)
    surface_utile = (largeur / pas) * hauteur

    # Le remplissage se mesure DANS le bloc de texte, en écartant les bandes de
    # garniture : l'en-tête et le pied de page courants sont présents sur toutes
    # les pages et donneraient un remplissage de 93 % même sur une page vide.
    # Sans cette précaution, la mesure ne détecte jamais une page creuse.
    bande_haute = 24.0 * par_mm          # marge supérieure + en-tête
    bande_basse = hauteur - 18.0 * par_mm
    dans_bloc = [y for y in lignes_encrees if bande_haute <= y <= bande_basse]
    hauteur_bloc = max(1.0, bande_basse - bande_haute)
    remplissage = ((max(dans_bloc) - min(dans_bloc)) / hauteur_bloc) if dans_bloc else 0.0

    return {
        "blank": False,
        "ink_ratio": round(total_encre / surface_utile, 4),
        "fill_ratio": round(remplissage, 3),
        "content_top_mm": round(min(dans_bloc) / par_mm, 1) if dans_bloc else None,
        "content_bottom_mm": round((hauteur - max(dans_bloc)) / par_mm, 1)
        if dans_bloc else None,
        "top_mm": round(haut / par_mm, 1),
        "bottom_mm": round((hauteur - bas) / par_mm, 1),
        "left_mm": round(gauche / par_mm, 1),
        "right_mm": round((largeur - droite) / par_mm, 1),
        "tail_white_ratio": round(
            (bande_basse - max(dans_bloc)) / hauteur_bloc, 3) if dans_bloc else 1.0,
        "width_px": largeur, "height_px": hauteur,
    }


def planche_contact(images, destination, colonnes=None, largeur_vignette=340):
    """Assemble les pages d'un document en une planche unique."""
    from PIL import Image
    if not images:
        return None
    colonnes = colonnes or min(len(images), 5)
    vignettes = []
    for chemin in images:
        image = Image.open(chemin)
        ratio = largeur_vignette / image.width
        vignettes.append(image.resize((largeur_vignette,
                                       int(image.height * ratio)), Image.LANCZOS))
    lignes = (len(vignettes) + colonnes - 1) // colonnes
    hauteur_vignette = max(v.height for v in vignettes)
    planche = Image.new("RGB", (colonnes * largeur_vignette + (colonnes + 1) * 8,
                                lignes * hauteur_vignette + (lignes + 1) * 8), "white")
    for index, vignette in enumerate(vignettes):
        colonne, ligne = index % colonnes, index // colonnes
        planche.paste(vignette, (8 + colonne * (largeur_vignette + 8),
                                 8 + ligne * (hauteur_vignette + 8)))
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    planche.save(destination)
    return str(destination)


def auditer(chemin_pdf, dossier_travail, dpi=150, contact=True) -> dict:
    """Audit complet d'un PDF : format, pages, densité, marges, planche."""
    chemin_pdf = Path(chemin_pdf)
    infos = infos_pdf(chemin_pdf)
    infos["document"] = chemin_pdf.name
    infos["sha256"] = sha256(chemin_pdf)

    dossier_pages = Path(dossier_travail) / "pages" / chemin_pdf.stem
    images = rasteriser(chemin_pdf, dossier_pages, dpi=dpi)
    infos["rasterized_pages"] = len(images)

    mesures, alertes = [], []
    for numero, image in enumerate(images, start=1):
        mesure = mesurer_page(image)
        mesure["page"] = numero
        mesures.append(mesure)

        if mesure["blank"]:
            alertes.append({"page": numero, "code": "page_blanche",
                            "severite": "P0",
                            "detail": "page sans aucune encre"})
            continue
        for cote in ("top", "bottom", "left", "right"):
            valeur = mesure["%s_mm" % cote]
            if valeur is not None and valeur < MARGE_CRITIQUE_MM:
                alertes.append({
                    "page": numero, "code": "marge_critique", "severite": "P1",
                    "detail": "encre à %.1f mm du bord %s (seuil %.0f mm)"
                              % (valeur, cote, MARGE_CRITIQUE_MM)})
        if mesure["ink_ratio"] > DENSITE_FORTE:
            alertes.append({"page": numero, "code": "page_saturee", "severite": "P2",
                            "detail": "densité d'encre %.0f %%"
                                      % (mesure["ink_ratio"] * 100)})
        # Le blanc de pied n'est pas mesuré séparément : sur un document à structure
        # éditoriale fixe, chaque saut de page volontaire en produit un, et le
        # signaler reviendrait à signaler la structure elle-même. Ce qui compte est
        # qu'une page ne soit pas creuse — c'est le contrôle suivant.
        if mesure.get("fill_ratio", 1.0) < REMPLISSAGE_FAIBLE and numero < len(images):
            alertes.append({"page": numero, "code": "page_creuse", "severite": "P2",
                            "detail": "seulement %.0f %% de la hauteur occupée, sur une "
                                      "page non finale"
                                      % (mesure["fill_ratio"] * 100)})

    if not infos["is_a4"]:
        alertes.append({"page": None, "code": "format_non_a4", "severite": "P0",
                        "detail": "format %s" % infos["page_size"]})

    texte = texte_pdf(chemin_pdf)
    infos["text_extractable"] = len(texte.strip()) > 200
    if not infos["text_extractable"]:
        alertes.append({"page": None, "code": "texte_non_selectionnable",
                        "severite": "P1",
                        "detail": "moins de 200 caractères extractibles"})

    if contact and images:
        infos["contact_sheet"] = planche_contact(
            images, Path(dossier_travail) / "contact" / ("%s.png" % chemin_pdf.stem))

    infos["pages_measured"] = mesures
    infos["alerts"] = alertes
    infos["visual_status"] = "OK" if not [a for a in alertes
                                          if a["severite"] in ("P0", "P1")] else "REVOIR"
    return infos


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dossier", help="répertoire contenant les PDF à auditer")
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--travail", default=None, help="répertoire de travail")
    ap.add_argument("--json", default=None, help="fichier de sortie JSON")
    ap.add_argument("--no-contact", action="store_true")
    args = ap.parse_args(argv)

    for outil in ("pdfinfo", "pdftoppm", "pdftotext"):
        if not shutil.which(outil):
            print("outil manquant : %s" % outil, file=sys.stderr)
            return 2

    travail = Path(args.travail or tempfile.mkdtemp(prefix="nexus_pdfqa_"))
    pdfs = sorted(Path(args.dossier).glob("*.pdf"))
    if not pdfs:
        print("aucun PDF dans %s" % args.dossier, file=sys.stderr)
        return 2

    rapports = [auditer(p, travail, args.dpi, not args.no_contact) for p in pdfs]
    alertes = [dict(a, document=r["document"]) for r in rapports for a in r["alerts"]]
    par_severite = {}
    for alerte in alertes:
        par_severite[alerte["severite"]] = par_severite.get(alerte["severite"], 0) + 1

    print("%-52s %5s %6s %8s %s" % ("document", "pages", "A4", "densité", "état"))
    for rapport in rapports:
        densites = [m["ink_ratio"] for m in rapport["pages_measured"] if not m["blank"]]
        print("%-52s %5d %6s %7.0f%% %s"
              % (rapport["document"][:52], rapport["pages"],
                 "oui" if rapport["is_a4"] else "NON",
                 100 * (sum(densites) / len(densites) if densites else 0),
                 rapport["visual_status"]))
    print()
    print("documents %d · pages %d · alertes %s"
          % (len(rapports), sum(r["pages"] for r in rapports),
             par_severite or "aucune"))
    print("travail : %s" % travail)

    if args.json:
        Path(args.json).write_text(
            json.dumps({"documents": rapports, "alerts": alertes,
                        "by_severity": par_severite, "workdir": str(travail)},
                       ensure_ascii=False, indent=2), encoding="utf-8")
    bloquantes = [a for a in alertes if a["severite"] in ("P0", "P1")]
    return 0 if not bloquantes else 1


if __name__ == "__main__":
    sys.exit(main())
