# seed.py
import pandas as pd
import os
import csv
import uuid
import mysql.connector
from mysql.connector import errorcode

# Database configuration

DB_HOST = os.environ.get("DB_HOST")
DB_USER= os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT= os.environ.get("DB_PORT")
user_data_csv_path = os.environ.get("user_data_csv_path")

TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS user_data (
    user_id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL NOT NULL,
    INDEX (user_id)
)
"""

def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("[✓] Connected to MySQL server")
        return conn
    except mysql.connector.Error as err:
        print(f"[✗] Error connecting: {err}")
        exit(1)

def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"[✓] Database '{DB_NAME}' checked/created")
    except mysql.connector.Error as err:
        print(f"[✗] Failed creating database: {err}")
        exit(1)
    cursor.close()

def connect_to_prodev():
    try:
        conn = mysql.connector.connect(database=DB_NAME, DB_HOST, DB_USER, DB_PASSWORD, DB_PORT)
        print("[✓] Connected to ALX_prodev")
        return conn
    except mysql.connector.Error as err:
        print(f"[✗] Error connecting to ALX_prodev: {err}")
        exit(1)

def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(TABLE_SCHEMA)
        print("[✓] Table 'user_data' checked/created")
    except mysql.connector.Error as err:
        print(f"[✗] Failed creating table: {err}")
    cursor.close()

def insert_data(connection, data):
    cursor = connection.cursor()
    for row in data:
        name, email, age = row
        # Check if user already exists (based on email)
        cursor.execute("SELECT user_id FROM user_data WHERE email = %s", (email,))
        if cursor.fetchone():
            print(f"[→] Skipping duplicate email: {email}")
            continue
        user_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
            (user_id, name, email, age)
        )
        print(f"[+] Inserted user: {name}, {email}, {age}")
    connection.commit()
    cursor.close()

def read_csv(/Users/ikennauzodike/alx-backend-python/python-generators-0x00/user_data.csv):
    with open(/Users/ikennauzodike/alx-backend-python/python-generators-0x00/user_data.csv, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        return [row for row in reader]

if __name__ == "__main__":
    raw_conn = connect_db()
    create_database(raw_conn)
    raw_conn.close()

    db_conn = connect_to_prodev()
    create_table(db_conn)
    
    sample_data = read_csv("user_data.csv")
    insert_data(db_conn, sample_data)

    db_conn.close()
    print("[✓] Seeding complete.")
