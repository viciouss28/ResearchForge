import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_web(query: str):

    response = client.search(
        query=query,
        search_depth="basic",
        max_results=3
    )

    return response.get("results", [])
