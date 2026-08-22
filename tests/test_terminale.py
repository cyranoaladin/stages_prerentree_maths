"""Garde-fous du pipeline Terminale (modules tle_spe et tle_nsi).

Ce pipeline est indépendant de `tools/build.py` : ces tests vérifient à la fois qu'il est
cohérent en lui-même, et qu'il n'a pas empiété sur le pipeline mathématique existant.

Trois familles de vérifications :

1. **Cohérence des sources** — registre, diagnostics et banque d'items se répondent, et la
   banque décrit exactement l'instrument passé par les élèves.
2. **Individualisation réelle** — chaque livret est construit sur le diagnostic de son
   élève, aucun document n'est le doublon d'un autre, et le contenu varie avec le profil.
3. **Confidentialité** — aucun nom d'élève hors des dossiers nominatifs, aucune fuite d'un
   élève dans le dossier d'un autre, aucun corrigé dans un document élève.
"""

from __future__ import annotations

import copy
import json
import re
import sys
import unicodedata
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.build_terminale import (  # noqa: E402
    MODULES,
    BuildError,
    slug,
    build_documents,
    check_sources,
    items_to_revisit,
    items_to_secure,
    worked_domains,
)

MODULE_ROOTS = {"tle_spe": ROOT / "tle_spe", "tle_nsi": ROOT / "tle_nsi"}
NOMINATIVE_DIRS = {"tle_spe": "04_NOMINATIFS", "tle_nsi": "05_NOMINATIFS"}


@pytest.fixture(scope="module")
def registry() -> dict:
    return json.loads((ROOT / "content/students_terminale.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def diagnostics() -> dict:
    return json.loads((ROOT / "content/diagnostics_terminale.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def items() -> dict:
    return json.loads((ROOT / "content/items_terminale.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def documents() -> dict[str, str]:
    return build_documents(ROOT)


def normalize(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


# --------------------------------------------------------------------------------------
# 1. Cohérence des sources
# --------------------------------------------------------------------------------------

def test_sources_are_consistent(registry, diagnostics, items):
    check_sources(registry, diagnostics, items)


def test_cohort_is_split_into_the_two_declared_groups(registry):
    groups = {group["id"]: group for group in registry["groupes"]}
    assert set(groups) == {"groupe-1-maths-nsi", "groupe-2-maths-pc"}
    counts: dict[str, int] = {}
    for student in registry["students"]:
        counts[student["groupe"]] = counts.get(student["groupe"], 0) + 1
    for group_id, group in groups.items():
        assert counts[group_id] == group["effectif"], (
            f"{group_id} : {counts[group_id]} élèves pour un effectif déclaré de "
            f"{group['effectif']}"
        )


def _modules_of(student: dict) -> set[str]:
    return {subject["module"] for subject in student["matieres"]} | {
        missing["module"] for missing in student.get("matieresSansDiagnostic", [])
    }


def test_every_group_1_student_follows_both_modules(registry):
    """Le groupe 1 est défini par « maths et NSI » : chacun doit avoir les deux modules."""
    for student in registry["students"]:
        if student["groupe"] != "groupe-1-maths-nsi":
            continue
        modules = _modules_of(student)
        assert modules == {"tle_spe", "tle_nsi"}, (
            f"{student['displayName']} est en groupe 1 mais ne suit que {sorted(modules)}"
        )


def test_every_student_follows_at_least_the_maths_module(registry):
    """Tous les élèves de la cohorte suivent les mathématiques, quel que soit leur groupe."""
    for student in registry["students"]:
        assert "tle_spe" in _modules_of(student), (
            f"{student['displayName']} ne suit pas le module de mathématiques"
        )


def test_a_student_outside_the_group_nominal_pair_states_what_they_actually_follow(registry):
    """Le groupe porte une combinaison nominale ; un élève peut ne pas la suivre exactement.

    Dans ce cas, son livret ne doit pas se contenter de l'étiquette du groupe : il doit
    annoncer les spécialités réellement suivies et expliquer le rattachement.
    """
    groups = {group["id"]: group for group in registry["groupes"]}
    for student in registry["students"]:
        override = student.get("specialites")
        if override is None:
            continue
        assert override != groups[student["groupe"]]["specialites"], (
            f"{student['displayName']} : surcharge inutile, identique à celle du groupe"
        )
        assert student.get("noteGroupe", "").strip(), (
            f"{student['displayName']} suit autre chose que la combinaison de son groupe "
            "sans qu'aucune note n'explique le rattachement"
        )


def test_group_2_students_do_not_follow_the_nsi_module(registry):
    for student in registry["students"]:
        if student["groupe"] != "groupe-2-maths-pc":
            continue
        modules = {subject["module"] for subject in student["matieres"]}
        assert "tle_nsi" not in modules, f"{student['displayName']} ne suit pas NSI"


# Les effectifs de groupe sont recopiés à la main dans plusieurs documents rédigés. Sans
# garde-fou, ils dérivent dès qu'un élève rejoint la cohorte.
DOCUMENTS_CITANT_LES_EFFECTIFS = (
    "tle_spe/05_SOURCES/stage_prerentree_terminale_maths.md",
    "tle_spe/00_MASTER/tle_spe_MASTER_Documentation_Stage.md",
    "tle_spe/01_ENSEIGNANT/tle_spe_Guide_Formateur.md",
    "README.md",
)


def test_prose_group_sizes_match_the_registry(registry):
    """Un effectif écrit dans un document doit être celui du registre."""
    expected = {group["libelle"].split("—")[0].strip(): group["effectif"]
                for group in registry["groupes"]}
    mismatches = []
    for relative in DOCUMENTS_CITANT_LES_EFFECTIFS:
        for line in (ROOT / relative).read_text(encoding="utf-8").splitlines():
            row = re.match(r"^\|\s*(Groupe \d)\s*\|[^|]*\|\s*(\d+)\s*\|", line)
            if not row:
                continue
            group, written = row.group(1), int(row.group(2))
            if group in expected and written != expected[group]:
                mismatches.append(
                    f"{relative} : « {group} » annoncé à {written}, "
                    f"le registre en compte {expected[group]}"
                )
    assert mismatches == [], mismatches


def test_total_cohort_size_is_stated_consistently(registry):
    total = len(registry["students"])
    written = {"8": "huit", "9": "neuf", "10": "dix"}
    stale = []
    for relative in DOCUMENTS_CITANT_LES_EFFECTIFS:
        text = (ROOT / relative).read_text(encoding="utf-8")
        for digits, word in written.items():
            if int(digits) == total:
                continue
            for form in (f"{digits} élèves", f"{word} élèves"):
                if form in text:
                    stale.append(f"{relative} : « {form} » alors que la cohorte en compte {total}")
    assert stale == [], stale


def test_every_declared_source_report_exists(registry):
    missing = [
        report
        for student in registry["students"]
        for subject in student["matieres"]
        for report in (subject["sourceStudentReport"], subject["sourceParentReport"])
        if not (ROOT / "Bilans" / report).exists()
    ]
    assert missing == [], f"Bilans PDF déclarés mais absents : {missing}"


def test_item_bank_matches_the_instrument_actually_taken(diagnostics, items):
    """Chaque entrée de banque doit reprendre l'énoncé exact du positionnement passé.

    C'est aussi le garde-fou principal contre une extraction dégradée. Avant la 6.16, pypdf
    restitue mal l'espacement de ces bilans et coupe les mots au milieu — « T erm inale »,
    « num érateur » — sans rien signaler. Les 18 énoncés étant comparés ici à une banque
    écrite à la main, caractère pour caractère, une telle dégradation fait échouer ce test
    plutôt que d'atteindre le livret d'un élève.
    """
    for diagnostic_id, diagnostic in diagnostics["diagnostics"].items():
        bank = items["instruments"][diagnostic["matiere"]]["items"]
        assert len(bank) == len(diagnostic["items"]) == 18
        for rank, (item, reference) in enumerate(zip(diagnostic["items"], bank), 1):
            assert item["question"] == reference["question"], f"{diagnostic_id} item {rank}"
            assert item["domaine"] == reference["domaine"], f"{diagnostic_id} item {rank}"


def test_every_bank_item_carries_a_corrected_variant(items):
    for subject, instrument in items["instruments"].items():
        for reference in instrument["items"]:
            where = f"{subject} item {reference['rang']}"
            for field in ("competence", "geste_correct", "variante", "corrige_variante"):
                assert reference[field].strip(), f"{where} : champ '{field}' vide"
            assert reference["variante"] != reference["question"], (
                f"{where} : la variante reprend l'énoncé du positionnement au lieu d'en "
                "proposer un autre"
            )


def test_every_domain_is_linked_to_the_terminale_programme(diagnostics, items):
    for diagnostic in diagnostics["diagnostics"].values():
        domains = items["instruments"][diagnostic["matiere"]]["domaines"]
        for domain in diagnostic["reussite_par_domaine"]:
            assert domain in domains, f"{domain} absent de la banque"
            for field in ("prerequis_premiere", "ouverture_terminale", "reference_programme"):
                assert domains[domain][field].strip(), f"{domain} : '{field}' vide"


def test_quadrants_cover_every_evaluated_domain(diagnostics):
    """Un domaine évalué appartient à exactement une case de la matrice."""
    for diagnostic_id, diagnostic in diagnostics["diagnostics"].items():
        card = diagnostic["carte_maitrise_confiance"]
        placed = [domain for values in card.values() for domain in values]
        assert sorted(placed) == sorted(diagnostic["reussite_par_domaine"]), diagnostic_id
        assert len(placed) == len(set(placed)), f"{diagnostic_id} : domaine classé deux fois"


def test_extracted_text_is_free_of_extraction_artefacts(diagnostics):
    raw = json.dumps(diagnostics, ensure_ascii=False)
    assert "--- p" not in raw, "un marqueur de page a fuité dans les diagnostics"
    assert "’" not in raw, "apostrophe typographique non normalisée"


def test_the_extraction_records_the_library_that_produced_it(diagnostics):
    assert diagnostics["extraitAvec"].startswith("pypdf ")
    major, minor = (int(part) for part in diagnostics["extraitAvec"].split()[1].split(".")[:2])
    assert (major, minor) >= (6, 16), (
        "les diagnostics committés ont été extraits par une version de pypdf qui coupe les "
        "mots ; régénérer avec pypdf >= 6.16"
    )


# --------------------------------------------------------------------------------------
# 2. Individualisation
# --------------------------------------------------------------------------------------

def test_every_student_and_subject_has_its_three_documents(registry, documents):
    for student in registry["students"]:
        for subject in student["matieres"]:
            module = MODULES[subject["module"]]
            suffix = student["slug"]
            if subject["matiere"] != module.subject_label:
                suffix = f"{student['slug']}_{slug(subject['matiere'])}"
            directory = f"{module.key}/{module.nominative_dir}/{student['slug']}"
            for name in (
                f"{module.key}_Livret_Individuel_{suffix}.md",
                f"{module.key}_Remediation_Ciblee_{suffix}_ELEVE.md",
                f"{module.key}_Remediation_Ciblee_{suffix}_PROF_Corrige.md",
            ):
                assert f"{directory}/{name}" in documents, f"document manquant : {name}"


def test_no_two_nominative_documents_are_identical(documents):
    seen: dict[str, str] = {}
    duplicates = []
    for relative, content in documents.items():
        if "NOMINATIFS" not in relative:
            continue
        if content in seen:
            duplicates.append(f"{relative} identique à {seen[content]}")
        seen[content] = relative
    assert duplicates == [], duplicates


def test_each_livret_reports_its_own_diagnostic(registry, diagnostics, documents):
    """Chaque livret cite son bilan source et les scores qui en proviennent."""
    for student in registry["students"]:
        for subject in student["matieres"]:
            module = MODULES[subject["module"]]
            diagnostic = diagnostics["diagnostics"][subject["diagnosticId"]]
            relative = next(
                key for key in documents
                if key.startswith(f"{module.key}/{module.nominative_dir}/{student['slug']}/")
                and "_Livret_Individuel_" in key
                and (subject["matiere"] == module.subject_label) != ("expertes" in key)
            )
            content = documents[relative]
            assert student["displayName"] in content
            assert Path(diagnostic["source_pdf"]).name in content
            assert diagnostic["date_bilan"] in content


def test_each_livret_reprend_toutes_les_erreurs_de_son_eleve(registry, diagnostics, items,
                                                            documents):
    """Aucune erreur du bilan ne doit manquer dans le livret : c'est le cœur du dispositif."""
    for student in registry["students"]:
        for subject in student["matieres"]:
            module = MODULES[subject["module"]]
            diagnostic = diagnostics["diagnostics"][subject["diagnosticId"]]
            bank = items["instruments"][subject["matiere"]]["items"]
            relative = next(
                key for key in documents
                if key.startswith(f"{module.key}/{module.nominative_dir}/{student['slug']}/")
                and "_Livret_Individuel_" in key
                and (subject["matiere"] == module.subject_label) != ("expertes" in key)
            )
            content = documents[relative]
            for rank, item, _reference in items_to_revisit(diagnostic, bank):
                assert item["question"] in content, (
                    f"{relative} : l'énoncé de l'item {rank} manque"
                )
                if item["origine_erreur"]:
                    assert item["origine_erreur"] in content, (
                        f"{relative} : l'origine de l'erreur de l'item {rank} manque"
                    )


def test_remediation_sheets_only_target_the_student_own_weaknesses(registry, diagnostics,
                                                                   items, documents):
    for student in registry["students"]:
        for subject in student["matieres"]:
            module = MODULES[subject["module"]]
            diagnostic = diagnostics["diagnostics"][subject["diagnosticId"]]
            bank = items["instruments"][subject["matiere"]]["items"]
            expected = {
                reference["variante"]
                for _rank, _item, reference in items_to_revisit(diagnostic, bank)
            } | {
                reference["variante"]
                for _rank, _item, reference in items_to_secure(diagnostic, bank)
            }
            relative = next(
                key for key in documents
                if key.startswith(f"{module.key}/{module.nominative_dir}/{student['slug']}/")
                and key.endswith("_ELEVE.md")
                and (subject["matiere"] == module.subject_label) != ("expertes" in key)
            )
            content = documents[relative]
            for reference in bank:
                present = reference["variante"] in content
                if reference["variante"] in expected:
                    assert present, f"{relative} : exercice attendu absent"
                else:
                    assert not present, (
                        f"{relative} : exercice hors profil, sur une compétence que cet "
                        "élève réussit avec assurance"
                    )


def test_priority_order_puts_wrong_certainties_first(diagnostics):
    for diagnostic_id, diagnostic in diagnostics["diagnostics"].items():
        ordered = worked_domains(diagnostic)
        wrong = diagnostic["carte_maitrise_confiance"].get("certitudes_a_revoir", [])
        for index, (domain, quadrant) in enumerate(ordered):
            if quadrant != "certitudes_a_revoir":
                remaining = [d for d, _q in ordered[index:]]
                assert not set(remaining) & set(wrong), (
                    f"{diagnostic_id} : une certitude erronée passe après un autre travail"
                )
                break


def test_a_student_without_diagnostic_gets_an_explicit_notice(registry, documents):
    for student in registry["students"]:
        for missing in student.get("matieresSansDiagnostic", []):
            module = MODULES[missing["module"]]
            relative = (
                f"{module.key}/{module.nominative_dir}/{student['slug']}/"
                f"{module.key}_Livret_Individuel_{student['slug']}.md"
            )
            content = documents[relative]
            assert "Diagnostic à établir" in content
            assert missing["motif"] in content
            assert "Aucune conclusion n'est donc formulée" in content
            if student.get("noteGroupe"):
                assert student["noteGroupe"] in content, (
                    f"{relative} : la note de rattachement au groupe manque"
                )
            for speciality in student.get("specialites", []):
                assert speciality in content
            # Pas de plan de remédiation : il n'y a rien à remédier tant qu'on ne sait rien.
            assert f"{module.key}_Remediation_Ciblee_{student['slug']}_ELEVE.md" not in "".join(
                key for key in documents
                if key.startswith(f"{module.key}/{module.nominative_dir}/{student['slug']}/")
            )


def test_homonym_students_are_never_merged(registry):
    """Deux élèves peuvent porter le même nom à des niveaux différents."""
    flagged = [s for s in registry["students"] if s.get("homonymeAvertissement")]
    assert flagged, "l'homonymie connue de la cohorte n'est plus signalée"
    for student in flagged:
        assert student["slug"] not in {
            path.name for path in (ROOT / "1re_nsi" / "05_NOMINATIFS").iterdir()
        }, f"{student['displayName']} partage un dossier avec son homonyme de Première"


# --------------------------------------------------------------------------------------
# 3. Confidentialité
# --------------------------------------------------------------------------------------

def _student_names(registry: dict) -> list[str]:
    return [name for student in registry["students"] for name in student["aliases"]]


def test_no_student_name_outside_nominative_and_dashboard_documents(registry):
    names = _student_names(registry)
    leaks = []
    for module_key, module_root in MODULE_ROOTS.items():
        nominative = NOMINATIVE_DIRS[module_key]
        for path in sorted(module_root.rglob("*")):
            if not path.is_file() or path.suffix not in {".md", ".py", ".csv"}:
                continue
            relative = path.relative_to(ROOT).as_posix()
            if nominative in path.parts or path.name.endswith("Tableau_Bord_Enseignant.md"):
                continue  # seul document commun autorisé à être nominatif
            text = path.read_text(encoding="utf-8", errors="ignore")
            for name in names:
                if normalize(name) in normalize(text):
                    leaks.append(f"{relative} : '{name}'")
    assert leaks == [], leaks


def test_no_student_appears_in_another_student_folder(registry):
    names = {student["slug"]: student["aliases"] for student in registry["students"]}
    leaks = []
    for module_key, module_root in MODULE_ROOTS.items():
        nominative = module_root / NOMINATIVE_DIRS[module_key]
        for path in sorted(nominative.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            for slug, aliases in names.items():
                if slug == path.parent.name:
                    continue
                for alias in aliases:
                    if normalize(alias) in normalize(text):
                        leaks.append(f"{path.relative_to(ROOT)} : '{alias}'")
    assert leaks == [], leaks


def test_student_facing_documents_carry_no_answer_key(registry):
    """Une feuille élève ne doit jamais contenir le corrigé — bug déjà rencontré (ERR-008)."""
    offenders = []
    for module_key, module_root in MODULE_ROOTS.items():
        nominative = module_root / NOMINATIVE_DIRS[module_key]
        for path in sorted(nominative.rglob("*_ELEVE.md")):
            text = path.read_text(encoding="utf-8")
            for marker in ("## Corrigé", "**Corrigé.**", "Relevé de maîtrise"):
                if marker in text:
                    offenders.append(f"{path.relative_to(ROOT)} : '{marker}'")
    assert offenders == [], offenders


def test_nominative_documents_all_carry_the_confidentiality_banner():
    for module_key, module_root in MODULE_ROOTS.items():
        nominative = module_root / NOMINATIVE_DIRS[module_key]
        for path in sorted(nominative.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            assert "DOCUMENT CONFIDENTIEL" in text, path.relative_to(ROOT)


def test_generated_documents_on_disk_are_up_to_date(documents):
    stale = [
        relative for relative, content in documents.items()
        if not (ROOT / relative).exists()
        or (ROOT / relative).read_text(encoding="utf-8") != content
    ]
    assert stale == [], (
        "Documents périmés : relancer `python3 tools/build_terminale.py`. " + str(stale)
    )


def test_relative_links_resolve():
    broken = []
    for module_root in MODULE_ROOTS.values():
        for path in sorted(module_root.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"\]\((\.[^)]+)\)", text):
                if not (path.parent / target).resolve().exists():
                    broken.append(f"{path.relative_to(ROOT)} -> {target}")
    assert broken == [], broken


# --------------------------------------------------------------------------------------
# 3 bis. Composition des paquets PDF
#
# Ces tests portent sur le *plan* d'assemblage, pas sur le rendu : ils s'exécutent sans
# pandoc ni WeasyPrint, donc partout, y compris en intégration continue.
# --------------------------------------------------------------------------------------

@pytest.fixture(scope="module")
def bundles():
    from tools.build_terminale_pdf import plan_bundles

    return plan_bundles(ROOT)


def test_every_session_has_its_own_pdf_in_both_modules(bundles):
    """Une séance est l'unité de travail : elle doit exister comme fichier à elle seule."""
    produced = {bundle.filename for bundle in bundles}
    missing = []
    for key in MODULES:
        label = "Tle_SPE" if key == "tle_spe" else "Tle_NSI"
        for number in range(1, 6):
            for name in (f"{label}_S{number}_PREPARATION_ENSEIGNANT.pdf",
                         f"{label}_S{number}_FICHE_ELEVE.pdf"):
                if name not in produced:
                    missing.append(name)
    assert missing == [], missing


def test_a_session_bundle_holds_only_that_session(bundles):
    """Le PDF de la séance 3 ne doit pas embarquer la séance 4."""
    strays = []
    for bundle in bundles:
        match = re.search(r"_S(\d)_(PREPARATION_ENSEIGNANT|FICHE_ELEVE)\.pdf$", bundle.filename)
        if not match:
            continue
        expected = f"_S{match.group(1)}_"
        for source in bundle.sources:
            if expected not in source.name:
                strays.append(f"{bundle.filename} contient {source.name}")
    assert strays == [], strays


def test_session_bundles_carry_the_expected_documents(bundles):
    """Préparation = fiche professeur + supports + cartes d'aide. Fiche élève = l'activité."""
    by_name = {bundle.filename: bundle for bundle in bundles}
    for key, module in MODULES.items():
        label = "Tle_SPE" if key == "tle_spe" else "Tle_NSI"
        supports = "SUPPORTS_Pratiques" if key == "tle_nsi" else "SUPPORTS_Manipulation"
        for number in range(1, 6):
            prof = by_name[f"{label}_S{number}_PREPARATION_ENSEIGNANT.pdf"]
            assert [source.name for source in prof.sources] == [
                f"{key}_S{number}_PROF_Fiche.md",
                f"{key}_S{number}_{supports}.md",
                f"{key}_S{number}_AIDES_Cartes.md",
            ], prof.filename

            eleve = by_name[f"{label}_S{number}_FICHE_ELEVE.pdf"]
            assert [source.name for source in eleve.sources] == [
                f"{key}_S{number}_ELEVE_Activite.md"
            ], eleve.filename


def test_no_student_bundle_can_hold_a_teacher_document(bundles):
    """Le contrôle d'audience doit refuser l'assemblage, pas seulement nommer le fichier."""
    from tools.build_terminale_pdf import PdfBuildError, enforce_audience

    for bundle in bundles:
        if bundle.audience == "eleve":
            enforce_audience(bundle)   # ne doit rien lever

    victim = next(b for b in bundles if b.audience == "eleve")
    tampered = copy.deepcopy(victim)
    tampered.sources = list(tampered.sources) + [
        ROOT / "tle_spe/02_SEANCES/S1/tle_spe_S1_PROF_Fiche.md"
    ]
    with pytest.raises(PdfBuildError, match="document enseignant"):
        enforce_audience(tampered)


def test_student_directories_never_receive_a_teacher_bundle(bundles):
    """`eleves/` et `seances/` doivent rester sûrs à distribuer, dossier par dossier."""
    offenders = [
        f"{bundle.directory}/{bundle.filename}"
        for bundle in bundles
        if bundle.directory in ("eleves", "seances") and bundle.audience != "eleve"
    ]
    assert offenders == [], offenders


def test_every_planned_source_exists(bundles):
    missing = [
        str(source.relative_to(ROOT))
        for bundle in bundles for source in bundle.sources
        if not source.exists()
    ]
    assert missing == [], missing


# --------------------------------------------------------------------------------------
# 4. Non-régression sur le pipeline existant
# --------------------------------------------------------------------------------------

def test_terminale_modules_are_outside_the_maths_build_pipeline():
    """`tools/build.py` ne doit pas ramasser les modules Terminale.

    La constante est lue dans le source plutôt qu'importée : `tools/build.py` importe
    WeasyPrint dès son chargement, dépendance lourde qui n'a pas à conditionner ce test.
    """
    source = (ROOT / "tools/build.py").read_text(encoding="utf-8")
    declaration = re.search(r"^LEVELS = \((.*?)\)$", source, re.M)
    assert declaration, "déclaration LEVELS introuvable dans tools/build.py"
    levels = re.findall(r'"([^"]+)"', declaration.group(1))
    assert levels == ["4e", "3e", "2nde", "1ere_spe"]
    assert "tle_spe" not in levels and "tle_nsi" not in levels

    registry_source = (ROOT / "tools/student_registry.py").read_text(encoding="utf-8")
    registry_levels = re.search(r"^LEVELS = \((.*?)\)$", registry_source, re.M)
    assert registry_levels, "déclaration LEVELS introuvable dans tools/student_registry.py"
    assert "tle_" not in registry_levels.group(1)


def test_the_existing_student_registry_is_untouched():
    registry = json.loads((ROOT / "content/students.json").read_text(encoding="utf-8"))
    assert registry["scope"] == "stages_maths_2026"
    assert len(registry["students"]) == 13
    assert all(
        student["level"] in {"4e", "3e", "2nde", "1ere_spe"}
        for student in registry["students"]
    )


def test_check_sources_rejects_a_diagnostic_under_another_name(registry, diagnostics, items):
    broken = json.loads(json.dumps(registry))
    broken["students"][0]["aliases"] = ["Quelqu'un d'autre"]
    broken["students"][0]["displayName"] = "Quelqu'un d'autre"
    with pytest.raises(BuildError, match="absent des alias"):
        check_sources(broken, diagnostics, items)


def test_check_sources_rejects_a_bank_that_drifted_from_the_instrument(registry, diagnostics,
                                                                       items):
    broken = json.loads(json.dumps(items))
    broken["instruments"]["Mathématiques"]["items"][0]["question"] = "Autre énoncé."
    with pytest.raises(BuildError, match="énoncé divergent"):
        check_sources(registry, diagnostics, broken)
