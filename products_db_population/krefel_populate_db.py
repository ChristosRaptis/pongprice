import psycopg2
import json

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="1234", port=5432
)

cur = conn.cursor()

with open("data/krefel_product_data.json", "r") as f:
    data = json.load(f)

for item in data:
        
    cur.execute(
        "INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s);",
        (item.get("url"), item.get("product_name"), item.get("product_price")),
    )

conn.commit()
cur.close()
conn.close()
