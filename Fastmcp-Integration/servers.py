from fastmcp import FastMCP

mcp = FastMCP("Demo MCP Server")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert an amount from one currency to another (using fixed demo rates)."""
    rates = {"USD": 1.0, "INR": 83.0, "EUR": 0.92, "JPY": 145.0}  # demo rates
    if from_currency not in rates or to_currency not in rates:
        raise ValueError("Unsupported currency")
    usd_value = amount / rates[from_currency]
    return round(usd_value * rates[to_currency], 2)

@mcp.resource("demo://system_info")
def system_info() -> dict:
    """Return system information as resource."""
    import platform
    return {
        "os": platform.system(),
        "version": platform.version(),
        "python_version": platform.python_version(),
    }

@mcp.resource("demo://data/{name}")
def sample_data(name: int) -> dict:
    """Return some static resource (like config or reference data)."""
    return {
        "countries": ["India", "USA", "Germany", "Japan"],
        "currencies": {"India": "INR", "USA": "USD", "Germany": "EUR", "Japan": "JPY"}
    }

@mcp.prompt()
def code_reviewer(code: str, focus: str = "general") -> str:
    """
    Review a piece of Python code for improvements, bugs, and best practices.
    
    Args:
        code: The Python code to review.
        focus: The type of review ("general", "performance", "security").
    """
    instructions = {
        "general": "Review the code for readability, maintainability, and Pythonic style.",
        "performance": "Identify any performance bottlenecks and suggest optimizations.",
        "security": "Check for security issues and unsafe patterns.",
    }
    return f"You are a strict Python code reviewer. {instructions.get(focus, instructions['general'])}\n\nCode:\n{code}"

@mcp.prompt()
def sql_generator(request: str, table: str = "employee_information") -> str:
    """
    Generate a SQL query based on natural language request.
    
    Args:
        request: The natural language query (e.g., "top 10 employees by salary").
        table: The default table to query against.
    """
    return (
        f"You are a SQL query assistant. Generate a valid SQL query only.\n\n"
        f"Table: {table}\n"
        f"User request: {request}\n"
    )

if __name__ == "__main__":
    mcp.run()
