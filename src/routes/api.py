from flask import Blueprint, request, jsonify, current_app

# Create a blueprint for API routes
api_bp = Blueprint('api', __name__)

@api_bp.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests and return responses."""
    user_input = request.json.get('message')
    current_app.logger.debug(f"Received user input: {user_input}")
    
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get response from the chatbot
    response = current_app.chatbot.get_response(user_input)
    current_app.logger.debug(f"Generated response: {response}")
    
    return jsonify({'response': response})