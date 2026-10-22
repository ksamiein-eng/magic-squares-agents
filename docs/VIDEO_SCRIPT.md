# Video script (target 3:45, hard limit 4:00)

Record with Loom or OBS: screen = `docs/slides.html` in a browser (arrow keys), with a
Claude Code window for the two live moments. Speak at a normal pace; do not speed up audio.

---

**[0:00–0:25] Slide 1, title.**
"Can nine different square numbers form a 3-by-3 magic square? Nobody knows. It is the
Parker-square problem. I have a paper that attacks it in a strange way: it throws away all
the prime-number arithmetic and keeps only rational points on a circle. The obstruction
survives. That paper has open conjectures, machine-checkable ones. For this hackathon I
turned the paper into an agent and sent a team of agents at its own open problems."

**[0:25–0:55] Slide 2, the problem.**
"Each line through the centre of the square is a Pythagorean triangle on the same
hypotenuse, so it is a point on the rational unit circle. The magic conditions say four
sines of integer combinations of the angles have magnitudes a, b, a plus b, a minus b.
Rigidity says: for every full-depth frequency matrix, this never happens on the rational
circle. The paper proves it for two parameters up to exponent sum seven, with two thousand
exact certificates, and reduces the first three-parameter case to a genus-five curve."

**[0:55–1:25] Slide 3, Paper2Agent.**
"Step one, following Paper2Agent from Miao and Zou's Nature paper: the paper and its
251-file verification tree become an MCP server. Fourteen tools, each bound to the paper's
own code: rerun a certificate stage, evaluate a configuration exactly, search the curve,
run the four-parameter sweep. Five resources, three prompts. Every tool is tested in-process."
*(Live: run `python paper_mcp/test_mcp.py`, show 14 tools and the stage passing.)*

**[1:25–1:55] Slide 4, the team.**
"Step two: five specialists, one referee, one scribe. Auditor reruns the proof tree.
Point-hunter searches at large height. Quotient-geometer looks for structure the paper
missed. Certificate-extender pushes the proven range. Torsion-prober tests the structural
hypothesis the paper calls its most important one. The skeptic reruns one computation per
specialist and tags every sentence: proved, machine-verified, database-quoted, search
evidence, or conjectural. Nothing reaches the write-up without a tag."

**[1:55–2:40] Slide 5, finding one.**
"What the agents found. The genus-five curve is even and palindromic, so it has two extra
symmetries. Its Jacobian splits off three elliptic curves. The paper's own known points give
a point of infinite order on each, by exact Nagell–Lutz arithmetic, and the LMFDB identifies
them as 123.a1, 492.b1 and 1968.j1, all of rank one. So the paper's rank-zero descent method
can never close this conjecture. It is a quadratic-Chabauty problem on a bielliptic genus-two
curve of rank two. That is a precise, new, and honest statement of what it will take."

**[2:40–3:15] Slide 6, finding two and three.**
"Second: the certificate extender reran the paper's own producer and independent checker on
the next exponent sum. Thirty-two new representatives, fifteen hundred new signed systems,
three hundred thousand exact determinants. The checker passed. Theorem 1.1 now holds through
exponent sum eight. Third: the torsion prober recorded every exact rational solution of every
signed system at height three, two hundred seventy-three thousand of them, and tested the
paper's torsion-coset hypothesis with a complete Gaussian-prime test. Zero exceptions, and a
sharper pattern: the relation rank never exceeds two. Fourth: the point hunter pushed the
empty region on the genus-five curve from height fifteen hundred to three hundred thousand
in thirty-seven seconds."

**[3:15–3:40] Slide 7, the referee.**
"Here is the skeptic's table. {{SKEPTIC_SENTENCE}} The write-up is one page and every
sentence carries its tag."

**[3:40–4:00] Slide 8, close.**
"The repository runs with one slash command inside Claude Code or unattended through the
Agent SDK. The paper's proof records are never modified. The problem is still open. But the
paper now knows exactly where it is stuck, and it can keep attacking itself. Thank you."
