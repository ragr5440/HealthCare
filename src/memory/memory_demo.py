from src.memory.langchain_memory import (
    build_memory_chain
)

def main():

    chain, memory = (
        build_memory_chain()
    )

    print(
        "\n=== SESSION A ===\n"
    )

    session_a = {
        "configurable": {
            "session_id":
                "session_a"
        }
    }

    response_1 = chain.invoke(
        "My appointment ID is APT-0001",
        config=session_a,
    )

    print(response_1)

    response_2 = chain.invoke(
        "What appointment ID did I mention earlier?",
        config=session_a,
    )

    print(response_2)

    history = (
        memory.get_session_history(
            "session_a"
        )
    )

    print(
        "\nStored Messages:"
    )

    for message in history.messages:

        print(message)

    print(
        "\n=== SESSION B ===\n"
    )

    session_b = {
        "configurable": {
            "session_id":
                "session_b"
        }
    }

    history_b = (
        memory.get_session_history(
            "session_b"
        )
    )

    print(
        "Message Count:",
        len(
            history_b.messages
        ),
    )


if __name__ == "__main__":
    main()