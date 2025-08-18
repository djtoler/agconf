import asyncio
import json
import uuid
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse
from fastmcp.tools.tool import ToolResult
from a2a.server.tasks.task_manager import TaskManager, TaskStore
from a2a.types import (
    TaskStatus,
    TaskState,
    Task
)

from _a2a_components import create_message, create_artifact, create_task
from _mcp_tools import mcp_agent


class InMemoryTaskStore(TaskStore):
    def __init__(self):
        self._tasks = {}

    async def get(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    async def save(self, task: Task) -> None:
        self._tasks[task.id] = task

    async def delete(self, task_id: str) -> None:
        self._tasks.pop(task_id, None)

task_store = InMemoryTaskStore()

async def handle_a2a_task(request: Request) -> JSONResponse:
    """Handles an incoming A2A task and orchestrates MCP tool calls using the A2A SDK."""
    try:
        request_json = await request.json()
        print(f"Received A2A task: {request_json}")
        
        # Use the factory function to create the initial task object.
        task = create_task(request_json)
        
        # Correctly initialize the TaskManager with only the required arguments.
        task_manager = TaskManager(
            task_id=task.id,
            context_id=task.context_id,
            task_store=task_store,
            initial_message=None # Remove the initial message from the constructor call
        )
        
        # The rest of the logic should now work correctly.
        await task_manager.save_task_event(task)
        
        print(f"Orchestrating a tool call for task {task.id}...")
        
        tool = await mcp_agent._tool_manager.get_tool("add")
        if not tool:
            raise ValueError("Tool 'add' not found on the agent.")
            
        tool_result: ToolResult = await tool.run(arguments=request_json["params"])

        # Use the factory function to create the artifact from the tool's result.
        artifact = create_artifact(tool_result)

        # Create the final agent message using the `create_message` factory function.
        agent_completion_message = create_message(
            role='agent',
            description="Tool call completed successfully."
        )

        # Update the task status with the new, factory-created message.
        task.status = TaskStatus(state=TaskState.completed, message=agent_completion_message)
        
        if task.artifacts is None:
            task.artifacts = []
        task.artifacts.append(artifact)
        
        await task_manager.save_task_event(task)

        # The final JSON response is now based on the standardized Task object.
        return JSONResponse(task.model_dump())
        
    except Exception as e:
        print(f"Error handling A2A task: {e}")
        return JSONResponse({"status": "failed", "error": str(e)}, status_code=500)

async def handle_a2a_stream_task(request: Request) -> StreamingResponse:
    async def event_generator():
        yield json.dumps({"status": "started", "message": "Streaming session initiated."}) + '\n'
        for i in range(3):
            yield json.dumps({"status": "in_progress", "step": i + 1, "message": f"Processing step {i + 1}..."}) + '\n'
            await asyncio.sleep(1)
        final_result = {"status": "completed", "result": "Task finished successfully."}
        yield json.dumps(final_result) + '\n'
    return StreamingResponse(event_generator(), media_type="application/json")