# FastMCP Integration

This project demonstrates how to build and expose tools, resources, and prompts using the FastMCP framework. The integration provides a demo MCP server with several example functionalities.

## Features

- **Tools**
  - `add(a: int, b: int)`: Adds two numbers.
  - `convert_currency(amount: float, from_currency: str, to_currency: str)`: Converts currency amounts using fixed demo rates.

- **Resources**
  - `system_info`: Returns basic system information (OS, version, Python version).
  - `sample_data(name: int)`: Returns static reference data (countries and currencies).

- **Prompts**
  - `code_reviewer(code: str, focus: str)`: Reviews Python code for improvements, bugs, and best practices. Supports focus areas: general, performance, security.
  - `sql_generator(request: str, table: str)`: Generates SQL queries from natural language requests.

## Usage

1. **Install dependencies**  
   ```
    pip install -r requirements.txt
   ```

2. **Run the server**  
   Execute the following command in the `Fastmcp-Integration` directory:
   ```
   python servers.py
   ```

3. **Access tools and resources**  
   The MCP server will expose the defined tools, resources, and prompts for integration with compatible clients.

## File Structure

- `servers.py`: Main MCP server implementation.
- `requirements.txt`: List of required Python packages.

