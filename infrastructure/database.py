import sqlite3
import os


class Database:

    def __init__(self, db_path="storage/executions/orion.db"):

        self.db_path = db_path

        # asegurar que el directorio existe
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def connect(self):
        return sqlite3.connect(self.db_path)

    def initialize(self):

        conn = self.connect()
        cursor = conn.cursor()

        # tabla users
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        conn.close()