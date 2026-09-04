---
source_anchor: "README.md#technologies-used"
source_commit: "b0a19e0cc647bd638c9848b681df48d741980fbe"
status: "updated"
---

**Why flagged:** system_monitor_mcp_server/pyproject.toml: The new runtime dependency python-dotenv is not listed among the technologies. / system_monitor_mcp_server/src/system_monitor/server.py: The added `dotenv` import should be reflected in the technologies list, which currently omits it.

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
