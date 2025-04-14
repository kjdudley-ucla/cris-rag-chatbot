import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join('instance', '.env'))

# Set environment to production by default for the WSGI server
os.environ.setdefault('FLASK_ENV', 'production')

# Import the application factory and create the app
from src import create_app
application = create_app()

if __name__ == "__main__":
    import argparse
    from waitress import serve
    
    parser = argparse.ArgumentParser(description='Run the CRIS RAG chatbot application')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind the server to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind the server to')
    parser.add_argument('--dev', action='store_true', help='Run in development mode using Flask\'s built-in server')
    
    args = parser.parse_args()
    
    if args.dev:
        # Development mode using Flask's built-in server
        application.run(host=args.host, port=args.port, debug=True)
    else:
        # Production mode using Waitress
        print(f"Starting Waitress server on {args.host}:{args.port}")
        serve(application, host=args.host, port=args.port)