"""Patient-facing API endpoints - ACCEPTS RAW OR ENCRYPTED DATA"""
from datetime import datetime
import logging
from uuid import UUID
import base64
import json

from fastapi import APIRouter, HTTPException, Request

from app.models.schemas import AppointmentResponse, PatientResultResponse
from app.services.crypto_mock import crypto_service
from app.services.db_service import db_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/patient", tags=["Patient"])


@router.post("/submit-intake", response_model=AppointmentResponse)
async def submit_patient_intake(request: Request) -> AppointmentResponse:
    """
    Submit patient intake - accepts BOTH encrypted and raw data for demo.
    """
    try:
        # Get raw JSON from request
        data = await request.json()
        logger.info(f"Received patient data: {list(data.keys())}")
        
        # Check if data is already encrypted (has encrypted_intake field)
        if "encrypted_intake" in data:
            logger.info("Data is encrypted, processing normally...")
            encrypted_intake = data["encrypted_intake"]
            encrypted_lab = data["encrypted_lab_results"]
            wrapped_key = data["wrapped_key"]
            doctor_id = UUID(data["doctor_id"])
            appointment_time = datetime.fromisoformat(data["appointment_time"])
        else:
            logger.info("Data is RAW (not encrypted), encrypting now...")
            
            # Extract intake and lab data from raw JSON
            intake_data = {
                "age": data.get("age"),
                "gender": data.get("gender"),
                "chief_complaint": data.get("chief_complaint"),
                "symptoms": data.get("symptoms"),
                "symptom_duration": data.get("symptom_duration"),
                "medical_history": data.get("medical_history"),
                "current_medications": data.get("current_medications"),
                "allergies": data.get("allergies"),
            }
            
            lab_data = {
                "fasting_glucose": data.get("fasting_glucose"),
                "hba1c": data.get("hba1c"),
                "blood_pressure_systolic": data.get("blood_pressure_systolic"),
                "blood_pressure_diastolic": data.get("blood_pressure_diastolic"),
                "bmi": data.get("bmi"),
                "cholesterol_total": data.get("cholesterol_total"),
                "cholesterol_ldl": data.get("cholesterol_ldl"),
                "cholesterol_hdl": data.get("cholesterol_hdl"),
                "triglycerides": data.get("triglycerides"),
            }
            
            # Encrypt the data
            encrypted_intake, key1 = crypto_service.encrypt(intake_data)
            encrypted_lab, key2 = crypto_service.encrypt(lab_data)
            wrapped_key = key1  # Use same key for simplicity
            
            # Default values
            doctor_id = UUID("11111111-1111-1111-1111-111111111111")
            appointment_time = datetime.now()
        
        # Create appointment
        appointment_id = await db_service.create_appointment(
            patient_id=None,
            doctor_id=doctor_id,
            appointment_time=appointment_time,
        )
        
        # Store encrypted data
        await db_service.store_encrypted_intake(
            appointment_id=appointment_id,
            encrypted_intake=encrypted_intake,
            encrypted_lab_results=encrypted_lab,
            wrapped_key=wrapped_key,
        )
        
        logger.info(f"Successfully created appointment {appointment_id}")
        
        return AppointmentResponse(
            appointment_id=appointment_id,
            status="pending",
            message="Your intake form has been submitted successfully",
        )
        
    except Exception as e:
        logger.error(f"Error submitting intake: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/result/{appointment_id}", response_model=PatientResultResponse)
async def get_patient_result(appointment_id: UUID) -> PatientResultResponse:
    """Get consultation results for a patient."""
    try:
        logger.info(f"Patient requesting results for appointment {appointment_id}")
        
        result = await db_service.get_consultation_result(appointment_id)
        
        if not result:
            logger.info(f"No results found for appointment {appointment_id}")
            raise HTTPException(
                status_code=404,
                detail="Results not ready yet"
            )
        
        # Decrypt the result
        decrypted_result = crypto_service.decrypt(
            result["encrypted_result"],
            result["wrapped_key"]
        )
        
        # Get doctor name
        doctor_id = result.get("doctor_id") or decrypted_result.get("approved_by")
        doctor_name = "Dr. Smith"
        if doctor_id:
            try:
                doctor_name = await db_service.get_doctor_name(UUID(doctor_id))
            except:
                pass
        
        logger.info(f"Successfully retrieved results for appointment {appointment_id}")
        
        return PatientResultResponse(
            appointment_id=appointment_id,
            status="completed",
            approved_by=UUID(doctor_id) if doctor_id else UUID("11111111-1111-1111-1111-111111111111"),
            approved_at=datetime.fromisoformat(result.get("created_at", datetime.now().isoformat())),
            doctor_name=doctor_name,
            doctor_notes=decrypted_result.get("doctor_notes"),
            ai_analysis=decrypted_result.get("ai_analysis"),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving patient result: {e}")
        raise HTTPException(status_code=500, detail=str(e))
