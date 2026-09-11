from src.tools.rag_tool import (
    search_policy
)

def test_policy_found():

    result = search_policy(
        "How do I cancel my appointment?"
    )

    assert result["found"] is True


def test_policy_not_found():

    result = search_policy(
        "What is machine learning?"
    )

    assert result["found"] is False
    assert (
        result["message"]
        == "No relevant clinic policy information found."
    )