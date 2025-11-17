import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function CheckResults() {
  const navigate = useNavigate();
  const [appointmentId, setAppointmentId] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!appointmentId.trim()) {
      setError('Please enter your appointment ID');
      return;
    }

    // Navigate to results page
    navigate(`/patient/result/${appointmentId.trim()}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Back Button */}
        <button
          onClick={() => navigate('/')}
          className="flex items-center text-blue-600 hover:text-blue-700 mb-6"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Home
        </button>

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Check Your Results</h1>
            <p className="text-gray-600">Enter your appointment ID to view your consultation results</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Appointment ID Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Appointment ID
              </label>
              <input
                type="text"
                value={appointmentId}
                onChange={(e) => {
                  setAppointmentId(e.target.value);
                  setError('');
                }}
                placeholder="e.g., 1d787531-a368-49ec-aa6c-5fb42dc4b907"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-colors"
              />
              <p className="mt-2 text-sm text-gray-500">
                💡 You received this ID when you submitted your patient intake form
              </p>
            </div>

            {/* Error Message */}
            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                {error}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 font-medium transition-colors flex items-center justify-center"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              View My Results
            </button>
          </form>

          {/* Help Text */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <h3 className="font-semibold text-blue-900 mb-2">Don't have your appointment ID?</h3>
            <p className="text-sm text-blue-800">
              Your appointment ID was provided when you submitted your intake form. Please check your email or contact your doctor's office.
            </p>
          </div>
        </div>

        {/* Privacy Notice */}
        <div className="mt-6 text-center text-sm text-gray-600">
          <svg className="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          Your results are encrypted and secure
        </div>
      </div>
    </div>
  );
}
