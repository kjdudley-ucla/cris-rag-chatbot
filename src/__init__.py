import os
import logging
from flask import Flask
from .config import get_config
from .chat.bot import ChatBot

def create_app(config_name=None):
    """
    Application factory function that creates and configures the Flask application.
    
    Args:
        config_name: The name of the configuration to use (development, testing, production)
        
    Returns:
        The configured Flask application
    """
    # Create and configure the app
    app = Flask(__name__)
    
    # Load configuration
    config_obj = get_config(config_name)
    app.config.from_object(config_obj)
    
    # Configure logging
    configure_logging(app)
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    return app

def configure_logging(app):
    """Configure the application's logging system."""
    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    
    # Setup handlers
    log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'chatbot.log')
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()
    
    # Format logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Configure app logger
    app.logger.setLevel(log_level)

def init_extensions(app):
    """Initialize Flask extensions."""
    # Initialize the chatbot instance
    api_key = app.config.get('OPENAI_API_KEY')
    system_prompt = app.config.get('SYSTEM_PROMPT')
    force_reprocess = app.config.get('FORCE_REPROCESS')
    
    if not api_key:
        app.logger.error("OPENAI_API_KEY not found in configuration!")
    
    # Create a chatbot instance and attach it to the app
    app.chatbot = ChatBot(
        api_key=api_key, 
        system_prompt=system_prompt, 
        force_reprocess=force_reprocess
    )
    app.logger.info("ChatBot initialized successfully")

def register_blueprints(app):
    """Register Flask blueprints."""
    from .routes.main import main_bp
    from .routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

def run_app():
    """
    Console script entry point to run the application.
    This function is referenced in setup.py entry_points.
    """
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv(os.path.join('instance', '.env'))
    
    # Get configuration from environment
    config_name = os.getenv('FLASK_ENV', 'development')
    
    # Create the application
    app = create_app(config_name)
    
    # Run the Flask application with settings from config
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000))
    )