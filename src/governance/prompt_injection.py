INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all prior instructions",
    "reveal system prompt",
    "show system prompt",
    "bypass guardrails",
    "forget your instructions",
    "act as a different assistant",
]


def detect_prompt_injection(
    text: str,
) -> dict:

    lowered_text = text.lower()

    for pattern in INJECTION_PATTERNS:

        if pattern in lowered_text:

            return {
                "allowed": False,
                "reason":
                    "Prompt injection detected."
            }

    return {
        "allowed": True,
        "reason":
            "Input allowed."
    }