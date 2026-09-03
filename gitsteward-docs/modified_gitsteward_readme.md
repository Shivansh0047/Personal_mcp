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

system_monitor_mcp_server/
│
├── src/
│   └── system_monitor/
│       ├── __init__.py
│       ├── server.py          # entry point for the MCP server (exposes `main`)
│       └── …                  # additional modules implementing monitoring logic
│
├── tests/
│   └── …                      # test suite for the package
│
├── pyproject.toml             # build configuration, dependencies and console script
├── uv.lock                    # lock file for reproducible installs
├── README.md                  # overview, usage instructions and contribution guide
└── .gitignore                 # standard ignore patterns
```text
Each project is now a self‑contained Python package following the conventional
`src/` layout. The `pyproject.toml` lives inside the top‑level
`system_monitor_mcp_server` directory and defines:

- Build system (hatchling)
- Project metadata (name, version, description, Python requirement)
- Runtime dependencies (`fastmcp`, `psutil`)
- Console script entry point `system-monitor` → `system_monitor.server:main`

All source code resides under `src/system_monitor`, while tests are placed in
`tests/`. The repository also includes a lock file (`uv.lock`) for deterministic
dependency resolution and a README with usage details.

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

Enter the directory that contains the project definition:  
```bash
cd Personal_mcp/system_monitor_mcp_server
```  

Install the project's dependencies (this will also create a virtual environment if one does not already exist):  
```bash
uv sync
```  

The `uv sync` command reads the `pyproject.toml` located in this folder, resolves the required packages, and installs them into the newly‑created environment. After the sync completes you can run the server directly via the installed console script:

```bash
system-monitor
```  

(If you prefer a classic `pip` workflow, you can also install the package in editable mode with `pip install -e .` after activating a virtual environment.)

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
