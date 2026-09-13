import asyncio

from src.autogen_review.review_team import (
    run_review_team,
)
from src.crew.full_crew_runner import (
    run_full_crew,
)


def print_team_messages(
    task_result,
) -> None:
    """
    Print all messages as evidence that both AutoGen
    agents participated.
    """

    print("\nAUTOGEN TEAM MESSAGES")
    print("-" * 60)

    for message in task_result.messages:
        print(f"Source: {message.source}")
        print(f"Content: {message.content}")
        print("-" * 60)


async def approval_demo() -> None:
    """
    Generate a real CrewAI-backed draft and demonstrate
    approval without modification.
    """

    crew_result = await run_full_crew(
        "Check appointment status for APT-0015"
    )

    verdict, task_result = await run_review_team(
        original_query=crew_result["query"],
        retrieved_context=(
            crew_result["retrieved_context"]
        ),
        draft_answer=(
            crew_result["draft_answer"]
        ),
    )

    print("\nAPPROVAL TEST")
    print("=" * 60)
    print("Original query:")
    print(crew_result["query"])

    print("\nRetrieved context:")
    print(crew_result["retrieved_context"])

    print("\nCrewAI draft:")
    print(crew_result["draft_answer"])

    print_team_messages(task_result)

    print("\nSTRUCTURED VERDICT")
    print(verdict.model_dump_json(indent=2))

    assert verdict.approved is True

    assert (
        verdict.final_answer
        == crew_result["draft_answer"]
    )

    print("\nPASS: Draft approved unchanged.")


async def revision_demo() -> None:
    """
    Deliberately inject an unsupported claim into a
    CrewAI-backed draft and demonstrate revision.
    """

    crew_result = await run_full_crew(
        "What is the cancellation policy?"
    )

    injected_draft = (
        f"{crew_result['draft_answer']} "
        "Patients also receive free MRI scans."
    )

    verdict, task_result = await run_review_team(
        original_query=crew_result["query"],
        retrieved_context=(
            crew_result["retrieved_context"]
        ),
        draft_answer=injected_draft,
    )

    print("\nREVISION TEST")
    print("=" * 60)
    print("Original query:")
    print(crew_result["query"])

    print("\nRetrieved context:")
    print(crew_result["retrieved_context"])

    print("\nDeliberately modified draft:")
    print(injected_draft)

    print_team_messages(task_result)

    print("\nSTRUCTURED VERDICT")
    print(verdict.model_dump_json(indent=2))

    assert verdict.approved is False

    assert "free MRI" not in verdict.final_answer

    print(
        "\nPASS: Unsupported claim detected "
        "and removed."
    )


async def main() -> None:
    await approval_demo()
    await revision_demo()


if __name__ == "__main__":
    asyncio.run(main())