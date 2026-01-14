from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional


class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ExpenseCreate(BaseModel):
    merchant: str = Field(..., min_length=1, max_length=200)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)  # Category NAME
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    notes: Optional[str] = None

    @field_validator('amount')
    @classmethod
    def round_amount(cls, v):
        return round(v, 2)


class ExpenseUpdate(BaseModel):
    merchant: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1)  # Category NAME
    date: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}-\d{2}$')
    notes: Optional[str] = None


class ExpenseResponse(BaseModel):
    id: int
    merchant: str
    amount: float
    category: str  # Category NAME
    date: date
    notes: Optional[str]
    receipt_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OCRResponse(BaseModel):
    merchant: Optional[str]
    amount: Optional[float]
    date: Optional[str]
    raw_text: str