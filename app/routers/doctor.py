"""Doctor-facing API endpoints"""
from datetime import datetime
import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    AppointmentListItem,
    DecryptedPatientRecord,
    DoctorAnalysisRequest,
)
from app.services.crypto_mock import crypto_service
from app.services.db_service import db_service
from app.services.ai_service import analyze_patient_data

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/doctor", tags=["Doctor"])


@router.get("/appointments", response_model=list[AppointmentListItem])
async def get_appointments(doctor_id: str):
    """Get all appointments for a doctor"""
    try:
        logger.info(f"Fetching appointments for doctor {doctor_id}")
        
        appointments = await db_service.list_doctor_appointments(UUID(doctor_id))
        
        logger.info(f"Found {len(appointments)} appointments")
        return appointments
        
    except Exception as e:
        logger.error(f"Error fetching appointments: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/record/{appointment_id}")
async def get_patient_record(appointment_id: str):
    """
    Get decrypted patient record for doctor to review.
    Returns intake data and lab results in plaintext.
    """
    try:
        logger.info(f"Doctor requesting record for appointment {appointment_id}")
        
        # Convert to UUID
        apt_id = UUID(appointment_id)
        
        # Get encrypted record
        encrypted_record = await db_service.get_encrypted_record(apt_id)
        
        # Get appointment details
        appointment = await db_service.get_appointment(apt_id)
        
        # Decrypt the outer layer
        decrypted_outer = crypto_service.decrypt(
            encrypted_record["encrypted_blob"],
            encrypted_record["wrapped_key"]
        )
        
        # Decrypt the inner layers
        intake_data = crypto_service.decrypt(
            decrypted_outer["encrypted_intake"],
            encrypted_record["wrapped_key"]
        )
        
        lab_results = crypto_service.decrypt(
            decrypted_outer["encrypted_lab_results"],
            encrypted_record["wrapped_key"]
        )
        
        logger.info("Successfully decrypted patient record")
        
        # Return decrypted data - let Pydantic handle conversion
        return {
            "appointment_id": str(apt_id),
            "patient_id": appointment.get("patient_id"),  # May be None
            "intake_data": intake_data,
            "lab_results": lab_results,
            "appointment_time": appointment["appointment_time"],
            "status": appointment["status"]
        }
        
    except Exception as e:
        logger.error(f"Error retrieving patient record: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze")
async def analyze_and_approve(request: DoctorAnalysisRequest):
    """
    Analyze patient data with AI and store encrypted results.
    This approves the consultation and makes results available to patient.
    """
    try:
        logger.info(f"Doctor {request.doctor_id} analyzing appointment {request.appointment_id}")
        
        apt_id = UUID(str(request.appointment_id))
        
        # Get encrypted record
        encrypted_record = await db_service.get_encrypted_record(apt_id)
        
        # Decrypt to get patient data
        decrypted_outer = crypto_service.decrypt(
            encrypted_record["encrypted_blob"],
            encrypted_record["wrapped_key"]
        )
        
        intake_data = crypto_service.decrypt(
            decrypted_outer["encrypted_intake"],
            encrypted_record["wrapped_key"]
        )
        
        lab_results = crypto_service.decrypt(
            decrypted_outer["encrypted_lab_results"],
            encrypted_record["wrapped_key"]
        )
        
        # Run AI analysis if requested
        ai_analysis = None
        if request.request_ai_analysis:
            logger.info("Running AI analysis...")
            
            from app.models.schemas import PatientIntakeData, LabResults
            
            # Convert to Pydantic models for AI
            intake_model = PatientIntakeData(**intake_data)
            lab_model = LabResults(**lab_results)
            
            ai_result = await analyze_patient_data(intake_model, lab_model)
            ai_analysis = ai_result.dict()
            
            logger.info(f"AI analysis complete. Risk score: {ai_analysis.get('risk_score')}")
        
        # Create result package
        result_data = {
            "doctor_notes": request.doctor_notes,
            "ai_analysis": ai_analysis,
            "approved_by": str(request.doctor_id),
            "approved_at": datetime.now().isoformat()
        }
        
        # Encrypt the result for patient
        encrypted_result, wrapped_key = crypto_service.encrypt(result_data)
        
        # Store consultation result
        await db_service.store_consultation_result(
            appointment_id=apt_id,
            encrypted_result=encrypted_result,
            wrapped_key=wrapped_key,
            doctor_id=UUID(str(request.doctor_id))
        )
        
        logger.info(f"Consultation result stored for appointment {apt_id}")
        
        return {
            "status": "success",
            "message": "Analysis complete and results encrypted for patient",
            "ai_analysis": ai_analysis  # Return to doctor for display
        }
        
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
