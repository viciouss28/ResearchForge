import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_agent_llm(agent_name: str):

    agent_name = agent_name.upper()

    api_key = os.getenv(f"{agent_name}_GROQ_API_KEY")
    model = os.getenv(f"{agent_name}_MODEL")

    if not api_key:
        raise ValueError(
            f"Missing API key for {agent_name}"
        )

    if not model:
        raise ValueError(
            f"Missing model configuration for {agent_name}"
        )

    return ChatGroq(
        model=model,
        api_key=api_key,
        temperature=0,
        max_retries=2
    )
