def validate_grounded_answer(
    rag_response: dict,
) -> dict:
    """
    Refuse answers when retrieval
    does not support a response.
    """

    if not rag_response.get(
        "found",
        False,
    ):
        return {
            "allowed": False,
            "answer":
                "I don't know."
        }

    return {
        "allowed": True,
        "answer": None,
    }