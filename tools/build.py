#!/usr/bin/env python3
"""Build local et reproductible de la documentation des stages de mathématiques."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from datetime import date

from pypdf import PdfReader, PdfWriter
from weasyprint import HTML

LEVELS = ("4e", "3e", "2nde", "1ere_spe")
ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
VERSION = "2026.1"
STUDENT_NAMES = (
    "Sinda Chikhaoui", "Fares Darghouth", "Sarah Bargaoui", "Selim Mansouri",
    "Amine Mansouri", "Fares Laajili", "Noa Maniaci", "Ahmed Bakir",
    "Donia Khadhrani", "Malek Khadhrani", "Ahmad Beldi",
)


def classify_document(path: Path) -> dict[str, object]:
    """Classify one operational Markdown source without reading private PDFs."""
    path_text = path.as_posix()
    level = next((item for item in LEVELS if item in path.parts), "racine")
    session = next((item for item in path.parts if item.startswith("S") and item[1:].isdigit()), None)
    name = path.stem
    confidential = "04_NOMINATIFS" in path.parts
    if confidential:
        audience = "nominatif_prive"
    elif "ELEVE" in name:
        audience = "eleve"
    elif "PROF" in name or "ENSEIGNANT" in path_text or "Guide_Formateur" in name:
        audience = "enseignant"
    else:
        audience = "mixte"
    if "Evaluation" in name or "Diagnostic" in name:
        document_type = "evaluation"
    elif "ELEVE" in name:
        document_type = "fiche_eleve"
    elif "PROF" in name:
        document_type = "fiche_professeur"
    elif "SUPPORTS" in name:
        document_type = "supports"
    elif "AIDES" in name:
        document_type = "aides"
    elif "Portfolio" in name:
        document_type = "portfolio"
    elif "Dossier" in name:
        document_type = "dossier"
    elif "Remediation" in name:
        document_type = "remediation"
    elif "Guide" in name:
        document_type = "guide"
    elif "Tableau" in name:
        document_type = "tableau_bord"
    elif "MASTER" in name:
        document_type = "master"
    else:
        document_type = "index" if name == "index" else "document"
    return {
        "id": path.with_suffix("").as_posix().replace("/", "--"),
        "level": level,
        "session": session,
        "source": path.as_posix(),
        "title": name.replace("_", " "),
        "audience": audience,
        "type": document_type,
        "confidential": confidential,
    }


def public_documents(documents: list[dict[str, object]]) -> list[dict[str, object]]:
    return [document for document in documents if not document["confidential"]]


def output_pdf_name(document: dict[str, object]) -> str:
    return Path(str(document["source"])).with_suffix(".pdf").name


def build_catalog(root: Path = ROOT) -> list[dict[str, object]]:
    """Return every operational Markdown file, never a canonical source."""
    catalog: list[dict[str, object]] = []
    for level in LEVELS:
        level_root = root / level
        if not level_root.exists():
            continue
        for path in sorted(level_root.rglob("*.md")):
            if "05_SOURCES" in path.parts:
                continue
            relative = path.relative_to(root)
            document = classify_document(relative)
            text = path.read_text(encoding="utf-8", errors="replace")
            contains_pii = any(name in text for name in STUDENT_NAMES)
            if contains_pii:
                document["confidential"] = True
                if document["audience"] != "nominatif_prive":
                    document["audience"] = "enseignant_prive"
            document["contains_pii"] = contains_pii
            document["order"] = len(catalog) + 1
            document["pedagogical_source"] = f"{level}/05_SOURCES/stage_prerentree_{ {'4e':'quatrieme','3e':'troisieme','2nde':'seconde','1ere_spe':'premiere'}[level] }_maths.md"
            catalog.append(document)
    return catalog


def is_individual_student_doc(document: dict[str, object]) -> bool:
    """True only for a per-student dossier under 04_NOMINATIFS, not for a generic
    teacher/master document that merely mentions a student's name in passing."""
    return "04_NOMINATIFS" in Path(str(document["source"])).parts


def document_bucket(document: dict[str, object]) -> str:
    if is_individual_student_doc(document):
        return "nominatifs-prives"
    if (
        document["audience"] in {"enseignant", "enseignant_prive"}
        or document["type"] in {"fiche_professeur", "guide", "tableau_bord", "master"}
        or "Corrige" in str(document["source"])
    ):
        return "enseignants"
    if document["type"] == "evaluation":
        return "evaluations"
    if document["type"] in {"supports", "aides"}:
        return "supports"
    return "eleves"


def document_html_path(document: dict[str, object], private: bool = False) -> Path:
    site = DIST / ("site-private" if private else "site-public")
    return site / Path(str(document["source"])).with_suffix(".html")


def document_pdf_path(document: dict[str, object]) -> Path:
    return DIST / "pdf" / str(document["level"]) / document_bucket(document) / output_pdf_name(document)


def relative_link(source: Path, destination: Path) -> str:
    return os.path.relpath(destination, source.parent).replace(os.sep, "/")


def _mathml_tag(node: ET.Element) -> str:
    tag = node.tag
    return tag.split('}')[-1] if '}' in tag else tag


def _render_mathml_node(node: ET.Element) -> str:
    """Render one MathML node as HTML/CSS. WeasyPrint 68.1 does not lay out MathML
    structural elements (mfrac/msup/msub/msqrt render as flat, ambiguous concatenated
    text -- see reports/SOURCE_ERRATA.md ERR-009), so structural math is rendered as
    plain HTML/CSS instead of relying on native <math> box layout."""
    tag = _mathml_tag(node)
    children = list(node)
    text = html.escape(node.text) if node.text else ""

    if tag in ("math", "mrow", "mstyle", "mpadded", "mphantom"):
        return "".join(_render_mathml_node(c) for c in children)
    if tag == "semantics":
        return _render_mathml_node(children[0]) if children else ""
    if tag == "annotation" or tag == "annotation-xml":
        return ""
    if tag in ("mn", "mi", "mo", "mtext"):
        return text
    if tag == "mspace":
        return " "
    if tag == "msup" and len(children) == 2:
        return _render_mathml_node(children[0]) + "<sup>" + _render_mathml_node(children[1]) + "</sup>"
    if tag == "msub" and len(children) == 2:
        return _render_mathml_node(children[0]) + "<sub>" + _render_mathml_node(children[1]) + "</sub>"
    if tag == "msubsup" and len(children) == 3:
        base, sub, sup = children
        return (
            _render_mathml_node(base)
            + "<sub>" + _render_mathml_node(sub) + "</sub>"
            + "<sup>" + _render_mathml_node(sup) + "</sup>"
        )
    if tag == "mfrac" and len(children) == 2:
        num, den = children
        return (
            '<span class="mfrac"><span class="mfrac-num">' + _render_mathml_node(num) + "</span>"
            '<span class="mfrac-den">' + _render_mathml_node(den) + "</span></span>"
        )
    if tag == "msqrt":
        inner = "".join(_render_mathml_node(c) for c in children)
        return '<span class="msqrt"><span class="msqrt-sym">√</span><span class="msqrt-content">' + inner + "</span></span>"
    if tag == "mroot" and len(children) == 2:
        base, index = children
        return (
            '<span class="msqrt"><sup class="msqrt-index">' + _render_mathml_node(index) + "</sup>"
            '<span class="msqrt-sym">√</span><span class="msqrt-content">' + _render_mathml_node(base) + "</span></span>"
        )
    # Fallback for any other MathML element (mtable, menclose, ...): render children inline.
    return "".join(_render_mathml_node(c) for c in children)


def render_math_for_print(fragment: str) -> str:
    def replace(match: "re.Match[str]") -> str:
        xml_text = re.sub(r'\bxmlns="[^"]*"', '', match.group(0), count=1)
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return match.group(0)
        display = match.group(1) or "inline"
        rendered = _render_mathml_node(root)
        css_class = "math-display" if display == "block" else "math-inline"
        return f'<span class="{css_class}">{rendered}</span>'

    return re.sub(r'<math display="(inline|block)"[^>]*>(.*?)</math>', replace, fragment, flags=re.S)


def render_fragment(source: Path) -> str:
    result = subprocess.run(
        ["pandoc", str(source), "--from=gfm", "--to=html5", "--mathml", "--shift-heading-level-by=1"],
        check=True,
        capture_output=True,
        text=True,
    )
    fragment = render_math_for_print(result.stdout)
    # A wide table (many columns) must scroll within its own box on narrow screens;
    # the page itself must never gain a horizontal scrollbar (section 7.6).
    return re.sub(r'(<table[^>]*>.*?</table>)', r'<div class="table-scroll">\1</div>', fragment, flags=re.S)


def page_shell(title: str, content: str, css_href: str, js_href: str, breadcrumbs: str, badge: str, pdf_href: str | None, confidential: bool) -> str:
    safe_title = html.escape(title)
    confidentiality = '<p class="notice confidential">CONFIDENTIEL — diffusion strictement limitée.</p>' if confidential else ''
    pdf_action = f'<a class="button" href="{html.escape(pdf_href)}">Télécharger le PDF</a>' if pdf_href else ''
    return f'''<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <meta name="generator" content="Nexus Réussite {VERSION}">
  <title>{safe_title} — Nexus Réussite</title>
  <link rel="stylesheet" href="{html.escape(css_href)}">
  <link rel="stylesheet" href="{html.escape(css_href.rsplit('/', 1)[0] + '/print.css')}" media="print">
  <script defer src="{html.escape(js_href)}"></script>
</head>
<body>
  <a class="skip-link" href="#contenu">Aller au contenu principal</a>
  <header class="site-header"><a class="brand" href="{html.escape(relative_link_placeholder())}">Nexus Réussite</a><span class="badge">{html.escape(badge)}</span>{pdf_action}<button class="print-button" type="button" onclick="window.print()">Imprimer</button></header>
  <nav class="breadcrumbs" aria-label="Fil d’Ariane">{breadcrumbs}</nav>
  <main id="contenu"><h1>{safe_title}</h1>{confidentiality}{content}</main>
  <footer>Version {VERSION} · Génération locale {date.today().isoformat()} · Nexus Réussite</footer>
</body>
</html>'''


def relative_link_placeholder() -> str:
    """Replaced after shell creation to keep document markup simple."""
    return "__ROOT__"


def write_document_html(document: dict[str, object], private: bool) -> Path:
    source = ROOT / str(document["source"])
    target = document_html_path(document, private)
    target.parent.mkdir(parents=True, exist_ok=True)
    css = relative_link(target, (DIST / ("site-private" if private else "site-public") / "assets/site.css"))
    js = relative_link(target, (DIST / ("site-private" if private else "site-public") / "assets/site.js"))
    site_root = DIST / ("site-private" if private else "site-public")
    root_link = relative_link(target, site_root / "index.html")
    level_link = relative_link(target, site_root / str(document["level"]) / "index.html")
    pdf = document_pdf_path(document)
    pdf_href = relative_link(target, pdf) if pdf.exists() else relative_link(target, pdf)
    crumb = f'<a href="{html.escape(root_link)}">Accueil</a> / <a href="{html.escape(level_link)}">{html.escape(str(document["level"]))}</a> / {html.escape(str(document["session"] or document["type"]))}'
    page = page_shell(
        str(document["title"]), render_fragment(source), css, js, crumb,
        str(document["audience"]).replace("_", " ").upper(), pdf_href, bool(document["confidential"]),
    ).replace("__ROOT__", root_link)
    target.write_text(page, encoding="utf-8")
    return target


def copy_assets(site: Path) -> None:
    source = ROOT / "assets"
    destination = site / "assets"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def copy_reports(site: Path) -> None:
    source = ROOT / "reports"
    destination = site / "reports"
    if destination.exists():
        shutil.rmtree(destination)
    if source.exists():
        shutil.copytree(source, destination)


def portal_page(site: Path, catalog: list[dict[str, object]], private: bool) -> None:
    site.mkdir(parents=True, exist_ok=True)
    copy_assets(site)
    copy_reports(site)
    documents = catalog if private else public_documents(catalog)
    cards = "".join(
        f'<article class="level-card"><h2>{level}</h2><p>5 séances × 2 h</p><a class="button" href="{level}/index.html">Ouvrir le niveau</a></article>'
        for level in LEVELS
    )
    confidentiality = '<p class="notice confidential">Zone privée : les dossiers nominatifs sont confidentiels.</p>' if private else '<p class="notice">Le portail public local exclut toutes les données nominatives.</p>'
    content = f'''{confidentiality}
<section><h2>Stages de mathématiques 2026-2027</h2><div class="card-grid">{cards}</div></section>
<section><h2>Recherche locale</h2><label for="search">Rechercher un document</label><input id="search" type="search" data-search-input placeholder="Niveau, séance, type ou audience"><div id="search-results" data-search-results></div></section>
<section><h2>Accès rapides</h2><p><a href="preparer-seance.html">Préparer la séance du jour</a> · <a href="packs.html">Packs prêts à imprimer</a>{' · <a href="suivi-nominatif.html">Suivi nominatif</a>' if private else ' · <a href="../site-private/index.html">Ouvrir le dossier confidentiel</a>'}</p></section>
<section><h2>État QA</h2><p><a href="reports/FINAL_DELIVERY_REPORT.md">Rapport de build</a></p></section>'''
    page = page_shell("Portail documentation", content, "assets/site.css", "assets/site.js", "Accueil", "PRIVÉ" if private else "LOCAL", None, private).replace("__ROOT__", "index.html")
    page = page.replace('<script defer src="assets/site.js"></script>', '<script defer src="assets/search-index.js"></script><script defer src="assets/site.js"></script>')
    (site / "index.html").write_text(page, encoding="utf-8")
    index = [{key: item[key] for key in ("title", "level", "session", "audience", "type", "confidential", "source")} for item in documents]
    (site / "assets/search-index.js").write_text("window.NEXUS_SEARCH_INDEX = " + json.dumps(index, ensure_ascii=False) + ";\n", encoding="utf-8")


def level_page(site: Path, level: str, catalog: list[dict[str, object]], private: bool) -> None:
    entries = [item for item in (catalog if private else public_documents(catalog)) if item["level"] == level]
    sessions = []
    for number in range(1, 6):
        session = f"S{number}"
        actions = []
        for entry in entries:
            if entry["session"] == session and entry["type"] in {"fiche_professeur", "fiche_eleve", "supports", "aides"}:
                target = document_html_path(entry, private)
                label = {"fiche_professeur": "Professeur", "fiche_eleve": "Élève", "supports": "Supports", "aides": "Aides"}[str(entry["type"])]
                actions.append(f'<a href="{html.escape(relative_link(site / level / "index.html", target))}">{label}</a>')
        if not private:
            existing = " ".join(actions)
            for label in ("Professeur", "Élève", "Supports", "Aides"):
                if f">{label}<" not in existing:
                    actions.append(f'<a href="../../site-private/{level}/index.html">{label} (zone privée)</a>')
        sessions.append(f'<article class="session-card"><h2>Séance {number}</h2><p>{" · ".join(actions) or "Documents privés ou à générer"}</p></article>')
    content = '<p><a href="../index.html">Retour au portail</a></p><div class="card-grid">' + "".join(sessions) + '</div><h2>Documents du niveau</h2><ul>' + "".join(f'<li><a href="{html.escape(relative_link(site / level / "index.html", document_html_path(item, private)))}">{html.escape(str(item["title"]))}</a> <span class="badge">{html.escape(str(item["audience"]).upper())}</span></li>' for item in entries if item["session"] is None) + '</ul>'
    page = page_shell(f"Niveau {level}", content, "../assets/site.css", "../assets/site.js", f'<a href="../index.html">Accueil</a> / {level}', "PRIVÉ" if private else "LOCAL", None, private).replace("__ROOT__", "../index.html")
    target = site / level / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")


def utility_pages(site: Path, private: bool) -> None:
    pages = {
        "preparer-seance.html": "<p>Choisissez le niveau puis la séance. Chaque carte donne accès aux fiches, supports, aides et PDF correspondants.</p>",
        "packs.html": "<p>Les packs PDF sont produits localement dans <code>dist/packs</code>. Utilisez les liens depuis les pages de niveau ou ouvrez ce dossier local.</p>",
    }
    if private:
        pages["suivi-nominatif.html"] = "<p class=\"notice confidential\">Accès réservé à l’équipe pédagogique. Les dossiers sont isolés par élève dans les PDF et manifests privés.</p>"
    for name, content in pages.items():
        page = page_shell(name.removesuffix(".html").replace("-", " ").title(), content, "assets/site.css", "assets/site.js", f'<a href="index.html">Accueil</a> / {name}', "PRIVÉ" if private else "LOCAL", None, private).replace("__ROOT__", "index.html")
        (site / name).write_text(page, encoding="utf-8")


def write_catalog(catalog: list[dict[str, object]]) -> None:
    destination = ROOT / "content/catalog.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    enriched = []
    for document in catalog:
        item = dict(document)
        item["html_public"] = document_html_path(document, False).relative_to(ROOT).as_posix() if not document["confidential"] else None
        item["html_private"] = document_html_path(document, True).relative_to(ROOT).as_posix()
        item["pdf"] = document_pdf_path(document).relative_to(ROOT).as_posix()
        item["validation_status"] = "pending_qa"
        enriched.append(item)
    destination.write_text(json.dumps(enriched, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_html(catalog: list[dict[str, object]] | None = None, clean: bool = True) -> list[dict[str, object]]:
    catalog = catalog or build_catalog()
    if clean:
        for name in ("site-public", "site-private"):
            shutil.rmtree(DIST / name, ignore_errors=True)
    write_catalog(catalog)
    for private in (False, True):
        site = DIST / ("site-private" if private else "site-public")
        portal_page(site, catalog, private)
        utility_pages(site, private)
        for level in LEVELS:
            level_page(site, level, catalog, private)
        for document in catalog:
            if private or not document["confidential"]:
                write_document_html(document, private)
    reports_target = DIST / "reports"
    shutil.rmtree(reports_target, ignore_errors=True)
    if (ROOT / "reports").exists():
        shutil.copytree(ROOT / "reports", reports_target)
    return catalog


def add_pdf_metadata(path: Path, document: dict[str, object]) -> None:
    reader = PdfReader(path)
    writer = PdfWriter()
    writer.append(reader)
    writer.add_metadata({
        "/Title": str(document["title"]), "/Author": "Nexus Réussite", "/Subject": f"{document['level']} — {document['audience']}",
        "/Keywords": f"Nexus Réussite, mathématiques, {document['level']}, {document['type']}", "/Lang": "fr-FR",
        "/NexusVersion": VERSION, "/Audience": str(document["audience"]),
    })
    with path.open("wb") as stream:
        writer.write(stream)


def build_pdf(catalog: list[dict[str, object]] | None = None, clean: bool = True) -> list[Path]:
    catalog = catalog or build_html()
    if clean:
        shutil.rmtree(DIST / "pdf", ignore_errors=True)
    paths: list[Path] = []
    for document in catalog:
        html_path = document_html_path(document, bool(document["confidential"]))
        pdf_path = document_pdf_path(document)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        HTML(filename=str(html_path), base_url=str(html_path.parent)).write_pdf(str(pdf_path))
        add_pdf_metadata(pdf_path, document)
        paths.append(pdf_path)
    return paths


def pack_writer(destination: Path, documents: list[dict[str, object]]) -> bool:
    files = [document_pdf_path(document) for document in documents if document_pdf_path(document).exists()]
    if not files:
        return False
    writer = PdfWriter()
    for path in files:
        writer.append(PdfReader(path))
    writer.add_metadata({"/Title": destination.stem, "/Author": "Nexus Réussite", "/Lang": "fr-FR", "/NexusVersion": VERSION})
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as stream:
        writer.write(stream)
    return True


def is_teacher(document: dict[str, object]) -> bool:
    source = str(document["source"])
    return document["audience"] in {"enseignant", "enseignant_prive"} or "PROF" in source or "Corrige" in source


def student_pack_documents(documents: list[dict[str, object]]) -> list[dict[str, object]]:
    return [document for document in documents if not document["confidential"] and not is_teacher(document) and document["type"] not in {"master", "index", "guide", "tableau_bord"}]


def build_packs(catalog: list[dict[str, object]] | None = None, clean: bool = True) -> list[Path]:
    catalog = catalog or build_catalog()
    destination = DIST / "packs"
    if clean:
        shutil.rmtree(destination, ignore_errors=True)
    paths: list[Path] = []
    for level in LEVELS:
        documents = [item for item in catalog if item["level"] == level]
        public = [item for item in documents if not item["confidential"]]
        non_individual = [item for item in documents if not is_individual_student_doc(item)]
        groups = {
            destination / "eleves" / f"{level}_PACK_ELEVE_COMPLET.pdf": student_pack_documents(public),
            destination / "enseignants" / f"{level}_PACK_ENSEIGNANT_COMPLET.pdf": non_individual,
            destination / "eleves" / f"{level}_PACK_EVALUATIONS_ELEVE.pdf": [item for item in public if item["type"] == "evaluation" and not is_teacher(item)],
            destination / "enseignants" / f"{level}_PACK_EVALUATIONS_CORRIGE.pdf": [item for item in non_individual if item["type"] == "evaluation" and is_teacher(item)],
        }
        for number in range(1, 6):
            session_public = [item for item in public if item["session"] == f"S{number}"]
            session_all = [item for item in non_individual if item["session"] == f"S{number}"]
            groups[destination / "eleves" / f"{level}_S{number}_PACK_ELEVE.pdf"] = student_pack_documents(session_public)
            groups[destination / "enseignants" / f"{level}_S{number}_PACK_ENSEIGNANT.pdf"] = session_all
        for pack, selection in groups.items():
            if pack_writer(pack, selection):
                paths.append(pack)
        private = [item for item in documents if item["confidential"]]
        for student in sorted({Path(str(item["source"])).parts[2] for item in private if "04_NOMINATIFS" in Path(str(item["source"])).parts}):
            selection = [item for item in private if f"04_NOMINATIFS/{student}/" in str(item["source"])]
            display = student.replace("_", "_")
            for suffix, chosen in (("PACK_TRAVAIL_PERSONNALISE", [item for item in selection if not is_teacher(item)]), ("DOSSIER_ENSEIGNANT_CONFIDENTIEL", selection)):
                pack = destination / "nominatifs-prives" / f"{level}_{display}_{suffix}.pdf"
                if pack_writer(pack, chosen):
                    paths.append(pack)
    return paths


A4_WIDTH_PT = 595.28
A4_HEIGHT_PT = 841.89
A4_TOLERANCE_PT = 2.0


def is_a4_page(width: float, height: float, tolerance: float = A4_TOLERANCE_PT) -> bool:
    """True only for A4 portrait, within a small point tolerance."""
    return abs(width - A4_WIDTH_PT) <= tolerance and abs(height - A4_HEIGHT_PT) <= tolerance


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifests() -> tuple[Path, Path]:
    public = ROOT / "MANIFEST_PUBLIC.csv"
    private = ROOT / "MANIFEST_PRIVATE.csv"
    for destination, roots in ((public, [DIST / "site-public", DIST / "pdf", DIST / "packs" / "eleves", DIST / "packs" / "enseignants"]), (private, [DIST / "site-private", DIST / "pdf", DIST / "packs" / "nominatifs-prives"])):
        with destination.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(["path", "sha256", "confidential"])
            for root in roots:
                if not root.exists():
                    continue
                for path in sorted(item for item in root.rglob("*") if item.is_file()):
                    confidential = "nominatifs-prives" in path.parts or "site-private" in path.parts
                    if destination == public and confidential:
                        continue
                    writer.writerow([path.relative_to(ROOT).as_posix(), sha256(path), "oui" if confidential else "non"])
    manifests = DIST / "manifests"
    manifests.mkdir(parents=True, exist_ok=True)
    shutil.copy2(public, manifests / public.name)
    shutil.copy2(private, manifests / private.name)
    return public, private


def qa(catalog: list[dict[str, object]] | None = None) -> dict[str, int]:
    catalog = catalog or build_catalog()
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    generated_html = list((DIST / "site-public").rglob("*.html")) + list((DIST / "site-private").rglob("*.html"))
    generated_pdf = list((DIST / "pdf").rglob("*.pdf")) + list((DIST / "packs").rglob("*.pdf"))
    external = 0
    html_errors: list[str] = []
    for path in generated_html:
        text = path.read_text(encoding="utf-8", errors="replace")
        if '<html lang="fr">' not in text or '<main id="contenu">' not in text or 'skip-link' not in text:
            html_errors.append(path.relative_to(ROOT).as_posix())
        external += len(re.findall(r'<(?:script|link|img)[^>]+(?:src|href)=["\']https?://', text, flags=re.I))
    names = STUDENT_NAMES
    student_leaks = 0
    cross_student = 0
    for document in catalog:
        source = ROOT / str(document["source"])
        text = source.read_text(encoding="utf-8", errors="replace")
        if document["audience"] == "eleve" and re.search(r'(?i)\b(corrig[ée]|réponses? attendues?|barème)\b', text):
            student_leaks += 1
        if "04_NOMINATIFS" in source.parts:
            owner = source.parts[source.parts.index("04_NOMINATIFS") + 1].replace("_", " ")
            if any(name in text for name in names if name != owner):
                cross_student += 1
    session_errors = 0
    for level in LEVELS:
        for path in (ROOT / level / "02_SEANCES").glob("S*/*_PROF_Fiche.md"):
            endpoints = [int(value) for value in re.findall(r'\|\s*(?:\d+\s*[–-]\s*)?(\d+)\s*min', path.read_text(), flags=re.I)]
            if not endpoints or max(endpoints) != 120:
                session_errors += 1
    pdf_failures: list[str] = []
    page_count = 0
    for path in generated_pdf:
        try:
            reader = PdfReader(path)
            page_count += len(reader.pages)
            if reader.is_encrypted or path.stat().st_size == 0:
                pdf_failures.append(path.relative_to(ROOT).as_posix())
        except Exception:
            pdf_failures.append(path.relative_to(ROOT).as_posix())
    counts = {
        "generated_html": len(generated_html), "generated_pdf": len(generated_pdf), "pages": page_count,
        "external_resources": external, "html_errors": len(html_errors), "student_correction_leaks": student_leaks,
        "cross_student_pii_leaks": cross_student, "session_duration_errors": session_errors,
        "pdf_structural_failures": len(pdf_failures),
    }
    # Automated counters only. This file is safe to overwrite on every build.
    # NAVIGATION_QA.md, ACCESSIBILITY_QA.md, MATH_CONTENT_AUDIT.md and PDF_STRUCTURAL_QA.md
    # hold the real, manually/agent-audited reports and must never be overwritten here.
    (reports / "BUILD_QA_COUNTERS.md").write_text(
        "# Compteurs QA automatisés (régénérés à chaque build)\n\n"
        f"- Pages HTML générées : {len(generated_html)}\n"
        f"- Erreurs structurelles HTML : {len(html_errors)}\n"
        f"- Ressources externes chargées : {external}\n"
        f"- PDF contrôlés : {len(generated_pdf)}\n"
        f"- Pages PDF totales : {page_count}\n"
        f"- Échecs d'ouverture/chiffrement/vide PDF : {len(pdf_failures)}\n"
        f"- Fiches professeur à 120 minutes : {20 - session_errors}/20\n"
        f"- Fuites de corrigé côté élève détectées : {student_leaks}\n"
        f"- Fuites de PII inter-élèves détectées : {cross_student}\n\n"
        "Pour l'audit détaillé (méthode, preuves, sévérité), voir NAVIGATION_QA.md, ACCESSIBILITY_QA.md, "
        "MATH_CONTENT_AUDIT.md et PDF_STRUCTURAL_QA.md dans ce même dossier.\n",
        encoding="utf-8",
    )
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("audit", "html", "pdf", "packs", "qa", "all"))
    args = parser.parse_args()
    catalog = build_catalog()
    if args.command == "audit":
        write_catalog(catalog)
        print(f"Catalogue : {len(catalog)} documents")
        return
    if args.command == "html":
        build_html(catalog)
    elif args.command == "pdf":
        build_pdf(catalog)
    elif args.command == "packs":
        build_packs(catalog)
    elif args.command == "qa":
        print(json.dumps(qa(catalog), ensure_ascii=False, indent=2))
        return
    elif args.command == "all":
        build_html(catalog)
        build_pdf(catalog)
        build_packs(catalog)
    write_manifests()
    print(json.dumps(qa(catalog), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
