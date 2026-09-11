from src.memory.session_memory import (
    SessionMemory
)


def test_create_session():

    memory = SessionMemory()

    memory.create_session(
        "session_1"
    )

    assert (
        "session_1"
        in memory.sessions
    )


def test_add_message():

    memory = SessionMemory()

    memory.add_message(
        "session_1",
        "user",
        "Hello"
    )

    session = memory.get_session(
        "session_1"
    )

    assert (
        len(
            session[
                "conversation_history"
            ]
        )
        == 1
    )


def test_add_tool_result():

    memory = SessionMemory()

    memory.add_tool_result(
        "session_1",
        "lookup",
        {"status": "confirmed"}
    )

    session = memory.get_session(
        "session_1"
    )

    assert (
        session[
            "tool_results"
        ][0][
            "tool_name"
        ]
        == "lookup"
    )


def test_add_retrieved_document():

    memory = SessionMemory()

    memory.add_retrieved_document(
        "session_1",
        "appointment_cancellation"
    )

    session = memory.get_session(
        "session_1"
    )

    assert (
        "appointment_cancellation"
        in session[
            "retrieved_documents"
        ]
    )