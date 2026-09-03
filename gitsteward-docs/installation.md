---
source_anchor: "README.md#installation"
source_commit: "397b112f70b30ca0bd4ec90210908ecf2c016f20"
status: "updated"
---

**Why flagged:** system_monitor_mcp_server/pyproject.toml: Installation instructions assume running `uv sync` at the repo root, but the new pyproject.toml resides in a subfolder

Clone the repository:  
```bash
git clone https://github.com/Shivansh0047/Personal_mcp.git
```  

Enter the directory that contains the project definition:  
```bash
cd Personal_mcp/system_monitor_mcp_server
```  

Install the project's dependencies (this will also create a virtual environment if one does not already exist):  
```bash
uv sync
```  

The `uv sync` command reads the `pyproject.toml` located in this folder, resolves the required packages, and installs them into the newly‑created environment. After the sync completes you can run the server directly via the installed console script:

```bash
system-monitor
```  

(If you prefer a classic `pip` workflow, you can also install the package in editable mode with `pip install -e .` after activating a virtual environment.)
