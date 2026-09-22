from fastapi import FastAPI, HTTPException, Response, status
from accordops.services import (
    get_expense_service,
    update_expense_service,
    delete_expense_service,
    get_policy_service,
    update_policy_service,
    ExpenseNotFoundError,
    PolicyNotFoundError,
)
from accordops.schemas import ExpenseCreate, ExpenseUpdate, PolicyCreate, PolicyUpdate
from accordops.db import (
    get_expenses,
    get_connection,
    add_expense,
    get_policies,
    add_policy,
)

app = FastAPI()


@app.get("/expenses")
async def list_expenses():
    with get_connection() as conn:
        expenses = get_expenses(conn)
        return expenses


@app.get("/expenses/{item_id}")
async def get_expense(item_id: int):
    try:
        return get_expense_service(item_id)
    except ExpenseNotFoundError:
        raise HTTPException(404)


@app.post("/expenses")
async def create_expense(expense: ExpenseCreate):
    with get_connection() as conn:
        new_id = add_expense(conn, expense.category, expense.amount)
        return {"id": new_id, "category": expense.category, "amount": expense.amount}


@app.patch("/expenses/{item_id}")
async def update_expense(item_id: int, expense_update: ExpenseUpdate):
    try:
        expense = update_expense_service(item_id, expense_update.amount)
    except ExpenseNotFoundError:
        raise HTTPException(404)
    return expense


@app.delete("/expenses/{id}")
async def delete_exp(id: int):
    try:
        delete_expense_service(id)
    except ExpenseNotFoundError:
        raise HTTPException(404)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/policies")
async def list_policies():
    with get_connection() as conn:
        return get_policies(conn)


@app.get("/policies/{policy_id}")
async def get_policy(policy_id: int):
    try:
        return get_policy_service(policy_id)
    except PolicyNotFoundError:
        raise HTTPException(404)


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
    try:
        policy = update_policy_service(
            policy_id=policy_id,
            new_category=policy.category,
            new_amount=policy.max_amount,
        )
    except PolicyNotFoundError:
        raise HTTPException(404)
    return policy
