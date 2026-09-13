import json
from typing import Any

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import StructuredMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.models import ModelFamily
from autogen_ext.models.replay import ReplayChatCompletionClient

from src.autogen_review.verdict import VerdictModel


MODEL_INFO = {
    "vision": False,
    "function_calling": False,
    "json_output": True,
    "family": ModelFamily.UNKNOWN,
    "structured_output": True,
}


def normalize_text(text: str) -> str:
    """
    Normalize text for deterministic comparison.

    This ignores capitalization and repeated whitespace.
    """

    return " ".join(text.casefold().split())


def draft_is_supported(
    retrieved_context: str,
    draft_answer: str,
) -> bool:
    """
    Determine whether the full draft is present in the
    retrieved context.

    This is the deterministic MOCK_LLM groundedness rule
    used by the AutoGen review team.
    """

    normalized_context = normalize_text(
        retrieved_context
    )

    normalized_draft = normalize_text(
        draft_answer
    )

    if not normalized_draft:
        return False

    return normalized_draft in normalized_context


def build_review_responses(
    retrieved_context: str,
    draft_answer: str,
) -> tuple[str, str]:
    """
    Create the two deterministic responses consumed by
    the AutoGen ReplayChatCompletionClient instances.

    The first response belongs to the Policy Compliance
    Reviewer.

    The second response belongs to the Final Editor and
    must validate against VerdictModel.
    """

    supported = draft_is_supported(
        retrieved_context=retrieved_context,
        draft_answer=draft_answer,
    )

    if supported:
        reviewer_response = (
            "APPROVE. The CrewAI draft is fully supported "
            "by the retrieved context and should remain "
            "unchanged."
        )

        verdict = VerdictModel(
            approved=True,
            final_answer=draft_answer,
            reason=(
                "The draft answer is fully supported by "
                "the retrieved context."
            ),
        )

    else:
        reviewer_response = (
            "REVISE. The CrewAI draft contains one or more "
            "claims that are not supported by the retrieved "
            "context."
        )

        verdict = VerdictModel(
            approved=False,
            final_answer=(
                "I cannot verify this information from "
                "the available clinic policies."
            ),
            reason=(
                "The draft contained unsupported content, "
                "so the unsupported claim was removed."
            ),
        )

    editor_response = json.dumps(
        verdict.model_dump(),
        ensure_ascii=False,
    )

    return reviewer_response, editor_response


def create_review_team(
    retrieved_context: str,
    draft_answer: str,
) -> RoundRobinGroupChat:
    """
    Create the required two-agent AutoGen review team.

    Turn 1:
        Policy Compliance Reviewer

    Turn 2:
        Final Editor
    """

    reviewer_response, editor_response = (
        build_review_responses(
            retrieved_context=retrieved_context,
            draft_answer=draft_answer,
        )
    )

    reviewer_model_client = ReplayChatCompletionClient(
        chat_completions=[
            reviewer_response,
        ],
        model_info=MODEL_INFO,
    )

    editor_model_client = ReplayChatCompletionClient(
        chat_completions=[
            editor_response,
        ],
        model_info=MODEL_INFO,
    )

    policy_reviewer = AssistantAgent(
        name="policy_compliance_reviewer",
        description=(
            "Reviews the CrewAI draft answer against the "
            "original retrieved context."
        ),
        model_client=reviewer_model_client,
        system_message=(
            "You are the Policy Compliance Reviewer. "
            "Compare the CrewAI draft answer with the "
            "original retrieved context. Approve only "
            "claims supported by that context. Identify "
            "unsupported claims. Do not introduce new "
            "clinic, appointment, or medical information."
        ),
    )

    final_editor = AssistantAgent(
        name="final_editor",
        description=(
            "Produces the final structured review verdict."
        ),
        model_client=editor_model_client,
        system_message=(
            "You are the Final Editor. Review the Policy "
            "Compliance Review, the original retrieved "
            "context, and the CrewAI draft. Approve a "
            "supported draft without changing it. If the "
            "draft contains unsupported claims, revise it "
            "by removing those claims. Return only a "
            "structured VerdictModel."
        ),
        output_content_type=VerdictModel,
    )

    team = RoundRobinGroupChat(
        participants=[
            policy_reviewer,
            final_editor,
        ],
        max_turns=2,
        custom_message_types=[
            StructuredMessage[VerdictModel],
        ],
    )

    return team


def extract_verdict(
    task_result: Any,
) -> VerdictModel:
    """
    Find the Final Editor message in the AutoGen TaskResult
    and validate it as a VerdictModel.
    """

    for message in reversed(task_result.messages):
        source = getattr(
            message,
            "source",
            None,
        )

        if source != "final_editor":
            continue

        content = getattr(
            message,
            "content",
            None,
        )

        if isinstance(content, VerdictModel):
            return content

        if isinstance(content, dict):
            return VerdictModel.model_validate(
                content
            )

        if isinstance(content, str):
            return VerdictModel.model_validate_json(
                content
            )

    raise ValueError(
        "The AutoGen Final Editor did not return "
        "a valid structured VerdictModel."
    )


async def run_review_team(
    original_query: str,
    retrieved_context: str,
    draft_answer: str,
) -> tuple[VerdictModel, Any]:
    """
    Create and execute the two-agent AutoGen review team.

    Returns:
        verdict:
            The validated structured VerdictModel.

        task_result:
            The complete AutoGen TaskResult, retained for
            transcript evidence.
    """

    team = create_review_team(
        retrieved_context=retrieved_context,
        draft_answer=draft_answer,
    )

    review_task = (
        "Review the CrewAI draft answer using only the "
        "original retrieved context.\n\n"
        "ORIGINAL USER QUERY:\n"
        f"{original_query}\n\n"
        "ORIGINAL RETRIEVED CONTEXT:\n"
        f"{retrieved_context}\n\n"
        "CREWAI COMPOSER DRAFT:\n"
        f"{draft_answer}\n\n"
        "The Policy Compliance Reviewer must review the "
        "draft first. The Final Editor must then approve "
        "the draft unchanged or revise it and return a "
        "structured VerdictModel."
    )

    task_result = await team.run(
        task=review_task
    )

    verdict = extract_verdict(
        task_result
    )

    return verdict, task_result