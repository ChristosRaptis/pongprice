import psycopg2
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

cur = conn.cursor()

insert_query = """
WITH Duplicates AS (
    SELECT product_name, ctid,
    ROW_NUMBER() OVER (PARTITION BY
        REPLACE(REPLACE(
            CASE
                WHEN product_name LIKE '%GB%' THEN 'Go'
                WHEN product_name LIKE '%GO%' THEN 'Go'
                ELSE product_name
            END, 'inch', 'pouces'), ' ', '') ORDER BY ctid) AS rnum
    FROM products
    WHERE url LIKE '%vandenborre%' -- Only apply the criteria to rows where URL includes 'vandenborre'
)
DELETE FROM products
WHERE (product_name, ctid) IN (
    SELECT product_name, ctid
    FROM Duplicates
    WHERE rnum > 1
);
"""


cur.execute(insert_query)

conn.commit()
cur.close()
conn.close()
