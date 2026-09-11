import json

from src.tools.crewai_tools import (
    clinic_policy_search,
    appointment_record_lookup,
)


def test_crewai_policy_tool():

    raw_result = clinic_policy_search.run(
        query="How do I cancel my appointment?"
    )

    result = json.loads(raw_result)

    assert result["found"] is True
    assert len(result["results"]) > 0
    assert (
        result["results"][0]["document_id"]
        == "appointment_cancellation"
    )


def test_crewai_appointment_tool():

    raw_result = appointment_record_lookup.run(
        appointment_id="APT-0001"
    )

    result = json.loads(raw_result)

    assert result["found"] is True
    assert (
        result["appointment"]["record_id"]
        == "APT-0001"
    )


def test_crewai_invalid_appointment():

    raw_result = appointment_record_lookup.run(
        appointment_id="APT-9999"
    )

    result = json.loads(raw_result)

    assert result["found"] is False