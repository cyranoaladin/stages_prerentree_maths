import json, subprocess
from pathlib import Path

ROOT = Path(".")
raster_dir = ROOT/"tmp/pdf_qa/raster"
sheets_dir = ROOT/"tmp/pdf_qa/sheets"
sheets_dir.mkdir(parents=True, exist_ok=True)

manifest = json.loads((ROOT/"tmp/pdf_qa/raster_manifest.json").read_text())
sheet_index = []
for m in manifest:
    doc_id = m["doc_id"]
    pages = m["pages_sampled"]
    width = 3 if m["pages_total"] >= 100 else (2 if m["pages_total"] >= 10 else 1)
    chunk = 6
    for i in range(0, len(pages), chunk):
        group = pages[i:i+chunk]
        files = [str(raster_dir/f"{doc_id}-{p:0{width}d}.png") for p in group]
        out = sheets_dir/f"{doc_id}_sheet{i//chunk+1:02d}.png"
        cmd = ["montage"] + files + ["-tile", "2x3", "-geometry", "480x679+3+3", "-label", "%f", str(out)]
        subprocess.run(cmd, check=True)
        sheet_index.append({"doc_id": doc_id, "pdf": m["pdf"], "sheet": str(out), "pages": group, "pages_total": m["pages_total"], "coverage": m["coverage"]})

(ROOT/"tmp/pdf_qa/sheet_index.json").write_text(json.dumps(sheet_index, ensure_ascii=False, indent=2))
print("sheets:", len(sheet_index))
