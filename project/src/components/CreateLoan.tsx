import React, { useState } from 'react';
import { CreditCard } from 'lucide-react';

function CreateLoan() {
  const [formData, setFormData] = useState({
    customer_id: '',
    loan_amount: '',
    interest_rate: '',
    tenure: ''
  });
  const [response, setResponse] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/create-loan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (res.ok) {
        setResponse(data);
        setError('');
      } else {
        setError(data.message || 'Failed to create loan');
      }
    } catch (err) {
      setError('Failed to connect to server');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div>
      <div className="flex items-center mb-6">
        <CreditCard className="h-6 w-6 text-indigo-600 mr-2" />
        <h2 className="text-2xl font-bold text-gray-900">Create Loan</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Customer ID</label>
            <input
              type="number"
              name="customer_id"
              value={formData.customer_id}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Loan Amount</label>
            <input
              type="number"
              name="loan_amount"
              value={formData.loan_amount}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Interest Rate (%)</label>
            <input
              type="number"
              name="interest_rate"
              value={formData.interest_rate}
              onChange={handleChange}
              step="0.01"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Tenure (months)</label>
            <input
              type="number"
              name="tenure"
              value={formData.tenure}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              required
            />
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            Create Loan
          </button>
        </div>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-md">
          {error}
        </div>
      )}

      {response && (
        <div className="mt-4 p-4 bg-green-50 rounded-md">
          <h3 className="text-lg font-medium text-green-800">
            {response.loan_approved ? 'Loan Created Successfully' : 'Loan Not Approved'}
          </h3>
          <dl className="mt-2 grid grid-cols-2 gap-4">
            {response.loan_approved && (
              <>
                <div>
                  <dt className="text-sm font-medium text-green-600">Loan ID</dt>
                  <dd className="text-sm text-green-900">{response.loan_id}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-green-600">Monthly Installment</dt>
                  <dd className="text-sm text-green-900">₹{response.monthly_installment.toLocaleString()}</dd>
                </div>
              </>
            )}
            {!response.loan_approved && response.message && (
              <div className="col-span-2">
                <dt className="text-sm font-medium text-green-600">Message</dt>
                <dd className="text-sm text-green-900">{response.message}</dd>
              </div>
            )}
          </dl>
        </div>
      )}
    </div>
  );
}

export default CreateLoan;