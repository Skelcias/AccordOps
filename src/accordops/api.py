from fastapi import FastAPI, HTTPException
from accordops.db import get_expenses,get_connection,get_expense_by_id,add_expense
from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    category : str
    amount : float


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

@app.post("/expenses")
async def create_expense(expense:ExpenseCreate):
    with get_connection() as conn:
        new_id = add_expense(conn,expense.category,expense.amount)
        return {
    "id": new_id,
    "category": expense.category,
    "amount": expense.amount
        }