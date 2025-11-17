"""Database service for Supabase operations"""
from datetime import datetime
from uuid import UUID, uuid4
from typing import List, Dict, Optional, Any
import logging

from app.database import get_db

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for all database operations"""
    
    async def create_appointment(
        self,
        patient_id: Optional[UUID],
        doctor_id: UUID,
        appointment_time: datetime,
    ) -> UUID:
        """Create a new appointment"""
        try:
            db = get_db()
            appointment_id = uuid4()
            
            appointment_data = {
                "appointment_id": str(appointment_id),
                "doctor_id": str(doctor_id),
                "appointment_time": appointment_time.isoformat(),
                "status": "pending",
                "created_at": datetime.now().isoformat()
            }
            
            # Only add patient_id if it's not None
            if patient_id:
                appointment_data["patient_id"] = str(patient_id)
            
            result = db.table("appointments").insert(appointment_data).execute()
            
            logger.info(f"Created appointment {appointment_id}")
            return appointment_id
            
        except Exception as e:
            logger.error(f"Failed to create appointment: {e}")
            raise
    
    async def store_encrypted_intake(
        self,
        appointment_id: UUID,
        encrypted_intake: str,
        encrypted_lab_results: str,
        wrapped_key: str,
    ):
        """Store encrypted patient intake data"""
        try:
            db = get_db()
            
            # Create encrypted package
            encrypted_data = {
                "encrypted_intake": encrypted_intake,
                "encrypted_lab_results": encrypted_lab_results
            }
            
            # Import crypto service here to avoid circular imports
            from app.services.crypto_mock import crypto_service
            encrypted_blob, outer_key = crypto_service.encrypt(encrypted_data)
            
            record_data = {
                "record_id": str(uuid4()),
                "appointment_id": str(appointment_id),
                "encrypted_blob": encrypted_blob,
                "wrapped_key": outer_key,
                "created_at": datetime.now().isoformat()
            }
            
            result = db.table("encrypted_records").insert(record_data).execute()
            
            logger.info(f"Stored encrypted record for appointment {appointment_id}")
            
        except Exception as e:
            logger.error(f"Failed to store encrypted intake: {e}")
            raise
    
    async def get_encrypted_record(self, appointment_id: UUID) -> Dict[str, Any]:
        """Get encrypted record for an appointment"""
        try:
            db = get_db()
            
            result = db.table("encrypted_records")\
                .select("*")\
                .eq("appointment_id", str(appointment_id))\
                .execute()
            
            if not result.data:
                raise Exception(f"No encrypted record found for appointment {appointment_id}")
            
            return result.data[0]
            
        except Exception as e:
            logger.error(f"Failed to get encrypted record: {e}")
            raise
    
    async def get_appointment(self, appointment_id: UUID) -> Dict[str, Any]:
        """Get appointment details"""
        try:
            db = get_db()
            
            result = db.table("appointments")\
                .select("*")\
                .eq("appointment_id", str(appointment_id))\
                .execute()
            
            if not result.data:
                raise Exception(f"No appointment found with ID {appointment_id}")
            
            return result.data[0]
            
        except Exception as e:
            logger.error(f"Failed to get appointment: {e}")
            raise
    
    async def list_doctor_appointments(self, doctor_id: UUID) -> List[Dict[str, Any]]:
        """List all appointments for a doctor"""
        try:
            db = get_db()
            
            # Get appointments
            appointments = db.table("appointments")\
                .select("*")\
                .eq("doctor_id", str(doctor_id))\
                .order("appointment_time", desc=True)\
                .execute()
            
            # Check which have results
            result_list = []
            for apt in appointments.data:
                apt_id = apt["appointment_id"]
                
                # Check if has consultation result
                has_result = db.table("consultation_results")\
                    .select("result_id")\
                    .eq("appointment_id", apt_id)\
                    .execute()
                
                result_list.append({
                    "appointment_id": apt_id,
                    "patient_id": apt.get("patient_id"),
                    "appointment_time": apt["appointment_time"],
                    "status": apt["status"],
                    "has_result": len(has_result.data) > 0
                })
            
            return result_list
            
        except Exception as e:
            logger.error(f"Failed to list appointments: {e}")
            raise
    
    async def store_consultation_result(
        self,
        appointment_id: UUID,
        encrypted_result: str,
        wrapped_key: str,
        doctor_id: UUID,
    ):
        """Store consultation result"""
        try:
            db = get_db()
            
            result_data = {
                "result_id": str(uuid4()),
                "appointment_id": str(appointment_id),
                "encrypted_result": encrypted_result,
                "wrapped_key": wrapped_key,
                "created_at": datetime.now().isoformat()
            }
            
            db.table("consultation_results").insert(result_data).execute()
            
            # Update appointment status
            db.table("appointments")\
                .update({"status": "completed"})\
                .eq("appointment_id", str(appointment_id))\
                .execute()
            
            logger.info(f"Stored consultation result for appointment {appointment_id}")
            
        except Exception as e:
            logger.error(f"Failed to store consultation result: {e}")
            raise
    
    async def get_consultation_result(self, appointment_id: UUID) -> Optional[Dict[str, Any]]:
        """Get consultation result for an appointment"""
        try:
            db = get_db()
            
            result = db.table("consultation_results")\
                .select("*, doctors(name)")\
                .eq("appointment_id", str(appointment_id))\
                .execute()
            
            if not result.data:
                return None
            
            return result.data[0]
            
        except Exception as e:
            logger.error(f"Failed to get consultation result: {e}")
            raise
    
    async def get_doctor_name(self, doctor_id: UUID) -> str:
        """Get doctor's name"""
        try:
            db = get_db()
            
            result = db.table("doctors")\
                .select("name")\
                .eq("doctor_id", str(doctor_id))\
                .execute()
            
            if result.data:
                return result.data[0]["name"]
            else:
                return "Dr. Smith"  # Fallback
                
        except Exception as e:
            logger.warning(f"Failed to get doctor name: {e}")
            return "Dr. Smith"


# Global instance
db_service = DatabaseService()
