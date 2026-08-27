import json
from pathlib import Path


class JsonMemoryStore:
    """Small JSON-backed key/value memory store for JARVIS."""

    def __init__(self, path: Path | str = "jarvis_memory.json") -> None:
        self.path = Path(path)

    @staticmethod
    def normalise_key(key: str) -> str:
        return key.strip().lower().replace(" ", "_")

    def load(self) -> dict[str, str]:
        if not self.path.exists():
            return {}

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

        return data if isinstance(data, dict) else {}

    def save(self, memory: dict[str, str]) -> None:
        self.path.write_text(
            json.dumps(memory, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

    def remember(self, key: str, value: str) -> tuple[str, str]:
        clean_key = self.normalise_key(key)
        clean_value = value.strip()
        memory = self.load()
        memory[clean_key] = clean_value
        self.save(memory)
        return clean_key, clean_value

    def recall(self, key: str) -> str | None:
        clean_key = self.normalise_key(key)
        return self.load().get(clean_key)

    def forget(self, key: str) -> bool:
        clean_key = self.normalise_key(key)
        memory = self.load()
        if clean_key not in memory:
            return False
        del memory[clean_key]
        self.save(memory)
        return True
