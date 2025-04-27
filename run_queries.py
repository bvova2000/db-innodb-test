import time
import mysql.connector

def run_query():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="testdb"
    )
    cursor = conn.cursor()

    query = """
    SELECT * FROM users
    WHERE date_of_birth BETWEEN '1980-01-01' AND '1981-01-01'
    LIMIT 100;
    """

    start = time.time()
    cursor.execute(query)
    results = cursor.fetchall()
    end = time.time()

    print(f"Returned {len(results)} rows in {end - start:.4f} sec")
    cursor.close()
    conn.close()

run_query()
