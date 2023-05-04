import json
import os

# Used so e2e tests don't actually record events
os.environ["DRY_MODE"] = "1"
test_site_client_key = "dbcbbc3cc9e27ed8d18449f6b3391cf1"

from starlette.testclient import TestClient

from cronitor_rum_relay.api import app

client = TestClient(app)


def test_health():
    for path in {"/", "/health"}:
        response = client.get(path)
        assert response.status_code == 200
        assert response.text == "OK"


def test_script():
    response = client.get("/script.js")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/javascript"
    assert "public" in response.headers["cache-control"]


def test_collect():
    response = client.post(
        "/api/rum/events",
        json={
            "client_key": test_site_client_key,
            "event_name": "Pageview"
        },
        headers={"content-type": "text/plain"},
    )
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]

    event = json.loads(response.text)
    assert event["client_key"] == test_site_client_key
    assert event["event_name"] == "Pageview"
    assert bool(event["relay_session_id"])
