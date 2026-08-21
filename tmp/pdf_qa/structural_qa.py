import csv, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.build import is_a4_page

STUDENT_NAMES = (
    "Sinda Chikhaoui", "Fares Darghouth", "Sarah Bargaoui", "Selim Mansouri",
    "Amine Mansouri", "Fares Laajili", "Noa Maniaci", "Ahmed Bakir",
    "Donia Khadhrani", "Malek Khadhrani", "Ahmad Beldi",
)

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

results = []
pdfs = sorted((ROOT/"dist/pdf").rglob("*.pdf")) + sorted((ROOT/"dist/packs").rglob("*.pdf"))
for pdf in pdfs:
    rel = pdf.relative_to(ROOT).as_posix()
    row = {"path": rel, "issues": []}
    # qpdf --check
    qc = run(["qpdf", "--check", str(pdf)])
    if qc.returncode != 0:
        row["issues"].append(f"qpdf_check_fail: {qc.stdout.strip()[:200]} {qc.stderr.strip()[:200]}")
    # pdfinfo
    pi = run(["pdfinfo", str(pdf)])
    info = dict(re.findall(r'^([A-Za-z ]+):\s+(.*)$', pi.stdout, flags=re.M))
    pages = int(info.get("Pages", "0") or 0)
    row["pages"] = pages
    encrypted = "yes" in info.get("Encrypted", "").lower()
    if encrypted:
        row["issues"].append("encrypted")
    size_match = re.search(r'([\d.]+)\s*x\s*([\d.]+)\s*pts', pi.stdout)
    if size_match:
        w, h = float(size_match.group(1)), float(size_match.group(2))
        if not is_a4_page(w, h):
            row["issues"].append(f"not_a4: {w}x{h}pt")
    else:
        row["issues"].append("no_page_size_reported")
    if pages == 0:
        row["issues"].append("zero_pages")
    # pdffonts: embedded check
    pf = run(["pdffonts", str(pdf)])
    font_lines = [l for l in pf.stdout.splitlines()[2:] if l.strip()]
    not_embedded = [l for l in font_lines if re.search(r'\bno\b', l.split()[-3] if len(l.split())>=3 else "")]
    # column "emb" is typically near the end; do a simpler robust check
    not_embedded2 = []
    for l in font_lines:
        parts = l.split()
        if len(parts) >= 5 and parts[-5] == "no":
            not_embedded2.append(l.strip())
    if not_embedded2:
        row["issues"].append(f"fonts_not_embedded:{len(not_embedded2)}")
    row["font_count"] = len(font_lines)
    # pdftotext: extractability + correction leak check for eleve docs
    pt = run(["pdftotext", str(pdf), "-"])
    text = pt.stdout
    row["text_len"] = len(text.strip())
    if len(text.strip()) == 0:
        row["issues"].append("no_extractable_text")
    is_eleve_pdf = (
        "/eleves/" in rel or "PACK_ELEVE" in rel or "PACK_TRAVAIL_PERSONNALISE" in rel
        or (pdf.name.endswith("_ELEVE.pdf") or "_ELEVE_" in pdf.name)
    ) and "DOSSIER_ENSEIGNANT" not in rel and "PROF" not in pdf.name
    if is_eleve_pdf:
        benign = re.sub(r'(?i)consulter le corrig[ée]e?s?|comment je (?:la|le) corrige', '', text)
        leak = re.findall(r'(?i)\bcorrig[ée]e?s?\b|\bbar[eè]me\b', benign)
        if leak:
            row["issues"].append(f"possible_correction_leak:{len(leak)}")
    # cross-student PII check for nominatif packs (each per-student file must not mention other students)
    if "nominatifs-prives" in rel:
        m = re.search(r'_(?:PACK_TRAVAIL_PERSONNALISE|DOSSIER_ENSEIGNANT_CONFIDENTIEL)', pdf.name)
        if m:
            owner_guess = None
            for name in STUDENT_NAMES:
                key = name.replace(" ", "_")
                if key in pdf.name:
                    owner_guess = name
            if owner_guess:
                others = [n for n in STUDENT_NAMES if n != owner_guess and n in text]
                if others:
                    row["issues"].append(f"cross_student_pii:{others}")
    results.append(row)

out_csv = ROOT/"tmp/pdf_qa/structural_results.csv"
with out_csv.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["path","pages","font_count","text_len","issues"])
    for r in results:
        w.writerow([r["path"], r["pages"], r.get("font_count"), r.get("text_len"), ";".join(r["issues"])])

failures = [r for r in results if r["issues"]]
print(f"TOTAL_PDF={len(results)}")
print(f"TOTAL_PAGES={sum(r['pages'] for r in results)}")
print(f"WITH_ISSUES={len(failures)}")
for r in failures:
    print(r["path"], "->", r["issues"])
