from src.crew.mock_llm import (
    MockLLM
)

def test_lookup_route():

    llm = MockLLM()

    result = llm.call(
        "What is the status of APT-0001?"
    )

    assert (
        "appointment lookup"
        in result.lower()
    )

def test_policy_route():

    llm = MockLLM()

    result = llm.call(
        "How do I cancel my appointment?"
    )

    assert (
        "policy retrieval"
        in result.lower()
    )