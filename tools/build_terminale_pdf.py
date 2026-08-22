#!/usr/bin/env python3
"""Rendu imprimable des stages de pré-rentrée Terminale.

Les documents Markdown produits par `tools/build_terminale.py` sont la source de vérité ;
ce script les assemble en PDF A4 prêts à distribuer, sans jamais les modifier.

Quatre familles de sorties, sous `dist/terminale/` :

- `eleves/`      un dossier par élève et par matière : livret individuel + plan de
                 remédiation, **sans aucun corrigé** ;
- `enseignant/`  les corrigés nominatifs, le tableau de bord et le pack complet du module ;
- `seances/`     les fiches élèves des cinq séances, à photocopier pour le groupe ;
- `MANIFEST_TERMINALE.csv` l'inventaire de ce qui a été produit.

La séparation élève / enseignant est vérifiée à l'assemblage, pas seulement par
convention de nommage : un document dont le nom contient `PROF` ou `Corrige` ne peut pas
entrer dans un dossier élève. Le dépôt a déjà connu une fuite de corrigé dans un pack
nominatif (ERR-008) ; c'est ce contrôle qui l'empêche de se reproduire.

Le rendu passe par LaTeX : pandoc traduit chaque document en LaTeX, la charte
`tools/assets/nexus_terminale.sty` lui donne sa forme, et LuaLaTeX compose le PDF. Les
paquets disciplinaires y sont chargés — `amsmath`/`mathtools`/`esvect` pour les
mathématiques, `siunitx`/`mhchem`/`chemfig` pour la physique-chimie, `listings` pour le
code — de sorte que les formules, les unités et les équations de réaction sont
typographiées et non plus approchées avec des caractères Unicode.

Les PDF ne sont pas committés : leur contenu binaire dépend de la version de LuaLaTeX et
des paquets TeX installés. Ils se régénèrent avec `make terminale-pdf`.

Usage :
    python3 tools/build_terminale_pdf.py               # tout produire
    python3 tools/build_terminale_pdf.py --module tle_spe
    python3 tools/build_terminale_pdf.py --list        # lister sans rendre
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.build_terminale import MODULES, Module, load_json  # noqa: E402

OUTPUT_DIR = ROOT / "dist" / "terminale"
# La charte Terminale vit sous tools/ et non sous assets/ : `tools/build.py` recopie
# l'intégralité de assets/ dans les deux sites publiés et fait entrer chaque fichier dans
# MANIFEST_PUBLIC.csv et MANIFEST_PRIVATE.csv. Un fichier ajouté là ferait diverger les
# manifests du pipeline mathématique, que ce module ne doit pas toucher.
LATEX_STYLE = ROOT / "tools" / "assets" / "nexus_terminale.sty"

# LuaLaTeX et non pdflatex : voir l'entête de nexus_terminale.sty. Le code Python et SQL
# des modules porte des commentaires accentués que pdflatex, via listings et inputenc,
# recompose dans le désordre.
LATEX_ENGINE = "lualatex"

# Un document dont le nom porte l'un de ces marqueurs ne peut jamais rejoindre un pack élève.
TEACHER_MARKERS = ("PROF", "Corrige", "Tableau_Bord", "Guide_Formateur")

CONFIDENTIAL_NOTICE = (
    "Ce document contient des données personnelles d'un élève mineur. Sa circulation est "
    "strictement limitée à Nexus Réussite et à la famille concernée. Ne pas le joindre à un "
    "pack collectif, ne pas le remettre à un autre élève du groupe."
)


class PdfBuildError(RuntimeError):
    """Assemblage impossible ou règle de confidentialité violée."""


@dataclass
class Bundle:
    """Un PDF à produire : une page de garde et une suite de documents Markdown."""

    filename: str
    title: str
    subtitle: str
    audience: str          # "eleve" | "enseignant"
    directory: str         # sous-dossier de dist/terminale
    meta: list[tuple[str, str]]
    sources: list[Path]
    confidential: bool = False
    toc: bool = True
    student: str = ""
    module_key: str = ""
    pages: int = 0
    size_bytes: int = 0
    warnings: list[str] = field(default_factory=list)


def check_tooling() -> None:
    missing = []
    if subprocess.run(["pandoc", "--version"], capture_output=True).returncode != 0:
        missing.append("pandoc")
    if shutil.which(LATEX_ENGINE) is None:
        missing.append(LATEX_ENGINE)
    if missing:
        raise PdfBuildError(
            "Outils manquants : " + ", ".join(missing) + ". "
            "Voir README.md, section « Dépendances »."
        )
    if not LATEX_STYLE.exists():
        raise PdfBuildError(f"Charte LaTeX introuvable : {LATEX_STYLE}")


# Caractères que le corpus ne doit plus contenir : ils relèvent des mathématiques et
# doivent être écrits en LaTeX ($\square$, $\geqslant$…). Les laisser passer produirait
# des caractères manquants silencieux dans le PDF, donc des consignes illisibles.
FORBIDDEN_TEXT_SYMBOLS = "☐≥≤≠−×÷≈∞√∈∉⊂∪∩∀∃⇒⇔₀₁₂₃₄₅₆₇₈₉ₙ⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ"

LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
    "_": r"\_", "{": r"\{", "}": r"\}",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}


def latex_escape(text: str) -> str:
    """Échappe une chaîne destinée au LaTeX (titres, noms d'élèves, métadonnées)."""
    return "".join(LATEX_SPECIALS.get(char, char) for char in text)


# Une suite de points dans le Markdown est une ligne de réponse à remplir. À l'impression,
# un filet plein est plus lisible qu'une file de points et consomme moins d'encre.
DOTTED_RUN = re.compile(r"\.{8,}")
# Largeur du filet, en millimètres, pour un point de la source. Un point de la police
# Latin Modern mesure environ 1,2 mm à 10 pt : le filet garde la longueur voulue par
# l'auteur du document.
MM_PER_DOT = 1.2
MAX_RULE_MM = 168.0


def _rule_for(dots: int) -> str:
    width = min(dots * MM_PER_DOT, MAX_RULE_MM)
    if width >= MAX_RULE_MM:
        return r"\answerline"
    return r"\rule{%.0fmm}{0.32pt}" % width


def latex_fragment(source: Path) -> str:
    """Traduit un document Markdown en fragment LaTeX, via pandoc."""
    result = subprocess.run(
        [
            "pandoc", str(source),
            "--from=gfm+tex_math_dollars+raw_attribute",
            "--to=latex",
            "--top-level-division=section",
            "--wrap=preserve",
            # `--listings` fait passer les blocs de code par `listings`, dont la charte
            # définit déjà le style. Sans lui, pandoc émet ses propres environnements de
            # coloration (`Shaded`, `Highlighting`) qui supposent son gabarit.
            "--listings",
        ],
        check=True, capture_output=True, text=True,
    )
    fragment = result.stdout
    # pandoc échappe les points ; ils ressortent tels quels et repassent ici en filets.
    fragment = DOTTED_RUN.sub(lambda match: _rule_for(len(match.group(0))), fragment)
    return fragment


def check_source_notation(sources: list[Path]) -> list[str]:
    """Signale les symboles mathématiques laissés en Unicode dans une source."""
    warnings = []
    for source in sources:
        text = source.read_text(encoding="utf-8")
        found = sorted({char for char in text if char in FORBIDDEN_TEXT_SYMBOLS})
        if found:
            warnings.append(
                f"{source.relative_to(ROOT)} : notation Unicode restante « "
                + " ".join(found) + " »"
            )
    return warnings


def cover_latex(bundle: Bundle) -> str:
    # La première métadonnée sert de titre secondaire en gros ; les suivantes vont dans
    # l'encadré. La répéter dans les deux ferait doublon sur la page de garde.
    headline = bundle.meta[0][1] if bundle.meta else ""
    headline = latex_escape("" if headline and headline in bundle.subtitle else headline)
    meta = r" \\[1mm] ".join(
        rf"\textbf{{{latex_escape(label)} :}} {latex_escape(value)}"
        for label, value in bundle.meta[1:]
    )
    band = (
        rf"\nexusconfidentiel{{{latex_escape(CONFIDENTIAL_NOTICE)}}}"
        if bundle.confidential else ""
    )
    return (
        rf"\nexuscover{{{latex_escape(bundle.title)}}}"
        rf"{{{latex_escape(bundle.subtitle)}}}"
        rf"{{{headline}}}"
        rf"{{{meta}}}{{{band}}}"
    )


# En deçà de ce seuil, un sommaire coûterait une feuille par élève pour deux lignes que
# la page de garde annonce déjà.
TOC_MINIMUM_DOCUMENTS = 3


def toc_latex(bundle: Bundle) -> str:
    if not bundle.toc or len(bundle.sources) < TOC_MINIMUM_DOCUMENTS:
        return ""
    entries = "\n".join(
        rf"\item {latex_escape(document_title(source))}" for source in bundle.sources
    )
    return (
        "\\sectiontitle{Contenu de ce dossier}\n"
        "\\begin{enumerate}\n" + entries + "\n\\end{enumerate}\n\\clearpage\n"
    )


def document_title(source: Path) -> str:
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return source.stem.replace("_", " ")


def enforce_audience(bundle: Bundle) -> None:
    """Un pack élève ne peut contenir aucun document enseignant."""
    if bundle.audience != "eleve":
        return
    offenders = [
        source.name for source in bundle.sources
        if any(marker in source.name for marker in TEACHER_MARKERS)
    ]
    if offenders:
        raise PdfBuildError(
            f"Le dossier élève « {bundle.filename} » contiendrait un document enseignant : "
            + ", ".join(offenders)
        )


# Au-delà, l'intitulé passe à la ligne dans l'entête et mange la marge haute.
HEADER_MAX_CHARACTERS = 72


def shorten(text: str, limit: int = HEADER_MAX_CHARACTERS) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return f"{cut}\u2026"


def latex_document(bundle: Bundle) -> str:
    header_right = latex_escape(shorten(bundle.subtitle or bundle.title))
    footer_left = latex_escape(bundle.title)
    body = "\n\n\\clearpage\n\n".join(latex_fragment(source) for source in bundle.sources)
    return "\n".join([
        r"\documentclass[10pt,a4paper]{article}",
        r"\usepackage{nexus_terminale}",
        rf"\setnexusheader{{{header_right}}}{{{footer_left}}}",
        r"\begin{document}",
        cover_latex(bundle),
        toc_latex(bundle),
        body,
        r"\end{document}",
        "",
    ])


def render(bundle: Bundle) -> Path:
    enforce_audience(bundle)
    missing = [source for source in bundle.sources if not source.exists()]
    if missing:
        raise PdfBuildError(
            f"{bundle.filename} : source(s) introuvable(s) — "
            + ", ".join(str(path.relative_to(ROOT)) for path in missing)
        )
    bundle.warnings.extend(check_source_notation(bundle.sources))

    target = OUTPUT_DIR / bundle.directory / bundle.filename
    target.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="nexus-tle-") as workdir:
        work = Path(workdir)
        shutil.copy(LATEX_STYLE, work / LATEX_STYLE.name)
        job = "document"
        (work / f"{job}.tex").write_text(latex_document(bundle), encoding="utf-8")
        compile_latex(work, job, bundle.filename)
        shutil.copy(work / f"{job}.pdf", target)

    bundle.size_bytes = target.stat().st_size
    bundle.pages = count_pages(target)
    return target


# Deux passes suffisent : la seconde résout \pageref{LastPage} du pied de page. latexmk
# les enchaîne et s'arrête dès que les références sont stables.
def compile_latex(work: Path, job: str, label: str) -> None:
    result = subprocess.run(
        [
            "latexmk", f"-{LATEX_ENGINE}", "-interaction=nonstopmode",
            "-halt-on-error", "-file-line-error", f"-jobname={job}", f"{job}.tex",
        ],
        cwd=work, capture_output=True, text=True,
    )
    if result.returncode != 0 or not (work / f"{job}.pdf").exists():
        log = (work / f"{job}.log")
        detail = ""
        if log.exists():
            errors = [
                line for line in log.read_text(encoding="utf-8", errors="replace").splitlines()
                if line.startswith("!") or ".tex:" in line
            ]
            detail = "\n".join(errors[:12])
        raise PdfBuildError(f"LaTeX a échoué sur « {label} » :\n{detail or result.stdout[-2000:]}")


def count_pages(pdf_path: Path) -> int:
    try:
        from pypdf import PdfReader
    except ImportError:
        return 0
    return len(PdfReader(str(pdf_path)).pages)


def nominative_dir(module: Module) -> Path:
    return ROOT / module.key / module.nominative_dir


def student_documents(module: Module, slug: str, suffix: str) -> dict[str, Path]:
    base = nominative_dir(module) / slug
    return {
        "livret": base / f"{module.key}_Livret_Individuel_{suffix}.md",
        "remediation_eleve": base / f"{module.key}_Remediation_Ciblee_{suffix}_ELEVE.md",
        "remediation_prof": base / f"{module.key}_Remediation_Ciblee_{suffix}_PROF_Corrige.md",
    }


def subject_suffix(module: Module, matiere: str, slug: str) -> str:
    from tools.build_terminale import slug as slugify

    return slug if matiere == module.subject_label else f"{slug}_{slugify(matiere)}"


def session_sheets(module: Module, audience: str) -> list[Path]:
    kind = "ELEVE_Activite" if audience == "eleve" else "PROF_Fiche"
    return [
        ROOT / module.key / "02_SEANCES" / f"S{number}" / f"{module.key}_S{number}_{kind}.md"
        for number, _theme in module.sessions
    ]


def support_sheets(module: Module) -> list[Path]:
    supports = "SUPPORTS_Pratiques" if module.key == "tle_nsi" else "SUPPORTS_Manipulation"
    paths: list[Path] = []
    for number, _theme in module.sessions:
        folder = ROOT / module.key / "02_SEANCES" / f"S{number}"
        paths.append(folder / f"{module.key}_S{number}_{supports}.md")
        paths.append(folder / f"{module.key}_S{number}_AIDES_Cartes.md")
    return paths


def evaluation_sheets(module: Module, audience: str) -> list[Path]:
    folder = ROOT / module.key / "03_EVALUATIONS"
    if module.key == "tle_spe":
        diagnostic = f"{module.key}_Mini_Diagnostic_"
    else:
        diagnostic = f"{module.key}_Mini_Diagnostic_Pratique_"
    if audience == "eleve":
        names = [f"{diagnostic}ELEVE.md", f"{module.key}_Evaluation_Finale_ELEVE.md"]
    else:
        names = [
            f"{diagnostic}PROF_Corrige.md",
            f"{module.key}_Evaluation_Finale_PROF_Corrige_Bareme.md",
        ]
    return [folder / name for name in names]


def portfolio_sheets(module: Module) -> list[Path]:
    if module.key == "tle_spe":
        return [ROOT / module.key / "03_EVALUATIONS" / f"{module.key}_Portfolio_Individuel.md"]
    folder = ROOT / module.key / "04_PORTFOLIO"
    return [
        folder / f"{module.key}_Memento_Python_Terminale_ELEVE.md",
        folder / f"{module.key}_Portfolio_Individuel.md",
    ]


def plan_bundles(root: Path = ROOT) -> list[Bundle]:
    """Établit la liste des PDF à produire, sans rien rendre."""
    registry = load_json(root, "content/students_terminale.json")
    groups = {group["id"]: group for group in registry["groupes"]}
    bundles: list[Bundle] = []

    for student in registry["students"]:
        if not student.get("active", True):
            continue
        group = groups[student["groupe"]]
        subjects = list(student["matieres"]) + [
            dict(missing, diagnosticId=None)
            for missing in student.get("matieresSansDiagnostic", [])
        ]
        for subject in subjects:
            module = MODULES[subject["module"]]
            suffix = subject_suffix(module, subject["matiere"], student["slug"])
            documents = student_documents(module, student["slug"], suffix)
            label = module.key.replace("tle_", "Tle_").upper().replace("TLE_", "Tle_")
            matiere_tag = "" if subject["matiere"] == module.subject_label else "_EXPERTES"

            # Dossier élève : livret + remédiation, jamais de corrigé.
            eleve_sources = [documents["livret"]]
            if subject.get("diagnosticId") is not None:
                eleve_sources.append(documents["remediation_eleve"])
            bundles.append(Bundle(
                filename=f"{label}{matiere_tag}_{student['slug']}_DOSSIER_ELEVE_PERSONNALISE.pdf",
                title="Dossier individuel",
                subtitle=f"{student['displayName']} — {subject['matiere']}",
                audience="eleve",
                directory="eleves",
                meta=[
                    ("Élève", student["displayName"]),
                    ("Groupe", group["libelle"]),
                    ("Matière", subject["matiere"]),
                    ("Stage", "5 séances de 2 heures"),
                    ("Année préparée", registry["anneeScolairePreparee"]),
                ],
                sources=eleve_sources,
                confidential=True,
                student=student["displayName"],
                module_key=module.key,
            ))

            # Corrigé enseignant, tenu à part.
            if subject.get("diagnosticId") is not None:
                bundles.append(Bundle(
                    filename=f"{label}{matiere_tag}_{student['slug']}_REMEDIATION_CORRIGE_ENSEIGNANT.pdf",
                    title="Plan de remédiation — corrigé",
                    subtitle=f"{student['displayName']} — {subject['matiere']}",
                    audience="enseignant",
                    directory="enseignant",
                    meta=[
                        ("Élève", student["displayName"]),
                        ("Matière", subject["matiere"]),
                        ("Usage", "Enseignant uniquement"),
                    ],
                    sources=[documents["remediation_prof"]],
                    confidential=True,
                    toc=False,
                    student=student["displayName"],
                    module_key=module.key,
                ))

    for key, module in MODULES.items():
        label = "Tle_SPE" if key == "tle_spe" else "Tle_NSI"
        sources_dir = "07_SOURCES" if key == "tle_nsi" else "05_SOURCES"
        supports = "SUPPORTS_Pratiques" if key == "tle_nsi" else "SUPPORTS_Manipulation"

        # Une séance est l'unité de travail réelle de l'enseignant : il prépare la séance 3,
        # pas « le module ». Sans ces fichiers, il faudrait imprimer un pack de cent pages ou
        # extraire des plages de pages à la main.
        for number, theme in module.sessions:
            folder = ROOT / key / "02_SEANCES" / f"S{number}"

            bundles.append(Bundle(
                filename=f"{label}_S{number}_PREPARATION_ENSEIGNANT.pdf",
                title=f"Séance {number} — préparation",
                subtitle=f"{module.label} · {theme}",
                audience="enseignant",
                directory="enseignant/seances",
                meta=[
                    ("Module", module.label),
                    ("Séance", f"{number} sur 5 — {theme}"),
                    ("Contenu", "Fiche professeur, supports, cartes d'aide"),
                    ("Durée", "2 heures"),
                ],
                sources=[
                    folder / f"{key}_S{number}_PROF_Fiche.md",
                    folder / f"{key}_S{number}_{supports}.md",
                    folder / f"{key}_S{number}_AIDES_Cartes.md",
                ],
                module_key=key,
            ))

            bundles.append(Bundle(
                filename=f"{label}_S{number}_FICHE_ELEVE.pdf",
                title=f"Séance {number}",
                subtitle=f"{module.label} · {theme}",
                audience="eleve",
                directory="seances",
                meta=[
                    ("Module", module.label),
                    ("Séance", f"{number} sur 5 — {theme}"),
                    ("Durée", "2 heures"),
                    ("Usage", "Un exemplaire par élève"),
                ],
                sources=[folder / f"{key}_S{number}_ELEVE_Activite.md"],
                toc=False,
                module_key=key,
            ))

        bundles.append(Bundle(
            filename=f"{label}_PACK_ELEVE_SEANCES.pdf",
            title="Fiches élèves des cinq séances",
            subtitle=module.label,
            audience="eleve",
            directory="seances",
            meta=[
                ("Module", module.label),
                ("Contenu", "5 fiches de séance, évaluations, portfolio"),
                ("Usage", "À photocopier pour le groupe"),
            ],
            sources=[
                *session_sheets(module, "eleve"),
                *evaluation_sheets(module, "eleve"),
                *portfolio_sheets(module),
            ],
            module_key=key,
        ))

        bundles.append(Bundle(
            filename=f"{label}_PACK_ENSEIGNANT_COMPLET.pdf",
            title="Pack enseignant complet",
            subtitle=module.label,
            audience="enseignant",
            directory="enseignant",
            meta=[
                ("Module", module.label),
                ("Contenu", "Programme, guide, fiches professeur, supports, corrigés, tableau de bord"),
                ("Usage", "Enseignant uniquement — contient les corrigés et des données nominatives"),
            ],
            sources=[
                ROOT / key / sources_dir / module.source_document,
                ROOT / key / "01_ENSEIGNANT" / f"{key}_Guide_Formateur.md",
                *([ROOT / key / "01_ENSEIGNANT" / f"{key}_Option_Maths_Expertes.md"]
                  if key == "tle_spe" else []),
                *session_sheets(module, "enseignant"),
                *support_sheets(module),
                *evaluation_sheets(module, "enseignant"),
                ROOT / key / "01_ENSEIGNANT" / f"{key}_Tableau_Bord_Enseignant.md",
            ],
            confidential=True,
            module_key=key,
        ))

    return bundles


def write_manifest(bundles: list[Bundle]) -> Path:
    target = OUTPUT_DIR / "MANIFEST_TERMINALE.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "fichier", "module", "destinataire", "eleve", "confidentiel",
            "documents_assembles", "pages", "octets",
        ])
        for bundle in sorted(bundles, key=lambda b: (b.directory, b.filename)):
            writer.writerow([
                f"{bundle.directory}/{bundle.filename}",
                bundle.module_key,
                bundle.audience,
                bundle.student,
                "oui" if bundle.confidential else "non",
                len(bundle.sources),
                bundle.pages,
                bundle.size_bytes,
            ])
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", choices=sorted(MODULES), help="ne traiter qu'un module")
    parser.add_argument("--list", action="store_true", help="lister les PDF sans les rendre")
    args = parser.parse_args(argv)

    try:
        bundles = plan_bundles()
    except (OSError, ValueError, KeyError) as error:
        print(f"ÉCHEC : sources illisibles — {error}")
        return 1
    if args.module:
        bundles = [bundle for bundle in bundles if bundle.module_key == args.module]

    if args.list:
        for bundle in sorted(bundles, key=lambda b: (b.directory, b.filename)):
            print(f"{bundle.directory}/{bundle.filename}  "
                  f"({len(bundle.sources)} document(s), {bundle.audience})")
        print(f"\n{len(bundles)} PDF à produire.")
        return 0

    try:
        check_tooling()
        for bundle in bundles:
            target = render(bundle)
            print(f"  {target.relative_to(ROOT)}  ({bundle.pages} p., "
                  f"{bundle.size_bytes // 1024} Kio)")
        manifest = write_manifest(bundles)
    except (PdfBuildError, subprocess.CalledProcessError) as error:
        print(f"ÉCHEC : {error}")
        return 1

    print(f"\n{len(bundles)} PDF écrits sous {OUTPUT_DIR.relative_to(ROOT)}/")
    print(f"Manifeste : {manifest.relative_to(ROOT)}")

    # Une notation restée en Unicode ne fait pas échouer la compilation : elle produit un
    # caractère absent de la police, donc une consigne trouée. Il faut la voir.
    alerts = sorted({warning for bundle in bundles for warning in bundle.warnings})
    if alerts:
        print(f"\n{len(alerts)} document(s) à convertir en notation LaTeX :")
        for alert in alerts:
            print(f"  {alert}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
