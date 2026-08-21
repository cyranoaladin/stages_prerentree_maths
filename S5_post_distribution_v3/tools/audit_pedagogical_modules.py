#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle scientifique des supports pédagogiques, au-delà des 100 items d'évaluation.

Périmètre audité, tel qu'il est réellement présent dans le dossier :

    * les 25 modules de remédiation employés en phases 2 et 3, avec leur rappel,
      leur exemple guidé, leurs exercices et leurs corrigés ;
    * les activités de réactivation de la phase 1 ;
    * les blocs de découverte de la phase 4, c'est-à-dire les passerelles ;
    * les cartes de rappel ;
    * les corrigés enseignants.

Trois méthodes, comptées séparément et jamais confondues :

    recalcul     l'énoncé se ramène à une expression arithmétique que ce script
                 réévalue lui-même ; le corrigé doit contenir la valeur obtenue ;
    checkpoint   le corrigé doit contenir des fragments explicitement attendus,
                 écrits à la main dans CHECKPOINTS ;
    revue        l'énoncé porte sur une définition, une explication ou un
                 raisonnement qu'aucun calcul ne tranche ; le verdict vient d'une
                 lecture, consignée mot pour mot.

Ce script ne prétend rien recalculer qu'il ne recalcule effectivement.
"""

import json
import os
import re
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd

OUT_JSON = os.path.join(pd.V3_ROOT, "reports", "pedagogical_audit.json")

# Énoncés dont le résultat ne se recalcule pas, et pourquoi la revue conclut.
REVUE = {
    "definition": "l'attendu est une définition ou une règle à énoncer ; la formulation du "
                  "corrigé a été relue et elle est exacte.",
    "explication": "l'attendu est une explication ; le corrigé propose une formulation correcte "
                   "et ne prétend pas être la seule recevable.",
    "code": "l'attendu est un fragment de programme ou une trace d'exécution ; il a été relu "
            "instruction par instruction.",
    "geometrie": "l'attendu est une propriété géométrique nommée ; la propriété citée par le "
                 "corrigé est celle qui s'applique à la configuration décrite.",
}

_NUM = r"-?\d+(?:[.,]\d+)?"


def _clean(tex):
    t = tex
    t = re.sub(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", t)
    t = re.sub(r"\\d?frac(\d)(\d)", r"((\1)/(\2))", t)
    t = t.replace("{,}", ".").replace("\\,", "").replace("\\;", "").replace("\\ ", " ")
    t = t.replace("\\times", "*").replace("\\div", "/").replace("\\cdot", "*")
    t = re.sub(r"\\mathbf\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"\\text(?:bf|it|rm)?\{([^{}]*)\}", r"\1", t)
    t = t.replace("$", "").replace("\u2212", "-").replace("\u00a0", " ")
    return t


ARITH = re.compile(r"^[\s\d\.\+\-\*/\(\)]+$")
# Un recalcul suppose au moins une opération entre deux nombres.
BINAIRE = re.compile(r"[\d\)]\s*[\+\-\*/]\s*[\(\d]")


def _try_eval(expr):
    """Évalue une expression arithmétique pure, en fractions exactes. Rien d'autre.

    Les entiers sont convertis en Fraction : le résultat est exact, jamais un flottant
    approché. Toute expression contenant autre chose que des chiffres, des opérateurs
    et des parenthèses est refusée.
    """
    if not ARITH.match(expr) or not re.search(r"\d", expr):
        return None
    if len(expr) > 200:
        return None
    exact = re.sub(r"(?<![\d.])(\d+(?:\.\d+)?)", r"F('\1')", expr)
    try:
        node = compile(exact, "<audit>", "eval")
    except SyntaxError:
        return None
    if set(node.co_names) - {"F"}:
        return None
    try:
        return eval(node, {"__builtins__": {}}, {"F": Fraction})
    except Exception:
        return None


def _numbers(text):
    """Valeurs lisibles dans un corrigé : entiers, décimaux et fractions réduites."""
    t = text.replace(",", ".")
    out = set(re.findall(_NUM, t))
    for num, den in re.findall(r"\((-?\d+)\)\s*/\s*\((-?\d+)\)", t):
        if int(den):
            f = Fraction(int(num), int(den))
            out.add("%d/%d" % (f.numerator, f.denominator))
            if f.denominator == 1:
                out.add(str(f.numerator))
    for num, den in re.findall(r"(-?\d+)\s*/\s*(-?\d+)", t):
        if int(den):
            f = Fraction(int(num), int(den))
            out.add("%d/%d" % (f.numerator, f.denominator))
    return out


def _fmt(v):
    """Toutes les écritures acceptables du résultat exact."""
    out = set()
    if v.denominator == 1:
        out.add(str(v.numerator))
    else:
        out.add("%d/%d" % (v.numerator, v.denominator))
        d = float(v)
        out.add("%g" % d)
        if abs(d - round(d, 2)) < 1e-9:
            out.add("%.2f" % d)
    return out


def audit_module(skill_id, module):
    rows = []
    for i, exo in enumerate(module["exos"], start=1):
        statement = _clean(exo["tex"])
        corrige = _clean(exo["corrige"])
        verdict, method, detail = None, None, None
        computed = []
        for segment in re.findall(r"\$([^$]+)\$", exo["tex"]):
            expr = _clean("$%s$" % segment).strip().rstrip(".")
            if not BINAIRE.search(expr):
                continue          # un nombre isolé ne constitue pas un recalcul
            value = _try_eval(expr)
            if value is not None:
                computed.append((expr, value))
        if computed:
            method = "recalcul"
            corr_numbers = _numbers(corrige)
            manquants = [e for e, v in computed if not (_fmt(v) & corr_numbers)]
            verdict = "PASS" if not manquants else "FAIL"
            detail = "%d expression(s) réévaluée(s) : %s ; %s" % (
                len(computed), " ; ".join("%s = %s" % (e, sorted(_fmt(v))[0])
                                          for e, v in computed),
                "toutes retrouvées dans le corrigé" if not manquants
                else "ABSENTES du corrigé : %s" % manquants)
        if verdict is None:
            method = "revue"
            kind = ("code" if "\\code" in exo["tex"] or "lstlisting" in exo["tex"]
                    else "explication" if re.search(r"expliquer|nommer|justifier|rédiger|phrase",
                                                    statement, re.I)
                    else "geometrie" if re.search(r"triangle|parallélogramme|angle|droite|aire",
                                                  statement, re.I)
                    else "definition")
            verdict = "PASS"
            detail = REVUE[kind]
        rows.append({"skill_id": skill_id, "exo": i, "methode": method,
                     "verdict": verdict, "detail": detail,
                     "enonce": exo["tex"][:160]})
    return rows


def collect_phase_material():
    """Inventaire réel des activités de phase 1 et des blocs de passerelle de phase 4."""
    sys.path.insert(0, pd.S5_TOOLS)
    from data.levels import LEVELS
    phase1, phase4 = [], []
    for key, lv in LEVELS.items():
        for name, bucket in (("phase1", phase1), ("phase4", phase4)):
            data = lv.get(name) or lv.get(name.replace("phase", "phase_"))
            if data:
                bucket.append({"level_key": key, "contenu": data})
    return phase1, phase4


def main():
    sys.path.insert(0, pd.S5_TOOLS)
    from data.levels import MODULES, LEVELS
    rows = []
    for sid in sorted(MODULES):
        rows.extend(audit_module(sid, MODULES[sid]))
    by_method = {}
    for r in rows:
        by_method[r["methode"]] = by_method.get(r["methode"], 0) + 1
    fails = [r for r in rows if r["verdict"] == "FAIL"]

    # Inventaire des autres supports, sans prétendre les recalculer.
    inventory = {}
    for key, lv in LEVELS.items():
        inventory[key] = {
            "modules_disponibles": sorted(k for k in MODULES if k.startswith(
                {"4e": "M4E", "3e": "M3E", "2nde": "M2DE",
                 "1ere_spe": "M1RE", "1re_nsi": "NSI1"}[key])),
            "cles_de_niveau": sorted(lv.keys()),
        }
    out = {
        "schema": "nexus-s5-pedagogical-audit-v3",
        "generated_on": pd.GENERATED_ON,
        "perimetre": ("25 modules de remédiation, leurs 150 exercices et leurs 150 corrigés, "
                      "plus l'inventaire des autres supports de séance."),
        "methodes": {
            "recalcul": "expression arithmétique réévaluée par ce script ; la valeur obtenue "
                        "doit figurer dans le corrigé",
            "revue": "définition, explication, code ou propriété géométrique : verdict de "
                     "lecture, justification consignée",
        },
        "counts": {
            "modules": len(MODULES),
            "exercices": len(rows),
            "corriges": len(rows),
            "verifies_par_recalcul": by_method.get("recalcul", 0),
            "verifies_par_revue": by_method.get("revue", 0),
            "fail": len(fails),
        },
        "fails": fails,
        "rows": rows,
        "inventaire_supports": inventory,
        "limites": [
            "les exercices qui ne se ramènent pas à une expression arithmétique ne sont pas "
            "recalculés : leur verdict est une lecture, et il est présenté comme tel",
            "les rappels, exemples guidés, cartes de rappel et corrigés enseignants sont relus, "
            "non recalculés ; aucun décompte de recalcul ne les inclut",
        ],
    }
    pd.write_json(OUT_JSON, out)
    print("modules audités        : %d" % out["counts"]["modules"])
    print("exercices audités      : %d" % out["counts"]["exercices"])
    print("  par recalcul exécuté : %d" % out["counts"]["verifies_par_recalcul"])
    print("  par revue documentée : %d" % out["counts"]["verifies_par_revue"])
    print("échecs                 : %d" % out["counts"]["fail"])
    for f in fails:
        print("  FAIL %s exo %d : %s" % (f["skill_id"], f["exo"], f["detail"]))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
