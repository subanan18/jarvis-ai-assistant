from app.memory_store import JsonMemoryStore


def test_remember_recall_forget(tmp_path):
    store = JsonMemoryStore(tmp_path / "memory.json")
    key, value = store.remember("Favourite Colour", "Blue")

    assert key == "favourite_colour"
    assert value == "Blue"
    assert store.recall("favourite colour") == "Blue"
    assert store.forget("Favourite Colour") is True
    assert store.recall("favourite colour") is None


def test_invalid_json_returns_empty_memory(tmp_path):
    path = tmp_path / "memory.json"
    path.write_text("not-json", encoding="utf-8")
    assert JsonMemoryStore(path).load() == {}
