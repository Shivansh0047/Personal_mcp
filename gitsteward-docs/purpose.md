---
source_anchor: "README.md#purpose"
source_commit: "86a1ff1e2b52118b55942dd654bf05bf6fb6cc98"
status: "updated"
---

**Why flagged:** system_monitor_mcp_server/README.md: The new README no longer includes the purpose description, making it stale.

This repository provides a FastMCP server that exposes a suite of system‑monitoring tools. It enables:

- **Health checks** via a simple `ping` endpoint.  
- **Resource metrics**: CPU usage, RAM (including swap), and disk partition statistics.  
- **Process inspection**: list of running processes, top‑resource consumers, and name‑based search.  
- **Log handling**: discovery of log files, reading with optional filtering, and summarising errors/warnings.  
- **Anomaly detection**: combines the above data into a health score to flag abnormal conditions.  

The server is intended as a reusable MCP component for local automation, observability pipelines, and AI‑driven workflows. Install locally with `pip install -e .` and start the service via `python src/system_monitor/server.py`.
