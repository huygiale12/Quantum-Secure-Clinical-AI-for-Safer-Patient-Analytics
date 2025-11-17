import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Calendar, User, Brain, CheckCircle, Clock, AlertCircle } from 'lucide-react';
import { doctorAPI } from '../services/api';

const DoctorDashboard = () => {
  const navigate = useNavigate();
  const [appointments, setAppointments] = useState([]);
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [patientRecord, setPatientRecord] = useState(null);
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [doctorNotes, setDoctorNotes] = useState('');

  // For demo, using Dr. Sarah Chen
  const DOCTOR_ID = '11111111-1111-1111-1111-111111111111';

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    try {
      setLoading(true);
      const data = await doctorAPI.getAppointments(DOCTOR_ID);
      setAppointments(data);
    } catch (error) {
      console.error('Error fetching appointments:', error);
      alert('Failed to load appointments');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAppointment = async (appointment) => {
    try {
      setSelectedAppointment(appointment);
      setPatientRecord(null);
      setAiAnalysis(null);
      setLoading(true);

      const record = await doctorAPI.getPatientRecord(appointment.appointment_id);
      setPatientRecord(record);
    } catch (error) {
      console.error('Error fetching patient record:', error);
      alert('Failed to load patient record');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeAndApprove = async () => {
    if (!selectedAppointment) return;

    try {
      setAnalyzing(true);
      const result = await doctorAPI.analyzeAndApprove(
        selectedAppointment.appointment_id,
        DOCTOR_ID,
        doctorNotes,
        true
      );

      // Extract AI analysis from the encrypted result
      // In a real app, this would be properly decrypted
      alert('Analysis complete! Results saved and encrypted for patient.');
      
      // Refresh appointments to show completion
      await fetchAppointments();
      setSelectedAppointment(null);
      setPatientRecord(null);
      setDoctorNotes('');
    } catch (error) {
      console.error('Error analyzing:', error);
      alert('Failed to complete analysis');
    } finally {
      setAnalyzing(false);
    }
  };

  const getRiskColor = (score) => {
    if (score < 30) return 'text-green-600';
    if (score < 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getRiskBgColor = (score) => {
    if (score < 30) return 'bg-green-100';
    if (score < 70) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <button onClick={() => navigate('/')} className="flex items-center text-gray-600 hover:text-gray-900">
              <ArrowLeft className="h-5 w-5 mr-2" />
              Back to Home
            </button>
            <div className="flex items-center space-x-3">
              <User className="h-5 w-5 text-gray-600" />
              <span className="text-sm font-medium">Dr. Sarah Chen</span>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Doctor Dashboard</h1>
          <p className="text-gray-600">Review appointments and analyze patient data with AI assistance</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Appointments List */}
          <div className="lg:col-span-1">
            <div className="card">
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <Calendar className="h-5 w-5 mr-2" />
                Appointments
              </h2>

              {loading && appointments.length === 0 && (
                <div className="text-center py-8">
                  <div className="animate-spin h-8 w-8 border-4 border-primary-600 border-t-transparent rounded-full mx-auto"></div>
                </div>
              )}

              {appointments.length === 0 && !loading && (
                <p className="text-gray-500 text-center py-8">No appointments found</p>
              )}

              <div className="space-y-3">
                {appointments.map((apt) => (
                  <button
                    key={apt.appointment_id}
                    onClick={() => handleSelectAppointment(apt)}
                    className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                      selectedAppointment?.appointment_id === apt.appointment_id
                        ? 'border-primary-600 bg-primary-50'
                        : 'border-gray-200 hover:border-primary-300'
                    }`}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        <User className="h-4 w-4 text-gray-400" />
                        <span className="font-medium text-sm">
                          Patient {apt.patient_id ? apt.patient_id.slice(0, 8) + '...' : apt.appointment_id.slice(0, 8) + '...'}
                        </span>
                      </div>
                      {apt.status === 'completed' ? (
                        <CheckCircle className="h-4 w-4 text-green-600" />
                      ) : (
                        <Clock className="h-4 w-4 text-yellow-600" />
                      )}
                    </div>
                    <p className="text-xs text-gray-500">
                      {new Date(apt.appointment_time).toLocaleDateString()}
                    </p>
                    <div className="mt-2 flex items-center space-x-2">
                      <span className={`text-xs px-2 py-1 rounded ${
                        apt.status === 'completed' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                      }`}>
                        {apt.status}
                      </span>
                      {apt.has_result && (
                        <span className="text-xs px-2 py-1 rounded bg-blue-100 text-blue-700">
                          AI ✓
                        </span>
                      )}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Patient Record & Analysis */}
          <div className="lg:col-span-2">
            {!selectedAppointment && (
              <div className="card text-center py-16">
                <AlertCircle className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500">Select an appointment to view patient details</p>
              </div>
            )}

            {selectedAppointment && loading && (
              <div className="card text-center py-16">
                <div className="animate-spin h-12 w-12 border-4 border-primary-600 border-t-transparent rounded-full mx-auto mb-4"></div>
                <p className="text-gray-600">Loading patient record...</p>
              </div>
            )}

            {selectedAppointment && patientRecord && (
              <div className="space-y-6">
                {/* Patient Information */}
                <div className="card">
                  <h2 className="text-xl font-semibold mb-4">Patient Information</h2>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-500">Age</p>
                      <p className="font-medium">{patientRecord.intake_data.age} years</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Gender</p>
                      <p className="font-medium capitalize">{patientRecord.intake_data.gender}</p>
                    </div>
                    <div className="md:col-span-2">
                      <p className="text-sm text-gray-500">Chief Complaint</p>
                      <p className="font-medium">{patientRecord.intake_data.chief_complaint}</p>
                    </div>
                  </div>
                </div>

                {/* Symptoms */}
                <div className="card">
                  <h2 className="text-xl font-semibold mb-4">Symptoms</h2>
                  <div className="space-y-3">
                    <div>
                      <p className="text-sm text-gray-500">Description</p>
                      <p className="text-gray-900">{patientRecord.intake_data.symptoms}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Duration</p>
                      <p className="text-gray-900">{patientRecord.intake_data.duration}</p>
                    </div>
                  </div>
                </div>

                {/* Medical History */}
                <div className="card">
                  <h2 className="text-xl font-semibold mb-4">Medical History</h2>
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-gray-500 mb-2">Past Conditions</p>
                      <p className="text-gray-900">{patientRecord.intake_data.medical_history || 'None reported'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 mb-2">Current Medications</p>
                      <p className="text-gray-900">{patientRecord.intake_data.current_medications || 'None reported'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 mb-2">Allergies</p>
                      <p className="text-gray-900">{patientRecord.intake_data.allergies || 'None reported'}</p>
                    </div>
                  </div>
                </div>

                {/* Lab Results */}
                <div className="card">
                  <h2 className="text-xl font-semibold mb-4">Lab Results</h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {Object.entries(patientRecord.lab_results || {}).map(([key, value]) => (
                      value && (
                        <div key={key} className="bg-gray-50 p-3 rounded">
                          <p className="text-xs text-gray-500 uppercase">{key.replace(/_/g, ' ')}</p>
                          <p className="font-semibold text-gray-900">{value}</p>
                        </div>
                      )
                    ))}
                  </div>
                </div>

                {/* Doctor Notes & AI Analysis */}
                <div className="card">
                  <h2 className="text-xl font-semibold mb-4 flex items-center">
                    <Brain className="h-5 w-5 mr-2 text-primary-600" />
                    AI-Assisted Analysis
                  </h2>

                  <div className="space-y-4">
                    <div>
                      <label className="label">Doctor's Notes</label>
                      <textarea
                        value={doctorNotes}
                        onChange={(e) => setDoctorNotes(e.target.value)}
                        className="input"
                        rows="4"
                        placeholder="Add your clinical notes and recommendations..."
                      />
                    </div>

                    <button
                      onClick={handleAnalyzeAndApprove}
                      disabled={analyzing || selectedAppointment.status === 'completed'}
                      className="btn-primary w-full flex items-center justify-center space-x-2"
                    >
                      {analyzing ? (
                        <>
                          <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
                          <span>Analyzing with AI...</span>
                        </>
                      ) : (
                        <>
                          <Brain className="h-5 w-5" />
                          <span>Analyze with AI & Approve</span>
                        </>
                      )}
                    </button>

                    {selectedAppointment.status === 'completed' && (
                      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                        <p className="text-sm text-green-700 flex items-center">
                          <CheckCircle className="h-4 w-4 mr-2" />
                          This consultation has been completed and results sent to patient
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DoctorDashboard;
