---
source_anchor: "README.md#features"
source_commit: "0f7ce0991b795fb25f39336b105d20abde588e22"
status: "updated"
---

**Why flagged:** system_monitor_mcp_server/src/system_monitor/server.py: Several new monitoring tools (CPU, RAM, disk, process, log analysis, anomaly detection) are introduced but not reflected in the feature list.

- Multiple independent MCP projects  
- Built with Python  
- Managed using **uv**  
- FastMCP‑based server exposing a rich set of system‑monitoring tools  
- SQLite database integration for MCP state persistence  
- AI‑friendly tool interfaces that can be invoked by language models  
- Modular and extensible project structure  
- Easy to add new MCP servers and tools  

**Comprehensive system‑monitoring suite**  
- Real‑time CPU statistics: overall usage, per‑core percentages, core counts, current/min/max frequency, timestamped results  
- Detailed RAM and swap usage: total, used, available in GB, percentage used, timestamped results  
- Disk usage inspection: per‑path totals, free space, usage percentage, full partition enumeration, timestamped results  
- Process enumeration: list of running processes with PID, name, status, memory % , CPU % , username, start time; sortable by memory, CPU or name; limitable to avoid context overload, timestamped results  
- Process search: case‑insensitive partial name matching, returns matching processes with command line and start time, timestamped results  
- Log file handling: safe discovery of `.log` and `.txt` files, size‑aware reading of recent lines, optional level filtering, timestamped results  
- Log analysis: automatic counting of errors and warnings, identification of most frequent error messages, recent error/warning excerpts, size checks, timestamped results  
- Anomaly detection: health check that evaluates CPU, RAM, swap, disk usage and top resource‑hogs, produces a health score (0‑100), status badge, prioritized criticals/warnings/info, summary and timestamp  

- Utilizes **psutil** for cross‑platform system metrics  
- All tool outputs include a `sampled_at` ISO‑8601 timestamp for traceability
