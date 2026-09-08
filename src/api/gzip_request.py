"""Decode large source submissions before FastAPI parses their ordinary JSON schema."""
import os
import zlib

from fastapi import HTTPException, Request
from fastapi.routing import APIRoute


MAX_INFLATED_BYTES = int(os.getenv("DOSSIER_MAX_INFLATED_REQUEST_BYTES", str(128 * 1024 * 1024)))


class GzipRequestRoute(APIRoute):
    def get_route_handler(self):
        original = super().get_route_handler()

        async def handle(request: Request):
            if request.headers.get("content-encoding", "").strip().lower() != "gzip":
                return await original(request)
            compressed = await request.body()
            try:
                decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
                body = decoder.decompress(compressed, MAX_INFLATED_BYTES + 1)
                if len(body) > MAX_INFLATED_BYTES or decoder.unconsumed_tail:
                    raise HTTPException(413, "Inflated dossier request exceeds the configured byte limit")
                if not decoder.eof or decoder.unused_data:
                    raise HTTPException(400, "Incomplete or trailing gzip request data")
            except zlib.error as exc:
                raise HTTPException(400, "Invalid gzip request body") from exc
            scope = dict(request.scope)
            scope["headers"] = [(key, value) for key, value in scope["headers"]
                                if key.lower() not in (b"content-encoding", b"content-length")]
            scope["headers"].append((b"content-length", str(len(body)).encode()))
            inflated = Request(scope, receive=request.receive)
            inflated._body = body
            return await original(inflated)

        return handle
