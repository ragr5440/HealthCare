import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "appointments.json"
)


def load_appointments():

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def calculate_escalation_score(
    appointment
):
    """
    Combines:
    - follow-up status
    - recency
    """

    recency_score = (
        1
        - (
            appointment[
                "days_since_created"
            ]
            / 30
        )
    )

    recency_score = max(
        0,
        min(recency_score, 1)
    )

    follow_up_score = (
        1
        if appointment[
            "follow_up_required"
        ]
        else 0
    )

    escalation_score = (
        0.7
        * follow_up_score
        +
        0.3
        * recency_score
    )

    return round(
        escalation_score,
        2
    )


def lookup_appointment(
    appointment_id
):

    appointments = (
        load_appointments()
    )

    for appointment in appointments:

        if (
            appointment["record_id"]
            == appointment_id
        ):

            return {
                "found": True,
                "appointment":
                    appointment,
                "escalation_score":
                    calculate_escalation_score(
                        appointment
                    ),
            }

    return {
        "found": False,
        "message":
            "Appointment not found."
    }