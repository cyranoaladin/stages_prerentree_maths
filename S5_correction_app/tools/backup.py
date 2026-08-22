#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sauvegarde locale : base, manifestes, rapports, copies réelles et pages rendues.

Les documents distribués ne sont pas recopiés : ils sont volumineux, reproductibles
et déjà identifiés par leurs empreintes dans le manifeste d'immutabilité. Les copies
réelles des élèves, elles, sont irremplaçables — il n'en existe pas de seconde
source — et leurs octets figurent donc bien dans l'archive, avec leurs empreintes.
Les pages rendues pour la lecture assistée les accompagnent : elles vivent sous la
même racine ``source_copies/`` et portent, elles aussi, une empreinte vérifiable.

Les transcriptions, les campagnes de lecture, les versions de consigne et les
vérifications humaines sont dans la base, donc dans ``corrections.sqlite3``.

    python3 tools/backup.py                    # sauvegarde
    python3 tools/backup.py --verifier <zip>   # restaure dans un temporaire et
                                               # recontrôle chaque empreinte
"""

import argparse
import datetime as dt
import json
import sqlite3
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import APP_VERSION, config                       # noqa: E402
from app.domain import immutability                        # noqa: E402
from app.security import sha256_file                       # noqa: E402


def create_backup(target: Path = None) -> dict:
    config.ensure_runtime()
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    target = Path(target or Path(config.BACKUPS_DIR) / ("backup_%s.zip" % stamp))
    files = 0
    copies = []
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        if config.DB_PATH.exists():
            # La base est en mode WAL : archiver le seul fichier principal
            # produirait une sauvegarde incomplète, voire sans ses dernières
            # tables. On en prend d'abord un instantané cohérent.
            with tempfile.TemporaryDirectory(prefix="nexus_snapshot_") as instantane:
                copie = Path(instantane) / "corrections.sqlite3"
                source = sqlite3.connect(str(config.DB_PATH))
                destination = sqlite3.connect(str(copie))
                try:
                    source.backup(destination)
                finally:
                    destination.close()
                    source.close()
                zf.write(copie, "corrections.sqlite3")
            files += 1
        for path in sorted(Path(config.REPORTS_DIR).rglob("*")):
            if path.is_file():
                zf.write(path, str(Path("reports") / path.relative_to(config.REPORTS_DIR)))
                files += 1
        for path in sorted(Path(config.EXPORTS_DIR).rglob("*.json")):
            zf.write(path, str(Path("exports") / path.relative_to(config.EXPORTS_DIR)))
            files += 1
        # Les copies réelles : les octets, et l'empreinte qui permettra de constater
        # à la restauration que ce sont bien les mêmes.
        # Le répertoire des secrets n'est jamais sauvegardé : une clé d'API n'a
        # rien à faire dans une archive que l'on copiera peut-être ailleurs.
        source_root = Path(config.SOURCE_COPIES_DIR)
        if source_root.exists():
            for path in sorted(source_root.rglob("*")):
                if not path.is_file():
                    continue
                arc = str(Path("source_copies") / path.relative_to(source_root))
                zf.write(path, arc)
                copies.append({"chemin": arc, "sha256": sha256_file(path),
                               "octets": path.stat().st_size})
                files += 1
        # Le cache de lecture assistée : il ne porte aucune preuve — les résultats
        # sont en base, dans ocr_page.raw_json — mais le restaurer évite de refacturer
        # une campagne entière après une restauration.
        caches = 0
        cache_root = Path(config.OCR_CACHE_DIR)
        if cache_root.exists():
            for path in sorted(cache_root.glob("*.json")):
                zf.write(path, str(Path("ocr_cache") / path.name))
                caches += 1
                files += 1
        zf.writestr("BACKUP_MANIFEST.json", json.dumps({
            "created_at": dt.datetime.now().astimezone().isoformat(),
            "app_version": APP_VERSION,
            "fichiers": files,
            "immutability": immutability.verify().summary(),
            "copies_sources_total": len(copies),
            "copies_sources": copies,
            "cache_ocr_total": caches,
            "note": "les documents distribués ne sont pas recopiés ; leurs empreintes "
                    "figurent dans IMMUTABLE_STUDENT_ARTIFACTS.json. Les copies réelles "
                    "des élèves sont incluses ici avec leurs empreintes : elles n'ont "
                    "pas de seconde source.",
        }, ensure_ascii=False, indent=2))
    # L'archive contient des copies d'élèves et leurs transcriptions : elle est
    # réservée à son propriétaire. Elle n'est PAS chiffrée — l'intégrité est
    # garantie par les empreintes, la confidentialité seulement par les droits du
    # fichier. Une archive sortie de cette machine doit être chiffrée par ailleurs.
    try:
        Path(target).chmod(0o600)
    except OSError:
        pass
    return {"archive": target, "fichiers": files, "copies_sources": len(copies),
            "cache_ocr": caches, "sha256": sha256_file(target)}


def verify_backup(archive: Path) -> dict:
    """Restaure l'archive dans un répertoire temporaire et recontrôle les empreintes.

    Ne touche pas à ``runtime/`` : la restauration réelle est une opération distincte
    et délibérée. Ici, on répond seulement à « la sauvegarde rendrait-elle exactement
    les mêmes octets ? ».
    """
    archive = Path(archive)
    with zipfile.ZipFile(archive) as zf:
        manifest = json.loads(zf.read("BACKUP_MANIFEST.json").decode("utf-8"))
        attendus = manifest.get("copies_sources", [])
        verified, mismatched, missing = [], [], []
        names = set(zf.namelist())
        with tempfile.TemporaryDirectory(prefix="nexus_restore_") as tmp:
            root = Path(tmp)
            for entry in attendus:
                if entry["chemin"] not in names:
                    missing.append(entry["chemin"])
                    continue
                zf.extract(entry["chemin"], root)
                observed = sha256_file(root / entry["chemin"])
                if observed != entry["sha256"]:
                    mismatched.append({"chemin": entry["chemin"],
                                       "attendu": entry["sha256"], "observe": observed})
                    continue
                verified.append(entry["chemin"])
            base_present = "corrections.sqlite3" in names
    ok = base_present and not mismatched and not missing
    return {"ok": ok, "base_presente": base_present,
            "copies_attendues": len(attendus), "copies_verifiees": len(verified),
            "differentes": mismatched, "absentes": missing,
            "verdict": "RESTORE VERIFIED" if ok else "RESTORE FAILURE"}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--verifier", metavar="ARCHIVE", default=None)
    args = parser.parse_args(argv)

    if args.verifier:
        report = verify_backup(args.verifier)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["ok"] else 1

    result = create_backup()
    print("sauvegarde : %s" % result["archive"])
    print("  %d fichier(s) dont %d de copies réelles et %d de cache de lecture,"
          " %d octets, sha256 %s"
          % (result["fichiers"], result["copies_sources"], result["cache_ocr"],
             Path(result["archive"]).stat().st_size, result["sha256"][:16]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
