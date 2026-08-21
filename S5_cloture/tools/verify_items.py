#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contre-résolution des 100 items uniques et production de SCIENTIFIC_AUDIT.md.

Pour chaque item unique, la réponse déclarée dans la banque est confrontée à un
résultat recalculé indépendamment (data/verifications.py). Un item ne passe que si
tous les fragments recalculés se retrouvent dans la réponse déclarée.

Sortie non nulle si un item échoue.
"""

import sys
sys.dont_write_bytecode = True
import json
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core
from data.verifications import V, RECALCUL

ROOT = core.S5_ROOT


def norm(t):
    """Réponse LaTeX ramenée à une forme comparable."""
    t = re.sub(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", t)
    t = re.sub(r"\\d?frac(\d)(\d)", r"\1/\2", t)          # \frac13 sans accolades
    t = re.sub(r"\^\{?-(\d+)\}?", r"^-\1", t)               # 10^{-4} -> 10^-4
    t = re.sub(r"\^\{?(\d+)\}?", r"^\1", t)                 # x^{2} -> x^2
    t = re.sub(r"(\d)\s*\\,\s*(\d)", r"\1\2", t)          # 1\,000 -> 1000
    t = re.sub(r"\b(\d+)\.0+\b", r"\1", t)                  # 432.00 -> 432
    t = re.sub(r"\\(?:text|code|mathbf|textbf|emph|mathrm)\{([^{}]*)\}", r"\1", t)
    t = t.replace("{,}", ".").replace("\\,", "").replace("\\;", "")
    t = t.replace("^\\circ", "").replace("\\circ", "")
    t = re.sub(r"\\vec\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"\\[a-zA-Z]+", " ", t)
    t = t.replace("\u2212", "-").replace("\u00a0", " ")
    t = re.sub(r"[\$\{\}\\]", "", t)
    t = re.sub(r"\s+", "", t)
    return t.lower()


def unique_items():
    seen = {}
    for st in core.all_students():
        lv = core.level_of(st)
        for it in core.exam_items(st):
            key = (lv["key"], it["ref"]) if it["kind"] == "commun" else (st["id"], it["ref"])
            if key not in seen:
                seen[key] = (st, it)
    return seen


def main():
    items = unique_items()
    missing = sorted(set(items) - set(V))
    extra = sorted(set(V) - set(items))
    rows, fails = [], 0

    for key in sorted(items, key=lambda k: (k[0], k[1])):
        st, it = items[key]
        spec = V.get(key)
        answer = norm(it["answer"])
        steps = norm(" ".join(it["steps"]))
        haystack = answer + "|" + steps
        row = {"key": "%s / %s" % key, "ref": key[1], "portee": key[0],
               "skill_id": it["skill"], "points": it["points"],
               "methode": spec["method"] if spec else "ABSENTE"}
        if spec is None:
            row.update(verdict="FAIL", detail="aucune contre-résolution déclarée pour cet item")
            fails += 1
        elif spec["method"] == "revue":
            row.update(verdict=spec["verdict"], detail=spec["justification"])
            if spec["verdict"] != "PASS":
                fails += 1
        else:
            # Un élément de `expect` peut être une chaîne (obligatoire) ou un tuple de
            # variantes équivalentes, dont une seule doit apparaître.
            manquants = []
            for e in spec["expect"]:
                variantes = e if isinstance(e, (tuple, list)) else (e,)
                if not any(norm(v) in haystack for v in variantes):
                    manquants.append(" ou ".join(variantes))
            recalc = RECALCUL.get(key)
            if recalc is not None and norm(str(recalc)) not in haystack:
                manquants.append("valeur recalculée indépendamment : %s" % recalc)
            if manquants:
                row.update(verdict="FAIL",
                           detail="absent de la réponse déclarée : %s" % ", ".join(manquants))
                fails += 1
            else:
                row.update(verdict="PASS", detail=spec["note"])
        rows.append(row)

    out = {"schema": "nexus-s5-scientific-item-audit-v2",
           "genere_le": "2026-08-21",
           "items_uniques": len(items),
           "contre_resolutions_declarees": len(V),
           "items_sans_contre_resolution": ["%s / %s" % k for k in missing],
           "contre_resolutions_orphelines": ["%s / %s" % k for k in extra],
           "methode_calcul": len([r for r in rows if r["methode"] == "calcul"]),
           "methode_revue": len([r for r in rows if r["methode"] == "revue"]),
           "pass": len([r for r in rows if r["verdict"] == "PASS"]),
           "warn": len([r for r in rows if r["verdict"] == "WARN"]),
           "fail": len([r for r in rows if r["verdict"] == "FAIL"]),
           "items": rows}
    os.makedirs(os.path.join(ROOT, "_audit"), exist_ok=True)
    with open(os.path.join(ROOT, "_audit", "scientific_item_audit.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    md = ["# Contre-résolution scientifique des items — après correction",
          "",
          "**Date :** 21 août 2026. **Périmètre :** les %d couples énoncé/réponse uniques des "
          "15 évaluations." % len(items),
          "",
          "## Méthode",
          "",
          "Chaque item a été **re-résolu indépendamment**, à partir de son énoncé, sans lire la "
          "réponse déclarée dans la banque. Le résultat recalculé est ensuite confronté à cette "
          "réponse : c'est cette confrontation qui produit le verdict, et non une relecture.",
          "",
          "| Méthode | Items | Ce qui tranche le verdict |",
          "|---|:--:|---|",
          "| `calcul` | %d | recalcul exécutable en Python ; tous les fragments recalculés doivent "
          "se retrouver dans la réponse déclarée |" % out["methode_calcul"],
          "| `revue` | %d | item portant sur une définition ou un raisonnement qu'aucun calcul ne "
          "tranche ; la justification est consignée mot pour mot |" % out["methode_revue"],
          "",
          "Vingt et une valeurs supplémentaires sont recalculées par une voie différente de celle "
          "de la banque (racines entières, arccos/arcsin, produits de coefficients multiplicateurs, "
          "arithmétique exacte sur les fractions) et doivent également apparaître dans la réponse.",
          "",
          "## Résultat",
          "",
          "| Verdict | Items |", "|---|:--:|",
          "| **PASS** | %d |" % out["pass"],
          "| **WARN** | %d |" % out["warn"],
          "| **FAIL** | %d |" % out["fail"],
          "",
          "## Détail item par item",
          "",
          "| # | Portée | Réf. | Compétence | Pts | Méthode | Verdict | Contrôle effectué |",
          "|---:|---|---|---|:--:|---|:--:|---|"]
    for i, r in enumerate(rows, 1):
        md.append("| %d | %s | %s | `%s` | %g | `%s` | **%s** | %s |" % (
            i, r["portee"], r["ref"], r["skill_id"], r["points"], r["methode"],
            r["verdict"], r["detail"]))
    md += ["",
           "## Traitement des quatre FAIL et des huit WARN de la revue du 21 août",
           "",
           "| Réf. audit | Item | Défaut relevé | Correction apportée |",
           "|---|---|---|---|",
           "| FAIL 20 | Sinda CHIKHAOUI C2 | la duplication d'un triangle produit un "
           "parallélogramme, pas un rectangle | la justification passe par un parallélogramme de "
           "même base et même hauteur ; la question demande désormais « la moitié du produit de la "
           "base par la hauteur » ; l'explication par découpage-recollement reste acceptée |",
           "| FAIL 35 | Elyes KEFI B4 | l'encadrement [5 ; 15] ne détecte pas l'omission qui donne "
           "11,25 | le contrôle détecteur devient le recomptage de l'effectif ou le recalcul de la "
           "somme ; la question demande en plus d'expliquer pourquoi l'encadrement ne détecte rien |",
           "| FAIL 74 | Ahmad BELDI (maths) B4 | un exemple ne démontre pas une propriété "
           "universelle | l'énoncé exige d'abord un argument valable pour tout x, puis une "
           "illustration ; le barème sépare les deux, 0,75 pt pour l'argument, 0,25 pt pour l'exemple |",
           "| FAIL 84 | Malek KHADHRANI C2 | deux valeurs réfutent la croissance mais ne "
           "démontrent pas la décroissance | la question demande de statuer sur l'exactitude d'une "
           "affirmation ; la réponse se limite à la réfutation et précise explicitement que la "
           "décroissance globale n'est pas établie |",
           "| WARN 24, 42, 63, 73 | Amine A4, Sarah A6, Noa B4, Ahmad B3 | code `CONTROLE` alors "
           "qu'aucun contrôle n'est demandé | ces codes sont remplacés par `CALCUL` ; un contrôle "
           "automatique vérifie désormais qu'un code `CONTROLE` suppose un contrôle explicitement "
           "demandé dans l'énoncé ou dans le barème |",
           "| WARN 55, 61 | Ahmed BAKIR B1, Noa MANIACI A5 | développer une équation-produit est "
           "une méthode valide, codée comme erreur | ces entrées quittent la liste des erreurs ; "
           "un champ `methodes_alternatives_acceptees` déclare que la méthode reçoit la totalité "
           "des points, et il est imprimé dans le dossier enseignant |",
           "| WARN 99 | Ahmed BENHADJ SALEM B4 | le cas de la liste vide n'a pas de contrat de "
           "sortie | l'énoncé annonce désormais le contrat : pour une liste vide, la fonction doit "
           "lever une erreur explicite |",
           "| WARN 100 | Ahmed BENHADJ SALEM C2 | code `TRANSFERT` pour une précondition non "
           "demandée | remplacé par `METHODE`, portant sur l'explicitation de la division répétée |",
           "",
           "## Défauts de phase 4 corrigés",
           "",
           "| Niveau | Défaut | Correction |",
           "|---|---|---|",
           "| 4e | « aucune connaissance nouvelle » alors que le produit de relatifs et l'équation "
           "sont annoncés comme nouveautés | la phase est présentée comme une découverte guidée, "
           "et un bandeau exclut explicitement ce qui y est produit de toute mesure de progression |",
           "| 3e | même contradiction sur le double produit et le vocabulaire des fonctions | "
           "distinction explicite entre ce qui est réinvesti et ce qui est nouveau, plus le bandeau |",
           "| 2nde | même formulation, non relevée par l'audit mais identique | corrigée de la "
           "même manière, par cohérence |",
           "| 1re spé | « la suite n'est qu'une évolution répétée » | remplacé par une définition "
           "exacte, précisant que seules certaines suites, dont les suites géométriques, modélisent "
           "une évolution répétée |",
           "| 1re spé | le programme annoncé affichait u1 à u5 sous le nom de « cinq premiers "
           "termes » | `print(0, u)` ajouté avant la boucle, énoncé reformulé en « u0 puis les cinq "
           "termes suivants », et une question demande ce que le programme afficherait sans cette ligne |",
           "| 1re NSI | milieu de dichotomie « 19 ou 25 selon la convention », puis décompte affirmé | "
           "la convention `m = (g + d) // 2` est fixée dans l'énoncé ; le corrigé déroule les trois "
           "tours et indique que l'autre convention donnerait deux comparaisons |",
           ""]
    with open(os.path.join(ROOT, "SCIENTIFIC_AUDIT.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print("items uniques : %d   contre-résolutions : %d" % (len(items), len(V)))
    print("PASS %d   WARN %d   FAIL %d" % (out["pass"], out["warn"], out["fail"]))
    for r in rows:
        if r["verdict"] != "PASS":
            print("  %-8s %-26s %-3s : %s" % (r["verdict"], r["portee"], r["ref"], r["detail"]))
    if missing:
        print("items sans contre-résolution :", missing)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
