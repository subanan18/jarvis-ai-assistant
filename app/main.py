import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .models import ClientMessage, RealtimeEvent
from .realtime import manager

app = FastAPI(title="JARVIS Realtime Assistant", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, object]:
    return {
        "status": "ok",
        "service": "jarvis-realtime-assistant",
        "active_connections": manager.active_connections,
    }


async def generate_demo_response(message: str) -> str:
    """Small local response layer used until an LLM provider is configured.

    Keeping this deterministic makes the realtime transport runnable without
    exposing API keys or requiring a paid external service.
    """
    await asyncio.sleep(0.15)
    cleaned = message.strip()
    return f"JARVIS received: {cleaned}"


@app.websocket("/ws/assistant/{session_id}")
async def assistant_socket(websocket: WebSocket, session_id: str) -> None:
    room = f"session:{session_id}"
    client_id = await manager.connect(websocket, room)
    await manager.send(
        client_id,
        RealtimeEvent(
            type="client.connected",
            message="Realtime assistant session connected.",
            metadata={"session_id": session_id, "client_id": client_id},
        ),
    )

    try:
        while True:
            payload = await websocket.receive_json()
            parsed = ClientMessage.model_validate(payload)

            await manager.send(
                client_id,
                RealtimeEvent(
                    type="assistant.thinking",
                    message="Processing request",
                    metadata={"session_id": session_id},
                ),
            )

            response = await generate_demo_response(parsed.message)
            await manager.send(
                client_id,
                RealtimeEvent(
                    type="assistant.response",
                    message=response,
                    metadata={"session_id": session_id},
                ),
            )
    except WebSocketDisconnect:
        await manager.disconnect(client_id, room)
    except Exception as exc:
        await manager.send(
            client_id,
            RealtimeEvent(type="assistant.error", message=str(exc), metadata={"session_id": session_id}),
        )
        await manager.disconnect(client_id, room)
