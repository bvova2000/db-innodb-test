from flask import Flask
import mysql.connector
from faker import Faker
import random
from datetime import date

app = Flask(__name__)
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
    return fake.name(), fake.email(), date(year, month, day)

@app.route('/insert_user', methods=['GET'])  # 💥 теперь это GET
def insert_user():
    name, email, dob = generate_user()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, date_of_birth) VALUES (%s, %s, %s)",
        (name, email, dob)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return "User inserted via GET", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)
