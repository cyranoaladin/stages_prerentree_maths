# -*- coding: utf-8 -*-
"""Socle commun de la couche post-distribution V3.

Cette couche ne produit aucun sujet et ne modifie aucun document élève. Elle lit
les artefacts distribués en lecture seule et construit, à côté d'eux, ce qui
permet de les corriger et de les interpréter honnêtement.

Invariant tenu par tout ce module : aucune fonction n'ouvre un fichier de
``S5_cloture`` en écriture. Les seules écritures se font dans
``S5_post_distribution_v3``.
"""

import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True

V3_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(V3_ROOT)
S5_ROOT = os.path.join(REPO_ROOT, "S5_cloture")
S5_TOOLS = os.path.join(S5_ROOT, "tools")

SCHEMA_VERSION = "v3"
GENERATED_ON = "2026-08-21"

# Identifiant technique de l'élève fictif du jeu de tests : jamais un élève réel.
SYNTHETIC_ID = "eleve-synthetique-test"


class PostDistributionError(Exception):
    pass


# --------------------------------------------------------------------- accès
def _import_s5_data():
    """Importe les tables de données de S5_cloture sans écrire le moindre octet."""
    if S5_TOOLS not in sys.path:
        sys.path.insert(0, S5_TOOLS)
    import core  # noqa: E402
    return core


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path, label="fichier"):
    if not os.path.exists(path):
        raise PostDistributionError("%s introuvable : %s" % (label, path))
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    """Écriture atomique, et uniquement sous S5_post_distribution_v3."""
    full = os.path.abspath(path)
    if not full.startswith(V3_ROOT + os.sep):
        raise PostDistributionError(
            "écriture refusée hors de la couche post-distribution : %s" % full)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    tmp = full + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")
    os.replace(tmp, full)
    return full


def write_text(path, text):
    full = os.path.abspath(path)
    if not full.startswith(V3_ROOT + os.sep):
        raise PostDistributionError(
            "écriture refusée hors de la couche post-distribution : %s" % full)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    tmp = full + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
        if not text.endswith("\n"):
            f.write("\n")
    os.replace(tmp, full)
    return full


# ------------------------------------------------------------------- élèves
def students():
    """Les 15 couples élève x matière réellement distribués, dans un ordre stable."""
    core = _import_s5_data()
    out = []
    for st in core.all_students():
        if st["id"] == SYNTHETIC_ID:
            continue
        level = core.level_of(st)
        d = core.student_output_dir(st)
        out.append({
            "student_id": st["id"],
            "student_name": st["name"],
            "level_key": level["key"],
            "level_label": level["label"],
            "subject": level["subject"],
            "dir": d,
            "rel_dir": os.path.relpath(d, REPO_ROOT),
            "teacher_dir": os.path.join(d, "_ENSEIGNANT"),
            "travail_pdf": os.path.join(d, core.doc_basename("TRAVAIL", st) + ".pdf"),
            "travail_tex": os.path.join(d, core.doc_basename("TRAVAIL", st) + ".tex"),
            "evaluation_pdf": os.path.join(d, core.doc_basename("EVALUATION", st) + ".pdf"),
            "evaluation_tex": os.path.join(d, core.doc_basename("EVALUATION", st) + ".tex"),
        })
    out.sort(key=lambda s: (s["level_key"], s["student_id"]))
    return out


def manifest_of(student):
    return read_json(os.path.join(student["teacher_dir"], "evaluation_manifest.json"),
                     "manifeste d'évaluation")


def answer_key_of(student):
    return read_json(os.path.join(student["teacher_dir"], "answer_key.json"), "corrigé")


def profile_of(student):
    return read_json(os.path.join(student["dir"], "student_learning_profile.json"), "profil")


def skills_of_level(level_key):
    core = _import_s5_data()
    from data.levels import LEVELS
    return LEVELS[level_key]["skills"]
