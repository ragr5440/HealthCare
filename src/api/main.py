from urllib import request

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from src.api.models import (
    AskRequest,
    AskResponse, 
    AddDocumentRequest,
    AddDocumentResponse
)

app = FastAPI(
    title="Practo Support Agent"
)

@app.get("/")
def root():
    return {
        "message": "Practo Support Agent API is running"
    }

@app.post(
    "/ask",
    response_model=AskResponse
)
def ask_question(
    request: AskRequest
):
    """
    Sends query through
    guardrails -> crew -> output validator
    """

    answer = (
        "Demo answer"
    )

    return AskResponse(
        answer=answer,
        grounded=True,
        sources=["knowledge_base"]
    )

@app.post(
    "/add-document",
    response_model=AddDocumentResponse
)
def add_document(
    request: AddDocumentRequest
):

# TODO:
# chunk text
# embed text
# chroma upsert

    return AddDocumentResponse(
        message=f"Document {request.doc_id} added"
    )

@app.websocket("/chat")
async def chat_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    try:

        while True:

            message = (
                await websocket.receive_text()
            )

            response = (
                f"Received: {message}"
            )

            await websocket.send_text(
                response
            )

    except WebSocketDisconnect:

        print(
            "Client disconnected."
        )
