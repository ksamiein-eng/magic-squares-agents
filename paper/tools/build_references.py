#!/usr/bin/env python3
"""Emit BibTeX and the directly compiled bibliography from the audited metadata."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
refs=json.loads((ROOT/'editorial/references.json').read_text())
tex=[r'\begin{thebibliography}{99}',r'\small']
bib=[]
for r in refs:
    tex.append(r'\bibitem{'+r['key']+'} '+r['tex'])
    fields=[f'  {k} = {{{v}}}' for k,v in r.items() if k not in {'key','type','tex','support','review'}]
    bib.append('@'+r['type']+'{'+r['key']+',\n'+',\n'.join(fields)+'\n}\n')
tex.append(r'\end{thebibliography}')
(ROOT/'manuscript/references.tex').write_text('\n'.join(tex)+'\n')
(ROOT/'manuscript/references.bib').write_text('\n'.join(bib))
print(len(refs),'references written')
