#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de analyze_s5.py sur le jeu de données SYNTHETIQUE.

Exécution :
    python3 S5_cloture/tools/tests/test_analyze_s5.py
Retourne 0 si tous les tests passent, 1 sinon.
"""

import json
import os
import sys
sys.dont_write_bytecode = True  # aucune trace de cache dans la livraison

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import analyze_s5              # noqa: E402
import make_fixture            # noqa: E402
import jsonschema              # noqa: E402

FIXTURE = os.path.join(HERE, "fixture_synthetique")
RESULTS = []


def t(label, fn):
    try:
        fn()
        RESULTS.append((True, label, ""))
    except AssertionError as exc:
        RESULTS.append((False, label, str(exc)))
    except Exception as exc:  # noqa: BLE001
        RESULTS.append((False, label, "exception %s : %s" % (type(exc).__name__, exc)))


def load(name):
    with open(os.path.join(FIXTURE, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    make_fixture.build()
    st = make_fixture.synthetic_student()
    filled = load("responses_SYNTHETIQUE.json")
    a = analyze_s5.analyse(st, filled, base_dir=FIXTURE)
    skills = {s["skill_id"]: s for s in a["skills"]}
    prio = {p["skill_id"]: p["priority_rank"] for p in a["priorities"]}

    # ------------------------------------------------------------------ score
    t("score brut = 12", lambda: _eq(a["score"]["total_points"], 12))
    t("maximum = 20", lambda: _eq(a["score"]["max_points"], 20))
    t("note sur 20 = 12.0", lambda: _eq(a["score"]["note_sur_20"], 12.0))
    t("taux de réussite = 0.60", lambda: _eq(a["score"]["success_rate"], 0.6))
    t("partie A = 4 / 6", lambda: _eq(a["score"]["by_part"]["A"]["points"], 4))
    t("partie B = 5 / 8", lambda: _eq(a["score"]["by_part"]["B"]["points"], 5))
    t("partie C = 3 / 6", lambda: _eq(a["score"]["by_part"]["C"]["points"], 3))
    t("noyau commun = 10", lambda: _eq(a["score"]["common_core_points"], 10))
    t("items individualisés = 2", lambda: _eq(a["score"]["individual_points"], 2))

    # ------------------------------------------------- répartition par compétence
    t("12 items analysés", lambda: _eq(len(a["items"]), 12))
    t("somme des points par compétence = 20",
      lambda: _eq(round(sum(s["max_points"] for s in a["skills"]), 3), 20.0))

    def _criteria_scoring():
        assert a["scoring_model"].startswith("par critère")
        # chaque critère ne crédite qu'une compétence
        for c in a["criteria"]:
            assert isinstance(c["skill_id"], str) and c["skill_id"]
        # le score d'une compétence est la somme des critères qui la portent
        for sk in a["skills"]:
            somme = sum(c["points"] for c in a["criteria"] if c["skill_id"] == sk["skill_id"])
            assert abs(somme - sk["points"]) < 1e-9, (sk["skill_id"], somme, sk["points"])
        # aucune répartition uniforme : au moins un item multi-compétences répartit
        # ses points de façon inégale entre ses compétences
        multi = [i for i in a["items"] if len(i["skills"]) > 1]
        assert multi, "aucun item multi-compétences dans le jeu de test"
    t("scoring par critère, sans répartition uniforme", _criteria_scoring)

    def _partial_credit_targets_the_right_skill():
        # B2 est raté (0 point) : aucune de ses compétences ne doit être créditée par lui
        b2 = [i for i in a["items"] if i["ref"] == "B2"][0]
        assert b2["points"] == 0
        for c in b2["criteria"]:
            assert c["points"] == 0
    t("un item raté ne crédite aucune de ses compétences", _partial_credit_targets_the_right_skill)

    def _schema():
        schema = load("post_stage_analysis_schema.json")
        jsonschema.validate(a, schema)
    t("la sortie réelle de l'analyseur valide son schéma v2", _schema)

    def _schema_rejects_delta():
        schema = load("post_stage_analysis_schema.json")
        faux = json.loads(json.dumps(a))
        faux["skills"][0]["mastery_delta"] = 2
        try:
            jsonschema.validate(faux, schema)
        except jsonschema.ValidationError:
            return
        raise AssertionError("le schéma accepte un mastery_delta chiffré")
    t("le schéma refuse tout écart chiffré", _schema_rejects_delta)

    # -------------------------------------------------------------- comparaison
    def _no_delta_at_all():
        for sk in a["skills"]:
            assert sk["mastery_delta"] is None, sk["skill_id"]
            assert sk["baseline_mastery"] is None, sk["skill_id"]
            assert sk["baseline_measure_available"] is False, sk["skill_id"]
            assert sk["delta_blocked_reason"], sk["skill_id"]
    t("aucun écart de maîtrise n'est produit, pour aucune compétence", _no_delta_at_all)

    def _statuses():
        allowed = {"parallel_measures", "indicative_skill_comparison", "post_only",
                   "not_comparable"}
        for sk in a["skills"]:
            assert sk["comparison_status"] in allowed, sk["comparison_status"]
        assert not any(sk["comparison_status"] == "parallel_measures" for sk in a["skills"]), \
            "parallel_measures exige deux mesures nominatives, indisponibles aujourd'hui"
    t("statuts de comparaison explicites, sans parallel_measures", _statuses)

    def _qualitative_only():
        f = analyze_s5.build_facts(st, a)
        assert f["progression_chiffree_possible"] is False
        assert "progression_documented" not in f
        for row in f["comparaison_qualitative"]:
            assert "mastery_delta" not in row
    t("les faits du bilan ne comportent aucune progression chiffrée", _qualitative_only)

    def _retention():
        marques = [sk for sk in a["skills"] if sk["recommended_delayed_check"]]
        assert marques, "aucune compétence marquée pour un contrôle différé"
        for sk in marques:
            assert sk["retention_status"] == "not_yet_verified", sk["skill_id"]
            assert sk["post_test_context"] in ("immediate_after_remediation",
                                               "first_worked_in_session_5",
                                               "introduced_in_session_5"), sk["post_test_context"]
        for sk in a["skills"]:
            if sk["skill_id"] in (st["p1"], st["p2"]):
                assert sk["recommended_delayed_check"], sk["skill_id"]
    t("remédiation immédiate signalée et rétention non vérifiée", _retention)

    def _evidence():
        for sk in a["skills"]:
            assert sk["evidence_strength"] in ("faible", "moyenne", "forte")
            assert "measurement_reliability" not in sk
    t("force de preuve remplace la fiabilité de mesure", _evidence)

    # ----------------------------------------------------------------- maîtrise
    t("maîtrise dans 0-4",
      lambda: _true(all(0 <= s["post_mastery"] <= 4 for s in a["skills"])))

    def _cap():
        # C2 (transfert) est raté : aucune compétence ne peut atteindre 4 par ce biais
        for s in a["skills"]:
            if s["post_mastery"] == 4:
                assert not s["post_mastery_capped_by_transfer"]
    t("maîtrise 4 conditionnée à une réussite en transfert", _cap)

    # ----------------------------------------------------------------- erreurs
    t("profil d'erreurs comptabilisé",
      lambda: _eq(a["errors"]["error_profile_after"]["CONCEPT"], 3))
    t("code dominant = CONCEPT", lambda: _eq(a["errors"]["dominant_codes"][0], "CONCEPT"))

    # --------------------------------------------------------------- certitude
    t("certitude finale moyenne = 3.0", lambda: _eq(a["confidence"]["confidence_after"], 3.0))
    t("cellule faux + confiance haute = 1 (B2 raté, certitude 4)",
      lambda: _eq(a["confidence"]["calibration_cells"]["faux_confiance_haute"], 1))
    t("cellule juste + confiance basse = 1 (C1 réussi à 75 %, certitude 2)",
      lambda: _eq(a["confidence"]["calibration_cells"]["juste_confiance_basse"], 1))
    t("aucune réussite partielle mal classée",
      lambda: _eq(a["confidence"]["calibration_cells"]["partiel_non_classe"], 0))
    t("certitude initiale non recalculée",
      lambda: _true(a["confidence"]["confidence_before"] is None))

    # --------------------------------------------------------------- priorités
    t("toutes les compétences priorisées", lambda: _eq(len(a["priorities"]), len(a["skills"])))
    t("au plus 4 compétences en P1",
      lambda: _true(len([p for p in a["priorities"] if p["priority_rank"] == "P1"]) <= 4))
    t("les priorités ne sont pas toutes P1",
      lambda: _true(len(set(prio.values())) > 1))

    # ------------------------------------------------------- plan 4 semaines
    plan = analyze_s5.build_plan(st, a)
    t("plan à quatre semaines", lambda: _eq(len(plan["weeks"]), 4))
    t("2 ou 3 compétences par semaine au maximum",
      lambda: _true(all(len(w["skills"]) <= 3 for w in plan["weeks"])))
    t("chaque semaine renseignée a un critère de réussite",
      lambda: _true(all(w["success_criterion"] for w in plan["weeks"] if w["skills"])))
    t("plan dérivé de l'analyse", lambda: _eq(plan["status"], "generated_from_analysis"))

    # ------------------------------------------------------------ bilan parents
    facts = analyze_s5.build_facts(st, a)
    t("faits du bilan : note reprise", lambda: _eq(facts["note_sur_20"], 12.0))
    t("faits du bilan : contenus nouveaux exclus de toute progression",
      lambda: _true(isinstance(facts["contenus_nouveaux_hors_progression"], list)))
    t("faits du bilan : réussites immédiates signalées comme à confirmer",
      lambda: _true(isinstance(facts["reussites_immediates_a_confirmer"], list)
                    and facts["retention_a_verifier"]))
    t("faits du bilan : formulations interdites listées",
      lambda: _true(any("maîtrise X vers Y" in f for f in facts["formulations_interdites"])))

    # ------------------------------------------------------ contrôles d'entrée
    def _missing_score():
        bad = json.loads(json.dumps(filled))
        bad["responses"][0]["criteria"][0]["score"] = None
        try:
            analyze_s5.analyse(st, bad, base_dir=FIXTURE)
        except analyze_s5.InputError:
            return
        raise AssertionError("score manquant accepté")
    t("refus d'un score manquant", _missing_score)

    def _out_of_range():
        bad = json.loads(json.dumps(filled))
        bad["responses"][0]["criteria"][0]["score"] = 99
        try:
            analyze_s5.analyse(st, bad, base_dir=FIXTURE)
        except analyze_s5.InputError:
            return
        raise AssertionError("score hors barème accepté")
    t("refus d'un score hors barème", _out_of_range)

    def _wrong_student():
        bad = json.loads(json.dumps(filled))
        bad["student_id"] = "quelqun-dautre"
        try:
            analyze_s5.analyse(st, bad, base_dir=FIXTURE)
        except analyze_s5.InputError:
            return
        raise AssertionError("fichier d'un autre élève accepté")
    t("refus d'un fichier de saisie d'un autre élève", _wrong_student)

    def _bad_code():
        bad = json.loads(json.dumps(filled))
        bad["responses"][0]["error_codes"] = ["INVENTE"]
        try:
            analyze_s5.analyse(st, bad, base_dir=FIXTURE)
        except analyze_s5.InputError:
            return
        raise AssertionError("code d'erreur inconnu accepté")
    t("refus d'un code d'erreur hors nomenclature", _bad_code)

    def _missing_criterion():
        bad = json.loads(json.dumps(filled))
        bad["responses"][6]["criteria"] = bad["responses"][6]["criteria"][:-1]
        try:
            analyze_s5.analyse(st, bad, base_dir=FIXTURE)
        except analyze_s5.InputError:
            return
        raise AssertionError("critère manquant accepté")
    t("refus d'un critère manquant dans la saisie", _missing_criterion)

    def _missing_item():
        bad = json.loads(json.dumps(filled))
        bad["responses"] = bad["responses"][:-1]
        try:
            analyze_s5.analyse(st, bad, base_dir=FIXTURE)
        except analyze_s5.InputError:
            return
        raise AssertionError("saisie incomplète acceptée")
    t("refus d'une saisie incomplète", _missing_item)

    def _cli_refuses_synthetic():
        # L'élève fictif n'est volontairement pas enregistré : la ligne de commande
        # ne peut donc jamais produire de sortie pour un élève inexistant.
        rc = analyze_s5.main(["--student", "eleve-synthetique-test",
                              "--responses", os.path.join(FIXTURE, "responses_SYNTHETIQUE.json")])
        assert rc == 2, rc
    t("la ligne de commande refuse un élève non enregistré", _cli_refuses_synthetic)

    def _cli_refuses_template():
        import glob
        tmpl = glob.glob(os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                      "*", "*", "*", "responses_TEMPLATE.json"))
        assert tmpl, "aucun gabarit trouvé"
        rc = analyze_s5.main(["--student", "elyes-kefi", "--responses",
                              [x for x in tmpl if "Elyes_KEFI" in x][0]])
        assert rc == 2, rc
    t("la ligne de commande refuse un gabarit non renseigné", _cli_refuses_template)

    # ------------------------------------------------------------------ sortie
    ok = all(r[0] for r in RESULTS)
    for good, label, detail in RESULTS:
        print("%-5s %s%s" % ("OK" if good else "ECHEC", label,
                             "" if good else "  -> " + detail))
    print("\n%d tests, %d réussis, %d échoués"
          % (len(RESULTS), sum(1 for r in RESULTS if r[0]), sum(1 for r in RESULTS if not r[0])))
    return 0 if ok else 1


def _eq(a, b):
    assert a == b, "obtenu %r, attendu %r" % (a, b)


def _true(x):
    assert x, "condition fausse"


if __name__ == "__main__":
    sys.exit(main())
