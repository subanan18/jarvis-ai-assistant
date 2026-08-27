# Run the realtime API

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Health check: `http://localhost:8000/health`

WebSocket endpoint: `ws://localhost:8000/ws/assistant/{session_id}`

Example client message:

```json
{"message":"open my dashboard"}
```

The current response layer is intentionally deterministic so the transport can be run without paid API keys. An LLM or LiveKit voice layer can be attached behind the same realtime event contract.
