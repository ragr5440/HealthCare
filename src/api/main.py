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
from src.governance.prompt_injection import detect_prompt_injection
from src.governance.runtime_budget import validate_budget

import time

from fastapi import HTTPException

from src.autogen_review.review_team import run_review_team
from src.crew.full_crew_runner import run_full_crew
from src.rag.chunking import build_sentence_chunks, sentence_chunk
from src.rag.indexing import add_chunks_to_collection
from src.rag.retrieval import MODEL, get_collection

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
    response_model=AskResponse,
)
async def ask_question(
    request: AskRequest,
) -> AskResponse:
    start_time = time.time()

    budget_result = validate_budget(
        request.query
    )

    if not budget_result["allowed"]:
        raise HTTPException(
            status_code=413,
            detail={
                "error": budget_result["error"],
                "estimated_tokens": budget_result[
                    "estimated_tokens"
                ],
                "token_budget": budget_result[
                    "token_budget"
                ],
            },
        )

    masked_query = mask_contact_numbers(
        request.query
    )

    crew_result = await run_full_crew(
        masked_query
    )

    verdict, _ = await run_review_team(
        original_query=crew_result["query"],
        retrieved_context=crew_result[
            "retrieved_context"
        ],
        draft_answer=crew_result[
            "draft_answer"
        ],
    )

    latency_ms = (
        time.time() - start_time
    ) * 1000

    log_request(
        query=masked_query,
        response_status="success",
        latency_ms=latency_ms,
    )

    return AskResponse(
        answer=verdict.final_answer,
        grounded=verdict.approved,
        sources=["knowledge_base"],
    )

@app.post(
    "/add-document",
    response_model=AddDocumentResponse,
)
async def add_document(
    request: AddDocumentRequest,
) -> AddDocumentResponse:
    start_time = time.time()

    budget_check = validate_budget(
        request.text
    )

    if not budget_check["allowed"]:
        raise HTTPException(
            status_code=413,
            detail={
                "error": budget_check["error"],
                "estimated_tokens": budget_check[
                    "estimated_tokens"
                ],
                "token_budget": budget_check[
                    "token_budget"
                ],
            },
        )

    masked_text = mask_contact_numbers(
        request.text
    )

    document = {
        request.doc_id: masked_text
    }

    chunks = build_sentence_chunks(
        document
    )

    collection = get_collection(
        "clinic_sentence_chunks"
    )

    add_chunks_to_collection(
        collection=collection,
        chunks=chunks,
        model=MODEL,
    )

    latency_ms = (
        time.time() - start_time
    ) * 1000

    log_request(
        query=masked_text,
        response_status="document_added",
        latency_ms=latency_ms,
    )

    return AddDocumentResponse(
        message=(
            f"Document {request.doc_id} added "
            f"with {len(chunks)} chunks"
        )
    )

@app.websocket("/chat")
async def chat_endpoint(
    websocket: WebSocket,
):
    await websocket.accept()

    try:
        while True:
            message = await websocket.receive_text()

            start_time = time.time()

            budget_check = validate_budget(
                message
            )

            if not budget_check["allowed"]:
                await websocket.send_json(
                    {
                        "error": budget_check["error"],
                        "estimated_tokens": budget_check[
                            "estimated_tokens"
                        ],
                        "token_budget": budget_check[
                            "token_budget"
                        ],
                    }
                )

                continue

            masked_message = mask_contact_numbers(
                message
            )

            injection_result = detect_prompt_injection(
                masked_message
            )

            if not injection_result["allowed"]:
                await websocket.send_json(
                    {
                        "error": injection_result["error"]
                    }
                )

                continue


            crew_result = await run_full_crew(
                masked_message
            )

            verdict, _ = await run_review_team(
                original_query=crew_result["query"],
                retrieved_context=crew_result[
                    "retrieved_context"
                ],
                draft_answer=crew_result[
                    "draft_answer"
                ],
            )

            latency_ms = (
                time.time() - start_time
            ) * 1000

            log_request(
                query=masked_message,
                response_status="success",
                latency_ms=latency_ms,
            )

            if "APT-" in masked_message.upper():
                sources = [
                    "appointment_dataset"
                ]
            else:
                sources = [
                    "knowledge_base"
                ]

            await websocket.send_json(
                {
                    "answer": verdict.final_answer,
                    "grounded": verdict.approved,
                    "sources": sources,
                }
            )

    except WebSocketDisconnect:
        print(
            "Client disconnected safely."
        )