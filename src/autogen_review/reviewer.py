from src.autogen_review.verdict import (
    VerdictModel,
)


def review_answer(
    retrieved_context: str,
    draft_answer: str,
) -> VerdictModel:

    if draft_answer in retrieved_context:

        return VerdictModel(
            approved=True,
            final_answer=draft_answer,
            reason=(
                "Answer is supported by "
                "retrieved context."
            ),
        )

    return VerdictModel(
        approved=False,
        final_answer=(
            "I cannot verify this information "
            "from the retrieved context."
        ),
        reason=(
            "Unsupported content removed."
        ),
    )