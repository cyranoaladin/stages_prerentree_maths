#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Porte de qualité des bilans PDF.

Elle échoue sur ce qu'une machine peut établir sans se tromper : un format qui
n'est pas A4, une page blanche, un débordement dans la marge, une pagination hors
limites, du LaTeX brut visible, un identifiant technique dans un document destiné
aux familles, un chemin local ou un marqueur de test oublié.

Elle **ne dit rien** de l'esthétique, de la hiérarchie visuelle ou de la justesse
d'une formulation. Ces jugements relèvent d'une relecture humaine, et le rapport
de QA le dit explicitement. Une porte verte ne signifie pas « le document est
bon » : elle signifie « aucun des défauts objectivables n'est présent ».
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import pdf_visual_qa as visual                      # noqa: E402

# Pagination attendue par type de document.
#
# Le bilan parents vise quatre a cinq pages. Il en fait six : le plan des quatre
# semaines occupe une page entiere des que l'eleve cumule plusieurs priorites, et
# c'est la partie que la famille utilisera. La sixieme page porte la cloture —
# priorites, conseil, limites. L'ecart a la cible est assume et documente dans
# FINAL_REPORT_PDF_QA.md ; au-dela de six pages, il devient un defaut.
PAGES_ATTENDUES = {
    "PARENTS": (4, 6),
    "ELEVE": (1, 2),
    "ENSEIGNANT": (2, 8),
}

# Cible editoriale, distincte de la limite : un depassement de la cible sans
# depassement de la limite est signale en P3, pour rester visible sans bloquer.
CIBLE_PAGES = {"PARENTS": (4, 5)}

# Séquences qui ne doivent jamais atteindre un lecteur.
LATEX_BRUT = (r"\begin{", r"\end{", r"\item ", r"\textbf{", r"\code{", r"\hline",
              r"\VAR{", r"\BLOCK{")

# Identifiants techniques, interdits dans les documents parents et élève.
RE_SKILL_ID = re.compile(r"\b(?:M\d?[A-Z]{1,4}\d?_[A-Z0-9_]{2,}|NSI\d_[A-Z0-9_]{2,})\b")
RE_CRITERION_ID = re.compile(r"\b\d?[A-Z]{1,4}_[A-Z_]+_[A-Z]\d+_c\d+(?:_v\d+)?\b")
RE_CLE_TECHNIQUE = re.compile(
    r"\b(?:n_minus_1|bridge_n|curriculum_scope|mastery_delta|evidence_strength|"
    r"scoring_id|P1|P2|P3)\b")

# Termes proscrits, quel que soit le document destiné aux familles.
TERMES_INTERDITS = ("lacune", "définitivement acquis", "élève faible",
                    "n'a pas le niveau", "est indispensable")

RE_PROGRESSION = re.compile(
    r"progress\w*[^.]{0,40}?[+-]?\s*\d+([.,]\d+)?\s*(?:%|points?|niveaux?)",
    re.IGNORECASE)

# Fuites d'environnement.
RE_URI_LOCAL = re.compile(r"file://|/home/[a-z]|/Users/[A-Za-z]|C:\\\\Users")

# Marqueurs de fixture, tolérés dans un corpus de QA, interdits ailleurs.
MARQUEURS_TEST = ("TEST_INES", "SYNTHETIQUE", "FIXTURE", "eleve-synthetique")


def _audience(nom_fichier: str) -> str:
    for prefixe in ("PARENTS", "ELEVE", "ENSEIGNANT"):
        if nom_fichier.upper().startswith(prefixe):
            return prefixe
    return "INCONNU"


def controler(chemin_pdf, dossier_travail, autoriser_marqueurs=False) -> dict:
    """Contrôle un PDF. Retourne son relevé et la liste de ses défauts."""
    audit = visual.auditer(chemin_pdf, dossier_travail, dpi=110, contact=False)
    audience = _audience(Path(chemin_pdf).name)
    texte = visual.texte_pdf(chemin_pdf)
    defauts = []

    def signaler(severite, code, detail):
        defauts.append({"severite": severite, "code": code, "detail": detail,
                        "document": Path(chemin_pdf).name})

    if not audit["is_a4"]:
        signaler("P0", "format_papier", "format %s au lieu de A4" % audit["page_size"])
    if audit["pages"] == 0:
        signaler("P0", "document_vide", "aucune page")

    for mesure in audit["pages_measured"]:
        if mesure["blank"]:
            signaler("P0", "page_blanche", "page %d sans aucun contenu" % mesure["page"])

    for alerte in audit["alerts"]:
        if alerte["code"] == "marge_critique":
            signaler("P1", "debordement",
                     "page %s : %s" % (alerte["page"], alerte["detail"]))

    bornes = PAGES_ATTENDUES.get(audience)
    if bornes and not (bornes[0] <= audit["pages"] <= bornes[1]):
        severite = "P1" if audit["pages"] > bornes[1] else "P2"
        signaler(severite, "pagination",
                 "%d pages, hors de l'intervalle admis %d–%d"
                 % (audit["pages"], bornes[0], bornes[1]))
    cible = CIBLE_PAGES.get(audience)
    if cible and bornes and (bornes[0] <= audit["pages"] <= bornes[1]) \
            and not (cible[0] <= audit["pages"] <= cible[1]):
        signaler("P3", "pagination_cible",
                 "%d pages, au-delà de la cible éditoriale %d–%d ; écart documenté"
                 % (audit["pages"], cible[0], cible[1]))

    for sequence in LATEX_BRUT:
        if sequence in texte:
            signaler("P0", "latex_brut", "séquence %r visible" % sequence)

    if RE_URI_LOCAL.search(texte) or RE_URI_LOCAL.search(
            "%s %s %s" % (audit["title"], audit["author"], audit["subject"])):
        signaler("P0", "uri_local", "un chemin local apparaît dans le document")

    if audience in ("PARENTS", "ELEVE"):
        for motif, code in ((RE_CRITERION_ID, "criterion_id"),
                            (RE_SKILL_ID, "skill_id"),
                            (RE_CLE_TECHNIQUE, "cle_technique")):
            trouve = motif.search(texte)
            if trouve:
                signaler("P0", code, "« %s » dans un document non technique"
                         % trouve.group(0))
        minuscule = texte.lower()
        for terme in TERMES_INTERDITS:
            if terme in minuscule:
                signaler("P0", "terme_interdit", "« %s »" % terme)
        if RE_PROGRESSION.search(texte):
            signaler("P0", "progression_chiffree",
                     "une progression chiffrée est annoncée")

    if not autoriser_marqueurs:
        for marqueur in MARQUEURS_TEST:
            if marqueur in texte:
                signaler("P1", "marqueur_de_test",
                         "« %s » subsiste dans un document destiné à être remis"
                         % marqueur)

    if audience == "PARENTS" and not audit["title"]:
        signaler("P2", "metadonnees", "le PDF ne porte pas de titre")
    if not audit["text_extractable"]:
        signaler("P1", "texte_non_selectionnable",
                 "le contenu n'est pas extractible : page rasterisée ?")

    return {"audit": audit, "audience": audience, "defauts": defauts}


def run(dossier, dossier_travail=None, autoriser_marqueurs=False) -> dict:
    import tempfile
    travail = Path(dossier_travail or tempfile.mkdtemp(prefix="nexus_pdfgate_"))
    pdfs = sorted(Path(dossier).glob("*.pdf"))
    releves = [controler(p, travail, autoriser_marqueurs) for p in pdfs]
    defauts = [d for r in releves for d in r["defauts"]]
    par_severite = {}
    for defaut in defauts:
        par_severite[defaut["severite"]] = par_severite.get(defaut["severite"], 0) + 1
    bloquants = [d for d in defauts if d["severite"] in ("P0", "P1")]
    return {"documents": len(releves), "reports": releves, "defects": defauts,
            "by_severity": par_severite, "blocking": len(bloquants),
            "ok": not bloquants, "workdir": str(travail)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dossier", help="répertoire des PDF à contrôler")
    ap.add_argument("--travail", default=None)
    ap.add_argument("--allow-test-markers", action="store_true",
                    help="corpus de QA : les marqueurs de fixture y sont normaux")
    ap.add_argument("--json", default=None)
    args = ap.parse_args(argv)

    rapport = run(args.dossier, args.travail, args.allow_test_markers)
    if not rapport["documents"]:
        print("aucun PDF dans %s" % args.dossier, file=sys.stderr)
        return 2

    for releve in rapport["reports"]:
        etat = "OK" if not releve["defauts"] else ", ".join(
            "%s:%s" % (d["severite"], d["code"]) for d in releve["defauts"])
        print("%-52s %2d p  %s" % (releve["audit"]["document"][:52],
                                   releve["audit"]["pages"], etat))
    print()
    print("documents %d · défauts %s · bloquants %d"
          % (rapport["documents"], rapport["by_severity"] or "aucun",
             rapport["blocking"]))
    print("REPORT_PDF_QUALITY = %s" % ("PASS" if rapport["ok"] else "FAIL"))

    if args.json:
        Path(args.json).write_text(json.dumps(rapport, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
    return 0 if rapport["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
