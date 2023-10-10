import psycopg2
from config import DATABASE_CONFIG

conn = psycopg2.connect(
    host=DATABASE_CONFIG["host"],
    port=DATABASE_CONFIG["port"],
    user=DATABASE_CONFIG["user"],
    password=DATABASE_CONFIG["password"],
)

cur = conn.cursor()

insert_query = """
DELETE FROM products
WHERE (product_name, ctid) NOT IN (
    SELECT product_name, MIN(ctid) as min_ctid
    FROM products
    GROUP BY product_name)
    """

cur.execute(insert_query)

conn.commit()
cur.close()
conn.close()
