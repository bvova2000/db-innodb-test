import mysql.connector
from faker import Faker
from datetime import date
import random
import time
from concurrent.futures import ThreadPoolExecutor

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

def insert_batch(batch_id, batch_size):
    conn = get_connection()
    cursor = conn.cursor()
    data = [generate_user() for _ in range(batch_size)]
    cursor.executemany(
        "INSERT INTO users (name, email, date_of_birth) VALUES (%s, %s, %s)",
        data
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Batch {batch_id} done")

# Параметры
batch_size = 5000
total_batches = 200       # 200 * 5000 = 1,000,000 записей
max_workers = 8           # Кол-во потоков

start = time.time()

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(lambda b: insert_batch(b, batch_size), range(total_batches))

end = time.time()
print(f"\n✅ Total inserted: {batch_size * total_batches}")
print(f"⏱️ Total time: {end - start:.2f} seconds")
