from agents.llm_config import get_agent_llm
from graph.state import ResearchState


llm = get_agent_llm("PLANNER")

def planner_agent(state: ResearchState):

    query = state["query"]
    previous_feedback = state.get("feedback", "")


    prompt = f"""
    You are an expert research planning agent.

    Your task is to break the user's research topic
    into focused and meaningful research questions.

    
    Original research query:
    {state['query']}
    
    Previous orchestrator review:
    {previous_feedback if previous_feedback else "No previous review."}
    
    Create a research plan that addresses the original query
    and improves upon the previous review if previous review is there.

    Generate exactly 4 research questions.

    Requirements:
    1. Cover different aspects of the topic.
    2. Avoid repetitive questions.
    3. Include technical details where relevant.
    4. Make questions suitable for web research.

    Return ONLY the questions as a numbered list.
    """

    response = llm.invoke(prompt)

    questions = [
        line.strip()
        for line in response.content.splitlines()
        if line.strip()
    ]

    research_plan = [
        question.lstrip("0123456789.-) ").strip()
        for question in questions
    ]

    research_plan = [
        question for question in research_plan if question
    ][:4]

    if len(research_plan) < 2:
        raise ValueError(
            "Planner failed to generate enough research questions."
        )

    print("\n[PLANNER] Research plan generated.")

    return {
        "research_plan": research_plan
    }
