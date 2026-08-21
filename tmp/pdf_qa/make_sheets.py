import json, subprocess, math
from pathlib import Path

ROOT = Path(".")
raster_dir = ROOT/"tmp/pdf_qa/raster"
sheets_dir = ROOT/"tmp/pdf_qa/sheets"
raster_dir.mkdir(parents=True, exist_ok=True)
sheets_dir.mkdir(parents=True, exist_ok=True)

sample = json.loads((ROOT/"tmp/pdf_qa/sample_list.json").read_text())

manifest = []
for entry in sample:
    partial = entry.endswith("|PARTIAL")
    pdf_rel = entry.split("|")[0]
    pdf = ROOT/pdf_rel
    doc_id = pdf.stem
    out_prefix = raster_dir/doc_id
    # page count
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    pages = 0
    for line in info.splitlines():
        if line.startswith("Pages:"):
            pages = int(line.split(":")[1].strip())
    if partial and pages > 20:
        # first 10, middle 5, last 5
        first = list(range(1, min(10, pages)+1))
        mid_start = max(1, pages//2 - 2)
        mid = list(range(mid_start, min(mid_start+5, pages)+1))
        last = list(range(max(1, pages-4), pages+1))
        page_list = sorted(set(first+mid+last))
        coverage = f"partial:{len(page_list)}/{pages}"
    else:
        page_list = list(range(1, pages+1))
        coverage = f"full:{pages}/{pages}"
    for p in page_list:
        png = f"{out_prefix}-{p:03d}.png"
        if not Path(png).exists():
            subprocess.run(["pdftoppm", "-png", "-r", "110", "-f", str(p), "-l", str(p), str(pdf), str(out_prefix)], check=True)
    manifest.append({"pdf": pdf_rel, "doc_id": doc_id, "pages_total": pages, "pages_sampled": page_list, "coverage": coverage})

(ROOT/"tmp/pdf_qa/raster_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
print("done", len(manifest))
