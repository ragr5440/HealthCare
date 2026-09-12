from langchain_core.chat_history import (
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import (
    RunnableWithMessageHistory,
)
from langchain_core.runnables import (
    RunnableLambda,
)


class LangChainSessionMemory:

    def __init__(self):

        self.store = {}

    def get_session_history(
        self,
        session_id: str,
    ):

        if session_id not in self.store:

            self.store[session_id] = (
                InMemoryChatMessageHistory()
            )

        return self.store[session_id]


def build_memory_chain():

    memory = LangChainSessionMemory()

    def healthcare_chat(user_input):

        return (
            f"Healthcare Assistant Response: "
            f"{user_input}"
        )

    runnable = RunnableLambda(
        healthcare_chat
    )

    chain = RunnableWithMessageHistory(
        runnable=runnable,
        get_session_history=(
            memory.get_session_history
        ),
    )

    return chain, memory