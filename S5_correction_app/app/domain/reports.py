# -*- coding: utf-8 -*-
"""Rapports : blocs éditables, rendu LaTeX, compilation PDF, manifeste.

Quatre documents, produits sans le moindre appel réseau :

    BILAN_PARENTS         3 à 4 pages, sans jargon, sans identifiant technique
    SYNTHESE_ENSEIGNANT   technique, critère par critère
    PLAN_RENTREE          une page, quatre semaines
    FICHE_ELEVE           langage élève, deux objectifs

Chaque bloc textuel porte sa provenance et son état d'approbation. Une régénération ne
remplace jamais un bloc qu'un humain a modifié et approuvé : elle le laisse en place et
le signale.
"""

import datetime as dt
import json
import re
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from .. import config
from ..models import Report, ReportBlock, ReportBlockHistory
from ..security import SecurityError, run_command, safe_slug, sha256_file
from . import correction as corr
from . import narrative, points

TEMPLATE_VERSION = "1.0.0"

REPORT_TYPES = {
    "BILAN_PARENTS": {
        "label": "Bilan parents",
        "template": "bilan_parents.tex.j2",
        "prefix": "BILAN_PARENTS",
        "audience": "familles",
    },
    "SYNTHESE_ENSEIGNANT": {
        "label": "Synthèse enseignant",
        "template": "synthese_enseignant.tex.j2",
        "prefix": "SYNTHESE_ENSEIGNANT",
        "audience": "enseignant",
    },
    "PLAN_RENTREE": {
        "label": "Plan des quatre semaines",
        "template": "plan_4_semaines.tex.j2",
        "prefix": "PLAN_RENTREE_4_SEMAINES",
        "audience": "familles",
    },
    "FICHE_ELEVE": {
        "label": "Fiche élève",
        "template": "fiche_eleve.tex.j2",
        "prefix": "FICHE_ELEVE",
        "audience": "élève",
    },
}

BLOCK_KIND = {"BILAN_PARENTS": "bilan_parents",
              "SYNTHESE_ENSEIGNANT": "synthese_enseignant",
              "PLAN_RENTREE": "plan_rentree",
              "FICHE_ELEVE": "fiche_eleve"}


class ReportError(Exception):
    pass


# ------------------------------------------------------------------- LaTeX
_LATEX_ESCAPES = {
    "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "$": r"\$", "&": r"\&",
    "#": r"\#", "_": r"\_", "%": r"\%", "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def latex_escape(value) -> str:
    """Aucun texte saisi par un humain n'atteint LaTeX sans passer par ici."""
    if value is None:
        return ""
    text = str(value)
    out = []
    for char in text:
        out.append(_LATEX_ESCAPES.get(char, char))
    text = "".join(out)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{2,}", r"\\par ", text)
    text = text.replace("\n", r"\\ ")
    return text


def _environment() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(config.LATEX_DIR)),
        block_start_string=r"\BLOCK{", block_end_string="}",
        variable_start_string=r"\VAR{", variable_end_string="}",
        comment_start_string=r"\#{", comment_end_string="}",
        line_statement_prefix="%%#", trim_blocks=True, lstrip_blocks=True,
        autoescape=False, undefined=StrictUndefined,
    )
    env.filters["esc"] = latex_escape
    return env


# ------------------------------------------------------------------- blocs
def _context(session, assessment, correction, analysis, plan, delayed):
    student = assessment.student
    display = student.person.display_name
    first_name = display.split(" ")[0].capitalize() if display else "L'élève"
    subject_phrase = ("mathématiques" if assessment.subject.lower().startswith("math")
                      else assessment.subject)
    observations = []
    for key, label in corr.GENERAL_OBSERVATION_FIELDS:
        value = json.loads(correction.general_observations_json or "{}").get(key)
        if value:
            observations.append({"key": key, "label": label, "value": value})
    return {
        "analysis": analysis, "plan": plan, "delayed": delayed,
        "first_name": first_name, "display_name": display,
        "subject_phrase": subject_phrase,
        "level_label": student.level_label, "subject": assessment.subject,
        "observations": observations,
    }


def build_blocks(kind: str, ctx: dict, generator_name: str = "deterministic"):
    generator = narrative.get_generator(generator_name)
    return generator.blocks(BLOCK_KIND[kind], ctx), generator.name


def ensure_report(session, assessment, correction, analysis, plan, delayed,
                  report_type: str, regenerate: bool = False,
                  generator_name: str = "deterministic") -> Report:
    """Crée ou met à jour un rapport. Les blocs approuvés par un humain sont préservés."""
    if report_type not in REPORT_TYPES:
        raise ReportError("type de rapport inconnu : %s" % report_type)
    if correction.status not in ("VALIDATED", "REPORT_READY", "REPORT_APPROVED"):
        raise ReportError("la correction doit être validée avant toute génération de bilan.")

    existing = (session.query(Report)
                .filter_by(assessment_id=assessment.assessment_id, report_type=report_type)
                .order_by(Report.version.desc()).first())
    ctx = _context(session, assessment, correction, analysis, plan, delayed)
    blocks, source = build_blocks(report_type, ctx, generator_name)

    if existing is None:
        report = Report(assessment_id=assessment.assessment_id,
                        correction_id=correction.correction_id, report_type=report_type,
                        version=1, status="DRAFT",
                        analysis_sha256=analysis["analysis_sha256"],
                        template_version=TEMPLATE_VERSION)
        session.add(report)
        session.flush()
        for position, (key, title, content) in enumerate(blocks, start=1):
            session.add(ReportBlock(report_id=report.report_id, block_key=key,
                                    position=position, title=title, content=content,
                                    source=source, approved=False))
        corr.audit(session, "report.created", "report", report.report_id,
                   assessment.assessment_id, new_value="%s v1" % report_type)
        session.flush()
        return report

    if existing.status == "APPROVED" and regenerate:
        report = Report(assessment_id=assessment.assessment_id,
                        correction_id=correction.correction_id, report_type=report_type,
                        version=existing.version + 1, status="DRAFT",
                        analysis_sha256=analysis["analysis_sha256"],
                        template_version=TEMPLATE_VERSION)
        session.add(report)
        session.flush()
        approved = {b.block_key: b for b in existing.blocks if b.approved}
        for position, (key, title, content) in enumerate(blocks, start=1):
            kept = approved.get(key)
            session.add(ReportBlock(
                report_id=report.report_id, block_key=key, position=position, title=title,
                content=kept.content if kept else content,
                source=kept.source if kept else source,
                approved=bool(kept)))
        corr.audit(session, "report.version", "report", report.report_id,
                   assessment.assessment_id, old_value="v%d" % existing.version,
                   new_value="v%d" % report.version,
                   reason="régénération après approbation ; les blocs approuvés sont conservés")
        session.flush()
        return report

    report = existing
    report.correction_id = correction.correction_id
    report.analysis_sha256 = analysis["analysis_sha256"]
    report.template_version = TEMPLATE_VERSION
    current = {b.block_key: b for b in report.blocks}
    kept = []
    for position, (key, title, content) in enumerate(blocks, start=1):
        block = current.get(key)
        if block is None:
            session.add(ReportBlock(report_id=report.report_id, block_key=key,
                                    position=position, title=title, content=content,
                                    source=source, approved=False))
            continue
        block.position = position
        block.title = title
        if block.approved or block.source == "human":
            kept.append(key)
            continue
        if regenerate or block.content != content:
            if block.content:
                session.add(ReportBlockHistory(report_id=report.report_id, block_key=key,
                                               content=block.content, source=block.source))
            block.content = content
            block.source = source
    if kept:
        corr.audit(session, "report.regenerated", "report", report.report_id,
                   assessment.assessment_id,
                   new_value="blocs conservés car modifiés par un humain : %s" % ", ".join(kept))
    session.flush()
    return report


def edit_block(session, report: Report, block_key: str, content: str, approve: bool = True):
    block = next((b for b in report.blocks if b.block_key == block_key), None)
    if block is None:
        raise ReportError("bloc inconnu : %s" % block_key)
    if block.content:
        session.add(ReportBlockHistory(report_id=report.report_id, block_key=block_key,
                                       content=block.content, source=block.source))
    block.content = (content or "").strip()
    block.source = "human"
    block.approved = bool(approve)
    corr.audit(session, "report.block_edited", "report_block",
               "%s/%s" % (report.report_id, block_key), report.assessment_id,
               new_value="source=human approved=%s" % block.approved)
    return block


# ------------------------------------------------------------------- rendu
def _pct(value):
    if value is None:
        return "---"
    return ("%.0f" % float(value)).replace(".", ",") + r"\,\%"


def _scope_badge(scope):
    return {"n_minus_1": "[N--1]", "bridge_n": "[PASSERELLE N]",
            "mixed": "[MIXTE]"}.get(scope, "[?]")


def _error_rows(analysis):
    n1 = list(analysis["error_profile"]["n_minus_1"].items())
    br = list(analysis["error_profile"]["bridge_n"].items())
    rows = []
    for i in range(max(len(n1), len(br), 1)):
        a = n1[i] if i < len(n1) else ("---", "")
        b = br[i] if i < len(br) else ("---", "")
        rows.append({"n1_code": a[0], "n1_count": a[1], "br_code": b[0], "br_count": b[1]})
    return rows


def _domain_table(analysis):
    rows = []
    seen = set()
    for s in analysis["skills"]:
        if s["curriculum_scope"] != "n_minus_1":
            continue
        domain = s["domain"] or "Autres"
        if domain in seen:
            continue
        seen.add(domain)
        initial = {"acquis": "point d'appui", "en_voie_acquisition": "en cours d'acquisition",
                   "fragile": "point de vigilance",
                   "non_evalue": "non documenté"}.get(
            s["baseline_status_qualitative"], "non documenté")
        rows.append({"domain": latex_escape(domain), "initial": latex_escape(initial),
                     "final": latex_escape(s["status_label"].lower())})
    return rows[:8]


class _Blocks(dict):
    """Un bloc absent vaut la chaîne vide : un gabarit ne doit pas casser pour si peu."""

    def __missing__(self, key):
        return ""


def render_tex(report: Report, assessment, analysis, plan) -> str:
    spec = REPORT_TYPES[report.report_type]
    env = _environment()
    template = env.get_template(spec["template"])
    blocks = _Blocks((b.block_key, latex_escape(b.content)) for b in report.blocks)
    student = assessment.student
    header = {
        "student_name": latex_escape(student.person.display_name),
        "level_label": latex_escape(student.level_label),
        "subject": latex_escape(assessment.subject),
        "generated_on": dt.date.today().strftime("%d/%m/%Y"),
    }
    observations = [{"label": latex_escape(o["label"]), "value": latex_escape(o["value"])}
                    for o in _observations_of(report, assessment)]
    return template.render(
        h=header, a=analysis, plan=plan, blocks=blocks,
        pct=_pct, scope_badge=_scope_badge, centi=points.format_fr,
        error_rows=_error_rows(analysis), domain_table=_domain_table(analysis),
        observations=observations)


def _observations_of(report, assessment):
    correction = next((c for c in assessment.corrections
                       if c.correction_id == report.correction_id), None)
    if correction is None:
        return []
    data = json.loads(correction.general_observations_json or "{}")
    return [{"label": label, "value": data[key]}
            for key, label in corr.GENERAL_OBSERVATION_FIELDS if data.get(key)]


# -------------------------------------------------------------- compilation
def output_basename(report_type: str, assessment) -> str:
    """Nom sûr, sans collision entre deux matières d'une même personne."""
    spec = REPORT_TYPES[report_type]
    student = assessment.student
    name = safe_slug(student.person.display_name)
    subject = safe_slug(assessment.subject)[:4]
    siblings = [s for s in student.person.students]
    suffix = "_%s" % subject if len(siblings) > 1 else ""
    return "%s_%s%s" % (spec["prefix"], name, suffix)


def compile_pdf(report: Report, tex_source: str, assessment) -> dict:
    """Compile le LaTeX. En cas d'échec, le .tex est conservé et le rapport n'est pas généré."""
    config.ensure_runtime()
    basename = output_basename(report.report_type, assessment)
    work = Path(config.BUILD_DIR) / ("%s_v%d" % (basename, report.version))
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    shutil.copy2(config.LATEX_DIR / "nexus_bilan.sty", work / "nexus_bilan.sty")
    tex_path = work / ("%s.tex" % basename)
    tex_path.write_text(tex_source, encoding="utf-8")

    engine = config.LATEX_ENGINE
    if not shutil.which(engine):
        return {"ok": False, "tex_path": str(tex_path),
                "error": "le moteur LaTeX « %s » est introuvable sur cette machine." % engine,
                "stdout": "", "stderr": "", "returncode": None}
    argv = [engine, "-interaction=nonstopmode", "-halt-on-error",
            "-file-line-error", "%s.tex" % basename]
    last = None
    try:
        for _ in range(2):        # deux passes : \pageref{LastPage}
            last = run_command(argv, work, config.LATEX_TIMEOUT_SECONDS)
            if last.returncode != 0:
                break
    except (SecurityError, OSError) as exc:
        return {"ok": False, "tex_path": str(tex_path), "error": str(exc),
                "stdout": "", "stderr": "", "returncode": None}
    except Exception as exc:      # timeout compris : on ne masque rien
        return {"ok": False, "tex_path": str(tex_path), "error": str(exc),
                "stdout": "", "stderr": "", "returncode": None}

    pdf_src = work / ("%s.pdf" % basename)
    if last.returncode != 0 or not pdf_src.exists():
        return {"ok": False, "tex_path": str(tex_path),
                "error": "la compilation LaTeX a échoué ; le fichier .tex est conservé.",
                "stdout": (last.stdout or "")[-4000:], "stderr": (last.stderr or "")[-2000:],
                "returncode": last.returncode}

    target_dir = Path(config.REPORTS_DIR) / assessment.student_id
    target_dir.mkdir(parents=True, exist_ok=True)
    pdf_target = target_dir / ("%s_v%d.pdf" % (basename, report.version))
    tex_target = target_dir / ("%s_v%d.tex" % (basename, report.version))
    shutil.copy2(pdf_src, pdf_target)
    shutil.copy2(tex_path, tex_target)
    return {"ok": True, "pdf_path": str(pdf_target), "tex_path": str(tex_target),
            "pdf_sha256": sha256_file(pdf_target), "stdout": "", "stderr": "",
            "returncode": 0}


def write_manifest(report: Report, assessment, result: dict) -> str:
    target_dir = Path(result["pdf_path"]).parent
    manifest = {
        "document_id": "%s-v%d-%s" % (report.report_type, report.version,
                                      assessment.assessment_id),
        "student_id": assessment.student_id,
        "assessment_id": assessment.assessment_id,
        "report_type": report.report_type,
        "correction_revision": next((c.revision for c in assessment.corrections
                                     if c.correction_id == report.correction_id), None),
        "analysis_sha256": report.analysis_sha256,
        "template_version": report.template_version,
        "generated_at": dt.datetime.now().astimezone().isoformat(),
        "pdf_sha256": result["pdf_sha256"],
        "pdf_path": str(Path(result["pdf_path"]).name),
    }
    path = target_dir / ("%s.manifest.json" % Path(result["pdf_path"]).stem)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    return str(path)
