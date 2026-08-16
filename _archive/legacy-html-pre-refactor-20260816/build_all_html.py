#!/usr/bin/env python3
from pathlib import Path
import subprocess
ROOT=Path(__file__).parent
CSS=ROOT/"assets"/"print.css"
for md in ROOT.rglob("*.md"):
    if md.name=="README.md":
        continue
    out=md.with_suffix(".html")
    subprocess.run(["pandoc",str(md),"-s","--mathml","--css",str(CSS),"--embed-resources","--resource-path",str(ROOT),"-o",str(out)],check=True)
print("HTML régénérés.")
