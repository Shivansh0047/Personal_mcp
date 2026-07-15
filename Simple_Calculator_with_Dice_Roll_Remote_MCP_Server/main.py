import random
from fastmcp import FastMCP
import json

# Create a FastMCP server instance
mcp = FastMCP(name="Calculator_with_Dice_Roll")

@mcp.tool
def roll_dice(n_dice: int = 1) -> list[int]:
    """Roll n_dice 6-sided dice and return the result."""
    return [random.randint(1, 6) for _ in range(n_dice)]

@mcp.tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@mcp.tool
def subtract_numbers(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b

@mcp.tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@mcp.tool
def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b

# A resource for giving server information
@mcp.resource("infp://server")
def server_info() -> str:
    """Get information about this server"""
    info = {
        "name": "Simple Calculator with dice Roll Server",
        "version": "1.0.0",
        "description": "A basic MCP server with math tools and random number generator",
        "tools":["roll_dice","add_numbers","subtract_numbers","multiply_numbers","divide_numbers"],
        "author":"Shivansh Pandey"
    }
    return json.dumps(info, indent=2)

if __name__ == "__main__":
    # mcp.run() --> this means we are setting our transport is STDIO
    mcp.run(transport="http", host="0.0.0.0",port=8001) # We defind our transport as http , allows all hosts and set port to 8001