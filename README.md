# Personal MCP

A collection of **personal Model Context Protocol (MCP) projects** built while exploring the MCP ecosystem. This repository serves as a playground for experimenting with MCP servers, tool development, database integrations, AI workflows, and real-world automation.

---

## About

This repository contains multiple standalone MCP projects developed for learning, experimentation, and building practical AI applications.

The primary objective is to explore the **Model Context Protocol (MCP)** by creating servers that expose useful tools which can be consumed by MCP-compatible clients such as Claude Desktop or custom AI agents.

Projects range from simple examples to more feature-rich applications involving databases, local automation, and external APIs.

---

## Repository Structure

```text
Personal_mcp/
│
├── Expense_Traker_MCP_Server/
├── MCP_Chatbot_Client/
├── Simple_Calculator_with_Dice_Roll_Local_MCP_Server/
├── Simple_Calculator_with_Dice_Roll_Remote_MCP_Server/
├── gitsteward-docs/
├── system_monitor_mcp_server/
│
├── .gitignore
├── Notes.md
└── README.md
```

Each project is self-contained and includes its own dependencies, tool implementations, and documentation.

---

## Projects

### 🧮 Simple Calculator with Dice Roll — Local
A local MCP server exposing basic calculator operations and a dice-roll tool. The starting point for understanding how MCP servers and tools work over stdio transport.

### 🌐 Simple Calculator with Dice Roll — Remote
The HTTP counterpart to the local calculator server. Demonstrates how to expose MCP tools over the network using streamable-http transport.

### 💸 Expense Tracker MCP Server
An MCP server for tracking personal expenses, backed by a SQLite database. Exposes tools for adding, querying, and summarising expense records through an AI-friendly interface.

### 🤖 MCP Chatbot Client
A custom MCP client implementation. Demonstrates how to connect to MCP servers programmatically and consume tools from a Python-based AI agent or chatbot.

### 📚 GitSteward Docs
A documentation-focused MCP project related to GitSteward.

### 🖥️ System Monitor MCP Server
A production-ready MCP server deployed on Render for real-time system monitoring. Built with FastMCP and psutil.

**Live at:** `https://system-monitor-mcp-server.onrender.com/mcp`

**Tools:**
- `ping` — health check
- `get_cpu_usage` — CPU percent, per-core breakdown, frequency
- `get_ram_usage` — RAM and swap in GB with usage percent
- `get_disk_usage` — all disk partitions with free/used space
- `get_running_processes` — top processes sorted by RAM or CPU
- `find_process` — search for a running process by name
- `read_log_file` — read and filter a log file by severity level
- `analyze_log_file` — error/warning summary with top repeated errors
- `list_log_files` — discover log files in any directory
- `detect_anomalies` — full health check with a 0–100 score

**Connect to Claude:** Go to Claude.ai → Settings → Integrations and add the URL above.

---

## Requirements

- Python 3.10 or later
- `pip` or `uv`

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Shivansh0047/Personal_mcp.git
cd Personal_mcp
```

Navigate into any project and install its dependencies:

```bash
cd system_monitor_mcp_server
pip install -e .
```

Projects using `uv`:

```bash
uv sync
```

---

## Running a Project

Each project has its own entry point. For example:

```bash
# System Monitor (local stdio mode)
cd system_monitor_mcp_server
python src/system_monitor/server.py
```

```bash
# Calculator or Expense Tracker
cd Simple_Calculator_with_Dice_Roll_Local_MCP_Server
uv run server.py
```

---

## Technologies Used

- Python
- Model Context Protocol (MCP)
- FastMCP
- psutil
- SQLite
- uv
- Render (deployment)

---

## Contributing

This repository is primarily for personal experimentation, but suggestions and improvements are always welcome. Feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License.

---

## Author

**Shivansh Pandey**

GitHub: [https://github.com/Shivansh0047](https://github.com/Shivansh0047)