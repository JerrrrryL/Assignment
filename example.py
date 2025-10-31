#!/usr/bin/env python3
import psycopg2
import os

print(os.getenv("USER"))
conn = psycopg2.connect(
    dbname="labor_certification",
    user=os.getenv("USER"),
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM cases limit 3;")
print(f"{cursor.fetchall()}")

cursor.close()
conn.close()
