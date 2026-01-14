// Type definitions matching the backend schemas

export interface Expense {
  id: number;
  merchant: string;
  amount: number;
  category: string;
  date: string; // ISO date string
  notes?: string;
  receipt_url?: string;
  created_at: string;
  updated_at?: string;
}

export interface ExpenseCreate {
  merchant: string;
  amount: number;
  category: string;
  date: string; // ISO date string
  notes?: string;
}

export interface ExpenseUpdate {
  merchant?: string;
  amount?: number;
  category?: string;
  date?: string;
  notes?: string;
}

export interface Category {
  id: string;
  name: string;
  icon: string;
  color: string;
}

export interface ReceiptOCRResult {
  expense: Expense;
  confidence: number;
  raw_text: string;
}

export interface SpendingByCategory {
  category: string;
  amount: number;
  percentage: number;
  count: number;
}

export interface SpendingSummary {
  total: number;
  by_category: SpendingByCategory[];
  period: {
    start_date: string;
    end_date: string;
  };
}

export interface TrendDataPoint {
  date: string;
  amount: number;
  count: number;
}

export interface SpendingTrends {
  period: string;
  data: TrendDataPoint[];
}

export interface ExpenseFilters {
  category?: string;
  start_date?: string;
  end_date?: string;
  min_amount?: number;
  max_amount?: number;
  search?: string;
}