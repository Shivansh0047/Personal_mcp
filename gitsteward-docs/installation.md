---
source_anchor: "README.md#installation"
source_commit: "b0a19e0cc647bd638c9848b681df48d741980fbe"
status: "updated"
---

**Why flagged:** system_monitor_mcp_server/src/system_monitor/server.py: The server now imports python‑dotenv, but the installation instructions don’t mention installing this dependency or setting up a .env file.

Clone the repository:  
```bash
git clone https://github.com/Shivansh0047/Personal_mcp.git
```  

Enter the directory that contains the server code:  
```bash
cd Personal_mcp/system_monitor_mcp_server
```  

(Optional) Create and activate a virtual environment so the installation does not affect your global Python installation:  
```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
```  

Install the package in editable mode, which also pulls in the new **python‑dotenv** dependency declared in `pyproject.toml`:  
```bash
pip install -e .
```  

If you need to provide configuration values (e.g., custom FastMCP host or port), create a `.env` file in the project root and add the required variables, for example:  
```dotenv
FASTMCP_HOST=0.0.0.0
FASTMCP_PORT=8000
```  
The server automatically loads this file at startup via `python‑dotenv`. If no `.env` file is present, default settings are used.

Run the server locally:  
```bash
python src/system_monitor/server.py
```  

These steps install all current dependencies, optionally allow you to override configuration through a `.env` file, and start the FastMCP‑based system‑monitoring server that provides CPU, RAM, disk, process, and log monitoring APIs.
