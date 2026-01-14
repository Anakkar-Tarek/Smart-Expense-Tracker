import type { Expense, Category } from '../types';
import { format } from 'date-fns';

interface Props {
  expenses: Expense[];
  onDelete: (id: number) => void;
  categories: Category[];
}

export default function ExpenseList({ expenses, onDelete, categories }: Props) {
  const getCategoryIcon = (categoryId: string) => {
    const cat = categories.find(c => c.id === categoryId);
    return cat ? cat.icon : 'í³Œ';
  };

  if (expenses.length === 0) {
    return (
      <div className="bg-white shadow-md rounded-lg p-8 text-center text-gray-500">
        No expenses yet. Add your first expense!
      </div>
    );
  }

  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Merchant</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Notes</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {expenses.map((expense) => (
            <tr key={expense.id} className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {format(new Date(expense.date), 'MMM dd, yyyy')}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {expense.merchant}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm">
                <span className="text-lg">{getCategoryIcon(expense.category)}</span>
                <span className="ml-2 text-gray-600">{expense.category}</span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                ${expense.amount.toFixed(2)}
              </td>
              <td className="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                {expense.notes || '-'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm">
                <button
                  onClick={() => {
                    if (confirm('Delete this expense?')) {
                      onDelete(expense.id);
                    }
                  }}
                  className="text-red-600 hover:text-red-900"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
