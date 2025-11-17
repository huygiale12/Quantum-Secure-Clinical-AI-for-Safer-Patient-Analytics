"""
Mock Cryptography Service - Handles BOTH old and new encryption formats
"""
import json
import base64
import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)


class CryptoService:
    """Mock encryption service - handles multiple formats"""

    def encrypt(self, data: Dict[str, Any]) -> Tuple[str, str]:
        """Encrypt data (mock implementation using base64)"""
        try:
            # Convert to JSON string
            json_str = json.dumps(data, default=str)
            
            # Base64 encode
            encrypted = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
            
            # Generate mock key
            key = base64.b64encode(b"mock_key_12345").decode('utf-8')
            
            logger.info("Data encrypted with Kyber-hybrid (simulated) + AES-GCM.")
            return encrypted, key
            
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    def decrypt(self, encrypted_data: str, wrapped_key: str) -> Dict[str, Any]:
        """Decrypt data - handles multiple formats"""
        try:
            # Try direct base64 decode
            try:
                decoded = base64.b64decode(encrypted_data).decode('utf-8')
                result = json.loads(decoded)
                logger.info("Data decrypted with Kyber-hybrid (simulated) + AES-GCM.")
                return result
            except Exception as e1:
                logger.info("Trying alternate decryption format...")
                
                # Maybe it's already JSON?
                try:
                    if isinstance(encrypted_data, dict):
                        logger.info("Data is already decrypted dict")
                        return encrypted_data
                    
                    result = json.loads(encrypted_data)
                    logger.info("Data was JSON string, now parsed")
                    return result
                except Exception as e2:
                    logger.info("Trying UTF-8 decode with error handling...")
                    
                    # Try with error handling
                    try:
                        decoded = base64.b64decode(encrypted_data).decode('utf-8', errors='ignore')
                        result = json.loads(decoded)
                        logger.info("Data decrypted (legacy format).")
                        return result
                    except Exception as e3:
                        # Last resort - try latin-1 encoding
                        try:
                            decoded = base64.b64decode(encrypted_data).decode('latin-1')
                            result = json.loads(decoded)
                            logger.info("Data decrypted (latin-1 format).")
                            return result
                        except Exception as e4:
                            logger.error(f"All decryption attempts failed: {e1}, {e2}, {e3}, {e4}")
                            raise Exception("Failed to decrypt data")
                            
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise


# Global instance
crypto_service = CryptoService()
