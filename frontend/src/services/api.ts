import axios from 'axios';
import type {
  Expense,
  ExpenseCreate,
  ExpenseUpdate,
  Category,
  ReceiptOCRResult,
  SpendingSummary,
  SpendingTrends,
  ExpenseFilters
} from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const expenseAPI = {
  // Expenses
  listExpenses: async (filters?: ExpenseFilters): Promise<Expense[]> => {
    const response = await api.get('/api/expenses', { params: filters });
    return response.data;
  },

  createExpense: async (expense: ExpenseCreate): Promise<Expense> => {
    const response = await api.post('/api/expenses', expense);
    return response.data;
  },

  getExpense: async (id: number): Promise<Expense> => {
    const response = await api.get(`/api/expenses/${id}`);
    return response.data;
  },

  updateExpense: async (id: number, expense: ExpenseUpdate): Promise<Expense> => {
    const response = await api.put(`/api/expenses/${id}`, expense);
    return response.data;
  },

  deleteExpense: async (id: number): Promise<void> => {
    await api.delete(`/api/expenses/${id}`);
  },

  uploadReceipt: async (file: File): Promise<ReceiptOCRResult> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/api/expenses/upload-receipt', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  exportExpenses: async (startDate?: string, endDate?: string): Promise<Blob> => {
    const response = await api.get('/api/expenses/export', {
      params: { start_date: startDate, end_date: endDate },
      responseType: 'blob',
    });
    return response.data;
  },

  // Categories
  listCategories: async (): Promise<Category[]> => {
    const response = await api.get('/api/categories');
    return response.data;
  },

  // Analytics
  getSpendingSummary: async (startDate?: string, endDate?: string): Promise<SpendingSummary> => {
    const response = await api.get('/api/analytics/summary', {
      params: { start_date: startDate, end_date: endDate },
    });
    return response.data;
  },

  getSpendingTrends: async (period: string = 'monthly', months: number = 6): Promise<SpendingTrends> => {
    const response = await api.get('/api/analytics/trends', {
      params: { period, months },
    });
    return response.data;
  },
};

export default api;
