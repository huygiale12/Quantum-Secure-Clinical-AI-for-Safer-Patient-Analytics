"""AI Service - Enhanced with Disease Probability Assessment"""
import logging
import google.generativeai as genai
from app.config import settings
from app.models.schemas import PatientIntakeData, LabResults, AIAnalysisResult

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


async def analyze_patient_data(
    intake_data: PatientIntakeData,
    lab_results: LabResults
) -> AIAnalysisResult:
    """
    Analyze patient data using Google Gemini AI with enhanced disease probability assessment.
    
    Returns structured clinical analysis with risk assessment, disease probabilities, and recommendations.
    """
    try:
        logger.info("Starting AI analysis with Gemini")
        
        # Prepare simplified prompt for shorter response
        prompt = f"""You are a medical AI assistant. Analyze this patient case and provide a concise assessment.

**PATIENT DATA:**
Age: {intake_data.age}, Gender: {intake_data.gender}
Chief Complaint: {intake_data.chief_complaint}
Symptoms: {intake_data.symptoms}
Duration: {intake_data.duration or intake_data.symptom_duration or 'Unknown'}
Medical History: {intake_data.medical_history}
Medications: {intake_data.current_medications or "None"}
Allergies: {intake_data.allergies or "None"}

**LAB RESULTS:**
Glucose: {lab_results.fasting_glucose} mg/dL | HbA1c: {lab_results.hba1c}%
BP: {lab_results.blood_pressure_systolic}/{lab_results.blood_pressure_diastolic} mmHg | BMI: {lab_results.bmi}
Cholesterol: Total {lab_results.cholesterol_total}, LDL {lab_results.cholesterol_ldl}, HDL {lab_results.cholesterol_hdl} mg/dL

**REQUIRED JSON OUTPUT (keep it concise):**
{{
  "risk_score": <0-10>,
  "overall_health_status": "<excellent/good/fair/concerning/critical>",
  "disease_probabilities": [
    {{"disease": "Type 2 Diabetes", "probability": "high", "confidence": "90%", "key_indicators": ["HbA1c 8.2%", "High glucose"], "explanation": "Brief explanation"}}
  ],
  "primary_concerns": ["Concern 1", "Concern 2"],
  "differential_diagnoses": ["Diagnosis 1", "Diagnosis 2"],
  "recommended_tests": ["Test 1", "Test 2"],
  "clinical_summary": "2-3 sentence summary",
  "treatment_recommendations": ["Recommendation 1", "Recommendation 2"],
  "lifestyle_recommendations": ["Lifestyle 1", "Lifestyle 2"],
  "follow_up_timeline": "Timeline",
  "urgent_actions_needed": ["Action" or "None"],
  "patient_friendly_summary": "Simple explanation of health status and risks"
}}

CRITICAL: Return ONLY valid JSON. Keep explanations brief (1-2 sentences max). NO markdown, NO extra text."""

        # Call Gemini API with safety settings
        model = genai.GenerativeModel('gemini-2.5-flash')
        logger.info("Calling Gemini API...")
        
        # Configure safety settings to allow medical content
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]
        
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.3,
                max_output_tokens=4096,  # Increased from 2048
            ),
            safety_settings=safety_settings
        )
        
        # Parse response
        import json
        
        # Check if response was blocked
        if not response.candidates or not response.candidates[0].content.parts:
            logger.error(f"Gemini blocked the response. Finish reason: {response.candidates[0].finish_reason if response.candidates else 'unknown'}")
            logger.error(f"Safety ratings: {response.candidates[0].safety_ratings if response.candidates else 'unknown'}")
            raise Exception("AI response was blocked by safety filters. This is a medical analysis request and should be allowed.")
        
        response_text = response.text.strip()
        
        # Clean up response (remove markdown if present)
        if response_text.startswith('```json'):
            response_text = response_text.split('```json')[1]
        if response_text.endswith('```'):
            response_text = response_text.rsplit('```', 1)[0]
        response_text = response_text.strip()
        
        try:
            ai_result = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.error(f"Response text (first 1000 chars): {response_text[:1000]}")
            
            # Try to fix truncated JSON by adding closing braces
            logger.info("Attempting to fix truncated JSON...")
            try:
                # Count opening and closing braces
                open_braces = response_text.count('{')
                close_braces = response_text.count('}')
                open_brackets = response_text.count('[')
                close_brackets = response_text.count(']')
                
                # Add missing closing characters
                fixed_text = response_text
                if open_brackets > close_brackets:
                    fixed_text += ']' * (open_brackets - close_brackets)
                if open_braces > close_braces:
                    fixed_text += '}' * (open_braces - close_braces)
                
                ai_result = json.loads(fixed_text)
                logger.info("Successfully fixed and parsed truncated JSON")
            except Exception as fix_error:
                logger.error(f"Failed to fix JSON: {fix_error}")
                raise Exception("AI returned invalid response format")
        
        logger.info(f"AI analysis complete. Risk score: {ai_result.get('risk_score', 'N/A')}")
        
        # Create structured response (keep all fields from AI)
        return AIAnalysisResult(
            risk_score=float(ai_result.get('risk_score', 5.0)),
            primary_concerns=ai_result.get('primary_concerns', []),
            differential_diagnoses=ai_result.get('differential_diagnoses', []),
            recommended_tests=ai_result.get('recommended_tests', []),
            clinical_summary=ai_result.get('clinical_summary', ''),
            treatment_recommendations=ai_result.get('treatment_recommendations', []),
            follow_up_timeline=ai_result.get('follow_up_timeline', 'Follow up in 1-2 weeks'),
            # Add extra fields as dict for frontend to use
            **{
                'overall_health_status': ai_result.get('overall_health_status'),
                'disease_probabilities': ai_result.get('disease_probabilities', []),
                'lifestyle_recommendations': ai_result.get('lifestyle_recommendations', []),
                'urgent_actions_needed': ai_result.get('urgent_actions_needed', []),
                'patient_friendly_summary': ai_result.get('patient_friendly_summary', '')
            }
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response as JSON: {e}")
        logger.error(f"Response text: {response_text}")
        raise Exception("AI returned invalid response format")
    except Exception as e:
        logger.error(f"AI analysis failed: {e}")
        raise Exception(f"Failed to analyze patient data: {str(e)}")
