import base64
import json
import logging
import os
import hashlib

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

logger = logging.getLogger(__name__)

DUMMY_PUBLIC_KEY = b"kyber-public-key-demo"
DUMMY_PRIVATE_KEY = b"kyber-private-key-demo"


def kyber_encaps(public_key: bytes) -> tuple[bytes, bytes]:
    ct = os.urandom(64)
    shared_secret = hashlib.sha256(ct).digest()
    return ct, shared_secret


def kyber_decaps(ct: bytes, private_key: bytes) -> bytes:
    shared_secret = hashlib.sha256(ct).digest()
    return shared_secret


class MockCryptoService:
    AES_KEY_BYTES = 32
    NONCE_BYTES = 12

    @staticmethod
    def encrypt(plaintext_data: dict) -> tuple[str, str]:
        try:
            json_str = json.dumps(plaintext_data)
            plaintext = json_str.encode("utf-8")

            ct, shared_secret = kyber_encaps(DUMMY_PUBLIC_KEY)
            aes_key = shared_secret[: MockCryptoService.AES_KEY_BYTES]
            nonce = os.urandom(MockCryptoService.NONCE_BYTES)

            aes = AESGCM(aes_key)
            ciphertext = aes.encrypt(nonce, plaintext, associated_data=None)

            blob = nonce + ciphertext
            encrypted_blob = base64.b64encode(blob).decode("utf-8")
            wrapped_key = base64.b64encode(ct).decode("utf-8")

            logger.info("Data encrypted with Kyber-hybrid (simulated) + AES-GCM.")
            return encrypted_blob, wrapped_key
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    @staticmethod
    def decrypt(encrypted_blob: str, wrapped_key: str) -> dict:
        try:
            ct = base64.b64decode(wrapped_key.encode("utf-8"))
            shared_secret = kyber_decaps(ct, DUMMY_PRIVATE_KEY)
            aes_key = shared_secret[: MockCryptoService.AES_KEY_BYTES]

            blob = base64.b64decode(encrypted_blob.encode("utf-8"))
            nonce = blob[: MockCryptoService.NONCE_BYTES]
            ciphertext = blob[MockCryptoService.NONCE_BYTES :]

            aes = AESGCM(aes_key)
            plaintext = aes.decrypt(nonce, ciphertext, associated_data=None)

            json_str = plaintext.decode("utf-8")
            plaintext_data = json.loads(json_str)

            logger.info("Data decrypted with Kyber-hybrid (simulated) + AES-GCM.")
            return plaintext_data
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise


crypto_service = MockCryptoService()
