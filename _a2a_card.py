
import uuid
from typing import List, Dict, Any

from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill
)

def create_agent_card_from_config(config_data: Dict[str, Any], agent_url: str) -> AgentCard:
    """
    Creates an AgentCard instance from a parsed YAML configuration dictionary.
    
    Args:
        config_data: The dictionary containing the agent's configuration.
        agent_url: The base URL where the agent is hosted.

    Returns:
        A fully constructed AgentCard object.
    """
    agent_skills: List[AgentSkill] = []

    tools_from_yaml = config_data.get('agent', {}).get('tools', [])
    
    for tool_data in tools_from_yaml:
        # Filter the dictionary to only include fields that match AgentSkill
        skill_data = {k: v for k, v in tool_data.items() if k in AgentSkill.model_fields}
        agent_skills.append(AgentSkill(**skill_data))

    agent_card_data = config_data.get("agent", {})
    agent_capabilities = AgentCapabilities(web=config_data.get("capabilities", {}).get("web", False))
    
    agent_card = AgentCard(
        id=agent_card_data.get("id", str(uuid.uuid4())),
        name=agent_card_data.get("name"),
        description=agent_card_data.get("description"),
        version=agent_card_data.get("version"),
        url=agent_url,
        capabilities=agent_capabilities,
        defaultInputModes=config_data.get("default_input_modes", ["text"]),
        defaultOutputModes=config_data.get("default_output_modes", ["text"]),
        skills=agent_skills,
        endpoints={"mcp": "/mcp", "message_send": "/message/send", "message_stream": "/message/stream"}
    )
    
    return agent_card