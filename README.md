# Quantum-Safe Patient Analytics & Consultation System

A secure healthcare data management system with AI-powered clinical analysis, built for the hackathon. This backend API uses hybrid encryption (simulated post-quantum cryptography + AES-256-GCM) to protect sensitive patient data.

## 🏥 Project Overview

This system enables secure patient-doctor consultations with end-to-end encryption:

- **Patients** submit encrypted medical intake forms and lab results
- **Doctors** decrypt and review patient data securely
- **AI** (Google Gemini) analyzes patient data and provides clinical insights
- **Results** are encrypted and returned to patients

### Key Features

- 🔐 **Hybrid Encryption**: Simulated Kyber (post-quantum) + AES-256-GCM
- 🤖 **AI-Powered Analysis**: Google Gemini for clinical risk assessment
- 💾 **Secure Storage**: Supabase (PostgreSQL) with encrypted data at rest
- 🚀 **Fast API**: Built with FastAPI for high performance
- 📊 **5 Core Endpoints**: Complete patient-doctor workflow

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Patient   │────────▶│    Backend   │────────▶│   Doctor    │
│  (Encrypt)  │         │  (FastAPI)   │         │  (Decrypt)  │
└─────────────┘         └──────────────┘         └─────────────┘
                              │    │
                              │    └──────────▶ Google Gemini AI
                              │
                              └──────────▶ Supabase Database
```

### Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: Supabase (PostgreSQL)
- **AI**: Google Gemini 2.5 Flash (Free tier)
- **Encryption**: 
  - Simulated Kyber key encapsulation
  - AES-256-GCM symmetric encryption
  - HMAC-SHA256 authentication
- **Deployment**: Docker-ready

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Supabase account (free tier)
- Google Gemini API key (free)

### Installation

1. **Clone the repository**
   ```bash
   cd Quantum-Secure-Clinical-AI-for-Safer-Patient-Analytics
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # Supabase Configuration
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key-here

   # Google Gemini AI (Free)
   GEMINI_API_KEY=your-gemini-api-key-here

   # Application Settings
   ENVIRONMENT=development
   DEBUG=True
   API_VERSION=v1
   ```

4. **Set up the database**

   Go to your Supabase project → SQL Editor and run:
   ```sql
   -- Enable UUID extension
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

   -- Create tables
   CREATE TABLE patients (
       patient_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       created_at TIMESTAMP DEFAULT NOW()
   );

   CREATE TABLE doctors (
       doctor_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       name VARCHAR(255) NOT NULL,
       specialty VARCHAR(100),
       created_at TIMESTAMP DEFAULT NOW()
   );

   CREATE TABLE appointments (
       appointment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       patient_id UUID REFERENCES patients(patient_id),
       doctor_id UUID REFERENCES doctors(doctor_id),
       appointment_time TIMESTAMP NOT NULL,
       status VARCHAR(50) DEFAULT 'pending',
       created_at TIMESTAMP DEFAULT NOW()
   );

   CREATE TABLE encrypted_records (
       record_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       appointment_id UUID REFERENCES appointments(appointment_id) UNIQUE,
       encrypted_blob TEXT NOT NULL,
       wrapped_key TEXT NOT NULL,
       metadata JSONB,
       created_at TIMESTAMP DEFAULT NOW()
   );

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

5. **Run tests**
   ```bash
   python run_tests.py
   ```

   You should see:
   ```
   🎉 ALL TESTS PASSED (5/5)
   ✅ Your backend is ready to use!
   ```

6. **Start the server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API**
   - API Root: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 📡 API Endpoints

### Patient Endpoints

#### 1. Submit Patient Intake
```http
POST /api/v1/patient/submit-intake
```

**Request Body:**
```json
{
  "encrypted_intake": "base64_encrypted_intake_data",
  "encrypted_lab_results": "base64_encrypted_lab_results",
  "wrapped_key": "base64_wrapped_encryption_key",
  "appointment_time": "2025-11-20T10:00:00Z",
  "doctor_id": "11111111-1111-1111-1111-111111111111"
}
```

**Response:**
```json
{
  "appointment_id": "uuid-here",
  "status": "pending",
  "message": "Your data has been securely submitted..."
}
```

#### 2. Get Consultation Result
```http
GET /api/v1/patient/result/{appointment_id}
```

**Response:**
```json
{
  "appointment_id": "uuid-here",
  "encrypted_result": "base64_encrypted_result",
  "wrapped_key": "base64_wrapped_key",
  "approved_by_doctor": "Dr. Sarah Chen",
  "approved_at": "2025-11-20T10:30:00Z",
  "status": "completed"
}
```

### Doctor Endpoints

#### 3. List Appointments
```http
GET /api/v1/doctor/appointments?doctor_id={uuid}
```

**Response:**
```json
[
  {
    "appointment_id": "uuid-here",
    "patient_id": "uuid-here",
    "appointment_time": "2025-11-20T10:00:00Z",
    "status": "pending",
    "has_ai_analysis": false,
    "created_at": "2025-11-20T09:00:00Z"
  }
]
```

#### 4. Get Patient Record
```http
GET /api/v1/doctor/record/{appointment_id}
```

**Response:**
```json
{
  "appointment_id": "uuid-here",
  "patient_id": "uuid-here",
  "intake_data": {
    "age": 45,
    "gender": "Male",
    "chief_complaint": "Increased thirst and frequent urination",
    "medical_history": ["Hypertension"],
    "current_medications": ["Lisinopril 10mg"],
    "allergies": ["Penicillin"],
    "symptoms": "Fatigue, increased thirst...",
    "symptom_duration": "3 months"
  },
  "lab_results": {
    "glucose": 165.0,
    "hba1c": 7.8,
    "cholesterol": 235.0,
    "triglycerides": 210.0,
    "hdl": 38.0,
    "ldl": 155.0,
    "blood_pressure": "145/92",
    "bmi": 28.5
  },
  "appointment_time": "2025-11-20T10:00:00Z",
  "status": "pending"
}
```

#### 5. Analyze and Approve
```http
POST /api/v1/doctor/record/{appointment_id}/analyze-and-approve
```

**Request Body:**
```json
{
  "doctor_id": "11111111-1111-1111-1111-111111111111",
  "request_ai_analysis": true,
  "doctor_notes": "Patient counseled on lifestyle modifications",
  "approved": true
}
```

**Response:**
```json
{
  "appointment_id": "uuid-here",
  "encrypted_result": "base64_encrypted_analysis",
  "wrapped_key": "base64_wrapped_key",
  "approved_by": "uuid-here",
  "approved_at": "2025-11-20T10:30:00Z",
  "doctor_name": "Dr. Sarah Chen"
}
```

The AI analysis (encrypted in the result) includes:
- Risk score (0-100)
- Primary concerns
- Differential diagnoses
- Recommended tests
- Follow-up questions
- Clinical recommendations
- Clinical summary

## 🔐 Encryption Implementation

### Hybrid Encryption Workflow

```
┌─────────────────────────────────────────────────────────┐
│                    ENCRYPTION                            │
├─────────────────────────────────────────────────────────┤
│ 1. Patient data (JSON) → bytes                          │
│ 2. Generate random ciphertext (simulated Kyber)         │
│ 3. Derive AES session key from ciphertext (SHA-256)     │
│ 4. Encrypt data with AES-256-GCM                        │
│ 5. Generate HMAC-SHA256 for authentication              │
│ 6. Package: nonce + ciphertext → base64 blob            │
│ 7. Return: (encrypted_blob, wrapped_key)                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    DECRYPTION                            │
├─────────────────────────────────────────────────────────┤
│ 1. Decode base64 blob and wrapped key                   │
│ 2. Derive AES session key from ciphertext               │
│ 3. Extract nonce and ciphertext                         │
│ 4. Verify HMAC (data integrity check)                   │
│ 5. Decrypt with AES-256-GCM                             │
│ 6. bytes → JSON → Python dict                           │
└─────────────────────────────────────────────────────────┘
```

### Security Features

- ✅ **AES-256-GCM**: Industry-standard symmetric encryption
- ✅ **HMAC-SHA256**: Message authentication prevents tampering
- ✅ **Random nonces**: Unique per encryption (prevents replay attacks)
- ✅ **Simulated post-quantum**: Architecture ready for real Kyber upgrade
- ✅ **End-to-end encryption**: Data encrypted in transit and at rest

### Crypto Service API

```python
from app.services.crypto_mock import crypto_service

# Encrypt
data = {"patient_info": {...}, "lab_results": {...}}
encrypted_blob, wrapped_key = crypto_service.encrypt(data)

# Decrypt
decrypted_data = crypto_service.decrypt(encrypted_blob, wrapped_key)
```

## 🤖 AI Integration

### Google Gemini 2.5 Flash

The system uses Google's Gemini AI for clinical analysis:

**What it analyzes:**
- Patient demographics and medical history
- Current symptoms and medications
- Lab results (glucose, cholesterol, blood pressure, etc.)

**What it provides:**
- **Risk Score**: 0-100 numerical assessment
- **Primary Concerns**: Key health issues identified
- **Differential Diagnoses**: Possible conditions to investigate
- **Recommended Tests**: Additional diagnostics needed
- **Follow-up Questions**: What to ask the patient
- **Clinical Recommendations**: Treatment and lifestyle advice
- **Summary**: Comprehensive clinical overview

**Fallback Handling:**
- If Gemini API fails, the system provides fallback responses
- Doctors can still approve consultations without AI analysis
- System remains operational even if external AI is unavailable

## 🧪 Testing

### Quick Tests

```bash
# Test crypto encryption/decryption
python test_crypto_quick.py

# Run full test suite
python run_tests.py

# Create sample encrypted patient data
python create_test_data.py
```

### Manual API Testing

#### Using Browser (Recommended)
1. Start server: `uvicorn app.main:app --reload --port 8000`
2. Open: http://localhost:8000/docs
3. Test endpoints interactively in Swagger UI

#### Using curl

```bash
# Health check
curl http://localhost:8000/health

# List doctor appointments
curl "http://localhost:8000/api/v1/doctor/appointments?doctor_id=11111111-1111-1111-1111-111111111111"

# Submit patient data (after creating with create_test_data.py)
curl -X POST http://localhost:8000/api/v1/patient/submit-intake \
  -H "Content-Type: application/json" \
  -d @data/realistic_patient.json
```

### Test Coverage

The `run_tests.py` script verifies:
- ✅ All modules import correctly
- ✅ Crypto encryption/decryption works
- ✅ Configuration loads from .env
- ✅ Database connection established
- ✅ Pydantic models validate correctly

## 📁 Project Structure

```
Quantum-Secure-Clinical-AI-for-Safer-Patient-Analytics/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── database.py             # Supabase client setup
│   ├── routers/
│   │   ├── patient.py          # Patient API endpoints
│   │   └── doctor.py           # Doctor API endpoints
│   ├── services/
│   │   ├── crypto_mock.py      # Encryption service
│   │   ├── db_service.py       # Database operations
│   │   └── ai_service.py       # Gemini AI integration
│   ├── models/
│   │   └── schemas.py          # Pydantic data models
│   └── utils/
│       └── prompts.py          # AI prompt templates
├── tests/
│   ├── test_crypto.py          # Basic crypto tests
│   └── test_kyber_integration.py  # Integration tests
├── data/
│   └── .gitkeep                # Sample data directory
├── test_crypto_quick.py        # Quick crypto verification
├── run_tests.py                # Full test suite
├── create_test_data.py         # Generate sample data
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── README.md                   # This file
├── TESTING_GUIDE.md           # Detailed testing instructions
└── TESTING_README.md          # Quick testing guide
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build the image
docker-compose build

# Start the services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the services
docker-compose down
```

### Docker Compose Configuration

The `docker-compose.yml` includes:
- FastAPI backend on port 8000
- Environment variable injection from `.env`
- Volume mounts for development
- Auto-reload for code changes

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SUPABASE_URL` | Supabase project URL | Yes | - |
| `SUPABASE_KEY` | Supabase anon/public key | Yes | - |
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `ENVIRONMENT` | Environment name | No | `development` |
| `DEBUG` | Debug mode | No | `True` |
| `API_VERSION` | API version prefix | No | `v1` |

### Getting API Keys

**Supabase:**
1. Go to https://supabase.com
2. Create a new project (free tier)
3. Go to Settings → API
4. Copy the URL and anon key

**Google Gemini:**
1. Go to https://aistudio.google.com/app/apikey
2. Create API key (free tier: 1,500 requests/day)
3. Copy the API key

## 🚨 Security Considerations

### Current Implementation (Hackathon/Demo)

✅ **What's Secure:**
- AES-256-GCM encryption for data
- HMAC authentication prevents tampering
- Encrypted data at rest in database
- Environment variables for secrets
- CORS protection
- Input validation with Pydantic

⚠️ **Demo Limitations:**
- Simulated Kyber (not real post-quantum)
- Keys stored in encrypted blob (simplified)
- No authentication/authorization
- No rate limiting
- No audit logging

### Production Hardening Checklist

Before deploying to production:

- [ ] Replace simulated Kyber with real liboqs implementation
- [ ] Implement proper key management (AWS KMS, Azure Key Vault, etc.)
- [ ] Add user authentication (OAuth 2.0, JWT)
- [ ] Implement role-based access control (RBAC)
- [ ] Add rate limiting and DDoS protection
- [ ] Enable audit logging for all operations
- [ ] Use HTTPS/TLS for all communications
- [ ] Implement key rotation policies
- [ ] Add comprehensive monitoring and alerting
- [ ] Conduct security audit and penetration testing
- [ ] Implement backup and disaster recovery
- [ ] Add input sanitization for XSS/SQL injection prevention

## 🤝 Team

This project was built for a 72-hour hackathon by a 4-person team:

- **Backend + AI Integration**: [Your Name]
- **Cryptography**: Raymond
- **Frontend Development**: [Team Members]

## 📚 Additional Resources

### Documentation
- **TESTING_README.md** - Quick start testing guide
- **TESTING_GUIDE.md** - Comprehensive testing instructions
- **http://localhost:8000/docs** - Interactive API documentation (Swagger UI)
- **http://localhost:8000/redoc** - Alternative API documentation (ReDoc)

### External Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Google Gemini API](https://ai.google.dev/docs)
- [AES-GCM Encryption](https://en.wikipedia.org/wiki/Galois/Counter_Mode)
- [Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)

## 🐛 Troubleshooting

### Common Issues

**Problem**: `ModuleNotFoundError: No module named 'cryptography'`
```bash
pip install cryptography --break-system-packages
```

**Problem**: Database connection fails
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check that Supabase project is active
- Ensure database tables are created

**Problem**: Gemini API errors
- Verify `GEMINI_API_KEY` in `.env`
- Check API quota at https://aistudio.google.com/app/apikey
- System will use fallback responses if AI fails

**Problem**: Port 8000 already in use
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001

# Or kill the process using port 8000
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -i :8000
```

## 📄 License

This project is part of a hackathon submission and is provided as-is for educational purposes.

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **Supabase** for the database platform
- **Google** for the Gemini AI API
- **Open Quantum Safe** for post-quantum cryptography research

---

**Built with ❤️ using FastAPI, Supabase, and Google Gemini AI**

**For the Hackathon** | **72 Hours** | **4-Person Team**

---

## 📞 Support

For questions or issues:
1. Check the TESTING_GUIDE.md for detailed instructions
2. Review the troubleshooting section above
3. Check the API documentation at http://localhost:8000/docs
4. Contact the team

**Ready to test?** Run `python run_tests.py` to get started! 🚀
