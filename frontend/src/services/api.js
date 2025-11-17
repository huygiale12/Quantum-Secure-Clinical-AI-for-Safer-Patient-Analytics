import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Patient API
export const patientAPI = {
  submitIntake: async (data) => {
    const response = await api.post('/api/v1/patient/submit-intake', data);
    return response.data;
  },
  
  getResult: async (appointmentId) => {
    const response = await api.get(`/api/v1/patient/result/${appointmentId}`);
    return response.data;
  },
};

// Doctor API
export const doctorAPI = {
  getAppointments: async (doctorId) => {
    const response = await api.get('/api/v1/doctor/appointments', {
      params: { doctor_id: doctorId }
    });
    return response.data;
  },
  
  getPatientRecord: async (appointmentId) => {
    const response = await api.get(`/api/v1/doctor/record/${appointmentId}`);
    return response.data;
  },
  
  analyzeAndApprove: async (appointmentId, doctorId, doctorNotes, requestAiAnalysis = true) => {
    const response = await api.post(
      `/api/v1/doctor/analyze`,
      {
        appointment_id: appointmentId,
        doctor_id: doctorId,
        doctor_notes: doctorNotes,
        request_ai_analysis: requestAiAnalysis,
        approved: true
      }
    );
    return response.data;
  },
};

export default api;
