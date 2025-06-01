import React, { useState } from 'react';
import { FileText, Search } from 'lucide-react';

function ViewLoans() {
  const [customerId, setCustomerId] = useState('');
  const [loans, setLoans] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchLoans = async () => {
    if (!customerId) return;
    
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/api/view-loans/${customerId}`);
      const data = await res.json();
      if (res.ok) {
        setLoans(data);
        setError('');
      } else {
        setError(data.message || 'Failed to fetch loans');
        setLoans([]);
      }
    } catch (err) {
      setError('Failed to connect to server');
      setLoans([]);
    }
    setLoading(false);
  };

  return (
    <div>
      <div className="flex items-center mb-6">
        <FileText className="h-6 w-6 text-indigo-600 mr-2" />
        <h2 className="text-2xl font-bold text-gray-900">View Customer Loans</h2>
      </div>

      <div className="flex gap-4 mb-6">
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700">Customer ID</label>
          <div className="mt-1 flex rounded-md shadow-sm">
            <input
              type="number"
              value={customerId}
              onChange={(e) => setCustomerId(e.target.value)}
              className="flex-1 rounded-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
              placeholder="Enter customer ID"
            />
            <button
              onClick={fetchLoans}
              className="ml-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              <Search className="h-4 w-4 mr-2" />
              Search
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-700 rounded-md">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-center py-4">Loading...</div>
      ) : loans.length > 0 ? (
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Loan ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Loan Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Interest Rate
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Monthly Installment
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Repayments Left
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {loans.map((loan) => (
                <tr key={loan.loan_id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {loan.loan_id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ₹{loan.loan_amount.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {loan.interest_rate}%
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ₹{loan.monthly_installment.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {loan.repayments_left}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : customerId && (
        <div className="text-center py-4 text-gray-500">No loans found for this customer</div>
      )}
    </div>
  );
}

export default ViewLoans;