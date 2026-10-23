# Public post (LinkedIn / X / Bluesky; attach cover.png and results.png; no video required)

**Single post version (LinkedIn):**

Can nine different squares form a 3×3 magic square? Still open. For #OSIHackathon 2026 I turned my own paper on the problem into an AI agent and sent a team of agents at the paper's own open conjectures, with a referee agent tagging every claim.

Three iterations in one afternoon:
• the paper's main theorem extended three times (exponent sum 7 → 10; 8,688 independently checked certificates)
• the exact obstruction to its central conjecture located: three elliptic quotients of rank 1, so it is a quadratic-Chabauty problem
• a never-tested structural hypothesis checked on 1,916,672 exact rational solutions: zero exceptions
• the loop refuted its own first sharpening, and the failure became a proved lemma and a new, stronger conjecture

Every claim carries a tag (proved / machine-verified / database-quoted / search-evidence / conjectural), one command reproduces all six agent-added verification stages, and every agent transcript is in the repo with hashes. Two weeks after openai/math released 719 AI manuscripts with three withdrawn in a day, the point is this: candidate theorems are cheap, verified status is not.

Built with Claude Code and Paper2Agent (Miao, Zou et al., Nature 2026). With Jonathan Wolinski.
Code, manuscript v3, write-up: https://github.com/ksamiein-eng/magic-squares-agents
#mathematics #AIforScience #OpenScience

**Thread version (X / Bluesky):**

1/ Can nine different squares form a 3×3 magic square? Still open. For #OSIHackathon I turned my paper on it into an AI agent and sent agents at the paper's own open conjectures. Three iterations, one afternoon. 🧵

2/ The paper's proof tree became 14 tools. Specialists attack by playbook; a skeptic agent reruns one computation per specialist and tags every sentence. Accepted results become new stages of the paper's own verification suite. A planner emits the next iteration.

3/ Moved: main theorem extended three times (8,688 certificates, checker PASS). Central conjecture's obstruction located: three elliptic quotients, all rank 1 → quadratic Chabauty. Untested hypothesis checked on 1,916,672 solutions: zero exceptions.

4/ Best part: iteration 1 proposed a sharper conjecture, iteration 2 refuted it, and the refutation explained itself as a two-line lemma that predicts exactly which configurations can misbehave. Still exactly those at height 5.

5/ Candidate theorems are cheap; verified status is not (see openai/math this month). Here every claim is tagged, everything reproduces from one command, transcripts are verbatim, corrections are recorded. The problem is still open. The paper can keep attacking itself.
https://github.com/ksamiein-eng/magic-squares-agents
