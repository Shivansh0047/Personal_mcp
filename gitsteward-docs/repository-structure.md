---
source_anchor: "README.md#repository-structure"
source_commit: "397b112f70b30ca0bd4ec90210908ecf2c016f20"
status: "updated"
---

**Why flagged:** system_monitor_mcp_server/pyproject.toml: pyproject.toml is now located inside a subdirectory rather than at the repository root as depicted

system_monitor_mcp_server/
│
├── src/
│   └── system_monitor/
│       ├── __init__.py
│       ├── server.py          # entry point for the MCP server (exposes `main`)
│       └── …                  # additional modules implementing monitoring logic
│
├── tests/
│   └── …                      # test suite for the package
│
├── pyproject.toml             # build configuration, dependencies and console script
├── uv.lock                    # lock file for reproducible installs
├── README.md                  # overview, usage instructions and contribution guide
└── .gitignore                 # standard ignore patterns
```text
Each project is now a self‑contained Python package following the conventional
`src/` layout. The `pyproject.toml` lives inside the top‑level
`system_monitor_mcp_server` directory and defines:

- Build system (hatchling)
- Project metadata (name, version, description, Python requirement)
- Runtime dependencies (`fastmcp`, `psutil`)
- Console script entry point `system-monitor` → `system_monitor.server:main`

All source code resides under `src/system_monitor`, while tests are placed in
`tests/`. The repository also includes a lock file (`uv.lock`) for deterministic
dependency resolution and a README with usage details.
