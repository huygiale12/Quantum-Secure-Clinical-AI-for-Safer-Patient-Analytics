from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import List
from app.models.schemas import (
    AppointmentListItem,
    DecryptedPatientRecord,
    PatientIntakeData,
    LabResults,
    DoctorAnalysisRequest,
    ConsultationResult,
    AIAnalysisResult
)
from app.services.crypto_mock import crypto_service
from app.services.db_service import db_service
from app.services.ai_service import analyze_patient_data
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/doctor", tags=["Doctor"])


@router.get("/appointments", response_model=List[AppointmentListItem])
async def list_appointments(
    doctor_id: UUID = Query(..., description="Doctor's UUID")
):
    """
    List all appointments for a doctor.
    
    Shows:
    - Pending appointments
    - Completed appointments
    - Whether AI analysis has been done
    """
    try:
        logger.info(f"Fetching appointments for doctor {doctor_id}")
        
        appointments = await db_service.list_doctor_appointments(doctor_id)
        
        logger.info(f"Found {len(appointments)} appointments")
        return appointments
        
    except Exception as e:
        logger.error(f"Error fetching appointments: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/record/{appointment_id}", response_model=DecryptedPatientRecord)
async def get_patient_record(appointment_id: UUID):
    """
    Decrypt and retrieve patient record for a specific appointment.
    
    Flow:
    1. Fetch encrypted record from DB
    2. Decrypt using Raymond's crypto service
    3. Parse and return structured data
    """
    try:
        logger.info(f"Doctor requesting record for appointment {appointment_id}")
        
        # Get encrypted record
        encrypted_record = await db_service.get_encrypted_record(appointment_id)
        appointment = await db_service.get_appointment(appointment_id)
        
        # Decrypt using Raymond's crypto
        decrypted_data = crypto_service.decrypt(
            encrypted_record["encrypted_blob"],
            encrypted_record["wrapped_key"]
        )
        
        # The decrypted data contains encrypted_intake and encrypted_lab_results
        # These are base64 strings that were encrypted by the patient
        # For demo purposes, we'll decrypt them again (in real app, patient encrypts once)
        
        intake_encrypted = decrypted_data["encrypted_intake"]
        lab_encrypted = decrypted_data["encrypted_lab_results"]
        
        # In a real scenario, these would be decrypted with patient's key
        # For demo, we'll assume they're also encrypted with our crypto service
        intake_data_raw = crypto_service.decrypt(intake_encrypted, encrypted_record["wrapped_key"])
        lab_data_raw = crypto_service.decrypt(lab_encrypted, encrypted_record["wrapped_key"])
        
        # Parse into Pydantic models
        intake_data = PatientIntakeData(**intake_data_raw)
        lab_results = LabResults(**lab_data_raw)
        
        logger.info("Successfully decrypted patient record")
        
        return DecryptedPatientRecord(
            appointment_id=UUID(appointment["appointment_id"]),
            patient_id=UUID(appointment["patient_id"]),
            intake_data=intake_data,
            lab_results=lab_results,
            appointment_time=datetime.fromisoformat(appointment["appointment_time"]),
            status=appointment["status"]
        )
        
    except Exception as e:
        logger.error(f"Error retrieving patient record: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/record/{appointment_id}/analyze-and-approve", response_model=ConsultationResult)
async def analyze_and_approve(
    appointment_id: UUID,
    request: DoctorAnalysisRequest
):
    """
    Doctor analyzes patient data with AI and approves consultation.
    
    Flow:
    1. Decrypt patient data
    2. If AI requested, analyze with Gemini
    3. Create consultation result
    4. Encrypt result
    5. Store in database
    6. Return to doctor
    """
    try:
        logger.info(f"Doctor {request.doctor_id} analyzing appointment {appointment_id}")
        
        # Get encrypted record
        encrypted_record = await db_service.get_encrypted_record(appointment_id)
        appointment = await db_service.get_appointment(appointment_id)
        
        # Decrypt patient data
        decrypted_data = crypto_service.decrypt(
            encrypted_record["encrypted_blob"],
            encrypted_record["wrapped_key"]
        )
        
        intake_encrypted = decrypted_data["encrypted_intake"]
        lab_encrypted = decrypted_data["encrypted_lab_results"]
        
        intake_data_raw = crypto_service.decrypt(intake_encrypted, encrypted_record["wrapped_key"])
        lab_data_raw = crypto_service.decrypt(lab_encrypted, encrypted_record["wrapped_key"])
        
        intake_data = PatientIntakeData(**intake_data_raw)
        lab_results = LabResults(**lab_data_raw)
        
        # AI Analysis
        ai_analysis = None
        if request.request_ai_analysis:
            logger.info("Requesting AI analysis from Gemini...")
            ai_analysis = await analyze_patient_data(intake_data, lab_results)
            logger.info(f"AI analysis complete. Risk score: {ai_analysis.risk_score}")
        
        # Create consultation result
        result_data = {
            "appointment_id": str(appointment_id),
            "doctor_notes": request.doctor_notes,
            "approved": request.approved,
            "approved_at": datetime.now().isoformat(),
            "ai_analysis": ai_analysis.dict() if ai_analysis else None
        }
        
        # Encrypt result using Raymond's crypto
        encrypted_result, wrapped_key = crypto_service.encrypt(result_data)
        
        # Store in database
        await db_service.store_consultation_result(
            appointment_id=appointment_id,
            encrypted_result=encrypted_result,
            wrapped_key=wrapped_key,
            doctor_id=request.doctor_id
        )
        
        # Get doctor name
        doctor_name = await db_service.get_doctor_name(request.doctor_id)
        
        logger.info(f"Consultation approved and stored for appointment {appointment_id}")
        
        return ConsultationResult(
            appointment_id=appointment_id,
            encrypted_result=encrypted_result,
            wrapped_key=wrapped_key,
            approved_by=request.doctor_id,
            approved_at=datetime.now(),
            doctor_name=doctor_name
        )
        
    except Exception as e:
        logger.error(f"Error in analyze and approve: {e}")
        raise HTTPException(status_code=500, detail=str(e))
