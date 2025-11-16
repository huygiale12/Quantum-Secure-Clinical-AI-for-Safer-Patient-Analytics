import google.generativeai as genai
import json
import logging
from app.config import settings
from app.models.schemas import AIAnalysisResult, PatientIntakeData, LabResults
from app.utils.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

async def analyze_patient_data(
    intake_data: PatientIntakeData,
    lab_results: LabResults
) -> AIAnalysisResult:
    """
    Analyze patient data using Google Gemini (FREE!)
    """
    try:
        # Format user prompt
        user_prompt = USER_PROMPT_TEMPLATE.format(
            age=intake_data.age,
            gender=intake_data.gender,
            symptoms=intake_data.symptoms,
            medical_history=", ".join(intake_data.medical_history) if intake_data.medical_history else "None",
            medications=", ".join(intake_data.current_medications) if intake_data.current_medications else "None",
            glucose=lab_results.fasting_glucose,
            hba1c=lab_results.hba1c,
            creatinine=lab_results.creatinine,
            cholesterol=lab_results.total_cholesterol,
            ldl=lab_results.ldl,
            hdl=lab_results.hdl,
            triglycerides=lab_results.triglycerides,
            lab_notes=lab_results.notes or "None"
        )
        
        logger.info("Sending request to Gemini API...")
        
        # Use Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        full_prompt = f"{SYSTEM_PROMPT}\n\n{user_prompt}"
        
        response = model.generate_content(
            full_prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 1500,
            }
        )
        
        # Parse response
        response_text = response.text
        
        # Extract JSON (Gemini might wrap it in markdown)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
            
        ai_result = json.loads(response_text)
        
        logger.info(f"AI analysis completed. Risk score: {ai_result.get('risk_score')}")
        
        return AIAnalysisResult(**ai_result)
        
    except Exception as e:
        logger.error(f"Error in AI analysis: {e}")
        return _get_fallback_response()

def _get_fallback_response() -> AIAnalysisResult:
    """Fallback response if API fails"""
    logger.warning("Using fallback AI response")
    return AIAnalysisResult(
        risk_score=5.0,
        risk_level="moderate",
        diagnosis_suggestions=[
            "Unable to complete AI analysis. Please review patient data manually."
        ],
        follow_up_questions=[
            "Please conduct a thorough clinical examination"
        ],
        recommendations=[
            "Manual review required due to AI system unavailability"
        ]
    )
