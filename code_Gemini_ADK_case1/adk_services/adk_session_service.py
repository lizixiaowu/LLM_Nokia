from google.adk.sessions import BaseSessionService

class ADKSessionService(BaseSessionService):
    """
    Custom session manager for ADK v1.18.0.
    Provides simple in-memory session handling.
    """

    def __init__(self):
        super().__init__()
        self.sessions = {}
        print("🧠 ADK BaseSessionService initialized.")

    # --- Required abstract methods ---
    def create_session(self, session_id: str, **kwargs):
        """Create a session and store metadata"""
        self.sessions[session_id] = {"data": kwargs, "status": "created"}
        print(f"[Session] Created: {session_id}")
        return self.sessions[session_id]

    def get_session(self, session_id: str):
        """Retrieve session info"""
        session = self.sessions.get(session_id)
        print(f"[Session] Get: {session_id} -> {session}")
        return session

    def list_sessions(self):
        """List all current session IDs"""
        ids = list(self.sessions.keys())
        print(f"[Session] Active sessions: {ids}")
        return ids

    def delete_session(self, session_id: str):
        """Delete session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            print(f"[Session] Deleted: {session_id}")
            return True
        print(f"[Session] Delete failed: {session_id} not found.")
        return False


def get_adk_session_service():
    """Return an initialized ADK session service."""
    return ADKSessionService()

