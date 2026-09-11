from src.crew.mock_llm import MockLLM


POLICY_SYSTEM_MESSAGE = """
Tool Name: clinic_policy_search
Tool Arguments: {
  "properties": {
    "query": {
      "title": "Query",
      "type": "string"
    }
  },
  "required": ["query"],
  "type": "object"
}
Tool Description: Search clinic policies.

Observation: the result of the action
"""


APPOINTMENT_SYSTEM_MESSAGE = """
Tool Name: appointment_record_lookup
Tool Arguments: {
  "properties": {
    "appointment_id": {
      "title": "Appointment Id",
      "type": "string"
    }
  },
  "required": ["appointment_id"],
  "type": "object"
}
Tool Description: Find an appointment record.

Observation: the result of the action
"""


def test_policy_action_uses_query_schema():

    llm = MockLLM()

    response = llm.call(
        [
            {
                "role": "system",
                "content": POLICY_SYSTEM_MESSAGE,
            },
            {
                "role": "user",
                "content": (
                    "Current Task: Answer this question: "
                    "'How do I cancel my appointment?'"
                ),
            },
        ]
    )

    assert (
        "Action: clinic_policy_search"
        in response
    )

    assert (
        '"query": '
        in response
    )

    assert "Final Answer:" not in response


def test_appointment_action_uses_id_schema():

    llm = MockLLM()

    response = llm.call(
        [
            {
                "role": "system",
                "content": APPOINTMENT_SYSTEM_MESSAGE,
            },
            {
                "role": "user",
                "content": (
                    "Check the status of APT-0001."
                ),
            },
        ]
    )

    assert (
        "Action: appointment_record_lookup"
        in response
    )

    assert (
        '"appointment_id": "APT-0001"'
        in response
    )


def test_system_placeholder_is_not_observation():

    llm = MockLLM()

    response = llm.call(
        [
            {
                "role": "system",
                "content": POLICY_SYSTEM_MESSAGE,
            },
            {
                "role": "user",
                "content": (
                    "How do I cancel my appointment?"
                ),
            },
        ]
    )

    assert "Action:" in response
    assert "Final Answer:" not in response


def test_real_observation_creates_final_answer():

    llm = MockLLM()

    response = llm.call(
        [
            {
                "role": "system",
                "content": POLICY_SYSTEM_MESSAGE,
            },
            {
                "role": "user",
                "content": (
                    "How do I cancel my appointment?"
                ),
            },
            {
                "role": "assistant",
                "content": (
                    "Thought: I should use the tool.\n"
                    "Action: clinic_policy_search\n"
                    "Action Input: "
                    '{"query": "How do I cancel my appointment?"}'
                ),
            },
            {
                "role": "user",
                "content": (
                    'Observation: {"found": true, '
                    '"results": [{"text": '
                    '"Patients may cancel up to 24 hours '
                    'before the scheduled time."}]}'
                ),
            },
        ]
    )

    assert "Final Answer:" in response

    assert (
        "Patients may cancel up to 24 hours"
        in response
    )