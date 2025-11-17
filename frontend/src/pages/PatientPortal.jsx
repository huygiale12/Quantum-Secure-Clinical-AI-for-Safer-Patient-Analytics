import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, ArrowLeft, Send, CheckCircle2 } from 'lucide-react';
import { patientAPI } from '../services/api';

const PatientPortal = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [appointmentId, setAppointmentId] = useState(null);
  
  const [formData, setFormData] = useState({
    age: '',
    gender: 'male',
    chief_complaint: '',
    medical_history: '',
    current_medications: '',
    allergies: '',
    symptoms: '',
    symptom_duration: '',
    doctor_id: '11111111-1111-1111-1111-111111111111', // Dr. Sarah Chen
  });

  const [labData, setLabData] = useState({
    glucose: '',
    hba1c: '',
    cholesterol: '',
    triglycerides: '',
    hdl: '',
    ldl: '',
    blood_pressure: '',
    bmi: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleLabChange = (e) => {
    setLabData({ ...labData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Convert comma-separated strings to arrays
      const intakeData = {
        age: parseInt(formData.age),
        gender: formData.gender,
        chief_complaint: formData.chief_complaint,
        medical_history: formData.medical_history.split(',').map(s => s.trim()).filter(Boolean),
        current_medications: formData.current_medications.split(',').map(s => s.trim()).filter(Boolean),
        allergies: formData.allergies.split(',').map(s => s.trim()).filter(Boolean),
        symptoms: formData.symptoms,
        symptom_duration: formData.symptom_duration,
      };

      const labResults = {
        glucose: labData.glucose ? parseFloat(labData.glucose) : null,
        hba1c: labData.hba1c ? parseFloat(labData.hba1c) : null,
        cholesterol: labData.cholesterol ? parseFloat(labData.cholesterol) : null,
        triglycerides: labData.triglycerides ? parseFloat(labData.triglycerides) : null,
        hdl: labData.hdl ? parseFloat(labData.hdl) : null,
        ldl: labData.ldl ? parseFloat(labData.ldl) : null,
        blood_pressure: labData.blood_pressure || null,
        bmi: labData.bmi ? parseFloat(labData.bmi) : null,
      };

      const appointmentTime = new Date().toISOString();

      const response = await patientAPI.submitIntake(
        intakeData,
        labResults,
        formData.doctor_id,
        appointmentTime
      );

      setAppointmentId(response.appointment_id);
      setSubmitted(true);
    } catch (error) {
      console.error('Submission error:', error);
      alert('Failed to submit data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <button onClick={() => navigate('/')} className="flex items-center text-gray-600 hover:text-gray-900">
              <ArrowLeft className="h-5 w-5 mr-2" />
              Back to Home
            </button>
          </div>
        </header>

        <div className="max-w-2xl mx-auto px-4 py-16">
          <div className="card text-center">
            <CheckCircle2 className="h-16 w-16 text-green-600 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Submission Successful!</h2>
            <p className="text-gray-600 mb-6">Your medical data has been securely encrypted and sent to your doctor.</p>
            
            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <p className="text-sm text-gray-600 mb-2">Your Appointment ID:</p>
              <p className="font-mono text-sm bg-white px-3 py-2 rounded border border-gray-200 break-all">
                {appointmentId}
              </p>
            </div>

            <p className="text-sm text-gray-500 mb-6">
              Save this ID to check your results later.
            </p>

            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <button
                onClick={() => navigate(`/patient/result/${appointmentId}`)}
                className="btn-primary"
              >
                Check Results
              </button>
              <button
                onClick={() => {
                  setSubmitted(false);
                  setAppointmentId(null);
                }}
                className="btn-secondary"
              >
                Submit Another
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

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
            <div className="flex items-center space-x-2">
              <Shield className="h-5 w-5 text-green-600" />
              <span className="text-sm text-gray-600">End-to-End Encrypted</span>
            </div>
          </div>
        </div>
      </header>

      {/* Form */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Patient Medical Intake</h1>
          <p className="text-gray-600">All data is encrypted before transmission</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Personal Information */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Personal Information</h2>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="label">Age *</label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="label">Gender *</label>
                <select name="gender" value={formData.gender} onChange={handleChange} className="input" required>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>
          </div>

          {/* Medical Information */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Medical Information</h2>
            <div className="space-y-4">
              <div>
                <label className="label">Chief Complaint *</label>
                <input
                  type="text"
                  name="chief_complaint"
                  value={formData.chief_complaint}
                  onChange={handleChange}
                  className="input"
                  placeholder="e.g., Frequent urination and increased thirst"
                  required
                />
              </div>

              <div>
                <label className="label">Current Symptoms *</label>
                <textarea
                  name="symptoms"
                  value={formData.symptoms}
                  onChange={handleChange}
                  className="input"
                  rows="3"
                  placeholder="Describe your symptoms in detail"
                  required
                />
              </div>

              <div>
                <label className="label">Symptom Duration *</label>
                <input
                  type="text"
                  name="symptom_duration"
                  value={formData.symptom_duration}
                  onChange={handleChange}
                  className="input"
                  placeholder="e.g., 2 weeks"
                  required
                />
              </div>

              <div>
                <label className="label">Medical History (comma-separated)</label>
                <input
                  type="text"
                  name="medical_history"
                  value={formData.medical_history}
                  onChange={handleChange}
                  className="input"
                  placeholder="e.g., Hypertension, Family history of diabetes"
                />
              </div>

              <div>
                <label className="label">Current Medications (comma-separated)</label>
                <input
                  type="text"
                  name="current_medications"
                  value={formData.current_medications}
                  onChange={handleChange}
                  className="input"
                  placeholder="e.g., Lisinopril 10mg, Metformin 500mg"
                />
              </div>

              <div>
                <label className="label">Allergies (comma-separated)</label>
                <input
                  type="text"
                  name="allergies"
                  value={formData.allergies}
                  onChange={handleChange}
                  className="input"
                  placeholder="e.g., Penicillin, Peanuts"
                />
              </div>
            </div>
          </div>

          {/* Lab Results */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Lab Results (Optional)</h2>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="label">Glucose (mg/dL)</label>
                <input type="number" name="glucose" value={labData.glucose} onChange={handleLabChange} className="input" step="0.1" />
              </div>
              <div>
                <label className="label">HbA1c (%)</label>
                <input type="number" name="hba1c" value={labData.hba1c} onChange={handleLabChange} className="input" step="0.1" />
              </div>
              <div>
                <label className="label">Total Cholesterol (mg/dL)</label>
                <input type="number" name="cholesterol" value={labData.cholesterol} onChange={handleLabChange} className="input" step="0.1" />
              </div>
              <div>
                <label className="label">Triglycerides (mg/dL)</label>
                <input type="number" name="triglycerides" value={labData.triglycerides} onChange={handleLabChange} className="input" step="0.1" />
              </div>
              <div>
                <label className="label">HDL (mg/dL)</label>
                <input type="number" name="hdl" value={labData.hdl} onChange={handleLabChange} className="input" step="0.1" />
              </div>
              <div>
                <label className="label">LDL (mg/dL)</label>
                <input type="number" name="ldl" value={labData.ldl} onChange={handleLabChange} className="input" step="0.1" />
              </div>
              <div>
                <label className="label">Blood Pressure</label>
                <input type="text" name="blood_pressure" value={labData.blood_pressure} onChange={handleLabChange} className="input" placeholder="e.g., 120/80" />
              </div>
              <div>
                <label className="label">BMI</label>
                <input type="number" name="bmi" value={labData.bmi} onChange={handleLabChange} className="input" step="0.1" />
              </div>
            </div>
          </div>

          {/* Submit */}
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="btn-primary flex items-center space-x-2 px-8"
            >
              {loading ? (
                <>
                  <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
                  <span>Encrypting & Submitting...</span>
                </>
              ) : (
                <>
                  <Send className="h-5 w-5" />
                  <span>Submit Securely</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PatientPortal;
