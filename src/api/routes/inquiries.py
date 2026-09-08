"""Central methods and durable receipts for workers owned by other applications."""
from fastapi import APIRouter

from src.inquiries import planning, service
from src.inquiries.planning_schemas import PlanningCompleteRequest, PlanningPrepareRequest
from src.inquiries.schemas import CompleteRequest, Feedback, PrepareRequest

router = APIRouter(prefix="/inquiries", tags=["inquiries"])


@router.post("/planning/prepare")
def planning_prepare(request: PlanningPrepareRequest):
    return planning.prepare(request)


@router.post("/planning/complete")
def planning_complete(request: PlanningCompleteRequest):
    return planning.complete(request)


@router.get("/planning/receipts/{receipt_id}")
def planning_receipt(receipt_id: str):
    return planning.get_receipt(receipt_id)


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
