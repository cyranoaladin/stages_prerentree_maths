#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit docimologique des quinze évaluations et matrice de comparabilité par niveau.

Produit `_audit/audit_docimologique.json` et une sortie lisible.
Contrôles :
  1.  table item / durée / points / compétence, et somme des durées ;
  2.  faisabilité en 45 minutes, marge conservée ;
  3.  barème effectivement sur 20 ;
  4.  validité de contenu : toute compétence évaluée appartient au référentiel du
      niveau et a été travaillée, ou bien est explicitement déclarée comme contenu
      introduit en séance 5 ;
  5.  difficulté progressive par partie ;
  6.  équilibre automatismes / application / transfert ;
  7.  absence de surpondération d'une compétence ;
  8.  indépendance des questions (aucun énoncé ne renvoie à la réponse d'un autre) ;
  9.  crédit partiel disponible sur tout item valant au moins 2 points ;
  10. absence de question à choix fermé, donc pas de réussite par hasard ;
  11. capacité à distinguer les familles d'erreur sur l'ensemble de la copie ;
  12. noyau commun identique entre élèves d'un même niveau (équité) ;
  13. matrice de comparabilité initial / final.
"""

import json
import os
import re
import sys
sys.dont_write_bytecode = True  # aucune trace de cache dans la livraison
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core
from data import common
from data.levels import LEVELS, LEVEL_ORDER

AUDIT = os.path.join(core.S5_ROOT, "_audit")
# La chaîne à distinguer est : connaissance -> choix de méthode -> exécution.
# En mathématiques elle se lit CONCEPT / METHODE / CALCUL ; en NSI, le choix de
# méthode se manifeste dans l'enchaînement des instructions (ALGORITHME) et
# l'exécution dans l'écriture du langage (SYNTAXE).
FAMILLES_ATTENDUES = {
    "Mathématiques": {"CONCEPT", "METHODE", "CALCUL"},
    "NSI": {"CONCEPT", "ALGORITHME", "SYNTAXE"},
}
FAMILLES_CONTROLE = {"LECTURE", "JUSTIFICATION", "CONTROLE", "NOTATION", "TRANSFERT"}
FAMILLES_SECONDAIRES = {"LECTURE", "JUSTIFICATION", "CONTROLE", "NOTATION",
                        "ALGORITHME", "SYNTAXE", "TRANSFERT", "ETOURDERIE", "METHODE", "CALCUL"}
CHOIX_FERME = re.compile(r"\bcocher\b|\bQCM\b|\bparmi les propositions\b|\bréponse [A-D]\b", re.I)

# ------------------------------------------------------------------------------
# Estimateur secondaire, indépendant du générateur.
#
# L'estimateur principal (data/timing.py) part du TEXTE de l'item : caractères à
# lire, sous-questions, lignes de réponse. Celui-ci part du BARÈME : nombre de
# sous-parties distinctes, nature de la preuve exigée sur chacune, difficulté de
# l'item, points en jeu. Les deux modèles n'ont aucune entrée commune, ce qui rend
# leur accord informatif. La durée retenue pour juger la faisabilité est la plus
# prudente des deux.
COUT_PREUVE = {"automatisme": 0.8, "procedure": 1.1, "controle": 0.9,
               "justification": 1.3, "transfert": 1.5, "communication": 1.2}
FACTEUR_DIFFICULTE = {"socle": 0.8, "standard": 1.0, "transfert": 1.15}
OUVERTURE_ITEM = 0.5     # prise de connaissance de l'item
REDACTION_PAR_POINT = 0.55


def duree_par_bareme(item):
    """Durée estimée à partir du seul barème, sans lire l'énoncé."""
    parts = defaultdict(list)
    for c in item["criteria"]:
        parts[c["subpart"]].append(COUT_PREUVE[c["evidence_type"]])
    traitement = sum(max(v) for v in parts.values()) * FACTEUR_DIFFICULTE[item["difficulty"]]
    return round(OUVERTURE_ITEM + traitement + REDACTION_PAR_POINT * item["points"], 3)


def audit_student(st):
    lv = core.level_of(st)
    items = core.exam_items(st)
    tot = core.exam_totals(items)
    findings, warnings = [], []

    table = [{
        "item_id": it["item_id"], "ref": it["ref"], "part": it["part"], "kind": it["kind"],
        "duree_estimee_min": it["minutes"],
        "duree_par_bareme_min": duree_par_bareme(it),
        "decomposition_duree": it["time_estimate"]["breakdown"],
        "points": it["points"],
        "criteres": [{"criterion_id": c["criterion_id"], "points": c["points"],
                      "skill_id": c["skill_id"], "evidence_type": c["evidence_type"],
                      "subpart": c["subpart"]} for c in it["criteria"]],
        "competence": it["skill"],
        "competences_secondaires": it.get("skills_extra", []),
        "type_de_tache": it["task"], "difficulte": it["difficulty"],
        "nb_criteres_bareme": len(it["criteria"]),
        "codes_erreur": sorted({e["code"] for e in it["errors"]}),
        "comparaison": it["comparison_status"],
        "baseline_item_id": it["baseline_item"],
    } for it in items]

    # 1-3 : deux estimations indépendantes, la plus prudente fait foi
    somme_a = round(sum(t["duree_estimee_min"] for t in table), 2)
    somme_b = round(sum(duree_par_bareme(it) for it in items), 2)
    prudent = max(somme_a, somme_b)
    marge = round(common.EXAM_MINUTES - prudent, 2)
    ecart = round(100.0 * (somme_b - somme_a) / somme_a, 1)
    somme_pts = sum(t["points"] for t in table)
    if prudent > common.EXAM_MAX_ESTIMATED_MINUTES:
        findings.append("durée prudente %s min supérieure au plafond de %s min"
                        % (prudent, common.EXAM_MAX_ESTIMATED_MINUTES))
    if marge < common.EXAM_MIN_MARGIN_MINUTES:
        findings.append("marge de %s min sur les 45 minutes, minimum exigé %s min"
                        % (marge, common.EXAM_MIN_MARGIN_MINUTES))
    if abs(ecart) > 20:
        warnings.append("les deux estimateurs divergent de %.1f %% : %s min par le contenu, "
                        "%s min par le barème" % (ecart, somme_a, somme_b))
    if abs(somme_pts - 20) > 1e-9:
        findings.append("barème total de %s points au lieu de 20" % somme_pts)

    # critères : une compétence par critère, types de preuve déclarés
    for it in items:
        for c in it["criteria"]:
            if not c.get("criterion_id") or not c.get("skill_id"):
                findings.append("%s : critère sans identifiant ou sans compétence" % it["ref"])
            if c.get("evidence_type") not in COUT_PREUVE:
                findings.append("%s : type de preuve inconnu (%s)" % (it["ref"], c.get("evidence_type")))
        if len({c["skill_id"] for c in it["criteria"]}) != len(core.item_skills(it)):
            findings.append("%s : compétences de l'item et des critères divergentes" % it["ref"])

    # 4 : validité de contenu
    for it in items:
        for sid in [it["skill"]] + it.get("skills_extra", []):
            if sid not in lv["skills"]:
                findings.append("%s : compétence %s hors du référentiel du niveau" % (it["ref"], sid))
                continue
            sk = lv["skills"][sid]
            if not sk["sessions"]:
                warnings.append("%s : compétence %s (%s) n'a été travaillée dans aucune séance ; "
                                "elle provient du diagnostic initial" % (it["ref"], sid, sk["domain"]))
            elif sk["sessions"] == ["S5"] and not sk["baseline_items"]:
                if it["comparison_status"] != "not_comparable":
                    findings.append("%s : compétence %s introduite en séance 5 et sans item initial, "
                                    "mais déclarée comparable" % (it["ref"], sid))
            elif sk["sessions"] == ["S5"]:
                warnings.append("%s : compétence %s diagnostiquée au positionnement initial mais "
                                "travaillée seulement lors de la séance 5 du niveau ; l'item reste "
                                "comparable au diagnostic, et relève de l'application, non du transfert "
                                "d'un contenu nouveau" % (it["ref"], sid))

    # 5 : difficulté par partie
    d = {t["ref"]: t["difficulte"] for t in table}
    if not all(d[r] == "socle" for r in ("A1", "A2", "A3", "A4", "A5", "A6")):
        findings.append("partie A : toutes les questions ne sont pas de niveau socle")
    if not all(d[r] in ("standard", "transfert") for r in ("B1", "B2", "B3", "B4")):
        findings.append("partie B : difficulté inadaptée")
    if d["C1"] != "transfert":
        findings.append("partie C : la tâche de synthèse C1 n'est pas de niveau transfert")
    if d["C2"] == "socle":
        findings.append("partie C : l'item individualisé C2 est de niveau socle")

    # 6 : équilibre des types de tâches
    types = Counter(t["type_de_tache"] for t in table)
    if types["automatisme"] != 6 or types["application"] != 4 or types["transfert"] != 2:
        findings.append("équilibre des tâches inattendu : %s" % dict(types))
    pts_par_type = defaultdict(float)
    for t in table:
        pts_par_type[t["type_de_tache"]] += t["points"]

    # 7 : surpondération
    pps = core.points_per_skill(st, items)
    top_skill = max(pps, key=pps.get)
    if 100.0 * pps[top_skill] / somme_pts > 30:
        findings.append("surpondération : %.1f %% des points sur %s"
                        % (100.0 * pps[top_skill] / somme_pts, top_skill))
    if len(pps) < 6:
        warnings.append("seulement %d compétences couvertes par l'évaluation" % len(pps))

    # 8 : indépendance
    refs = set(common.EXAM_ITEM_ORDER)
    for it in items:
        cites = {w for w in re.findall(r"\b([ABC][1-6])\b", it["tex"])} & refs - {it["ref"]}
        if cites:
            findings.append("%s renvoie explicitement à %s : indépendance rompue"
                            % (it["ref"], ", ".join(sorted(cites))))

    # 9 : crédit partiel
    for it in items:
        if it["points"] >= 2 and len(it["criteria"]) < 2:
            findings.append("%s vaut %s points sans crédit partiel (un seul critère)"
                            % (it["ref"], it["points"]))
    tout_ou_rien = [it["ref"] for it in items if len(it["criteria"]) == 1]
    if len(tout_ou_rien) > 6:
        warnings.append("%d items sans crédit partiel" % len(tout_ou_rien))

    # 10 : pas de question à choix fermé
    for it in items:
        if CHOIX_FERME.search(it["tex"]):
            findings.append("%s semble être une question à choix fermé : réussite par hasard possible"
                            % it["ref"])

    # 11 : familles d'erreurs distinguables
    familles = set()
    for it in items:
        familles |= {e["code"] for e in it["errors"]}
    attendues = FAMILLES_ATTENDUES[lv["subject"]]
    manquantes = attendues - familles
    if manquantes:
        findings.append("le barème ne permet pas de distinguer les familles %s "
                        "(chaîne connaissance / méthode / exécution incomplète)"
                        % ", ".join(sorted(manquantes)))
    if not (familles & FAMILLES_CONTROLE):
        findings.append("aucune erreur de justification, de lecture ou de contrôle n'est prévue au barème")
    if len(familles & FAMILLES_SECONDAIRES) < 3:
        warnings.append("moins de trois familles d'erreurs secondaires mobilisées")

    # 13 : comparabilité
    comp = Counter(t["comparaison"] for t in table)
    skills_avec_baseline = {sid for sid, sk in lv["skills"].items() if sk["baseline_items"]}
    skills_evaluees = set(pps)
    couverture = len(skills_evaluees & skills_avec_baseline)
    if comp.get("parallel_measures"):
        findings.append("%d items revendiquent des mesures appariées, indisponibles"
                        % comp["parallel_measures"])
    if comp.get("indicative_skill_comparison", 0) < 6:
        warnings.append("seulement %d items rattachés à un énoncé du positionnement initial"
                        % comp.get("indicative_skill_comparison", 0))
    # rétention : ce qui est remédié puis évalué le jour même
    immediats = sorted({sid for sid in pps
                        if core.retention_context(st, sid)["recommended_delayed_check"]})
    if not immediats:
        warnings.append("aucune compétence signalée pour un contrôle différé : à vérifier")

    return {
        "student_id": st["id"], "name": st["name"], "level_key": lv["key"], "subject": lv["subject"],
        "table_items": table,
        "duree_estimee_par_le_contenu_min": somme_a,
        "duree_estimee_par_le_bareme_min": somme_b,
        "ecart_entre_estimateurs_pct": ecart,
        "duree_prudente_min": prudent,
        "somme_durees_min": prudent,
        "duree_epreuve_min": common.EXAM_MINUTES,
        "marge_min": marge,
        "competences_a_controle_differe": immediats,
        "total_points": somme_pts,
        "duree_par_partie": {p: sum(t["duree_estimee_min"] for t in table if t["part"] == p)
                             for p in "ABC"},
        "points_par_partie": {p: sum(t["points"] for t in table if t["part"] == p) for p in "ABC"},
        "points_par_type_de_tache": dict(pts_par_type),
        "points_par_competence": pps,
        "competence_la_plus_ponderee": {"skill_id": top_skill,
                                        "pct": round(100.0 * pps[top_skill] / somme_pts, 1)},
        "nb_competences_evaluees": len(pps),
        "competences_evaluees_avec_mesure_initiale": couverture,
        "repartition_comparaison": dict(comp),
        "familles_erreur_mobilisees": sorted(familles),
        "items_sans_credit_partiel": tout_ou_rien,
        "anomalies": findings,
        "avertissements": warnings,
        "verdict": "FAIL" if findings else ("PASS WITH WARNINGS" if warnings else "PASS"),
    }


def level_matrix(level_key, rows):
    lv = LEVELS[level_key]
    sts = [st for st in core.all_students() if st["level"] == level_key]
    ref_items = {it["ref"]: it for it in core.exam_items(sts[0])}
    identique = True
    for st in sts[1:]:
        cur = {it["ref"]: it for it in core.exam_items(st)}
        for ref in ("A1", "A2", "A3", "A4", "B1", "B2", "B3", "C1"):
            if cur[ref]["tex"] != ref_items[ref]["tex"] or cur[ref]["points"] != ref_items[ref]["points"]:
                identique = False
    return {
        "level_key": level_key, "label": lv["label"], "subject": lv["subject"],
        "eleves": [st["id"] for st in sts],
        "noyau_commun_identique_entre_eleves": identique,
        "noyau_commun": [{
            "ref": ref, "skill_id": ref_items[ref]["skill"], "points": ref_items[ref]["points"],
            "duree_min": ref_items[ref]["minutes"], "difficulte": ref_items[ref]["difficulty"],
            "baseline_item_id": ref_items[ref]["baseline_item"],
            "baseline_item_text": lv["baseline_items"].get(ref_items[ref]["baseline_item"]),
            "comparaison": ref_items[ref]["comparison_status"],
        } for ref in ("A1", "A2", "A3", "A4", "B1", "B2", "B3", "C1")],
        "items_individualises_par_eleve": {
            st["id"]: [{"ref": ref,
                        "skill_id": core.exam_items(st)[common.EXAM_ITEM_ORDER.index(ref)]["skill"],
                        "points": core.exam_items(st)[common.EXAM_ITEM_ORDER.index(ref)]["points"],
                        "baseline_item_id": core.exam_items(st)[common.EXAM_ITEM_ORDER.index(ref)]["baseline_item"],
                        "comparaison": core.exam_items(st)[common.EXAM_ITEM_ORDER.index(ref)]["comparison_status"]}
                       for ref in ("A5", "A6", "B4", "C2")]
            for st in sts},
        "competences_du_niveau_avec_item_initial": sorted(
            sid for sid, sk in lv["skills"].items() if sk["baseline_items"]),
        "competences_du_niveau_sans_item_initial": sorted(
            sid for sid, sk in lv["skills"].items() if not sk["baseline_items"]),
    }


def main():
    rows = [audit_student(st) for st in core.all_students()]
    matrices = [level_matrix(k, rows) for k in LEVEL_ORDER]
    out = {"schema": "nexus-s5-audit-docimologique-v1", "genere_le": "2026-08-20",
           "eleves": rows, "matrices_de_comparabilite": matrices}
    os.makedirs(AUDIT, exist_ok=True)
    with open(os.path.join(AUDIT, "audit_docimologique.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("%-22s %-9s %6s %6s %7s %6s %5s  %s"
          % ("élève", "niveau", "contenu", "barème", "prudent", "marge", "pts", "verdict"))
    for r in rows:
        print("%-22s %-9s %6s %6s %7s %6s %5s  %s"
              % (r["student_id"], r["level_key"], r["duree_estimee_par_le_contenu_min"],
                 r["duree_estimee_par_le_bareme_min"], r["duree_prudente_min"],
                 r["marge_min"], r["total_points"], r["verdict"]))
        for a in r["anomalies"]:
            print("        ANOMALIE : %s" % a)
        for w in r["avertissements"]:
            print("        note     : %s" % w)
    print()
    for m in matrices:
        print("%-10s noyau commun identique entre élèves : %s" % (m["level_key"],
              "oui" if m["noyau_commun_identique_entre_eleves"] else "NON"))
    return 0 if all(r["verdict"] != "FAIL" for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
