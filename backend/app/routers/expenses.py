import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
import csv
import io

from app.database import get_db
from app.models import Expense
from app.schemas import (
    ExpenseCreate, ExpenseUpdate, Expense as ExpenseSchema,
    ReceiptOCRResult, ErrorResponse
)
from app.services.ocr_service import ocr_service
from app.config import settings

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


@router.get("", response_model=List[ExpenseSchema])
def list_expenses(
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all expenses with optional filtering.
    
    Filters:
    - category: Filter by expense category
    - start_date: Filter expenses from this date onwards
    - end_date: Filter expenses up to this date
    - min_amount: Minimum expense amount
    - max_amount: Maximum expense amount
    - search: Search in merchant name or notes
    """
    query = db.query(Expense)
    
    if category:
        query = query.filter(Expense.category == category)
    
    if start_date:
        query = query.filter(Expense.date >= start_date)
    
    if end_date:
        query = query.filter(Expense.date <= end_date)
    
    if min_amount is not None:
        query = query.filter(Expense.amount >= min_amount)
    
    if max_amount is not None:
        query = query.filter(Expense.amount <= max_amount)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Expense.merchant.ilike(search_filter)) |
            (Expense.notes.ilike(search_filter))
        )
    
    expenses = query.order_by(Expense.date.desc()).all()
    return expenses


@router.post("", response_model=ExpenseSchema, status_code=201)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):
    """Create a new expense manually."""
    db_expense = Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.get("/{expense_id}", response_model=ExpenseSchema)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific expense by ID."""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return expense


@router.put("/{expense_id}", response_model=ExpenseSchema)
def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing expense."""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    # Update only provided fields
    update_data = expense_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)
    
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=204)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):
    """Delete an expense."""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()
    return None


@router.post("/upload-receipt", response_model=ReceiptOCRResult)
async def upload_receipt(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a receipt image and extract expense data using OCR.
    
    Accepts: JPG, PNG images (max 5MB)
    Returns: Extracted expense data with confidence score
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/jpg", "image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
        )
    
    # Read file
    contents = await file.read()
    
    # Validate file size
    if len(contents) > settings.max_upload_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.max_upload_size / (1024*1024)}MB"
        )
    
    # Save file temporarily
    file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(settings.upload_dir, unique_filename)
    
    try:
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Process with OCR
        try:
            expense_data, confidence, raw_text = ocr_service.process_receipt(file_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"OCR processing failed: {str(e)}")
        
        # Create expense in database
        expense_data["receipt_url"] = f"/uploads/{unique_filename}"
        db_expense = Expense(**expense_data)
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        
        return ReceiptOCRResult(
            expense=db_expense,
            confidence=confidence,
            raw_text=raw_text
        )
        
    except HTTPException:
        # Clean up file if OCR failed
        if os.path.exists(file_path):
            os.remove(file_path)
        raise
    except Exception as e:
        # Clean up file on unexpected error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/export", response_class=StreamingResponse)
def export_expenses(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Export expenses to CSV file.
    
    Optional filters:
    - start_date: Export expenses from this date
    - end_date: Export expenses up to this date
    """
    query = db.query(Expense)
    
    if start_date:
        query = query.filter(Expense.date >= start_date)
    
    if end_date:
        query = query.filter(Expense.date <= end_date)
    
    expenses = query.order_by(Expense.date.desc()).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Date', 'Merchant', 'Category', 'Amount', 'Notes', 'Created At'])
    
    # Write data
    for expense in expenses:
        writer.writerow([
            expense.id,
            expense.date.isoformat(),
            expense.merchant,
            expense.category,
            f"{expense.amount:.2f}",
            expense.notes or '',
            expense.created_at.isoformat() if expense.created_at else ''
        ])
    
    output.seek(0)
    
    # Generate filename with date range
    filename = "expenses"
    if start_date:
        filename += f"_{start_date.isoformat()}"
    if end_date:
        filename += f"_to_{end_date.isoformat()}"
    filename += ".csv"
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )