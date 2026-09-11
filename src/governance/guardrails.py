import re


class GuardrailResult:

    def __init__(
        self,
        allowed: bool,
        reason: str,
    ):
        self.allowed = allowed
        self.reason = reason

    def to_dict(self):

        return {
            "allowed": self.allowed,
            "reason": self.reason,
        }


class Guardrails:
    """
    Governance checks for:

    - Appointment IDs
    - Out-of-scope questions
    - Empty answers
    """

    APPOINTMENT_PATTERN = (
        r"^APT-\d{4}$"
    )

    @staticmethod
    def validate_appointment_id(
        appointment_id: str,
    ):

        if re.match(
            Guardrails.APPOINTMENT_PATTERN,
            appointment_id,
        ):
            return GuardrailResult(
                True,
                "Valid appointment ID.",
            )

        return GuardrailResult(
            False,
            "Invalid appointment ID format.",
        )

    @staticmethod
    def validate_rag_response(
        rag_result,
    ):

        if not rag_result.get(
            "found",
            False,
        ):
            return GuardrailResult(
                False,
                "No relevant policy found.",
            )

        return GuardrailResult(
            True,
            "Valid policy response.",
        )

    @staticmethod
    def validate_final_response(
        response_text: str,
    ):

        if (
            response_text
            is None
        ):
            return GuardrailResult(
                False,
                "Response is None.",
            )

        if not response_text.strip():
            return GuardrailResult(
                False,
                "Response is empty.",
            )

        return GuardrailResult(
            True,
            "Valid response.",
        )