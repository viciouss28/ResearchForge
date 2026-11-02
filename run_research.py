
from graph.workflow import research_graph


def run_research(query: str):

    initial_state = {
        "query": query,
        "research_plan": [],
        "sources": [],
        "report": "",
        "decision": "",
        "feedback": "",
        "research_attempts": 0,
        "revision_count": 0,
        "status": "pending",
        "errors": []
    }

    result = research_graph.invoke(initial_state)

    return result


if __name__ == "__main__":

    query = input("\nEnter your research topic: ").strip()

    if not query:
        print("Research query cannot be empty.")
        raise SystemExit(1)

    result = run_research(query)

    print("\n" + "=" * 70)
    print("FINAL RESEARCH REPORT")
    print("=" * 70)

    print(result.get("report", "No report generated."))

    print("\n" + "=" * 70)
    print("RESEARCH SUMMARY")
    print("=" * 70)

    print("Status:", result.get("status"))
    print("Decision:", result.get("decision"))
    print("Sources:", len(result.get("sources", [])))
    print(f"Iterations: {result.get('iteration', 1)}")
    print("Revisions:", result.get("max_iterations"))
