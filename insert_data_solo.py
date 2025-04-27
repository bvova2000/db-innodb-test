import mysql.connector
from faker import Faker
from datetime import date
import random
import time

fake = Faker()

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="testdb"
    )

def generate_user():
    year = random.randint(1960, 2005)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return (fake.name(), fake.email(), date(year, month, day))

def insert_single_row(cursor):
    user = generate_user()
    cursor.execute(
        "INSERT INTO users (name, email, date_of_birth) VALUES (%s, %s, %s)",
        user
    )

# Параметры
total_records = 10000  # Начнем с 10 тысяч записей, можно увеличить

conn = get_connection()
cursor = conn.cursor()

start = time.time()

for i in range(total_records):
    insert_single_row(cursor)
    time.sleep(0.002)  # 2 мс задержка
    conn.commit()  # ⛔️ Коммитим каждую запись отдельно

    if (i + 1) % 1000 == 0:
        print(f"Inserted {i+1} rows")

end = time.time()

cursor.close()
conn.close()

print(f"\n✅ Total inserted: {total_records}")
print(f"⏱️ Total time: {end - start:.2f} seconds")
