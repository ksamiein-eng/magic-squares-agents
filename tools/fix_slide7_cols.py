#!/usr/bin/env python3
"""Lay slide 7 out in two columns so its five boxes fit a 1280x720 viewport. Idempotent."""
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "docs" / "slides.html"
s = p.read_text(encoding="utf-8")
start = s.find('<section class="slide">\n  <h2>Findings 2')
end = s.find("</section>", start)
assert start > 0 and end > start
sec = s[start:end]  # without the closing tag
if 'class="cols dense"' in sec:
    print("already two columns"); raise SystemExit
parts = sec.split('<div class="box">')
head = parts[0]
items = ['<div class="box">' + b.rstrip() for b in parts[1:]]
assert len(items) == 5, len(items)
left = "\n".join(items[i] for i in (0, 1, 4))
right = "\n".join(items[i] for i in (2, 3))
new = head.rstrip() + '\n  <div class="cols dense">\n    <div>\n' + left + '\n    </div>\n    <div>\n' + right + '\n    </div>\n  </div>\n'
s = s[:start] + new + s[end:]
if ".dense p" not in s:
    s = s.replace("  .counter {", "  .dense p { font-size:16.5px; line-height:1.32; } .dense .box { padding:10px 14px; margin:6px 0; } .dense .tag { font-size:13px; }\n  .counter {")
p.write_text(s, encoding="utf-8")
i = s.find("Findings 2"); sec2 = s[i:s.find("</section>", i)]
print("sections:", s.count('<section class="slide"'), "boxes in slide 7:", sec2.count('class="box"'))
