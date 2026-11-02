from graph.state import ResearchState
from tools.web_search import search_web


def search_agent(state: ResearchState):

    print("\n[SEARCH] Collecting web sources...")

    sources = []
    seen_urls = set()

    for question in state["research_plan"]:

        results = search_web(question)

        for result in results:

            url = result.get("url")

            if not url or url in seen_urls:
                continue

            seen_urls.add(url)

            sources.append({
                "title": result.get("title", ""),
                "url": url,
                "content": result.get("content", ""),
                "query": question
            })

    print(f"[SEARCH] Collected {len(sources)} sources.")

    return {
        "sources": sources
    }
