from flask import Blueprint, render_template, current_app

# Create a blueprint for main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Render the home page with the chat interface."""
    return render_template('chat.html')