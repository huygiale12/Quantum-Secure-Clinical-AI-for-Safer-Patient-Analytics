from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# ==================== PATIENT INTAKE DATA ====================
class PatientIntakeData(BaseModel):
    """Patient's medical intake form (decrypted version)"""
    age: int
    gender: str
    chief_complaint: str
    medical_history: List[str]
    current_medications: List[str]
    allergies: List[str]
    symptoms: str
    symptom_duration: str

class LabResults(BaseModel):
    """Lab test results"""
    glucose: Optional[float] = None
    hba1c: Optional[float] = None
    cholesterol: Optional[float] = None
    triglycerides: Optional[float] = None
    hdl: Optional[float] = None
    ldl: Optional[float] = None
    blood_pressure: Optional[str] = None
    bmi: Optional[float] = None

# ==================== ENCRYPTED DATA MODELS ====================
class EncryptedPatientData(BaseModel):
    """Encrypted patient data for submission"""
    encrypted_intake: str = Field(..., description="Base64 encrypted intake data")
    encrypted_lab_results: str = Field(..., description="Base64 encrypted lab results")
    wrapped_key: str = Field(..., description="Wrapped encryption key")
    appointment_time: datetime
    doctor_id: UUID

class PatientSubmitResponse(BaseModel):
    """Response after patient submits data"""
    appointment_id: UUID
    status: str
    message: str

# ==================== DOCTOR MODELS ====================
class AppointmentListItem(BaseModel):
    """Appointment in doctor's list"""
    appointment_id: UUID
    patient_id: UUID
    appointment_time: datetime
    status: str
    has_ai_analysis: bool
    created_at: datetime

class DecryptedPatientRecord(BaseModel):
    """Full decrypted patient record for doctor"""
    appointment_id: UUID
    patient_id: UUID
    intake_data: PatientIntakeData
    lab_results: LabResults
    appointment_time: datetime
    status: str

# ==================== AI ANALYSIS ====================
class AIAnalysisResult(BaseModel):
    """AI-generated clinical analysis"""
    risk_score: int = Field(..., ge=0, le=100)
    primary_concerns: List[str]
    differential_diagnoses: List[str]
    recommended_tests: List[str]
    follow_up_questions: List[str]
    recommendations: List[str]
    clinical_summary: str

class DoctorAnalysisRequest(BaseModel):
    """Doctor's request for AI analysis"""
    doctor_id: UUID
    request_ai_analysis: bool = True
    doctor_notes: Optional[str] = None
    approved: bool

class ConsultationResult(BaseModel):
    """Final consultation result"""
    appointment_id: UUID
    encrypted_result: str
    wrapped_key: str
    approved_by: UUID
    approved_at: datetime
    doctor_name: str

# ==================== PATIENT RESULT ====================
class PatientResultResponse(BaseModel):
    """Patient's view of consultation results"""
    appointment_id: UUID
    encrypted_result: str
    wrapped_key: str
    approved_by_doctor: str
    approved_at: datetime
    status: str
