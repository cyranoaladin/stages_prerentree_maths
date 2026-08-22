# -*- coding: utf-8 -*-
"""Rendu du bilan longitudinal : contexte du gabarit, contrôle, compilation.

L'ordre est celui-ci, et il n'est pas négociable : on rend le texte, **on le
contrôle**, et seulement ensuite on compile. Un document qui laisse fuiter un
identifiant technique ou qui annonce une progression chiffrée ne doit pas exister
sous forme de PDF : à ce stade, il serait déjà transmissible.
"""

import json
import shutil
import subprocess
from pathlib import Path

from ... import config
from .. import reports as reports_module
from . import guard as guard_module
from . import narrative as narrative_module

TEMPLATE = "bilan_longitudinal_parents.tex.j2"
TEMPLATE_VERSION = "1.0.0"

_FINAL_LABELS = {
    "SOLIDE": "solide", "SATISFAISANT": "satisfaisant",
    "A_CONSOLIDER": "à consolider", "PRIORITAIRE": "prioritaire",
    "A_CONFIRMER": "à confirmer", "PREUVE_INSUFFISANTE": "éléments insuffisants",
    None: "non évalué par ce sujet",
}


def build_context(facts: dict, blocks=None) -> dict:
    """Contexte du gabarit. Aucun identifiant technique n'y entre."""
    blocs = dict((cle, contenu) for cle, _, contenu in (blocks or
                                                        narrative_module.parent_blocks(facts)))
    # Le gabarit est rendu en StrictUndefined : une section absente doit exister
    # comme chaîne vide, sinon un dossier sans point à consolider fait échouer la
    # compilation. Les sections conditionnelles se testent alors naturellement.
    for cle in ("essentiel", "objectifs_stage", "situation_depart", "fil_conducteur",
                "travail_realise", "score_brut", "consolidation", "passerelles",
                "points_forts", "points_consolider", "a_confirmer", "non_evaluees",
                "conseil"):
        blocs.setdefault(cle, "")
    listes = {cle: [l[2:] for l in contenu.splitlines() if l.startswith("— ")]
              for cle, contenu in blocs.items() if contenu.startswith("— ")}
    for cle in ("points_forts", "points_consolider", "a_confirmer", "non_evaluees"):
        listes.setdefault(cle, [])

    domaines = []
    for domaine in facts["domains"]:
        etat = _FINAL_LABELS.get(domaine["final_status"], "non évalué par ce sujet")
        if domaine["skills_without_final_evidence"]:
            # Formulation brève : la colonne fait 44 mm, et la phrase longue y
            # occupait quatre lignes à chaque domaine concerné.
            nombre = domaine["skills_without_final_evidence"]
            etat += (" — %d compétence%s non mesurée%s par ce sujet"
                     % (nombre, "s" if nombre > 1 else "", "s" if nombre > 1 else ""))
        domaines.append({**domaine, "final_label": etat})

    # Les priorités reprennent le libellé de la compétence, pas la phrase entière de
    # l'objectif : celle-ci figure déjà dans le tableau du plan, et la répéter en
    # pied de page coûtait une page complète.
    priorites = []
    for entree in facts["four_week_plan"]["priorities"][:3]:
        libelle = (entree.get("label") or "").rstrip(".")
        domaine = entree.get("domain")
        priorites.append("%s%s" % (libelle, " (%s)" % domaine if domaine else ""))
    if not priorites:
        priorites = [o["objective"] for s in facts["four_week_plan"]["weeks"][:2]
                     for o in s["objectives"][:1]][:3]

    etudiant = facts["student"]
    return {
        "student_name": etudiant["display_name"],
        "level_label": etudiant["level_label"],
        "subject": etudiant["subject"],
        "school_year": "2026-2027",
        "blocks": blocs,
        "lists": listes,
        "sessions": facts["stage_trajectory"]["sessions"],
        "domains": domaines,
        "weeks": facts["four_week_plan"]["weeks"],
        "plan_mode_note": facts["four_week_plan"]["mode_note"],
        "priorities": priorites,
        # Deux réserves suffisent en pied de document ; la liste complète reste
        # dans les faits, et la synthèse enseignant la porte intégralement.
        "limits": facts["interpretation_limits"][:2],
    }


def render_tex(facts: dict, blocks=None) -> str:
    env = reports_module._environment()
    return env.get_template(TEMPLATE).render(**build_context(facts, blocks))


def render_and_check(facts: dict, blocks=None) -> dict:
    """Rend le document et le soumet au contrôle. Ne compile rien."""
    blocs = blocks or narrative_module.parent_blocks(facts)
    tex = render_tex(facts, blocs)
    # Le contrôle porte sur le texte rédigé, pas sur le LaTeX : les commandes de
    # mise en forme ne sont pas du contenu et n'ont pas à être inspectées.
    texte = "\n".join(contenu for _, _, contenu in blocs)
    controle = guard_module.validate(texte, facts.get("skills"), "parents")
    return {"tex": tex, "blocks": blocs, "validation": controle}


def compile_pdf(facts: dict, basename: str, blocks=None, work_dir=None) -> dict:
    """Contrôle puis compile. Un document refusé au contrôle n'est jamais compilé."""
    rendu = render_and_check(facts, blocks)
    if not rendu["validation"]["ok"]:
        return {"ok": False, "reason": "le texte n'a pas passé le contrôle de langue",
                "validation": rendu["validation"], "pdf_path": None, "tex_path": None}

    config.ensure_runtime()
    travail = Path(work_dir or config.BUILD_DIR) / basename
    if travail.exists():
        shutil.rmtree(travail)
    travail.mkdir(parents=True)
    shutil.copy2(config.LATEX_DIR / "nexus_bilan.sty", travail / "nexus_bilan.sty")
    chemin_tex = travail / ("%s.tex" % basename)
    chemin_tex.write_text(rendu["tex"], encoding="utf-8")

    moteur = getattr(config, "LATEX_ENGINE", "lualatex")
    if not shutil.which(moteur):
        return {"ok": False, "reason": "aucun moteur LaTeX disponible (%s)" % moteur,
                "validation": rendu["validation"], "tex_path": str(chemin_tex),
                "pdf_path": None}

    journal = ""
    for _ in range(2):
        acheve = subprocess.run(
            [moteur, "-interaction=nonstopmode", "-halt-on-error", chemin_tex.name],
            cwd=str(travail), shell=False, capture_output=True,
            encoding="utf-8", errors="replace")
        journal = acheve.stdout or ""
        if acheve.returncode != 0:
            return {"ok": False, "reason": "la compilation LaTeX a échoué",
                    "validation": rendu["validation"], "tex_path": str(chemin_tex),
                    "pdf_path": None, "log": journal[-2500:]}
    chemin_pdf = travail / ("%s.pdf" % basename)
    return {"ok": chemin_pdf.exists(), "validation": rendu["validation"],
            "tex_path": str(chemin_tex),
            "pdf_path": str(chemin_pdf) if chemin_pdf.exists() else None,
            "pdf_sha256": _sha256(chemin_pdf) if chemin_pdf.exists() else None}


def _sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(str(path), "rb") as f:
        for bloc in iter(lambda: f.read(1 << 16), b""):
            h.update(bloc)
    return h.hexdigest()


def write_manifest(facts: dict, resultat: dict, destination) -> str:
    """REPORT_MANIFEST.json — ce qui a été lu, et ce qui a été produit."""
    manifeste = {
        "schema": "nexus-longitudinal-report-manifest-v1",
        "student_id": facts["student"]["student_id"],
        "assessment_id": facts.get("assessment_id"),
        "correction_revision": facts["final_assessment"]["correction_revision"],
        "report_version": TEMPLATE_VERSION,
        "facts_sha256": facts.get("facts_sha256"),
        "analysis_sha256": facts.get("analysis_sha256"),
        "pdf_sha256": resultat.get("pdf_sha256"),
        "diagnostic_sources": [s for s in facts["sources"]
                               if s["role"] in ("initial_diagnostic_instrument",
                                                "individual_dossier", "learning_profile")],
        "session_sources": [s for s in facts["sources"]
                            if s["role"] in ("session_material",
                                             "personalised_session_dossier")],
        "missing_sources": [s for s in facts["sources"] if not s["present"]],
    }
    chemin = Path(destination)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps(manifeste, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    return str(chemin)
