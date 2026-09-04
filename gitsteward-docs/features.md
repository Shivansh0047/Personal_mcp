---
source_anchor: "README.md#features"
source_commit: "86a1ff1e2b52118b55942dd654bf05bf6fb6cc98"
status: "updated"
---

**Why flagged:** system_monitor_mcp_server/README.md: The README was replaced with a new minimal version, removing the detailed features section.

- Multiple independent MCP projects  
- Built with Python  
- Managed using **uv**  
- FastMCP‑based server exposing a rich set of system‑monitoring tools  
- SQLite database integration for MCP state persistence  
- AI‑friendly tool interfaces that can be invoked by language models  
- Modular and extensible project structure  
- Easy to add new MCP servers and tools  

**Provided tools**  
- `ping` – simple health‑check endpoint returning a `sampled_at` timestamp  
- `get_cpu_usage` – overall and per‑core usage percentages, core count, current/min/max frequency, with `sampled_at`  
- `get_ram_usage` – total, used and available RAM and swap (GB and %), with `sampled_at`  
- `get_disk_usage` – per‑mount‑point total, used, free space and usage %; enumerates full partitions, with `sampled_at`  
- `get_running_processes` – list of active processes (PID, name, status, memory %, CPU %, username, start time); sortable and limitable, with `sampled_at`  
- `find_process` – case‑insensitive partial‑name search returning matching processes, command line and start time, with `sampled_at`  
- `list_log_files` – safe discovery of `.log` and `.txt` files under configured directories, size‑aware listing, with `sampled_at`  
- `read_log_file` – read recent lines from a log file, optional level filtering, size‑aware handling, with `sampled_at`  
- `analyze_log_file` – count errors and warnings, highlight most frequent error messages, provide recent excerpts and size checks, with `sampled_at`  
- `detect_anomalies` – evaluates CPU, RAM, swap, disk usage and top resource‑hog processes; returns a numeric health score (0‑100), a textual status (Healthy / Degraded / Critical), prioritized lists of critical/warning/info messages, a concise summary, and a `sampled_at` ISO‑8601 timestamp  

- All tool outputs include a `sampled_at` ISO‑8601 timestamp for traceability  
- System metrics are gathered via **psutil**, ensuring cross‑platform compatibility
