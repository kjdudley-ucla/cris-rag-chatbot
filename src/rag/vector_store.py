from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from .cache_manager import CacheManager
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, api_key: str):
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Increased for better context
            chunk_overlap=200,  # Increased overlap for better coherence
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]  # Added period separator for better sentence handling
        )
        self.vector_store = None
        self.persist_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'vector_store')
        os.makedirs(self.persist_directory, exist_ok=True)
        self.index_file = os.path.join(self.persist_directory, 'faiss_index')
        self.cache_manager = CacheManager(self.persist_directory)

    def add_documents(self, documents: List[Dict[str, str]], docs_path: str, force_reprocess: bool = False) -> None:
        # Skip cache check if force_reprocess is True
        if not force_reprocess and not self.cache_manager.have_documents_changed(docs_path):
            logger.debug("No document changes detected, using cached embeddings")
            try:
                if os.path.exists(self.index_file):
                    self.vector_store = FAISS.load_local(
                        self.index_file, 
                        self.embeddings,
                        allow_dangerous_deserialization=True
                    )
                    return
            except Exception as e:
                logger.error(f"Error loading cached index: {str(e)}")

        # Process documents into chunks if force_reprocess is True or there are changes/cache loading failed
        logger.debug("Processing documents for new embeddings" + (" (forced)" if force_reprocess else ""))
        texts = []
        metadatas = []
        
        logger.debug(f"\n=== Document Processing Debug ===")
        logger.debug(f"Number of documents to process: {len(documents)}")
        
        for doc in documents:
            logger.debug(f"\nProcessing document: {doc['filename']}")
            chunks = self.text_splitter.split_text(doc['content'])
            logger.debug(f"Generated {len(chunks)} chunks")
            logger.debug(f"First chunk preview: {chunks[0][:200]}..." if chunks else "No chunks generated")
            logger.debug(f"Average chunk length: {sum(len(c) for c in chunks)/len(chunks) if chunks else 0:.2f} characters")
            
            texts.extend(chunks)
            metadatas.extend([{'source': doc['filename']} for _ in chunks])
        
        logger.debug(f"\nTotal chunks across all documents: {len(texts)}")
        logger.debug("=== End Document Processing Debug ===\n")
        
        # Create or update vector store
        if texts:
            self.vector_store = FAISS.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas
            )
            # Save the index
            self.vector_store.save_local(self.index_file)
            logger.debug("New embeddings created and saved")

    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        # Try to load existing index if no vector store exists
        if not self.vector_store and os.path.exists(self.index_file):
            try:
                self.vector_store = FAISS.load_local(
                    self.index_file,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                logger.error(f"Error loading index: {str(e)}")
                return []

        if not self.vector_store:
            return []
        
        try:
            # Search for relevant documents
            results = self.vector_store.similarity_search_with_score(query_text, k=top_k)
            
            # Filter and format results with stricter threshold and normalized scores
            filtered_results = []
            for doc, score in results:
                # Convert distance to similarity score (0-1 range)
                similarity_score = 1.0 / (1.0 + score)
                
                # Only include documents with high similarity (threshold of 0.7)
                if similarity_score > 0.7:
                    filtered_results.append({
                        'content': doc.page_content,
                        'source': doc.metadata.get('source', 'unknown'),
                        'score': similarity_score
                    })
            
            return filtered_results

        except Exception as e:
            logger.error(f"Error during vector search: {str(e)}")
            return []