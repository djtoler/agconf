
import asyncio
from typing import List, Dict, Any

def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

async def get_tools_from_client(remote_client) -> List:
    """Gets tools from a remote client."""
    if remote_client:
        async with remote_client:
            tools = await remote_client.list_tools()
            return tools
    return []

async def call_tool_on_client(remote_client, tool_name: str, params: dict) -> any:
    """Calls a tool on a remote client."""
    if remote_client:
        async with remote_client:
            result = await remote_client.call_tool(tool_name, params)
            return result
    return {"error": "Remote client not initialized."}

def hello_world() -> str:
    """Returns a simple greeting string."""
    return "Hello, World!"