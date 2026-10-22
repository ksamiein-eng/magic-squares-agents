#!/usr/bin/env python3
"""Build the paper with pdflatex; no BibTeX executable or network is required."""
from pathlib import Path
import argparse,shutil,subprocess,tempfile
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=ROOT/'manuscript/paper.pdf')
    args=ap.parse_args()
    if not shutil.which('pdflatex'):raise SystemExit('pdflatex is required. Install a TeX distribution with the packages listed in the README.')
    logdir=ROOT/'verification_runs/build';logdir.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='rational-circle-tex-') as temp:
        for n in range(3):
            p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+temp,'paper.tex'],cwd=ROOT/'manuscript',capture_output=True,text=True)
            (logdir/f'pass_{n+1}.txt').write_text(p.stdout+p.stderr)
            if p.returncode:raise SystemExit('LaTeX failed; see verification_runs/build/')
        log=(Path(temp)/'paper.log').read_text(errors='replace')
        for error in ['There were undefined references','There were undefined citations','Overfull \\hbox','Overfull \\vbox']:
            if error in log:raise SystemExit('Build requires review: '+error)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(Path(temp)/'paper.pdf',args.output)
        shutil.copy2(Path(temp)/'paper.log',logdir/'paper.log')
        shutil.copy2(Path(temp)/'paper.aux',logdir/'paper.aux')
    print(args.output)
if __name__=='__main__':main()
