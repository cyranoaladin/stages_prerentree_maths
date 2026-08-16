from pathlib import Path

from pypdf import PdfReader, PdfWriter

from tools.build import sanitize_pdf_local_file_links


def extract_uris(path: Path) -> list[str]:
    uris: list[str] = []

    reader = PdfReader(path)

    for page in reader.pages:
        for ref in page.get("/Annots") or []:
            annot = ref.get_object()

            if annot.get("/Subtype") != "/Link":
                continue

            action = annot.get("/A")
            if not action:
                continue

            action = action.get_object()

            if action.get("/S") == "/URI":
                uris.append(str(action.get("/URI", "")))

    return uris


def test_sanitize_pdf_local_file_links_removes_only_file_uris(tmp_path: Path) -> None:
    pdf = tmp_path / "links.pdf"

    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)

    # Lien local à supprimer.
    writer.add_uri(
        0,
        "file:///home/alice/private/generated-page.html",
        [10, 10, 180, 30],
    )

    # Vrai lien web à conserver.
    writer.add_uri(
        0,
        "https://example.org/resource",
        [10, 50, 180, 70],
    )

    with pdf.open("wb") as stream:
        writer.write(stream)

    assert set(extract_uris(pdf)) == {
        "file:///home/alice/private/generated-page.html",
        "https://example.org/resource",
    }

    removed = sanitize_pdf_local_file_links(pdf)

    assert removed == 1
    assert extract_uris(pdf) == ["https://example.org/resource"]

    # Le PDF réécrit doit rester structurellement lisible.
    reader = PdfReader(pdf)
    assert len(reader.pages) == 1
