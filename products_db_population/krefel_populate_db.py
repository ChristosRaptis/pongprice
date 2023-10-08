import psycopg2
import json
<<<<<<< HEAD
import re
from dotenv import load_dotenv
import os


def clean_price(s):
    s = (
        s.replace(" ", "")
        .replace("\xa0", "")
        .replace(".", "")
        .replace("€", "")
        .replace("\u202f", "")
        .replace("–", "")
        .replace(",", ".")
        .rstrip("0")
        .rstrip(",")
        .rstrip("-")
    )
    return float(s)


load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(
    host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password
=======

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="1234", port=5432
>>>>>>> 97252e9 (modify json)
)

cur = conn.cursor()

with open("data/krefel_product_data.json", "r") as f:
    data = json.load(f)
<<<<<<< HEAD
print(len(data))
print(data[0])
print("before")
for item in data:
    try:
        if item != None and item["product_price"] != "N/A":
            item["product_price"] = clean_price(item["product_price"])

    except:
        continue
print(data[0])
print(len(data))
for item in data:
    try:
        if item != None and item["product_price"] != "N/A":
            cur.execute(
                "INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s);",
                (item.get("url"), item.get("product_name"), item.get("product_price")),
            )
    except:
        continue
=======

for item in data:
        
    cur.execute(
        "INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s);",
        (item.get("url"), item.get("product_name"), item.get("product_price")),
    )
>>>>>>> 97252e9 (modify json)

conn.commit()
cur.close()
conn.close()
