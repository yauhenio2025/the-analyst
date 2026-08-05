# Migration Guide: Analyzer & Visualizer Have New URLs

**From:** Evgeny
**For:** Anyone consuming the Analyzer or Visualizer services (including via the Visualizer MCP server)
**Date:** 2026-08-05

This document is written so you can feed it directly to Claude Code (or any coding agent) and have it apply the changes to your local setup. Human summary first, agent instructions below.

## What happened

The Analyzer and Visualizer services moved to a different Render account. **The services themselves are unchanged** — same code, same API keys, same endpoints, same behavior. The only thing that changed is their hostnames:

| Service | OLD URL (stops working after cutover) | NEW URL |
|---|---|---|
| Analyzer API | `https://analyzer-3wsg.onrender.com` | `https://analyzer-43fk.onrender.com` |
| Visualizer | `https://visualizer-tw4i.onrender.com` | `https://visualizer-alu5.onrender.com` |
| Analyzer v2 (if you ever reference it) | `https://analyzer-v2.onrender.com` | `https://analyzer-v2-3blo.onrender.com` |

**Timing:** the cutover has happened — the old URLs are now suspended and no longer respond. Apply these changes right away; the new URLs are live with all data migrated. Applying takes a few minutes; no other coordination needed.

**API keys:** all existing keys (`ANALYZER_API_KEY`, etc.) keep working unchanged. Nothing to rotate on your side. This document intentionally contains no secrets.

---

## Instructions for the coding agent

You are updating a local development environment to point at the new hostnames. Apply the following, adapting to whatever is actually present on this machine — the file list below is from a reference checkout and may differ here.

### Step 1 — Find every reference

Search the user's project directories (and Claude/MCP config locations) for the old hostnames:

```bash
grep -rn --exclude-dir={node_modules,.git,venv,__pycache__,dist,build} \
  -e "analyzer-3wsg.onrender.com" \
  -e "visualizer-tw4i.onrender.com" \
  ~/projects 2>/dev/null
grep -rn "onrender.com" ~/.claude.json ~/.claude/settings.json 2>/dev/null
```

Also check for MCP registrations: run `claude mcp list` and look for a `visualizer` server (stdio, pointing at a wrapper script in a visualizer checkout).

### Step 2 — Replace hostnames

In every **functional** file found (env files, configs, code defaults, install scripts), replace:

- `analyzer-3wsg.onrender.com` → `analyzer-43fk.onrender.com`
- `visualizer-tw4i.onrender.com` → `visualizer-alu5.onrender.com`
- `analyzer-v2.onrender.com` → `analyzer-v2-3blo.onrender.com` (only if present)

Leave documentation/markdown/historical files alone unless the user wants them updated.

Known likely locations (from the reference checkout of the `visualizer` repo):

| File | What to change |
|---|---|
| `visualizer/mcp_server/.env.mcp` | `VISUALIZER_API_URL` and `ANALYZER_API_URL` values |
| `visualizer/mcp_server/.env.mcp.template` | same two values |
| `visualizer/mcp_server/install-mcp-server.sh` | hardcoded fallback URLs (~lines 85–86 and 233–234) |
| `visualizer/mcp_server/mcp_server.py` | default values in `os.environ.get(...)` calls (~lines 10–11, 166–167) |
| `visualizer/mcp_server/job_poller.py` | default `VISUALIZER_API_URL` (~line 33) |
| any `.env` / `.env.local` files in consuming projects | any of the three hostnames |

### Step 3 — Refresh the MCP server registration (if one exists)

If `claude mcp list` shows a `visualizer` server: the registration itself (a wrapper-script path) usually doesn't change — only the `.env.mcp` it reads. After editing `.env.mcp`, restart Claude Code / Claude Desktop so the MCP server picks up the new URLs. If the setup was originally created by `install-mcp-server.sh`, re-running that script (after Step 2's edits) is the cleanest refresh.

### Step 4 — Verify

```bash
curl -s https://analyzer-43fk.onrender.com/health          # expect HTTP 200 JSON
curl -s -o /dev/null -w '%{http_code}\n' https://visualizer-alu5.onrender.com/   # expect 200 (or app-normal response)
```

Then exercise one real workflow through the MCP server or client code to confirm end-to-end.

### Step 5 — Report

Summarize to the user: which files were changed, which old-hostname references were found but intentionally left (docs/history), and the verification results. If anything failed verification, do not revert — report the failure so it can be relayed back to Evgeny.

---

**Problems?** Write back to Evgeny with the failing command/output.
