"""Knowledge base loader and alias resolver."""
import json
from functools import lru_cache
from pathlib import Path

KB_PATH = Path(__file__).resolve().parent.parent / "knowledge_base" / "machines.json"


@lru_cache(maxsize=1)
def load_kb() -> dict:
    with open(KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def list_machines() -> list[dict]:
    return load_kb()["machines"]


def resolve_machine(query: str) -> dict | None:
    """Resolve a free-text query (e.g. 'ac motor') to a machine record."""
    if not query:
        return None
    q = query.strip().lower()
    for m in list_machines():
        if q == m["machine_name"].lower():
            return m
        for alias in m.get("aliases", []):
            if alias.lower() in q or q in alias.lower():
                return m
    return None
