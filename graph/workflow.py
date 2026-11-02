
from langgraph.graph import StateGraph, START, END

from graph.state import ResearchState

from agents.planner import planner_agent
from agents.search import search_agent
from agents.writer import writer_agent
from agents.orchestrator import orchestrator_agent


# 1. Initialize research
def initialize_research(state: ResearchState):

    return {
        "iteration": 1,
        "max_iterations": 3,
        "decision": "",
        "feedback": "",
        "report": "",
        "research_plan": [],
        "sources": [],
        "errors": [],
        "status": "running"
    }


# 2. Check whether planning was successful
def route_after_planning(state: ResearchState):

    if len(state.get("research_plan", [])) >= 2:
        return "search"

    return "end"


# 3. Check whether sources were collected
def route_after_search(state: ResearchState):

    if state.get("sources"):
        return "writer"

    return "end"


# 4. Decide whether to approve or restart research
def route_after_orchestration(state: ResearchState):

    decision = state.get("decision", "REVISE")

    iteration = state.get("iteration", 1)
    max_iterations = state.get("max_iterations", 3)

    if decision == "APPROVE":
        return "end"

    if decision == "RESEARCH" and iteration < max_iterations:
        return "search"

    if decision == "REVISE" and iteration < max_iterations:
        return "planner"

    return "end"


# 5. Increment research iteration
def increment_iteration(state: ResearchState):

    return {
        "iteration": state.get("iteration", 1) + 1
    }


# 6. Finalize research
def finalize_research(state: ResearchState):

    status = (
        "completed"
        if state.get("decision") == "APPROVE"
        else "completed_with_warnings"
    )

    return {"status": status}


# 7. Build LangGraph workflow
builder = StateGraph(ResearchState)

builder.add_node("initialize", initialize_research)
builder.add_node("planner", planner_agent)
builder.add_node("search", search_agent)
builder.add_node("writer", writer_agent)
builder.add_node("orchestrator", orchestrator_agent)
builder.add_node("iteration_counter", increment_iteration)
builder.add_node("finalize", finalize_research)


# 8. Define workflow edges
builder.add_edge(START, "initialize")

builder.add_edge("initialize", "planner")

builder.add_conditional_edges(
    "planner",
    route_after_planning,
    {
        "search": "search",
        "end": "finalize"
    }
)

builder.add_conditional_edges(
    "search",
    route_after_search,
    {
        "writer": "writer",
        "end": "finalize"
    }
)

builder.add_edge("writer", "orchestrator")

builder.add_conditional_edges(
    "orchestrator",
    route_after_orchestration,
    {
        "planner": "iteration_counter",
        "end": "finalize"
    }
)

builder.add_edge("iteration_counter", "planner")

builder.add_edge("finalize", END)


# 9. Compile graph
research_graph = builder.compile()
