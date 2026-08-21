#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Traçabilité et canonicalisation de la distribution.

Produit :
  _audit/source_evidence_manifest.json  chemin, SHA-256, type et usage de chaque
                                        source S1-S4 réellement exploitée, afin que
                                        l'audit soit reproductible sans le corpus.
  CANONICAL_DELIVERY.json               pour chaque élève, le document exact à
                                        distribuer, et les documents qu'il remplace.
"""

import sys
sys.dont_write_bytecode = True
import hashlib
import json
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core

ROOT = core.S5_ROOT
REPO = core.REPO_ROOT
DATE = "2026-08-21"

# Documents antérieurs, d'une autre architecture, que la présente livraison remplace.
SUPERSEDES = {
    "ines-kefi": ["Bilans/4e_Ines_Kefi_LIVRETS_S4_S5_PERSONNALISES.pdf"],
    "sinda-chikhaoui": ["Bilans/4e_Sinda_Chikhaoui_LIVRETS_S4_S5_PERSONNALISES.pdf"],
    "fares-darghouth": ["Nexus_4e_Fares_Darghouth_S4_S5_PDF/4e_S5_Fares_Darghouth_DOSSIER_ELEVE_PERSONNALISE.pdf",
                        "Nexus_4e_Fares_Darghouth_S4_S5_PDF/4e_Fares_Darghouth_LIVRETS_S4_S5_PERSONNALISES.pdf"],
}

TYPES = [
    ("_Dossier_Individuel_", "dossier individuel", "diagnostic initial, points d'appui, priorités"),
    ("_Remediation_Ciblee_", "plan de remédiation", "exercices déjà proposés à l'élève"),
    ("Test_Initial", "test de positionnement", "18 items du diagnostic initial"),
    ("02_SEANCES", "séance de niveau", "contenu réellement travaillé en S1 à S5"),
    ("_S2_", "livret personnalisé S2", "trajectoire individuelle"),
    ("_S3_", "livret personnalisé S3", "trajectoire individuelle"),
    ("_S4_", "livret personnalisé S4", "trajectoire individuelle"),
    ("_S5_", "livret personnalisé S5 antérieur", "architecture précédente, remplacée"),
    ("LIVRETS_S4_S5", "livret personnalisé S4+S5 antérieur", "architecture précédente, remplacée"),
    ("SOURCE_Bilan", "bilan de positionnement", "résultats par domaine"),
    ("06_CODE", "code Python du stage", "supports de programmation"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def classify(rel):
    for pat, kind, usage in TYPES:
        if pat in rel:
            return kind, usage
    return "source du stage", "contexte"


def main():
    sources = {}
    for st in core.all_students():
        for rel in core.student_sources(st):
            abs_ = os.path.join(REPO, rel)
            if os.path.isdir(abs_):
                for fn in sorted(os.listdir(abs_)):
                    if fn.endswith((".md", ".pdf")):
                        sources.setdefault(os.path.join(rel, fn), set()).add(st["id"])
            elif os.path.exists(abs_):
                sources.setdefault(rel, set()).add(st["id"])

    entries = []
    for rel in sorted(sources):
        abs_ = os.path.join(REPO, rel)
        kind, usage = classify(rel)
        st_ids = sorted(sources[rel])
        entries.append({
            "chemin_canonique": rel,
            "sha256": sha256(abs_),
            "taille_octets": os.path.getsize(abs_),
            "type_de_source": kind,
            "usage_dans_la_s5": usage,
            "eleves_concernes": st_ids,
            "matieres": sorted({core.level_of([s for s in core.all_students()
                                               if s["id"] == i][0])["subject"] for i in st_ids}),
        })

    # ce qui a été extrait de chaque source, élève par élève
    extraits = []
    for st in core.all_students():
        lv = core.level_of(st)
        rows = core.skill_table(st)
        extraits.append({
            "student_id": st["id"], "niveau": lv["key"], "matiere": lv["subject"],
            "dossier_individuel": [s for s in core.student_sources(st) if "Dossier_Individuel" in s],
            "observations_extraites": [{"domaine": d, "statut": s, "observation": o}
                                       for d, s, o in st["baseline"]["observations"]],
            "priorites_extraites": st["baseline"]["priorites"],
            "points_d_appui_extraits": st["baseline"]["appuis"],
            "competences_derivees": [{"skill_id": r["skill_id"],
                                      "statut_avant_s5": r["statut_avant_s5"],
                                      "preuve": r["preuve"]} for r in rows],
            "axes_retenus": {"P1": st["p1"], "P2": st["p2"]},
        })

    manifest = {
        "schema": "nexus-s5-source-evidence-v1",
        "genere_le": DATE,
        "objet": ("permettre de vérifier la traçabilité de la S5 vers les sources S1-S4 sans "
                  "disposer du corpus : chaque source exploitée est identifiée par son empreinte "
                  "SHA-256, et ce qui en a été extrait est consigné élève par élève"),
        "racine_de_reference": os.path.basename(REPO),
        "nb_sources": len(entries),
        "sources": entries,
        "extraits_par_eleve": extraits,
    }
    os.makedirs(os.path.join(ROOT, "_audit"), exist_ok=True)
    with open(os.path.join(ROOT, "_audit", "source_evidence_manifest.json"), "w",
              encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # ------------------------------------------------------ livraison canonique
    deliveries = []
    for st in core.all_students():
        lv = core.level_of(st)
        d = core.student_output_dir(st)
        td = os.path.join(d, "_ENSEIGNANT")
        work = os.path.join(d, core.doc_basename("TRAVAIL", st) + ".pdf")
        exam = os.path.join(d, core.doc_basename("EVALUATION", st) + ".pdf")
        teach = os.path.join(td, core.doc_basename("ENSEIGNANT", st) + ".pdf")
        for p in (work, exam, teach):
            if not os.path.exists(p):
                raise SystemExit("document canonique absent : %s" % p)
        deliveries.append({
            "student_id": st["id"], "student_name": st["name"],
            "level_key": lv["key"], "subject": lv["subject"],
            "canonical_work_pdf": os.path.relpath(work, REPO),
            "canonical_work_sha256": sha256(work),
            "canonical_assessment_pdf": os.path.relpath(exam, REPO),
            "canonical_assessment_sha256": sha256(exam),
            "teacher_pdf": os.path.relpath(teach, REPO),
            "teacher_pdf_sha256": sha256(teach),
            "ordre_de_remise": [
                "1. remettre le livret de travail au début de la séance",
                "2. ne remettre l'évaluation qu'à l'issue des 75 minutes de travail",
                "3. le dossier enseignant ne quitte jamais les mains de l'enseignant",
            ],
            "supersedes": [x for x in SUPERSEDES.get(st["id"], [])
                           if os.path.exists(os.path.join(REPO, x))],
            "supersedes_declares_introuvables": [x for x in SUPERSEDES.get(st["id"], [])
                                                 if not os.path.exists(os.path.join(REPO, x))],
            "supersedes_note": ("documents d'une architecture antérieure, conservés comme sources "
                                "mais à ne pas distribuer")
            if SUPERSEDES.get(st["id"]) else None,
        })
    canonical = {
        "schema": "nexus-s5-canonical-delivery-v1",
        "genere_le": DATE,
        "objet": "désigner sans ambiguïté le document à distribuer à chaque élève",
        "nb_eleves": len(deliveries),
        "regle": ("un document ne figurant pas dans cette liste ne doit pas être distribué au "
                  "titre de la séance 5"),
        "livraisons": deliveries,
    }
    with open(os.path.join(ROOT, "CANONICAL_DELIVERY.json"), "w", encoding="utf-8") as f:
        json.dump(canonical, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("source_evidence_manifest.json : %d sources empreintées" % len(entries))
    print("CANONICAL_DELIVERY.json       : %d élèves, %d documents remplacés"
          % (len(deliveries), sum(len(d["supersedes"]) for d in deliveries)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
