from src.governance.guardrails import (
    Guardrails
)


def test_valid_appointment_id():

    result = (
        Guardrails
        .validate_appointment_id(
            "APT-0001"
        )
    )

    assert result.allowed is True


def test_invalid_appointment_id():

    result = (
        Guardrails
        .validate_appointment_id(
            "APT-ABC"
        )
    )

    assert result.allowed is False


def test_valid_rag_response():

    result = (
        Guardrails
        .validate_rag_response(
            {
                "found": True
            }
        )
    )

    assert result.allowed is True


def test_invalid_rag_response():

    result = (
        Guardrails
        .validate_rag_response(
            {
                "found": False
            }
        )
    )

    assert result.allowed is False


def test_empty_response():

    result = (
        Guardrails
        .validate_final_response(
            ""
        )
    )

    assert result.allowed is False


def test_valid_response():

    result = (
        Guardrails
        .validate_final_response(
            "Hello"
        )
    )

    assert result.allowed is True