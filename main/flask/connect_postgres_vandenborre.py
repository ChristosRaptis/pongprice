import psycopg2
import pandas as pd
from main.flask.config import DATABASE_CONFIG

conn = psycopg2.connect(
    host=DATABASE_CONFIG["host"],
    port=DATABASE_CONFIG["port"],
    user=DATABASE_CONFIG["user"],
    password=DATABASE_CONFIG["password"],
)

cur = conn.cursor()

cur.execute(
    "CREATE TABLE products (url VARCHAR(255), product_name VARCHAR(255), product_price VARCHAR(255));"
)

data = pd.read_csv("df_products_vandeborre.csv")
data = data.drop("Unnamed: 0", axis=1)
data = list(data.itertuples(index=False))

insert_query = (
    "INSERT INTO products (url, product_name, product_price) VALUES (%s, %s, %s)"
)

for row in data:
    cur.execute(insert_query, row)

conn.commit()
cur.close()
conn.close()
