from fastapi import FastAPI, HTTPException, Response, status
from accordops.db import (
    get_expenses,
    get_connection,
    get_expense_by_id,
    add_expense,
    update_expense_amount,
    delete_expense,
    get_policies,
    add_policy,
    update_policy,
    get_policy_by_id,
)
from pydantic import BaseModel
from typing import Optional


class ExpenseCreate(BaseModel):
    category: str
    amount: float


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None


app = FastAPI()


@app.get("/expenses")
async def list_expenses():
    with get_connection() as conn:
        expenses = get_expenses(conn)
        return expenses


@app.get("/expenses/{item_id}")
async def get_expense(item_id: int):
    with get_connection() as conn:
        expense = get_expense_by_id(conn, item_id)
        if expense is None:
            raise HTTPException(status_code=404, detail="Expense not found")
        return expense


@app.post("/expenses")
async def create_expense(expense: ExpenseCreate):
    with get_connection() as conn:
        new_id = add_expense(conn, expense.category, expense.amount)
        return {"id": new_id, "category": expense.category, "amount": expense.amount}


@app.patch("/expenses/{item_id}")
async def update_expense(item_id: int, expense_update: ExpenseUpdate):
    with get_connection() as conn:
        existing_expense = get_expense_by_id(conn, item_id)
        if existing_expense is None:
            raise HTTPException(status_code=404, detail="Expense not found")
        update_expense_amount(conn, item_id, expense_update.amount)
        updated_expense = get_expense_by_id(conn, item_id)
        return updated_expense


@app.delete("/expenses/{id}")
async def delete_exp(id: int):
    with get_connection() as conn:
        existing_expense = get_expense_by_id(conn, id)
        if existing_expense is None:
            raise HTTPException(status_code=404, detail="Expense not found")
        delete_expense(conn, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)


class PolicyCreate(BaseModel):
    category: str
    max_amount: float


class PolicyUpdate(BaseModel):
    category: str
    max_amount: float


@app.get("/policies")
async def list_policies():
    with get_connection() as conn:
        return get_policies(conn)


@app.get("/policies/{policy_id}")
async def get_policy(policy_id: int):
    with get_connection() as conn:
        policy = get_policy_by_id(conn, policy_id)

        if policy is None:
            raise HTTPException(
                status_code=404,
                detail="Policy not found",
            )

        return policy


@app.post("/policies")
async def create_policy(policy: PolicyCreate):
    with get_connection() as conn:
        new_id = add_policy(
            conn,
            policy.category,
            policy.max_amount,
        )

        return {
            "id": new_id,
            "category": policy.category,
            "max_amount": policy.max_amount,
        }


@app.patch("/policies/{policy_id}")
async def patch_policy(policy_id: int, policy: PolicyUpdate):
    with get_connection() as conn:
        existing_policy = get_policy_by_id(conn, policy_id)

        if existing_policy is None:
            raise HTTPException(
                status_code=404,
                detail="Policy not found",
            )

        update_policy(
            conn,
            policy_id,
            policy.category,
            policy.max_amount,
        )

        return get_policy_by_id(conn, policy_id)
