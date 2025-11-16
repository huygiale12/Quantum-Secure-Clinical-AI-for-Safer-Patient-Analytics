from supabase import create_client, Client
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    _instance: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get Supabase client instance (singleton pattern)"""
        if cls._instance is None:
            try:
                cls._instance = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_KEY
                )
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                raise
        return cls._instance

# Convenience function
def get_db() -> Client:
    """Get database client"""
    return Database.get_client()
