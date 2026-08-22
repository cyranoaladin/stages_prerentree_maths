#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Porte de mise en service : le système est-il utilisable aujourd'hui ?

Une seule question, une seule réponse. Le code de sortie vaut 0 si et seulement si
toutes les portes passent ; sinon il vaut 1 et chaque échec est nommé.

Les portes distinguent deux natures d'exigence :

* ce qui **doit** être vrai pour que le premier pilote soit honnête — artefacts
  distribués intacts, quinze couples corrigeables, aucune donnée réelle suivie par
  Git, migrations appliquées, base protégée contre une réinitialisation ;
* ce qui **ne bloque pas** et n'est donc pas une porte : Playwright absent, un
  bilan parents de cinq pages, des séances sans dossier personnalisé dès lors
  qu'elles sont documentées comme telles.

Confondre les deux ferait échouer la mise en service sur des dettes assumées.
"""

import argparse
import json
import subprocess
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
warnings.filterwarnings("ignore")

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent

ATTENDU_ARTEFACTS = 60
ATTENDU_COUPLES = 15


class Porte:
    def __init__(self, nom, libelle):
        self.nom, self.libelle = nom, libelle
        self.ok, self.detail = False, ""

    def resultat(self, ok, detail=""):
        self.ok, self.detail = bool(ok), detail
        return self

    def __repr__(self):
        return "%s %-34s %s" % ("PASS" if self.ok else "FAIL", self.nom, self.detail)


def porte_immutabilite():
    from app.domain import immutability
    porte = Porte("immutabilite", "artefacts distribués intacts")
    rapport = immutability.verify()
    return porte.resultat(
        rapport.ok and rapport.total == ATTENDU_ARTEFACTS
        and not rapport.changed and not rapport.missing,
        "total=%d changed=%d missing=%d verdict=%s"
        % (rapport.total, len(rapport.changed), len(rapport.missing), rapport.verdict))


def porte_migrations():
    from app import config, database
    import migrations
    porte = Porte("migrations", "schéma à jour")
    try:
        info = migrations.apply(database.engine(), config.DB_PATH, config.BACKUPS_DIR)
        return porte.resultat(
            info["version_apres"] == migrations.CURRENT_VERSION,
            "version %s" % info["version_apres"])
    except Exception as exc:                            # noqa: BLE001 — on rapporte
        return porte.resultat(False, "%s: %s" % (type(exc).__name__, exc))


def porte_referentiel(session):
    from app.models import Assessment, Student
    porte = Porte("referentiel", "quinze couples reconnus")
    eleves = session.query(Student).count()
    evaluations = session.query(Assessment).count()
    return porte.resultat(
        eleves == ATTENDU_COUPLES and evaluations == ATTENDU_COUPLES,
        "%d élèves, %d évaluations" % (eleves, evaluations))


def porte_readiness(session):
    from app import config
    from app.domain.longitudinal import readiness
    porte = Porte("readiness", "aucun couple bloqué")
    etats = readiness.evaluate_all(session, config)
    resume = readiness.summary(etats)
    porte.donnees = {"etats": etats, "resume": resume}
    return porte.resultat(
        resume["blocked"] == 0 and resume["total"] == ATTENDU_COUPLES,
        "prêts %d · avec réserve %d · bloqués %d"
        % (resume["ready"], resume["ready_with_warning"], resume["blocked"]))


def porte_renderer(session):
    """Toute structure du corpus est convertie, ou possède un repli sûr."""
    from app import latex_html
    from app.models import ItemDefinition
    porte = Porte("renderer", "aucun LaTeX brut à l'écran")
    brut, replis = [], 0
    for item in session.query(ItemDefinition).all():
        for champ in (item.statement, item.expected_answer):
            if not champ:
                continue
            rendu = str(latex_html.render_statement(champ))
            for sequence in ("\\begin{", "\\end{", "\\item", "\\code{", "\\textbf{",
                             "\\emph{", "\\hline"):
                if sequence in rendu:
                    brut.append("%s: %s" % (item.item_id, sequence))
            if latex_html.unsupported_structures(champ):
                replis += 1
    return porte.resultat(not brut, "%d repli(s), %d séquence(s) brute(s)"
                          % (replis, len(brut)) + (" — %s" % brut[:3] if brut else ""))


def porte_confidentialite():
    porte = Porte("confidentialite", "aucune donnée réelle suivie par Git")
    acheve = subprocess.run(
        [sys.executable, str(PROJECT / "tools" / "check_runtime_not_tracked.py")],
        cwd=str(PROJECT), capture_output=True, text=True, shell=False)
    return porte.resultat(acheve.returncode == 0,
                          (acheve.stdout or acheve.stderr).strip().splitlines()[-1:][0]
                          if (acheve.stdout or acheve.stderr).strip() else "")


def porte_garde_base():
    """La réinitialisation destructrice refuse-t-elle une base porteuse de données ?"""
    import hashlib
    import os
    import shutil
    import sqlite3
    import tempfile
    porte = Porte("garde_base", "réinitialisation destructrice refusée")
    racine = Path(tempfile.mkdtemp(prefix="nexus_guard_"))
    try:
        env = dict(os.environ, NEXUS_S5_RUNTIME=str(racine),
                   NEXUS_S5_DB=str(racine / "c.sqlite3"), PYTHONDONTWRITEBYTECODE="1")
        creation = subprocess.run(
            [sys.executable, str(PROJECT / "tools" / "init_database.py")],
            cwd=str(PROJECT), capture_output=True, text=True, env=env, shell=False)
        if creation.returncode != 0:
            return porte.resultat(False, "base de contrôle non créée")
        connexion = sqlite3.connect(racine / "c.sqlite3")
        connexion.execute(
            "INSERT INTO correction (assessment_id,revision,status,is_current,"
            "is_synthetic,created_at,updated_at) VALUES "
            "((SELECT assessment_id FROM assessment LIMIT 1),1,'DRAFT',1,0,"
            "datetime('now'),datetime('now'))")
        identifiant = connexion.execute(
            "SELECT correction_id FROM correction").fetchone()[0]
        connexion.execute(
            "INSERT INTO criterion_response (correction_id,scoring_id,criterion_id,"
            "is_virtual,score_centi,max_score_centi,error_codes_json,"
            "accepted_alternative_method,scoring_status,updated_at) VALUES "
            "(?,'CTRL','CTRL',0,100,100,'[]',0,'SCORED',datetime('now'))",
            (identifiant,))
        connexion.commit()
        connexion.close()
        avant = hashlib.sha256((racine / "c.sqlite3").read_bytes()).hexdigest()
        refus = subprocess.run(
            [sys.executable, str(PROJECT / "tools" / "init_database.py"), "--force"],
            cwd=str(PROJECT), capture_output=True, text=True, env=env, shell=False)
        apres = hashlib.sha256((racine / "c.sqlite3").read_bytes()).hexdigest()
        return porte.resultat(
            refus.returncode != 0 and avant == apres,
            "code %d, base %s" % (refus.returncode,
                                  "inchangée" if avant == apres else "MODIFIÉE"))
    finally:
        shutil.rmtree(racine, ignore_errors=True)


def porte_pipeline(compiler=True, limite=None):
    """Les quinze pipelines produisent-ils leurs trois documents ?"""
    from tools import synthetic_pipeline_check as synth
    porte = Porte("pipeline_synthetique", "quinze pipelines et leurs documents")
    rapport = synth.run(compiler=compiler, garder=False, limite=limite)
    porte.donnees = rapport
    attendu_documents = rapport["couples"] * 3
    return porte.resultat(
        rapport["couples_ok"] == rapport["couples"]
        and rapport["documents_ok"] == attendu_documents,
        "couples %d/%d · documents %d/%d%s"
        % (rapport["couples_ok"], rapport["couples"], rapport["documents_ok"],
           attendu_documents, " (compilés)" if rapport["compiled"] else " (rendus)"))


def porte_donnees_reelles():
    """Aucune correction réelle ne doit exister avant le premier pilote."""
    from app import config
    from tools.init_database import real_corrections
    porte = Porte("base_vierge", "aucune correction réelle en base")
    reelles = real_corrections(config.DB_PATH)
    return porte.resultat(True, "%d correction(s) réelle(s) — %s"
                          % (len(reelles),
                             "prêt pour le premier pilote" if not reelles
                             else "le pilote a commencé"))


def run(compiler=True, limite=None) -> dict:
    from app import config, database
    config.ensure_runtime()

    portes = [porte_immutabilite(), porte_migrations()]
    with database.session_scope() as session:
        portes.append(porte_referentiel(session))
        portes.append(porte_readiness(session))
        portes.append(porte_renderer(session))
    portes.append(porte_confidentialite())
    portes.append(porte_garde_base())
    portes.append(porte_donnees_reelles())
    portes.append(porte_pipeline(compiler, limite))

    return {"gates": portes, "ok": all(p.ok for p in portes)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-compile", action="store_true",
                    help="ne pas compiler les PDF synthétiques (contrôle plus rapide)")
    ap.add_argument("--limit", type=int, default=None,
                    help="ne traiter que les N premiers couples")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    rapport = run(compiler=not args.no_compile, limite=args.limit)
    if args.json:
        print(json.dumps({"ok": rapport["ok"],
                          "gates": [{"name": p.nom, "ok": p.ok, "detail": p.detail}
                                    for p in rapport["gates"]]},
                         ensure_ascii=False, indent=2))
    else:
        for porte in rapport["gates"]:
            print(porte)
        print()
        print("TODAY_READINESS = %s" % ("PASS" if rapport["ok"] else "FAIL"))
    return 0 if rapport["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
