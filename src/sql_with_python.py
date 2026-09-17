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


def add_expense(id:int,category:str,amount:float):
    with psycopg.connect(
    dbname = os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="localhost",
    port=5433
) as conn :
        with conn.cursor() as cursor:
                cursor.execute(
                     "INSERT INTO expenses (id, category, amount) VALUES(%s,%s,%s)",
                     (id,category,amount)
                )
               
def update_expense_amount(id:int,new_amount:float):
     with psycopg.connect(
         dbname = os.getenv("POSTGRES_DB"),
         user=os.getenv("POSTGRES_USER"),
         password=os.getenv("POSTGRES_PASSWORD"),
         host="localhost",
         port=5433
     ) as conn :
          with conn.cursor() as cursor:
               cursor.execute(
                    "UPDATE expenses SET amount = %s WHERE id = %s",
                    (new_amount,id)
               )
def delete_expense(id:int):
     with psycopg.connect(
              dbname = os.getenv("POSTGRES_DB"),
              user=os.getenv("POSTGRES_USER"),
              password=os.getenv("POSTGRES_PASSWORD"),
              host="localhost",
              port=5433
          ) as conn :
               with conn.cursor() as cursor:
                    cursor.execute(
                         "DELETE FROM expenses WHERE id = %s",
                         (id,)
                    )
if __name__ == "__main__":

    # answers:list = compare_policy_to_expense(policies,expenses)
    
    # for answer in answers:
    #     print(answer)
    add_expense(5,'hotel',89.0)
