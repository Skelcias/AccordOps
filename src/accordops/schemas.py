from pydantic import BaseModel, Field
from decimal import Decimal


class ExpenseCreate(BaseModel):
    category: str
    amount: Decimal = Field(ge=0)


class ExpenseUpdate(BaseModel):
    amount: Decimal | None = None


class PolicyCreate(BaseModel):
    category: str
    max_amount: Decimal = Field(ge=0)


class PolicyUpdate(BaseModel):
    category: str | None = None
    max_amount: Decimal | None = Field(ge=0)


class TicketExpense(BaseModel):
    merchant: str | None = None
    date: str | None = None
    amount: Decimal | None = Field(default=None, ge=0)
    category: str | None = None


class TicketExpenseLLM(BaseModel):
    merchant: str | None = None
    date: str | None = None
    amount: float | None = Field(default=None, ge=0)
    category: str | None = None
