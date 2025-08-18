
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse, StreamingResponse

from a2a.types import AgentCard

from _mcp_tools import mcp_agent
from _a2a_task import handle_a2a_task, handle_a2a_stream_task

def create_agent_endpoints(agent_card: AgentCard) -> FastAPI:
    """
    Creates and configures a FastAPI application with all agent endpoints.
    
    Args:
        agent_card: The pre-constructed AgentCard object to expose.
        
    Returns:
        The configured FastAPI application instance.
    """
    app = FastAPI(title="SAOP Agent")
    app.mount("/mcp", mcp_agent.http_app())

    @app.get("/.well-known/agent-card.json", response_model=AgentCard)
    async def get_agent_card() -> AgentCard:
        return agent_card
    
    @app.post("/message/send")
    async def message_send(request: Request) -> JSONResponse:
        return await handle_a2a_task(request)

    @app.post("/message/stream")
    async def message_stream(request: Request) -> StreamingResponse:
        return await handle_a2a_stream_task(request)

    return app
















