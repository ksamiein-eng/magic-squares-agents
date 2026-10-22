import re, subprocess
src=open('paper.md',encoding='utf-8').read()
src=re.sub(r"```latex\n(.*?)\n```", lambda m: "$$"+m.group(1)+"$$", src, flags=re.S)
CODE={'used','false','config','elements','E_polys','systems[]','G1','G2','common_factor','projection','factors[]',
 'nondegenerate_solutions','univariate','degenerate_component','isolated_line_points','linear_in_circle_point','nonlinear',
 'basis_M','quotients[]','D(tau)','curve_kind','lifted_points','status','linear_relation','exact_verification','fibers','summary',
 'any_nondegenerate_solution','saturation','ellrank','ellratpoints','ellsaturation','Genus','MordellWeilShaInformation','tau','genus>=2'}
def is_code(s): return s in CODE or bool(re.search(r"\.(py|json)\b",s)) or 'certs/' in s or '[]' in s or 'repro/' in s
def conv(m):
    s=m.group(1)
    if is_code(s):
        s=s.replace('\\','\\textbackslash{}').replace('_','\\_').replace('[','{[}').replace(']','{]}').replace('<','\\textless{}').replace('>','\\textgreater{}').replace('*','\\*')
        return '\\texttt{'+s+'}'
    return '$'+s+'$'
src=re.sub(r"`([^`]+)`", conv, src)
src=re.sub(r'×(\d+)', lambda m: '$\\times '+m.group(1)+'$', src)
for k,v in {'∎':' $\\blacksquare$','≥':'$\\ge$','≤':'$\\le$','→':'$\\to$','≡':'$\\equiv$','≠':'$\\ne$','−':'-','×':'$\\times$','∈':'$\\in$','≈':'$\\approx$','±':'$\\pm$','√':'$\\surd$'}.items(): src=src.replace(k,v)
src=src.replace('3$\\times$3','$3\\times3$')
src=re.sub(r"^## (\d+)\. ", "## ", src, flags=re.M)
src=re.sub(r"^## Appendix ([AB])\. ", lambda m: "## Appendix "+m.group(1)+": ", src, flags=re.M)
open('paper_pre.md','w',encoding='utf-8').write(src)
open('meta.yaml','w').write('---\ntitle: "Magic squares of squares and Pythagorean triangles on a common hypotenuse: the cases of one, two and three prime factors"\nauthor: "Draft, 1 October 2026"\ndate: ""\n---\n')
r=subprocess.run(['pandoc','meta.yaml','paper_pre.md','-s','-f','markdown+tex_math_dollars+pipe_tables','-t','latex','--template=template.tex','-o','paper.tex','--wrap=preserve','--shift-heading-level-by=-1'],capture_output=True,text=True)
print(r.stderr[-1500:] if r.stderr else 'pandoc OK')
