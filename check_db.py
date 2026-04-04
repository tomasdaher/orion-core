import sqlite3

conn = sqlite3.connect("storage/executions/orion.db")
cursor = conn.cursor()

print("\n📊 TABLAS EN LA DB:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    print("-", table[0])

print("\n👤 USUARIOS:")

try:
    cursor.execute("SELECT * FROM users LIMIT 10;")
    users = cursor.fetchall()

    if not users:
        print("⚠️ No hay usuarios guardados")
    else:
        for user in users:
            print(user)

except Exception as e:
    print("❌ Error leyendo users:", e)

conn.close()