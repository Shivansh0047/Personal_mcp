---
source_anchor: "README.md#installation"
source_commit: "86a1ff1e2b52118b55942dd654bf05bf6fb6cc98"
status: "updated"
---

**Why flagged:** system_monitor_mcp_server/README.md: Installation instructions were removed in the new README.

Clone the repository:  
```bash
git clone https://github.com/Shivansh0047/Personal_mcp.git
```  

Enter the directory that contains the server code:  
```bash
cd Personal_mcp/system_monitor_mcp_server
```  

(Optionally create and activate a virtual environment so the installation does not affect your global Python.)  
```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
```  

Install the package in editable mode so you can modify the source and have the changes reflected immediately:  
```bash
pip install -e .
```  

Run the server locally:  
```bash
python src/system_monitor/server.py
```  

These steps install the current dependencies defined in `pyproject.toml` and start the FastMCP server that provides CPU, RAM, disk, process, and log monitoring APIs.
