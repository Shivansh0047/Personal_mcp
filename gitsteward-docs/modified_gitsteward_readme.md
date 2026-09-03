# Personal MCP

A collection of **personal Model Context Protocol (MCP) projects** built while exploring the MCP ecosystem. This repository serves as a playground for experimenting with MCP servers, tool development, database integrations, AI workflows, and real-world automation.  
All projects are managed using **uv**, providing fast dependency management, virtual environments, and reproducible development environments.  
---

## About

This repository contains multiple standalone MCP projects developed for learning, experimentation, and building practical AI applications.  
The primary objective is to explore the **Model Context Protocol (MCP)** by creating servers that expose useful tools which can be consumed by MCP-compatible clients such as Claude Desktop or custom AI agents.  
Projects range from simple examples to more feature-rich applications involving databases, local automation, and external APIs.  
---

## Features

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
- Detailed RAM and swap usage: total, used, available in GB, percentage used, timestamped results  
- Disk usage inspection: per‑path totals, free space, usage percentage, full‑partition enumeration, timestamped results  
- Process enumeration: list of running processes with PID, name, status, memory %, CPU %, username, start time; sortable by memory, CPU or name; limitable to avoid context overload, timestamped results  
- Process search: case‑insensitive partial name matching, returns matching processes with command line and start time, timestamped results  
- Log file handling: safe discovery of `.log` and `.txt` files, size‑aware reading of recent lines, optional level filtering, timestamped results  
- Log analysis: automatic counting of errors and warnings, identification of most frequent error messages, recent error/warning excerpts, size checks, timestamped results  
- Anomaly detection: evaluates CPU, RAM, swap, disk usage and top resource‑hog processes, produces a numeric health score (0‑100), a textual health status (Healthy / Degraded / Critical), prioritized lists of criticals, warnings and informational messages, a concise summary, and a `sampled_at` ISO‑8601 timestamp  

- Utilizes **psutil** for cross‑platform system metrics  
- All tool outputs include a `sampled_at` ISO‑8601 timestamp for traceability

## Repository Structure

```text
Personal_mcp/
│
├── Project_1/
├── Project_2/
├── Project_3/
│
├── pyproject.toml
├── uv.lock
└── README.md
```  
Each project is self-contained and may include its own:  
- MCP server
- Database
- Configuration files
- Tool implementations
- Documentation  
---

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
Navigate into the project:  
```bash
cd Personal_mcp
```  
Install all dependencies:  
```bash
uv sync
```  
This command automatically creates a virtual environment (if needed) and installs all required packages.  
---

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

This repository is intended for:  
- Learning MCP development
- Building reusable MCP tools
- Experimenting with AI workflows
- Developing local automation servers
- Exploring database-backed MCP applications
- Understanding how LLMs interact with external tools  
---

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
