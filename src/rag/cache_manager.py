import os
import json
import hashlib
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        self.cache_file = os.path.join(cache_dir, 'document_cache.json')
        self.document_hashes = self._load_cache()

    def _load_cache(self) -> Dict[str, str]:
        """Load document hashes from cache file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading cache: {str(e)}")
                return {}
        return {}

    def _save_cache(self) -> None:
        """Save document hashes to cache file"""
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.document_hashes, f)
        except Exception as e:
            logger.error(f"Error saving cache: {str(e)}")

    def _compute_file_hash(self, file_path: str) -> Optional[str]:
        """Compute SHA-256 hash of a file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Error computing hash for {file_path}: {str(e)}")
            return None

    def have_documents_changed(self, folder_path: str) -> bool:
        """Check if any documents in the folder have changed"""
        current_hashes = {}
        has_changes = False

        try:
            for filename in os.listdir(folder_path):
                if filename.endswith('.docx'):
                    file_path = os.path.join(folder_path, filename)
                    current_hash = self._compute_file_hash(file_path)
                    if current_hash:
                        current_hashes[filename] = current_hash
                        if (filename not in self.document_hashes or 
                            self.document_hashes[filename] != current_hash):
                            has_changes = True

            # Check for deleted files
            if set(self.document_hashes.keys()) - set(current_hashes.keys()):
                has_changes = True

            if has_changes:
                self.document_hashes = current_hashes
                self._save_cache()

            return has_changes
        except Exception as e:
            logger.error(f"Error checking document changes: {str(e)}")
            return True  # Assume changes on error to force refresh