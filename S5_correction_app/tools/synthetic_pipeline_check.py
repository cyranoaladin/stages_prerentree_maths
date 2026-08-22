#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle du pipeline complet sur les quinze couples, en données synthétiques.

Pour chaque couple élève × matière : remplir la copie, valider, analyser,
construire les faits longitudinaux, produire les trois documents, les compiler, et
contrôler leur langue. Puis détruire la fixture.

Deux précautions, qui ne sont pas décoratives :

* **la base réelle n'est jamais touchée.** Tout se passe dans un répertoire
  temporaire, et les corrections créées portent ``is_synthetic = True`` ;
* **les PDF produits ne rejoignent jamais ``runtime/reports``.** Ils sont écrits
  sous ``tmp/tests`` et supprimés à la fin, sauf demande explicite. Un bilan de
  test ne doit pas pouvoir être confondu avec un bilan d'élève.

Ce contrôle répond à une seule question : *le système saurait-il produire un bilan
pour n'importe lequel des quinze, aujourd'hui ?* Il ne dit rien des résultats des
élèves, qui n'existent pas encore.
"""

import argparse
import json
import shutil
import sys
import tempfile
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
warnings.filterwarnings("ignore")

PROJECT = Path(__file__).resolve().parents[1]
SORTIE_PAR_DEFAUT = PROJECT.parent / "tmp" / "tests" / "synthetic_reports"

TYPES = ("BILAN_PARENTS_LONGITUDINAL", "FICHE_ELEVE", "SYNTHESE_ENSEIGNANT")


def _isoler_runtime(racine: Path):
    """Bascule la configuration sur un runtime jetable, en mode fixtures.

    Le mode de données par défaut est REAL — volontairement protecteur : une copie
    d'élève ne s'ouvre pas sans authentification. Cet outil ne manipule aucune donnée
    réelle, et le déclare explicitement ; sans quoi toutes ses requêtes recevraient
    un refus d'authentification, et le contrôle échouerait sans rapport avec ce qu'il
    prétend mesurer.
    """
    from app import config, database
    for cle, valeur in (("RUNTIME_DIR", racine), ("DB_PATH", racine / "corrections.sqlite3"),
                        ("EXPORTS_DIR", racine / "exports"),
                        ("REPORTS_DIR", racine / "reports"),
                        ("BACKUPS_DIR", racine / "backups"),
                        ("BUILD_DIR", racine / "build"),
                        ("SOURCE_COPIES_DIR", racine / "source_copies"),
                        ("OCR_CACHE_DIR", racine / "ocr_cache"),
                        ("SECRETS_DIR", racine / "secrets")):
        setattr(config, cle, valeur)
    config.OPENROUTER_KEY_FILE = config.SECRETS_DIR / "openrouter.key"
    config.settings.data_mode = "SYNTHETIC"
    config.ensure_runtime()
    database.reset_engine()
    return config


def _remplir(client, database, student_id, motif) -> int:
    """Remplit une copie de façon synthétique. ``motif`` décide de chaque score."""
    from app.domain import correction as corr
    from app.models import Assessment

    client.get("/eleve/%s" % student_id)
    with database.session_scope() as session:
        assessment = session.query(Assessment).filter_by(student_id=student_id).one()
        courante = corr.current_correction(session, assessment.assessment_id)
        courante.is_synthetic = True            # §22 : la fixture se déclare
        lignes = [(r.scoring_id, r.max_score_centi, r.criterion_id)
                  for r in courante.responses]
    for index, (scoring_id, maximum, _) in enumerate(lignes):
        client.post("/eleve/%s/critere/%s" % (student_id, scoring_id),
                    json=motif(index, maximum))
    client.post("/eleve/%s/valider" % student_id, follow_redirects=False)
    return len(lignes)


def _motif_mixte(index, maximum):
    """Copie synthétique volontairement contrastée.

    Un plein score partout ne mettrait à l'épreuve ni les priorités, ni le profil
    d'erreurs, ni la sélection des points à consolider. On alterne donc, de façon
    déterministe, pour que chaque bilan produit ait de la matière à dire.
    """
    if index % 5 == 0:
        return {"score_centi": 0, "error_codes": ["CONCEPT"]}
    if index % 5 == 1:
        moitie = (maximum // 10) * 5
        return {"score_centi": moitie, "error_codes": ["CALCUL"]}
    return {"score_centi": maximum, "error_codes": []}


def _documents(session, assessment, correction, faits, dossier_sortie, compiler=True):
    """Produit les trois documents. Retourne un relevé par document."""
    from app.domain import analysis as ana
    from app.domain import reports as rep
    from app.domain.longitudinal import guard, narrative, render

    releves = []
    base = assessment.student_id.replace("-", "_").upper()

    # 1. Bilan parents longitudinal — le livrable de cette mise en service.
    blocs = narrative.parent_blocks(faits)
    if compiler:
        resultat = render.compile_pdf(faits, "BILAN_PARENTS_%s" % base, blocs,
                                      work_dir=dossier_sortie / "_build")
    else:
        rendu = render.render_and_check(faits, blocs)
        resultat = {"ok": rendu["validation"]["ok"], "validation": rendu["validation"],
                    "pdf_path": None}
    releves.append({"type": "BILAN_PARENTS_LONGITUDINAL", "ok": bool(resultat["ok"]),
                    "pdf": resultat.get("pdf_path"),
                    "violations": resultat.get("validation", {}).get("violations", []),
                    "reason": resultat.get("reason")})

    # 2 et 3. Fiche élève et synthèse enseignant, par le moteur existant.
    analyse = ana.analyse(session, correction, assessment)
    from app.domain import action_plan
    from app.routes import delayed_checks
    ancien_plan = action_plan.build(analyse, delayed_checks(session, assessment.student_id))
    for report_type, audience in (("FICHE_ELEVE", "eleve"),
                                  ("SYNTHESE_ENSEIGNANT", "enseignant")):
        try:
            rapport = rep.ensure_report(session, assessment, correction, analyse,
                                        ancien_plan, delayed_checks(session, assessment.student_id),
                                        report_type, regenerate=True)
            tex = rep.render_tex(rapport, assessment, analyse, ancien_plan)
            texte = "\n".join(b.content for b in rapport.blocks)
            controle = guard.validate(texte, faits["skills"], audience)
            resultat = rep.compile_pdf(rapport, tex, assessment) if compiler else \
                {"ok": True, "pdf_path": None}
            releves.append({"type": report_type,
                            "ok": bool(resultat.get("ok")) and controle["ok"],
                            "pdf": resultat.get("pdf_path"),
                            "violations": controle["violations"],
                            "reason": resultat.get("reason") or resultat.get("log")})
        except Exception as exc:                       # noqa: BLE001 — on rapporte
            releves.append({"type": report_type, "ok": False, "pdf": None,
                            "violations": [], "reason": "%s: %s"
                            % (type(exc).__name__, exc)})
    return releves


# Nom de QA : type, niveau, élève. Les planches contact se lisent ainsi d'un coup
# d'œil, et un défaut se rattache immédiatement à un niveau.
_ETIQUETTE_TYPE = {"BILAN_PARENTS_LONGITUDINAL": "PARENTS",
                   "FICHE_ELEVE": "ELEVE", "SYNTHESE_ENSEIGNANT": "ENSEIGNANT"}


def _ranger(releves, level_key, student_id, dossier_sortie):
    """Copie les PDF produits sous un nom stable, pour l'audit visuel."""
    destination = Path(dossier_sortie)
    destination.mkdir(parents=True, exist_ok=True)
    for releve in releves:
        chemin = releve.get("pdf")
        if not chemin or not Path(chemin).exists():
            continue
        nom = "%s__%s__%s.pdf" % (_ETIQUETTE_TYPE.get(releve["type"], releve["type"]),
                                  level_key, student_id)
        cible = destination / nom
        shutil.copy2(chemin, cible)
        releve["qa_pdf"] = str(cible)
        releve["sha256"] = _sha256(cible)
        releve["bytes"] = cible.stat().st_size
    return releves


def _sha256(chemin):
    import hashlib
    h = hashlib.sha256()
    with open(str(chemin), "rb") as f:
        for bloc in iter(lambda: f.read(1 << 16), b""):
            h.update(bloc)
    return h.hexdigest()


def run(compiler=True, garder=False, sortie=None, limite=None) -> dict:
    racine = Path(tempfile.mkdtemp(prefix="nexus_synthetic_"))
    dossier_sortie = Path(sortie or SORTIE_PAR_DEFAUT)
    dossier_sortie.mkdir(parents=True, exist_ok=True)

    _isoler_runtime(racine)   # effet de bord : redirige runtime/ vers le temporaire
    from app import database
    from app.domain import correction as corr
    from app.domain.longitudinal import LongitudinalReportService
    from app.models import Assessment, Student
    from fastapi.testclient import TestClient
    from app.main import app

    resultats = []
    try:
        with TestClient(app, headers={"X-Requested-With": "nexus-synthetic"}) as client:
            with database.session_scope() as session:
                eleves = [s.student_id for s in
                          session.query(Student).order_by(Student.student_id).all()]
            if limite:
                eleves = eleves[:limite]

            for student_id in eleves:
                releve = {"student_id": student_id, "documents": [], "ok": False}
                try:
                    releve["scoring_lines"] = _remplir(client, database, student_id,
                                                       _motif_mixte)
                    with database.session_scope() as session:
                        assessment = session.query(Assessment).filter_by(
                            student_id=student_id).one()
                        correction = corr.current_correction(
                            session, assessment.assessment_id)
                        releve["correction_status"] = correction.status
                        service = LongitudinalReportService(session)
                        obstacles = service.check_ready(correction)
                        if obstacles:
                            releve["reason"] = " ; ".join(obstacles)
                            resultats.append(releve)
                            continue
                        faits = service.build_longitudinal_facts(
                            assessment, correction, persist=True)
                        releve["facts_sha256"] = faits["facts_sha256"]
                        releve["p1"] = faits["four_week_plan"]["p1_count"]
                        releve["plan_mode"] = faits["four_week_plan"]["mode"]
                        releve["level_key"] = assessment.level_key
                        releve["documents"] = _documents(
                            session, assessment, correction, faits,
                            dossier_sortie, compiler)
                        if compiler and garder:
                            _ranger(releve["documents"], assessment.level_key,
                                    student_id, dossier_sortie)
                    releve["ok"] = all(d["ok"] for d in releve["documents"])
                except Exception as exc:                # noqa: BLE001 — on rapporte
                    releve["reason"] = "%s: %s" % (type(exc).__name__, exc)
                resultats.append(releve)
    finally:
        shutil.rmtree(racine, ignore_errors=True)
        if not garder:
            shutil.rmtree(dossier_sortie, ignore_errors=True)

    documents = [d for r in resultats for d in r["documents"]]
    return {
        "couples": len(resultats),
        "couples_ok": sum(1 for r in resultats if r["ok"]),
        "documents": len(documents),
        "documents_ok": sum(1 for d in documents if d["ok"]),
        "compiled": compiler,
        "results": resultats,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-compile", action="store_true",
                    help="contrôler le rendu et la langue sans compiler les PDF")
    ap.add_argument("--keep", action="store_true",
                    help="conserver les PDF produits sous tmp/tests")
    ap.add_argument("--limit", type=int, default=None,
                    help="ne traiter que les N premiers couples")
    ap.add_argument("--json", action="store_true", help="sortie JSON")
    args = ap.parse_args(argv)

    rapport = run(compiler=not args.no_compile, garder=args.keep, limite=args.limit)
    if args.json:
        print(json.dumps(rapport, ensure_ascii=False, indent=2))
        return 0 if rapport["couples_ok"] == rapport["couples"] else 1

    print("%-24s %-8s %-6s %s" % ("élève", "lignes", "P1", "documents"))
    for releve in rapport["results"]:
        etat = "  ".join("%s %s" % ("OK " if d["ok"] else "ÉCHEC", d["type"][:22])
                         for d in releve["documents"]) or releve.get("reason", "—")
        print("%-24s %-8s %-6s %s" % (releve["student_id"],
                                      releve.get("scoring_lines", "—"),
                                      releve.get("p1", "—"), etat))
    print()
    print("couples   %d / %d" % (rapport["couples_ok"], rapport["couples"]))
    print("documents %d / %d%s" % (rapport["documents_ok"], rapport["documents"],
                                   " (compilés)" if rapport["compiled"] else " (rendus)"))
    return 0 if rapport["couples_ok"] == rapport["couples"] else 1


if __name__ == "__main__":
    sys.exit(main())
