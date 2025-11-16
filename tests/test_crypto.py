from app.services.crypto_mock import hybrid_encrypt_and_decrypt

def test_crypto():
    message = b"Hello post-quantum world"
    result = hybrid_encrypt_and_decrypt(message)
    assert result == message
    print("Test passed.")

test_crypto()
