from typing import Literal
from pydantic import BaseModel, Field

class EvaluationClass(BaseModel):

    topic_relevance: Literal["PASS", "PARTIAL", "FAIL"] = Field(
        description="How closely the report addresses the original query."
    )

    research_coverage: Literal["PASS", "PARTIAL", "FAIL"] = Field(
        description="How adequately the research questions are answered."
    )

    source_quality: Literal["PASS", "PARTIAL", "FAIL"] = Field(
        description="The relevance and credibility of the sources."
    )

    evidence_quality: Literal["PASS", "PARTIAL", "FAIL"] = Field(
        description="How well factual claims are supported by evidence."
    )

    technical_depth: Literal["PASS", "PARTIAL", "FAIL"] = Field(
        description="The depth and accuracy of technical analysis."
    )

    issues: list[str] = Field(
        default_factory=list,
        description="Specific weaknesses found in the report."
    )

    strengths: list[str] = Field(
        default_factory=list,
        description="Positive aspects of the report."
    )

    recommendation: Literal["APPROVE", "REVISE"] = Field(
        description="Whether the report is ready for final review."
    )