# System Monitor MCP Server

A FastMCP server for monitoring CPU, RAM, disk, processes, and logs.

## Tools
- `ping` — health check
- `get_cpu_usage` — CPU stats
- `get_ram_usage` — RAM + swap
- `get_disk_usage` — disk partitions
- `get_running_processes` — top processes
- `find_process` — search by name
- `read_log_file` — read + filter logs
- `analyze_log_file` — error/warning summary
- `list_log_files` — discover logs
- `detect_anomalies` — full health score

## Run locally
```bash
pip install -e .
python src/system_monitor/server.py
```