import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv


load_dotenv()
# Connectinon 

def get_connection():
    conn = psycopg.connect(
    dbname = os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="localhost",
    port=5433
)
    return conn

# Ajouter 
def add_policy(conn,category:str,max_amount:float):
        with conn.cursor() as cursor:
                cursor.execute(
                     "INSERT INTO policy (category, max_amount) VALUES(%s,%s)",
                     (category,max_amount)
                )

def add_expense(conn,category:str,amount:float):
        with conn.cursor() as cursor:
                cursor.execute(
                     "INSERT INTO expenses (category, amount) VALUES(%s,%s) RETURNING id",
                     (category,amount)
                )
                row = cursor.fetchone()
                return row[0]

# Modifier 

def update_expense_amount(conn,id:int,new_amount:float):
          with conn.cursor() as cursor:
               cursor.execute(
                    "UPDATE expenses SET amount = %s WHERE id = %s",
                    (new_amount,id)
               )

# SUPPRIMER 

def delete_expense(conn,id:int):
          
          with conn.cursor() as cursor:
                    cursor.execute(
                         "DELETE FROM expenses WHERE id = %s",
                         (id,)
                    )

# LIRE

def get_policies(conn):
        with conn.cursor(row_factory=dict_row) as cursor:
               cursor.execute(
                        "SELECT * FROM policy;"
                )        
               policy = cursor.fetchall()
               return policy

def get_expenses(conn):
        with conn.cursor(row_factory=dict_row) as cursor:
               cursor.execute(
                        "SELECT * FROM expenses;"
                )        
               expenses = cursor.fetchall()
               return expenses

def get_expense_by_id(conn,id):
        with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                        "SELECT * FROM expenses WHERE id = %s",
                        (id,)
                      
                )
                expense = cursor.fetchone()
                return expense