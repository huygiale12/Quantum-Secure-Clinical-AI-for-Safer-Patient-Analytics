import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.crypto_mock import (
    create_session_keypair, get_public_key, get_secret_key,
    hybrid_encrypt, hybrid_decrypt
)

def test_crypto():
    user_id = "doctor_001"
    session_id = create_session_keypair(user_id)
    public_key = get_public_key(session_id)
    secret_key = get_secret_key(session_id)

    message = b"Medical record encrypted for post-quantum security"
    encrypted = hybrid_encrypt(message, public_key)
    decrypted = hybrid_decrypt(encrypted, secret_key)

    assert decrypted == message
    print("✅ Encryption and decryption successful")

if __name__ == "__main__":
    test_crypto()
