
import re


# Requests seeking operational weapon or explosive construction
UNSAFE_PATTERNS = [
    r"\b(make|making|build|building|construct|constructing|manufacture|manufacturing)\b.{0,100}\b(bomb|explosive|explosives|weapon)\b",

    r"\b(bomb|explosive|explosives)\b.{0,100}\b(build|make|manufacture|construct|recipe|blueprint)\b",

    r"\b(instructions|steps|procedure|guide)\b.{0,100}\b(make|making|build|building|manufacture|manufacturing)\b.{0,100}\b(bomb|explosive|explosives)\b",

    r"\b(destructive power|explosive power|blast radius)\b.{0,80}\b(increase|maximize|optimize|enhance)\b",
]


def check_input_safety(query: str):

    normalized_query = query.lower()

    for pattern in UNSAFE_PATTERNS:

        if re.search(pattern, normalized_query):

            return {
                "safe": False,
                "reason": (
                    "The request seeks potentially harmful "
                    "operational instructions involving "
                    "explosives or weapons."
                )
            }

    return {
        "safe": True,
        "reason": ""
    }
