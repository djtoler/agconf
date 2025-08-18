
import uuid
from typing import Dict, Any, List, Optional

from fastmcp.tools.tool import ToolResult
from a2a.types import (
    Task, 
    Message, 
    TextPart, 
    DataPart, 
    Artifact, 
    A2ABaseModel,
    TaskStatus,
    TaskState,
)

def create_message(role: str, description: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> Message:
    """Creates a Message object from provided data."""
    message_parts: List[A2ABaseModel] = []
    if description:
        message_parts.append(TextPart(kind="text", text=description))
    
    return Message(
        message_id=str(uuid.uuid4()),
        role=role,
        parts=message_parts,
        metadata=params or {},
    )

def create_artifact(tool_result: ToolResult) -> Artifact:
    """Creates an Artifact object from a ToolResult."""
    artifact_parts: List[A2ABaseModel] = []
    result_to_serialize = tool_result.to_mcp_result()
    
    if isinstance(result_to_serialize, tuple):
        content_list, structured_content = result_to_serialize
        if content_list:
            # Assuming the first content block is text
            artifact_parts.append(TextPart(kind="text", text=content_list[0].text))
        if structured_content:
            artifact_parts.append(DataPart(kind="data", data=structured_content))
    else:
        content_list = result_to_serialize
        if content_list and content_list[0].text:
            artifact_parts.append(TextPart(kind="text", text=content_list[0].text))
            
    return Artifact(
        artifact_id=str(uuid.uuid4()),
        kind='tool_call_result',
        parts=artifact_parts,
    )

def create_task(request_json: Dict[str, Any]) -> Task:
    """Creates a Task object with an initial message from a JSON request."""
   
    task_id = request_json.get("id", str(uuid.uuid4()))
    context_id = request_json.get("context_id", str(uuid.uuid4()))
    
    initial_message = create_message(
        role='user',
        description=request_json.get("description", ""),
        params=request_json.get("params", {}),
    )
    

    initial_status = TaskStatus(state=TaskState.submitted)

    return Task(
        id=task_id,
        task_id=task_id,
        context_id=context_id,
        status=initial_status,
        initial_message=initial_message,
    )