import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.services.crypto_mock import crypto_service


def main():
    sample = {
        "intake_data": {
            "age": 45,
            "gender": "Male",
            "symptoms": "Increased thirst, frequent urination, fatigue for 3 months",
            "medical_history": ["Hypertension (5 years)", "Family history of Type 2 Diabetes"],
            "current_medications": ["Lisinopril 10mg daily"],
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
            "notes": "Fasting sample. Poor glycemic control, possible early nephropathy.",
        },
    }

    encrypted_blob, wrapped_key = crypto_service.encrypt(sample)
    print("Encrypted blob length:", len(encrypted_blob))
    print("Wrapped key length:", len(wrapped_key))

    decrypted = crypto_service.decrypt(encrypted_blob, wrapped_key)
    assert decrypted == sample
    print("Decryption OK, payload matches.")


if __name__ == "__main__":
    main()

