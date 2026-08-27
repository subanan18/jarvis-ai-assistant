from __future__ import annotations

import asyncio
from collections import defaultdict
from uuid import uuid4

from fastapi import WebSocket

from .models import RealtimeEvent


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[str, WebSocket] = {}
        self._rooms: dict[str, set[str]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, room: str = "default") -> str:
        await websocket.accept()
        client_id = str(uuid4())
        async with self._lock:
            self._connections[client_id] = websocket
            self._rooms[room].add(client_id)
        return client_id

    async def disconnect(self, client_id: str, room: str = "default") -> None:
        async with self._lock:
            self._connections.pop(client_id, None)
            if room in self._rooms:
                self._rooms[room].discard(client_id)
                if not self._rooms[room]:
                    self._rooms.pop(room, None)

    async def send(self, client_id: str, event: RealtimeEvent) -> None:
        websocket = self._connections.get(client_id)
        if websocket is not None:
            await websocket.send_json(event.model_dump(mode="json"))

    async def broadcast(self, event: RealtimeEvent, room: str = "default") -> None:
        client_ids = list(self._rooms.get(room, set()))
        stale: list[str] = []
        for client_id in client_ids:
            websocket = self._connections.get(client_id)
            if websocket is None:
                continue
            try:
                await websocket.send_json(event.model_dump(mode="json"))
            except Exception:
                stale.append(client_id)

        for client_id in stale:
            await self.disconnect(client_id, room)

    @property
    def active_connections(self) -> int:
        return len(self._connections)


manager = ConnectionManager()
