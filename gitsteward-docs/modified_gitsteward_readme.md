# Personal MCP

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

## About

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

## Features

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

## Repository Structure

system_monitor_mcp_server/
│
├── src/
│   └── system_monitor/
│       ├── __init__.py               # makes `system_monitor` a package
│       ├── server.py                 # entry point for the MCP server (exposes `main`)
│       └── …                         # additional modules that implement the monitoring logic
│
├── tests/
│   └── …                             # test suite for the package
│
├── pyproject.toml                    # build configuration, project metadata, runtime dependencies and console‑script entry point
├── uv.lock                           # lock file for deterministic dependency resolution
├── README.md                         # short overview, list of available monitoring tools and local‑run instructions
└── .gitignore                        # standard ignore patterns

**Key points**

* The repository follows the conventional *src/* layout, making the package self‑contained.
* All production code lives under `src/system_monitor`; the test suite is placed in the top‑level `tests/` directory.
* `pyproject.toml` uses **hatchling** as the build backend and defines:
  * Project metadata (name, version, description, required Python version).
  * Runtime dependencies: `fastmcp` and `psutil`.
  * A console‑script entry point `system-monitor` that maps to `system_monitor.server:main`.
* `uv.lock` pins exact versions of dependencies to ensure reproducible installations.
* The newly added `README.md` provides a concise description of the server, enumerates the monitoring tools it exposes (e.g., `ping`, `get_cpu_usage`, `read_log_file`, etc.), and shows how to run the server locally:

  ```bash
  pip install -e .
  python src/system_monitor/server.py
  ```

* No repository‑structure diagram is present in the README; the layout is documented here instead.

## Requirements

- Python 3.10 or later
- uv  
Install **uv** using pip:  
```bash
pip install uv
```  
Verify the installation:  
```bash
uv --version
```  
---

## Installation

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

## Running a Project

Navigate to the desired project.  
For example:  
```bash
cd ExpenseTracker
```  
Run the project:  
```bash
uv run main.py
```  
or  
```bash
uv run server.py
```  
depending on the project structure.  
---

## Managing Dependencies

Add a package:  
```bash
uv add package_name
```  
Remove a package:  
```bash
uv remove package_name
```  
Synchronize dependencies:  
```bash
uv sync
```  
Run any Python script:  
```bash
uv run script.py
```  
---

## Technologies Used

- Python
- Model Context Protocol (MCP)
- FastMCP
- SQLite
- JSON
- uv
- asyncio  
---

## Purpose

This repository provides a FastMCP server that exposes a suite of system‑monitoring tools. It enables:

- **Health checks** via a simple `ping` endpoint.  
- **Resource metrics**: CPU usage, RAM (including swap), and disk partition statistics.  
- **Process inspection**: list of running processes, top‑resource consumers, and name‑based search.  
- **Log handling**: discovery of log files, reading with optional filtering, and summarising errors/warnings.  
- **Anomaly detection**: combines the above data into a health score to flag abnormal conditions.  

The server is intended as a reusable MCP component for local automation, observability pipelines, and AI‑driven workflows. Install locally with `pip install -e .` and start the service via `python src/system_monitor/server.py`.

## Contributing

This repository is primarily for personal experimentation, but suggestions and improvements are always welcome.  
If you have ideas or find any issues, feel free to open an issue or submit a pull request.  
---

## License

This project is licensed under the MIT License.  
---

## Author

**Shivansh Pandey**  
GitHub: https://github.com/Shivansh0047
