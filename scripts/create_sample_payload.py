import json
from pathlib import Path
from app.services.crypto_mock import crypto_service


def build_intake():
    return {
        "age": 45,
        "gender": "Male",
        "symptoms": "Increased thirst, fatigue, frequent urination",
        "medical_history": ["Hypertension", "Family history of Type 2 Diabetes"],
        "current_medications": ["Lisinopril 10mg daily"]
    }


def build_lab_results():
    return {
        "test_date": "2025-11-15",
        "fasting_glucose": 165.0,
        "hba1c": 7.8,
        "creatinine": 1.3,
        "total_cholesterol": 235.0,
        "ldl": 155.0,
        "hdl": 38.0,
        "triglycerides": 210.0
    }


def main():
    intake = build_intake()
    labs = build_lab_results()

    encrypted_intake, wrapped_key = crypto_service.encrypt(intake)
    encrypted_labs, _ = crypto_service.encrypt(labs)

    payload = {
        "patient_id": None,
        "doctor_id": "11111111-1111-1111-1111-111111111111",
        "appointment_time": "2025-11-20T10:00:00Z",
        "encrypted_intake": encrypted_intake,
        "encrypted_lab_results": encrypted_labs,
        "wrapped_key": wrapped_key,
        "metadata": {
            "encryption_algorithm": "PQC-Hybrid-Demo",
            "key_algorithm": "Kyber-Demo"
        }
    }

    Path("data").mkdir(exist_ok=True)
    out = Path("data/patient_sample.json")
    out.write_text(json.dumps(payload, indent=2))

    print("Sample payload saved:", out)


if __name__ == "__main__":
    main()
