# eairt-store

The eairt store: the persisted text the eairt agent workers read, one top-level folder per
kind. Workers pin this repository once per run, so every folder is read at the same commit.

| Folder | Served as | What goes in it |
|---|---|---|
| `knowledge/` | `knowledge://system/...` | System knowledge: policies, `AGENTS.md`, `profiles/<name>/PROFILE.md` |
| `skills/` | `skill://<name>/...` | One Claude Code skill per directory (`<name>/SKILL.md`, `scripts/`, `references/`) |

A worker materialises only the folder a scheme maps. Nothing at the root (this README
included) and no other folder can be read through a logical path. A new kind of persisted
text gets its own folder, and it is read only once a use case maps a scheme to it.

Configure a worker with `EAIRT_STORE_URL=https://github.com/flycloudcnc/eairt-store.git`, plus
`EAIRT_STORE_REF` (default `main`) and, for a private copy, a read-only `EAIRT_STORE_TOKEN`.
A change is a merged commit here. The next run reads it, and nothing is rebuilt or redeployed.
