import sqlite3
from integrations.base_connector import BaseConnector


class DatabaseConnector(BaseConnector):

    name = "DatabaseConnector"

    def connect(self):

        db_path = self.config.get("db_path", "database.db")

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def read(self, query):

        self.cursor.execute(query)

        return self.cursor.fetchall()

    def write(self, query):

        self.cursor.execute(query)
        self.conn.commit()

    def execute(self, action, payload=None):

        if action == "query":
            return self.read(payload)

        if action == "write":
            return self.write(payload)