from fastapi import FastAPI, HTTPException
from accordops.db import get_expenses,get_connection,get_expense_by_id

app = FastAPI()

@app.get("/expenses")
async def list_expenses():
    with get_connection() as conn:
        expenses = get_expenses(conn)
        return expenses

@app.get("/expenses/{item_id}")
async def get_expense(item_id:int):
    with get_connection() as conn:
        expense = get_expense_by_id(conn,item_id)
        if expense is None:
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )
        return expense