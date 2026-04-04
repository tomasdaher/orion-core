import sqlite3

conn = sqlite3.connect("storage/executions/orion.db")
cursor = conn.cursor()

print("🧹 Cleaning old users...")

# Eliminar usuarios con nombre 'Unknown'
cursor.execute("""
DELETE FROM users
WHERE name = 'Unknown'
""")

deleted = cursor.rowcount

conn.commit()

print(f"✅ Deleted {deleted} old users")

# Verificar estado actual
print("\n📊 USERS ACTUALES:")

cursor.execute("SELECT * FROM users;")
users = cursor.fetchall()

for user in users:
    print(user)

conn.close()