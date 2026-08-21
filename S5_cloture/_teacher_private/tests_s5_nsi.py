#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Correction automatique partielle des productions de code — NSI, séance 5.

CE QUE CE SCRIPT FAIT
    Il exécute des tests déterministes sur les fonctions que l'élève a écrites,
    et uniquement sur celles-ci. Pour chaque test il indique le cas traité, le
    résultat attendu, le résultat obtenu et une classification de l'écart.

CE QUE CE SCRIPT NE FAIT PAS
    Il ne note pas. Plusieurs questions de l'évaluation portent sur une trace
    écrite, une explication ou un invariant : elles ne sont pas automatisables et
    restent intégralement à la charge de l'enseignant. Le script les signale
    comme « correction pédagogique requise » plutôt que de les ignorer.

AVERTISSEMENT DE SÉCURITÉ — À LIRE AVANT TOUTE EXÉCUTION
    Exécuter le code d'un tiers, c'est lui donner les droits de votre compte.
    Un sous-processus assorti d'un délai n'est PAS une sandbox : il protège d'une
    boucle infinie, pas d'une lecture de vos fichiers, d'un accès réseau ou d'une
    écriture hors du répertoire de travail.

    Par conséquent, **l'exécution est désactivée par défaut**. Deux modes seulement :

      --mode relu       vous certifiez avoir lu la copie ligne par ligne et n'y avoir
                        trouvé ni import système, ni accès fichier, ni accès réseau.
                        L'exécution a lieu dans un sous-processus séparé, avec un
                        délai maximal, mais SANS ISOLATION : mêmes droits que vous.

      --mode conteneur  exécution dans un conteneur jetable : réseau désactivé,
                        système de fichiers en lecture seule sauf /tmp, aucun HOME
                        ni secret monté, utilisateur non privilégié, limites de CPU,
                        de mémoire et de processus, délai externe. C'est le seul
                        mode acceptable pour une copie non relue.

USAGE
    # voir ce qui est attendu, sans exécuter la moindre ligne
    python3 S5_cloture/_teacher_private/tests_s5_nsi.py --eleve ahmad-beldi-nsi --attendu

    # après relecture humaine de la copie
    python3 .../tests_s5_nsi.py --eleve ahmad-beldi-nsi --copie copie.py --mode relu

    # sans relecture : conteneur jetable
    python3 .../tests_s5_nsi.py --eleve ahmad-beldi-nsi --copie copie.py --mode conteneur

    # rapport JSON exploitable
    python3 .../tests_s5_nsi.py --eleve ... --copie ... --mode relu --json rapport.json
"""

import argparse
import json
import os
import subprocess
import sys
sys.dont_write_bytecode = True  # aucune trace de cache dans la livraison
import tempfile

# ---------------------------------------------------------------- banque de tests
# Chaque entrée décrit une fonction attendue et ses cas de test déterministes.
# "erreur_visee" indique ce que l'échec du cas révèle, selon la nomenclature du barème.
BANQUE = {
    "moyenne": {
        "item": "B2",
        "enonce": "corriger la fonction pour qu'elle renvoie la moyenne au lieu de l'afficher",
        "signature": "moyenne(valeurs)",
        "cas": [
            {"id": "B2-nominal", "args": [[4, 6]], "attendu": 5.0, "type": "cas nominal",
             "erreur_visee": "ALGORITHME"},
            {"id": "B2-un-element", "args": [[7]], "attendu": 7.0, "type": "cas limite",
             "erreur_visee": "ALGORITHME"},
            {"id": "B2-negatifs", "args": [[-2, -4]], "attendu": -3.0, "type": "cas nominal",
             "erreur_visee": "CALCUL"},
            {"id": "B2-renvoie-bien", "args": [[1, 3]], "attendu": 2.0, "type": "contrat",
             "erreur_visee": "CONCEPT",
             "note": "un résultat None signale que print a été conservé à la place de return"},
        ],
        "non_automatisable": "l'identification d'un appel provoquant une erreur (liste vide) et "
                             "son explication relèvent de la correction pédagogique",
    },
    "chercher": {
        "item": "C1",
        "enonce": "renvoyer l'indice du premier enregistrement dont la clé id vaut l'identifiant, sinon -1",
        "signature": "chercher(mesures, identifiant)",
        "cas": [
            {"id": "C1-present", "args": [[{"id": "C01"}, {"id": "C02"}, {"id": "C03"}], "C03"],
             "attendu": 2, "type": "cas nominal", "erreur_visee": "ALGORITHME"},
            {"id": "C1-premier", "args": [[{"id": "C01"}, {"id": "C02"}], "C01"],
             "attendu": 0, "type": "cas limite",
             "erreur_visee": "ALGORITHME",
             "note": "renvoyer -1 ici révèle une valeur sentinelle confondue avec l'indice 0"},
            {"id": "C1-absent", "args": [[{"id": "C01"}, {"id": "C02"}], "C09"],
             "attendu": -1, "type": "cas limite", "erreur_visee": "ALGORITHME"},
            {"id": "C1-vide", "args": [[], "C01"], "attendu": -1, "type": "cas limite",
             "erreur_visee": "ALGORITHME"},
            {"id": "C1-doublon", "args": [[{"id": "C01"}, {"id": "C02"}, {"id": "C01"}], "C01"],
             "attendu": 0, "type": "cas limite", "erreur_visee": "ALGORITHME",
             "note": "la première occurrence est attendue, non la dernière"},
        ],
        "non_automatisable": "l'énoncé de la précondition de tri et du gain de la dichotomie "
                             "est une explication : correction pédagogique",
    },
    "premier_negatif": {
        "item": "C2 (Ahmad BELDI)",
        "enonce": "renvoyer l'indice de la première valeur strictement négative, sinon -1",
        "signature": "premier_negatif(L)",
        "cas": [
            {"id": "C2A-nominal", "args": [[4, 7, -2, -5]], "attendu": 2, "type": "cas nominal",
             "erreur_visee": "ALGORITHME"},
            {"id": "C2A-aucun", "args": [[1, 2, 3]], "attendu": -1, "type": "cas limite",
             "erreur_visee": "ALGORITHME"},
            {"id": "C2A-premier", "args": [[-1, 5]], "attendu": 0, "type": "cas limite",
             "erreur_visee": "ALGORITHME"},
            {"id": "C2A-vide", "args": [[]], "attendu": -1, "type": "cas limite",
             "erreur_visee": "ALGORITHME"},
            {"id": "C2A-zero", "args": [[0, -3]], "attendu": 1, "type": "cas limite",
             "erreur_visee": "CONCEPT",
             "note": "zéro n'est pas strictement négatif"},
        ],
        "non_automatisable": None,
    },
    "triple": {
        "item": "phase 2, exercice 1",
        "enonce": "renvoyer le triple de n",
        "signature": "triple(n)",
        "cas": [
            {"id": "P2-1", "args": [7], "attendu": 21, "type": "cas nominal", "erreur_visee": "ALGORITHME"},
            {"id": "P2-2", "args": [0], "attendu": 0, "type": "cas limite", "erreur_visee": "CONCEPT",
             "note": "un résultat None révèle une fonction sans return"},
        ],
        "non_automatisable": None,
    },
    "somme": {
        "item": "phase 2, exercice 3",
        "enonce": "renvoyer la somme de a et b",
        "signature": "somme(a, b)",
        "cas": [
            {"id": "P2-3", "args": [2, 3], "attendu": 5, "type": "cas nominal", "erreur_visee": "CONCEPT",
             "note": "None révèle un print conservé à la place du return"},
        ],
        "non_automatisable": None,
    },
    "est_negatif": {
        "item": "phase 2, exercice 5",
        "enonce": "renvoyer True si n est strictement négatif",
        "signature": "est_negatif(n)",
        "cas": [
            {"id": "P2-5a", "args": [-3], "attendu": True, "type": "cas nominal", "erreur_visee": "ALGORITHME"},
            {"id": "P2-5b", "args": [5], "attendu": False, "type": "cas nominal", "erreur_visee": "ALGORITHME"},
            {"id": "P2-5c", "args": [0], "attendu": False, "type": "cas limite", "erreur_visee": "CONCEPT"},
        ],
        "non_automatisable": None,
    },
    "bilan": {
        "item": "phase 2, exercice 2 (Ahmed BENHADJ SALEM)",
        "enonce": "renvoyer la somme des éléments et le nombre de valeurs strictement négatives",
        "signature": "bilan(L)",
        "cas": [
            {"id": "P2B-1", "args": [[4, -2, 7, -1]], "attendu": [8, 2], "type": "cas nominal",
             "erreur_visee": "ALGORITHME"},
            {"id": "P2B-2", "args": [[]], "attendu": [0, 0], "type": "cas limite",
             "erreur_visee": "ALGORITHME"},
            {"id": "P2B-3", "args": [[5]], "attendu": [5, 0], "type": "cas limite",
             "erreur_visee": "ALGORITHME"},
        ],
        "non_automatisable": "l'énoncé de l'invariant et du variant est une explication : correction pédagogique",
    },
    "maximum": {
        "item": "phase 2, exercice 5 / phase 3, exercice 1",
        "enonce": "renvoyer la plus grande valeur d'une liste non vide",
        "signature": "maximum(L)",
        "cas": [
            {"id": "P3-1", "args": [[3, 9, 2]], "attendu": 9, "type": "cas nominal", "erreur_visee": "ALGORITHME"},
            {"id": "P3-2", "args": [[5]], "attendu": 5, "type": "cas limite", "erreur_visee": "ALGORITHME"},
            {"id": "P3-3", "args": [[-4, -1]], "attendu": -1, "type": "cas limite", "erreur_visee": "ALGORITHME",
             "note": "une initialisation à 0 échoue précisément ici"},
        ],
        "non_automatisable": "la justification de l'initialisation est une explication : correction pédagogique",
    },
    "indice_de": {
        "item": "phase 4, bloc A",
        "enonce": "renvoyer l'indice de la première occurrence de la cible, sinon -1",
        "signature": "indice_de(L, cible)",
        "cas": [
            {"id": "P4-1", "args": [[7, 3, 9, 3], 3], "attendu": 1, "type": "cas nominal",
             "erreur_visee": "ALGORITHME"},
            {"id": "P4-2", "args": [[7, 3, 9], 5], "attendu": -1, "type": "cas limite",
             "erreur_visee": "ALGORITHME"},
            {"id": "P4-3", "args": [[], 5], "attendu": -1, "type": "cas limite",
             "erreur_visee": "ALGORITHME"},
        ],
        "non_automatisable": "la justification de la valeur -1 est une explication : correction pédagogique",
    },
}

# Questions de l'évaluation qui ne peuvent pas être corrigées automatiquement.
CORRECTION_PEDAGOGIQUE = {
    "ahmad-beldi-nsi": [
        ("A5", "valeur de r et explication du None — réponse écrite"),
        ("A6", "valeurs de range et nombre de tours — réponse écrite"),
        ("B1", "tableau d'état d'un accumulateur — trace écrite"),
        ("B3", "lecture d'un extrait CSV et métadonnée — réponse écrite"),
        ("B4", "indexation et effet d'un alias — explication écrite"),
    ],
    "ahmed-benhadj-salem": [
        ("A5", "valeur finale d'un accumulateur et nombre de tours — réponse écrite"),
        ("A6", "choix for/while justifié — réponse écrite"),
        ("B1", "tableau d'état d'un accumulateur — trace écrite"),
        ("B2", "None, correction par return et cas limite — explication écrite"),
        ("B3", "lecture d'un extrait CSV et métadonnée — réponse écrite"),
        ("B4", "jeu de tests, assertion et problème des flottants — explication écrite"),
        ("C2", "coût comparé et invariant de la dichotomie — explication écrite"),
    ],
}

FONCTIONS_PAR_ELEVE = {
    "ahmad-beldi-nsi": ["triple", "somme", "est_negatif", "moyenne", "indice_de",
                        "chercher", "premier_negatif"],
    "ahmed-benhadj-salem": ["bilan", "maximum", "moyenne", "indice_de", "chercher"],
}

DRIVER = r'''
import contextlib, importlib.util, io, json, sys, traceback
copie, plan_json, sortie = sys.argv[1], sys.argv[2], sys.argv[3]
out = {"import_error": None, "results": []}
buf = io.StringIO()
spec = importlib.util.spec_from_file_location("copie_eleve", copie)
mod = importlib.util.module_from_spec(spec)
try:
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)
except Exception:
    out["import_error"] = traceback.format_exc(limit=3)
    open(sortie, "w", encoding="utf-8").write(json.dumps(out))
    sys.exit(0)
for nom, cas_list in json.loads(plan_json):
    fn = getattr(mod, nom, None)
    if fn is None:
        out["results"].append({"fonction": nom, "cas": None, "statut": "ABSENTE"})
        continue
    if not callable(fn):
        out["results"].append({"fonction": nom, "cas": None, "statut": "NON_APPELABLE"})
        continue
    for cas in cas_list:
        rec = {"fonction": nom, "cas": cas["id"]}
        b = io.StringIO()
        try:
            with contextlib.redirect_stdout(b):
                got = fn(*cas["args"])
            if isinstance(got, tuple):
                got = list(got)
            rec["obtenu"] = got
            rec["affichage"] = b.getvalue().strip()[:200]
            rec["statut"] = "OK" if got == cas["attendu"] else "ECHEC"
        except Exception as exc:
            rec["obtenu"] = None
            rec["affichage"] = b.getvalue().strip()[:200]
            rec["statut"] = "EXCEPTION"
            rec["exception"] = "%s: %s" % (type(exc).__name__, exc)
        out["results"].append(rec)
open(sortie, "w", encoding="utf-8").write(json.dumps(out))
'''


def attendu(eleve):
    noms = FONCTIONS_PAR_ELEVE[eleve]
    print("Fonctions attendues dans la copie de %s :\n" % eleve)
    for n in noms:
        b = BANQUE[n]
        print("  %-18s %s" % (b["signature"], b["enonce"]))
        print("  %-18s item %s, %d cas de test" % ("", b["item"], len(b["cas"])))
        if b["non_automatisable"]:
            print("  %-18s correction pédagogique : %s" % ("", b["non_automatisable"]))
        print()
    print("Questions non automatisables pour cet élève :")
    for ref, quoi in CORRECTION_PEDAGOGIQUE[eleve]:
        print("  %-4s %s" % (ref, quoi))


DOCKER_IMAGE = "python:3-slim"


def _docker_available():
    try:
        r = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=20)
        return r.returncode == 0
    except Exception:
        return False


def run(copie, eleve, timeout, mode):
    """Exécute les tests. `mode` vaut « relu » (sous-processus) ou « conteneur »."""
    noms = FONCTIONS_PAR_ELEVE[eleve]
    plan = [[n, BANQUE[n]["cas"]] for n in noms]
    workdir = tempfile.mkdtemp(prefix="s5nsi_")
    driver = os.path.join(workdir, "driver.py")
    resultat = os.path.join(workdir, "resultat.json")
    with open(driver, "w", encoding="utf-8") as f:
        f.write(DRIVER)
    try:
        if mode == "conteneur":
            if not _docker_available():
                return {"import_error": "mode conteneur demandé mais Docker n'est pas utilisable "
                                        "sur cette machine. Relisez la copie et employez "
                                        "--mode relu, ou installez un moteur de conteneurs.",
                        "results": [], "isolation": "aucune (exécution refusée)"}
            has_image = subprocess.run(["docker", "image", "inspect", DOCKER_IMAGE],
                                       capture_output=True, text=True).returncode == 0
            if not has_image:
                return {"import_error": "l'image %s n'est pas présente localement. Le mode "
                                        "conteneur ne télécharge rien de lui-même : préparez-la "
                                        "d'abord avec « docker pull %s », puis relancez."
                                        % (DOCKER_IMAGE, DOCKER_IMAGE),
                        "results": [], "isolation": "aucune (exécution refusée)"}
            cmd = [
                "docker", "run", "--rm",
                "--pull=never",                       # l'image doit être présente localement
                "--network=none",                     # aucun accès réseau
                "--read-only",                        # système de fichiers en lecture seule
                "--tmpfs", "/tmp:rw,noexec,nosuid,size=32m",
                "--user", "65534:65534",              # utilisateur non privilégié
                "--memory=256m", "--pids-limit=64", "--cpus=0.5",
                "--security-opt", "no-new-privileges",
                "--cap-drop", "ALL",
                "--env", "HOME=/tmp",                 # aucun HOME réel monté
                "-v", "%s:/travail/driver.py:ro" % driver,
                "-v", "%s:/travail/copie.py:ro" % os.path.abspath(copie),
                "-v", "%s:/sortie" % workdir,
                "-w", "/travail",
                DOCKER_IMAGE,
                "python", "/travail/driver.py", "/travail/copie.py",
                json.dumps(plan), "/sortie/resultat.json",
            ]
            # le conteneur tourne en utilisateur non privilégié : le répertoire de sortie,
            # créé par mktemp pour cette seule exécution, doit lui être ouvert en écriture.
            os.chmod(workdir, 0o777)
            isolation = ("conteneur jetable : réseau désactivé, FS en lecture seule sauf /tmp, "
                         "utilisateur non privilégié, 256 Mo, 64 processus, 0,5 CPU, "
                         "aucune image téléchargée implicitement")
        else:
            cmd = [sys.executable, driver, os.path.abspath(copie), json.dumps(plan), resultat]
            isolation = ("AUCUNE : sous-processus séparé avec délai maximal, mêmes droits que "
                         "le compte qui lance le script. Mode réservé à une copie relue.")
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return {"import_error": "délai de %d s dépassé : boucle infinie probable" % timeout,
                    "results": [], "isolation": isolation}
        if not os.path.exists(resultat):
            return {"import_error": (proc.stderr or "aucun résultat produit").strip()[:2000],
                    "results": [], "isolation": isolation}
        with open(resultat, encoding="utf-8") as f:
            body = f.read()
        if not body.strip():
            return {"import_error": (proc.stderr or "résultat vide").strip()[:2000],
                    "results": [], "isolation": isolation}
        out = json.loads(body)
        out["isolation"] = isolation
        return out
    finally:
        for f in (driver, resultat):
            if os.path.exists(f):
                os.unlink(f)
        try:
            os.rmdir(workdir)
        except OSError:
            pass


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--eleve", required=True, choices=sorted(FONCTIONS_PAR_ELEVE),
                    help="identifiant de l'élève de NSI")
    ap.add_argument("--copie", help="fichier Python contenant les fonctions de l'élève")
    ap.add_argument("--mode", choices=("relu", "conteneur"),
                    help="« relu » : sous-processus NON SANDBOXÉ, réservé à une copie "
                         "effectivement relue ligne par ligne. « conteneur » : conteneur "
                         "jetable isolé. Sans ce paramètre, aucune exécution n'a lieu.")
    ap.add_argument("--attendu", action="store_true",
                    help="affiche les fonctions attendues et sort, sans exécuter de code")
    ap.add_argument("--json", metavar="FICHIER", help="écrit le rapport détaillé en JSON")
    ap.add_argument("--timeout", type=int, default=10, help="délai maximal en secondes (défaut 10)")
    args = ap.parse_args()

    if args.attendu:
        attendu(args.eleve)
        return 0
    if not args.copie:
        ap.error("--copie est requis (ou utiliser --attendu)")
    if not os.path.exists(args.copie):
        print("fichier introuvable : %s" % args.copie, file=sys.stderr)
        return 2
    if not args.mode:
        print("EXÉCUTION REFUSÉE.\n\n"
              "Exécuter le code d'un élève revient à lui accorder les droits de votre compte.\n"
              "Ce script ne le fera pas sans instruction explicite. Choisissez un mode :\n\n"
              "  --mode relu        vous avez lu la copie ligne par ligne et n'y avez trouvé ni\n"
              "                     import système, ni accès fichier, ni accès réseau.\n"
              "                     L'exécution reste NON SANDBOXÉE.\n\n"
              "  --mode conteneur   exécution dans un conteneur jetable, sans réseau, en lecture\n"
              "                     seule, utilisateur non privilégié. Seul mode acceptable pour\n"
              "                     une copie non relue.\n\n"
              "Pour voir ce qui est attendu sans exécuter la moindre ligne : --attendu\n",
              file=sys.stderr)
        return 3
    if args.mode == "relu":
        print("AVERTISSEMENT : mode « relu ». L'exécution a lieu dans un sous-processus séparé,\n"
              "avec un délai maximal, mais SANS ISOLATION : le code de l'élève dispose des droits\n"
              "de votre compte. Ce mode suppose que vous avez relu la copie.\n")

    raw = run(args.copie, args.eleve, args.timeout, args.mode)
    rapport = {"schema": "nexus-s5-nsi-tests-v2", "eleve": args.eleve,
               "copie": os.path.basename(args.copie),
               "mode_execution": args.mode,
               "isolation": raw.get("isolation"),
               "import_error": raw["import_error"], "fonctions": [], "synthese": {},
               "correction_pedagogique_requise": [
                   {"item": r, "objet": q} for r, q in CORRECTION_PEDAGOGIQUE[args.eleve]],
               "avertissement": ("ces tests portent sur le comportement du code et sur lui seul : "
                                 "ils ne mesurent ni la lisibilité, ni la justification, ni la "
                                 "compréhension de l'algorithme.")}
    if raw["import_error"]:
        print("ERREUR À L'IMPORT DE LA COPIE (erreur de syntaxe ou exécution au niveau du module) :")
        print(raw["import_error"])
        rapport["synthese"] = {"classement": "SYNTAXE", "tests_ok": 0, "tests_total": 0}
    else:
        par_fn = {}
        for rec in raw["results"]:
            par_fn.setdefault(rec["fonction"], []).append(rec)
        ok_total = tot_total = 0
        for nom in FONCTIONS_PAR_ELEVE[args.eleve]:
            b = BANQUE[nom]
            recs = par_fn.get(nom, [])
            if recs and recs[0]["statut"] in ("ABSENTE", "NON_APPELABLE"):
                print("\n%-18s %s" % (b["signature"], recs[0]["statut"]))
                rapport["fonctions"].append({"fonction": nom, "item": b["item"],
                                             "statut": recs[0]["statut"], "cas": []})
                continue
            cas_out = []
            print("\n%-18s (item %s)" % (b["signature"], b["item"]))
            for cas, rec in zip(b["cas"], recs):
                tot_total += 1
                ok = rec["statut"] == "OK"
                ok_total += 1 if ok else 0
                verdict = ("OK" if ok else
                           ("EXCEPTION" if rec["statut"] == "EXCEPTION" else "ECHEC"))
                if ok:
                    classe = None
                elif rec["statut"] == "EXCEPTION":
                    classe = "SYNTAXE/EXECUTION"
                elif rec.get("obtenu") is None and rec.get("affichage"):
                    # la valeur est calculée puis affichée : la cause est le contrat
                    # de la fonction, pas l'algorithme.
                    classe = "CONCEPT"
                else:
                    classe = cas["erreur_visee"]
                print("   %-5s %-14s %-11s attendu %r, obtenu %r%s"
                      % (verdict, cas["id"], cas["type"], cas["attendu"], rec.get("obtenu"),
                         "" if ok else "   [%s]" % classe))
                if not ok and cas.get("note"):
                    print("         %s" % cas["note"])
                if not ok and rec.get("obtenu") is None and rec.get("affichage"):
                    print("         la fonction a AFFICHÉ %r au lieu de le renvoyer : "
                          "erreur de type CONCEPT (print au lieu de return)" % rec["affichage"])
                cas_out.append({"id": cas["id"], "type": cas["type"], "attendu": cas["attendu"],
                                "obtenu": rec.get("obtenu"), "statut": verdict,
                                "classe_erreur": classe, "note": cas.get("note"),
                                "affichage": rec.get("affichage"),
                                "exception": rec.get("exception")})
            if b["non_automatisable"]:
                print("   ---   correction pédagogique : %s" % b["non_automatisable"])
            rapport["fonctions"].append({"fonction": nom, "item": b["item"],
                                         "statut": "TESTEE", "cas": cas_out,
                                         "non_automatisable": b["non_automatisable"]})
        rapport["synthese"] = {"tests_ok": ok_total, "tests_total": tot_total,
                               "classement": ("ALGORITHME" if ok_total < tot_total else "CONFORME")}
        print("\n%d cas de test sur %d passés." % (ok_total, tot_total))

    print("\nÀ corriger manuellement pour cet élève :")
    for r, q in CORRECTION_PEDAGOGIQUE[args.eleve]:
        print("   %-4s %s" % (r, q))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(rapport, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("\nrapport écrit : %s" % args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
