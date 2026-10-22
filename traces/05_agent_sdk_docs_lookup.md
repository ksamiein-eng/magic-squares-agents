# Trace: subagent a547588d0c9123d72

Source transcript: `agent-a547588d0c9123d72.jsonl` (sha256 abfa481abba4a6c8…, 829,443 bytes)
Rendered by tools/export_traces.py. Thinking, prose and tool inputs are verbatim; long blocks are truncated and marked.
Span: 2026-10-22T20:58:25.745Z → 2026-10-22T21:00:12.342Z. Assistant turns: 18. Tool calls: 12. Model(s): claude-haiku-5-5.


## Task prompt

I am writing a Python script with the Claude Agent SDK (pip package `claude-agent-sdk`, version 0.2.x, October 2026) that: (1) registers a local stdio MCP server (command `python`, args `["paper_mcp/rational_circle_mcp.py"]`) so tools are available as `mcp__rational_circle__<tool>`; (2) defines several custom subagents programmatically (name, description, prompt, tools list, model) via the `agents` option so the main agent can delegate with the Agent/Task tool; (3) runs a single orchestration prompt with `ClaudeSDKClient` or `query()` and streams/prints assistant text and tool-use blocks; (4) sets `permission_mode` to bypass prompts for an unattended run, `cwd` to the project, and `setting_sources` so that `.claude/agents/*.md` and `.mcp.json` in the project are also loaded. Please give me the exact, current import names, the `ClaudeAgentOptions` field names (agents, mcp_servers, allowed_tools, permission_mode, cwd, setting_sources, max_turns, model), the `AgentDefinition` dataclass fields, the message/block class names to pattern-match on (AssistantMessage, TextBlock, ToolUseBlock, ResultMessage), and a minimal complete working example (~40 lines). Also: does the Python SDK bundle the Claude Code CLI binary, or must `claude` be installed separately, and how does authentication work (ANTHROPIC_API_KEY vs. Claude Code login)? Answer from the official docs; cite the doc URLs you used.

## Task prompt

<system-reminder>
Your final report is delivered through SubagentHandback: when your work is complete, call SubagentHandback({message: <your full report>}). The call ends your run, so make it your last step. Only a SubagentHandback call reaches your caller as your result; plain text you write at the end is not delivered.
</system-reminder>

## Assistant turn 1  `20:58:27`

## Assistant turn 2  `20:58:28`

**Tool call 1: WebFetch**

```json
{"url": "https://code.claude.com/docs/en/claude_code_docs_map.md", "prompt": "List every URL in this docs map that relates to the Agent SDK (Python SDK, subagents, MCP in agents, permissions, sessions, setting sources, authentication). Return the exact URLs."}
```

<details><summary>tool result</summary>

```
The visible portion of this docs map has no pages titled Agent SDK, Python SDK, setting sources, or permissions. The map is also cut off partway through the Setup and access section, so Agent SDK pages may appear in the truncated part. Below are the visible pages closest to your topics. I built the URLs from the map's `https://code.claude.com/docs/en/<slug>.md` pattern.

**Subagents and agents**
- https://code.claude.com/docs/en/sub-agents.md: includes frontmatter, tool and permission control, scoping MCP servers to a subagent, and permission modes
- https://code.claude.com/docs/en/agents.md
- https://code.claude.com/docs/en/agent-teams.md
- https://code.claude.com/docs/en/agent-view.md

**MCP**
- https://code.claude.com/docs/en/mcp.md
- https://code.claude.com/docs/en/mcp-quickstart.md

**Sessions**
- https://code.claude.com/docs/en/sessions.md: includes "Access conversations from scripts" and "Export and locate session data"

**Programmatic and non-interactive use**
- https://code.claude.com/docs/en/headless.md: includes "Auto-approve tools," "Get structured output," and "Continue conversations"

**Settings and configuration**
- https://code.claude.com/docs/en/claude-directory.md: covers the configuration file layout
- https://code.claude.com/docs/en/debug-your-config.md: covers checking resolved settings

**Authentication and setup**
- https://code.claude.com/docs/en/setup.md: includes an "Authenticate" section

**Hooks**
- https://code.claude.com/docs/en/hooks-guide.md

T
... [truncated, 364 more chars]
```

</details>

## Assistant turn 3  `20:58:38`

## Assistant turn 4  `20:58:38`

**Tool call 2: WebFetch**

```json
{"url": "https://code.claude.com/docs/en/claude_code_docs_map.md", "offset": 100000, "prompt": "Find every URL related to the Agent SDK (agent-sdk/*, Python SDK reference, TypeScript SDK, subagents in SDK, setting sources, authentication, permissions). Return exact URLs and their titles."}
```

<details><summary>tool result</summary>

```
<persisted-output>
Output too large (89KB). Full output saved to: C:\Users\kimia\.claude\projects\C--Users-kimia\e4ab3fed-fe0c-4e63-8ea3-c5514030f294\tool-results\toolu_01FHjH6z7rCRZwc9etKMkZPw.txt

Preview (first 2KB):
inGet
  * Uninstall with apt, dnf, or apk
  * Uninstall with npm
  * Remove configuration files

### [authentication](https://code.claude.com/docs/en/authentication.md)

* Log in to Claude Code
  * Login prompt still appears after an earlier sign-in
  * Log in with multiple accounts
* Set up team authentication
  * Claude for Teams or Enterprise
  * Claude Console authentication
    * Sign in without an API key
  * Cloud provider authentication
  * Restrict login to your organization
  * Restrict which API providers a machine may use
* Credential management
  * Renew an expiring login
  * Authentication precedence
    * Anthropic profiles and federation credentials
  * Generate a long-lived token

### [managed-settings](https://code.claude.com/docs/en/managed-settings.md)

* Deploy a managed settings file
* Choose a delivery mechanism
  * Where and when a policy applies
  * Where each mechanism stores the policy
  * Split a file-based policy across teams
* How Claude Code combines managed sources
  * When an admin document counts as present
  * Keys read from every admin source
  * Compose every managed source
  * Compute the policy with a helper program
  * Let an embedding host add policy
    * Keep Cowork folder access when only managed rules apply
  * What
... [truncated, 730 more chars]
```

</details>

## Assistant turn 5  `20:58:39`

**Tool call 3: WebFetch**

```json
{"url": "https://code.claude.com/docs/en/agent-sdk/python.md", "prompt": "Give me the exact current Python SDK API: import names (ClaudeSDKClient, query, ClaudeAgentOptions, AgentDefinition, AssistantMessage, TextBlock, ToolUseBlock, ResultMessage), every ClaudeAgentOptions field name and type (agents, mcp_servers, allowed_tools, permission_mode, cwd, setting_sources, max_turns, model, etc.), the AgentDefinition dataclass fields, whether the CLI is bundled, and the authentication section. Quote field names exactly."}
```

<details><summary>tool result</summary>

```
## Imports

The page's examples use these top-level imports from `claude_agent_sdk`:

```python
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AgentDefinition,
    AssistantMessage,
    TextBlock,
    ResultMessage,
    query,
)
```

The page documents `ToolUseBlock` as a content block type but doesn't show its import line, so check that it's exported at the top level. `PermissionResultAllow`, `PermissionResultDeny`, and `ToolPermissionContext` are imported from `claude_agent_sdk.types` in the examples.

## `ClaudeAgentOptions` fields

Field names and types as listed on the page:

| Field | Type | Default |
| :- | :- | :- |
| `tools` | `list[str] \| ToolsPreset \| None` | `None` |
| `allowed_tools` | `list[str]` | `[]` |
| `system_prompt` | `str \| SystemPromptPreset \| SystemPromptCustom \| SystemPromptFile \| None` | `None` |
| `mcp_servers` | `dict[str, McpServerConfig] \| str \| Path` | `{}` |
| `strict_mcp_config` | `bool` | `False` |
| `permission_mode` | `PermissionMode \| None` | `None` |
| `continue_conversation` | `bool` | `False` |
| `resume` | `str \| None` | `None` |
| `session_id` | `str \| None` | `None` |
| `max_turns` | `int \| None` | `None` |
| `max_budget_usd` | `float \| None` | `None` |
| `disallowed_tools` | `list[str]` | `[]` |
| `model` | `str \| None` | `None` |
| `fallback_model` | `str \| None` | `None` |
| `betas` | `list[SdkBeta]` | `[]` |
| `output_format` | `dict[str, Any] \| None` | `None` |
| `permission_promp
... [truncated, 4482 more chars]
```

</details>

## Assistant turn 6  `20:59:04`

## Assistant turn 7  `20:59:05`

**Tool call 4: WebFetch**

```json
{"url": "https://code.claude.com/docs/en/agent-sdk/python.md", "offset": 100000, "prompt": "Return the remaining content verbatim-ish: the rest of the ClaudeAgentOptions/types section, PermissionMode allowed values, SettingSource values and what they load, the message and block classes (AssistantMessage, TextBlock, ToolUseBlock, ResultMessage, and their fields, including whether ToolUseBlock is a top-level export), error types (CLINotFoundError etc.), and any text about the bundled CLI or version requirements."}
```

<details><summary>tool result</summary>

```
<persisted-output>
Output too large (60KB). Full output saved to: C:\Users\kimia\.claude\projects\C--Users-kimia\e4ab3fed-fe0c-4e63-8ea3-c5514030f294\tool-results\toolu_01KLdUFVmdb65NzZ85PkC5jr.txt

Preview (first 2KB):
eSDKError):
    def __init__(
        self, message: str, exit_code: int | None = None, stderr: str | None = None
    ):
        self.exit_code = exit_code
        self.stderr = stderr
```

### `ResultError`

Raised when the Claude Code process exits because the run ended with an error [result message](#resultmessage), such as a turn-limit error or an API error. `ResultError` subclasses `ProcessError`, so an existing `except ProcessError` handler also catches it. Its attributes carry the fields of that result message, so you can branch on why the run failed without parsing the message text. Requires Python Agent SDK 0.2.140 or later.

```python theme={null}
class ResultError(ProcessError):
    subtype: str | None  # "error_max_turns", "error_during_execution", ...; "success" when the run ended on a failed request
    errors: list[str]  # an empty list when the result message reported none
    result: str | None
    api_error_status: int | None
    terminal_reason: str | None  # "max_turns", "api_error", ...; check after data["stop_reason"], before subtype
    session_id: str | None
    data: dict[str, Any]  # the raw result message payload
```

To tell failures apart, check `data["stop_reason"]` first, then `terminal_reason`, then `subtype`. A declined respons
... [truncated, 736 more chars]
```

</details>

## Assistant turn 8  `20:59:06`

**Tool call 5: WebFetch**

```json
{"url": "https://code.claude.com/docs/en/agent-sdk/quickstart.md", "prompt": "Does the Python SDK bundle the Claude Code CLI or must it be installed separately (Node/npm install of @anthropic-ai/claude-code)? Describe the exact installation steps and the authentication options: ANTHROPIC_API_KEY, Claude Code login, cloud providers (Bedrock/Vertex/Foundry), and precedence. Include exact quoted text where relevant."}
```

<details><summary>tool result</summary>

```
> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Quickstart

> Get started with the Python or TypeScript Agent SDK to build AI agents that work autonomously

Use the Agent SDK to build an AI agent that reads your code, finds bugs, and fixes them, all without manual intervention.

**What you'll do:**

1. Set up a project with the Agent SDK
2. Create a file with some buggy code
3. Run an agent that finds and fixes the bugs automatically

## Prerequisites

* **Node.js 18+** or **Python 3.10+**
* An **Anthropic account**. If you don't have one, [sign up here](https://platform.claude.com/).

## Setup

**1. Create a project folder**

Create a new directory for this quickstart:

```bash theme={null}
mkdir my-agent
cd my-agent
```

For your own projects, you can run the SDK from any folder; it will have access to files in that directory and its subdirectories by default.

**2. Install the SDK**

Install the Agent SDK package for your language:

**TypeScript (new project)**

```bash theme={null}
npm init -y
npm pkg set type=module
npm install @anthropic-ai/claude-agent-sdk
npm install --save-dev tsx
```

Setting `"type": "module"` in `package.json` lets your agent script use top-level `await`, and [tsx](https://tsx.hirok.io) runs TypeScript files directly. npm prints `added N packages` when the install succeeds.

**TypeScript (existing project)**

```
... [truncated, 13044 more chars]
```

</details>

## Assistant turn 9  `20:59:07`

**Tool call 6: WebFetch**

```json
{"url": "https://code.claude.com/docs/en/agent-sdk/subagents.md", "prompt": "How are subagents defined programmatically in the Python SDK via the agents option (AgentDefinition)? What is the tool name the main agent uses to delegate (Agent vs Task), and does the parent need 'Agent' in allowed_tools? Are subagents loaded from .claude/agents/*.md when setting_sources includes project? Quote exact text and code."}
```

<details><summary>tool result</summary>

```
> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Subagents in the SDK

> Define and invoke subagents to isolate context, run tasks in parallel, and apply specialized instructions in your Claude Agent SDK applications.

Subagents are separate agent instances that your main agent can spawn to handle focused subtasks.
Use them to isolate context, run multiple analyses in parallel, and apply specialized instructions without adding to the main agent's prompt.

## Overview

You can create subagents in three ways:

* **Programmatically**: use the `agents` parameter in your `query()` options. See the [TypeScript](/docs/en/agent-sdk/typescript.md#agentdefinition) and [Python](/docs/en/agent-sdk/python.md#agentdefinition) references
* **Filesystem-based**: define agents as markdown files in `.claude/agents/` directories. See [defining subagents as files](/docs/en/sub-agents.md)
* **Built-in general-purpose**: Claude can invoke the built-in `general-purpose` subagent at any time via the Agent tool without you defining anything

This guide focuses on the programmatic approach, which is recommended for SDK applications.

## Benefits of using subagents

Because subagents are separate agent instances, delegating work to them gives you four benefits:

* **Context isolation**: each subagent runs in its own conversation, which starts fresh unless the subagent 
... [truncated, 39961 more chars]
```

</details>

## Assistant turn 10  `20:59:08`

**Tool call 7: WebFetch**

```json
{"url": "https://code.claude.com/docs/en/agent-sdk/mcp.md", "prompt": "How do you register a local stdio MCP server in the Python SDK (mcp_servers dict with type/command/args)? What is the tool naming convention (mcp__<server>__<tool>)? Does the SDK read .mcp.json automatically via setting_sources, and how do allowed_tools interact? Quote exact code and text."}
```

<details><summary>tool result</summary>

```
> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Connect to external tools with MCP

> Configure MCP servers to extend your agent with external tools. Covers transport types, tool search for large tool sets, authentication, and error handling.

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro) is an open standard for connecting AI agents to external tools and data sources. With MCP, your agent can query databases, integrate with APIs like Slack and GitHub, and connect to other services without writing custom tool implementations.

MCP servers can run as local processes, connect over HTTP, or execute directly within your SDK application.

> [!NOTE]
>
> This page covers MCP configuration for the Agent SDK. To add MCP servers to the Claude Code CLI so they load in every project, see [MCP installation scopes](/docs/en/mcp.md#mcp-installation-scopes).

## Quickstart

This example connects to the [Claude Code documentation](https://code.claude.com/docs) MCP server using [HTTP transport](#http%2Fsse-servers) and uses [`allowedTools`](#allow-mcp-tools) with a wildcard to permit all tools from the server.

```typescript TypeScript theme={null}
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Use the docs MCP server to explain what hooks are in Claude Co
... [truncated, 37627 more chars]
```

</details>

## Assistant turn 11  `20:59:20`

## Assistant turn 12  `20:59:20`

**Tool call 8: Read**

```json
{"file_path": "C:\\Users\\kimia\\.claude\\projects\\C--Users-kimia\\e4ab3fed-fe0c-4e63-8ea3-c5514030f294\\tool-results\\toolu_01KLdUFVmdb65NzZ85PkC5jr.txt"}
```

<details><summary>tool result</summary>

```
1	eSDKError):
2	    def __init__(
3	        self, message: str, exit_code: int | None = None, stderr: str | None = None
4	    ):
5	        self.exit_code = exit_code
6	        self.stderr = stderr
7	```
8	
9	### `ResultError`
10	
11	Raised when the Claude Code process exits because the run ended with an error [result message](#resultmessage), such as a turn-limit error or an API error. `ResultError` subclasses `ProcessError`, so an existing `except ProcessError` handler also catches it. Its attributes carry the fields of that result message, so you can branch on why the run failed without parsing the message text. Requires Python Agent SDK 0.2.140 or later.
12	
13	```python theme={null}
14	class ResultError(ProcessError):
15	    subtype: str | None  # "error_max_turns", "error_during_execution", ...; "success" when the run ended on a failed request
16	    errors: list[str]  # an empty list when the result message reported none
17	    result: str | None
18	    api_error_status: int | None
19	    terminal_reason: str | None  # "max_turns", "api_error", ...; check after data["stop_reason"], before subtype
20	    session_id: str | None
21	    data: dict[str, Any]  # the raw result message payload
22	```
23	
24	To tell failures apart, check `data["stop_reason"]` first, then `terminal_reason`, then `subtype`. A declined response has `stop_reason` `"refusal"`, usually with `subtype` `"success"`; its `terminal_reason` doesn't single it out and can read `"completed"` or `"api_error"`.
... [truncated, 67361 more chars]
```

</details>

## Assistant turn 13  `20:59:21`

**Tool call 9: WebFetch**

```json
{"url": "https://code.claude.com/docs/en/agent-sdk/claude-code-features.md", "prompt": "Explain setting_sources / settingSources precisely: the allowed values (\"user\", \"project\", \"local\"), the default when omitted in the Python SDK, and exactly what each source loads (CLAUDE.md, .claude/settings.json, .claude/agents/*.md, .claude/skills, .mcp.json, hooks). Quote the exact text and any Python code showing setting_sources=[\"project\"]."}
```

<details><summary>tool result</summary>

```
> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Claude Code features in the SDK

> Load project instructions, skills, hooks, and other Claude Code features into your SDK agents.

The Agent SDK is built on the same foundation as Claude Code, which means your SDK agents have access to the same filesystem-based features: project instructions (`CLAUDE.md` and rules), skills, hooks, and more.

When you omit `settingSources`, `query()` reads the same filesystem settings as the Claude Code CLI: user, project, and local settings, CLAUDE.md files, and `.claude/` skills, agents, and commands. To run without these, pass `settingSources: []`, which limits the agent to what you configure programmatically. Managed policy settings and the global `~/.claude.json` config are read regardless of this option. For more information, see [What settingSources does not control](#what-settingsources-does-not-control).

## Control filesystem settings with settingSources

The setting sources option ([`setting_sources`](/docs/en/agent-sdk/python#claudeagentoptions) in Python, [`settingSources`](/docs/en/agent-sdk/typescript#settingsource) in TypeScript) controls which filesystem-based settings the SDK loads. Pass an explicit list to opt in to specific sources, or pass an empty array to disable user, project, and local settings.

This example loads both user-level an
... [truncated, 18379 more chars]
```

</details>

## Assistant turn 14  `20:59:22`

**Tool call 10: WebFetch**

```json
{"url": "https://code.claude.com/docs/en/agent-sdk/permissions.md", "prompt": "List the exact permission_mode values (PermissionMode literal) and what each does, especially bypassPermissions and acceptEdits; state whether bypassPermissions is refused when running as root and any caveats about it; and how allowed_tools / disallowed_tools interact with it. Quote exact text."}
```

<details><summary>tool result</summary>

```
> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configure permissions

> Control how your agent uses tools with permission modes, hooks, and declarative allow/deny rules.

The Claude Agent SDK provides permission controls to manage how Claude uses tools. Use permission modes and rules to define what's allowed automatically, and the [`canUseTool` callback](/docs/en/agent-sdk/user-input) to handle everything else at runtime.

## How permissions are evaluated

When Claude requests a tool, the SDK checks permissions in this order:

**1. Hooks**

Run [hooks](/docs/en/agent-sdk/hooks.md) first. A hook can deny the call outright or pass it on. A hook that returns `allow` doesn't skip the deny and ask rules below, which are evaluated regardless of the hook result.

A `PreToolUse` hook that returns `allow` also can't approve an `rm` or `rmdir` command whose target Claude Code recognizes as a [critical path](/docs/en/permission-modes.md#critical-paths), such as `rm -rf ~`. For what that `allow` does in plan mode, see [Hook approvals in plan mode](/docs/en/permissions.md#hook-approvals-in-plan-mode).

**2. Deny rules**

Check `deny` rules (from `disallowed_tools` and [settings.json](/docs/en/settings-reference.md#permission-settings)). If a deny rule matches, the tool is blocked, even in `bypassPermissions` mode. Bare-name deny rules like `Bash` remove
... [truncated, 24418 more chars]
```

</details>

## Assistant turn 15  `20:59:30`

## Assistant turn 16  `20:59:31`

**Tool call 11: WebFetch**

```json
{"url": "https://code.claude.com/docs/en/authentication.md", "prompt": "Explain the authentication precedence order (ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN, CLAUDE_CODE_OAUTH_TOKEN, apiKeyHelper, Claude Code subscription login/credentials) and specifically how it applies to Agent SDK / claude -p / programmatic runs. Does the Agent SDK use a logged-in Claude Code subscription, or require an API key? Quote exact text, especially any note about third-party developers and claude.ai login."}
```

<details><summary>tool result</summary>

```
> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Authentication

> Log in to Claude Code and configure authentication for individuals, teams, and organizations.

Claude Code supports multiple authentication methods depending on your setup. Individual users can log in with a claude.ai account, while teams can use Claude for Teams or Enterprise, the Claude Console, or a cloud provider like Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry.

## Log in to Claude Code

After [installing Claude Code](/docs/en/setup.md#install-claude-code), run `claude` in your terminal. Claude Code opens a browser window for you to log in on first launch, except in cases such as these, where it can skip the login prompt:

* **API key**: you've set the `ANTHROPIC_API_KEY` environment variable and you approve the key when Claude Code asks whether to use it
* **Earlier sign-in**: you ran [`claude auth login`](/docs/en/cli-reference#cli-commands) in your shell before your first session, or you rebuilt a dev container that keeps your credentials in a [volume](/docs/en/devcontainer.md#persist-authentication-and-settings-across-rebuilds). If you see the login prompt anyway, [check what can cause it](#login-prompt-still-appears-after-an-earlier-sign-in).

If the browser doesn't open automatically, press `c` to copy the login URL to your clipboard, then pa
... [truncated, 31068 more chars]
```

</details>

## Assistant turn 17  `20:59:55`

## Assistant turn 18  `21:00:11`

**Tool call 12: SubagentHandback**

```json
{"message": "Claude Agent SDK (Python) answers, sourced from the official Agent SDK docs on code.claude.com. The docs do not state a current pip version number, so check it with `pip show claude-agent-sdk`. Several of your assumptions need correcting (see \"Corrections\" below).\n\nSOURCES\n- Python reference: https://code.claude.com/docs/en/agent-sdk/python.md\n- Quickstart (install, bundled CLI, API key): https://code.claude.com/docs/en/agent-sdk/quickstart.md\n- Subagents: https://code.claude.com/docs/en/agent-sdk/subagents.md\n- MCP: https://code.claude.com/docs/en/agent-sdk/mcp.md\n- Filesystem settings / setting_sources: https://code.claude.com/docs/en/agent-sdk/claude-code-features.md\n- Permissions: https://code.claude.com/docs/en/agent-sdk/permissions.md\n- Authentication: https://code.claude.com/docs/en/authentication.md\n- Docs index: https://code.claude.com/docs/en/claude_code_docs_map.md\n\nIMPORTS (verified in the docs examples)\nfrom claude_agent_sdk import (\n    query, ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition,\n    AssistantMessage, TextBlock, ToolUseBlock, ToolResultBlock,\n    ResultMessage, SystemMessage, HookMatcher, ResultError, CLINotFoundError,\n)\n- ToolUseBlock is imported from the top-level package in the subagents page example. The Python reference page itself does not show that import line.\n- PermissionResultAllow, PermissionResultDeny, ToolPermissionContext come from claude_agent_sdk.types in the docs.\n\nClaudeAgentOptions (snake_case; all of your listed fields exist)\n- agents: dict[str, AgentDefinition] | None\n- mcp_servers: dict[str, McpServerConfig] | str | Path (default {})\n- allowed_tools: list[str] (default [])\n- disallowed_tools: list[str] (default [])\n- permission_mode: PermissionMode | None. Values: \"default\", \"dontAsk\", \"acceptEdits\", \"bypassPermissions\", \"plan\", \"auto\"\n- cwd: str | Path | None\n- setting_sources: list[SettingSource] | None. Values: \"user\", \"project\", \"local\". Omitted = [\"user\",\"project\",\"local\"].\n- max_turns: int | None\n- model: str | None (aliases such as \"sonnet\", \"opus\", \"haiku\", \"fable\", \"inherit\", or a full model ID)\n- Other useful fields: system_prompt, tools, max_budget_usd, can_use_tool, hooks, add_dirs, env, cli_path, sandbox, skills, resume, continue_conversation, include_partial_messages, effort, thinking.\n\nAgentDefinition (a dataclass). It has NO name field: the name is the dict key in `agents`. Field names are camelCase for thes
... [truncated, 9000 more chars]
```

<details><summary>tool result</summary>

```
{"success":true,"message":"Report delivered to your caller."}
```

</details>
