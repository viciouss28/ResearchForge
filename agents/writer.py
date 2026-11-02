from agents.llm_config import get_agent_llm
from graph.state import ResearchState


llm = get_agent_llm("WRITER")


def writer_agent(state: ResearchState):

    print("\n[WRITER] Generating research report...")

    sources_text = ""

    for index, source in enumerate(state.get("sources", []), start=1):

        sources_text += f"""
        SOURCE [{index}]
        Title: {source['title']}
        URL: {source['url']}
        Content: {source['content']}

"""

    feedback = state.get("feedback", "")

    prompt = f"""
You are an expert academic research writer.

RESEARCH QUESTION:
{state['query']}

RESEARCH PLAN:
{state['research_plan']}

COLLECTED SOURCES:
{sources_text}

ORCHESTRATOR FEEDBACK:
{feedback if feedback else "No previous feedback."}

Write a detailed research report with the following sections:

1. Executive Summary
2. Introduction
3. Research Findings
4. Technical Analysis
5. Security Implications
6. Limitations
7. Conclusion
8. References

STRICT RULES:
- Use only the supplied source material for factual claims.
- Cite sources using [1], [2], etc.
- Citation numbers must match the SOURCE IDs.
- Never invent references, statistics or URLs.
- Identify unsupported claims.
- Mention contradictions where sources disagree.
- Clearly state when evidence is insufficient.

Return the report in Markdown.
"""

    response = llm.invoke(prompt)

    print("[WRITER] Report generated.")

    return {
        "report": response.content
    }
