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

    def save(self, execution_request, state):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Convertimos todo a string seguro para JSON
            safe_data = {
                "request_data": str(execution_request.data),
                "final_state": str(state._state)
            }

            cursor.execute("""
                INSERT INTO executions (objective, data, created_at)
                VALUES (?, ?, ?)
            """, (
                execution_request.objective.name,
                json.dumps(safe_data),
                datetime.utcnow().isoformat()
            ))

            conn.commit()
            return "sqlite://orion.db"

    def get_all(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM executions")
            return cursor.fetchall()