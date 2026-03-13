import os
from typing import Dict, Optional
from dotenv import load_dotenv

class Config:
    """Configuration manager for data harvester"""
    
    def __init__(self):
        # Load environment variables from .env file if it exists
        load_dotenv()
    
    @property
    def firecrawl_api_key(self) -> str:
        """Get Firecrawl API key from environment"""
        return os.getenv('FIRECRAWL_API_KEY', '')
    
    @property
    def google_places_api_key(self) -> str:
        """Get Google Places API key from environment"""
        return os.getenv('GOOGLE_PLACES_API_KEY', '')
    
    @property
    def google_search_api_key(self) -> str:
        """Get Google Search API key from environment"""
        return os.getenv('GOOGLE_SEARCH_API_KEY', '')
    
    @property
    def google_search_engine_id(self) -> str:
        """Get Google Search Engine ID from environment"""
        return os.getenv('GOOGLE_SEARCH_ENGINE_ID', '')
    
    @property
    def linkedin_api_key(self) -> str:
        """Get LinkedIn API key from environment"""
        return os.getenv('LINKEDIN_API_KEY', '')
    
    @property
    def linkedin_secret_key(self) -> str:
        """Get LinkedIn secret key from environment"""
        return os.getenv('LINKEDIN_SECRET_KEY', '')
    
    @property
    def smtp_host(self) -> str:
        """Get SMTP host from environment"""
        return os.getenv('SMTP_HOST', '')
    
    @property
    def smtp_port(self) -> int:
        """Get SMTP port from environment"""
        return int(os.getenv('SMTP_PORT', '587'))
    
    @property
    def smtp_username(self) -> str:
        """Get SMTP username from environment"""
        return os.getenv('SMTP_USERNAME', '')
    
    @property
    def smtp_password(self) -> str:
        """Get SMTP password from environment"""
        return os.getenv('SMTP_PASSWORD', '')
    
    @property
    def database_url(self) -> str:
        """Get database URL from environment"""
        return os.getenv('DATABASE_URL', '')
    
    @property
    def debug(self) -> bool:
        """Get debug setting from environment"""
        return os.getenv('DEBUG', 'False').lower() == 'true'
    
    @property
    def log_level(self) -> str:
        """Get log level from environment"""
        return os.getenv('LOG_LEVEL', 'INFO')
    
    @property
    def max_retries(self) -> int:
        """Get max retries from environment"""
        return int(os.getenv('MAX_RETRIES', '3'))
    
    @property
    def rate_limit_delay(self) -> int:
        """Get rate limit delay from environment"""
        return int(os.getenv('RATE_LIMIT_DELAY', '2'))
    
    def validate_required_keys(self) -> Dict[str, bool]:
        """Validate that required API keys are present"""
        required_keys = {
            'firecrawl': bool(self.firecrawl_api_key),
            'google_places': bool(self.google_places_api_key),
            'google_search': bool(self.google_search_api_key and self.google_search_engine_id),
        }
        return required_keys
    
    def get_missing_keys(self) -> list:
        """Get list of missing required API keys"""
        validation = self.validate_required_keys()
        missing = [key for key, present in validation.items() if not present]
        return missing

# Global config instance
config = Config()
