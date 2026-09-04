---
source_anchor: "README.md#personal-mcp"
source_commit: "86a1ff1e2b52118b55942dd654bf05bf6fb6cc98"
status: "updated"
---

**Why flagged:** system_monitor_mcp_server/README.md: The personal‑mcp overview was eliminated by the new concise README.

A **FastMCP server** that offers real‑time monitoring of the host system. It implements a collection of RPC tools for retrieving hardware statistics, process information, and log data, plus simple health‑check and anomaly‑detection utilities.

### Provided tools
- `ping` – basic health check  
- `get_cpu_usage` – current CPU utilization  
- `get_ram_usage` – RAM and swap usage  
- `get_disk_usage` – usage per disk partition  
- `get_running_processes` – list of active processes (top consumers)  
- `find_process` – locate processes by name  
- `read_log_file` – read a log file with optional filtering  
- `analyze_log_file` – summarize errors and warnings in a log  
- `list_log_files` – discover available log files on the system  
- `detect_anomalies` – compute an overall health score and flag outliers  

### Running the server locally
```bash
pip install -e .
python src/system_monitor/server.py
```

The server starts an MCP endpoint that can be queried by any MCP‑compatible client to obtain the above metrics and diagnostics.
