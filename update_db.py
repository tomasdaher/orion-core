import sqlite3

conn = sqlite3.connect("storage/executions/orion.db")
cursor = conn.cursor()

print("🧬 Updating DB schema...")

# Agregar columna score si no existe
try:
    cursor.execute("""
    ALTER TABLE users ADD COLUMN score INTEGER DEFAULT 0
    """)
    print("✅ Column 'score' added")
except Exception as e:
    print("⚠️ Column may already exist:", e)

conn.commit()
conn.close()