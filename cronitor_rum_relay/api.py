import datetime
import json
import logging

import httpx
from fastapi import FastAPI, Response, HTTPException, Body
from httpx import AsyncClient
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from cronitor_rum_relay import settings
from cronitor_rum_relay.helpers import (
    select_headers,
    sanitize_client_ip,
    create_relay_session_id,
    GeoIP,
)

log = logging.getLogger(__name__)

app = FastAPI()

geoip = GeoIP(settings.GEO_IP_CITY_DATABASE) if settings.GEO_IP_CITY_DATABASE else None


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(ValueError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse("Bad request", status_code=400)


@app.get("/")
@app.get("/health")
def health(request: Request):
    return Response(content="OK", status_code=200, media_type="text/plain")


@app.get("/script.js")
async def script():
    async with httpx.AsyncClient(base_url=settings.UPSTREAM_HOST) as client:
        proxied = await client.get("/script.js")
    headers = select_headers(
        proxied.headers,
        [
            "content-type",
            "cache-control",
            "pragma",
            "expires",
            "access-control-allow-origin",
            "access-control-allow-methods",
        ],
    )
    return Response(
        content=proxied.content, status_code=proxied.status_code, headers=headers
    )


# Do NOT auto-parse body, requests come as 'text/plain' due to CORS and cross-origin json handling
@app.post("/api/rum/events")
async def collect_rum_events(request: Request, body: str = Body()):
    if not body:
        raise ValueError("Missing JSON payload")

    payload = json.loads(body)
    if not isinstance(payload, dict):
        raise ValueError("JSON payload must be an object")

    client_ip = sanitize_client_ip(
        request.headers.get("X-Real-Ip")
        or f"{request.client.host}:{request.client.port}"
    )

    # do geo lookup for country and city
    payload["ts"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    payload["relay_session_id"] = create_relay_session_id(
        client_ip, settings.SECRET_SALT
    )

    if geoip:
        try:
            payload["country_code"] = geoip.lookup_country_code(client_ip)
            payload["city_name"] = geoip.lookup_city_name(client_ip)
        except Exception as e:
            log.warning(f"Failed to lookup geoip for {client_ip}: {e}")

    upstream_url = f"/api/rum/events{'?debug=1' if settings.DRY_MODE else ''}"

    async with httpx.AsyncClient(base_url=settings.UPSTREAM_HOST) as client:
        proxied = await client.post(
            upstream_url,
            content=json.dumps(payload),
            headers={
                "Content-Type": "text/plain",
                "Origin": request.headers.get("Origin") or "cronitor-rum-relay",
            },
        )

    headers = select_headers(
        proxied.headers,
        [
            "content-type",
            "cache-control",
            "pragma",
            "expires",
            "access-control-allow-origin",
            "access-control-allow-methods",
        ],
    )

    return Response(
        content=proxied.content, status_code=proxied.status_code, headers=headers
    )
