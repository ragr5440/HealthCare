from src.autogen_review.reviewer import (
    review_answer,
)


def approval_demo():

    retrieved_context = (
        "Patients may cancel appointments "
        "up to 24 hours before the appointment."
    )

    draft_answer = (
        "Patients may cancel appointments "
        "up to 24 hours before the appointment."
    )

    verdict = review_answer(
        retrieved_context,
        draft_answer,
    )

    print("\nAPPROVAL TEST")
    print("=" * 50)
    print(verdict)


def revision_demo():

    retrieved_context = (
        "Patients may cancel appointments "
        "up to 24 hours before the appointment."
    )

    draft_answer = (
        "Patients receive free MRI scans."
    )

    verdict = review_answer(
        retrieved_context,
        draft_answer,
    )

    print("\nREVISION TEST")
    print("=" * 50)
    print(verdict)


if __name__ == "__main__":

    approval_demo()

    revision_demo()