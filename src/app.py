from flask import Flask, render_template, request, jsonify
from chat.bot import ChatBot
from dotenv import load_dotenv
import os
import logging

# Configure logging with more detail
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('chatbot.log')
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
logger.debug("Loading environment variables...")
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
system_prompt = os.getenv('SYSTEM_PROMPT', 'You are a helpful assistant with access to CRIS documentation.')
force_reprocess = os.getenv('FORCE_REPROCESS', '').lower() == 'true'

if not api_key:
    logger.error("OPENAI_API_KEY not found in environment variables!")
else:
    logger.debug("OPENAI_API_KEY found")
logger.debug(f"Using system prompt: {system_prompt}")
logger.debug(f"Force reprocess embeddings: {force_reprocess}")

app = Flask(__name__)
logger.info("Initializing ChatBot...")
chatbot = ChatBot(api_key=api_key, system_prompt=system_prompt, force_reprocess=force_reprocess)
logger.info("ChatBot initialized successfully")

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('message')
    logger.debug(f"Received user input: {user_input}")
    response = chatbot.get_response(user_input)
    logger.debug(f"Generated response: {response}")
    return jsonify({'response': response})

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(debug=True, port=5000)