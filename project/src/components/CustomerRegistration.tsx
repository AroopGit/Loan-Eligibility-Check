import React, { useState } from 'react';

const CustomerRegistration: React.FC = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    age: '',
    monthly_salary: '',
    phone_number: '',
  });
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    // Convert age and monthly_salary to numbers
    const customerData = {
      first_name: formData.first_name,
      last_name: formData.last_name,
      age: parseInt(formData.age),
      monthly_salary: parseInt(formData.monthly_salary),
      phone_number: formData.phone_number,
    };

    try {
      const response = await fetch('http://localhost:8000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(customerData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setSuccess(`Customer registered successfully! Customer ID: ${data.customer_id}`);
      setFormData({
        first_name: '',
        last_name: '',
        age: '',
        monthly_salary: '',
        phone_number: '',
      });
    } catch (error: any) {
      console.error('Failed to connect to server:', {
        message: error.message,
        name: error.name,
        stack: error.stack,
      });
      if (error.message.includes('Failed to fetch')) {
        setError('Failed to connect to server: Unable to reach the backend. Check if the server is running and CORS is configured.');
      } else {
        setError(error.message);
      }
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Register Customer</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">
            First Name
          </label>
          <input
            type="text"
            name="first_name"
            id="first_name"
            value={formData.first_name}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            required
          />
        </div>
        <div>
          <label htmlFor="last_name" className="block text-sm font-medium text-gray-700">
            Last Name
          </label>
          <input
            type="text"
            name="last_name"
            id="last_name"
            value={formData.last_name}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            required
          />
        </div>
        <div>
          <label htmlFor="age" className="block text-sm font-medium text-gray-700">
            Age
          </label>
          <input
            type="number"
            name="age"
            id="age"
            value={formData.age}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            required
            min="18"
          />
        </div>
        <div>
          <label htmlFor="monthly_salary" className="block text-sm font-medium text-gray-700">
            Monthly Salary
          </label>
          <input
            type="number"
            name="monthly_salary"
            id="monthly_salary"
            value={formData.monthly_salary}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            required
            min="0"
          />
        </div>
        <div>
          <label htmlFor="phone_number" className="block text-sm font-medium text-gray-700">
            Phone Number
          </label>
          <input
            type="text"
            name="phone_number"
            id="phone_number"
            value={formData.phone_number}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            required
            pattern="[0-9]{10}"
            title="Phone number must be 10 digits"
          />
        </div>
        <button
          type="submit"
          className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700"
        >
          Register
        </button>
      </form>
      {success && (
        <div className="mt-4 p-4 bg-green-100 text-green-700 rounded-md">
          {success}
        </div>
      )}
      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded-md">
          {error}
        </div>
      )}
    </div>
  );
};

export default CustomerRegistration;