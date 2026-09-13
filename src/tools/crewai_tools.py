import json

from crewai.tools import tool

from src.rag.retrieval import retrieve
from src.tools.appointment_lookup import lookup_appointment


@tool("Clinic Policy Search")
def clinic_policy_search(query: str) -> str:
    """
    Search the clinic policy knowledge base.

    Use this tool for questions about booking, cancellation,
    rescheduling, fees, insurance, telemedicine, laboratory
    results, prescription refills, follow-up discounts,
    refunds, privacy, or patient support.
    """

    response = retrieve(
        query=query,
        collection_name="clinic_sentence_chunks",
        top_k=3,
    )

    if not response["in_scope"]:
        output = {
            "found": False,
            "message": (
                "No relevant clinic policy "
                "information found."
            ),
            "results": [],
        }

        return json.dumps(output)

    output = {
        "found": True,
        "results": response["results"],
    }

    return json.dumps(output)


@tool("Appointment Record Lookup")
def appointment_record_lookup(
    appointment_id: str,
) -> str:
    """
    Find one appointment record by its appointment ID.

    Use this tool only when the request contains an appointment
    ID in the form APT- followed by four digits, such as
    APT-0001.
    """

    result = lookup_appointment(
        appointment_id.upper().strip()
    )

    return json.dumps(result)