import logging

from fastapi import FastAPI
from pydantic import BaseModel, Field

from run_research import run_research
from security.input_guard import check_input_safety


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ResearchForge API",
    description="Multi-Agent AI Research and Security Testing System",
    version="1.0.0"
)


class ResearchRequest(BaseModel):
    query: str = Field(
        min_length=5,
        max_length=2000,
        description="Research topic"
    )


@app.get("/health")
def health_check():

    return {
        "status": "online",
        "application": "ResearchForge"
    }


@app.post("/research")
def research_endpoint(request: ResearchRequest):

    query = request.query

    # Input security check
    safety_result = check_input_safety(query)

    if not safety_result["safe"]:

        return {
            "status": "blocked",
            "decision": "REJECTED",
            "reason": safety_result["reason"],
            "report": (
                "ResearchForge refused this request because "
                "it violates the input safety policy."
            ),
            "sources": 0
        }

    try:

        logger.info("Research request received.")

        result = run_research(query)

        return {
            "query" : query,
            "status": result.get("status", "unknown"),
            "decision": result.get("decision", "unknown"),
            "report": result.get("report", ""),
            "sources": len(result.get("sources", [])),
            "iteration": result.get("iteration", 1),
            "max_iterations": result.get("max_iterations", 3),
            "validation_passed": result.get("validation_passed", False),
            "validation_issues": result.get("validation_issues", [])
        }


    except Exception:

        logger.exception("Research workflow failed.")

        return {
            "status": "error",
            "decision": "ERROR",
            "report": "The research workflow could not complete.",
            "sources": 0
        }
