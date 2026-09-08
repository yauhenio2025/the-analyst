"""Gzip changes source transport, never the received evidence or commission schema."""
import gzip
import hashlib
import json

from fastapi import APIRouter, FastAPI, Request
from fastapi.testclient import TestClient
import pytest

from src.api import gzip_request


@pytest.fixture
def endpoint():
    app = FastAPI()
    router = APIRouter(route_class=gzip_request.GzipRequestRoute)
    received = []

    @router.post("/receive")
    async def receive(payload: dict, request: Request):
        received.append(payload)
        return {"sha256": hashlib.sha256(await request.body()).hexdigest(),
                "length": request.headers["content-length"], "encoding": request.headers.get("content-encoding")}

    app.include_router(router)
    return TestClient(app), received


def test_transport_preserves_exact_unicode_json_and_clears_encoding(endpoint):
    client, received = endpoint
    payload = {"source": 'Riley’s œuvre 中文; literal \\n and "quotes".\n' * 24000, "cap_usd": 50}
    body = json.dumps(payload, ensure_ascii=False).encode()
    response = client.post("/receive", content=gzip.compress(body), headers={"Content-Type": "application/json", "Content-Encoding": "gzip"})
    assert response.status_code == 200
    assert response.json() == {"sha256": hashlib.sha256(body).hexdigest(), "length": str(len(body)), "encoding": None}
    assert received == [payload]


@pytest.mark.parametrize("body", [b"not gzip", gzip.compress(b'{}')[:-5], gzip.compress(b'{}') + b"trailing"])
def test_invalid_compressed_body_cannot_reach_commission(endpoint, body):
    client, received = endpoint
    response = client.post("/receive", content=body, headers={"Content-Type": "application/json", "Content-Encoding": "gzip"})
    assert response.status_code == 400
    assert not received


def test_inflation_limit_precedes_json_parsing_and_commission(endpoint, monkeypatch):
    client, received = endpoint
    monkeypatch.setattr(gzip_request, "MAX_INFLATED_BYTES", 1024)
    response = client.post("/receive", content=gzip.compress(b'"' + b'x' * 5000 + b'"'),
                           headers={"Content-Type": "application/json", "Content-Encoding": "gzip"})
    assert response.status_code == 413
    assert not received


def test_plain_json_unchanged_and_dossier_router_uses_transport(endpoint):
    from src.api.routes.dossier import router
    client, received = endpoint
    assert router.route_class is gzip_request.GzipRequestRoute
    response = client.post("/receive", json={"question": "A standalone inquiry"})
    assert response.status_code == 200
    assert received == [{"question": "A standalone inquiry"}]
