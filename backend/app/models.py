from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Expense(Base):
    """Expense model for storing individual expense records."""
    
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    merchant = Column(String(100), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    receipt_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Expense(id={self.id}, merchant='{self.merchant}', amount={self.amount})>"


class Category(Base):
    """Category model for predefined expense categories."""
    
    __tablename__ = "categories"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    icon = Column(String(10), nullable=False)
    color = Column(String(7), nullable=False)
    
    def __repr__(self):
        return f"<Category(id='{self.id}', name='{self.name}')>"


# Predefined categories
PREDEFINED_CATEGORIES = [
    {"id": "food", "name": "Food & Dining", "icon": "🍔", "color": "#FF6B6B"},
    {"id": "groceries", "name": "Groceries", "icon": "🛒", "color": "#4ECDC4"},
    {"id": "transport", "name": "Transportation", "icon": "🚗", "color": "#45B7D1"},
    {"id": "utilities", "name": "Utilities", "icon": "💡", "color": "#FFA07A"},
    {"id": "entertainment", "name": "Entertainment", "icon": "🎬", "color": "#98D8C8"},
    {"id": "healthcare", "name": "Healthcare", "icon": "🏥", "color": "#F7DC6F"},
    {"id": "shopping", "name": "Shopping", "icon": "🛍️", "color": "#BB8FCE"},
    {"id": "travel", "name": "Travel", "icon": "✈️", "color": "#85C1E2"},
    {"id": "education", "name": "Education", "icon": "📚", "color": "#F8B739"},
    {"id": "other", "name": "Other", "icon": "📌", "color": "#95A5A6"},
]


def seed_categories(db):
    """Seed the database with predefined categories."""
    for cat_data in PREDEFINED_CATEGORIES:
        existing = db.query(Category).filter(Category.id == cat_data["id"]).first()
        if not existing:
            category = Category(**cat_data)
            db.add(category)
    db.commit()