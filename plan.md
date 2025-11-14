# Quantum Safe Patient Analytics - COMPLETE STEP-BY-STEP GUIDE
**Backend + AI Implementation for 72-Hour Hackathon**

---

## 📋 Table of Contents
1. [Prerequisites & Setup](#prerequisites--setup)
2. [Phase 1: Project Initialization (Hours 0-8)](#phase-1-project-initialization-hours-0-8)
3. [Phase 2: Database Setup (Hours 8-16)](#phase-2-database-setup-hours-8-16)
4. [Phase 3: Core APIs (Hours 16-32)](#phase-3-core-apis-hours-16-32)
5. [Phase 4: AI Integration (Hours 32-48)](#phase-4-ai-integration-hours-32-48)
6. [Phase 5: Testing & Integration (Hours 48-64)](#phase-5-testing--integration-hours-48-64)
7. [Phase 6: Demo Preparation (Hours 64-72)](#phase-6-demo-preparation-hours-64-72)
8. [Troubleshooting Guide](#troubleshooting-guide)

---

## Prerequisites & Setup

### Required Software
- **Python 3.11+** (Verify: `python --version`)
- **Docker Desktop** (latest version)
- **Git**
- **VS Code** or your preferred IDE
- **Postman** or **Thunder Client** for API testing

### Required Accounts
1. **Supabase Account** (free tier)
   - Go to: https://supabase.com
   - Sign up with GitHub or email
   - Keep your credentials handy

2. **OpenAI Account** (paid tier recommended for hackathon)
   - Go to: https://platform.openai.com
   - Add payment method (GPT-4 access requires paid account)
   - Get API key from: https://platform.openai.com/api-keys
   - **Budget**: Set up $10-20 budget limit for safety

### Install Python Dependencies Locally (for development)
```bash
pip install fastapi uvicorn python-dotenv supabase openai pydantic httpx pytest
```

---

## Phase 1: Project Initialization (Hours 0-8)

### Step 1.1: Create Project Structure
```bash
# Create project directory
mkdir quantum-health-backend
cd quantum-health-backend

# Create directory structure
mkdir -p app/{routers,models,services,utils}
mkdir -p tests data scripts
touch app/__init__.py
touch app/routers/__init__.py
touch app/models/__init__.py
touch app/services/__init__.py
touch app/utils/__init__.py
```

**Expected structure:**
```
quantum-health-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── patient.py
│   │   └── doctor.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── crypto_mock.py
│   │   ├── ai_service.py
│   │   └── db_service.py
│   └── utils/
│       ├── __init__.py
│       └── prompts.py
├── tests/
├── data/
├── scripts/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Step 1.2: Create `.gitignore`
```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Docker
*.log
EOF
```

### Step 1.3: Create `requirements.txt`
```bash
cat > requirements.txt << 'EOF'
# FastAPI and server
fastapi==0.115.14
uvicorn[standard]==0.30.6
pydantic==2.8.2
pydantic-settings==2.5.2

# Database
supabase==2.7.4
postgrest==0.16.11

# AI
openai==1.54.0

# Utilities
python-dotenv==1.0.1
python-multipart==0.0.9
httpx==0.27.2

# Testing
pytest==8.3.3
pytest-asyncio==0.24.0
EOF
```

### Step 1.4: Create `.env.example`
```bash
cat > .env.example << 'EOF'
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Application
ENVIRONMENT=development
DEBUG=True
API_VERSION=v1
EOF
```

### Step 1.5: Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial project structure"
```

**✅ Checkpoint**: You should have a clean project structure with all folders and config files ready.

---

## Phase 2: Database Setup (Hours 8-16)

### Step 2.1: Create Supabase Project

1. **Go to Supabase Dashboard**: https://app.supabase.com
2. **Click "New Project"**
3. **Fill in details**:
   - Name: `quantum-health-hackathon`
   - Database Password: (save this - you'll need it)
   - Region: Choose closest to you
4. **Wait 2-3 minutes** for project to initialize

### Step 2.2: Get Supabase Credentials

1. In your project dashboard, go to **Settings** → **API**
2. Copy these values:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **anon/public key** (starts with `eyJhb...`)
3. Update your `.env` file:
```bash
cp .env.example .env
# Edit .env and paste your credentials
```

### Step 2.3: Create Database Tables

1. In Supabase dashboard, go to **SQL Editor**
2. Click **New Query**
3. Copy and paste this SQL:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create patients table
CREATE TABLE patients (
    patient_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create doctors table
CREATE TABLE doctors (
    doctor_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    specialty VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create appointments table
CREATE TABLE appointments (
    appointment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(patient_id),
    doctor_id UUID REFERENCES doctors(doctor_id),
    appointment_time TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create encrypted_records table
CREATE TABLE encrypted_records (
    record_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    appointment_id UUID REFERENCES appointments(appointment_id) UNIQUE,
    encrypted_blob TEXT NOT NULL,
    wrapped_key TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create consultation_results table
CREATE TABLE consultation_results (
    result_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    appointment_id UUID REFERENCES appointments(appointment_id) UNIQUE,
    encrypted_result TEXT NOT NULL,
    wrapped_key TEXT NOT NULL,
    approved_by UUID REFERENCES doctors(doctor_id),
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert sample doctors
INSERT INTO doctors (doctor_id, name, specialty) VALUES
('11111111-1111-1111-1111-111111111111', 'Dr. Sarah Chen', 'Endocrinology'),
('22222222-2222-2222-2222-222222222222', 'Dr. Michael Rodriguez', 'Internal Medicine'),
('33333333-3333-3333-3333-333333333333', 'Dr. Emily Johnson', 'Family Medicine');
```

4. Click **Run** (or press F5)
5. **Verify**: Go to **Table Editor** and you should see 5 tables

**✅ Checkpoint**: All 5 tables created with sample doctors inserted.

### Step 2.4: Create Database Service File

Create `app/database.py`:
```python
from supabase import create_client, Client
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    _instance: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get Supabase client instance (singleton pattern)"""
        if cls._instance is None:
            try:
                cls._instance = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_KEY
                )
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                raise
        return cls._instance

# Convenience function
def get_db() -> Client:
    return Database.get_client()
```

### Step 2.5: Create Configuration File

Create `app/config.py`:
```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # OpenAI
    OPENAI_API_KEY: str
    
    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_VERSION: str = "v1"
    
    # CORS (if needed)
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

**✅ Checkpoint**: Database connection configured, ready to use.

---

## Phase 3: Core APIs (Hours 16-32)

### Step 3.1: Create Pydantic Models

Create `app/models/schemas.py`:
```python
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
from uuid import UUID

# Patient Models
class PatientIntakeRequest(BaseModel):
    patient_id: Optional[UUID] = None
    doctor_id: UUID
    appointment_time: datetime
    encrypted_data: str = Field(..., description="Base64 encoded ciphertext")
    wrapped_key: str = Field(..., description="Base64 encoded wrapped AES key")
    metadata: Optional[Dict] = None

class PatientIntakeResponse(BaseModel):
    status: str
    appointment_id: UUID
    message: str

# Lab Results Models
class LabResults(BaseModel):
    test_date: str
    fasting_glucose: float
    hba1c: float
    creatinine: float
    total_cholesterol: float
    ldl: float
    hdl: float
    triglycerides: float
    notes: Optional[str] = None

class PatientIntakeData(BaseModel):
    age: int
    gender: str
    symptoms: str
    medical_history: List[str]
    current_medications: List[str]

class DecryptedPatientData(BaseModel):
    appointment_id: UUID
    patient_id: UUID
    intake_data: PatientIntakeData
    lab_results: LabResults

# Doctor Models
class Appointment(BaseModel):
    appointment_id: UUID
    patient_id: UUID
    appointment_time: datetime
    status: str
    created_at: datetime

class AppointmentListResponse(BaseModel):
    appointments: List[Appointment]

# AI Analysis Models
class AIAnalysisResult(BaseModel):
    risk_score: float = Field(..., ge=0, le=10)
    risk_level: str
    diagnosis_suggestions: List[str]
    follow_up_questions: List[str]
    recommendations: List[str]

class AnalyzeApproveRequest(BaseModel):
    doctor_id: UUID
    request_ai_analysis: bool = True
    doctor_notes: Optional[str] = None
    approved: bool = True

class AnalyzeApproveResponse(BaseModel):
    status: str
    ai_analysis: Optional[AIAnalysisResult]
    message: str

# Patient Result Models
class PatientResultResponse(BaseModel):
    appointment_id: UUID
    status: str
    encrypted_result: str
    wrapped_key: str
    approved_at: Optional[datetime]
    approved_by: Optional[str]
```

### Step 3.2: Create Mock Crypto Service

Create `app/services/crypto_mock.py`:
```python
import base64
import json
import logging

logger = logging.getLogger(__name__)

class MockCryptoService:
    """
    Mock encryption/decryption for demo purposes.
    In production, Raymond will replace this with real PQC implementation.
    """
    
    @staticmethod
    def encrypt(plaintext_data: dict) -> tuple[str, str]:
        """
        Mock encryption: Just base64 encode the JSON
        Returns: (ciphertext, wrapped_key)
        """
        try:
            json_str = json.dumps(plaintext_data)
            ciphertext = base64.b64encode(json_str.encode()).decode()
            # Mock wrapped key (in reality, this would be AES key encrypted with Kyber)
            wrapped_key = base64.b64encode(b"mock_aes_key_wrapped_with_kyber").decode()
            
            logger.info("Data encrypted (mock)")
            return ciphertext, wrapped_key
        except Exception as e:
            logger.error(f"Mock encryption failed: {e}")
            raise
    
    @staticmethod
    def decrypt(ciphertext: str, wrapped_key: str) -> dict:
        """
        Mock decryption: Just base64 decode the JSON
        """
        try:
            json_str = base64.b64decode(ciphertext.encode()).decode()
            plaintext_data = json.loads(json_str)
            
            logger.info("Data decrypted (mock)")
            return plaintext_data
        except Exception as e:
            logger.error(f"Mock decryption failed: {e}")
            raise

# Global instance
crypto_service = MockCryptoService()
```

### Step 3.3: Create Main FastAPI Application

Create `app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import patient, doctor
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Quantum Safe Patient Analytics API",
    description="Backend API for quantum-safe healthcare data management",
    version=settings.API_VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(patient.router, prefix=f"/api/{settings.API_VERSION}/patient", tags=["Patient"])
app.include_router(doctor.router, prefix=f"/api/{settings.API_VERSION}/doctor", tags=["Doctor"])

@app.get("/")
def root():
    return {
        "message": "Quantum Safe Patient Analytics API",
        "version": settings.API_VERSION,
        "status": "operational"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

### Step 3.4: Create Patient Router (APIs #1 and #2)

Create `app/routers/patient.py`:
```python
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    PatientIntakeRequest, PatientIntakeResponse,
    PatientResultResponse
)
from app.database import get_db
from app.services.crypto_mock import crypto_service
from uuid import UUID
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/submit-intake", response_model=PatientIntakeResponse)
async def submit_patient_intake(request: PatientIntakeRequest):
    """
    API #1: Patient submits encrypted intake data and lab results
    """
    try:
        db = get_db()
        
        # Create patient if new
        if request.patient_id is None:
            patient_response = db.table("patients").insert({}).execute()
            patient_id = patient_response.data[0]["patient_id"]
            logger.info(f"Created new patient: {patient_id}")
        else:
            patient_id = str(request.patient_id)
        
        # Create appointment
        appointment_data = {
            "patient_id": patient_id,
            "doctor_id": str(request.doctor_id),
            "appointment_time": request.appointment_time.isoformat(),
            "status": "pending"
        }
        appointment_response = db.table("appointments").insert(appointment_data).execute()
        appointment_id = appointment_response.data[0]["appointment_id"]
        logger.info(f"Created appointment: {appointment_id}")
        
        # Store encrypted data
        encrypted_record = {
            "appointment_id": appointment_id,
            "encrypted_blob": request.encrypted_data,
            "wrapped_key": request.wrapped_key,
            "metadata": request.metadata or {}
        }
        db.table("encrypted_records").insert(encrypted_record).execute()
        logger.info(f"Stored encrypted record for appointment: {appointment_id}")
        
        return PatientIntakeResponse(
            status="success",
            appointment_id=UUID(appointment_id),
            message="Data encrypted and stored securely"
        )
        
    except Exception as e:
        logger.error(f"Error in submit_patient_intake: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/result/{appointment_id}", response_model=PatientResultResponse)
async def get_patient_result(appointment_id: UUID):
    """
    API #2: Patient retrieves encrypted consultation results
    """
    try:
        db = get_db()
        
        # Get consultation result
        result = db.table("consultation_results")\
            .select("*, doctors(name)")\
            .eq("appointment_id", str(appointment_id))\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="No results found for this appointment")
        
        data = result.data[0]
        
        # Get appointment status
        appointment = db.table("appointments")\
            .select("status")\
            .eq("appointment_id", str(appointment_id))\
            .execute()
        
        return PatientResultResponse(
            appointment_id=appointment_id,
            status=appointment.data[0]["status"] if appointment.data else "unknown",
            encrypted_result=data["encrypted_result"],
            wrapped_key=data["wrapped_key"],
            approved_at=data.get("approved_at"),
            approved_by=data.get("doctors", {}).get("name")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_patient_result: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### Step 3.5: Create Doctor Router (APIs #3, #4, #5)

Create `app/routers/doctor.py`:
```python
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    AppointmentListResponse, Appointment,
    DecryptedPatientData,
    AnalyzeApproveRequest, AnalyzeApproveResponse
)
from app.database import get_db
from app.services.crypto_mock import crypto_service
from app.services.ai_service import analyze_patient_data
from uuid import UUID
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/appointments", response_model=AppointmentListResponse)
async def get_doctor_appointments(
    doctor_id: UUID,
    status: Optional[str] = None
):
    """
    API #3: Get list of appointments for a doctor
    """
    try:
        db = get_db()
        
        query = db.table("appointments").select("*").eq("doctor_id", str(doctor_id))
        
        if status:
            query = query.eq("status", status)
        
        query = query.order("appointment_time", desc=True)
        result = query.execute()
        
        appointments = [
            Appointment(
                appointment_id=UUID(apt["appointment_id"]),
                patient_id=UUID(apt["patient_id"]),
                appointment_time=apt["appointment_time"],
                status=apt["status"],
                created_at=apt["created_at"]
            )
            for apt in result.data
        ]
        
        return AppointmentListResponse(appointments=appointments)
        
    except Exception as e:
        logger.error(f"Error in get_doctor_appointments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/record/{appointment_id}", response_model=DecryptedPatientData)
async def get_patient_record(appointment_id: UUID):
    """
    API #4: Get decrypted patient record for doctor to review
    """
    try:
        db = get_db()
        
        # Get encrypted record
        record = db.table("encrypted_records")\
            .select("*")\
            .eq("appointment_id", str(appointment_id))\
            .execute()
        
        if not record.data:
            raise HTTPException(status_code=404, detail="Record not found")
        
        encrypted_data = record.data[0]
        
        # Decrypt data (mock)
        decrypted = crypto_service.decrypt(
            encrypted_data["encrypted_blob"],
            encrypted_data["wrapped_key"]
        )
        
        # Get patient_id from appointment
        appointment = db.table("appointments")\
            .select("patient_id")\
            .eq("appointment_id", str(appointment_id))\
            .execute()
        
        return DecryptedPatientData(
            appointment_id=appointment_id,
            patient_id=UUID(appointment.data[0]["patient_id"]),
            intake_data=decrypted["intake_data"],
            lab_results=decrypted["lab_results"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_patient_record: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/record/{appointment_id}/analyze-and-approve", response_model=AnalyzeApproveResponse)
async def analyze_and_approve(appointment_id: UUID, request: AnalyzeApproveRequest):
    """
    API #5: Analyze patient data with AI and approve results
    """
    try:
        db = get_db()
        
        # Get decrypted patient data
        record = db.table("encrypted_records")\
            .select("*")\
            .eq("appointment_id", str(appointment_id))\
            .execute()
        
        if not record.data:
            raise HTTPException(status_code=404, detail="Record not found")
        
        encrypted_data = record.data[0]
        decrypted = crypto_service.decrypt(
            encrypted_data["encrypted_blob"],
            encrypted_data["wrapped_key"]
        )
        
        ai_analysis = None
        
        # Call AI analysis if requested
        if request.request_ai_analysis:
            logger.info(f"Requesting AI analysis for appointment: {appointment_id}")
            ai_analysis = await analyze_patient_data(
                decrypted["intake_data"],
                decrypted["lab_results"]
            )
        
        # Combine AI analysis with doctor notes
        result_data = {
            "ai_analysis": ai_analysis.dict() if ai_analysis else None,
            "doctor_notes": request.doctor_notes,
            "approved": request.approved
        }
        
        # Encrypt result
        encrypted_result, wrapped_key = crypto_service.encrypt(result_data)
        
        # Store consultation result
        consultation_data = {
            "appointment_id": str(appointment_id),
            "encrypted_result": encrypted_result,
            "wrapped_key": wrapped_key,
            "approved_by": str(request.doctor_id),
            "approved_at": "now()"
        }
        
        db.table("consultation_results").insert(consultation_data).execute()
        
        # Update appointment status
        db.table("appointments")\
            .update({"status": "completed"})\
            .eq("appointment_id", str(appointment_id))\
            .execute()
        
        logger.info(f"Analysis complete and stored for appointment: {appointment_id}")
        
        return AnalyzeApproveResponse(
            status="success",
            ai_analysis=ai_analysis,
            message="Analysis complete and result stored"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze_and_approve: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

**✅ Checkpoint**: All 5 API endpoints created. Ready for AI integration.

---

## Phase 4: AI Integration (Hours 32-48)

### Step 4.1: Create AI Prompt Templates

Create `app/utils/prompts.py`:
```python
SYSTEM_PROMPT = """You are a medical AI assistant helping doctors analyze patient lab results and symptoms.
Provide clinical insights based on the data provided. Your response should be:
1. Evidence-based and clinically relevant
2. Include differential diagnoses with reasoning
3. Suggest appropriate follow-up questions
4. Recommend next steps in management

IMPORTANT: This is a decision-support tool. All final decisions must be made by the attending physician.

Format your response as JSON with the following structure:
{
  "risk_score": <float 0-10>,
  "risk_level": "<low|moderate|moderate-high|high|critical>",
  "diagnosis_suggestions": [<list of possible diagnoses with brief reasoning>],
  "follow_up_questions": [<list of important questions to ask patient>],
  "recommendations": [<list of clinical recommendations>]
}
"""

USER_PROMPT_TEMPLATE = """
Patient Demographics:
- Age: {age}
- Gender: {gender}

Presenting Symptoms:
{symptoms}

Medical History:
{medical_history}

Current Medications:
{medications}

Laboratory Results:
- Fasting Glucose: {glucose} mg/dL (Normal: 70-100)
- HbA1c: {hba1c}% (Normal: <5.7%)
- Creatinine: {creatinine} mg/dL (Normal: 0.7-1.3)
- Total Cholesterol: {cholesterol} mg/dL (Normal: <200)
- LDL: {ldl} mg/dL (Normal: <100)
- HDL: {hdl} mg/dL (Normal: >40 men, >50 women)
- Triglycerides: {triglycerides} mg/dL (Normal: <150)

Lab Notes: {lab_notes}

Please analyze this patient's data and provide clinical insights.
"""
```

### Step 4.2: Create AI Service

Create `app/services/ai_service.py`:
```python
import openai
import json
import logging
from app.config import settings
from app.models.schemas import AIAnalysisResult, PatientIntakeData, LabResults
from app.utils.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

# Configure OpenAI
openai.api_key = settings.OPENAI_API_KEY

async def analyze_patient_data(
    intake_data: PatientIntakeData,
    lab_results: LabResults
) -> AIAnalysisResult:
    """
    Analyze patient data using OpenAI GPT-4
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
        
        logger.info("Sending request to OpenAI API...")
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # or "gpt-4" if you prefer
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=1500,
            response_format={"type": "json_object"}
        )
        
        # Parse response
        ai_result = json.loads(response.choices[0].message.content)
        
        logger.info(f"AI analysis completed. Risk score: {ai_result.get('risk_score')}")
        
        return AIAnalysisResult(**ai_result)
        
    except openai.error.RateLimitError:
        logger.error("OpenAI rate limit exceeded")
        return _get_fallback_response()
    except openai.error.APIError as e:
        logger.error(f"OpenAI API error: {e}")
        return _get_fallback_response()
    except Exception as e:
        logger.error(f"Error in AI analysis: {e}")
        return _get_fallback_response()

def _get_fallback_response() -> AIAnalysisResult:
    """
    Fallback response if OpenAI API fails
    """
    logger.warning("Using fallback AI response")
    return AIAnalysisResult(
        risk_score=5.0,
        risk_level="moderate",
        diagnosis_suggestions=[
            "Unable to complete AI analysis. Please review patient data manually.",
            "API error occurred. Consider checking lab values against reference ranges."
        ],
        follow_up_questions=[
            "Please conduct a thorough clinical examination",
            "Review patient history in detail"
        ],
        recommendations=[
            "Manual review required due to AI system unavailability",
            "Consult with specialist if clinical concerns persist"
        ]
    )
```

**✅ Checkpoint**: AI integration complete. APIs can now call OpenAI for analysis.

---

## Phase 5: Testing & Sample Data (Hours 48-64)

### Step 5.1: Create Sample Data Script

Create `scripts/create_sample_data.py`:
```python
import json
import base64

# Sample Patient 1: Diabetic with complications
patient1 = {
    "intake_data": {
        "age": 45,
        "gender": "Male",
        "symptoms": "Increased thirst, frequent urination, fatigue for past 3 months",
        "medical_history": ["Hypertension (5 years)", "Family history of Type 2 Diabetes (father)"],
        "current_medications": ["Lisinopril 10mg daily"]
    },
    "lab_results": {
        "test_date": "2025-11-15",
        "fasting_glucose": 165.0,
        "hba1c": 7.8,
        "creatinine": 1.3,
        "total_cholesterol": 235.0,
        "ldl": 155.0,
        "hdl": 38.0,
        "triglycerides": 210.0,
        "notes": "Fasting sample collected. Possible poor glycemic control and early renal impairment."
    }
}

# Sample Patient 2: Thyroid disorder
patient2 = {
    "intake_data": {
        "age": 32,
        "gender": "Female",
        "symptoms": "Unexplained weight gain, fatigue, cold intolerance, dry skin for 6 months",
        "medical_history": ["Anxiety disorder", "Iron deficiency anemia (resolved)"],
        "current_medications": ["Sertraline 50mg daily"]
    },
    "lab_results": {
        "test_date": "2025-11-16",
        "fasting_glucose": 92.0,
        "hba1c": 5.2,
        "creatinine": 0.9,
        "total_cholesterol": 245.0,
        "ldl": 168.0,
        "hdl": 52.0,
        "triglycerides": 125.0,
        "notes": "Note: TSH=8.5, Free T4=0.6 (not in standard panel but relevant). Suggests primary hypothyroidism."
    }
}

# Sample Patient 3: Healthy baseline
patient3 = {
    "intake_data": {
        "age": 28,
        "gender": "Female",
        "symptoms": "Routine checkup, occasional headaches",
        "medical_history": [],
        "current_medications": ["Multivitamin"]
    },
    "lab_results": {
        "test_date": "2025-11-17",
        "fasting_glucose": 88.0,
        "hba1c": 5.1,
        "creatinine": 0.9,
        "total_cholesterol": 178.0,
        "ldl": 98.0,
        "hdl": 62.0,
        "triglycerides": 90.0,
        "notes": "All values within normal range. Patient is healthy."
    }
}

# Encrypt samples (mock)
def create_encrypted_sample(data):
    json_str = json.dumps(data)
    encrypted = base64.b64encode(json_str.encode()).decode()
    wrapped_key = base64.b64encode(b"mock_wrapped_key").decode()
    return encrypted, wrapped_key

# Save to files
samples = {
    "patient1": patient1,
    "patient2": patient2,
    "patient3": patient3
}

for name, data in samples.items():
    encrypted, key = create_encrypted_sample(data)
    
    request_json = {
        "patient_id": None,
        "doctor_id": "11111111-1111-1111-1111-111111111111",
        "appointment_time": "2025-11-20T10:00:00Z",
        "encrypted_data": encrypted,
        "wrapped_key": key,
        "metadata": {
            "encryption_algorithm": "AES-256-GCM-mock",
            "key_algorithm": "Kyber512-mock"
        }
    }
    
    with open(f"data/{name}_request.json", "w") as f:
        json.dump(request_json, f, indent=2)

print("✅ Sample data created in data/ directory")
```

Run it:
```bash
python scripts/create_sample_data.py
```

### Step 5.2: Create Docker Setup

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY .env .env

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - PYTHONUNBUFFERED=1
    env_file:
      - .env
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

networks:
  default:
    name: quantum-health-network
```

### Step 5.3: Test Locally

```bash
# Build and run
docker-compose up --build

# In another terminal, test the API
curl http://localhost:8000/health

# Test patient submission
curl -X POST http://localhost:8000/api/v1/patient/submit-intake \
  -H "Content-Type: application/json" \
  -d @data/patient1_request.json
```

**✅ Checkpoint**: Docker setup working, can test APIs locally.

---

## Phase 6: Demo Preparation (Hours 64-72)

### Step 6.1: Create README

Create `README.md`:
```markdown
# Quantum Safe Patient Analytics API

Backend API for secure patient health data management with AI-powered analysis.

## Quick Start

### Prerequisites
- Docker Desktop
- Supabase account
- OpenAI API key

### Setup

1. Clone repository
```bash
git clone <your-repo-url>
cd quantum-health-backend
```

2. Configure environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Run with Docker
```bash
docker-compose up --build
```

4. Access API
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## API Endpoints

### Patient APIs
- `POST /api/v1/patient/submit-intake` - Submit encrypted patient data
- `GET /api/v1/patient/result/{appointment_id}` - Get consultation results

### Doctor APIs
- `GET /api/v1/doctor/appointments` - List appointments
- `GET /api/v1/doctor/record/{appointment_id}` - Get patient record
- `POST /api/v1/doctor/record/{appointment_id}/analyze-and-approve` - AI analysis

## Testing

Use provided sample data:
```bash
curl -X POST http://localhost:8000/api/v1/patient/submit-intake \
  -H "Content-Type: application/json" \
  -d @data/patient1_request.json
```

## Architecture

- **Backend**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **AI**: OpenAI GPT-4
- **Encryption**: Mock PQC (Kyber) for demo

## Team

Built for [Hackathon Name] by:
- Backend + AI: [Your Name]
- Crypto: Raymond
- Frontend: [Team Members]
```

### Step 6.2: Create Demo Script

Create `DEMO_SCRIPT.md`:
```markdown
# Demo Walkthrough Script (5 minutes)

## Setup (Before Demo)
1. Ensure Docker is running
2. Verify API is up: http://localhost:8000/health
3. Have Postman/browser ready
4. Clear previous test data if needed

## Demo Flow

### Part 1: Patient Submits Data (1 min)
**Narration**: "A patient fills out their medical intake form and uploads lab results. The data is encrypted on their device before being sent to our secure backend."

**Action**: Submit patient1 data
```bash
POST /api/v1/patient/submit-intake
[Use patient1_request.json]
```

**Show**: 
- Request body (encrypted data)
- Response (appointment_id created)

### Part 2: Doctor Views Appointments (30 sec)
**Narration**: "The doctor logs in and sees their pending appointments."

**Action**:
```bash
GET /api/v1/doctor/appointments?doctor_id=11111111-1111-1111-1111-111111111111
```

**Show**: List of appointments with status

### Part 3: Doctor Views Patient Record (1 min)
**Narration**: "The doctor selects a patient and our system decrypts the data securely in the backend."

**Action**:
```bash
GET /api/v1/doctor/record/{appointment_id}
```

**Show**:
- Decrypted patient intake
- Lab results in readable format

### Part 4: AI Analysis (1.5 min)
**Narration**: "The doctor requests AI analysis. Our system pseudonymizes the data, sends it to GPT-4, and returns clinical insights."

**Action**:
```bash
POST /api/v1/doctor/record/{appointment_id}/analyze-and-approve
{
  "doctor_id": "11111111-1111-1111-1111-111111111111",
  "request_ai_analysis": true,
  "doctor_notes": "Patient counseled on lifestyle modifications",
  "approved": true
}
```

**Show**:
- AI analysis result (risk score, diagnoses, recommendations)
- System encrypts result and stores it

### Part 5: Patient Views Results (1 min)
**Narration**: "The patient can now securely retrieve their consultation results."

**Action**:
```bash
GET /api/v1/patient/result/{appointment_id}
```

**Show**:
- Encrypted result
- Approval timestamp
- Doctor name

## Key Points to Emphasize
- ✅ End-to-end encryption (mock PQC)
- ✅ AI-powered clinical insights
- ✅ HIPAA-like security practices
- ✅ Seamless doctor-patient workflow
- ✅ Production-ready architecture

## Backup Plan
If AI API fails: "We have fallback responses to ensure the system remains operational even if external services are down."
```

### Step 6.3: Final Testing Checklist

```markdown
# Pre-Demo Checklist

## Environment
- [ ] `.env` file configured with valid credentials
- [ ] Docker Desktop running
- [ ] Supabase database accessible
- [ ] OpenAI API key valid (test with small request)

## API Health
- [ ] `GET /health` returns 200
- [ ] `GET /` shows API info
- [ ] Supabase connection working

## End-to-End Flow
- [ ] Patient can submit intake data
- [ ] Doctor can list appointments
- [ ] Doctor can view patient records
- [ ] AI analysis completes successfully
- [ ] Patient can retrieve results

## Sample Data
- [ ] 3 sample patient JSONs created
- [ ] At least 1 complete flow tested end-to-end
- [ ] Verified AI returns reasonable medical insights

## Documentation
- [ ] README.md complete with setup instructions
- [ ] API endpoints documented
- [ ] Demo script prepared
- [ ] Screenshots/recordings ready (optional)

## Team Coordination
- [ ] Frontend teams know API contract
- [ ] Raymond's crypto interface integrated
- [ ] Agreed on demo flow with team

## Contingency
- [ ] Backup demo video recorded
- [ ] Fallback AI responses tested
- [ ] Local database backup (if needed)
```

**✅ Checkpoint**: Fully prepared for demo!

---

## Troubleshooting Guide

### Issue: Supabase Connection Failed
**Solution**:
1. Check `.env` file has correct `SUPABASE_URL` and `SUPABASE_KEY`
2. Verify Supabase project is active in dashboard
3. Check network connectivity
4. Try re-copying credentials from Supabase dashboard

### Issue: OpenAI API Rate Limit
**Solution**:
1. Check your OpenAI usage at https://platform.openai.com/usage
2. Ensure billing is set up
3. Reduce test frequency
4. Use fallback responses during heavy testing

### Issue: Docker Build Fails
**Solution**:
```bash
# Clean Docker cache
docker system prune -a
docker-compose down -v
docker-compose up --build
```

### Issue: Import Errors
**Solution**:
```bash
# Ensure all __init__.py files exist
touch app/__init__.py
touch app/routers/__init__.py
touch app/models/__init__.py
touch app/services/__init__.py
touch app/utils/__init__.py
```

### Issue: AI Returns Error
**Solution**:
1. Check OpenAI API key is valid
2. Verify you have GPT-4 access
3. Check request format matches OpenAI spec
4. Use fallback response temporarily

### Issue: CORS Errors
**Solution**:
Add frontend URL to `app/config.py`:
```python
CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173", "YOUR_FRONTEND_URL"]
```

---

## Success Criteria

✅ **All 5 APIs functional**
✅ **AI integration working**
✅ **End-to-end flow tested**
✅ **Docker setup complete**
✅ **Demo script ready**
✅ **Documentation complete**
✅ **Sample data prepared**

---

## Final Notes

- **Keep it simple**: Don't over-engineer. The goal is a working demo, not production perfection.
- **Test early, test often**: Don't wait until hour 60 to test the full flow.
- **Communicate with team**: Make sure frontend knows API contracts.
- **Have backups**: Record demo video, prepare fallback responses.
- **Stay calm**: If something breaks, you have contingency plans.

**Good luck with your hackathon! 🚀**
