from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


EventType = Literal["client.connected", "assistant.thinking", "assistant.response", "assistant.error", "ping", "pong"]


class RealtimeEvent(BaseModel):
    type: EventType
    message: str = ""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, str] = Field(default_factory=dict)


class ClientMessage(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
