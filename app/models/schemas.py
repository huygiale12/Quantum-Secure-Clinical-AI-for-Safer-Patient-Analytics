"""Pydantic models for API request/response schemas"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field


# ============================================================================
# Patient Intake Models
# ============================================================================

class PatientIntakeData(BaseModel):
    """Patient intake form data"""
    age: int
    gender: str
    chief_complaint: str
    symptoms: str
    duration: Optional[str] = None  # Accept either duration or symptom_duration
    symptom_duration: Optional[str] = None  # Legacy field
    medical_history: Any  # Can be string or list
    current_medications: Any = None  # Can be string or list
    allergies: Any = None  # Can be string or list
    
    class Config:
        extra = "allow"  # Allow extra fields
    
    @property
    def get_duration(self):
        """Get duration from either field"""
        return self.duration or self.symptom_duration or "Unknown"


class LabResults(BaseModel):
    """Laboratory test results"""
    fasting_glucose: Optional[float] = None
    hba1c: Optional[float] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    bmi: Optional[float] = None
    cholesterol_total: Optional[float] = None
    cholesterol_ldl: Optional[float] = None
    cholesterol_hdl: Optional[float] = None
    triglycerides: Optional[float] = None
    test_notes: Optional[str] = None


class EncryptedPatientData(BaseModel):
    """Encrypted patient submission"""
    encrypted_intake: Any  # Allow any type
    encrypted_lab_results: Any  # Allow any type
    wrapped_key: Any  # Allow any type
    doctor_id: Any  # Allow any type
    appointment_time: Any  # Allow any type
    
    class Config:
        extra = "allow"
        arbitrary_types_allowed = True


class AppointmentResponse(BaseModel):
    """Response after submitting patient intake"""
    appointment_id: UUID
    status: str
    message: str


# ============================================================================
# Doctor Dashboard Models
# ============================================================================

class AppointmentListItem(BaseModel):
    """Appointment list item for doctor dashboard"""
    appointment_id: UUID
    patient_id: Optional[UUID]
    appointment_time: datetime
    status: str
    has_result: bool = False


class DecryptedPatientRecord(BaseModel):
    """Decrypted patient record for doctor view"""
    appointment_id: UUID
    patient_id: Optional[str] = None  # Changed from UUID to str, can be None
    intake_data: PatientIntakeData
    lab_results: LabResults
    appointment_time: datetime
    status: str
    
    class Config:
        extra = "allow"


class DoctorAnalysisRequest(BaseModel):
    """Request for doctor analysis and approval"""
    appointment_id: UUID
    doctor_id: UUID
    request_ai_analysis: bool = True
    doctor_notes: str
    approved: bool


# ============================================================================
# AI Analysis Models
# ============================================================================

class AIAnalysisResult(BaseModel):
    """AI analysis result structure"""
    risk_score: float = Field(..., ge=0, le=10)
    primary_concerns: List[str]
    differential_diagnoses: List[str]
    recommended_tests: List[str]
    clinical_summary: str
    treatment_recommendations: List[str]
    follow_up_timeline: str


# ============================================================================
# Consultation Result Models
# ============================================================================

class ConsultationResult(BaseModel):
    """Encrypted consultation result"""
    appointment_id: UUID
    encrypted_result: str
    wrapped_key: str
    approved_by: UUID
    approved_at: datetime
    doctor_name: Optional[str] = None


class PatientResultResponse(BaseModel):
    """Patient-facing consultation result (decrypted)"""
    appointment_id: UUID
    status: str
    approved_by: UUID
    approved_at: datetime
    doctor_name: Optional[str] = None
    doctor_notes: Optional[str] = None
    ai_analysis: Optional[Dict[str, Any]] = None
