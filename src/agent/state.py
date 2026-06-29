from typing import Any, Optional, TypedDict


class AgentState(TypedDict):
    """Shared state passed through the engineering agent graph."""

    query: str
    file_path: str
    file_type: Optional[str]
    task_type: Optional[str]
    result: Optional[Any]
    error: Optional[str]
