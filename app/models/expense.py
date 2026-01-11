from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(..., ge=0)
    category: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    date: date

class ExpenseResponse(BaseModel):
    id: int
    amount: Decimal
    category: str
    description: Optional[str]
    date: date
    created_at: datetime
    updated_at: datetime

class ExpenseUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, ge=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    date: Optional[date]