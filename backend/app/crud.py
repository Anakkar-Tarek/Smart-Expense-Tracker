from sqlalchemy.orm import Session
from sqlalchemy import func, extract, desc
from app.models import Expense, Category
from app.schemas import ExpenseCreate, ExpenseUpdate
from typing import List, Optional
from datetime import datetime


def get_categories(db: Session) -> List[Category]:
    return db.query(Category).all()


def get_category_by_name(db: Session, name: str) -> Optional[Category]:
    return db.query(Category).filter(Category.name == name).first()


def get_category_by_id(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()


def get_expenses(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[Expense]:
    query = db.query(Expense)

    if category:
        cat = get_category_by_name(db, category)
        if cat:
            query = query.filter(Expense.category_id == cat.id)

    if start_date:
        query = query.filter(Expense.date >= start_date)

    if end_date:
        query = query.filter(Expense.date <= end_date)

    return query.order_by(desc(Expense.date)).offset(skip).limit(limit).all()


def get_expense(db: Session, expense_id: int) -> Optional[Expense]:
    return db.query(Expense).filter(Expense.id == expense_id).first()


def create_expense(db: Session, expense: ExpenseCreate, receipt_url: Optional[str] = None) -> Expense:
    category = get_category_by_name(db, expense.category)
    if not category:
        category = Category(name=expense.category)
        db.add(category)
        db.flush()

    db_expense = Expense(
        merchant=expense.merchant,
        amount=expense.amount,
        category_id=category.id,
        date=expense.date,
        notes=expense.notes,
        receipt_url=receipt_url
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def update_expense(db: Session, expense_id: int, expense: ExpenseUpdate) -> Optional[Expense]:
    db_expense = get_expense(db, expense_id)
    if not db_expense:
        return None

    update_data = expense.model_dump(exclude_unset=True)

    if 'category' in update_data:
        category = get_category_by_name(db, update_data['category'])
        if not category:
            category = Category(name=update_data['category'])
            db.add(category)
            db.flush()
        update_data['category_id'] = category.id
        del update_data['category']

    for field, value in update_data.items():
        setattr(db_expense, field, value)

    db_expense.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_expense)
    return db_expense


def delete_expense(db: Session, expense_id: int) -> bool:
    db_expense = get_expense(db, expense_id)
    if not db_expense:
        return False

    db.delete(db_expense)
    db.commit()
    return True


def get_spending_summary(
    db: Session,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    query = db.query(
        func.sum(Expense.amount).label('total'),
        func.count(Expense.id).label('count'),
        func.avg(Expense.amount).label('average')
    )

    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)

    result = query.first()

    top_category = db.query(
        Category.name,
        func.sum(Expense.amount).label('total')
    ).join(Expense).group_by(Category.name).order_by(desc('total')).first()

    return {
        'total_spending': float(result.total or 0),
        'expense_count': result.count or 0,
        'average_expense': float(result.average or 0),
        'top_category': top_category[0] if top_category else None,
        'top_category_amount': float(top_category[1]) if top_category else None
    }


def get_category_spending(
    db: Session,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    query = db.query(
        Category.name,
        func.sum(Expense.amount).label('total'),
        func.count(Expense.id).label('count')
    ).join(Expense).group_by(Category.name)

    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)

    results = query.all()
    total_spending = sum(r.total for r in results)

    return [
        {
            'category': r.name,
            'total': float(r.total),
            'count': r.count,
            'percentage': (float(r.total) / total_spending * 100) if total_spending > 0 else 0
        }
        for r in results
    ]


def get_spending_trends(
    db: Session,
    period: str = 'month',
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    if period == 'month':
        date_part = extract('month', Expense.date)
        format_str = 'month'
    elif period == 'week':
        date_part = extract('week', Expense.date)
        format_str = 'week'
    else:
        date_part = extract('day', Expense.date)
        format_str = 'day'

    query = db.query(
        date_part.label('period'),
        func.sum(Expense.amount).label('total'),
        func.count(Expense.id).label('count')
    ).group_by('period').order_by('period')

    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)

    results = query.all()

    return [
        {
            'period': f"{format_str}_{r.period}",
            'total': float(r.total),
            'count': r.count
        }
        for r in results
    ]