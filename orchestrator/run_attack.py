#!/usr/bin/env python3
"""Programmatic orchestrator (Claude Agent SDK) for the rigidity attack.

Equivalent to typing `/rigidity-attack <target>` inside Claude Code, but runnable
unattended:  python orchestrator/run_attack.py --target all

Requirements: pip install claude-agent-sdk ; authentication via ANTHROPIC_API_KEY or a
Claude Code login (`claude /login`). The MCP server is paper_mcp/rational_circle_mcp.py.
The agent team is the same as .claude/agents/*.md (loaded via setting_sources=["project"]);
the definitions below are passed programmatically too so the script is self-contained.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "paper_mcp" / "rational_circle_mcp.py"
MCP_TOOLS = "mcp__rational_circle__*"


def load_agent_md(name: str):
    """Read an agent definition from .claude/agents/<name>.md (frontmatter + body)."""
    text = (ROOT / ".claude" / "agents" / f"{name}.md").read_text(encoding="utf-8")
    _, fm, body = text.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    tools = [t.strip() for t in meta.get("tools", "").split(",") if t.strip()]
    model = meta.get("model", "inherit")
    return meta["description"], body.strip(), tools, (None if model == "inherit" else model)


AGENT_NAMES = ["auditor", "point-hunter", "quotient-geometer", "certificate-extender", "torsion-prober", "skeptic", "scribe"]

TARGET_PROMPTS = {
    "all": "Run the full /rigidity-attack workflow: Phase 0 (auditor), Phase 1 fan-out (point-hunter, quotient-geometer, certificate-extender, torsion-prober), Phase 2 (skeptic), Phase 3 (scribe). Wait for every launched agent's report before moving to the next phase. Finish with the three-line summary: which conjecture moved, by how much, next computation.",
    "D1": "Attack configuration D1 only: auditor on the D1 stages, quotient-geometer for the Chabauty-readiness memo, point-hunter on the genus-five curve, then skeptic, then scribe. Wait for each report.",
    "sum8": "Run certificate-extender for exponent sum 8, then skeptic on its report, then scribe. Wait for each report.",
    "torsion": "Run torsion-prober at height <= 3, then skeptic, then scribe. Wait for each report.",
    "r4": "Run point-hunter on the four-parameter sweep for orbits 0-9 at height 4, then skeptic, then scribe. Wait for each report.",
    "audit": "Run auditor on every cheap stage and classify the five main results. Then stop.",
}


async def main(target: str, model: str | None, max_turns: int) -> int:
    try:
        from claude_agent_sdk import (AgentDefinition, AssistantMessage, ClaudeAgentOptions, ResultMessage,
                                      TextBlock, ToolUseBlock, query)
    except ImportError:
        print("pip install claude-agent-sdk   (and authenticate: ANTHROPIC_API_KEY or `claude /login`)")
        return 2
    agents = {}
    for name in AGENT_NAMES:
        desc, prompt, tools, amodel = load_agent_md(name)
        agents[name] = AgentDefinition(description=desc, prompt=prompt, tools=tools or None,
                                       model=amodel, mcpServers=["rational_circle"])
    skill = (ROOT / ".claude" / "skills" / "rigidity-attack" / "SKILL.md").read_text(encoding="utf-8")
    options = ClaudeAgentOptions(
        mcp_servers={"rational_circle": {"command": sys.executable, "args": [str(SERVER)]}},
        agents=agents,
        allowed_tools=["Agent", "Read", "Grep", "Glob", "Bash", "Write", "Edit", MCP_TOOLS],
        permission_mode="bypassPermissions",
        disallowed_tools=["WebSearch"],
        cwd=str(ROOT),
        setting_sources=["project"],
        max_turns=max_turns,
        model=model,
        system_prompt=skill,
    )
    t0 = time.time()
    log = ROOT / "results" / f"attack_{target}_{int(t0)}.jsonl"
    log.parent.mkdir(exist_ok=True)
    with log.open("w", encoding="utf-8") as f:
        async for message in query(prompt=TARGET_PROMPTS[target], options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text, flush=True)
                        f.write(json.dumps({"t": time.time() - t0, "text": block.text}) + "\n")
                    elif isinstance(block, ToolUseBlock):
                        label = block.input.get("subagent_type") or block.input.get("description") or ""
                        print(f"[tool] {block.name} {label}", flush=True)
                        f.write(json.dumps({"t": time.time() - t0, "tool": block.name, "input": block.input}) + "\n")
            elif isinstance(message, ResultMessage):
                print(f"\n== {message.subtype} in {time.time() - t0:.0f}s, cost ${getattr(message, 'total_cost_usd', 0) or 0:.2f}")
                f.write(json.dumps({"result": message.subtype, "seconds": time.time() - t0}) + "\n")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", choices=sorted(TARGET_PROMPTS), default="all")
    ap.add_argument("--model", default=None, help="e.g. opus, sonnet, claude-fable-5-1")
    ap.add_argument("--max-turns", type=int, default=120)
    a = ap.parse_args()
    sys.exit(asyncio.run(main(a.target, a.model, a.max_turns)))
