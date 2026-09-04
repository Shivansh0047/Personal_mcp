---
source_anchor: "README.md#about"
source_commit: "86a1ff1e2b52118b55942dd654bf05bf6fb6cc98"
status: "updated"
---

**Why flagged:** system_monitor_mcp_server/README.md: The added README omits the about section, rendering it outdated.

This repository houses a collection of independent Model Context Protocol (MCP) server implementations. Each server is a self‑contained Python package that exposes a set of tools callable by any MCP‑compatible client (Claude Desktop, custom agents, etc.). The overarching goal is to explore MCP by providing practical, reusable services that can be run locally or deployed as standalone services.

**Current projects**

- **System Monitor MCP Server** – a FastMCP server that offers a health‑check (`ping`) and a comprehensive suite of system‑monitoring tools:
  - `get_cpu_usage` – CPU statistics  
  - `get_ram_usage` – RAM and swap usage  
  - `get_disk_usage` – disk partition usage  
  - `get_running_processes` – top‑process snapshot  
  - `find_process` – search processes by name  
  - `list_log_files` – discover log files on the host  
  - `read_log_file` – read and filter log contents  
  - `analyze_log_file` – summarize errors and warnings  
  - `detect_anomalies` – compute a health score across metrics  

  Install with `pip install -e .` and start the server via:

  ```bash
  python src/system_monitor/server.py
  ```

- **Other MCP servers** – additional projects remain in the repository, each with its own README that describes its purpose, available tools, and usage instructions.

All servers share a common design: they expose functions as MCP tools using the `fastmcp` framework, can be invoked remotely via the MCP protocol, and are intended for learning, experimentation, and building practical AI‑driven applications.
