import pytest

from pydantic import (
    ValidationError
)

from src.schemas.response_schema import (
    CrewResponse
)


def test_valid_response():

    response = CrewResponse(
        answer="Appointment confirmed.",
        source="appointment_lookup",
        confidence=0.95,
        requires_escalation=False,
    )

    assert (
        response.answer
        == "Appointment confirmed."
    )


def test_invalid_response():

    with pytest.raises(
        ValidationError
    ):

        CrewResponse(
            answer="hello"
        )