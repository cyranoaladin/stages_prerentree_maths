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
from tools.latex_notation import (  # noqa: E402
    to_latex,
    unsupported_characters,
)


def as_written(text: str, module_key: str) -> str:
    """Le texte tel que le générateur l'écrit : converti en LaTeX, chimie comprise."""
    return to_latex(text, chemistry=module_key == "tle_pc")

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


def test_cohort_is_split_into_the_declared_groups(registry):
    groups = {group["id"]: group for group in registry["groupes"]}
    assert set(groups) == {
        "groupe-1-maths-nsi", "groupe-2-maths", "groupe-3-maths-pc", "groupe-4-pc",
    }
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


def test_every_student_follows_the_modules_their_group_declares(registry):
    """Le groupe déclare des modules ; l'élève doit suivre exactement ceux-là.

    Tous les élèves ne suivent pas les mathématiques : celui du groupe 4 ne suit que la
    physique-chimie. C'est le groupe, et lui seul, qui dit quels stages sont suivis.
    """
    groups = {group["id"]: group for group in registry["groupes"]}
    for student in registry["students"]:
        declared = set(groups[student["groupe"]]["modules"])
        assert _modules_of(student) == declared, (
            f"{student['displayName']} suit {sorted(_modules_of(student))} "
            f"alors que son groupe déclare {sorted(declared)}"
        )


def test_every_student_declares_the_specialities_they_actually_follow(registry):
    """Le groupe dit quels stages l'élève suit, pas quelles spécialités il a choisies.

    Deux élèves du groupe « stage de mathématiques » suivent aussi la physique-chimie, deux
    autres ne suivent que les mathématiques : le livret doit annoncer le vrai, et une note
    doit expliquer le rattachement dès que le groupe ne suffit pas à le déduire.
    """
    groups = {group["id"]: group for group in registry["groupes"]}
    for student in registry["students"]:
        specialities = student.get("specialites")
        assert specialities, f"{student['displayName']} : aucune spécialité déclarée"
        assert "Mathématiques" in specialities, (
            f"{student['displayName']} : tous les élèves de la cohorte suivent les maths"
        )
        stages = groups[student["groupe"]]["stages"]
        if set(specialities) != set(stages):
            assert student.get("noteGroupe", "").strip(), (
                f"{student['displayName']} suit {specialities} alors que son groupe couvre "
                f"{stages}, sans note expliquant le rattachement"
            )


def test_group_2_students_do_not_follow_the_nsi_module(registry):
    for student in registry["students"]:
        if student["groupe"] != "groupe-2-maths":
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


# Un module ne couvre plus toute la cohorte : « 8 élèves » est une phrase juste dans le
# module de mathématiques, et fausse pour la cohorte. Le test ne peut donc plus bannir un
# nombre ; il vérifie la phrase qui annonce explicitement l'effectif de la cohorte.
NOMBRES_ECRITS = {
    "un": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5,
    "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10,
}
COHORTE_ANNONCEE = re.compile(
    r"[Ll]a cohorte compte (\d+|" + "|".join(NOMBRES_ECRITS) + r") élèves"
)


def test_total_cohort_size_is_stated_consistently(registry):
    total = len(registry["students"])
    stale = []
    for relative in DOCUMENTS_CITANT_LES_EFFECTIFS:
        text = (ROOT / relative).read_text(encoding="utf-8")
        for match in COHORTE_ANNONCEE.finditer(text):
            written = match.group(1)
            value = int(written) if written.isdigit() else NOMBRES_ECRITS[written]
            if value != total:
                stale.append(
                    f"{relative} : « la cohorte compte {written} élèves » "
                    f"alors qu'elle en compte {total}"
                )
    assert stale == [], stale


def test_each_module_states_how_many_of_the_cohort_it_covers(registry):
    """« 8 élèves » dans le module de mathématiques doit être le compte réel du module."""
    groups = {group["id"]: group for group in registry["groupes"]}
    covered = {
        key: sum(
            1 for student in registry["students"]
            if key in groups[student["groupe"]]["modules"]
        )
        for key in MODULES
    }
    assert covered["tle_spe"] == 8
    assert covered["tle_nsi"] == 4
    assert covered["tle_pc"] == 3
    assert sum(covered.values()) == sum(
        len(groups[student["groupe"]]["modules"]) for student in registry["students"]
    )


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
                # Le document compose l'énoncé en LaTeX ; c'est cette forme-là qu'on y
                # cherche, sans quoi le test comparerait deux notations différentes.
                assert as_written(item["question"], module.key) in content, (
                    f"{relative} : l'énoncé de l'item {rank} manque"
                )
                if item["origine_erreur"]:
                    assert as_written(item["origine_erreur"], module.key) in content, (
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
                present = as_written(reference["variante"], module.key) in content
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


def test_the_annual_option_is_folded_into_the_maths_livret(registry, diagnostics, documents):
    """L'option n'a pas de stage : elle vit dans le livret de mathématiques, pas à côté."""
    for student in registry["students"]:
        option = student.get("optionAnnuelle")
        if option is None:
            continue
        relative = (
            f"tle_spe/04_NOMINATIFS/{student['slug']}/"
            f"tle_spe_Livret_Individuel_{student['slug']}.md"
        )
        content = documents[relative]
        assert f"Option annuelle — {option['intitule']}" in content
        assert "Il n'y a pas de stage séparé pour cette option" in content

        # Le diagnostic d'option doit être repris, item par item, comme celui de la spécialité.
        option_diagnostic = diagnostics["diagnostics"][option["diagnosticId"]]
        for domain in option_diagnostic["reussite_par_domaine"]:
            assert domain in content, f"{relative} : domaine d'option '{domain}' absent"

        # Et il ne doit subsister aucun document séparé pour cette option.
        stray = [key for key in documents if "expertes" in key.lower()]
        assert stray == [], stray


def test_option_exercises_reach_both_remediation_sheets(registry, diagnostics, items, documents):
    for student in registry["students"]:
        option = student.get("optionAnnuelle")
        if option is None:
            continue
        option_diagnostic = diagnostics["diagnostics"][option["diagnosticId"]]
        bank = items["instruments"][option["intitule"]]["items"]
        expected = {
            reference["variante"]
            for _rank, _item, reference in items_to_revisit(option_diagnostic, bank)
        }
        base = f"tle_spe/04_NOMINATIFS/{student['slug']}/tle_spe_Remediation_Ciblee_{student['slug']}"
        eleve = documents[f"{base}_ELEVE.md"]
        prof = documents[f"{base}_PROF_Corrige.md"]
        for variante in expected:
            assert as_written(variante, "tle_spe") in eleve, (
                f"{student['displayName']} : exercice d'option absent"
            )
            assert as_written(variante, "tle_spe") in prof


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


def test_no_terminale_student_shares_a_folder_with_a_premiere_student(registry):
    """Un même patronyme peut exister à deux niveaux : les dossiers restent distincts."""
    premiere = {path.name for path in (ROOT / "1re_nsi" / "05_NOMINATIFS").iterdir()}
    for student in registry["students"]:
        assert student["slug"] not in premiere, (
            f"{student['displayName']} partage un répertoire avec un élève de Première"
        )
    for student in registry["students"]:
        if student.get("homonymeAvertissement"):
            assert student["homonymeAvertissement"].strip()


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
    from tools.build_terminale_pdf import file_label

    by_name = {bundle.filename: bundle for bundle in bundles}
    for key, module in MODULES.items():
        label = file_label(module)
        supports = module.supports_suffix
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


def test_terminale_tooling_adds_no_file_under_the_published_assets_tree():
    """`assets/` appartient au pipeline mathématique : rien de Terminale n'y entre.

    `tools/build.py` recopie l'intégralité de `assets/` dans les deux sites publiés, et
    chaque fichier publié entre dans MANIFEST_PUBLIC.csv et MANIFEST_PRIVATE.csv. Un seul
    fichier ajouté là fait diverger les manifests du pipeline mathématique et casse
    l'intégration continue, loin de sa cause — c'est arrivé avec la feuille de style
    d'impression Terminale, déplacée depuis sous `tools/assets/`.

    Le test compare l'arborescence réelle au manifeste committé : une addition légitime,
    accompagnée d'une régénération des manifests, continue de passer.
    """
    manifest = (ROOT / "MANIFEST_PUBLIC.csv").read_text(encoding="utf-8")
    published = {
        line.split(",")[0].removeprefix("dist/site-public/")
        for line in manifest.splitlines()[1:] if line
    }
    unpublished = [
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "assets").rglob("*"))
        if path.is_file() and path.relative_to(ROOT).as_posix() not in published
    ]
    assert unpublished == [], (
        "Fichier(s) sous assets/ absent(s) du manifeste publié : "
        + str(unpublished)
        + ". Les ressources propres aux modules Terminale vont sous tools/assets/."
    )


def test_the_terminale_charter_lives_outside_the_published_assets_tree():
    from tools.build_terminale_pdf import LATEX_STYLE

    assert LATEX_STYLE.exists(), "charte LaTeX Terminale introuvable"
    assert (ROOT / "assets") not in LATEX_STYLE.parents


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


# --------------------------------------------------------------------------- LaTeX
# Le rendu passe par LuaLaTeX. Un caractère que la police ne sait pas dessiner ne fait
# pas échouer la compilation : il laisse un trou dans la consigne, et personne ne le voit
# avant l'impression. Ces tests refusent la source plutôt que le PDF.

def test_no_document_carries_a_character_latex_cannot_typeset():
    offenders = {}
    for module in ("tle_spe", "tle_nsi", "tle_pc"):
        base = ROOT / module
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            left = unsupported_characters(path.read_text(encoding="utf-8"))
            if left:
                offenders[str(path.relative_to(ROOT))] = left
    assert offenders == {}, (
        "Notation Unicode à convertir en LaTeX : " + str(offenders)
        + ". Voir tools/mathify_terminale.py."
    )


def test_every_document_has_balanced_mathematics():
    """Un `$` orphelin fait basculer tout le reste du document en mode mathématique."""
    unbalanced = []
    for module in ("tle_spe", "tle_nsi", "tle_pc"):
        base = ROOT / module
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            fenced = display = False
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if line.startswith("```"):
                    fenced = not fenced
                    continue
                if fenced:
                    continue
                # Une formule hors-texte `$$…$$` s'étend souvent sur plusieurs lignes :
                # on suit son ouverture et sa fermeture avant de compter les `$` simples.
                opened = len(re.findall(r"(?<!\\)\$\$", line))
                stripped = re.sub(r"(?<!\\)\$\$", "", line)
                if display or opened:
                    display = (display + opened) % 2 == 1
                    if re.findall(r"(?<!\\)\$", stripped):
                        unbalanced.append(f"{path.relative_to(ROOT)}:{number}")
                    continue
                if len(re.findall(r"(?<!\\)\$", line)) % 2:
                    unbalanced.append(f"{path.relative_to(ROOT)}:{number}")
    assert unbalanced == [], "Délimiteur mathématique non refermé : " + str(unbalanced)


FRENCH_WORDS = re.compile(
    r"\b(?:le|la|les|de|des|du|et|ou|un|une|est|sont|pour|avec|dans|sur|par|que|qui"
    r"|pas|plus|moins|donc|alors|ainsi|entre|tout|tous|son|ses|cette|il|elle|on|aux)\b",
    re.IGNORECASE,
)


def test_no_french_prose_was_absorbed_into_a_formula():
    """La conversion reconnaît des motifs ; ce test vérifie qu'elle n'a pas trop pris."""
    absorbed = []
    for module in ("tle_spe", "tle_nsi", "tle_pc"):
        base = ROOT / module
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                # Les `$` s'apparient de gauche à droite : chercher chaque paire à partir
                # de la fin de la précédente, sinon le texte qui sépare deux formules
                # voisines passe lui-même pour une formule.
                for match in re.finditer(r"\$([^$\n]+)\$", re.sub(r"\$\$.*?\$\$", "", line)):
                    if FRENCH_WORDS.search(match.group(1)):
                        absorbed.append(f"{path.relative_to(ROOT)}:{number} ${match.group(1)}$")
    assert absorbed == [], "Prose française prise dans une formule : " + str(absorbed[:5])


def test_the_latex_charter_loads_the_packages_each_discipline_needs():
    charter = (ROOT / "tools/assets/nexus_terminale.sty").read_text(encoding="utf-8")
    required = {
        "amsmath": "mathématiques",
        "mathtools": "mathématiques",
        "esvect": "vecteurs à la française",
        "siunitx": "unités de physique",
        "mhchem": "équations de réaction",
        "chemfig": "formules développées",
        "listings": "code Python et SQL",
        "pgfplots": "courbes et repères",
        "babel": "typographie française",
    }
    missing = [name for name in required if name not in charter]
    assert missing == [], f"Paquets absents de la charte : {missing}"


def test_the_conversion_leaves_code_and_links_untouched():
    source = (
        "Voir `content/items_terminale.json` et [la fiche](../S1/tle_spe_S1_PROF_Fiche.md).\n"
        "```\nu₀ = 3 ; x ≥ 0\n```\n"
        "Mais ici u₀ = 3 devient des mathématiques.\n"
    )
    converted = to_latex(source)
    assert "`content/items_terminale.json`" in converted
    assert "(../S1/tle_spe_S1_PROF_Fiche.md)" in converted
    assert "```\nu₀ = 3 ; x ≥ 0\n```" in converted
    assert "$u_0 = 3$ devient" in converted


def test_the_conversion_is_stable_when_applied_twice():
    """Les documents committés sont déjà convertis : un second passage ne doit rien casser."""
    for module in ("tle_spe", "tle_nsi", "tle_pc"):
        base = ROOT / module
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            content = path.read_text(encoding="utf-8")
            assert to_latex(content) == content, (
                f"{path.relative_to(ROOT)} : la conversion n'est pas stable"
            )


# --------------------------------------------------- largeur des tableaux imprimés
# Le lecteur `gfm` de pandoc ne transporte aucune largeur de colonne : il produit des
# colonnes `l`, qui ne se coupent jamais. Les largeurs sont donc calculées à partir du
# contenu. Ces tests portent sur ce calcul, que l'intégration continue peut vérifier sans
# distribution TeX — la composition, elle, se contrôle à la construction des PDF, qui
# signale tout débordement de marge.

def _longtable(spec, rows):
    body = "\n" + "\\\\\n".join(rows) + "\\\\\n"
    return r"\begin{longtable}[]{@{}" + spec + "@{}}" + body + r"\end{longtable}"


def _column_shares(rebuilt):
    return [float(value) for value in re.findall(r"([\d.]+)\\linewidth", rebuilt)]


def test_a_narrow_table_keeps_its_content_sized_columns():
    from tools.build_terminale_pdf import size_tables

    table = _longtable("ll", ["Oui & Non", "Vrai & Faux"])
    assert size_tables(table) == table, "un tableau qui tient ne doit pas être redimensionné"


def test_a_wide_table_gets_proportional_wrapping_columns():
    from tools.build_terminale_pdf import size_tables

    rebuilt = size_tables(_longtable("ll", [
        "Erreur & Réponse",
        "Comparer les quantités brutes sans les coefficients & "
        "Faire poser le tableau, faire chercher quelle quantité s'annule la première",
    ]))
    shares = _column_shares(rebuilt)
    assert r"\raggedright" in rebuilt and "p{" in rebuilt
    assert len(shares) == 2
    assert abs(sum(shares) - 1.0) < 0.001, "les colonnes doivent occuper toute la justification"
    assert shares[1] > shares[0], "la colonne la plus fournie doit être la plus large"


def test_no_column_is_narrower_than_its_longest_word():
    """`**CONFRONTER**` débordait de 39 pt : un mot ne se coupe pas."""
    from tools.build_terminale_pdf import CHARACTERS_PER_LINE, size_tables

    rebuilt = size_tables(_longtable("lll", [
        "Rang & Domaine & Posture",
        r"1 & Fonction exponentielle & \textbf{CONFRONTER}",
        "2 & Suites numériques & Une réponse fausse a été donnée avec assurance, "
        "on part d'un cas qui met la conviction en défaut avant tout entraînement.",
    ]))
    shares = _column_shares(rebuilt)
    # « CONFRONTER » : dix capitales en gras, soit bien plus de dix chasses.
    assert shares[2] > 10 / CHARACTERS_PER_LINE, (
        f"la colonne des postures ne fait que {shares[2]:.3f} de la justification"
    )


def test_a_wide_sparse_table_tightens_its_gutters_instead_of_wrapping():
    """Dix-sept colonnes de quatre caractères : c'est le blanc qui déborde, pas le texte.

    C'est la table hexadécimal/décimal/binaire de la séance 1 de NSI, qui débordait de
    23 pt : le seul blanc entre ses colonnes dépasse la justification.
    """
    from tools.build_terminale_pdf import size_tables

    header = " & ".join(["Hex"] + list("0123456789ABCDEF"))
    decimal = " & ".join(["Déc"] + [str(n) for n in range(16)])
    binary = " & ".join(["Bin"] + [format(n, "04b") for n in range(16)])
    rebuilt = size_tables(_longtable("l" * 17, [header, decimal, binary]))
    assert r"\tabcolsep" in rebuilt and r"\small" in rebuilt
    assert "p{" not in rebuilt, "des cellules d'un caractère n'ont pas à être justifiées"


def test_ph_is_typeset_upright_inside_mathematics():
    """En italique, 10^{-pH} se lit comme le produit d'un p par un H."""
    converted = to_latex("[H₃O⁺] = 10^(−pH) et le pKa vaut 4,8.", chemistry=True)
    assert r"\mathrm{pH}" in converted
    assert "10^{ - pH}" not in converted
