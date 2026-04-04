import sqlite3
import json
from datetime import datetime
from pathlib import Path


class SQLiteExecutionRepository:
    def __init__(self, db_path: str = "storage/executions/orion.db"):
        self.db_path = db_path
        self._ensure_directory()
        self._initialize_database()

    def _ensure_directory(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def _initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    objective TEXT NOT NULL,
                    data TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_execution(self, state: dict):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO executions (objective, data, created_at)
                VALUES (?, ?, ?)
            """, (
                state.get("objective").name if state.get("objective") else "UNKNOWN",
                json.dumps({
                    "status": state.get("status"),
                    "execution_history": state.get("execution_history"),
                    "agents": state.get("agents_executed")
                }, default=str),
                datetime.utcnow().isoformat()
            ))

            conn.commit()

    def get_all(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM executions")
            return cursor.fetchall()

    def get_last(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM executions
                ORDER BY id DESC
                LIMIT 1
            """)
            return cursor.fetchone()

    def get_recent(self, limit: int = 5):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM executions
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()

    def get_by_objective(self, objective_name: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM executions
                WHERE objective = ?
                ORDER BY id DESC
            """, (objective_name,))
            return cursor.fetchall()