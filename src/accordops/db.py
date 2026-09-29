import psycopg
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv

load_dotenv()
# Connectinon


def get_connection():
    conn = psycopg.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="localhost",
        port=5433,
    )
    register_vector(conn)
    return conn


# Ajouter
def add_policy(conn, category: str, max_amount: float):
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO policy (category, max_amount) VALUES(%s,%s)",
            (category, max_amount),
        )


def add_expense(conn, category: str, amount: float):
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO expenses (category, amount) VALUES(%s,%s) RETURNING id",
            (category, amount),
        )
        row = cursor.fetchone()
        return row[0]


def add_document_chunk(conn, category, source, content, embedding):
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO document_chunks(category,source,content,embedding) VALUES(%s,%s,%s,%s) RETURNING id",
            (category, source, content, embedding),
        )
        row = cursor.fetchone()
        return row[0]


# Modifier


def update_expense_amount(conn, id: int, new_amount: float):
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE expenses SET amount = %s WHERE id = %s", (new_amount, id)
        )


def update_policy(conn, id: int, category: str, new_amount: float):
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE policy SET max_amount = %s, category = %s WHERE id = %s",
            (new_amount, category, id),
        )


# SUPPRIMER


def delete_expense(conn, id: int):

    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM expenses WHERE id = %s", (id,))


# LIRE


def get_policies(conn):
    with conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SELECT * FROM policy;")
        policy = cursor.fetchall()
        return policy


def get_expenses(conn):
    with conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SELECT * FROM expenses;")
        expenses = cursor.fetchall()
        return expenses


def get_expense_by_id(conn, id):
    with conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SELECT * FROM expenses WHERE id = %s", (id,))
        expense = cursor.fetchone()
        return expense


def get_policy_by_id(conn, id):
    with conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SELECT * FROM policy WHERE id =%s", (id,))
        policy = cursor.fetchone()
        return policy


def get_policy_by_category(conn, category):
    with conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute("SELECT * FROM policy WHERE category =%s", (category,))
        policy = cursor.fetchone()
        return policy


def search_similar_chunks(conn, query_embedding, limit=3):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT category, source, content, embedding <=> %s::vector AS distance FROM document_chunks ORDER BY distance LIMIT %s",
            (query_embedding, limit),
        )
        chunks = cursor.fetchall()
        return chunks
