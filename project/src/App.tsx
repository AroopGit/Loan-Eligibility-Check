import React, { useState } from 'react';
import { CreditCard, Users, CheckCircle, FileText, Building2 } from 'lucide-react';
import CustomerRegistration from './components/CustomerRegistration';
import LoanEligibility from './components/LoanEligibility';
import CreateLoan from './components/CreateLoan';
import ViewLoans from './components/ViewLoans';

function App() {
  const [activeTab, setActiveTab] = useState('register');

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <Building2 className="h-8 w-8 text-indigo-600" />
                <span className="ml-2 text-xl font-bold text-gray-900">Credit System</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex space-x-4 mb-8">
          <button
            onClick={() => setActiveTab('register')}
            className={`flex items-center px-4 py-2 rounded-lg ${
              activeTab === 'register'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Users className="h-5 w-5 mr-2" />
            Register Customer
          </button>
          <button
            onClick={() => setActiveTab('eligibility')}
            className={`flex items-center px-4 py-2 rounded-lg ${
              activeTab === 'eligibility'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            <CheckCircle className="h-5 w-5 mr-2" />
            Check Eligibility
          </button>
          <button
            onClick={() => setActiveTab('create')}
            className={`flex items-center px-4 py-2 rounded-lg ${
              activeTab === 'create'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            <CreditCard className="h-5 w-5 mr-2" />
            Create Loan
          </button>
          <button
            onClick={() => setActiveTab('view')}
            className={`flex items-center px-4 py-2 rounded-lg ${
              activeTab === 'view'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            <FileText className="h-5 w-5 mr-2" />
            View Loans
          </button>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          {activeTab === 'register' && <CustomerRegistration />}
          {activeTab === 'eligibility' && <LoanEligibility />}
          {activeTab === 'create' && <CreateLoan />}
          {activeTab === 'view' && <ViewLoans />}
        </div>
      </div>
    </div>
  );
}

export default App;