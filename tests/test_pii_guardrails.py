from src.governance.pii_guardrails import (
    mask_contact_numbers
)


def test_masking():

    result = mask_contact_numbers(
        "Call me at 9876543210"
    )

    assert (
        "9876543210"
        not in result
    )

    assert (
        "XXXXXXXX10"
        in result
    )