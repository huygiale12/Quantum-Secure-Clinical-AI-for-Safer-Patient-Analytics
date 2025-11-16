import base64
import hashlib
import hmac
import time
from uuid import uuid4

from pqcrypto.kem.kyber512 import generate_keypair, encapsulate, decapsulate
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

KEY_STORE = {}

def create_session_keypair(user_id: str) -> str:
    session_id = f"{user_id}_{uuid4()}"
    pk, sk = generate_keypair()
    KEY_STORE[session_id] = {
        "pk": pk,
        "sk": sk,
        "timestamp": time.time()
    }
    return session_id

def get_public_key(session_id: str):
    return KEY_STORE[session_id]["pk"]

def get_secret_key(session_id: str):
    return KEY_STORE[session_id]["sk"]

def rotate_session_key(user_id: str) -> str:
    return create_session_keypair(user_id)

def aes_encrypt(plaintext: bytes, key: bytes):
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return {
        "nonce": nonce,
        "ciphertext": ciphertext,
        "tag": tag
    }

def aes_decrypt(blob: dict, key: bytes):
    cipher = AES.new(key, AES.MODE_GCM, nonce=blob["nonce"])
    plaintext = cipher.decrypt_and_verify(blob["ciphertext"], blob["tag"])
    return plaintext

def generate_hmac(data: bytes, key: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha256).digest()

def verify_hmac(data: bytes, key: bytes, expected_mac: bytes) -> bool:
    return hmac.compare_digest(generate_hmac(data, key), expected_mac)

def hybrid_encrypt(plaintext: bytes, kyber_public_key: bytes):
    wrapped_key, session_key = encapsulate(kyber_public_key)
    encrypted = aes_encrypt(plaintext, session_key)
    mac = generate_hmac(encrypted["ciphertext"], session_key)
    return {
        "wrapped_key": wrapped_key,
        "ciphertext": encrypted,
        "hmac": mac
    }

def hybrid_decrypt(encrypted_package: dict, kyber_secret_key: bytes):
    session_key = decapsulate(encrypted_package["wrapped_key"], kyber_secret_key)
    valid = verify_hmac(
        encrypted_package["ciphertext"]["ciphertext"],
        session_key,
        encrypted_package["hmac"]
    )
    if not valid:
        raise Exception("HMAC verification failed")
    return aes_decrypt(encrypted_package["ciphertext"], session_key)

def encode_b64(data: bytes) -> str:
    return base64.b64encode(data).decode()

def decode_b64(data: str) -> bytes:
    return base64.b64decode(data)

def encode_cipher_json(cipher: dict) -> dict:
    return {
        "nonce": encode_b64(cipher["nonce"]),
        "ciphertext": encode_b64(cipher["ciphertext"]),
        "tag": encode_b64(cipher["tag"])
    }

def decode_cipher_json(blob: dict) -> dict:
    return {
        "nonce": decode_b64(blob["nonce"]),
        "ciphertext": decode_b64(blob["ciphertext"]),
        "tag": decode_b64(blob["tag"])
    }
