#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refuse mécaniquement les formulations que les données ne soutiennent pas.

Un bilan doit répondre aux données, et non l'inverse. Ce contrôleur lit un bilan
rédigé et le confronte aux faits structurés produits par l'analyseur. Il n'écrit
pas le bilan : il en interdit certaines phrases.

Sept interdits :

    1. une progression chiffrée quand aucune mesure initiale appariée n'existe ;
    2. « a progressé de N niveaux » ;
    3. « maîtrise désormais » adossé à une preuve faible ou insuffisante ;
    4. « non acquis » sur une notion de passerelle ;
    5. « lacune » sur une notion jamais enseignée ;
    6. « consolidation durable » après une remédiation immédiate ;
    7. « niveau insuffisant » fondé sur la seule note brute sur 20.
"""

import argparse
import os
import re
import sys
import unicodedata

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd

PROGRESSION = re.compile(
    r"(progress\w*|amelior\w*|gain)[^.\n]{0,40}?[-+]?\d+([.,]\d+)?\s*(%|points?|niveaux?)"
    r"|[-+]?\d+([.,]\d+)?\s*(%|points?|niveaux?)[^.\n]{0,20}?(de\s+)?progress", re.I)
NIVEAUX = re.compile(r"progress\w*\s+de\s+\d+\s+niveaux?", re.I)
MAITRISE = re.compile(r"maitrise\s+desormais|desormais\s+maitris", re.I)
DURABLE = re.compile(r"(consolidation|acquis)\s+durable|durablement\s+consolid", re.I)
INSUFFISANT = re.compile(r"niveau\s+insuffisant", re.I)
NOTE20 = re.compile(r"\b\d{1,2}([.,]\d+)?\s*/\s*20\b")
NON_ACQUIS = re.compile(r"non[\s-]+acquis|pas\s+acquise?\b", re.I)
LACUNE = re.compile(r"lacunes?\b", re.I)


def _fold(t):
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


# Mots trop courants pour identifier une notion à eux seuls.
BANALS = {"programme", "premiere", "troisieme", "quatrieme", "seconde", "cinquieme",
          "decouverte", "notion", "notions", "annee", "identification", "justification",
          "nommer", "employer", "cotes", "triangle", "rectangle", "acquis"}


def _keywords(label):
    """Mots distinctifs d'un libellé de compétence de passerelle."""
    words = re.findall(r"[a-z]{6,}", _fold(label or "").lower())
    return [w for w in words if w not in BANALS]


def _sentences(text):
    for raw in re.split(r"(?<=[.!?\n])\s+", text):
        s = raw.strip()
        if s:
            yield s


def check(text, facts=None):
    facts = facts or {}
    findings = []
    weak = {s["analysis_skill_id"] for s in facts.get("_skills", [])
            if s.get("evidence_strength") in ("insufficient", "low")}
    bridge_labels = [b.get("label") or "" for b in facts.get("premieres_passerelles", [])]
    bridge_ids = [b.get("analysis_skill_id", "") for b in facts.get("premieres_passerelles", [])]
    immediate = set(facts.get("reussites_immediates_a_confirmer", []))
    progression_possible = facts.get("progression_chiffree_possible", False)

    def hit(rule, sentence, why):
        findings.append({"regle": rule, "phrase": sentence.strip()[:300], "motif": why})

    for s in _sentences(text):
        f = _fold(s)
        if not progression_possible and (PROGRESSION.search(f) or NIVEAUX.search(f)):
            hit("progression_chiffree", s,
                "aucune mesure initiale appariée n'existe : aucune progression chiffrée ne peut "
                "être écrite")
        if MAITRISE.search(f):
            cited = [w for w in weak if w.lower() in s.lower()]
            hit("maitrise_desormais", s,
                "formulation d'acquisition définitive%s"
                % ((" sur une compétence à preuve faible : %s" % ", ".join(cited)) if cited
                   else " ; à n'employer que sur une preuve forte et confirmée à distance"))
        if DURABLE.search(f):
            hit("consolidation_durable", s,
                "la consolidation durable ne peut pas être affirmée après une remédiation "
                "immédiate ; %d compétence(s) attendent un contrôle différé" % len(immediate))
        if INSUFFISANT.search(f) and NOTE20.search(s):
            hit("niveau_insuffisant_sur_note", s,
                "un jugement de niveau ne peut pas se fonder sur la seule note brute sur 20")
        if NON_ACQUIS.search(f) or LACUNE.search(f):
            low = _fold(s).lower()
            for lab, sid in zip(bridge_labels, bridge_ids):
                keys = _keywords(lab)
                if (sid and sid.lower() in s.lower()) or (keys and any(k in low for k in keys)):
                    hit("deficit_sur_passerelle", s,
                        "« %s » relève d'une passerelle vers l'année N : ni « non acquis », ni "
                        "« lacune » ne sont autorisés" % (lab or sid))
                    break
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--bilan", required=True, help="fichier texte ou markdown du bilan")
    ap.add_argument("--facts", help="bilan_facts_v3.json de l'élève")
    ap.add_argument("--analysis", help="post_stage_analysis_v3.json, pour la force de preuve")
    args = ap.parse_args(argv)
    with open(args.bilan, encoding="utf-8") as f:
        text = f.read()
    facts = pd.read_json(args.facts, "faits du bilan") if args.facts else {}
    if args.analysis:
        facts["_skills"] = pd.read_json(args.analysis, "analyse")["skills"]
    findings = check(text, facts)
    if not findings:
        print("aucune formulation interdite détectée.")
        return 0
    for f in findings:
        print("REFUS [%s]\n  %s\n  -> %s" % (f["regle"], f["phrase"], f["motif"]))
    print("\n%d formulation(s) interdite(s)." % len(findings))
    return 1


if __name__ == "__main__":
    sys.exit(main())
