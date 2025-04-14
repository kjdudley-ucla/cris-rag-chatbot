import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT', 'You are a helpful assistant with access to CRIS documentation.')
    FORCE_REPROCESS = os.getenv('FORCE_REPROCESS', '').lower() == 'true'
    
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = False
    TESTING = True
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False

# Configuration dictionary to easily select environment
config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Return the appropriate configuration object based on the environment."""
    if not config_name:
        config_name = os.getenv('FLASK_ENV', 'default')
    return config_dict.get(config_name, config_dict['default'])