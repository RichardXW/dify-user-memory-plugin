import hashlib
import json

ALLOWED = {"origin_region", "residence_region", "work_region", "user_role", "default_region", "language", "default_currency", "response_preference"}


def key(user_id: str) -> str:
    return "user-memory:v1:" + hashlib.sha256(user_id.encode("utf-8")).hexdigest()


def load(storage, user_id: str) -> dict:
    raw = storage.get(key(user_id))
    if not raw:
        return {"schema_version": 1, "facts": {}}
    try:
        data = json.loads(raw.decode("utf-8"))
        return data if isinstance(data.get("facts"), dict) else {"schema_version": 1, "facts": {}}
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"schema_version": 1, "facts": {}}


def save(storage, user_id: str, data: dict) -> None:
    storage.set(key(user_id), json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
