import { useState, useEffect } from 'react';
import { expenseAPI } from '../services/api';
import type { SpendingSummary } from '../types';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F'];

export default function Dashboard() {
  const [summary, setSummary] = useState<SpendingSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    try {
      const data = await expenseAPI.getSpendingSummary();
      setSummary(data);
    } catch (error) {
      console.error('Failed to load summary:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center">Loading dashboard...</div>;
  }

  if (!summary) {
    return <div className="text-center">No data available</div>;
  }

  const chartData = summary.by_category.map((item) => ({
    name: item.category,
    value: item.amount,
  }));

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white shadow-md rounded-lg p-6">
          <h3 className="text-sm font-medium text-gray-500">Total Spending</h3>
          <p className="text-3xl font-bold text-gray-900 mt-2">
            ${summary.total.toFixed(2)}
          </p>
        </div>
        
        <div className="bg-white shadow-md rounded-lg p-6">
          <h3 className="text-sm font-medium text-gray-500">Number of Expenses</h3>
          <p className="text-3xl font-bold text-gray-900 mt-2">
            {summary.by_category.reduce((sum, cat) => sum + cat.count, 0)}
          </p>
        </div>
        
        <div className="bg-white shadow-md rounded-lg p-6">
          <h3 className="text-sm font-medium text-gray-500">Top Category</h3>
          <p className="text-3xl font-bold text-gray-900 mt-2">
            {summary.by_category[0]?.category || 'N/A'}
          </p>
        </div>
      </div>

      <div className="bg-white shadow-md rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">Spending by Category</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={(entry) => `${entry.name}: $${entry.value.toFixed(2)}`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white shadow-md rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">Category Breakdown</h3>
        <div className="space-y-3">
          {summary.by_category.map((cat, index) => (
            <div key={cat.category} className="flex items-center justify-between">
              <div className="flex items-center">
                <div
                  className="w-4 h-4 rounded mr-3"
                  style={{ backgroundColor: COLORS[index % COLORS.length] }}
                />
                <span className="text-gray-700 capitalize">{cat.category}</span>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-500">{cat.count} expenses</span>
                <span className="font-semibold">${cat.amount.toFixed(2)}</span>
                <span className="text-sm text-gray-500">{cat.percentage.toFixed(1)}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
