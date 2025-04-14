# CRIS RAG Chatbot

A web-based AI chatbot application that uses Retrieval-Augmented Generation (RAG) to provide context-aware responses based on CRIS documentation. The chatbot processes Microsoft Word documents from a specified folder and uses them as its knowledge base to provide accurate, contextual responses to user queries.

## Features

- Web-based chat interface
- OpenAI GPT-4 integration for natural language processing
- RAG implementation using LangChain and FAISS for efficient document retrieval
- Support for Microsoft Word (.docx) documents as knowledge base
- Real-time chat with markdown formatting support
- Vector store caching for improved performance

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cris-rag-chatbot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your environment configuration:
   ```bash
   cp instance/.env.example instance/.env
   ```
   Edit the `.env` file with your OpenAI API key and other settings.

6. Place your DOCX documents in the `docs` folder.

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Start chatting with the bot! The bot will use the documents in the `docs` folder as its knowledge base to provide contextual responses.

## Project Structure

```
cris-rag-chatbot/
├── docs/                  # Knowledge base documents (.docx files)
├── instance/              # Instance-specific configuration (not in version control)
│   └── .env.example       # Template for environment variables
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── src/                   # Application package
│   ├── __init__.py        # Application factory
│   ├── config.py          # Configuration classes
│   ├── chat/              # Chat functionality module
│   │   ├── __init__.py
│   │   └── bot.py         # ChatBot implementation
│   ├── rag/               # RAG implementation module
│   │   ├── __init__.py
│   │   ├── cache_manager.py
│   │   ├── document_loader.py
│   │   └── vector_store.py
│   ├── routes/            # Application routes/blueprints
│   │   ├── __init__.py
│   │   ├── api.py         # API endpoints
│   │   └── main.py        # Web page routes
│   ├── static/            # Web assets
│   │   ├── css/
│   │   └── js/
│   └── templates/         # HTML templates
└── vector_store/          # Persisted vector embeddings
```

## Configuration

The application uses a configuration system that supports different environments:

- Development (default): Debug mode enabled, suitable for development
- Testing: For running automated tests
- Production: Optimized for production use

Configure the environment by setting `FLASK_ENV` in your `.env` file.

## Technical Details

- **Framework**: Flask with application factory pattern and blueprints
- **AI Model**: OpenAI GPT-4
- **Vector Store**: FAISS
- **Document Processing**: python-docx
- **Embedding Model**: OpenAI Embeddings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.