from urllib import request

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
import time
from datetime import datetime

from src.api.models import (
    AskRequest,
    AskResponse, 
    AddDocumentRequest,
    AddDocumentResponse
)

from src.api.logger import log_request
from src.governance.pii_guardrails import mask_contact_numbers

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
    start_time = time.time()

    masked_query = mask_contact_numbers(request.query)


    answer = ( "Demo answer")

    latency_ms = (time.time() - start_time) * 1000

    log_request(
        query=masked_query,
        response_status="success",
        latency_ms=latency_ms
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
