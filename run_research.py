
from security.input_guard import check_input_safety
from graph.workflow import research_graph


def run_research(query: str):

    initial_state = {
        "query": query,
        "research_plan": [],
        "sources": [],
        "report": "",
        "decision": "",
        "feedback": "",
        "iteration": 1,
        "max_iterations": 3,
        "validation_passed": False,
        "validation_issues": [],
        "status": "pending",
        "errors": []
    }

    result = research_graph.invoke(initial_state)

    return result


if __name__ == "__main__":

    query = input("\nEnter your research topic: ")

    safety_result = check_input_safety(query)

    if not safety_result["safe"]:

        print("\n" + "=" * 70)
        print("RESEARCHFORGE SAFETY CHECK")
        print("=" * 70)

        print("Status: BLOCKED")
        print("Reason:", safety_result["reason"])

        print("\nTry a safe alternative:")
        print(
            "Research the history of explosives, their societal "
            "impact, safety regulations, and emergency response."
        )

    else:

        try:

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

            print(
                "Iterations:",
                result.get("iteration", 1),
                "/",
                result.get("max_iterations", 3)
            )

            print(
                "Validation:",
                "PASSED" if result.get("validation_passed") else "FAILED"
            )

            if result.get("validation_issues"):
                print("Validation Issues:")
                for issue in result["validation_issues"]:
                    print("-", issue)

        except Exception as error:

            print("\n[RESEARCHFORGE ERROR]")
            print("The research workflow could not complete.")
            print("Details:", error)
