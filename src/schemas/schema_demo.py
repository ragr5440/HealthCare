from pydantic import ValidationError

from src.schemas.response_schema import (
    CrewResponse
)


def main():

    print("VALID RESPONSE")
    print("=" * 50)

    valid_response = {
        "answer":
            "Appointment APT-0001 is confirmed.",
        "source":
            "appointment_lookup",
        "confidence":
            0.95,
        "requires_escalation":
            False,
    }

    try:

        validated = CrewResponse(
            **valid_response
        )

        print(validated.model_dump())

        print(
            "\nValidation Passed"
        )

    except ValidationError as e:

        print(e)

    print(
        "\nINVALID RESPONSE"
    )

    print("=" * 50)

    invalid_response = {
        "answer":
            "Appointment APT-0001"
    }

    try:

        CrewResponse(
            answer=final_answer,
            source="crew",
            confidence=0.95,
            requires_escalation=False,
        )   

    except ValidationError as e:

        print(e)

        print(
            "\nValidation Error Raised"
        )


if __name__ == "__main__":
    main()