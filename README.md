# eairt-store

The eairt store: the persisted text the eairt agent workers read, one top-level folder per
kind. Workers pin this repository once per run, so every folder a run reads is read at the same
commit.

| Folder | Served as | What goes in it |
|---|---|---|
| `knowledge/` | `knowledge://system/...` | System knowledge: policies, `AGENTS.md`, `profiles/<name>/PROFILE.md` |
| `skills/` | `skill://<name>/...` | One Claude Code skill per directory (`<name>/SKILL.md`, `scripts/`, `references/`) |
| `mcp/` | nothing: read at **deploy** | `mcp.json`, the workers' MCP servers and each tool's `write_class` ([fccnc/eairt-tinker#229](https://github.com/fccnc/eairt-tinker/issues/229)) |

A worker materialises only the folder a scheme maps. Nothing at the root (this README
included) and no other folder can be read through a logical path. A new kind of persisted
text gets its own folder, and it is read only once a use case maps a scheme to it.

Configure a worker with `EAIRT_STORE_URL=https://github.com/flycloudcnc/eairt-store.git`, plus
`EAIRT_STORE_REF` (default `main`) and, for a private copy, a read-only `EAIRT_STORE_TOKEN`.
A change to `knowledge/` or `skills/` is a merged commit here. The next run reads it, and
nothing is rebuilt or redeployed.

**`mcp/` is the exception.** An MCP server is a connection a worker opens at startup, so no run
reads this folder. The deploy script (`deploy/eairt-deploy.sh` in eairt-tinker) renders
`mcp/mcp.json` into the workers' ConfigMap at the commit it pins. Before applying anything, it
refuses a document that fails to parse, one that holds a credential value (credentials go in as
`{"credential": {"env": "<VARIABLE>"}}`), and one that names an HTTP server the worker
NetworkPolicy does not allow. The workers roll only when this document changes. A change here
takes effect on the next deploy, and a tool it adds still needs a human to admit it before any
run can be granted it. `{"servers": []}` means no MCP servers. A missing `mcp/mcp.json` fails
the deploy.
