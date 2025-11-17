import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function PatientResult() {
  const { appointmentId } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchResult();
  }, [appointmentId]);

  const fetchResult = async () => {
    try {
      setLoading(true);
      setError('');
      
      const response = await axios.get(
        `${API_BASE_URL}/api/v1/patient/result/${appointmentId}`
      );
      
      console.log('Result response:', response.data);
      setResult(response.data);
      
    } catch (err) {
      console.error('Error fetching result:', err);
      
      // Check if it's a 404 (results not ready yet)
      if (err.response?.status === 404) {
        setError('not_ready');
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Failed to load consultation results');
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your results...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate('/')}
            className="flex items-center text-blue-600 hover:text-blue-700 mb-4"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Home
          </button>
          <h1 className="text-3xl font-bold text-gray-800">Consultation Results</h1>
          <p className="text-gray-600">Appointment ID: {appointmentId}</p>
        </div>

        {/* Error or Not Ready State */}
        {error && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <div className="flex items-start">
              <svg className="w-8 h-8 text-yellow-600 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <h3 className="text-lg font-semibold text-yellow-900 mb-2">
                  Results Not Ready Yet
                </h3>
                {error === 'not_ready' ? (
                  <p className="text-yellow-800 mb-4">
                    Your doctor is still reviewing your data. Please check back later.
                  </p>
                ) : (
                  <p className="text-yellow-800 mb-4">{error}</p>
                )}
                <button
                  onClick={fetchResult}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Refresh
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Success - Show Results */}
        {result && !error && (
          <div className="space-y-6">
            {/* Status Banner */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-6">
              <div className="flex items-center text-green-700">
                <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                  <h3 className="font-semibold text-lg">Consultation Complete</h3>
                  <p className="text-sm">Reviewed by {result.doctor_name || 'Dr. Smith'}</p>
                </div>
              </div>
            </div>

            {/* Doctor's Notes */}
            {result.doctor_notes && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <svg className="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Doctor's Notes
                </h2>
                <p className="text-gray-700 whitespace-pre-wrap">{result.doctor_notes}</p>
              </div>
            )}

            {/* AI Analysis Results */}
            {result.ai_analysis && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                  <svg className="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  AI-Assisted Analysis
                </h2>

                <div className="space-y-4">
                  {/* Risk Score */}
                  {result.ai_analysis.risk_score && (
                    <div className="border-l-4 border-blue-500 pl-4">
                      <h3 className="font-semibold text-gray-700 mb-1">Risk Assessment</h3>
                      <p className="text-2xl font-bold text-blue-600">
                        {result.ai_analysis.risk_score}/10
                      </p>
                    </div>
                  )}

                  {/* Primary Concerns */}
                  {result.ai_analysis.primary_concerns && (
                    <div className="border-l-4 border-orange-500 pl-4">
                      <h3 className="font-semibold text-gray-700 mb-2">Primary Concerns</h3>
                      <ul className="list-disc list-inside space-y-1 text-gray-600">
                        {Array.isArray(result.ai_analysis.primary_concerns) ? (
                          result.ai_analysis.primary_concerns.map((concern, idx) => (
                            <li key={idx}>{concern}</li>
                          ))
                        ) : (
                          <li>{result.ai_analysis.primary_concerns}</li>
                        )}
                      </ul>
                    </div>
                  )}

                  {/* Recommendations */}
                  {result.ai_analysis.treatment_recommendations && (
                    <div className="border-l-4 border-green-500 pl-4">
                      <h3 className="font-semibold text-gray-700 mb-2">Recommendations</h3>
                      <ul className="list-disc list-inside space-y-1 text-gray-600">
                        {Array.isArray(result.ai_analysis.treatment_recommendations) ? (
                          result.ai_analysis.treatment_recommendations.map((rec, idx) => (
                            <li key={idx}>{rec}</li>
                          ))
                        ) : (
                          <li>{result.ai_analysis.treatment_recommendations}</li>
                        )}
                      </ul>
                    </div>
                  )}

                  {/* Clinical Summary */}
                  {result.ai_analysis.clinical_summary && (
                    <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                      <h3 className="font-semibold text-gray-700 mb-2">Clinical Summary</h3>
                      <p className="text-gray-600">{result.ai_analysis.clinical_summary}</p>
                    </div>
                  )}

                  {/* Show raw data for debugging (optional) */}
                  <details className="mt-4">
                    <summary className="cursor-pointer text-sm text-gray-500 hover:text-gray-700">
                      View Complete Analysis
                    </summary>
                    <pre className="mt-2 p-4 bg-gray-100 rounded text-xs overflow-auto">
                      {JSON.stringify(result.ai_analysis, null, 2)}
                    </pre>
                  </details>
                </div>
              </div>
            )}

            {/* No AI Analysis */}
            {!result.ai_analysis && (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
                <p className="text-gray-600">
                  Your consultation has been completed. Please contact your doctor if you have any questions.
                </p>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button
                onClick={() => navigate('/')}
                className="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 font-medium"
              >
                Back to Home
              </button>
              <button
                onClick={() => window.print()}
                className="flex-1 bg-gray-600 text-white py-3 rounded-lg hover:bg-gray-700 font-medium"
              >
                Print Results
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
