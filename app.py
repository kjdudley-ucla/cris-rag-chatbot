"""
Simple entry point for running the Flask application in development mode.
This file is designed to be easily launched by VS Code's debugger.
"""
import os
from src import create_app

if __name__ == "__main__":
    # Create application with development config
    app = create_app(config_name='development')
    
    # Run app in debug mode, accessible from network
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )