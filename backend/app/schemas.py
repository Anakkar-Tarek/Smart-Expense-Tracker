from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional


class ExpenseBase(BaseModel):
    """Base expense schema with common fields."""
    merchant: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
    date: date
    notes: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    """Schema for creating a new expense."""
    pass


class ExpenseUpdate(BaseModel):
    """Schema for updating an expense - all fields optional."""
    merchant: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    date: Optional[date] = None
    notes: Optional[str] = None


class Expense(ExpenseBase):
    """Schema for expense responses."""
    id: int
    receipt_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    """Schema for category responses."""
    id: str
    name: str
    icon: str
    color: str
    
    class Config:
        from_attributes = True


class ReceiptOCRResult(BaseModel):
    """Schema for OCR processing results."""
    expense: Expense
    confidence: float = Field(..., ge=0, le=1)
    raw_text: str


class SpendingByCategory(BaseModel):
    """Schema for spending breakdown by category."""
    category: str
    amount: float
    percentage: float
    count: int


class SpendingSummary(BaseModel):
    """Schema for spending summary response."""
    total: float
    by_category: list[SpendingByCategory]
    period: dict


class TrendDataPoint(BaseModel):
    """Schema for a single trend data point."""
    date: str
    amount: float
    count: int


class SpendingTrends(BaseModel):
    """Schema for spending trends response."""
    period: str
    data: list[TrendDataPoint]


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str
    detail: Optional[str] = None