"""Chat session management, history storage, editing/regeneration, and export."""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import uuid

from .config import DEFAULT_WORKSPACE, init_workspace


@dataclass
class Message:
    """Single message inside a conversation."""

    role: str  # "system", "user", "assistant", "tool"
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class ChatSession:
    """Represents a single chat session and its metadata."""

    id: str
    title: str
    system_prompt: str
    messages: List[Message] = field(default_factory=list)
    pinned: bool = False
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def touch(self) -> None:
        """Update the last-modified timestamp."""
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_model_messages(self) -> List[Dict[str, Any]]:
        """Format system prompt and messages for inference backends."""
        formatted: List[Dict[str, Any]] = []
        if self.system_prompt:
            formatted.append({"role": "system", "content": self.system_prompt})
        for msg in self.messages:
            item: Dict[str, Any] = {"role": msg.role, "content": msg.content}
            if msg.name:
                item["name"] = msg.name
            if msg.tool_call_id:
                item["tool_call_id"] = msg.tool_call_id
            formatted.append(item)
        return formatted


class SessionManager:
    """Manages local persistence, search, editing, and exports for chat sessions."""

    def __init__(self, workspace: Path = DEFAULT_WORKSPACE) -> None:
        self.dirs = init_workspace(workspace)
        self.sessions_dir = self.dirs["sessions"]
        self.exports_dir = self.dirs["exports"]

    def _session_path(self, session_id: str) -> Path:
        return self.sessions_dir / f"{session_id}.json"

    def create_session(self, title: str, system_prompt: str) -> ChatSession:
        """Create and save a new chat session."""
        session = ChatSession(
            id=str(uuid.uuid4())[:8],
            title=title,
            system_prompt=system_prompt,
        )
        self.save_session(session)
        return session

    def save_session(self, session: ChatSession) -> None:
        """Write a session to disk."""
        session.touch()
        path = self._session_path(session.id)
        path.write_text(
            json.dumps(asdict(session), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def load_session(self, session_id: str) -> ChatSession:
        """Load a session by ID."""
        path = self._session_path(session_id)
        data = json.loads(path.read_text(encoding="utf-8"))
        msgs = [Message(**m) for m in data.pop("messages", [])]
        return ChatSession(**data, messages=msgs)

    def list_sessions(self) -> List[ChatSession]:
        """Return all saved sessions, with pinned chats first."""
        sessions = [
            self.load_session(p.stem) for p in sorted(self.sessions_dir.glob("*.json"))
        ]
        sessions.sort(key=lambda s: (not s.pinned, s.updated_at), reverse=True)
        return sessions

    def search_sessions(self, query: str) -> List[ChatSession]:
        """Search sessions by title or message text."""
        q = query.lower().strip()
        results: List[ChatSession] = []
        for session in self.list_sessions():
            in_title = q in session.title.lower()
            in_msgs = any(q in m.content.lower() for m in session.messages)
            if in_title or in_msgs:
                results.append(session)
        return results

    def delete_session(self, session_id: str) -> bool:
        """Delete a session file if it exists."""
        path = self._session_path(session_id)
        if path.exists():
            path.unlink()
            return True
        return False

    def edit_message(
        self, session: ChatSession, index: int, new_content: str, truncate_after: bool = True
    ) -> ChatSession:
        """Edit an existing message and optionally truncate subsequent turns before regenerating."""
        if index < 0 or index >= len(session.messages):
            raise IndexError("Message index out of range.")
        session.messages[index].content = new_content
        if truncate_after:
            session.messages = session.messages[: index + 1]
        self.save_session(session)
        return session

    def export_json(self, session: ChatSession) -> Path:
        """Export a session as JSON."""
        out_path = self.exports_dir / f"{session.id}_{session.title[:24].replace(' ', '_')}.json"
        out_path.write_text(
            json.dumps(asdict(session), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return out_path

    def export_markdown(self, session: ChatSession) -> Path:
        """Export a session as a readable Markdown document."""
        lines = [
            f"# {session.title}",
            "",
            f"- **Session ID:** `{session.id}`",
            f"- **Updated:** {session.updated_at}",
            f"- **System Prompt:** {session.system_prompt}",
            "",
            "---",
            "",
        ]
        for msg in session.messages:
            header = f"### {msg.role.capitalize()}"
            if msg.name:
                header += f" (`{msg.name}`)"
            lines.append(header)
            lines.append("")
            lines.append(msg.content)
            lines.append("")
        out_path = self.exports_dir / f"{session.id}_{session.title[:24].replace(' ', '_')}.md"
        out_path.write_text("\n".join(lines), encoding="utf-8")
        return out_path
