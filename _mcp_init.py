
import os
import yaml
from fastmcp import Client

# This variable will be set by the main server file
remote_client = None

def set_remote_client(client_instance: Client):
    """Sets the remote_client instance for the tools to use."""
    global remote_client
    remote_client = client_instance

def initialize_mcp_client(config_path: str) -> dict:
    """
        parse yaml config.
    """
    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f)

    mcp_servers_config = config_data.get("mcp_servers", {})
    for server_name, server_config in mcp_servers_config.items():
        if "auth" in server_config and isinstance(server_config["auth"], str):
            if server_config["auth"].startswith("${") and server_config["auth"].endswith("}"):
                env_var_name = server_config["auth"][2:-1]
                api_key = os.getenv(env_var_name)
                if api_key:
                    server_config["auth"] = api_key
                else:
                    print(f"Warning: API key for {server_name} not found in environment.")

    client = Client(mcp_servers_config)
    set_remote_client(client)
    
    return config_data