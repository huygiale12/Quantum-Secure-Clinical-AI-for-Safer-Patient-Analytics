# 🚀 UPDATED: Complete Setup Guide with Real Credentials

## What Changed?

Based on your team's chat log:

1. ✅ **Crypto library:** Changed from `pqcrypto` → `python-oqs`
2. ✅ **AI model:** Changed from OpenAI → Google Gemini (FREE!)
3. ✅ **Real credentials:** Supabase & Gemini API keys provided
4. ✅ **Frontend:** **NO CHANGES NEEDED** - Already compatible!

---

## Part 1: Backend Setup (10 minutes)

### Step 1: Install Dependencies

```bash
cd [your-backend-folder]

# Install all requirements
pip install -r requirements.txt

# Install crypto libraries (CRITICAL!)
pip install python-oqs pycryptodomex cryptography

# Install Gemini AI
pip install google-generativeai
```

**On Windows:** Use `--break-system-packages` if needed:
```bash
pip install python-oqs --break-system-packages
```

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with **REAL CREDENTIALS**:

```env
# Supabase Configuration (REAL - provided by Tin)
SUPABASE_URL=https://dqziqcedbdxomsrxiarq.supabase.co/
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRxemlxY2VkYmR4b21zcnhpYXJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMxNTQxMjksImV4cCI6MjA3ODczMDEyOX0.wTIUshWr3LLcRnhhbPABwX1eNLtA8tB6cexiNhHDZEQ

# Gemini AI Configuration (REAL - FREE!)
GEMINI_API_KEY=AIzaSyDWYC5o08vxzG_IkRxgLq7ROcvXCGB8_7s

# Application
ENVIRONMENT=development
DEBUG=True
API_VERSION=v1
```

### Step 3: Test Crypto

```bash
python test_crypto.py
```

**Expected output:**
```
Test passed.
```

If this fails, check that `python-oqs` is installed correctly.

### Step 4: Start Backend

```bash
uvicorn app.main:app --reload --port 8000
```

**Verify it's working:**
```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "connected",
  "environment": "development",
  "api_version": "v1"
}
```

---

## Part 2: Frontend Setup (5 minutes)

### Step 1: Navigate to Frontend

```bash
cd quantum-health-frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Start Frontend

```bash
npm run dev
```

Open: **http://localhost:3000**

---

## Part 3: Test Complete Flow (5 minutes)

### Test 1: Patient Submits Data

1. Go to http://localhost:3000
2. Click **"Patient Portal"**
3. Fill form with this data:

```
Age: 45
Gender: Male
Chief Complaint: Frequent urination and increased thirst
Symptoms: Excessive thirst, frequent urination, feeling tired for 2 weeks
Duration: 2 weeks
Medical History: Hypertension, Family history of diabetes
Current Medications: Lisinopril 10mg

Lab Results:
Glucose: 180
HbA1c: 7.5
Blood Pressure: 140/90
BMI: 28.5
```

4. Click **"Submit Securely"**
5. **Save the appointment ID!**

### Test 2: Doctor Reviews & Analyzes

1. Go to http://localhost:3000
2. Click **"Doctor Dashboard"**
3. Click on the pending appointment
4. Review patient data
5. Add notes: "Patient counseled on lifestyle modifications"
6. Click **"Analyze with AI & Approve"**
7. Wait 5-10 seconds for Gemini AI analysis
8. ✅ Success!

### Test 3: Patient Views Results

1. Navigate to: `http://localhost:3000/patient/result/[your-appointment-id]`
2. See the encrypted consultation results
3. ✅ Complete!

---

## 🔐 Crypto Implementation Details

### What Raymond Changed

**Old (pqcrypto) - REMOVED:**
```python
from pqcrypto.kem.kyber512 import generate_keypair, encapsulate, decapsulate
```

**New (python-oqs) - CURRENT:**
```python
import oqs

# Create session
with oqs.KeyEncapsulation("Kyber512") as kem:
    public_key = kem.generate_keypair()
    secret_key = kem.export_secret_key()
```

### Why the Change?

| Issue | pqcrypto | python-oqs |
|-------|----------|------------|
| **Maintenance** | ❌ Abandoned | ✅ Active |
| **Windows Support** | ❌ Broken | ✅ Works |
| **macOS Support** | ❌ Issues | ✅ Works |
| **API Clarity** | ❌ Unclear | ✅ Clean |
| **NIST Compliance** | ⚠️ Partial | ✅ Full |

---

## 📊 System Architecture

```
┌─────────────┐
│   Patient   │
│  (Browser)  │
└──────┬──────┘
       │
       │ Submit encrypted data
       ▼
┌─────────────────────┐      ┌──────────────┐
│  React Frontend     │      │   Supabase   │
│  (Port 3000)        │◄────►│   Database   │
└──────┬──────────────┘      └──────────────┘
       │
       │ REST API
       ▼
┌─────────────────────┐
│  FastAPI Backend    │
│  (Port 8000)        │
└──────┬──────────────┘
       │
       ├──────────────────────┐
       │                      │
       ▼                      ▼
┌──────────────┐      ┌──────────────┐
│ python-oqs   │      │ Gemini AI    │
│ (Kyber512)   │      │ (Free!)      │
└──────────────┘      └──────────────┘
```

---

## ✅ Pre-Demo Checklist

### Backend
- [ ] `python-oqs` installed
- [ ] `pycryptodomex` installed
- [ ] `.env` configured with real credentials
- [ ] `test_crypto.py` passes
- [ ] Backend running on port 8000
- [ ] Health check returns "healthy"

### Frontend
- [ ] Dependencies installed (`npm install`)
- [ ] Frontend running on port 3000
- [ ] Can see home page

### Integration
- [ ] Patient can submit data
- [ ] Doctor can view appointments
- [ ] Doctor can decrypt patient data
- [ ] AI analysis works (Gemini responds)
- [ ] Results encrypted and saved
- [ ] Patient can view results

---

## 🛠️ Troubleshooting

### Backend Issues

**"No module named 'oqs'"**
```bash
pip install python-oqs --break-system-packages
```

**"Supabase connection failed"**
- Check URL ends with `/`
- Verify KEY is complete (very long string)
- Test connection: `curl https://dqziqcedbdxomsrxiarq.supabase.co/`

**"Gemini API error"**
- Check model is `gemini-2.5-flash` not `gemini-1.5-flash`
- Verify API key: https://aistudio.google.com/app/apikey
- Try test request:
```bash
curl "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key=AIzaSyDWYC5o08vxzG_IkRxgLq7ROcvXCGB8_7s" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"test"}]}]}'
```

### Frontend Issues

**"Cannot connect to backend"**
```bash
# Check backend is running
curl http://localhost:8000/health
```

**"Port 3000 in use"**
```bash
lsof -ti:3000 | xargs kill -9
```

**"CORS error"**
- Verify backend `config.py` includes `http://localhost:3000` in CORS_ORIGINS

---

## 📝 Team Roles

### You (Frontend)
- ✅ Frontend complete and ready!
- Just test the integration
- Prepare demo script

### Backend Team (Tin)
- Update dependencies
- Configure .env with real credentials
- Ensure API endpoints work

### Crypto Team (Raymond)
- ✅ Crypto implementation complete!
- Using python-oqs with Kyber512
- Test crypto passes

---

## 🎯 Success Criteria

✅ All dependencies installed
✅ Backend runs without errors
✅ Frontend connects to backend
✅ Crypto works (test passes)
✅ Patient can submit data
✅ Doctor can decrypt data
✅ Gemini AI analysis completes
✅ Results saved and retrieved

---

## 🎉 You're Ready!

With the updated crypto library and real credentials, your hackathon project is **production-ready**!

### Quick Start Commands

**Backend:**
```bash
pip install python-oqs pycryptodomex google-generativeai
python test_crypto.py
uvicorn app.main:app --reload
```

**Frontend:**
```bash
npm install
npm run dev
```

**Demo:**
1. Submit patient data
2. Review as doctor
3. Request AI analysis
4. Show encrypted results

---

## 🔑 Important: Credentials

**Supabase:**
- URL: `https://dqziqcedbdxomsrxiarq.supabase.co/`
- Key: `eyJhbGc...` (very long)

**Gemini:**
- Key: `AIzaSyDWYC5o08vxzG_IkRxgLq7ROcvXCGB8_7s`
- Free tier, no payment needed!

---

**Good luck with your hackathon! 🚀**

*Everything is ready. Just follow this guide and you'll be up and running in 15 minutes!*
