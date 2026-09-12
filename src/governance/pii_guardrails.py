import re


def mask_contact_numbers(text: str) -> str:
    """
    Mask 10-digit contact numbers.

    Example:
    9876543210 -> XXXXXXXX10
    """

    pattern = r"\b\d{10}\b"

    def mask_match(match):
        number = match.group(0)

        return (
            "X" * 8
            + number[-2:]
        )

    return re.sub(
        pattern,
        mask_match,
        text,
    )