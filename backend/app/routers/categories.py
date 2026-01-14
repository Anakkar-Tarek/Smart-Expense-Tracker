from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Category
from app.schemas import CategorySchema

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=List[CategorySchema])
def list_categories(db: Session = Depends(get_db)):
    """Get all available expense categories."""
    categories = db.query(Category).all()
    return categories