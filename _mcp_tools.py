# mcp_tools.py

from fastmcp.server.server import FastMCP
from fastmcp import Client

# Import the global client from the mcp_init module
from _mcp_init import remote_client

# Import the regular Python functions
from _funcs import (
    add_numbers,
    get_tools_from_client,
    call_tool_on_client,
    hello_world, # NEW: Import the new function
)


# Initialize the FastMCP agent
mcp_agent = FastMCP("SAOP Agent")

# Wrap the 'add_numbers' function as an MCP tool
@mcp_agent.tool()
def add(a: int, b: int) -> int:
    """Adds two numbers together."""
    return add_numbers(a, b)

# Wrap the 'get_tools_from_client' function as an MCP tool
@mcp_agent.tool()
async def list_all_remote_tools() -> list:
    """Lists all tools available across all connected remote servers."""
    return await get_tools_from_client(remote_client)

# Wrap the 'call_tool_on_client' function as an MCP tool
@mcp_agent.tool()
async def call_remote_tool(tool_name: str, params: dict) -> any:
    """Calls a specified tool on a remote server."""
    return await call_tool_on_client(remote_client, tool_name, params)

@mcp_agent.tool()
def hello_world_tool() -> str:
    """A tool that simply returns a 'Hello, World!' string."""
    return hello_world()