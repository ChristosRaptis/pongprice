import psycopg2
import json
<<<<<<< HEAD
from dotenv import load_dotenv
import os


load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(
    host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password
)


=======

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="1234", port=5432
)

>>>>>>> 97252e9 (modify json)
cur = conn.cursor()

with open("data/bol_products.json", "r") as f:
    data = json.load(f)

data = data[0]

<<<<<<< HEAD

for item in data:
    if item != None:
        print(item.get("url"))
        # cur.execute("INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s);",
        #     (item.get("url"), item.get("product_name"), item.get("product_price")))

print(len(data))
# conn.commit()
=======
for item in data:
        
    cur.execute(
        "INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s);",
        (item.get("url"), item.get("product_name"), item.get("product_price")),
    )

conn.commit()
>>>>>>> 97252e9 (modify json)
cur.close()
conn.close()
