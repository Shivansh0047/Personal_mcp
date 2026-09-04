from fastmcp import FastMCP
from system_monitor.tools import register_all
import os


mcp = FastMCP(
    name = "System Monitor",
    instructions = "A system monitoring server. Use these tools to check CPU, RAM, disk usage, running processes, and logs."
)

register_all(mcp)

@mcp.tool()
def ping() -> str:
    """Check if the system is alive"""
    return "System Monitor MCP is online"


def main():
    # Locally: stdio. On Render: streamable-http so LLMs can reach it over the internet
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    port      = int(os.environ.get("PORT", 8000))

    if transport == "http":
        mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()