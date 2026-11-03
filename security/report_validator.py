
import re
from urllib.parse import urlparse


REQUIRED_SECTIONS = [
    "Executive Summary",
    "Introduction",
    "Research Findings",
    "Technical Analysis",
    "Security Implications",
    "Limitations",
    "Conclusion",
    "References",
]


def validate_report(report: str, sources: list) -> list[str]:
    """
    Performs deterministic report validation.

    Returns:
        List of validation issues.
        Empty list means validation passed.
    """

    if not report or not report.strip():
        return ["The research report is empty."]

    issues = []

    # 1. Check minimum source count
    if len(sources) < 3:
        issues.append(
            f"Insufficient sources: only {len(sources)} sources collected."
        )

    # 2. Validate source titles and URLs
    for i, source in enumerate(sources, start=1):

        title = source.get("title", "")

        if not isinstance(title, str) or not title.strip():
            issues.append(f"Source [{i}] has no valid title.")

        raw_url = source.get("url", "")

        if not isinstance(raw_url, str):
            issues.append(f"Source [{i}] has an invalid URL.")
            continue

        try:
            parsed_url = urlparse(raw_url.strip())

            if (
                parsed_url.scheme not in ("http", "https")
                or not parsed_url.netloc
            ):
                issues.append(f"Source [{i}] has an invalid URL.")

        except ValueError:
            issues.append(f"Source [{i}] has an invalid URL.")

    # 3. Check numbered citations
    citation_ids = {
        int(value)
        for value in re.findall(r"\[(\d{1,2})\]", report)
    }

    if not citation_ids:
        issues.append("The report contains no numbered citations.")

    valid_ids = set(range(1, len(sources) + 1))

    invalid_ids = citation_ids - valid_ids

    if invalid_ids:
        issues.append(
            f"Invalid citation IDs found: {sorted(invalid_ids)}"
        )

    # 4. Check required report sections
    for section in REQUIRED_SECTIONS:

        pattern = rf"(?im)^#+\s+.*{re.escape(section)}"

        if not re.search(pattern, report):
            issues.append(
                f"Missing report section: {section}"
            )

    return issues


def validator_agent(state):

    print("\n[VALIDATOR] Checking report structure and citations...")

    report = state.get("report", "")
    sources = state.get("sources", [])

    issues = validate_report(report, sources)

    passed = len(issues) == 0

    print(
        "[VALIDATOR] Result:",
        "PASSED" if passed else "FAILED"
    )

    for issue in issues:
        print("[VALIDATOR]", issue)

    return {
        "validation_passed": passed,
        "validation_issues": issues
    }
