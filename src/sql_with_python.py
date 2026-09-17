import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv
from accordops.main import compare_policy_to_expense

### ouvrir une connection
load_dotenv()
 

with psycopg.connect(
    dbname = os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="localhost",
    port=5433
) as conn :

    with conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SELECT * FROM policy;")
        policies = cursor.fetchall()
        cursor.execute("SELECT * FROM expenses;")
        expenses = cursor.fetchall()

if __name__ == "__main__":

    answers:list = compare_policy_to_expense(policies,expenses)
    
    for answer in answers:
        print(answer)
    
