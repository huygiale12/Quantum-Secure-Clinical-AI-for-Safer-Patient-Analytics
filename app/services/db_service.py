from uuid import UUID
from datetime import datetime
from typing import List, Optional, Dict, Any
from app.database import get_db
from app.models.schemas import (
    AppointmentListItem,
    PatientIntakeData,
    LabResults,
    DecryptedPatientRecord
)
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service for database operations"""
    
    @staticmethod
    async def create_patient() -> UUID:
        """Create a new patient record"""
        db = get_db()
        result = db.table("patients").insert({}).execute()
        return UUID(result.data[0]["patient_id"])
    
    @staticmethod
    async def create_appointment(
        patient_id: UUID,
        doctor_id: UUID,
        appointment_time: datetime
    ) -> UUID:
        """Create a new appointment"""
        db = get_db()
        result = db.table("appointments").insert({
            "patient_id": str(patient_id),
            "doctor_id": str(doctor_id),
            "appointment_time": appointment_time.isoformat(),
            "status": "pending"
        }).execute()
        return UUID(result.data[0]["appointment_id"])
    
    @staticmethod
    async def store_encrypted_record(
        appointment_id: UUID,
        encrypted_blob: str,
        wrapped_key: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Store encrypted patient record"""
        db = get_db()
        db.table("encrypted_records").insert({
            "appointment_id": str(appointment_id),
            "encrypted_blob": encrypted_blob,
            "wrapped_key": wrapped_key,
            "metadata": metadata
        }).execute()
    
    @staticmethod
    async def get_encrypted_record(appointment_id: UUID) -> Dict[str, Any]:
        """Retrieve encrypted patient record"""
        db = get_db()
        result = db.table("encrypted_records")\
            .select("*")\
            .eq("appointment_id", str(appointment_id))\
            .single()\
            .execute()
        return result.data
    
    @staticmethod
    async def get_appointment(appointment_id: UUID) -> Dict[str, Any]:
        """Get appointment details"""
        db = get_db()
        result = db.table("appointments")\
            .select("*")\
            .eq("appointment_id", str(appointment_id))\
            .single()\
            .execute()
        return result.data
    
    @staticmethod
    async def list_doctor_appointments(doctor_id: UUID) -> List[AppointmentListItem]:
        """List all appointments for a doctor"""
        db = get_db()
        
        # Get appointments
        appointments = db.table("appointments")\
            .select("*")\
            .eq("doctor_id", str(doctor_id))\
            .order("appointment_time", desc=True)\
            .execute()
        
        # Check which ones have AI analysis
        result = []
        for apt in appointments.data:
            apt_id = apt["appointment_id"]
            
            # Check if consultation result exists
            consult = db.table("consultation_results")\
                .select("result_id")\
                .eq("appointment_id", apt_id)\
                .execute()
            
            result.append(AppointmentListItem(
                appointment_id=UUID(apt["appointment_id"]),
                patient_id=UUID(apt["patient_id"]),
                appointment_time=datetime.fromisoformat(apt["appointment_time"]),
                status=apt["status"],
                has_ai_analysis=len(consult.data) > 0,
                created_at=datetime.fromisoformat(apt["created_at"])
            ))
        
        return result
    
    @staticmethod
    async def store_consultation_result(
        appointment_id: UUID,
        encrypted_result: str,
        wrapped_key: str,
        doctor_id: UUID
    ):
        """Store AI analysis result"""
        db = get_db()
        
        # Update appointment status
        db.table("appointments")\
            .update({"status": "completed"})\
            .eq("appointment_id", str(appointment_id))\
            .execute()
        
        # Store result
        db.table("consultation_results").insert({
            "appointment_id": str(appointment_id),
            "encrypted_result": encrypted_result,
            "wrapped_key": wrapped_key,
            "approved_by": str(doctor_id),
            "approved_at": datetime.now().isoformat()
        }).execute()
    
    @staticmethod
    async def get_consultation_result(appointment_id: UUID) -> Dict[str, Any]:
        """Get consultation result"""
        db = get_db()
        result = db.table("consultation_results")\
            .select("*, doctors(name)")\
            .eq("appointment_id", str(appointment_id))\
            .single()\
            .execute()
        return result.data
    
    @staticmethod
    async def get_doctor_name(doctor_id: UUID) -> str:
        """Get doctor's name"""
        db = get_db()
        result = db.table("doctors")\
            .select("name")\
            .eq("doctor_id", str(doctor_id))\
            .single()\
            .execute()
        return result.data["name"]

db_service = DatabaseService()
