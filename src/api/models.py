from pydantic import BaseModel
from typing import List, Optional


class AskRequest(BaseModel):
    query: str
    session_id: str


class AskResponse(BaseModel):
    answer: str
    grounded: bool
    sources: List[str] = []


class AddDocumentRequest(BaseModel):
    doc_id: str
    text: str


class AddDocumentResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str