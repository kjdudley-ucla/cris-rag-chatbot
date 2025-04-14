import os
import sys
import logging
from dotenv import load_dotenv

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Load environment variables
load_dotenv()

# Import the application factory
from src import create_app

if __name__ == '__main__':
    # Get configuration from environment
    config_name = os.getenv('FLASK_ENV', 'development')
    
    # Create the application
    app = create_app(config_name)
    
    # Log startup information
    app.logger.info(f"Starting application in {config_name} mode...")
    
    # Run the Flask application with settings from config
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000))
    )