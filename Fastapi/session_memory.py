import uuid

class SessionStore:
    def __init__(self):
        self.sessions = {}

    def create_session(self, data: dict) -> str:
        sid = str(uuid.uuid4())
        self.sessions[sid] = data
        return sid

    def get(self, sid: str):
        return self.sessions.get(sid)

    def update(self, sid: str, updates: dict):
        if sid in self.sessions:
            self.sessions[sid].update(updates)

# Global instance (import this in main.py)
session_store = SessionStore()
