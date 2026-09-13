MAX_QUERY_LENGTH = 2000


def validate_budget(
    query: str,
):

    if len(query) > MAX_QUERY_LENGTH:

        return {
            "allowed": False,
            "error": "Budget exceeded",
        }

    return {
        "allowed": True,
    }