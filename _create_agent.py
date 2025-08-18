
import os
import uvicorn
import argparse
import asyncio
import uuid

from fastapi import FastAPI
from dotenv import load_dotenv

# Import modular functions and types
from _mcp_init import initialize_mcp_client
from _mcp_tools import mcp_agent
from _a2a_card import create_agent_card_from_config
from _agent_endpoints import create_agent_endpoints

# Load environment variables from the .env file.
load_dotenv()


def create_agent(config_path: str) -> FastAPI:
    """Creates a FastMCP agent and an A2A-compliant server from a YAML config."""
    # Step 1: Initialize the MCP client and get the config data
    config_data = initialize_mcp_client(config_path)

    # Step 2: Create the AgentCard from the config data
    agent_card_url = config_data.get("url", "")
    agent_card = create_agent_card_from_config(config_data, agent_card_url)
    
    # Step 3: Create the FastAPI application with all its endpoints
    app = create_agent_endpoints(agent_card)

    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a SAOP agent from a YAML config.")
    parser.add_argument("config_file", type=str, help="Path to the agent configuration YAML file.")
    args = parser.parse_args()
    agent_app = create_agent(args.config_file)
    uvicorn.run(agent_app, host="127.0.0.1", port=8000) 
