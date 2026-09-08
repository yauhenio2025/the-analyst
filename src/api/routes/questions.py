"""Reusable question development without application-owned accepted state."""
from fastapi import APIRouter

from src.inquiries.schemas import Feedback
from src.questions import service
from src.questions.schemas import CompleteRequest, PrepareRequest

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/prepare")
def prepare(request: PrepareRequest):
    return service.prepare(request)


@router.post("/complete")
def complete(request: CompleteRequest):
    return service.complete(request)


@router.get("/receipts/{receipt_id}")
def receipt(receipt_id: str):
    return service.get_receipt(receipt_id)


@router.post("/receipts/{receipt_id}/feedback")
def feedback(receipt_id: str, request: Feedback):
    return service.add_feedback(receipt_id, request)
