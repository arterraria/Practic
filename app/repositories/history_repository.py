import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from app.core.config import DB_PATH


class HistoryRepository:

    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    source_file TEXT NOT NULL,
                    result_file TEXT NOT NULL,
                    bus_count INTEGER NOT NULL
                )
                """
            )

    def add(self, source_file: str, result_file: str, bus_count: int) -> int:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO requests (created_at, source_file, result_file, bus_count)
                VALUES (?, ?, ?, ?)
                """,
                (created_at, source_file, result_file, bus_count),
            )
            return int(cursor.lastrowid)

    def list_last(self, limit: int = 20) -> List[Dict]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, created_at, source_file, result_file, bus_count
                FROM requests
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]
