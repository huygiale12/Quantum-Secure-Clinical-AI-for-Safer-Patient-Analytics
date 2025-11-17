# 🎬 Demo Flow Diagram

## Complete User Journey (5 Minutes)

```
┌─────────────────────────────────────────────────────────────────┐
│                     DEMO START (0:00)                            │
│                  http://localhost:3000                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    HOME PAGE (0:00-0:30)                         │
├─────────────────────────────────────────────────────────────────┤
│  👁️  SHOW:                                                       │
│     • Hero section with security badge                          │
│     • 3 feature cards (Security, AI, Real-time)                 │
│     • Patient Portal & Doctor Dashboard buttons                 │
│                                                                  │
│  🗣️  SAY:                                                        │
│     "Quantum-Secure Clinical AI combines post-quantum           │
│      cryptography with AI-powered medical analysis"             │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
    ┌───────────────────────┐  ┌───────────────────────┐
    │   PATIENT FLOW        │  │   DOCTOR FLOW         │
    │   (0:30-2:00)         │  │   (2:00-4:30)         │
    └───────────────────────┘  └───────────────────────┘
```

---

## Patient Flow (1:30 min)

```
PATIENT PORTAL
http://localhost:3000/patient

┌──────────────────────────────────────┐
│  STEP 1: Fill Form (0:30-1:30)       │
├──────────────────────────────────────┤
│                                       │
│  Personal Info:                       │
│  ├─ Age: 45                          │
│  └─ Gender: Male                     │
│                                       │
│  Medical Info:                        │
│  ├─ Chief Complaint:                 │
│  │  "Frequent urination and thirst"  │
│  ├─ Symptoms: [detailed]             │
│  ├─ Duration: "2 weeks"              │
│  ├─ Medical History:                 │
│  │  "Hypertension, Family diabetes"  │
│  └─ Medications: "Lisinopril 10mg"   │
│                                       │
│  Lab Results:                         │
│  ├─ Glucose: 180 mg/dL               │
│  ├─ HbA1c: 7.5%                      │
│  ├─ Blood Pressure: 140/90           │
│  └─ BMI: 28.5                        │
│                                       │
│  [Submit Securely] ←─────────────┐   │
│                                   │   │
└───────────────────────────────────│───┘
                                    │
                    🔐 ENCRYPTION   │
                                    ▼
┌──────────────────────────────────────┐
│  STEP 2: Success (1:30-2:00)         │
├──────────────────────────────────────┤
│                                       │
│  ✅ Submission Successful!            │
│                                       │
│  Your Appointment ID:                 │
│  ┌─────────────────────────────────┐ │
│  │ a1b2c3d4-e5f6-7890-abcd-...     │ │
│  └─────────────────────────────────┘ │
│                                       │
│  [Check Results] [Submit Another]    │
│                                       │
│  🗣️ SAY:                              │
│  "Data is encrypted before leaving   │
│   the browser using Kyber512"        │
│                                       │
└──────────────────────────────────────┘
```

---

## Doctor Flow (2:30 min)

```
DOCTOR DASHBOARD
http://localhost:3000/doctor

┌──────────────────────────────────────┐
│  STEP 1: View Appointments           │
│         (2:00-2:30)                   │
├──────────────────────────────────────┤
│                                       │
│  Appointments List:                   │
│                                       │
│  ┌─────────────────────────────────┐ │
│  │ 📋 Patient a1b2c3d4...          │ │
│  │    Nov 15, 2025                  │ │
│  │    Status: pending ⏰            │ │
│  │    [Select] ◄────────────┐      │ │
│  └─────────────────────────────────┘ │
│                                   │   │
│  🗣️ SAY:                          │   │
│  "Doctor logs in and sees their   │   │
│   pending appointments"           │   │
│                                   │   │
└───────────────────────────────────│───┘
                                    │
                                    ▼
┌──────────────────────────────────────┐
│  STEP 2: Review Patient Data         │
│         (2:30-3:30)                   │
├──────────────────────────────────────┤
│                                       │
│  Patient Information:                 │
│  ├─ Age: 45, Male                    │
│  └─ Complaint: "Frequent urination"  │
│                                       │
│  Symptoms:                            │
│  "Excessive thirst, frequent          │
│   urination, fatigue..."              │
│  Duration: 2 weeks                    │
│                                       │
│  Medical History:                     │
│  • Hypertension                       │
│  • Family history of diabetes         │
│                                       │
│  Current Medications:                 │
│  • Lisinopril 10mg                    │
│                                       │
│  Lab Results:                         │
│  ┌────────┬──────┬─────┬──────┐     │
│  │Glucose │HbA1c │  BP │ BMI  │     │
│  │  180   │ 7.5% │140/ │28.5  │     │
│  │        │      │ 90  │      │     │
│  └────────┴──────┴─────┴──────┘     │
│                                       │
│  🗣️ SAY:                              │
│  "System decrypts the data securely  │
│   for doctor review"                  │
│                                       │
└──────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────┐
│  STEP 3: AI Analysis                 │
│         (3:30-4:30)                   │
├──────────────────────────────────────┤
│                                       │
│  Doctor's Notes:                      │
│  ┌─────────────────────────────────┐ │
│  │ Patient counseled on lifestyle   │ │
│  │ modifications and medication     │ │
│  │ adherence. Follow-up in 3 months │ │
│  └─────────────────────────────────┘ │
│                                       │
│  [🧠 Analyze with AI & Approve]      │
│         ▼ (Click)                     │
│                                       │
│  ⏳ Loading... (5-10 seconds)         │
│                                       │
│  🗣️ SAY:                              │
│  "AI analyzes the data and provides  │
│   clinical insights. The data is     │
│   pseudonymized before being sent    │
│   to Gemini AI"                       │
│                                       │
│         ▼                             │
│                                       │
│  ✅ Analysis Complete!                │
│                                       │
│  Results encrypted and saved for     │
│  patient access                       │
│                                       │
└──────────────────────────────────────┘
```

---

## Optional: Patient Views Results (0:30 min)

```
PATIENT RESULT PAGE
http://localhost:3000/patient/result/a1b2c3d4...

┌──────────────────────────────────────┐
│  Consultation Results                 │
├──────────────────────────────────────┤
│                                       │
│  ✅ Consultation Completed            │
│                                       │
│  Reviewed by: Dr. Sarah Chen          │
│  Date: Nov 15, 2025, 2:45 PM         │
│                                       │
│  Your Results:                        │
│  ┌─────────────────────────────────┐ │
│  │ [Encrypted result data]          │ │
│  │ eyJhbGc...                       │ │
│  └─────────────────────────────────┘ │
│                                       │
│  🔐 Privacy Note:                     │
│  In production, this would be        │
│  decrypted on your device            │
│                                       │
│  Next Steps:                          │
│  • Review with your doctor           │
│  • Follow recommendations            │
│  • Contact if questions              │
│                                       │
└──────────────────────────────────────┘
```

---

## AI Analysis Output Example

```
┌─────────────────────────────────────────────┐
│  AI ANALYSIS RESULT (Behind the scenes)     │
├─────────────────────────────────────────────┤
│                                              │
│  Risk Score: 65/100 ⚠️                       │
│                                              │
│  Primary Concerns:                           │
│  • Elevated blood glucose                    │
│  • High HbA1c indicating poor control        │
│  • Hypertension                              │
│                                              │
│  Differential Diagnoses:                     │
│  • Type 2 Diabetes Mellitus                  │
│  • Metabolic Syndrome                        │
│  • Insulin Resistance                        │
│                                              │
│  Recommended Tests:                          │
│  • Fasting glucose repeat                    │
│  • Lipid panel                               │
│  • Kidney function tests                     │
│  • Eye examination                           │
│                                              │
│  Follow-up Questions:                        │
│  • Family history details?                   │
│  • Diet and exercise habits?                 │
│  • Previous glucose readings?                │
│                                              │
│  Recommendations:                            │
│  • Start metformin therapy                   │
│  • Lifestyle modifications                   │
│  • Blood pressure management                 │
│  • Follow-up in 3 months                     │
│                                              │
│  Clinical Summary:                           │
│  "45-year-old male with classic symptoms     │
│   of diabetes, elevated glucose and HbA1c.   │
│   Recommend immediate intervention..."       │
│                                              │
└─────────────────────────────────────────────┘
```

---

## Demo Timing Breakdown

| Section | Duration | Key Points |
|---------|----------|------------|
| **Home Page** | 0:00-0:30 | Intro, features, navigation |
| **Patient Portal** | 0:30-1:30 | Form filling, encryption |
| **Patient Success** | 1:30-2:00 | Confirmation, appointment ID |
| **Doctor Login** | 2:00-2:30 | Appointment list |
| **Patient Review** | 2:30-3:30 | Data decryption, review |
| **AI Analysis** | 3:30-4:30 | Request analysis, wait, results |
| **Wrap Up** | 4:30-5:00 | Features recap, Q&A |

---

## Visual Cues During Demo

### Patient Portal
- ✅ Green checkmarks when fields are filled
- 🔐 Encryption badge in header
- ⏳ Loading spinner during submission
- ✨ Success animation on completion

### Doctor Dashboard
- 📋 Appointment cards with status colors
- 🟡 Yellow = Pending
- 🟢 Green = Completed
- 🧠 AI badge when analysis done
- ⏳ Loading during AI analysis
- ✅ Success message when approved

---

## Talking Points

### Security (30 seconds)
> "Our platform uses Kyber512 post-quantum cryptography, ensuring patient data remains secure even against future quantum computers. Data is encrypted before it ever leaves the patient's device."

### AI Integration (30 seconds)
> "We integrate Google's Gemini AI to provide real-time clinical insights. The AI analyzes patient data and provides risk scores, differential diagnoses, and evidence-based recommendations."

### Workflow (30 seconds)
> "The workflow is seamless: patients submit encrypted data, doctors decrypt and review it securely, request AI analysis, and approve results—all within minutes instead of days."

---

## Backup Plan

If something goes wrong:

1. **Backend Down**
   - Have screenshots ready
   - Explain what would happen
   - Show code structure

2. **AI Takes Too Long**
   - "In production, this typically takes 5-10 seconds"
   - Continue with other features

3. **Browser Issues**
   - Have backup browser ready
   - Have video recording ready

---

## Post-Demo Q&A Preparation

### Expected Questions

**Q: How does the encryption work?**
A: "We use Kyber512, a post-quantum cryptography algorithm that creates shared secrets between patient and doctor without directly sharing keys."

**Q: What AI model do you use?**
A: "Google's Gemini 2.5 Flash for fast, accurate clinical analysis."

**Q: Is this HIPAA compliant?**
A: "This is a proof of concept. In production, we'd implement full HIPAA compliance with proper audit logs, access controls, and encryption at rest."

**Q: Can it scale?**
A: "Built on FastAPI and React with Supabase backend—designed to scale horizontally."

**Q: What about real-time notifications?**
A: "Great future feature! Could implement with WebSockets or Server-Sent Events."

---

## Success Indicators

✅ Patient data successfully submitted
✅ Doctor can view appointments
✅ Patient data decrypted properly
✅ AI analysis completes
✅ Results encrypted and stored
✅ Patient can view results

---

**Remember:** Practice makes perfect! Run through this flow 2-3 times before the actual demo.

**Good luck! 🚀**
