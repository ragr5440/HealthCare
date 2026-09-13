import os

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from src.crew.runner import (
    run_policy_query,
    run_lookup_query,
)


async def run_full_crew(
    query: str,
) -> dict:
    """
    Response composer role: combines agent outputs into a final draft response. Draft assembly is deterministic under MOCK_LLM.
    User Query
        ↓
    Retrieval Agent or Lookup Agent
        ↓
    Response Composer
        ↓
    Draft Answer

    Returns both the draft answer and the
    retrieved context for the review stage.
    """

    policy_result = ""

    appointment_result = ""

    query_lower = query.lower()

    if "apt-" in query_lower:

        appointment_result = (
            await run_lookup_query(query)
        )

    else:

        policy_result = (
            await run_policy_query(query)
        )

    draft_answer = (
        appointment_result
        if appointment_result
        else policy_result
    )

    retrieved_context = (
        appointment_result
        if appointment_result
        else policy_result
    )

    return {
        "query": query,
        "draft_answer": draft_answer,
        "retrieved_context": retrieved_context,
    }