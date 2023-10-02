import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="",
    password="",
)

cur = conn.cursor()

# cur.execute(
#     "CREATE TABLE products (url VARCHAR(255), product_name VARCHAR(255), product_price VARCHAR(255));"
# )

data = pd.read_csv("df_products_vandeborre_V5.csv")
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
