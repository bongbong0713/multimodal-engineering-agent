from src.agent.state import AgentState
from src.parsers.file_type import detect_file_type


def classify_task_from_query(query: str) -> str:
    """Lightweight rule-based task classifier.

    This can later be replaced with an LLM classifier.
    """
    q = query.lower()

    if any(k in q for k in ["segment", "segmentation", "분리", "분할", "바닥", "벽"]):
        return "segmentation"
    if any(k in q for k in ["cluster", "clustering", "군집", "객체"]):
        return "clustering"
    if any(k in q for k in ["bbox", "bounding", "box", "크기", "치수"]):
        return "bounding_box"
    if any(k in q for k in ["measure", "distance", "length", "거리", "길이"]):
        return "measurement"
    if any(k in q for k in ["summary", "summarize", "요약", "설명"]):
        return "summary"
    if any(k in q for k in ["extract", "text", "ocr", "스펙", "문서", "추출"]):
        return "text_extraction"

    return "summary"


def classify_node(state: AgentState):
    file_type = state.get("file_type") or detect_file_type(state["file_path"])
    task_type = state.get("task_type") or classify_task_from_query(state["query"])
    return {"file_type": file_type, "task_type": task_type}


def route_by_file_type(state: AgentState) -> str:
    file_type = state.get("file_type")

    if file_type == "point_cloud":
        return "point_cloud"
    if file_type == "cad":
        return "cad"
    if file_type == "document":
        return "document"
    if file_type in {"drawing", "bim", "gis"}:
        return "not_implemented"
    return "unsupported"
