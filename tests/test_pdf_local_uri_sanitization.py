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


def test_sanitize_pdf_preserves_metadata_and_internal_destinations(tmp_path: Path) -> None:
    pdf = tmp_path / "metadata_dest.pdf"

    writer = PdfWriter()
    page1 = writer.add_blank_page(width=200, height=200)
    page2 = writer.add_blank_page(width=200, height=200)

    writer.add_metadata({
        "/Title": "Document de Test",
        "/Author": "Nexus Réussite",
        "/Subject": "4e — Mathématiques",
        "/Keywords": "Nexus, Test",
        "/Lang": "fr-FR",
        "/NexusVersion": "2026.1",
    })

    # Add outline/bookmark
    parent_outline = writer.add_outline_item("Section 1", 0)
    writer.add_outline_item("Subsection 1.1", 1, parent=parent_outline)

    # Add a local file link and a web link
    writer.add_uri(0, "file:///tmp/secret.html", [10, 10, 100, 30])
    writer.add_uri(0, "https://nexus-reussite.fr", [10, 40, 100, 60])

    with pdf.open("wb") as stream:
        writer.write(stream)

    removed = sanitize_pdf_local_file_links(pdf)
    assert removed == 1

    reader = PdfReader(pdf)
    assert len(reader.pages) == 2

    # Check metadata preservation
    meta = reader.metadata
    assert meta is not None
    assert meta.get("/Title") == "Document de Test"
    assert meta.get("/Author") == "Nexus Réussite"
    assert meta.get("/Subject") == "4e — Mathématiques"
    assert meta.get("/Lang") == "fr-FR"
    assert meta.get("/NexusVersion") == "2026.1"

    # Check remaining URIs
    assert extract_uris(pdf) == ["https://nexus-reussite.fr"]

    # Check outlines
    assert len(reader.outline) >= 1

