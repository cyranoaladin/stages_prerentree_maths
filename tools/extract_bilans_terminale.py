#!/usr/bin/env python3
"""Extraction structurée des bilans de positionnement de la cohorte Terminale.

Les bilans PDF de `Bilans/` sont la seule source de vérité diagnostique du stage de
pré-rentrée Terminale. Ce script les lit et en produit `content/diagnostics_terminale.json`,
qui alimente ensuite `tools/build_terminale.py`.

Rien n'est inventé ici : chaque champ du JSON produit est un extrait littéral du bilan
(énoncé, réponse donnée, réponse attendue, origine de l'erreur, ce qu'il faut retenir,
pourcentage de réussite par domaine, posture pédagogique par séance). L'individualisation
des livrets repose entièrement sur ces données.

Usage :
    python3 tools/extract_bilans_terminale.py            # écrit content/diagnostics_terminale.json
    python3 tools/extract_bilans_terminale.py --check    # vérifie que le fichier est à jour
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pypdf
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_RELATIVE_PATH = "content/diagnostics_terminale.json"

# Les bilans sont produits avec une police dont pypdf, avant la 6.16, restitue mal
# l'espacement : « Terminale » ressort en « T erm inale », « numérateur » en « num érateur ».
# L'erreur est silencieuse — elle ne lève rien, elle abîme les énoncés — et se propagerait
# telle quelle dans les livrets des élèves. On refuse donc d'extraire sous cette version.
PYPDF_MINIMUM = (6, 16)

# Bilans de la cohorte Terminale, dans l'ordre de lecture. La clé est l'identifiant de
# diagnostic utilisé par content/students_terminale.json.
BILANS: dict[str, str] = {
    "adam-zahouani--maths": "Bilans/bilan-nexus-eleve_adam_zahouani_maths.pdf",
    "adam-zahouani--nsi": "Bilans/bilan-nexus-eleve_adam_zahouani_nsi.pdf",
    "alexandre-zahouani--maths": "Bilans/bilan-nexus-eleve_alexandre_zahouani_maths.pdf",
    "alexandre-zahouani--nsi": "Bilans/bilan-nexus-eleve_alexandre_zahouani_nsi.pdf",
    "sara-bsiri--maths": "Bilans/bilan-nexus-eleve_bsiri_maths.pdf",
    "sara-bsiri--maths-expertes": "Bilans/bilan-nexus-eleve_bsiri_maths_expertes.pdf",
    "sara-bsiri--nsi": "Bilans/bilan-nexus-eleve_bsiri_nsi.pdf",
    "yassine-ben-hassine--maths": "Bilans/bilan-nexus-eleve_yassine_maths.pdf",
    "yassine-ben-hassine--nsi": "Bilans/bilan-nexus-eleve_yassine_nsi.pdf",
    "ahmed-benhadj-salem-tle--nsi": "Bilans/bilan-nexus-eleve_benhadjsalem_nsi_terminale.pdf",
    "melek-smida--maths": "Bilans/bilan-nexus-eleve_bensmida_maths.pdf",
    "melek-smida--maths-expertes": "Bilans/bilan-nexus-eleve_bensmida_maths_expertes.pdf",
    "ines-darghouth--maths": "Bilans/bilan-nexus-eleve_ines_darghouth_maths.pdf",
    "rostom-fekih--maths": "Bilans/bilan-nexus-eleve_maths_rostom_fekih.pdf",
    "melek-smida--pc": "Bilans/bilan-nexus-eleve_smida_pc_terminale.pdf",
    "rostom-fekih--pc": "Bilans/bilan-nexus-eleve_PC_rostom_fekih.pdf",
    "mayar-ourabi--pc": "Bilans/bilan-nexus-eleve_mayar_PC_terminale.pdf",
}

SUBSCRIPTS = "₀₁₂₃₄₅₆₇₈₉ₙ"
# Les signes exposants + et − comptent : sans eux, « Cu²⁺ » ressort « Cu² ⁺ » et tous les
# ions de la chimie (H₃O⁺, Fe³⁺, HO⁻, e⁻) sont coupés en deux.
SUPERSCRIPTS = "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻"

# Le rendu PDF insère des espaces parasites autour des indices, exposants et symboles
# mathématiques. On les recolle pour que les énoncés restent lisibles en Markdown.
_GLUE_BEFORE = re.compile(r"\s+([" + SUBSCRIPTS + SUPERSCRIPTS + r"])")
_GLUE_AFTER = re.compile(r"([" + SUBSCRIPTS + SUPERSCRIPTS + r"])\s+(?=[0-9])")
# Un indice suivi d'un symbole d'élément lui-même exposé continue une formule chimique :
# « H₃ O⁺ » doit se recoller en « H₃O⁺ ». La condition sur l'exposant qui suit évite de
# souder du texte courant, où « u₀ est croissante » doit rester tel quel.
_GLUE_FORMULA = re.compile(
    r"([" + SUBSCRIPTS + r"])\s+([A-Z][a-z]?)(?=[" + SUPERSCRIPTS + r"])"
)
_SYMBOL_SPACING = re.compile(r"([ℝℕℤℚΔ∞])\s{2,}")

# Marqueurs de page insérés par _read_pages : ils ne doivent jamais atteindre le JSON.
PAGE_MARKER = re.compile(r"\s*--- p\d+ ---\s*")

VERDICT_LINE = re.compile(
    r"^(JUSTE|À REVOIR|NON TRAITÉE|NON TRAITÉ|SANS RÉPONSE)\s+"
    r"(?:Certitude déclarée\s*:\s*(\d)/4\s*—\s*«\s*(.+?)\s*»|Certitude non renseignée)\s*$"
)
# Ces libellés sont recherchés dans du texte déjà passé par clean(), donc avec des
# apostrophes droites : les écrire ici avec l'apostrophe typographique du PDF ne
# correspondrait plus à rien.
FIELD_REPONSE_DONNEE = "Réponse donnée"
FIELD_REPONSE = "Réponse"
FIELD_REPONSE_ATTENDUE = "Réponse attendue"
FIELD_ORIGINE_ERREUR = "D'où vient l'erreur"
FIELD_A_RETENIR = "Ce qu'il faut retenir"
FIELD_BOUNDARY = "|".join(
    re.escape(libelle) + r"\s*:"
    for libelle in (
        FIELD_REPONSE_DONNEE, FIELD_REPONSE, FIELD_REPONSE_ATTENDUE,
        FIELD_ORIGINE_ERREUR, FIELD_A_RETENIR,
    )
)
POSTURES = ("CONFRONTER", "INSTALLER", "CONSOLIDER", "DIAGNOSTIQUER")

QUADRANT_LABELS = (
    ("Réponses sûres… mais à revoir", "certitudes_a_revoir"),
    ("Réponses justes, données avec\nconfiance", "acquis"),
    ("Difficulté repérée, sans fausse certitude", "a_installer"),
    ("Réponses justes, mais hésitantes", "a_consolider"),
)
EMPTY_QUADRANT_PREFIXES = ("Rien ici", "Pas encore", "Aucun domaine", "Le bilan ne fait pas")
# Séparateurs de la légende qui suit la liste des domaines dans chaque quadrant.
QUADRANT_LEGEND = r"Priorité :|Acquis :|Prêt à apprendre|Presque acquis|Consolidation|On stabilise|On bâtit"


def clean(value: str) -> str:
    """Normalise un fragment de texte extrait du PDF en une ligne Markdown propre.

    Deux normalisations typographiques sont appliquées ici plutôt qu'à la génération :
    les marqueurs de page insérés par _read_pages sont retirés, et l'apostrophe
    typographique du PDF est ramenée à l'apostrophe droite — seule forme employée par
    les documents générés. Sans elle, un même livret mêlerait les deux formes selon que
    la phrase vient du bilan ou du gabarit.
    """
    value = PAGE_MARKER.sub(" ", value)
    value = value.replace("\u00a0", " ").replace("\u2019", "'").replace("\n", " ")
    value = _GLUE_BEFORE.sub(r"\1", value)
    value = _GLUE_AFTER.sub(r"\1", value)
    value = _GLUE_FORMULA.sub(r"\1\2", value)
    value = _SYMBOL_SPACING.sub(r"\1 ", value)
    value = re.sub(r"\s{2,}", " ", value)
    # Espace parasite avant le point ou la virgule, laissé par le recollage des formules.
    # On ne touche pas aux deux-points, points-virgules et points d'interrogation : la
    # typographie française y demande une espace.
    return re.sub(r"\s+([.,])", r"\1", value).strip()


def _block(text: str, start: str, end: str) -> str:
    found = re.search(start + r"\n(.*?)(?=\n(?:" + end + "))", text, re.S)
    return clean(found.group(1)) if found else ""


def _numbered(raw: str) -> list[str]:
    """Découpe une liste « 1. … 2. … » aplatie par l'extraction PDF."""
    if not raw:
        return []
    parts = re.split(r"(?:^|\s)(\d+)\.\s", " " + raw)
    return [clean(parts[index + 1]) for index in range(1, len(parts) - 1, 2)]


def _read_pages(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    marked = "\n".join(f"--- p{number} ---\n{page}" for number, page in enumerate(pages, 1))
    return re.sub(r"\nNexus Réussite · Document pédagogique confidentiel\n?", "\n", marked)


def _parse_scores(text: str) -> dict[str, float]:
    scores: dict[str, float] = {}
    section = re.search(r"Ta réussite par domaine\n(.*?)\nCes chiffres", text, re.S)
    if not section:
        return scores
    for line in section.group(1).splitlines():
        matched = re.match(r"^(.*?)\s+(\d+(?:,\d+)?)$", line.strip())
        if matched:
            scores[clean(matched.group(1))] = float(matched.group(2).replace(",", "."))
    return scores


def _parse_quadrants(text: str) -> dict[str, list[str]]:
    quadrants: dict[str, list[str]] = {}
    for label, key in QUADRANT_LABELS:
        found = re.search(
            re.escape(label) + r"\n(.*?)(?=\n(?:Réponses|Difficulté|Sans réponse|Ta carte|--- p))",
            text, re.S,
        )
        if not found:
            quadrants[key] = []
            continue
        body = clean(found.group(1))
        if body.startswith(EMPTY_QUADRANT_PREFIXES):
            quadrants[key] = []
            continue
        head = re.split(QUADRANT_LEGEND, body)[0]
        quadrants[key] = [
            clean(part) for part in head.split("·")
            if clean(part) and clean(part) != "—"
        ]
    unanswered = re.search(r"Sans réponse, à situer au démarrage\s*:\s*(.+?)\.\n", text)
    quadrants["sans_reponse"] = (
        [clean(part) for part in re.split(r",|·| et ", unanswered.group(1)) if clean(part)]
        if unanswered else []
    )
    return quadrants


def _parse_seances(text: str) -> list[dict[str, object]]:
    section = re.search(
        r"Ton parcours pendant le stage — cinq séances\n(.*?)(?=\nTon plan d’action)", text, re.S
    )
    if not section:
        return []
    body = re.sub(r"\n--- p\d+ ---\n", "\n", section.group(1))
    chunks = re.split(r"\nSÉANCE (\d+) · DEUX HEURES\n", "\n" + body)
    seances: list[dict[str, object]] = []
    postures = "|".join(POSTURES)
    for index in range(1, len(chunks) - 1, 2):
        content = chunks[index + 1]
        focus = [
            {
                "domaine": clean(found.group(1)),
                "posture": found.group(2),
                "objectif": clean(found.group(3)),
                "demarche": clean(found.group(4)),
            }
            for found in re.finditer(
                r"(.+?)\s(" + postures + r")\nObjectif\s*:\s*(.+?)\nDémarche\s*:\s*(.+?)"
                r"(?=\n[^\n]+ (?:" + postures + r")\n|\Z)",
                content, re.S,
            )
        ]
        seances.append({
            "seance": int(chunks[index]),
            "focus": focus,
            "consolidation_ensemble": not focus and "Consolidation d’ensemble" in content,
        })
    return seances


def _parse_items(text: str, domains: set[str]) -> list[dict[str, object]]:
    section = re.search(r"Le détail de tes réponses\n(.*?)(?=\nPour finir)", text, re.S)
    if not section:
        return []
    lines = re.sub(r"\n--- p\d+ ---\n", "\n", section.group(1)).splitlines()
    items: list[dict[str, object]] = []
    domain: str | None = None
    index = 0
    while index < len(lines):
        line = clean(lines[index])
        if line in domains:
            domain = line
            index += 1
            continue
        verdict_match = VERDICT_LINE.match(line)
        if not verdict_match:
            index += 1
            continue
        index += 1
        buffer: list[str] = []
        while index < len(lines) and not VERDICT_LINE.match(clean(lines[index])) and clean(lines[index]) not in domains:
            buffer.append(lines[index])
            index += 1
        blob = clean(" ".join(buffer))

        def field(name: str) -> str | None:
            found = re.search(re.escape(name) + r"\s*:\s*(.*?)(?=" + FIELD_BOUNDARY + r"|$)", blob)
            return clean(found.group(1)) if found else None

        items.append({
            "domaine": domain,
            "verdict": verdict_match.group(1),
            "certitude_sur_4": int(verdict_match.group(2)) if verdict_match.group(2) else None,
            "certitude_mot": verdict_match.group(3),
            "question": clean(re.split(FIELD_BOUNDARY, blob)[0]),
            "reponse_donnee": field(FIELD_REPONSE_DONNEE) or field(FIELD_REPONSE),
            "reponse_attendue": field(FIELD_REPONSE_ATTENDUE),
            "origine_erreur": field(FIELD_ORIGINE_ERREUR),
            "a_retenir": field(FIELD_A_RETENIR),
        })
    return items


def parse_bilan(path: Path) -> dict[str, object]:
    """Retourne le diagnostic complet contenu dans un bilan élève."""
    text = _read_pages(path)
    identity = re.search(
        r"^(.+?) · (Terminale|1re|2de|3e|4e) · (.+?) · (\d{4}-\d{2}-\d{2})$", text, re.M
    )
    if not identity:
        raise ValueError(f"En-tête d'identité introuvable dans {path}")
    scores = _parse_scores(text)
    return {
        "source_pdf": path.relative_to(ROOT).as_posix(),
        "eleve": clean(identity.group(1)),
        "niveau": identity.group(2),
        "matiere": clean(identity.group(3)),
        "date_bilan": identity.group(4),
        "reussite_par_domaine": scores,
        "carte_maitrise_confiance": _parse_quadrants(text),
        "points_appui": _numbered(_block(text, "Tes points d’appui", "Tes priorités pour le stage")),
        "priorites_stage": _numbered(_block(text, "Tes priorités pour le stage", "Ton parcours pendant le stage")),
        "plan_action_inter_seances": _numbered(
            _block(text, "Ton plan d’action entre les séances", "Ton auto-évaluation")
        ),
        "auto_evaluation": _block(text, "Ton auto-évaluation", "Le détail de tes réponses|Pour finir"),
        "parcours_seances": _parse_seances(text),
        "items": _parse_items(text, set(scores)),
    }


def check_pypdf_version() -> None:
    version = tuple(int(part) for part in pypdf.__version__.split(".")[:2])
    if version < PYPDF_MINIMUM:
        minimum = ".".join(str(part) for part in PYPDF_MINIMUM)
        raise RuntimeError(
            f"pypdf {pypdf.__version__} restitue mal l'espacement des bilans : les mots "
            f"ressortent coupés (« T erm inale »). Version minimale requise : {minimum}. "
            "Installez-la avant de régénérer, sinon les livrets hériteraient d'énoncés "
            "abîmés."
        )


def build_dataset(root: Path = ROOT) -> dict[str, object]:
    check_pypdf_version()
    diagnostics = {}
    for diagnostic_id, relative in BILANS.items():
        path = root / relative
        if not path.exists():
            raise FileNotFoundError(f"Bilan manquant : {relative}")
        diagnostics[diagnostic_id] = parse_bilan(path)
    return {
        "schemaVersion": "nexus-diagnostics-terminale-v1",
        "scope": "stages_terminale_2026",
        "note": (
            "Données extraites automatiquement des bilans de positionnement PDF par "
            "tools/extract_bilans_terminale.py. Ne pas éditer à la main : régénérer. "
            "L'extraction n'est pas rejouée en intégration continue — le rendu du texte "
            "d'un PDF dépend de la version de pypdf — mais tests/test_terminale.py vérifie "
            "que ce fichier reste cohérent avec le registre et la banque d'items."
        ),
        "extraitAvec": f"pypdf {pypdf.__version__}",
        "diagnostics": diagnostics,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="échoue si le JSON committé est périmé")
    args = parser.parse_args(argv)

    dataset = build_dataset()
    rendered = json.dumps(dataset, ensure_ascii=False, indent=2) + "\n"
    target = ROOT / OUTPUT_RELATIVE_PATH

    if args.check:
        if not target.exists():
            print(f"ÉCHEC : {OUTPUT_RELATIVE_PATH} absent.")
            return 1
        if target.read_text(encoding="utf-8") != rendered:
            print(f"ÉCHEC : {OUTPUT_RELATIVE_PATH} ne correspond plus aux bilans PDF.")
            return 1
        print(f"OK : {OUTPUT_RELATIVE_PATH} est à jour ({len(dataset['diagnostics'])} bilans).")
        return 0

    target.write_text(rendered, encoding="utf-8")
    print(f"Écrit {OUTPUT_RELATIVE_PATH} ({len(dataset['diagnostics'])} bilans).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
