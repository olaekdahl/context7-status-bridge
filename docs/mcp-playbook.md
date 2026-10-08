# Context7 MCP playbook

## Why use Context7 in this repo

Use Context7 when the task depends on current framework or library behavior, example patterns, or version-specific guidance. Do not use it as a substitute for understanding the local codebase.

A good workflow is:

1. Read the repo files first.
2. Identify the exact library question.
3. Use Context7 for that narrow question.
4. Compare the docs result with the local code before editing.
5. Explain the change in plain language.

## Setup

Project MCP config lives in `.cursor/mcp.json`. Open this folder in Cursor, then open **Customize** and confirm the `context7` server is connected.

If the server asks for a key, export it in the terminal before you start Cursor:

```bash
export CONTEXT7_API_KEY=your_key_here
```

When Agent calls a Context7 tool, read the approval card before you allow it. The server name in `.cursor/mcp.json` is `context7`.

## Good prompts

- `Use Context7 to confirm the current FastAPI recommendation for startup/lifespan handling.`
- `Use Context7 to verify current httpx timeout and error handling examples before changing feed fetching.`
- `Use Context7 to compare current FastAPI TestClient guidance with our existing tests.`

## What not to do

- Do not ask Context7 broad questions when the repo itself already answers them.
- Do not let documentation lookup replace tests.
- Do not copy large examples without adapting them to the actual repo.
- Do not allowlist `context7:*` in `.cursor/permissions.json` until you have seen which tools the server exposes.
