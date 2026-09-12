from pydantic import BaseModel


class CrewResponse(
    BaseModel
):
    answer: str
    source: str
    confidence: float
    requires_escalation: bool