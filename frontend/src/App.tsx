import { useState, useEffect } from 'react';
import { expenseAPI } from './services/api';
import type { Expense, Category } from './types';
import ExpenseForm from './components/ExpenseForm';
import ExpenseList from './components/ExpenseList';
import ReceiptUpload from './components/ReceiptUpload';
import Dashboard from './components/Dashboard';

function App() {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'expenses' | 'add'>('dashboard');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [expensesData, categoriesData] = await Promise.all([
        expenseAPI.listExpenses(),
        expenseAPI.listCategories(),
      ]);
      setExpenses(expensesData);
      setCategories(categoriesData);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExpenseAdded = () => {
    loadData();
    setActiveTab('expenses');
  };

  const handleExpenseDeleted = async (id: number) => {
    try {
      await expenseAPI.deleteExpense(id);
      loadData();
    } catch (error) {
      console.error('Failed to delete expense:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">í²° Expense Tracker</h1>
            </div>
            <div className="flex space-x-4 items-center">
              <button
                onClick={() => setActiveTab('dashboard')}
                className={`px-4 py-2 rounded-md ${
                  activeTab === 'dashboard'
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => setActiveTab('expenses')}
                className={`px-4 py-2 rounded-md ${
                  activeTab === 'expenses'
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                Expenses
              </button>
              <button
                onClick={() => setActiveTab('add')}
                className={`px-4 py-2 rounded-md ${
                  activeTab === 'add'
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                Add Expense
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'dashboard' && <Dashboard />}
        
        {activeTab === 'expenses' && (
          <ExpenseList expenses={expenses} onDelete={handleExpenseDeleted} categories={categories} />
        )}
        
        {activeTab === 'add' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <h2 className="text-xl font-semibold mb-4">Upload Receipt</h2>
              <ReceiptUpload onSuccess={handleExpenseAdded} />
            </div>
            <div>
              <h2 className="text-xl font-semibold mb-4">Manual Entry</h2>
              <ExpenseForm categories={categories} onSuccess={handleExpenseAdded} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
