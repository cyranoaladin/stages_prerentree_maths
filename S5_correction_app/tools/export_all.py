#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export de toutes les corrections, hors interface web."""

import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config, database                          # noqa: E402
from app.models import Assessment                          # noqa: E402
from app.routes.admin import _export_payload               # noqa: E402


def main() -> int:
    config.ensure_runtime()
    with database.session_scope() as session:
        payload = {"schema": "nexus-s5-correction-export-bundle-v1",
                   "exported_at": dt.datetime.now().astimezone().isoformat(),
                   "eleves": [_export_payload(session, a)
                              for a in session.query(Assessment).all()]}
    target = (Path(config.EXPORTS_DIR)
              / ("export_corrections_%s.json" % dt.datetime.now().strftime("%Y%m%d")))
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print("export : %s (%d élèves)" % (target, len(payload["eleves"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
