import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function DoctorRecordView() {
  const { appointmentId } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [patientRecord, setPatientRecord] = useState(null);
  const [doctorNotes, setDoctorNotes] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    fetchPatientRecord();
  }, [appointmentId]);

  const fetchPatientRecord = async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        `${API_BASE_URL}/api/v1/doctor/record/${appointmentId}`
      );
      setPatientRecord(response.data);
    } catch (err) {
      console.error('Error fetching patient record:', err);
      setError('Failed to load patient record');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!doctorNotes.trim()) {
      setError('Please add doctor notes before analyzing');
      return;
    }

    setAnalyzing(true);
    setError('');

    try {
      console.log('Sending AI analysis request...');
      const response = await axios.post(
        `${API_BASE_URL}/api/v1/doctor/record/${appointmentId}/analyze-and-approve`,
        {
          doctor_id: '11111111-1111-1111-1111-111111111111',
          request_ai_analysis: true,
          doctor_notes: doctorNotes,
          approved: true
        }
      );

      console.log('AI Analysis Response:', response.data);
      console.log('AI Analysis Object:', response.data.ai_analysis);
      setAnalysisResult(response.data);
      setShowSuccess(true);
      
      // Alert to show we got results
      if (response.data.ai_analysis) {
        console.log('✅ AI Analysis received!', response.data.ai_analysis);
      } else {
        console.warn('⚠️ No AI analysis in response');
      }
      
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.response?.data?.detail || 'Failed to analyze record');
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading patient record...</p>
        </div>
      </div>
    );
  }

  if (error && !patientRecord) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-lg max-w-md">
          <div className="text-red-600 mb-4">
            <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-800 text-center mb-4">Error Loading Record</h2>
          <p className="text-gray-600 text-center mb-6">{error}</p>
          <button
            onClick={() => navigate('/doctor')}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate('/doctor')}
            className="flex items-center text-blue-600 hover:text-blue-700 mb-4"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Dashboard
          </button>
          <h1 className="text-3xl font-bold text-gray-800">Patient Record</h1>
          <p className="text-gray-600">Appointment ID: {appointmentId}</p>
        </div>

        {/* Patient Information */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Intake Data */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <svg className="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Patient Intake
            </h2>
            <div className="space-y-3">
              <div>
                <label className="text-sm font-medium text-gray-600">Age & Gender</label>
                <p className="text-gray-800">{patientRecord?.intake_data?.age} years old, {patientRecord?.intake_data?.gender}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Chief Complaint</label>
                <p className="text-gray-800">{patientRecord?.intake_data?.chief_complaint}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Symptoms</label>
                <p className="text-gray-800">{patientRecord?.intake_data?.symptoms}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Duration</label>
                <p className="text-gray-800">{patientRecord?.intake_data?.duration}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Medical History</label>
                <p className="text-gray-800">{patientRecord?.intake_data?.medical_history}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Current Medications</label>
                <p className="text-gray-800">{patientRecord?.intake_data?.current_medications || 'None'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Allergies</label>
                <p className="text-gray-800">{patientRecord?.intake_data?.allergies || 'None'}</p>
              </div>
            </div>
          </div>

          {/* Lab Results */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <svg className="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Lab Results
            </h2>
            <div className="space-y-3">
              {patientRecord?.lab_results?.fasting_glucose && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Fasting Glucose</span>
                  <span className="font-medium">{patientRecord.lab_results.fasting_glucose} mg/dL</span>
                </div>
              )}
              {patientRecord?.lab_results?.hba1c && (
                <div className="flex justify-between">
                  <span className="text-gray-600">HbA1c</span>
                  <span className="font-medium">{patientRecord.lab_results.hba1c}%</span>
                </div>
              )}
              {patientRecord?.lab_results?.blood_pressure_systolic && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Blood Pressure</span>
                  <span className="font-medium">
                    {patientRecord.lab_results.blood_pressure_systolic}/{patientRecord.lab_results.blood_pressure_diastolic} mmHg
                  </span>
                </div>
              )}
              {patientRecord?.lab_results?.bmi && (
                <div className="flex justify-between">
                  <span className="text-gray-600">BMI</span>
                  <span className="font-medium">{patientRecord.lab_results.bmi}</span>
                </div>
              )}
              {patientRecord?.lab_results?.cholesterol_total && (
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Cholesterol</span>
                  <span className="font-medium">{patientRecord.lab_results.cholesterol_total} mg/dL</span>
                </div>
              )}
              {patientRecord?.lab_results?.cholesterol_ldl && (
                <div className="flex justify-between">
                  <span className="text-gray-600">LDL</span>
                  <span className="font-medium">{patientRecord.lab_results.cholesterol_ldl} mg/dL</span>
                </div>
              )}
              {patientRecord?.lab_results?.cholesterol_hdl && (
                <div className="flex justify-between">
                  <span className="text-gray-600">HDL</span>
                  <span className="font-medium">{patientRecord.lab_results.cholesterol_hdl} mg/dL</span>
                </div>
              )}
              {patientRecord?.lab_results?.test_notes && (
                <div>
                  <label className="text-sm font-medium text-gray-600">Notes</label>
                  <p className="text-gray-800 text-sm">{patientRecord.lab_results.test_notes}</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* AI Analysis Section */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
            <svg className="w-7 h-7 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            AI-Assisted Analysis
          </h2>

          {/* Doctor Notes */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Doctor's Notes
            </label>
            <textarea
              value={doctorNotes}
              onChange={(e) => setDoctorNotes(e.target.value)}
              placeholder="Add your clinical notes and recommendations..."
              className="w-full h-40 px-4 py-3 border-2 border-blue-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none resize-none"
              disabled={analyzing || showSuccess}
            />
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          {/* Analyze Button */}
          <button
            onClick={handleAnalyze}
            disabled={analyzing || showSuccess}
            className={`w-full py-3 px-6 rounded-lg font-medium flex items-center justify-center ${
              analyzing || showSuccess
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            }`}
          >
            {analyzing ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing with AI...
              </>
            ) : showSuccess ? (
              <>
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Analysis Complete
              </>
            ) : (
              <>
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                Analyze with AI & Approve
              </>
            )}
          </button>

          {/* Success Message */}
          {showSuccess && (
            <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center text-green-700">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="font-medium">This consultation has been completed and results sent to patient</span>
              </div>
            </div>
          )}

          {/* AI Analysis Results */}
          {analysisResult && (
            <div className="mt-6 space-y-4">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">📊 AI Analysis Results</h3>
              
              {/* Debug: Show raw data */}
              <details className="mb-4">
                <summary className="cursor-pointer text-blue-600 hover:text-blue-700">
                  View Raw Response (Debug)
                </summary>
                <pre className="mt-2 p-4 bg-gray-100 rounded text-xs overflow-auto">
                  {JSON.stringify(analysisResult, null, 2)}
                </pre>
              </details>

              {/* Show actual AI analysis if it exists */}
              {analysisResult.ai_analysis ? (
                <div className="p-6 bg-blue-50 rounded-lg border-2 border-blue-200">
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                    {JSON.stringify(analysisResult.ai_analysis, null, 2)}
                  </pre>
                </div>
              ) : (
                <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <p className="text-yellow-800">
                    ⚠️ Analysis completed but no AI results returned. Check backend logs.
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
