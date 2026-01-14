import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import csv
import io

from app.database import get_db
from app.schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse, OCRResponse
from app import crud
from app.services.ocr_service import ocr_service
from app.config import settings

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


def expense_to_response(expense) -> dict:
    return {
        "id": expense.id,
        "merchant": expense.merchant,
        "amount": expense.amount,
        "category": expense.category.name,
        "date": expense.date,
        "notes": expense.notes,
        "receipt_url": expense.receipt_url,
        "created_at": expense.created_at,
        "updated_at": expense.updated_at
    }


@router.get("", response_model=List[ExpenseResponse])
def list_expenses(
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    expenses = crud.get_expenses(db, category=category, start_date=start_date, end_date=end_date)
    return [expense_to_response(e) for e in expenses]


@router.post("", response_model=ExpenseResponse, status_code=201)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    try:
        db_expense = crud.create_expense(db, expense)
        return expense_to_response(db_expense)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = crud.get_expense(db, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense_to_response(expense)


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense_update: ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = crud.update_expense(db, expense_id, expense_update)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense_to_response(db_expense)


@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    success = crud.delete_expense(db, expense_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    return None


@router.post("/upload-receipt", response_model=OCRResponse)
async def upload_receipt(file: UploadFile = File(...), db: Session = Depends(get_db)):
    allowed_types = ["image/jpeg", "image/jpg", "image/png"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Invalid file type")
    
    contents = await file.read()
    if len(contents) > settings.max_upload_size:
        raise HTTPException(status_code=400, detail="File too large")
    
    file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(settings.upload_dir, unique_filename)

    try:
        with open(file_path, "wb") as f:
            f.write(contents)
        
        expense_data, confidence, raw_text = ocr_service.process_receipt(file_path)
        
        return OCRResponse(
            merchant=expense_data.get('merchant'),
            amount=expense_data.get('amount'),
            date=expense_data.get('date'),
            raw_text=raw_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/export", response_class=StreamingResponse)
def export_expenses(start_date: Optional[str] = None, end_date: Optional[str] = None, db: Session = Depends(get_db)):
    expenses = crud.get_expenses(db, start_date=start_date, end_date=end_date, limit=10000)
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Date', 'Merchant', 'Category', 'Amount', 'Notes'])
    
    for expense in expenses:
        writer.writerow([
            expense.id,
            expense.date,
            expense.merchant,
            expense.category.name,
            f"{expense.amount:.2f}",
            expense.notes or ''
        ])
    
    output.seek(0)
    filename = f"expenses_{datetime.now().strftime('%Y%m%d')}.csv"
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )