# -*- coding: utf-8 -*-
"""Confidentialité, exports, sauvegardes, et immutabilité de bout en bout."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from app import config, database
from app.domain import immutability
from conftest import fill

PROJECT = Path(config.PROJECT_DIR)
REPO = Path(config.REPO_ROOT)


def test_l_export_d_un_eleve_ne_contient_que_cet_eleve(client):
    student = "elyes-kefi"
    fill(client, student)
    client.post("/eleve/%s/valider" % student, follow_redirects=False)
    payload = client.get("/admin/export/%s" % student).json()
    assert payload["student_id"] == student
    texte = json.dumps(payload, ensure_ascii=False)
    autres = ["sarah-bargaoui", "ines-kefi", "ahmad-beldi", "noa-maniaci",
              "BARGAOUI", "KEFI, Ines", "MANIACI"]
    for autre in autres:
        assert autre not in texte, autre
    assert payload["correction"]["responses"]
    for row in payload["correction"]["responses"]:
        assert row["criterion_id"].startswith("3E_ELYES_KEFI")


def test_l_export_respecte_le_vocabulaire_v3(client):
    payload = client.get("/admin/export/elyes-kefi").json()
    row = payload["correction"]["responses"][0]
    assert set(("criterion_id", "score", "max_score", "error_codes", "observation",
                "criterion_scoring_status")) <= set(row)


def test_le_gitignore_couvre_les_donnees_reelles():
    contenu = (REPO / ".gitignore").read_text(encoding="utf-8")
    for regle in ("S5_correction_app/runtime/", "*.sqlite3", "corrections_reelles/",
                  "bilans_finaux/", "copies_eleves/", "responses_reelles/"):
        assert regle in contenu, regle


def test_aucune_donnee_reelle_n_est_suivie_par_git():
    script = PROJECT / "tools" / "check_runtime_not_tracked.py"
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True,
                            check=False)
    assert result.returncode == 0, result.stderr


def test_aucun_secret_n_est_inscrit_dans_le_depot():
    """Un secret est une chaîne littérale affectée à un nom qui en désigne un.

    Lire une variable d'environnement n'en est pas un : c'est exactement la bonne
    manière de faire, et le contrôle ne doit pas la confondre avec une clé en dur.
    """
    import ast
    suspects = ("password", "secret", "api_key", "apikey", "token", "passwd")
    for path in sorted(Path(config.APP_DIR).rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue
            cibles = node.targets if isinstance(node, ast.Assign) else [node.target]
            noms = [t.id.lower() for t in cibles if isinstance(t, ast.Name)]
            if not any(s in nom for nom in noms for s in suspects):
                continue
            valeur = node.value
            if isinstance(valeur, ast.Constant) and isinstance(valeur.value, str) \
                    and valeur.value:
                raise AssertionError("secret littéral dans %s ligne %d"
                                     % (path, node.lineno))


def test_l_application_ecoute_la_boucle_locale_par_defaut():
    assert config.DEFAULT_HOST == "127.0.0.1"
    cli = (Path(config.APP_DIR) / "cli.py").read_text(encoding="utf-8")
    assert "--allow-network" in cli
    assert "NEXUS_S5_PASSWORD" in cli


def test_le_mode_reseau_exige_un_mot_de_passe(monkeypatch):
    from app import cli
    monkeypatch.delenv("NEXUS_S5_PASSWORD", raising=False)
    assert cli.main(["serve", "--allow-network"]) == 2
    monkeypatch.setenv("NEXUS_S5_PASSWORD", "court")
    assert cli.main(["serve", "--allow-network"]) == 2


def test_la_sauvegarde_contient_la_base_et_les_rapports(client):
    body = client.post("/admin/backup", json={}).json()
    assert body["ok"]
    archive = Path(config.BACKUPS_DIR) / body["fichier"]
    assert archive.exists()
    import zipfile
    with zipfile.ZipFile(archive) as zf:
        noms = zf.namelist()
        assert "corrections.sqlite3" in noms
        assert "BACKUP_MANIFEST.json" in noms
        manifeste = json.loads(zf.read("BACKUP_MANIFEST.json"))
        assert manifeste["immutability"]["immutable_artifacts_changed"] == 0
        assert not any(n.endswith("S5_EVALUATION_4E_INES_KEFI.pdf") for n in noms)


def test_l_export_de_cloture_range_et_empreinte(client):
    body = client.post("/admin/export-cloture", json={}).json()
    assert body["ok"]
    root = Path(body["repertoire"])
    for dossier in ("bilans_parents", "syntheses_enseignants", "plans_4_semaines",
                    "fiches_eleves", "analyses_json"):
        assert (root / dossier).is_dir()
    manifeste = json.loads((root / "MANIFEST_SHA256.json").read_text(encoding="utf-8"))
    assert manifeste["immutability"]["immutable_artifacts_changed"] == 0
    for document in manifeste["documents"]:
        assert len(document["sha256"]) == 64


def test_zzz_aucun_artefact_distribue_n_a_change(immutability_before, client):
    """Dernier mot : après tout l'usage de l'application, les 60 documents sont intacts."""
    apres = immutability.verify()
    assert immutability_before.total == apres.total == 60
    assert apres.summary()["immutable_artifacts_changed"] == 0
    assert apres.summary()["immutable_artifacts_missing"] == 0
    assert apres.verdict == "PASS"
    for path, empreinte in immutability_before.by_path.items():
        assert apres.by_path[path] == empreinte, path
