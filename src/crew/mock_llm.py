import json
import re
from typing import Any

from crewai import BaseLLM


class MockLLM(BaseLLM):
    """
    Deterministic CrewAI-compatible mock LLM.

    It supports CrewAI's text-based ReAct workflow:

    Thought
    Action
    Action Input
    Observation
    Final Answer
    """

    def __init__(
        self,
        model: str = "mock-llm",
        temperature: float | None = None,
    ):
        super().__init__(
            model=model,
            temperature=temperature,
        )

    def call(
        self,
        messages,
        tools=None,
        callbacks=None,
        available_functions=None,
        **kwargs,
    ) -> str:
        """
        Generate either a ReAct tool action or a final answer.
        """

        normalized_messages = self._normalize_messages(
            messages
        )

        observation = self._find_real_observation(
            normalized_messages
        )

        if observation is not None:
            return self._create_final_answer(
                observation
            )

        system_content = self._get_message_content(
            normalized_messages,
            role="system",
        )

        user_content = self._get_latest_user_content(
            normalized_messages
        )

        tool_definition = self._extract_tool_definition(
            system_content
        )

        if tool_definition is None:
            return (
                "Thought: I cannot identify an available tool.\n"
                "Final Answer: I could not process the request."
            )

        tool_name = tool_definition["tool_name"]
        argument_names = tool_definition[
            "argument_names"
        ]

        action_input = self._build_action_input(
            argument_names=argument_names,
            user_content=user_content,
        )

        if action_input is None:
            return (
                "Thought: The request does not contain the "
                "information required by the available tool.\n"
                "Final Answer: I could not identify the required "
                "tool input."
            )

        return (
            "Thought: I need to use the available tool to "
            "answer the request.\n"
            f"Action: {tool_name}\n"
            f"Action Input: {json.dumps(action_input)}"
        )

    def _normalize_messages(
        self,
        messages,
    ) -> list[dict[str, Any]]:
        """
        Convert string input into CrewAI-style messages.
        """

        if isinstance(messages, str):
            return [
                {
                    "role": "user",
                    "content": messages,
                }
            ]

        return messages

    def _get_message_content(
        self,
        messages,
        role: str,
    ) -> str:
        """
        Combine content for messages with the requested role.
        """

        return "\n".join(
            str(message.get("content", ""))
            for message in messages
            if message.get("role") == role
        )

    def _get_latest_user_content(
        self,
        messages,
    ) -> str:
        """
        Return the latest non-system message content.
        """

        for message in reversed(messages):
            if message.get("role") != "system":
                return str(
                    message.get("content", "")
                )

        return ""

    def _extract_tool_definition(
        self,
        system_content: str,
    ) -> dict[str, Any] | None:
        """
        Extract the available tool name and argument schema.

        The argument schema determines how the request is
        dispatched. The tool name is used only after the schema
        has selected the appropriate input structure.
        """

        name_match = re.search(
            r"Tool Name:\s*([A-Za-z0-9_]+)",
            system_content,
        )

        if name_match is None:
            return None

        tool_name = name_match.group(1)

        schema_match = re.search(
            r"Tool Arguments:\s*(\{.*?\})"
            r"\s*Tool Description:",
            system_content,
            flags=re.DOTALL,
        )

        if schema_match is None:
            return None

        try:
            schema = json.loads(
                schema_match.group(1)
            )
        except json.JSONDecodeError:
            return None

        properties = schema.get(
            "properties",
            {}
        )

        return {
            "tool_name": tool_name,
            "argument_names": set(
                properties.keys()
            ),
        }

    def _build_action_input(
        self,
        argument_names: set[str],
        user_content: str,
    ) -> dict[str, str] | None:
        """
        Build tool arguments from the declared schema.

        This intentionally dispatches by argument schema,
        not by matching words in the tool name.
        """

        if argument_names == {"query"}:
            question = self._extract_task_question(
                user_content
            )

            return {
                "query": question,
            }

        if argument_names == {"appointment_id"}:
            appointment_match = re.search(
                r"\bAPT-\d{4}\b",
                user_content,
                flags=re.IGNORECASE,
            )

            if appointment_match is None:
                return None

            return {
                "appointment_id": (
                    appointment_match
                    .group(0)
                    .upper()
                )
            }

        return None

    def _extract_task_question(
        self,
        user_content: str,
    ) -> str:
        """
        Extract a quoted question from CrewAI's task prompt.
        """

        quoted_match = re.search(
            r"""question:\s*?P<question>.+?['"]""",
            user_content,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if quoted_match:
            return quoted_match.group("question").strip()

        current_task_match = re.search(
            r"Current Task:\s*(?P<task>.+?)(?:\n\n|$)",
            user_content,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if current_task_match:
            return current_task_match.group("task").strip()

        return user_content.strip()

    def _find_real_observation(
        self,
        messages,
    ) -> dict[str, Any] | None:
        """
        Find an actual tool observation.

        System messages are deliberately excluded because
        CrewAI's built-in ReAct template contains the placeholder:

        Observation: the result of the action
        """

        for message in reversed(messages):
            if message.get("role") == "system":
                continue

            content = str(
                message.get("content", "")
            )

            marker_position = content.rfind(
                "Observation:"
            )

            if marker_position == -1:
                continue

            observation_text = content[
                marker_position
                + len("Observation:"):
            ].strip()

            if not observation_text:
                continue

            if observation_text.startswith(
                "the result of the action"
            ):
                continue

            parsed_observation = (
                self._extract_json_object(
                    observation_text
                )
            )

            if parsed_observation is not None:
                return parsed_observation

        return None

    def _extract_json_object(
        self,
        text: str,
    ) -> dict[str, Any] | None:
        """
        Decode the first JSON object found in text.
        """

        object_start = text.find("{")

        if object_start == -1:
            return None

        decoder = json.JSONDecoder()

        try:
            value, _ = decoder.raw_decode(
                text[object_start:]
            )
        except json.JSONDecodeError:
            return None

        if not isinstance(value, dict):
            return None

        return value

    def _create_final_answer(
        self,
        observation: dict[str, Any],
    ) -> str:
        """
        Convert tool output into a deterministic final answer.
        """

        if not observation.get("found"):
            message = observation.get(
                "message",
                "No matching information was found.",
            )

            return (
                "Thought: I now know the final answer.\n"
                f"Final Answer: {message}"
            )

        if "appointment" in observation:
            appointment = observation[
                "appointment"
            ]

            answer = (
                f"Appointment "
                f"{appointment['record_id']} has status "
                f"{appointment['status']}. "
                f"The category is "
                f"{appointment['category']}, and the "
                f"consultation fee is ₹"
                f"{appointment['consultation_fee_inr']}. "
                f"The escalation score is "
                f"{observation['escalation_score']}."
            )

            return (
                "Thought: I now know the final answer.\n"
                f"Final Answer: {answer}"
            )

        results = observation.get(
            "results",
            []
        )

        if results:
            policy_text = results[0].get(
                "text",
                "No policy text was returned.",
            )

            return (
                "Thought: I now know the final answer.\n"
                f"Final Answer: {policy_text}"
            )

        return (
            "Thought: I now know the final answer.\n"
            "Final Answer: No matching information was found."
        )

    def supports_function_calling(
        self,
    ) -> bool:
        """
        Tool use occurs through CrewAI's text-based ReAct loop.
        """

        return False

    def get_context_window_size(
        self,
    ) -> int:
        return 8192