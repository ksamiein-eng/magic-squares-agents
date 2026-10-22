#!/usr/bin/env python3
"""Check the root release manifest. Byte identity is not a proof of mathematics."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parent
count=0
for line in (ROOT/'SHA256SUMS').read_text().splitlines():
    digest,rel=line.split('  ',1)
    path=(ROOT/rel).resolve()
    if ROOT not in path.parents:raise SystemExit('Unsafe manifest path: '+rel)
    if not path.is_file():raise SystemExit('Missing file: '+rel)
    if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise SystemExit('Changed file: '+rel)
    count+=1
print('PASS:',count,'manifested files match')
