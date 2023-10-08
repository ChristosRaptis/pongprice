import psycopg2
import json
import string

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="1234", port=5432
)

cur = conn.cursor()

with open("data/bol_products.json", "r") as f:
    data = json.load(f)

data = data[0]

printable = set(string.printable)
def remove_non_printable_characters(s):
    return "".join(filter(lambda x: x in string.printable, s))

     
for item in data:
    if item != None:
        item["product_name"] = remove_non_printable_characters(item["product_name"])

        cur.execute("INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s);",
            (item.get("url"), item.get("product_name"), item.get("product_price")))

conn.commit()
cur.close()
conn.close()
