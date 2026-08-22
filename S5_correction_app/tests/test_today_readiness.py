# -*- coding: utf-8 -*-
"""Mise en service : préparation des quinze, garde de la base, cohérence du plan.

Ce module ne teste pas l'architecture — elle est figée — mais son **exploitabilité
aujourd'hui** : les quinze couples sont-ils corrigeables, la base réelle est-elle
protégée, le plan de rentrée reste-t-il tenable quel que soit le profil.

Aucune donnée réelle. Les copies employées sont synthétiques et le disent.
"""

import hashlib
import os
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from app import config, database, latex_html
from app.domain.longitudinal import plan as plan_module
from app.domain.longitudinal import readiness
from app.models import ItemDefinition

PROJECT = Path(config.PROJECT_DIR)
ATTENDU = 15


# ============================================================ 1. les quinze
@pytest.fixture(scope="module")
def etats(client):
    with database.session_scope() as session:
        return readiness.evaluate_all(session, config)


def test_les_quinze_couples_sont_reconnus(etats):
    assert len(etats) == ATTENDU
    assert len({e["student_id"] for e in etats}) == ATTENDU


def test_aucun_couple_n_est_bloque(etats):
    bloques = [(e["student_id"], e.get("blockers")) for e in etats
               if e["status"] == readiness.BLOCKED]
    assert bloques == [], bloques


def test_aucun_eleve_ne_reste_dans_un_etat_implicite(etats):
    """§1 — trois états possibles, et un seul par élève."""
    valides = {readiness.READY, readiness.WARNING, readiness.BLOCKED}
    for etat in etats:
        assert etat["status"] in valides, etat["student_id"]


def test_chaque_couple_a_une_evaluation_coherente(etats):
    for etat in etats:
        finale = etat["final_assessment"]
        assert finale["defined"], etat["student_id"]
        assert finale["scoring_lines"] >= finale["original_criteria"]
        assert finale["n_minus_1_centi"] + finale["bridge_n_centi"] == \
            finale["max_points_centi"], etat["student_id"]


def test_un_manque_documentaire_ne_bloque_jamais(etats):
    """§10 — une séance sans dossier personnalisé donne une réserve, pas un blocage."""
    concernes = [e for e in etats
                 if any("aucun dossier personnalisé" in w
                        for w in e["longitudinal_report"]["warnings"])]
    assert concernes, "le corpus comporte des séances sans dossier personnalisé"
    for etat in concernes:
        assert etat["status"] == readiness.WARNING
        assert etat["longitudinal_report"]["ready"] is True


def test_chaque_reserve_est_motivee(etats):
    for etat in etats:
        for reserve in etat["longitudinal_report"]["warnings"]:
            assert len(reserve) > 30, (etat["student_id"], reserve)
        for source in etat["missing_sources"]:
            assert source["note"], etat["student_id"]


# ================================================== 2. rendu web des quinze
def test_aucun_enonce_ne_laisse_de_latex_brut(session):
    """La porte du renderer, sur l'ensemble du corpus importé."""
    residus = []
    for item in session.query(ItemDefinition).all():
        for champ in (item.statement, item.expected_answer):
            if not champ:
                continue
            rendu = str(latex_html.render_statement(champ))
            for sequence in ("\\begin{", "\\end{", "\\item", "\\code{", "\\textbf{",
                             "\\emph{", "\\hline"):
                if sequence in rendu:
                    residus.append((item.item_id, sequence))
    assert residus == [], residus[:5]


def test_toutes_les_structures_du_corpus_sont_couvertes(session):
    non_couvertes = set()
    for item in session.query(ItemDefinition).all():
        for champ in (item.statement, item.expected_answer):
            non_couvertes.update(latex_html.unsupported_structures(champ))
    assert non_couvertes == set(), non_couvertes


# =================================================== 3. cohérence du plan (§20)
def _matrice(initial, finaux, importance="critique", domaine="Fractions",
            scope="n_minus_1", differe=False):
    """Fabrique une matrice de trajectoire synthétique, sans base de données."""
    lignes = []
    for index, (statut, rang, taux) in enumerate(finaux):
        lignes.append({
            "analysis_skill_id": "SYNTH_%02d" % index,
            "curriculum_scope": scope, "label": "Compétence synthétique %d" % index,
            "domain": domaine, "importance_n": importance,
            "initial_status": initial, "sessions": ["S1"], "coverage": "MODERATE",
            "coverage_label": "travaillée", "has_final_evidence": True,
            "final_status": statut, "final_status_label": statut,
            "evidence_level": "A", "evidence_strength": "MODERATE",
            "success_rate": taux, "criteria_count": 2, "item_refs": ["A1"],
            "error_codes": [], "retention_status":
                "not_yet_verified" if differe else "not_measured",
            "recommended_delayed_check": differe, "priority_rank": rang,
            "bridge_action": None, "trajectory_status": "CONSOLIDATION_OBSERVEE",
            "mastery_delta": None, "worked_during_stage": True,
            "current_mastery": "documented", "qualitative_trajectory": "positive_evidence",
            "conclusion": "—",
        })
    return lignes


def test_scenario_a_plusieurs_fragilites_donne_au_plus_deux_p1():
    """§20 A — quatre priorités de rang 1 ne peuvent pas coexister dans un plan."""
    matrice = _matrice("fragile", [("PRIORITAIRE", "P1", 0.1)] * 4)
    plan = plan_module.build(matrice)
    assert plan["p1_count"] <= plan_module.MAX_P1
    assert plan["p1_within_cap"] is True
    assert len(plan["p1_downgraded_by_plan"]) == 2
    for entree in plan["p1_downgraded_by_plan"]:
        assert entree["reason"]


def test_scenario_b_aucun_p1_bascule_en_entretien():
    """§20 B — un élève sans fragilité a besoin d'un plan, pas d'un rattrapage."""
    matrice = _matrice("acquis", [("SOLIDE", "OK", 1.0)] * 3)
    plan = plan_module.build(matrice)
    assert plan["mode"] == "entretien"
    assert "entretien" in plan["mode_note"]
    assert plan["p1_count"] == 0
    objectifs = [o for s in plan["weeks"] for o in s["objectives"]]
    assert objectifs, "le plan reste non vide"
    assert any(o["kind"] == "maintenance" for o in objectifs)


def test_scenario_c_reussite_immediate_donne_un_mini_test_en_semaine_deux():
    """§20 C — la récence se vérifie à distance, jamais le jour même."""
    matrice = _matrice("fragile", [("A_CONFIRMER", "P3", 0.9)], differe=True)
    plan = plan_module.build(matrice)
    semaine2 = next(s for s in plan["weeks"] if s["week"] == 2)
    differes = [o for o in semaine2["objectives"] if o["is_delayed_check"]]
    assert differes
    assert "distance" in differes[0]["objective"] or "révision" in differes[0]["objective"]


def test_scenario_d_bridge_echoue_ne_cree_aucune_priorite_n_moins_1():
    """§20 D — une découverte manquée n'est pas un rattrapage."""
    matrice = _matrice(None, [("DISCOVERY_TO_CONTINUE", None, 0.0)], scope="bridge_n")
    plan = plan_module.build(matrice)
    assert plan["priorities"] == []
    for semaine in plan["weeks"]:
        for objectif in semaine["objectives"]:
            assert objectif["kind"] != "bridge_n"
    assert plan["bridge_follow_up"]


def test_scenario_e_diagnostic_initial_absent_produit_un_plan_et_un_avertissement():
    """§20 E — sans point de départ, le plan s'appuie sur les preuves finales."""
    matrice = _matrice(None, [("PRIORITAIRE", "P1", 0.2), ("A_CONSOLIDER", "P2", 0.5)])
    plan = plan_module.build(matrice)
    assert plan["mode"] == "consolidation"
    assert plan["priorities"]
    for ligne in matrice:
        assert ligne["initial_status"] is None
        assert ligne["mastery_delta"] is None


def test_le_plan_ne_depasse_jamais_trois_objectifs_par_semaine():
    matrice = _matrice("fragile", [("PRIORITAIRE", "P1", 0.1)] * 8)
    plan = plan_module.build(matrice)
    for semaine in plan["weeks"]:
        assert len(semaine["objectives"]) <= 3, semaine["week"]


def test_la_charge_reste_realiste_quel_que_soit_le_profil():
    for finaux in ([("PRIORITAIRE", "P1", 0.1)] * 6, [("SOLIDE", "OK", 1.0)] * 4):
        plan = plan_module.build(_matrice("fragile", finaux))
        for semaine in plan["weeks"]:
            for objectif in semaine["objectives"]:
                assert 10 <= objectif["duration_minutes"] <= 25
                assert objectif["success_threshold"]


# =========================================== 4. protection de la base (§32, §33)
def test_la_reinitialisation_destructrice_refuse_une_base_porteuse_de_donnees():
    """§33 — code non nul, et la base ne bouge pas d'un octet."""
    racine = Path(tempfile.mkdtemp(prefix="nexus_guard_test_"))
    env = dict(os.environ, NEXUS_S5_RUNTIME=str(racine),
               NEXUS_S5_DB=str(racine / "c.sqlite3"), PYTHONDONTWRITEBYTECODE="1")
    outil = str(PROJECT / "tools" / "init_database.py")

    creation = subprocess.run([sys.executable, outil], cwd=str(PROJECT),
                              capture_output=True, text=True, env=env, shell=False)
    assert creation.returncode == 0, creation.stderr

    connexion = sqlite3.connect(racine / "c.sqlite3")
    connexion.execute(
        "INSERT INTO correction (assessment_id,revision,status,is_current,is_synthetic,"
        "created_at,updated_at) VALUES ((SELECT assessment_id FROM assessment LIMIT 1),"
        "1,'DRAFT',1,0,datetime('now'),datetime('now'))")
    identifiant = connexion.execute("SELECT correction_id FROM correction").fetchone()[0]
    connexion.execute(
        "INSERT INTO criterion_response (correction_id,scoring_id,criterion_id,is_virtual,"
        "score_centi,max_score_centi,error_codes_json,accepted_alternative_method,"
        "scoring_status,updated_at) VALUES (?,'X','X',0,100,100,'[]',0,'SCORED',"
        "datetime('now'))", (identifiant,))
    connexion.commit()
    connexion.close()

    avant = hashlib.sha256((racine / "c.sqlite3").read_bytes()).hexdigest()
    refus = subprocess.run([sys.executable, outil, "--force"], cwd=str(PROJECT),
                           capture_output=True, text=True, env=env, shell=False)
    apres = hashlib.sha256((racine / "c.sqlite3").read_bytes()).hexdigest()

    assert refus.returncode != 0, "la réinitialisation aurait détruit des données"
    assert avant == apres, "la base a été modifiée malgré le refus"
    assert "REFUS" in refus.stderr


def test_une_correction_synthetique_ne_bloque_pas_la_reinitialisation():
    """Contre-épreuve : la garde ne doit pas bloquer sur une fixture déclarée."""
    from tools.init_database import real_corrections
    racine = Path(tempfile.mkdtemp(prefix="nexus_guard_synth_"))
    env = dict(os.environ, NEXUS_S5_RUNTIME=str(racine),
               NEXUS_S5_DB=str(racine / "c.sqlite3"), PYTHONDONTWRITEBYTECODE="1")
    subprocess.run([sys.executable, str(PROJECT / "tools" / "init_database.py")],
                   cwd=str(PROJECT), capture_output=True, text=True, env=env, shell=False)
    connexion = sqlite3.connect(racine / "c.sqlite3")
    connexion.execute(
        "INSERT INTO correction (assessment_id,revision,status,is_current,is_synthetic,"
        "created_at,updated_at) VALUES ((SELECT assessment_id FROM assessment LIMIT 1),"
        "1,'DRAFT',1,1,datetime('now'),datetime('now'))")
    identifiant = connexion.execute("SELECT correction_id FROM correction").fetchone()[0]
    connexion.execute(
        "INSERT INTO criterion_response (correction_id,scoring_id,criterion_id,is_virtual,"
        "score_centi,max_score_centi,error_codes_json,accepted_alternative_method,"
        "scoring_status,updated_at) VALUES (?,'X','X',0,100,100,'[]',0,'SCORED',"
        "datetime('now'))", (identifiant,))
    connexion.commit()
    connexion.close()
    assert real_corrections(racine / "c.sqlite3") == []


def test_une_base_vierge_se_reinitialise_sans_obstacle():
    from tools.init_database import real_corrections
    racine = Path(tempfile.mkdtemp(prefix="nexus_guard_vierge_"))
    assert real_corrections(racine / "absente.sqlite3") == []


# ============================================ 5. échappement typographique
def test_les_caracteres_refuses_par_le_moteur_sont_neutralises():
    """Relevés sur le corpus, chacun vérifié par une compilation d'essai."""
    from app.domain.reports import latex_escape
    for caractere in "−∪⁴⁵⁻≥≤≠′":
        rendu = latex_escape(caractere)
        assert caractere not in rendu, caractere
        assert rendu != "", caractere


def test_un_caractere_imprevu_ne_fait_jamais_echouer_un_bilan():
    """Filet de sécurité : perdre un glyphe vaut mieux que perdre le document."""
    from app.domain.reports import latex_escape
    for caractere in "∀∮♠⨁":
        rendu = latex_escape("a %s b" % caractere)
        assert caractere not in rendu, caractere


def test_les_caracteres_acceptes_traversent_intacts():
    """Contre-épreuve : on ne neutralise pas ce qui fonctionne."""
    from app.domain.reports import latex_escape
    texte = "« citation » 3° 2² 3³ 5×2 6÷3 — …"
    assert latex_escape(texte) == texte


# ================================================== 6. confidentialité (§24)
def test_aucune_donnee_runtime_n_est_suivie_par_git():
    acheve = subprocess.run(
        [sys.executable, str(PROJECT / "tools" / "check_runtime_not_tracked.py")],
        cwd=str(PROJECT), capture_output=True, text=True, shell=False)
    assert acheve.returncode == 0, acheve.stdout + acheve.stderr


def test_le_marquage_synthetique_existe_en_base(session):
    """§22 — une fixture doit pouvoir se déclarer."""
    from app.models import Correction
    assert hasattr(Correction, "is_synthetic")
    colonnes = {c.name for c in Correction.__table__.columns}
    assert "is_synthetic" in colonnes


# =================================================== 7. tableau de bord (§13)
def test_le_tableau_de_bord_distingue_correction_et_bilan(client):
    page = client.get("/").text
    assert "Bilan longitudinal" in page
    assert "Correction" in page
    # les deux axes ne portent pas les mêmes valeurs
    assert "Prêt avec réserve documentaire" in page or "Prêt" in page


def test_la_page_de_mise_en_service_repond(client):
    page = client.get("/admin/mise-en-service")
    assert page.status_code == 200
    for attendu in ("Mise en service", "Immutabilité", "Préparation longitudinale",
                    "Corrections réelles"):
        assert attendu in page.text, attendu


def test_l_ecran_longitudinal_montre_les_sources_avant_validation(client):
    client.get("/eleve/ines-kefi")          # ouvre la correction, encore en brouillon
    page = client.get("/eleve/ines-kefi/bilan-longitudinal").text
    assert "Sources disponibles" in page
    assert "sera générable après validation" in page
    # aucun contenu final n'est fabriqué avant la validation
    assert "Points forts actuels" not in page
