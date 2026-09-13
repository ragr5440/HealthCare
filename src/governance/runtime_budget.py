MAX_REQUEST_TOKENS = 500


def estimate_tokens(
    text: str,
) -> int:
    """
    Simple deterministic token estimate.

    Under MOCK_LLM mode we approximate tokens
    by counting whitespace-separated words.
    """

    return len(
        text.split()
    )


def validate_budget(
    query: str,
):

    estimated_tokens = (
        estimate_tokens(
            query
        )
    )

    if estimated_tokens > MAX_REQUEST_TOKENS:

        return {
            "allowed": False,
            "estimated_tokens": (
                estimated_tokens
            ),
            "token_budget": (
                MAX_REQUEST_TOKENS
            ),
            "error": (
                "Per-request token "
                "budget exceeded."
            ),
        }

    return {
        "allowed": True,
        "estimated_tokens": (
            estimated_tokens
        ),
        "token_budget": (
            MAX_REQUEST_TOKENS
        ),
    }