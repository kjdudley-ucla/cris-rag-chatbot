#!/usr/bin/env python
"""
Standalone script to run the CRIS RAG chatbot application using Waitress WSGI server.
This provides a production-ready server for deployment.

Usage:
    python run.py [--host HOST] [--port PORT] [--threads THREADS]
"""

import argparse
import os
from waitress import serve
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join('instance', '.env'))

# Set environment to production
os.environ['FLASK_ENV'] = 'production'

def main():
    parser = argparse.ArgumentParser(description='Run the CRIS RAG chatbot application with Waitress WSGI server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind the server to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind the server to (default: 8000)')
    parser.add_argument('--threads', type=int, default=4, help='Number of threads for Waitress (default: 4)')
    
    args = parser.parse_args()
    
    # Import the application factory and create the app
    from src import create_app
    application = create_app()
    
    print(f"Starting Waitress WSGI server on {args.host}:{args.port} with {args.threads} threads")
    print(f"Press Ctrl+C to stop the server")
    
    # Run the application with Waitress
    serve(application, host=args.host, port=args.port, threads=args.threads)

if __name__ == "__main__":
    main()