# -*- coding: utf-8 -*-
"""Import du référentiel depuis la couche post-distribution V3.

Rien n'est ressaisi à la main : élèves, items, critères, points, classements
curriculaires, alias analytiques, méthodes acceptées, limites d'interprétation, réponses
attendues, sondes de certitude, contexte de rétention, diagnostics initiaux et
mini-tests différés viennent tous des fichiers V3, lus en JSON.

Chaque fichier lu est empreinté et consigné. Si une source change après l'import, la
divergence est signalée à l'écran ; elle n'est jamais résorbée en silence.
"""

import json
from decimal import Decimal
from pathlib import Path

from .. import config
from ..models import (Assessment, BaselineStatus, CriterionDefinition, DelayedCheck,
                      ImportSource, ItemDefinition, Person, SkillReference, Student,
                      VirtualCriterionDefinition)
from ..security import sha256_file
from . import points


class ImportError_(Exception):
    pass


def _read(path: Path, sources: list, kind: str, schema_version: str = ""):
    path = Path(path)
    if not path.exists():
        raise ImportError_("source V3 introuvable : %s" % path)
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    sources.append({"source_path": str(path), "source_sha256": sha256_file(path),
                    "kind": kind,
                    "schema_version": schema_version or payload.get("schema", "")})
    return payload


def _person_id(student_id: str, display_name: str) -> str:
    """Une personne, plusieurs inscriptions. Le nom n'est pas la clé, il l'illustre."""
    base = display_name.strip().lower().replace(" ", "-")
    return "p-" + "".join(c for c in base if c.isalnum() or c == "-")


def _artifact_index(freeze: dict) -> dict:
    idx = {}
    for art in freeze.get("artifacts", []):
        idx.setdefault(art["student_id"], {})[(art["nature"], art["format"])] = art
    return idx


def _cloture_dir(pdf_relpath: str) -> Path:
    return (config.REPO_ROOT / pdf_relpath).parent


def run_import(session, v3_root: Path = None) -> dict:
    """Importe l'intégralité du référentiel. Idempotent : il refuse une base déjà peuplée."""
    v3_root = Path(v3_root or config.V3_ROOT)
    if session.query(Student).count():
        raise ImportError_("la base contient déjà un référentiel ; utiliser un import "
                           "explicite de remplacement")
    sources = []
    freeze = _read(v3_root / "IMMUTABLE_STUDENT_ARTIFACTS.json", sources, "immutability")
    scope = _read(v3_root / "curriculum_scope" / "criteria_scope.json", sources, "criteria_scope")
    aliases = _read(v3_root / "curriculum_scope" / "analysis_skills.json", sources,
                    "analysis_skills")
    delayed = _read(v3_root / "teacher_guidance" / "mini_test_differe_s2.json", sources,
                    "delayed_checks")

    artifacts = _artifact_index(freeze)
    alias_by_id = {a["analysis_skill_id"]: a for a in aliases.get("aliases", [])}
    scope_by_criterion = {c["criterion_id"]: c for c in scope["criteria"]}

    stats = {"persons": 0, "students": 0, "assessments": 0, "items": 0, "criteria": 0,
             "virtual_criteria": 0, "skills": 0, "baselines": 0, "delayed_checks": 0}
    persons = {}
    seen_skills = set()

    for policy_path in sorted((v3_root / "correction_overlays").glob("*/CORRECTION_POLICY.json")):
        student_dir = policy_path.parent
        policy = _read(policy_path, sources, "correction_policy")
        overlay = _read(student_dir / "ANSWER_KEY_OVERLAY.json", sources, "answer_key_overlay")
        sid = policy["student_id"]
        art = artifacts.get(sid)
        if not art:
            raise ImportError_("aucun artefact figé pour l'élève %s" % sid)

        pid = _person_id(sid, policy["student_name"])
        if pid not in persons:
            session.add(Person(person_id=pid, display_name=policy["student_name"]))
            persons[pid] = True
            stats["persons"] += 1

        session.add(Student(student_id=sid, person_id=pid, level_key=policy["level_key"],
                            level_label=policy["level_label"], subject=policy["subject"]))
        stats["students"] += 1
        # Les tables sans relationship() ne participent pas au tri de dépendance du flush :
        # on garantit l'ordre d'insertion nous-mêmes.
        session.flush()

        eval_pdf = art[("evaluation", "pdf")]
        trav_pdf = art[("travail", "pdf")]
        aid = "asm-%s" % sid
        split = policy["curriculum_split"]
        session.add(Assessment(
            assessment_id=aid, student_id=sid, subject=policy["subject"],
            level_key=policy["level_key"],
            evaluation_pdf_path=eval_pdf["path"], evaluation_pdf_sha256=eval_pdf["sha256"],
            travail_pdf_path=trav_pdf["path"], travail_pdf_sha256=trav_pdf["sha256"],
            distributed_on=policy.get("generated_on"),
            max_points_centi=points.to_centi(split["total_points"]),
            n_minus_1_available_centi=points.to_centi(split["n_minus_1_available_points"]),
            bridge_available_centi=points.to_centi(split["bridge_n_available_points"]),
            estimated_duration_minutes=int(round(policy.get("estimated_duration_minutes") or 0)),
            status="NOT_STARTED"))
        stats["assessments"] += 1
        session.flush()

        # Énoncés, étapes et erreurs probables : ils vivent dans le manifeste enseignant.
        manifest_path = _cloture_dir(eval_pdf["path"]) / "_ENSEIGNANT" / "evaluation_manifest.json"
        manifest = _read(manifest_path, sources, "evaluation_manifest")
        man_items = {i["ref"]: i for i in manifest["items"]}

        for position, ov_item in enumerate(overlay["items"], start=1):
            mi = man_items[ov_item["ref"]]
            session.add(ItemDefinition(
                item_id=ov_item["item_id"], assessment_id=aid, ref=ov_item["ref"],
                position=position, part=ov_item["part"], kind=ov_item["kind"],
                statement=mi["statement"],
                max_points_centi=points.to_centi(ov_item["original_points"]),
                expected_answer=ov_item.get("original_expected_answer"),
                significant_steps_json=json.dumps(mi.get("significant_steps") or [],
                                                  ensure_ascii=False),
                likely_errors_json=json.dumps(mi.get("likely_errors") or [],
                                              ensure_ascii=False),
                accepted_methods_json=json.dumps(
                    mi.get("methodes_alternatives_acceptees") or [], ensure_ascii=False),
                teacher_observation_non_scored_json=json.dumps(
                    ov_item.get("teacher_observation_non_scored") or [], ensure_ascii=False),
                confidence_probe=bool(mi.get("confidence_probe")),
                comparison_status=ov_item.get("comparison_status"),
                estimated_duration_minutes_centi=points.to_centi(
                    ov_item.get("estimated_duration_minutes") or 0)))
            stats["items"] += 1

            for crit in ov_item["criteria"]:
                meta = scope_by_criterion.get(crit["criterion_id"], {})
                alias = alias_by_id.get(crit["analysis_skill_id"], {})
                retention = (ov_item.get("retention") or {}).get(crit["original_skill_id"])
                session.add(CriterionDefinition(
                    criterion_id=crit["criterion_id"], item_id=ov_item["item_id"],
                    rank=crit["criterion_rank"], subpart=crit.get("subpart"),
                    description=crit["desc"],
                    max_score_centi=points.to_centi(crit["original_points"]),
                    original_skill_id=crit["original_skill_id"],
                    analysis_skill_id=crit["analysis_skill_id"],
                    analysis_skill_label=alias.get("label"),
                    curriculum_scope=crit["curriculum_scope"],
                    evidence_type=crit["evidence_type"],
                    evidence_quality=crit.get("evidence_quality", "standard"),
                    scope_rationale=crit.get("scope_rationale") or meta.get("scope_rationale"),
                    accepted_methods_json=json.dumps(crit.get("accepted_methods") or [],
                                                     ensure_ascii=False),
                    interpretation_limits_json=json.dumps(
                        crit.get("interpretation_limits") or [], ensure_ascii=False),
                    fairness_rules_json=json.dumps(crit.get("fairness_rules") or [],
                                                   ensure_ascii=False),
                    error_codes_allowed_json=json.dumps(crit.get("error_codes_allowed") or [],
                                                        ensure_ascii=False),
                    printed_prompt=crit.get("printed_prompt"),
                    proof_levels_json=json.dumps(crit["proof_levels"], ensure_ascii=False)
                    if crit.get("proof_levels") else None,
                    teacher_correction=crit.get("teacher_correction"),
                    rejected_json=json.dumps({
                        "general_justification": crit.get("rejected_as_general_justification"),
                        "detection": crit.get("rejected_as_detection")},
                        ensure_ascii=False) if (
                            crit.get("rejected_as_general_justification")
                            or crit.get("rejected_as_detection")) else None,
                    retention_json=json.dumps(retention, ensure_ascii=False)
                    if retention else None))
                stats["criteria"] += 1

                for vrank, virt in enumerate(crit.get("virtual_subcriteria") or [], start=1):
                    valias = alias_by_id.get(virt["analysis_skill_id"], {})
                    session.add(VirtualCriterionDefinition(
                        virtual_criterion_id=virt["virtual_criterion_id"],
                        criterion_id=crit["criterion_id"], rank=vrank,
                        description=virt["desc"],
                        max_score_centi=points.to_centi(virt["points"]),
                        analysis_skill_id=virt["analysis_skill_id"],
                        analysis_skill_label=valias.get("label"),
                        curriculum_scope=virt["curriculum_scope"]))
                    stats["virtual_criteria"] += 1

        # Diagnostic initial et compétences du niveau : le profil porte les deux.
        profile_path = _cloture_dir(eval_pdf["path"]) / "student_learning_profile.json"
        profile = _read(profile_path, sources, "student_learning_profile")
        session.flush()
        for row in profile["baseline"]["skills"]:
            session.add(BaselineStatus(student_id=sid, skill_id=row["skill_id"],
                                       status_qualitative=row.get("statut_avant_s5"),
                                       evidence=row.get("preuve")))
            stats["baselines"] += 1
            key = (policy["level_key"], row["skill_id"])
            if key not in seen_skills:
                seen_skills.add(key)
                session.add(SkillReference(
                    level_key=policy["level_key"], analysis_skill_id=row["skill_id"],
                    label=row["label"], domain=row.get("domain"),
                    importance_n=row.get("importance_n"),
                    curriculum_scope="n_minus_1", is_alias=False,
                    original_skill_ids_json=json.dumps([row["skill_id"]], ensure_ascii=False)))
                stats["skills"] += 1

    # Alias analytiques : ils n'existent pas dans les profils, ils viennent de la V3.
    for alias in aliases.get("aliases", []):
        for level_key in alias.get("level_keys", []):
            key = (level_key, alias["analysis_skill_id"])
            if key in seen_skills:
                continue
            seen_skills.add(key)
            origin = (alias.get("original_skill_ids") or [None])[0]
            ref = session.query(SkillReference).filter_by(
                level_key=level_key, analysis_skill_id=origin).one_or_none()
            session.add(SkillReference(
                level_key=level_key, analysis_skill_id=alias["analysis_skill_id"],
                label=alias.get("label") or alias["analysis_skill_id"],
                domain=ref.domain if ref else None,
                importance_n=ref.importance_n if ref else "importante",
                curriculum_scope=alias.get("curriculum_scope", "n_minus_1"), is_alias=True,
                original_skill_ids_json=json.dumps(alias.get("original_skill_ids") or [],
                                                   ensure_ascii=False)))
            stats["skills"] += 1

    session.flush()
    for row in delayed.get("eleves", []):
        for sk in row.get("skills", []):
            session.add(DelayedCheck(
                student_id=row["student_id"], skill_id=sk["skill_id"], label=sk.get("label"),
                importance_n=sk.get("importance_n"), reason=sk.get("raison"),
                parallel_items_json=json.dumps(sorted(set(sk.get("items_paralleles") or [])),
                                               ensure_ascii=False)))
            stats["delayed_checks"] += 1

    for src in sources:
        session.add(ImportSource(**src))
    session.flush()
    stats["sources"] = len(sources)
    return stats


def check_sources_unchanged(session) -> list:
    """Compare les empreintes enregistrées à l'état actuel des fichiers V3."""
    drift = []
    for src in session.query(ImportSource).all():
        path = Path(src.source_path)
        if not path.exists():
            drift.append({"source_path": src.source_path, "etat": "disparue"})
            continue
        if sha256_file(path) != src.source_sha256:
            drift.append({"source_path": src.source_path, "etat": "modifiée depuis l'import",
                          "importee_le": src.imported_at.isoformat() if src.imported_at else None})
    return drift
