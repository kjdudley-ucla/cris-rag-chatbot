from openai import OpenAI
from typing import Optional, List, Dict
from ..rag.vector_store import VectorStore
from ..rag.document_loader import load_documents_from_folder
import markdown
import os

class ChatBot:
    def __init__(self, api_key: str, system_prompt: str = "You are a helpful assistant with access to CRIS documentation.", force_reprocess: bool = True):
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []
        self.vector_store = VectorStore(api_key)
        self.system_prompt = system_prompt
        
        # Load and index documents
        self.docs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs')
        documents = load_documents_from_folder(self.docs_path)
        if documents:
            self.vector_store.add_documents(documents, self.docs_path, force_reprocess=force_reprocess)

    def get_response(self, user_input: str) -> Optional[str]:
        try:
            # Query relevant documents
            relevant_docs = self.vector_store.query(user_input, top_k=5)
            
            # Debug logging for retrieved documents
            print("\n=== Debug: Retrieved Documents ===")
            print(f"Query: {user_input}")
            print("\nMatched Documents:")
            for i, doc in enumerate(relevant_docs, 1):
                print(f"\n{i}. Source: {doc['source']}")
                print(f"Score: {doc.get('score', 'N/A')}")
                print(f"Content Preview: {doc['content'][:200]}...")
            print("\n==============================\n")
            
            # Construct system message with context and markdown formatting instructions
            system_message = {
                "role": "system",
                "content": self.system_prompt + "\nFormat your responses using Markdown for better readability. Use:\n" +
                          "- # for main headings\n" +
                          "- ## for subheadings\n" +
                          "- * or - for bullet points\n" +
                          "- 1. for numbered lists\n" +
                          "- **text** for bold/important points\n" +
                          "- *text* for emphasis/citations\n" +
                          "- `text` for technical terms or code\n" +
                          "- --- for horizontal rules"
            }
            
            if relevant_docs:
                context = "\n\n".join([f"From {doc['source']}:\n{doc['content']}" for doc in relevant_docs])
                system_message["content"] += "\n\nUse the following relevant information to answer questions. Format source citations in italics:\n\n" + context
            else:
                system_message["content"] += "\n\nNo specific documentation found for this query. Provide a general response."
            
            # Prepare messages for chat completion
            messages = [
                system_message,
                *self.conversation_history[-4:],  # Keep last 4 messages for context
                {"role": "user", "content": user_input}
            ]
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4.1-nano",  # Use standard GPT-4 model
                messages=messages,
                temperature=0.3,  # Reduced for more focused answers
                max_tokens=1000,  # Increased for more detailed responses
                presence_penalty=0.1,  # Slight penalty to prevent repetition
                frequency_penalty=0.1  # Slight penalty to prevent repetitive language
            )
            
            # Extract and convert markdown response to HTML
            assistant_message = response.choices[0].message.content
            html_response = markdown.markdown(assistant_message, extensions=['tables'])
            
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return html_response
            
        except Exception as e:
            print(f"Error getting response: {str(e)}")
            return "<p>I apologize, but I encountered an error processing your request.</p>"

    def process_input(self, user_input: str) -> str:
        return user_input.strip()