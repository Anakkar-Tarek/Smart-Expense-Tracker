import { useState } from 'react';
import { expenseAPI } from '../services/api';

interface Props {
  onSuccess: () => void;
}

export default function ReceiptUpload({ onSuccess }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<any>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError('');
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await expenseAPI.uploadReceipt(file);
      setResult(result);
      setFile(null);
      setTimeout(() => {
        onSuccess();
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6 space-y-4">
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
        <input
          type="file"
          accept="image/jpeg,image/png"
          onChange={handleFileChange}
          className="hidden"
          id="receipt-upload"
        />
        <label
          htmlFor="receipt-upload"
          className="cursor-pointer flex flex-col items-center"
        >
          <svg
            className="w-12 h-12 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
          <span className="mt-2 text-sm text-gray-600">
            {file ? file.name : 'Click to upload receipt'}
          </span>
          <span className="text-xs text-gray-500 mt-1">JPG or PNG (max 5MB)</span>
        </label>
      </div>

      {file && (
        <button
          onClick={handleUpload}
          disabled={loading}
          className="w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 disabled:bg-gray-400"
        >
          {loading ? 'Processing...' : 'Upload & Process'}
        </button>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-3 text-red-600 text-sm">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-green-50 border border-green-200 rounded-md p-4 space-y-2">
          <p className="font-semibold text-green-800">✓ Receipt processed successfully!</p>
          <div className="text-sm text-gray-700">
            <p><strong>Merchant:</strong> {result.expense.merchant}</p>
            <p><strong>Amount:</strong> ${result.expense.amount}</p>
            <p><strong>Category:</strong> {result.expense.category}</p>
            <p><strong>Confidence:</strong> {(result.confidence * 100).toFixed(0)}%</p>
          </div>
        </div>
      )}
    </div>
  );
}
