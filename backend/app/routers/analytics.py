from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Optional
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from app.database import get_db
from app.models import Expense
from app.schemas import SpendingSummary, SpendingByCategory, SpendingTrends, TrendDataPoint

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/summary", response_model=SpendingSummary)
def get_spending_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get spending summary by category for a time period.
    
    If no dates provided, uses current month.
    """
    # Default to current month if no dates provided
    if not start_date:
        start_date = date.today().replace(day=1)
    if not end_date:
        end_date = date.today()
    
    # Get expenses in period
    expenses = db.query(Expense).filter(
        Expense.date >= start_date,
        Expense.date <= end_date
    ).all()
    
    # Calculate total
    total = sum(e.amount for e in expenses)
    
    # Group by category
    category_data = {}
    for expense in expenses:
        if expense.category not in category_data:
            category_data[expense.category] = {
                'amount': 0,
                'count': 0
            }
        category_data[expense.category]['amount'] += expense.amount
        category_data[expense.category]['count'] += 1
    
    # Build response
    by_category = []
    for cat, data in category_data.items():
        percentage = (data['amount'] / total * 100) if total > 0 else 0
        by_category.append(SpendingByCategory(
            category=cat,
            amount=round(data['amount'], 2),
            percentage=round(percentage, 2),
            count=data['count']
        ))
    
    # Sort by amount descending
    by_category.sort(key=lambda x: x.amount, reverse=True)
    
    return SpendingSummary(
        total=round(total, 2),
        by_category=by_category,
        period={
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    )


@router.get("/trends", response_model=SpendingTrends)
def get_spending_trends(
    period: str = Query("monthly", regex="^(daily|weekly|monthly)$"),
    months: int = Query(6, ge=1, le=24),
    db: Session = Depends(get_db)
):
    """
    Get spending trends over time.
    
    Parameters:
    - period: Aggregation period (daily, weekly, monthly)
    - months: Number of months to analyze (1-24)
    """
    end_date = date.today()
    start_date = end_date - relativedelta(months=months)
    
    # Get expenses in period
    expenses = db.query(Expense).filter(
        Expense.date >= start_date,
        Expense.date <= end_date
    ).order_by(Expense.date).all()
    
    # Aggregate based on period
    trend_data = {}
    
    if period == "daily":
        for expense in expenses:
            date_key = expense.date.isoformat()
            if date_key not in trend_data:
                trend_data[date_key] = {'amount': 0, 'count': 0}
            trend_data[date_key]['amount'] += expense.amount
            trend_data[date_key]['count'] += 1
    
    elif period == "weekly":
        for expense in expenses:
            # Get Monday of the week
            week_start = expense.date - timedelta(days=expense.date.weekday())
            date_key = week_start.isoformat()
            if date_key not in trend_data:
                trend_data[date_key] = {'amount': 0, 'count': 0}
            trend_data[date_key]['amount'] += expense.amount
            trend_data[date_key]['count'] += 1
    
    elif period == "monthly":
        for expense in expenses:
            date_key = expense.date.replace(day=1).isoformat()
            if date_key not in trend_data:
                trend_data[date_key] = {'amount': 0, 'count': 0}
            trend_data[date_key]['amount'] += expense.amount
            trend_data[date_key]['count'] += 1
    
    # Convert to list of TrendDataPoints
    data_points = [
        TrendDataPoint(
            date=date_key,
            amount=round(data['amount'], 2),
            count=data['count']
        )
        for date_key, data in sorted(trend_data.items())
    ]
    
    return SpendingTrends(
        period=period,
        data=data_points
    )