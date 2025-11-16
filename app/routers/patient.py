from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.models.schemas import (
    EncryptedPatientData,
    PatientSubmitResponse,
    PatientResultResponse
)
from app.services.crypto_mock import crypto_service
from app.services.db_service import db_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/patient", tags=["Patient"])


@router.post("/submit-intake", response_model=PatientSubmitResponse)
async def submit_patient_intake(data: EncryptedPatientData):
    """
    Patient submits encrypted intake data and lab results.
    
    Flow:
    1. Receive encrypted data from patient
    2. Create patient record
    3. Create appointment
    4. Store encrypted data
    5. Return appointment_id
    """
    try:
        logger.info("Received patient intake submission")
        
        # Create patient
        patient_id = await db_service.create_patient()
        logger.info(f"Created patient: {patient_id}")
        
        # Create appointment
        appointment_id = await db_service.create_appointment(
            patient_id=patient_id,
            doctor_id=data.doctor_id,
            appointment_time=data.appointment_time
        )
        logger.info(f"Created appointment: {appointment_id}")
        
        # Combine encrypted data into one blob
        combined_data = {
            "encrypted_intake": data.encrypted_intake,
            "encrypted_lab_results": data.encrypted_lab_results
        }
        
        # Encrypt the combined data using Raymond's crypto
        encrypted_blob, wrapped_key = crypto_service.encrypt(combined_data)
        
        # Store in database
        await db_service.store_encrypted_record(
            appointment_id=appointment_id,
            encrypted_blob=encrypted_blob,
            wrapped_key=wrapped_key,
            metadata={"submitted_at": data.appointment_time.isoformat()}
        )
        
        logger.info(f"Successfully stored encrypted record for appointment {appointment_id}")
        
        return PatientSubmitResponse(
            appointment_id=appointment_id,
            status="pending",
            message="Your data has been securely submitted. Your doctor will review it soon."
        )
        
    except Exception as e:
        logger.error(f"Error submitting patient intake: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/result/{appointment_id}", response_model=PatientResultResponse)
async def get_consultation_result(appointment_id: UUID):
    """
    Patient retrieves their consultation results.
    
    Flow:
    1. Look up consultation result by appointment_id
    2. Return encrypted result (patient will decrypt on their device)
    """
    try:
        logger.info(f"Patient requesting result for appointment {appointment_id}")
        
        # Get consultation result
        result = await db_service.get_consultation_result(appointment_id)
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail="Consultation result not found. The doctor may not have completed the analysis yet."
            )
        
        # Get appointment status
        appointment = await db_service.get_appointment(appointment_id)
        
        return PatientResultResponse(
            appointment_id=appointment_id,
            encrypted_result=result["encrypted_result"],
            wrapped_key=result["wrapped_key"],
            approved_by_doctor=result["doctors"]["name"],
            approved_at=result["approved_at"],
            status=appointment["status"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving consultation result: {e}")
        raise HTTPException(status_code=500, detail=str(e))
