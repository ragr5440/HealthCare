from src.tools.appointment_lookup import (
    lookup_appointment
)
def test_valid_id():

    result = lookup_appointment(
        "APT-0034"
    )

    assert result["found"] is True


def test_invalid_id():

    result = lookup_appointment(
        "APT-9999"
    )

    assert result["found"] is False