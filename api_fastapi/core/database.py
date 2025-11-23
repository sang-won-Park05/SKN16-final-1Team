from __future__ import annotations
import datetime
import json
import secrets
from pathlib import Path
from typing import Any, Dict, List

# Base paths
BASE_DIR = Path(__file__).resolve().parent  # .../api_fastapi/core
DATA_DIR = BASE_DIR.parent / "data"         # .../api_fastapi/data
DATA_FILE = DATA_DIR / "fake_db_users.json"


class FakeDB:
    """
    Very simple file-backed store to persist users between restarts.
    Only users are persisted; other collections remain in-memory.
    """

    def __init__(self) -> None:
        self.users: Dict[str, Dict[str, Any]] = {}
        self.tokens: Dict[str, str] = {}
        self.refresh_tokens: Dict[str, str] = {}
        self.health_profiles: Dict[str, Dict[str, Any]] = {}
        self.health_history: Dict[str, List[Dict[str, Any]]] = {}
        self.conditions: Dict[str, Dict[str, Any]] = {}
        self.allergies: Dict[str, Dict[str, Any]] = {}
        self.drugs: Dict[str, Dict[str, Any]] = {}
        self.visits: Dict[str, Dict[str, Any]] = {}
        self.prescriptions: Dict[str, List[Dict[str, Any]]] = {}
        self.chat_history: Dict[str, List[Dict[str, Any]]] = {}
        self.files: Dict[str, Dict[str, Any]] = {}
        self.file_ocr_jobs: Dict[str, Dict[str, Any]] = {}
        self.stt_jobs: Dict[str, Dict[str, Any]] = {}
        self.schedules: Dict[str, Dict[str, Any]] = {}
        self.med_schedules: Dict[str, Dict[str, Any]] = {}

        print(f"[FakeDB] __file__: {__file__}", flush=True)
        print(f"[FakeDB] DATA_DIR: {DATA_DIR}", flush=True)
        print(f"[FakeDB] DATA_FILE: {DATA_FILE}", flush=True)

        self._load_users()

    def now(self) -> str:
        return datetime.datetime.utcnow().isoformat() + "Z"

    def next_id(self, prefix: str) -> str:
        return f"{prefix}_{secrets.token_hex(4)}"

    def issue_tokens(self, user_id: str) -> Dict[str, str]:
        access = secrets.token_urlsafe(24)
        refresh = secrets.token_urlsafe(24)
        self.tokens[access] = user_id
        self.refresh_tokens[refresh] = user_id
        return {"access_token": access, "refresh_token": refresh}

    def _load_users(self) -> None:
        """Load users from disk if available."""
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            print("[FakeDB] ensured data dir exists", flush=True)
        except Exception as exc:
            print(f"[FakeDB] Failed to ensure data dir: {exc}", flush=True)

        if DATA_FILE.exists():
            try:
                raw = DATA_FILE.read_text(encoding="utf-8")
                data = json.loads(raw) if raw.strip() else {}
                self.users = data.get("users", {})
                print(f"[FakeDB] Loaded users: {len(self.users)}", flush=True)
            except Exception as exc:
                print(f"[FakeDB] Failed to load users file: {exc}", flush=True)
                self.users = {}
        else:
            print("[FakeDB] No existing users file. Starting fresh.", flush=True)

    def _save_users(self) -> None:
        """Persist users to disk."""
        try:
            payload = {"users": self.users}
            DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[FakeDB] SAVE success -> {DATA_FILE}", flush=True)
        except Exception as exc:
            print(f"[FakeDB] Failed to save users file: {exc}", flush=True)

    def create_user(self, user: Dict[str, Any]) -> None:
        """Store a user and flush to disk."""
        print(f"[FakeDB] create_user called: {user}", flush=True)
        self.users[user["id"]] = user
        self._save_users()


db = FakeDB()
