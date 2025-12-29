<!-- Copilot instructions for contributors and AI coding agents -->
# Project-specific guidance for AI coding agents

This repository contains small MCP (Model Context Protocol) demo servers and clients used in hands-on workshops. The guidance below focuses on the concrete patterns, run/debug commands, and code examples an AI agent should use when making edits.

- **Big picture:** MCP servers are implemented with `FastMCP` (see `code/0-mcp-demo/*`). Servers expose tools via the `@mcp.tool()` decorator and resources via `@mcp.resource(...)`. Clients use `ClientSession` with transport helpers like `streamablehttp_client` and `stdio_client`.

- **Key files:**
  - `code/0-mcp-demo/stdio/stdio_server.py` — shows `@mcp.tool()` examples (`get_weather`, `summarize`, `add`, `list_folders_under_roots`) and use of `ctx` for `session` and progress reporting.
  - `code/0-mcp-demo/http/http_server.py` — minimal `FastMCP` server run with `transport="streamable-http"`.
  - `code/0-mcp-demo/http/http_client.py` and `code/0-mcp-demo/stdio/stdio_client.py` — client usage patterns (`ClientSession`, `streamablehttp_client`, `stdio_client`).
  - `README.md` — contains local dev commands and MCP Inspector instructions.

- **Typical patterns to follow (concrete):**
  - Tools are async and accept a `ctx: Context` param for access to `ctx.session`, `ctx.info(...)`, and `ctx.report_progress(...)`.
    - Example signature: `async def summarize(text_to_summarize: str, ctx: Context)` in `stdio_server.py`.
  - Use `ctx.session.create_message(...)` to run sampling/LLM calls (see `summarize`). Check `result.content.type == "text"` before returning text.
  - Publish small helper functions as `@mcp.resource("file:///<path>")` when you need to expose filesystem content (see `get_file()` in `stdio_server.py`). Use absolute paths constructed from `__file__` as shown.

- **Run / development commands (from README):**
  - Setup venv (project-specific helper `uv` is used in the README):

    ```bash
    cd code
    uv sync
    uv venv
    source .venv/bin/activate
    ```

  - Start stdio server for interactive JSON-RPC testing:

    ```bash
    cd code/0-mcp-demo/stdio
    python stdio_server.py
    ```

  - Start the HTTP server (uses `streamable-http` transport):

    ```bash
    python code/0-mcp-demo/http/http_server.py
    ```

- **Inspector / debug:** MCP Inspector can be launched with `npx @modelcontextprotocol/inspector` or via the brew installation described in `README.md`. The inspector expects the python executable path and the server script path as arguments (the README shows an example command).

- **Dependencies & packaging:** See `code/pyproject.toml` — this project expects `fastmcp`, `mcp[cli]`, `fastapi`, and sampling-related packages. Avoid changing dependency names without verifying `pyproject.toml` updates.

- **Conventions & constraints:**
  - Do not convert async tool handlers to synchronous functions. The MCP runtime expects `async` coroutines.
  - Keep `ctx` usage consistent: logging/info via `await ctx.info(...)`, progress via `await ctx.report_progress(percent, total)`.
  - Return simple JSON-serializable values (int, str, dict). When returning results from LLM sampling, extract `result.content.text`.

- **When you change server APIs:** Update both server and example client in `code/0-mcp-demo/*_client.py` so demos remain runnable.

- **Examples to copy/reuse:**
  - Call a tool from client (see `http_client.py`): initialize session, `await session.list_tools()`, `await session.call_tool(name="get_weather", arguments={...})` and inspect `result.content`.

If anything is unclear or you want more examples pulled from specific files, tell me which file(s) and I'll expand or adjust these instructions.
