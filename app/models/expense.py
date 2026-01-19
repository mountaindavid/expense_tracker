from pydantic import BaseModel, Field, field_validator
import datetime
from decimal import Decimal
from typing import Optional


class ExpenseBase(BaseModel):
    """Base model for an expense"""

    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    category: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    date: datetime.date

    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
        if v > datetime.date.today():
            raise ValueError("Date cannot be in the future")
        return v


class ExpenseCreate(ExpenseBase):
    """Request model for creating a new expense"""

    pass


class ExpenseResponse(ExpenseBase):
    """Response model for a single expense"""

    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ExpenseUpdate(BaseModel):
    """For partial updates - all optional"""

    amount: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    date: Optional[datetime.date] = None

    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
        if v is not None and v > datetime.date.today():
            raise ValueError("Date cannot be in the future")
        return v
