#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sauvegarde locale : base, manifestes et rapports générés.

Les documents distribués ne sont pas recopiés : ils sont volumineux et déjà identifiés
par leurs empreintes. Ce qui est irremplaçable ici, ce sont les corrections.
"""

import datetime as dt
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import APP_VERSION, config                       # noqa: E402
from app.domain import immutability                        # noqa: E402
from app.security import sha256_file                       # noqa: E402


def main() -> int:
    config.ensure_runtime()
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    target = Path(config.BACKUPS_DIR) / ("backup_%s.zip" % stamp)
    files = 0
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        if config.DB_PATH.exists():
            zf.write(config.DB_PATH, "corrections.sqlite3")
            files += 1
        for path in sorted(Path(config.REPORTS_DIR).rglob("*")):
            if path.is_file():
                zf.write(path, str(Path("reports") / path.relative_to(config.REPORTS_DIR)))
                files += 1
        for path in sorted(Path(config.EXPORTS_DIR).rglob("*.json")):
            zf.write(path, str(Path("exports") / path.relative_to(config.EXPORTS_DIR)))
            files += 1
        zf.writestr("BACKUP_MANIFEST.json", json.dumps({
            "created_at": dt.datetime.now().astimezone().isoformat(),
            "app_version": APP_VERSION,
            "fichiers": files,
            "immutability": immutability.verify().summary(),
            "note": "les documents distribués ne sont pas recopiés ; leurs empreintes "
                    "figurent dans IMMUTABLE_STUDENT_ARTIFACTS.json",
        }, ensure_ascii=False, indent=2))
    print("sauvegarde : %s" % target)
    print("  %d fichier(s), %d octets, sha256 %s"
          % (files, target.stat().st_size, sha256_file(target)[:16]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
