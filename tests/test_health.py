from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "jarvis-realtime-assistant"


def test_websocket_round_trip() -> None:
    with client.websocket_connect("/ws/assistant/test-session") as websocket:
        connected = websocket.receive_json()
        assert connected["type"] == "client.connected"

        websocket.send_json({"message": "open my dashboard"})
        thinking = websocket.receive_json()
        response = websocket.receive_json()

        assert thinking["type"] == "assistant.thinking"
        assert response["type"] == "assistant.response"
        assert "open my dashboard" in response["message"]
