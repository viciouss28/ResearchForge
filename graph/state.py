from typing import TypedDict


class ResearchState(TypedDict, total=False):

    # User input
    query: str

    # Planner output
    research_plan: list[str]

    # Search output
    sources: list[dict]

    # Writer output
    report: str

    # Orchestrator control
    decision: str
    feedback: str

    # Retry management
    max_iterations: int
    iteration: int

    # Execution status
    status: str
    errors: list[str]
