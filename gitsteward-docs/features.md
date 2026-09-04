---
source_anchor: "README.md#features"
source_commit: "04aab86d266ac4018890b67355acbc962e1bb664"
status: "updated"
---

**Why flagged:** README.md: The "Features" section was deleted from the README, making the previous description outdated.

- Multiple independent MCP projects, each self‑contained  
- Implemented in Python 3.10+  
- Dependency management via **uv** (or `pip` where preferred) with reproducible virtual environments  
- System‑monitor MCP server built with FastMCP and **psutil**, exposing a rich set of monitoring tools  
- SQLite persistence for stateful MCP services (e.g., expense tracker)  
- AI‑friendly tool interfaces designed for seamless LLM invocation  
- Modular, extensible project layout that makes adding new MCP servers or tools straightforward  

**Provided tools** (system_monitor_mcp_server)  
- `ping` – simple health‑check endpoint returning a `sampled_at` ISO‑8601 timestamp  
- `get_cpu_usage` – overall and per‑core usage percentages, core count, current/min/max frequency, with `sampled_at`  
- `get_ram_usage` – total, used and available RAM and swap (GB and %), with `sampled_at`  
- `get_disk_usage` – per‑mount‑point total, used, free space and usage %; enumerates all partitions, with `sampled_at`  
- `get_running_processes` – list of active processes (PID, name, status, memory %, CPU %, username, start time); sortable and limitable, with `sampled_at`  
- `find_process` – case‑insensitive partial‑name search returning matching processes, command line and start time, with `sampled_at`  
- `list_log_files` – safe discovery of `.log` and `.txt` files under configured directories, size‑aware listing, with `sampled_at`  
- `read_log_file` – read recent lines from a log file, optional level filtering, size‑aware handling, with `sampled_at`  
- `analyze_log_file` – count errors and warnings, highlight most frequent error messages, provide recent excerpts and size checks, with `sampled_at`  
- `detect_anomalies` – evaluates CPU, RAM, swap, disk usage and top resource‑hog processes; returns a numeric health score (0‑100), a textual status (Healthy / Degraded / Critical), prioritized lists of critical/warning/info messages, a concise summary, and a `sampled_at` ISO‑8601 timestamp  

- All tool outputs include a `sampled_at` ISO‑8601 timestamp for traceability  
- System metrics are gathered via **psutil**, ensuring cross‑platform compatibility
