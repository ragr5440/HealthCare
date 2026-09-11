from datetime import datetime

class SessionMemory:
    """
    In-memory session store.

    Each session tracks:
    - conversations
    - tool calls
    - retrieved documents
    """

    def __init__(self):

        self.sessions = {}

    def create_session(
        self,
        session_id: str,
    ):

        if session_id not in self.sessions:

            self.sessions[session_id] = {
                "created_at":
                    datetime.utcnow().isoformat(),

                "conversation_history": [],

                "tool_results": [],

                "retrieved_documents": [],
            }

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):

        self.create_session(
            session_id
        )

        self.sessions[
            session_id
        ][
            "conversation_history"
        ].append(
            {
                "role": role,
                "content": content,
            }
        )

    def add_tool_result(
        self,
        session_id: str,
        tool_name: str,
        result,
    ):

        self.create_session(
            session_id
        )

        self.sessions[
            session_id
        ][
            "tool_results"
        ].append(
            {
                "tool_name":
                    tool_name,
                "result":
                    result,
            }
        )

    def add_retrieved_document(
        self,
        session_id: str,
        document_id: str,
    ):

        self.create_session(
            session_id
        )

        if (
            document_id
            not in self.sessions[
                session_id
            ][
                "retrieved_documents"
            ]
        ):
            self.sessions[
                session_id
            ][
                "retrieved_documents"
            ].append(
                document_id
            )

    def get_session(
        self,
        session_id: str,
    ):

        return self.sessions.get(
            session_id
        )

    def clear_session(
        self,
        session_id: str,
    ):

        if (
            session_id
            in self.sessions
        ):
            del self.sessions[
                session_id
            ]