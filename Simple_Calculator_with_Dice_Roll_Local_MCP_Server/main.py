import random
from fastmcp import FastMCP

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

if __name__ == "__main__":
    mcp.run()