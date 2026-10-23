"""Render the one-page write-up (docs/ONEPAGE.md + inline figure) to docs/RESULTS.html, and the full
report (docs/RESULTS.md) to docs/FULL_REPORT.html. Both are self-contained single files."""
import markdown, pathlib, re

root = pathlib.Path(__file__).resolve().parent
svg = (root / "figure.svg").read_text(encoding="utf-8")
svg = re.sub(r"<svg ", '<svg style="width:100%;height:auto" ', svg, count=1)
CSS = """
 @page { size: A4; margin: 11mm; }
 body { font-family: "Segoe UI", Helvetica, Arial, sans-serif; color:#1b1b1b; max-width: 190mm; margin: 0 auto; }
 h1 { color:#1f3a93; margin: 0 0 4px; } h2 { color:#1f3a93; margin: 8px 0 3px; }
 p { margin: 3px 0; } table { border-collapse: collapse; margin: 3px 0; } td, th { border: 1px solid #ccc; padding: 2px 5px; vertical-align: top; }
 code { font-size: 90%; } a { color:#1f3a93; }
"""


def page(md_path, out_path, body_font, h1, h2, table_font, with_figure):
    body = markdown.markdown(md_path.read_text(encoding="utf-8"), extensions=["tables"])
    fig = f'<div style="margin:6px 0 2px">{svg}</div>' if with_figure else ""
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>Rigidity Lab — results</title><style>{CSS} body{{font-size:{body_font}px;line-height:1.3}} h1{{font-size:{h1}px}} h2{{font-size:{h2}px}} table{{font-size:{table_font}px}}</style></head>'
            f'<body>{body}{fig}</body></html>')
    out_path.write_text(html, encoding="utf-8")
    print("wrote", out_path)


page(root / "ONEPAGE.md", root / "RESULTS.html", 10.4, 17, 12.5, 9.4, True)
page(root / "RESULTS.md", root / "FULL_REPORT.html", 11.5, 20, 14, 10.5, True)
