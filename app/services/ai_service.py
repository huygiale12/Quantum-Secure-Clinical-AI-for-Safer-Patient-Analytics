import google.generativeai as genai
import json
import logging
from app.config import settings
from app.models.schemas import AIAnalysisResult, PatientIntakeData, LabResults

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


async def analyze_patient_data(
    intake_data: PatientIntakeData,
    lab_results: LabResults
) -> AIAnalysisResult:
    """
    Analyze patient data using Google Gemini AI.
    
    Returns structured clinical analysis with risk assessment and recommendations.
    """
    try:
        logger.info("Starting AI analysis with Gemini")
        
        # Create the prompt
        prompt = f"""You are an experienced clinical AI assistant. Analyze the following patient data and provide a structured clinical assessment.

PATIENT INTAKE:
- Age: {intake_data.age}
- Gender: {intake_data.gender}
- Chief Complaint: {intake_data.chief_complaint}
- Medical History: {', '.join(intake_data.medical_history)}
- Current Medications: {', '.join(intake_data.current_medications)}
- Allergies: {', '.join(intake_data.allergies)}
- Symptoms: {intake_data.symptoms}
- Duration: {intake_data.symptom_duration}

LAB RESULTS:
- Glucose: {lab_results.glucose} mg/dL
- HbA1c: {lab_results.hba1c}%
- Total Cholesterol: {lab_results.cholesterol} mg/dL
- Triglycerides: {lab_results.triglycerides} mg/dL
- HDL: {lab_results.hdl} mg/dL
- LDL: {lab_results.ldl} mg/dL
- Blood Pressure: {lab_results.blood_pressure}
- BMI: {lab_results.bmi}

Please provide a clinical analysis in the following JSON format (respond ONLY with valid JSON, no markdown):

{{
  "risk_score": <0-100 integer>,
  "primary_concerns": ["concern1", "concern2"],
  "differential_diagnoses": ["diagnosis1", "diagnosis2"],
  "recommended_tests": ["test1", "test2"],
  "follow_up_questions": ["question1", "question2"],
  "recommendations": ["recommendation1", "recommendation2"],
  "clinical_summary": "Brief clinical summary paragraph"
}}

IMPORTANT: Respond ONLY with the JSON object. Do not include markdown formatting, backticks, or any text outside the JSON structure."""

        # Use Gemini 2.5 Flash
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        response = model.generate_content(prompt)
        
        # Parse response
        response_text = response.text.strip()
        
        # Remove markdown formatting if present
        response_text = response_text.replace('```json\n', '').replace('```\n', '').replace('```', '').strip()
        
        # Parse JSON
        analysis_data = json.loads(response_text)
        
        # Create AIAnalysisResult
        result = AIAnalysisResult(
            risk_score=analysis_data["risk_score"],
            primary_concerns=analysis_data["primary_concerns"],
            differential_diagnoses=analysis_data["differential_diagnoses"],
            recommended_tests=analysis_data["recommended_tests"],
            follow_up_questions=analysis_data["follow_up_questions"],
            recommendations=analysis_data["recommendations"],
            clinical_summary=analysis_data["clinical_summary"]
        )
        
        logger.info(f"AI analysis completed. Risk score: {result.risk_score}")
        return result
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {e}")
        logger.error(f"Raw response: {response_text}")
        
        # Fallback response
        return AIAnalysisResult(
            risk_score=50,
            primary_concerns=["Unable to analyze - AI service error"],
            differential_diagnoses=["Manual review required"],
            recommended_tests=["Complete clinical examination"],
            follow_up_questions=["Please review patient data manually"],
            recommendations=["Manual clinical assessment needed"],
            clinical_summary="AI analysis unavailable. Please conduct manual review."
        )
        
    except Exception as e:
        logger.error(f"AI analysis failed: {e}")
        
        # Fallback response
        return AIAnalysisResult(
            risk_score=50,
            primary_concerns=["AI service temporarily unavailable"],
            differential_diagnoses=["Requires manual assessment"],
            recommended_tests=["Standard clinical workup"],
            follow_up_questions=["Review symptoms and history"],
            recommendations=["Manual clinical review recommended"],
            clinical_summary="AI analysis service is currently unavailable. Please proceed with standard clinical assessment."
        )
