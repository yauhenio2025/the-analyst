"""Central methods and durable receipts for workers owned by other applications."""
from fastapi import APIRouter

from src.inquiries import service
from src.inquiries.schemas import CompleteRequest, Feedback, PrepareRequest

router = APIRouter(prefix="/inquiries", tags=["inquiries"])


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
