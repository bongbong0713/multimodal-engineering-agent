from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from src.agent.router import classify_node, route_by_file_type
from src.agent.state import AgentState
from src.tools.cad import run_cad_tool
from src.tools.document import run_document_tool
from src.tools.point_cloud import run_point_cloud_tool


def point_cloud_node(state: AgentState):
    try:
        result = run_point_cloud_tool(state["file_path"], state.get("task_type") or "summary")
        return {"result": result, "error": None}
    except Exception as exc:
        return {"result": None, "error": str(exc)}


def cad_node(state: AgentState):
    try:
        result = run_cad_tool(state["file_path"], state.get("task_type") or "summary")
        return {"result": result, "error": None}
    except Exception as exc:
        return {"result": None, "error": str(exc)}


def document_node(state: AgentState):
    try:
        result = run_document_tool(state["file_path"], state.get("task_type") or "text_extraction")
        return {"result": result, "error": None}
    except Exception as exc:
        return {"result": None, "error": str(exc)}


def not_implemented_node(state: AgentState):
    return {
        "result": {
            "message": f"{state.get('file_type')} domain is planned but not implemented yet.",
            "recommended_next_steps": [
                "Add a parser module for this file type.",
                "Add domain-specific tools.",
                "Connect the new node in src/agent/graph.py.",
            ],
        },
        "error": None,
    }


def unsupported_node(state: AgentState):
    return {
        "result": None,
        "error": f"Unsupported file type for path: {state['file_path']}",
    }


def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("classify", classify_node)
    graph.add_node("point_cloud", point_cloud_node)
    graph.add_node("cad", cad_node)
    graph.add_node("document", document_node)
    graph.add_node("not_implemented", not_implemented_node)
    graph.add_node("unsupported", unsupported_node)

    graph.add_edge(START, "classify")
    graph.add_conditional_edges(
        "classify",
        route_by_file_type,
        {
            "point_cloud": "point_cloud",
            "cad": "cad",
            "document": "document",
            "not_implemented": "not_implemented",
            "unsupported": "unsupported",
        },
    )

    graph.add_edge("point_cloud", END)
    graph.add_edge("cad", END)
    graph.add_edge("document", END)
    graph.add_edge("not_implemented", END)
    graph.add_edge("unsupported", END)

    return graph.compile()
