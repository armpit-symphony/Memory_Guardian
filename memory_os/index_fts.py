"""FTS (Full-Text Search) index using SQLite FTS5."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Iterator

from memory_os.schemas import Event, EventType


class FTSIndex:
    """Full-text search index using SQLite FTS5."""

    def __init__(self, data_dir: str | Path | None = None):
        """Initialize FTS index."""
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data" / "indexes"
        self.data_dir = Path(data_dir)
        self.db_path = self.data_dir / "fts.sqlite"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the FTS database."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS events_fts USING fts5(
                id,
                timestamp,
                event_type,
                role,
                content,
                session_id,
                tokenize='porter unicode61'
            )
        """)
        conn.commit()
        conn.close()

    def index_event(self, event: Event) -> None:
        """Index a single event."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO events_fts (id, timestamp, event_type, role, content, session_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                event.id,
                event.timestamp.isoformat(),
                event.type.value,
                event.role,
                event.content,
                event.session_id
            )
        )
        conn.commit()
        conn.close()

    def index_events(self, events: Iterator[Event]) -> None:
        """Bulk index multiple events."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        data = [
            (
                e.id,
                e.timestamp.isoformat(),
                e.type.value,
                e.role,
                e.content,
                e.session_id
            )
            for e in events
        ]
        cursor.executemany(
            """INSERT INTO events_fts (id, timestamp, event_type, role, content, session_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            data
        )
        conn.commit()
        conn.close()

    def search(self, query: str, limit: int = 10, session_id: str | None = None) -> list[dict]:
        """Search the FTS index."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # FTS5 doesn't support parameterized queries in MATCH clause
        # Escape special characters and wrap in quotes
        escaped_query = query.replace('"', '""')
        
        sql = f"""
            SELECT id, timestamp, event_type, role, content, session_id,
                   bm25(events_fts) as score
            FROM events_fts
            WHERE events_fts MATCH '"{escaped_query}"'
        """
        
        if session_id:
            sql += f" AND session_id = '{session_id}'"
        
        sql += f" ORDER BY score LIMIT {limit}"
        
        cursor.execute(sql)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results

    def rebuild_from_ledger(self, ledger_path: Path) -> None:
        """Rebuild the entire FTS index from the ledger."""
        # Clear existing index
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events_fts")
        conn.commit()
        conn.close()
        
        # Re-index all events
        with open(ledger_path, "r") as f:
            for line in f:
                if line.strip():
                    event = Event.model_validate_json(line)
                    self.index_event(event)
