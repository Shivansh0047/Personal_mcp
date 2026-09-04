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
- FastMCP-based servers
- SQLite database integration
- AI-friendly tool interfaces
- Modular and extensible project structure
- Easy to add new MCP servers and tools  
---

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

Enter the directory that contains the server code:  
```bash
cd Personal_mcp/system_monitor_mcp_server
```  

(Optional) Create and activate a virtual environment so the installation does not affect your global Python installation:  
```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
```  

Install the package in editable mode, which also pulls in the new **python‑dotenv** dependency declared in `pyproject.toml`:  
```bash
pip install -e .
```  

If you need to provide configuration values (e.g., custom FastMCP host or port), create a `.env` file in the project root and add the required variables, for example:  
```dotenv
FASTMCP_HOST=0.0.0.0
FASTMCP_PORT=8000
```  
The server automatically loads this file at startup via `python‑dotenv`. If no `.env` file is present, default settings are used.

Run the server locally:  
```bash
python src/system_monitor/server.py
```  

These steps install all current dependencies, optionally allow you to override configuration through a `.env` file, and start the FastMCP‑based system‑monitoring server that provides CPU, RAM, disk, process, and log monitoring APIs.

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

- Python (3.10+)  
- Model Context Protocol (MCP)  
- FastMCP  
- psutil (cross‑platform system and process utilities)  
- python‑dotenv (loads environment variables from `.env` files)  
- datetime (standard library for timestamps)  
- pathlib (filesystem path handling)  
- re (regular‑expression utilities)  
- os (operating‑system interfaces)  
- collections (e.g., Counter for log analysis)  
- SQLite (via the built‑in sqlite3 module)  
- JSON (standard library serialization)  
- uv (asynchronous server runtime)  
- asyncio (standard library for asynchronous programming)

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
