#!/usr/bin/env python3
"""Export Claude Code transcripts (JSONL) to readable Markdown traces.

Usage: python tools/export_traces.py <transcript.jsonl> <out.md> [--title T] [--max-result N] [--max-think N]
Each assistant turn is rendered as: reasoning (thinking blocks), prose, tool calls (name + input);
each tool result is rendered truncated. Nothing is paraphrased; truncation is marked.
"""
import json, sys, argparse, datetime, hashlib

def trunc(s, n):
    s = s if isinstance(s, str) else json.dumps(s, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + f"\n... [truncated, {len(s)-n} more chars]"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--title", default=None); ap.add_argument("--max-result", type=int, default=1500)
    ap.add_argument("--max-think", type=int, default=4000); ap.add_argument("--max-input", type=int, default=2500)
    a = ap.parse_args()
    raw = open(a.src, "rb").read()
    out = [f"# Trace: {a.title or a.src}", "",
           f"Source transcript: `{a.src.split('/')[-1].split(chr(92))[-1]}` (sha256 {hashlib.sha256(raw).hexdigest()[:16]}…, {len(raw):,} bytes)",
           "Rendered by tools/export_traces.py. Thinking, prose and tool inputs are verbatim; long blocks are truncated and marked.", ""]
    n_turns = n_tools = 0; models = set(); first = last = None
    for line in raw.decode("utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line: continue
        try: d = json.loads(line)
        except Exception: continue
        t = d.get("type"); ts = d.get("timestamp")
        if ts: first = first or ts; last = ts
        if t == "assistant":
            msg = d.get("message", {}); models.add(msg.get("model") or d.get("requestedModel") or "")
            blocks = msg.get("content", [])
            if isinstance(blocks, str): blocks = [{"type": "text", "text": blocks}]
            n_turns += 1
            out.append(f"\n## Assistant turn {n_turns}  `{(ts or '')[11:19]}`")
            for b in blocks:
                bt = b.get("type")
                if bt == "thinking" and b.get("thinking"):
                    out.append("\n<details><summary>reasoning</summary>\n\n" + trunc(b["thinking"], a.max_think) + "\n\n</details>")
                elif bt == "text" and b.get("text", "").strip():
                    out.append("\n" + b["text"].strip())
                elif bt == "tool_use":
                    n_tools += 1
                    inp = b.get("input", {})
                    if isinstance(inp, dict) and "command" in inp:
                        body = "```bash\n" + trunc(inp["command"], a.max_input) + "\n```"
                        desc = inp.get("description", "")
                        out.append(f"\n**Tool call {n_tools}: {b.get('name')}** — {desc}\n\n{body}")
                    else:
                        out.append(f"\n**Tool call {n_tools}: {b.get('name')}**\n\n```json\n{trunc(inp, a.max_input)}\n```")
        elif t == "user":
            msg = d.get("message", {}); c = msg.get("content")
            if isinstance(c, str):
                out.append("\n## Task prompt\n\n" + trunc(c, 6000))
            elif isinstance(c, list):
                for b in c:
                    if b.get("type") == "tool_result":
                        cc = b.get("content")
                        if isinstance(cc, list): cc = "\n".join(x.get("text", "") for x in cc if isinstance(x, dict))
                        out.append("\n<details><summary>tool result</summary>\n\n```\n" + trunc(cc or "", a.max_result) + "\n```\n\n</details>")
                    elif b.get("type") == "text" and b.get("text", "").strip():
                        out.append("\n## Message to agent\n\n" + trunc(b["text"], 4000))
    out.insert(4, f"Span: {first} → {last}. Assistant turns: {n_turns}. Tool calls: {n_tools}. Model(s): {', '.join(sorted(m for m in models if m))}.")
    open(a.out, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"wrote {a.out}: {n_turns} turns, {n_tools} tool calls, span {first} -> {last}")

if __name__ == "__main__":
    main()
