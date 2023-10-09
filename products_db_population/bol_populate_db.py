import psycopg2
import json
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 14b8c84 (html logos)
from dotenv import load_dotenv
import os


load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

<<<<<<< HEAD
conn = psycopg2.connect(
    host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password
)


=======
=======
import string
>>>>>>> 2bb951a (populated products db and tested app)
=======

>>>>>>> ca87103 (modified files for prices)

=======
>>>>>>> 14b8c84 (html logos)
conn = psycopg2.connect(
    host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password
)

<<<<<<< HEAD
>>>>>>> 97252e9 (modify json)
=======

>>>>>>> 14b8c84 (html logos)
cur = conn.cursor()

with open("data/bol_products.json", "r") as f:
    data = json.load(f)

data = data[0]

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

for item in data:
    if item != None:
        print(item.get("url"))
        # cur.execute("INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s);",
        #     (item.get("url"), item.get("product_name"), item.get("product_price")))

print(len(data))
<<<<<<< HEAD
# conn.commit()
=======
=======
printable = set(string.printable)
def remove_non_printable_characters(s):
    return "".join(filter(lambda x: x in string.printable, s))

     
>>>>>>> 2bb951a (populated products db and tested app)
=======


   
>>>>>>> ca87103 (modified files for prices)
for item in data:
    if item != None:
        print(item.get("url"))
        # cur.execute("INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s);",
        #     (item.get("url"), item.get("product_name"), item.get("product_price")))

<<<<<<< HEAD
        cur.execute("INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s);",
            (item.get("url"), item.get("product_name"), item.get("product_price")))

conn.commit()
>>>>>>> 97252e9 (modify json)
=======
print(len(data))  
=======
>>>>>>> 14b8c84 (html logos)
# conn.commit()
>>>>>>> ca87103 (modified files for prices)
cur.close()
conn.close()
