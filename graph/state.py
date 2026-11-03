
from typing import TypedDict

from agents.evaluation_schema import EvaluationClass


class ResearchState(TypedDict, total=False):

    # User input
    query: str

    # Planner Agent
    research_plan: list[str]

    # Search Agent
    sources: list[dict]

    # Writer Agent
    report: str

    generated_sections: dict[str, str]
    completed_sections: list[str]
    failed_sections: list[str]
    stage_attempts: dict[str, int]
    writer_iteration: int

    # Research Evaluator Agent
    evaluation: EvaluationClass

    # Python Report Validator
    validation_passed: bool
    validation_issues: list[str]

    # Orchestrator Agent
    decision: str
    feedback: str
    decision_reason: str

    # Workflow control
    iteration: int
    max_iterations: int

    # Execution status
    status: str
    errors: list[str]
