"""
Debug Test Script for CRIS RAG Chatbot

This script helps diagnose issues with the Flask application setup.
"""
import os
import sys
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Print Python and environment information
logger.info(f"Python version: {sys.version}")
logger.info(f"Python executable: {sys.executable}")
logger.info(f"Working directory: {os.getcwd()}")

# Try to load environment variables
print("\n=== Environment Variables Test ===")
try:
    # Try loading from instance/.env
    load_dotenv(os.path.join('instance', '.env'))
    logger.info("Loaded environment from instance/.env")
    
    # Print important environment variables (without revealing API key)
    flask_env = os.getenv('FLASK_ENV')
    api_key_exists = "Yes" if os.getenv('OPENAI_API_KEY') else "No"
    system_prompt_exists = "Yes" if os.getenv('SYSTEM_PROMPT') else "No"
    
    logger.info(f"FLASK_ENV: {flask_env}")
    logger.info(f"OPENAI_API_KEY exists: {api_key_exists}")
    logger.info(f"SYSTEM_PROMPT exists: {system_prompt_exists}")
except Exception as e:
    logger.error(f"Error loading environment: {str(e)}")

# Try to import Flask and create a simple app
print("\n=== Flask Import Test ===")
try:
    from flask import Flask
    logger.info("Successfully imported Flask")
    
    app = Flask(__name__)
    logger.info("Successfully created Flask app instance")
    
except ImportError as e:
    logger.error(f"Error importing Flask: {str(e)}")
except Exception as e:
    logger.error(f"Error creating Flask app: {str(e)}")

# Try to import and initialize the app factory
print("\n=== App Factory Test ===")
try:
    sys.path.append(os.getcwd())  # Add current directory to path
    from src import create_app
    logger.info("Successfully imported create_app factory")
    
    try:
        app = create_app('development')
        logger.info("Successfully created app with factory")
    except Exception as e:
        logger.error(f"Error creating app with factory: {str(e)}")
        
except ImportError as e:
    logger.error(f"Error importing create_app factory: {str(e)}")

print("\nDebug test complete. Check the output for any errors.")