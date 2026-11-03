
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


AGENT_DEFAULTS = {
    "PLANNER": {
        "temperature": 0.2,
    },
    "WRITER": {
        "temperature": 0.2,
    },
    "EVALUATOR": {
        "temperature": 0.0,
    },
    "ORCHESTRATOR": {
        "temperature": 0.0,
    },
}


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

    defaults = AGENT_DEFAULTS.get(
        agent_name,
        {"temperature": 0.0}
    )

    temperature = float(
        os.getenv(
            f"{agent_name}_TEMPERATURE",
            defaults["temperature"]
        )
    )

    max_tokens = os.getenv(
        f"{agent_name}_MAX_TOKENS"
    )

    config = {
        "model": model,
        "api_key": api_key,
        "temperature": temperature,
        "max_retries": 2,
    }

    if max_tokens:
        config["max_tokens"] = int(max_tokens)

    return ChatGroq(**config)
