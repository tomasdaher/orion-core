import sqlite3

DB_PATH = "storage/executions/orion.db"

def reset_scores():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("♻️ Reseteando scores...")

    cursor.execute("UPDATE users SET score = 0")

    conn.commit()
    conn.close()

    print("✅ Scores reseteados correctamente")


if __name__ == "__main__":
    reset_scores()