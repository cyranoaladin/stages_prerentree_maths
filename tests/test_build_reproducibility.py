from tools.build import page_shell


def test_page_shell_contains_no_volatile_build_date():
    html = page_shell(
        title="Document test",
        content="<p>Contenu</p>",
        css_href="assets/site.css",
        js_href="assets/site.js",
        breadcrumbs="Accueil",
        badge="LOCAL",
        pdf_href=None,
        confidential=False,
    )

    assert "Génération locale" not in html
    assert "Version 2026.1 · Nexus Réussite" in html


def test_write_manifests_uses_lf_line_endings(tmp_path, monkeypatch):
    from tools import build as build_module

    root = tmp_path
    dist = root / "dist"

    public_site = dist / "site-public"
    private_site = dist / "site-private"
    public_site.mkdir(parents=True)
    private_site.mkdir(parents=True)

    (public_site / "public.txt").write_text("public\n", encoding="utf-8")
    (private_site / "private.txt").write_text("private\n", encoding="utf-8")

    monkeypatch.setattr(build_module, "ROOT", root)
    monkeypatch.setattr(build_module, "DIST", dist)

    public_manifest, private_manifest = build_module.write_manifests()

    for manifest in (public_manifest, private_manifest):
        data = manifest.read_bytes()

        assert b"\r\n" not in data
        assert data.startswith(b"path,sha256,confidential\n")
        assert data.endswith(b"\n")
