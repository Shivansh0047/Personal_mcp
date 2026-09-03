from fastmcp import FastMCP

mcp = FastMCP(
    name = "System Monitor",
    instructions="A system monitoring server. Use these tools to check CPU, RAM, disk usage, running processes, and logs."
)

@mcp.tool()
def ping() -> str:
    """Check if the system is alive"""
    return "System Monitor MCP is online"

def main():
    mcp.run()


if __name__ == "__main__":
    main()