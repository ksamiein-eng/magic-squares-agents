"""Render docs/RESULTS.md (+ figure) to docs/RESULTS.html, printable to a one-page PDF."""
import markdown, pathlib
root = pathlib.Path(__file__).resolve().parent
md = (root / "RESULTS.md").read_text(encoding="utf-8")
body = markdown.markdown(md, extensions=["tables"])
html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Rigidity Lab — results</title>
<style>
 @page {{ size: A4; margin: 12mm; }}
 body {{ font-family: "Segoe UI", Helvetica, Arial, sans-serif; font-size: 10.2px; line-height: 1.32; color:#1b1b1b; max-width: 190mm; margin: 0 auto; }}
 h1 {{ font-size: 17px; margin: 0 0 4px; color:#1f3a93; }} h2 {{ font-size: 12.5px; margin: 8px 0 3px; color:#1f3a93; }}
 p {{ margin: 3px 0; }} table {{ border-collapse: collapse; font-size: 9.4px; margin: 3px 0; }} td, th {{ border: 1px solid #ccc; padding: 2px 5px; }}
 img {{ width: 100%; margin: 4px 0; }} code {{ font-size: 9px; }}
</style></head><body>{body.replace('Figure: <code>docs/figure.svg</code>', 'Figure below.')}
<img src="figure.svg" alt="architecture figure"></body></html>"""
(root / "RESULTS.html").write_text(html, encoding="utf-8")
print("wrote", root / "RESULTS.html")
