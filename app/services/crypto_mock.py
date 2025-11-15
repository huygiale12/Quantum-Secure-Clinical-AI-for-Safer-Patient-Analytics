import base64
import json
import logging
import os
import hashlib

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

logger = logging.getLogger(__name__)


# ==============================
#  Kyber-like KEM (SIMULATION)
# ==============================
#
# Ý tưởng:
# - Thay vì dùng lib Kyber thật, ta mô phỏng KEM:
#   ct            = os.urandom(64)
#   shared_secret = SHA256(ct)
#
# - Encrypt:
#     ct, shared_secret = kyber_encaps(PUBLIC_KEY)
#     aes_key = shared_secret[:32]
# - Decrypt:
#     shared_secret = kyber_decaps(ct, PRIVATE_KEY)
#     aes_key = shared_secret[:32]
#
# Sau này muốn dùng Kyber thật, chỉ việc thay
# thân 2 hàm kyber_encaps / kyber_decaps.


DUMMY_PUBLIC_KEY = b"kyber-public-key-demo"
DUMMY_PRIVATE_KEY = b"kyber-private-key-demo"


def kyber_encaps(public_key: bytes) -> tuple[bytes, bytes]:
    """
    Mô phỏng Kyber Encaps:
    - Tạo ct ngẫu nhiên
    - shared_secret = SHA256(ct)
    """
    ct = os.urandom(64)  # giả lập Kyber ciphertext
    shared_secret = hashlib.sha256(ct).digest()  # 32 bytes
    return ct, shared_secret


def kyber_decaps(ct: bytes, private_key: bytes) -> bytes:
    """
    Mô phỏng Kyber Decaps:
    - shared_secret = SHA256(ct)
    (giống với kyber_encaps → không cần state)
    """
    shared_secret = hashlib.sha256(ct).digest()
    return shared_secret


class MockCryptoService:
    """
    PQC Hybrid Crypto DEMO:

    - Layer KEM: Kyber (mô phỏng bằng SHA256(ct))
    - Layer mã hoá dữ liệu: AES-256-GCM
    - Lưu vào DB:
        encrypted_blob = base64( nonce || ciphertext )
        wrapped_key    = base64( ct )   # ct là Kyber ciphertext
    """

    AES_KEY_BYTES = 32   # 256-bit AES
    NONCE_BYTES = 12     # 96-bit nonce cho GCM

    @staticmethod
    def encrypt(plaintext_data: dict) -> tuple[str, str]:
        """
        Encrypt một dict Python bằng hybrid Kyber + AES-GCM.

        Returns:
            encrypted_blob: base64(nonce || ciphertext)
            wrapped_key:    base64(ct)  (Kyber ciphertext)
        """
        try:
            # 1) JSON hoá dữ liệu
            json_str = json.dumps(plaintext_data)
            plaintext = json_str.encode("utf-8")

            # 2) Kyber Encaps → ct, shared_secret
            ct, shared_secret = kyber_encaps(DUMMY_PUBLIC_KEY)

            # 3) Dùng shared_secret làm khoá AES-256
            aes_key = shared_secret[:MockCryptoService.AES_KEY_BYTES]
            nonce = os.urandom(MockCryptoService.NONCE_BYTES)

            aes = AESGCM(aes_key)
            ciphertext = aes.encrypt(nonce, plaintext, associated_data=None)

            # 4) Gộp nonce + ciphertext rồi base64
            blob = nonce + ciphertext
            encrypted_blob = base64.b64encode(blob).decode("utf-8")

            # 5) Gói ct thành wrapped_key (base64)
            wrapped_key = base64.b64encode(ct).decode("utf-8")

            logger.info("Data encrypted with Kyber-hybrid (simulated) + AES-GCM.")
            return encrypted_blob, wrapped_key

        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    @staticmethod
    def decrypt(encrypted_blob: str, wrapped_key: str) -> dict:
        """
        Giải mã data đã encrypt bằng encrypt().

        Args:
            encrypted_blob: base64(nonce || ciphertext)
            wrapped_key:    base64(ct)  (Kyber ciphertext)

        Returns:
            plaintext_data: dict
        """
        try:
            # 1) Decode ct từ wrapped_key
            ct = base64.b64decode(wrapped_key.encode("utf-8"))

            # 2) Kyber Decaps → shared_secret
            shared_secret = kyber_decaps(ct, DUMMY_PRIVATE_KEY)

            # 3) Dùng shared_secret làm khoá AES
            aes_key = shared_secret[:MockCryptoService.AES_KEY_BYTES]

            # 4) Decode blob → tách nonce + ciphertext
            blob = base64.b64decode(encrypted_blob.encode("utf-8"))
            nonce = blob[:MockCryptoService.NONCE_BYTES]
            ciphertext = blob[MockCryptoService.NONCE_BYTES:]

            aes = AESGCM(aes_key)
            plaintext = aes.decrypt(nonce, ciphertext, associated_data=None)

            json_str = plaintext.decode("utf-8")
            plaintext_data = json.loads(json_str)

            logger.info("Data decrypted with Kyber-hybrid (simulated) + AES-GCM.")
            return plaintext_data

        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise


# Instance global – routers dùng cái này
crypto_service = MockCryptoService()
