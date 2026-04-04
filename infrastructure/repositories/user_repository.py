from infrastructure.database import Database


class UserRepository:

    def __init__(self):
        self.db = Database()

    def find_by_email(self, email):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, name, email FROM users WHERE email = ?
        """, (email,))

        user = cursor.fetchone()

        conn.close()

        if user:
            return {
                "id": user[0],
                "name": user[1],
                "email": user[2]
            }

        return None

    def create_user(self, name, email):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users (name, email)
        VALUES (?, ?)
        """, (name, email))

        conn.commit()

        user_id = cursor.lastrowid

        conn.close()

        return {
            "id": user_id,
            "name": name,
            "email": email
        }

    def update_user_name(self, user_id, new_name):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE users
        SET name = ?
        WHERE id = ?
        """, (new_name, user_id))

        conn.commit()
        conn.close()

    def update_score(self, user_id, score):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE users
        SET score = ?
        WHERE id = ?
        """, (score, user_id))

        conn.commit()
        conn.close()