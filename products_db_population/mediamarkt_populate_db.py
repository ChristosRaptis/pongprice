import psycopg2
import json

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="1234", port=5432
)

cur = conn.cursor()

with open("data/mediamarkt_products.json", "r") as f:
    data = json.load(f)

cur.execute(
    "CREATE TABLE products (url VARCHAR(255), product_name TEXT, product_price VARCHAR(255));"
)

for item in data:
    cur.execute(
        "INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s);",
        (item["product_url"], item["product_name"], item["product_price"]),
    )

conn.commit()
cur.close()
conn.close()
