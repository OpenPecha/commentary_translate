"""
Caching module for the Tibetan Buddhist Commentary Translation Library.
"""

import hashlib
import json
import os
import time
from typing import Optional, Dict

class TranslationCache:
    """
    A simple file-based cache for translation results.
    """
    
    def __init__(self, cache_dir="./translation_cache", ttl=None):
        """
        Initialize the translation cache.
        
        Args:
            cache_dir: Directory to store cache files
            ttl: Time-to-live in seconds (None means no expiration)
        """
        self.cache_dir = cache_dir
        self.ttl = ttl
        self.memory_cache = {}  # In-memory cache for fast lookups
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
    
    def _generate_key(self, root_text: str, commentary_text: str, target_language: str) -> str:
        """Generate a unique cache key based on inputs."""
        key_string = f"{root_text}|{commentary_text}|{target_language}"
        return hashlib.md5(key_string.encode('utf-8')).hexdigest()
    
    def _get_cache_path(self, key: str) -> str:
        """Get the path to a cache file for a given key."""
        return os.path.join(self.cache_dir, f"{key}.json")
    
    def get(self, root_text: str, commentary_text: str, target_language: str) -> Optional[str]:
        """
        Retrieve a cached translation if available.
        
        Args:
            root_text: The root text in Tibetan
            commentary_text: The commentary text in Tibetan
            target_language: Target language for translation
            
        Returns:
            Cached translation or None if not found
        """
        key = self._generate_key(root_text, commentary_text, target_language)
        
        # Check in-memory cache first
        if key in self.memory_cache:
            return self.memory_cache[key]
        
        # Check file cache
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                # Check if cache is expired
                if self.ttl is not None:
                    cache_time = cache_data.get('timestamp', 0)
                    if time.time() - cache_time > self.ttl:
                        return None  # Cache expired
                
                # Store in memory cache and return
                translation = cache_data.get('translation', '')
                self.memory_cache[key] = translation
                return translation
            except:
                # Ignore corrupted cache files
                return None
        
        return None  # Cache miss
    
    def set(self, root_text: str, commentary_text: str, target_language: str, translation: str) -> None:
        """
        Store a translation in the cache.
        
        Args:
            root_text: The root text in Tibetan
            commentary_text: The commentary text in Tibetan
            target_language: Target language for translation
            translation: Translated text to cache
        """
        key = self._generate_key(root_text, commentary_text, target_language)
        
        # Store in memory cache
        self.memory_cache[key] = translation
        
        # Store in file cache
        cache_data = {
            'translation': translation,
            'timestamp': time.time(),
            'metadata': {
                'target_language': target_language
            }
        }
        
        with open(self._get_cache_path(key), 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False)
    
    def clear(self) -> None:
        """Clear the entire cache."""
        # Clear memory cache
        self.memory_cache = {}
        
        # Clear file cache
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.json'):
                try:
                    os.remove(os.path.join(self.cache_dir, filename))
                except:
                    pass
    
    def stats(self) -> Dict:
        """Get cache statistics."""
        file_count = len([f for f in os.listdir(self.cache_dir) if f.endswith('.json')])
        return {
            'files': file_count,
            'memory_entries': len(self.memory_cache)
        }