---
source_anchor: "README.md#installation"
source_commit: "04aab86d266ac4018890b67355acbc962e1bb664"
status: "updated"
---

**Why flagged:** README.md: The README no longer includes the detailed .env setup and uv‑specific steps; installation now uses generic git clone and pip install.

Clone the repository:  
```bash
git clone https://github.com/Shivansh0047/Personal_mcp.git
cd Personal_mcp
```  

(Optional) Create and activate a virtual environment so the installation does not affect your global Python installation:  
```bash
python -m venv .venv
# Unix/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```  

### Install a project  

Each sub‑directory under the repository is a self‑contained MCP project with its own `pyproject.toml`. Install the dependencies for the project you want to work with in editable mode; this also pulls in the new **python‑dotenv** dependency.

```bash
# Example: System Monitor MCP Server
cd system_monitor_mcp_server
pip install -e .
```  

### Provide configuration (optional)  

If the project reads configuration values from environment variables, create a `.env` file in the project root (or repository root) and add the required keys. For the System Monitor server a typical file looks like:

```dotenv
FASTMCP_HOST=0.0.0.0
FASTMCP_PORT=8000
```  

The server automatically loads this file at startup via `python‑dotenv`. If no `.env` file is present, default settings are used.

### Run the project  

```bash
# System Monitor (local stdio mode)
python src/system_monitor/server.py
```  

Other projects have their own entry points. For example:

```bash
# Simple Calculator with Dice Roll – Local (uses uv)
cd Simple_Calculator_with_Dice_Roll_Local_MCP_Server
uv run server.py
```

or, after installing with `pip install -e .`:

```bash
cd Simple_Calculator_with_Dice_Roll_Local_MCP_Server
python main.py
```  

These steps install all current dependencies, optionally let you override configuration through a `.env` file, and start the chosen FastMCP‑based MCP server.
