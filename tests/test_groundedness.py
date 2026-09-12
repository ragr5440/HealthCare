from src.governance.groundedness import (
    validate_grounded_answer
)


def test_refusal():

    result = (
        validate_grounded_answer(
            {
                "found": False
            }
        )
    )

    assert (
        result["allowed"]
        is False
    )

    assert (
        result["answer"]
        == "I don't know."
    )


def test_supported_response():

    result = (
        validate_grounded_answer(
            {
                "found": True
            }
        )
    )

    assert (
        result["allowed"]
        is True
    )