
from langgraph.graph import StateGraph, START, END

from graph.state import ResearchState

# Agents
from agents.planner import planner_agent
from agents.search import search_agent
from agents.writer import writer_agent
from agents.evaluator import evaluator_agent
from agents.orchestrator import orchestrator_agent

# Security
from security.report_validator import validator_agent


# --------------------------------------------------
# 1. Initialize research
# --------------------------------------------------

def initialize_research(state: ResearchState):

    return {
        "iteration": 1,
        "max_iterations": 3,

        # Orchestrator
        "decision": "",
        "feedback": "",
        "decision_reason": "",

        # Research data
        "report": "",
        "research_plan": [],
        "sources": [],

        # Writer progress
        "generated_sections": {},
        "completed_sections": [],
        "failed_sections": [],
        "stage_attempts": {},
        "writer_iteration": 0,

        # Evaluator
        "evaluation": None,

        # Validator
        "validation_passed": False,
        "validation_issues": [],

        # Execution
        "errors": [],
        "status": "running"
    }


# --------------------------------------------------
# 2. Route after Planner
# --------------------------------------------------

def route_after_planning(state: ResearchState):

    research_plan = state.get("research_plan", [])

    if len(research_plan) >= 2:
        return "search"

    return "end"


# --------------------------------------------------
# 3. Route after Search
# --------------------------------------------------

def route_after_search(state: ResearchState):

    if state.get("sources"):
        return "writer"

    return "end"


# --------------------------------------------------
# 4. Route after Writer
# --------------------------------------------------

def route_after_writer(state: ResearchState):

    failed_sections = state.get("failed_sections", [])
    stage_attempts = state.get("stage_attempts", {})

    if failed_sections:

        failed_stage = failed_sections[0]

        if stage_attempts.get(failed_stage, 0) < 3:
            print(
                f"[WORKFLOW] Retrying Writer stage: {failed_stage}"
            )
            return "retry"

        print(
            f"[WORKFLOW] Maximum retries reached: {failed_stage}"
        )

    return "checks"


# --------------------------------------------------
# 5. Start parallel quality checks
# --------------------------------------------------

def start_checks(state: ResearchState):

    print(
        "\n[WORKFLOW] Starting quality checks..."
    )

    return {}


# --------------------------------------------------
# 6. Route after Orchestrator
# --------------------------------------------------

def route_after_orchestration(state: ResearchState):

    decision = state.get("decision", "REVISE")

    iteration = state.get("iteration", 1)
    max_iterations = state.get("max_iterations", 3)

    # Successful approval
    if (
        decision == "APPROVE"
        and state.get("validation_passed", False)
    ):

        return "end"

    # Restart from Planner if iterations remain
    if iteration < max_iterations:

        return "iteration_counter"

    # Maximum iterations reached
    return "end"


# --------------------------------------------------
# 7. Increment research iteration
# --------------------------------------------------

def increment_iteration(state: ResearchState):

    print(
        f"\n[WORKFLOW] Starting research cycle "
        f"{state.get('iteration', 1) + 1}"
    )

    return {
        "iteration": state.get("iteration", 1) + 1
    }


# --------------------------------------------------
# 8. Finalize research
# --------------------------------------------------

def finalize_research(state: ResearchState):

    status = (
        "completed"
        if (
            state.get("decision") == "APPROVE"
            and state.get("validation_passed", False)
        )
        else "completed_with_warnings"
    )

    print(
        f"\n[WORKFLOW] Research status: {status}"
    )

    return {
        "status": status
    }


# --------------------------------------------------
# 9. Build LangGraph
# --------------------------------------------------

builder = StateGraph(ResearchState)


# Register nodes
builder.add_node("initialize", initialize_research)

builder.add_node("planner", planner_agent)
builder.add_node("search", search_agent)
builder.add_node("writer", writer_agent)

builder.add_node("checks", start_checks)

builder.add_node("evaluator", evaluator_agent)
builder.add_node("validator", validator_agent)

builder.add_node("orchestrator", orchestrator_agent)

builder.add_node("iteration_counter", increment_iteration)
builder.add_node("finalize", finalize_research)


# --------------------------------------------------
# 10. Define graph connections
# --------------------------------------------------

# START -> Initialize -> Planner

builder.add_edge(START, "initialize")

builder.add_edge("initialize", "planner")


# Planner -> Search OR Finalize

builder.add_conditional_edges(
    "planner",
    route_after_planning,
    {
        "search": "search",
        "end": "finalize"
    }
)


# Search -> Writer OR Finalize

builder.add_conditional_edges(
    "search",
    route_after_search,
    {
        "writer": "writer",
        "end": "finalize"
    }
)


# Writer -> Retry OR Checks

builder.add_conditional_edges(
    "writer",
    route_after_writer,
    {
        "retry": "writer",
        "checks": "checks"
    }
)


# Checks -> Evaluator AND Validator

builder.add_edge("checks", "evaluator")

builder.add_edge("checks", "validator")


# Wait for both agents before Orchestrator

builder.add_edge(
    ["evaluator", "validator"],
    "orchestrator"
)


# Orchestrator -> Iteration Counter OR Finalize

builder.add_conditional_edges(
    "orchestrator",
    route_after_orchestration,
    {
        "iteration_counter": "iteration_counter",
        "end": "finalize"
    }
)


# Iteration Counter -> Planner

builder.add_edge(
    "iteration_counter",
    "planner"
)


# Finalize -> END

builder.add_edge("finalize", END)


# --------------------------------------------------
# 11. Compile graph
# --------------------------------------------------

research_graph = builder.compile()

print("[WORKFLOW] ResearchForge graph compiled successfully.")
