"""
Core translator module for the Tibetan Buddhist Commentary Translation Library.
"""

import os
import concurrent.futures
from typing import List, Dict, Optional, Union, Any
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from tqdm import tqdm

from .claude_api import translate_with_claude
from .utils import get_default_few_shot_examples, setup_logging

logger = setup_logging()

def translate_commentaries(
    commentary_root_pairs: List[Dict[str, str]],
    target_language: str,
    few_shot_examples: Optional[List[Dict]] = None,
    num_threads: int = 4,
    api_key: Optional[str] = None,
    use_cache: bool = True,
    cache_dir: str = "./translation_cache",
    cache_ttl: Optional[int] = None
) -> List[Dict[str, str]]:
    """
    Translate a list of Tibetan commentary-root pairs into the specified target language.
    
    Args:
        commentary_root_pairs: List of dictionaries with 'root' and 'commentary' keys
        target_language: Target language name (e.g., 'English', 'Chinese', 'French')
        few_shot_examples: Optional multi-turn conversation examples to guide translation style
                          (if None, default examples will be used)
        num_threads: Number of threads for parallel processing
        api_key: Optional Claude API key (if not provided, will read from .env)
        use_cache: Whether to cache translation results (default: True)
        cache_dir: Directory to store cached translations
        cache_ttl: Time-to-live for cache entries in seconds (None = no expiration)
        
    Returns:
        List of dictionaries with 'root' (unchanged), 'commentary' (original text), 
        and 'commentary_translation' (translated text) keys
    """
    # Load default examples if none provided
    if few_shot_examples is None:
        few_shot_examples = get_default_few_shot_examples(target_language)
    
    # Get API key from environment if not provided
    if api_key is None:
        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("API key not provided and not found in .env file")
    
    # Initialize cache if enabled
    cache = None
    if use_cache:
        try:
            from .cache import TranslationCache
            cache = TranslationCache(cache_dir=cache_dir, ttl=cache_ttl)
            logger.info(f"Translation cache enabled: {cache_dir}")
        except ImportError:
            logger.warning("Cache module not found. Continuing without caching.")
    
    # Prepare results list with same length as input
    results = [None] * len(commentary_root_pairs)
    
    # Filter tasks - skip empty commentaries
    translation_tasks = []
    for idx, pair in enumerate(commentary_root_pairs):
        if pair.get("commentary", "") == "":
            # Keep empty commentaries as-is
            results[idx] = {
                "root": pair.get("root", ""), 
                "commentary": "", 
                "commentary_translation": ""
            }
        else:
            # Add to translation tasks
            translation_tasks.append((idx, pair))
    
    # Process translations in parallel with thread pool and progress bar
    total_translations = len(translation_tasks)
    active_threads = 0
    completed = 0
    
    # Prepare progress bar with thread info
    pbar_desc = f"Translating to {target_language} [0/{num_threads} threads]"
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Create progress bar
        with tqdm(total=total_translations, desc=pbar_desc, unit="commentary") as pbar:
            # Submit initial batch of tasks
            futures_to_idx = {}
            
            # Helper function to update progress bar with thread info
            def update_progress_bar():
                nonlocal active_threads, completed
                pbar.set_description(
                    f"Translating to {target_language} [{active_threads}/{num_threads} threads] "
                    f"({completed}/{total_translations} done)"
                )
            
            # Submit initial batch of tasks up to num_threads
            for idx, pair in translation_tasks[:num_threads]:
                future = executor.submit(
                    _translate_single_commentary,
                    pair,
                    target_language,
                    few_shot_examples,
                    api_key,
                    cache
                )
                futures_to_idx[future] = idx
                active_threads += 1
            
            update_progress_bar()
            
            # Process completed tasks and submit new ones
            remaining_tasks = translation_tasks[num_threads:]
            
            while futures_to_idx:
                # Wait for a task to complete
                done, _ = concurrent.futures.wait(
                    futures_to_idx, 
                    return_when=concurrent.futures.FIRST_COMPLETED
                )
                
                for future in done:
                    idx = futures_to_idx.pop(future)
                    active_threads -= 1
                    completed += 1
                    
                    try:
                        translated_commentary = future.result()
                        # Check if we have a valid translation
                        if translated_commentary and translated_commentary.strip():
                            results[idx] = {
                                "root": commentary_root_pairs[idx].get("root", ""),
                                "commentary": commentary_root_pairs[idx].get("commentary", ""),
                                "commentary_translation": translated_commentary
                            }
                        else:
                            # Empty translation but no error - log a warning
                            logger.warning(f"Empty translation received for index {idx}")
                            original_pair = commentary_root_pairs[idx]
                            results[idx] = {
                                "root": original_pair.get("root", ""),
                                "commentary": original_pair.get("commentary", ""),
                                "commentary_translation": ""  # Empty on failure
                            }
                    except Exception as e:
                        logger.error(f"Translation failed at index {idx}: {str(e)}")
                        # Preserve original on failure
                        original_pair = commentary_root_pairs[idx]
                        results[idx] = {
                            "root": original_pair.get("root", ""),
                            "commentary": original_pair.get("commentary", ""),
                            "commentary_translation": ""  # Empty on failure
                        }
                    
                    # Submit a new task if there are more to process
                    if remaining_tasks:
                        new_idx, new_pair = remaining_tasks.pop(0)
                        new_future = executor.submit(
                            _translate_single_commentary,
                            new_pair,
                            target_language,
                            few_shot_examples,
                            api_key,
                            cache
                        )
                        futures_to_idx[new_future] = new_idx
                        active_threads += 1
                    
                    # Update progress bar
                    pbar.update(1)
                    update_progress_bar()
    
    return results

def _translate_single_commentary(
    pair: Dict[str, str],
    target_language: str,
    few_shot_examples: List[Dict],
    api_key: str,
    cache=None
) -> str:
    """
    Helper function to translate a single commentary.
    
    Args:
        pair: Dictionary containing 'root' and 'commentary' keys
        target_language: Target language for translation
        few_shot_examples: Few-shot learning examples to guide translation
        api_key: Anthropic API key
        cache: Optional translation cache
        
    Returns:
        Translated commentary text
    """
    root_text = pair.get("root", "")
    commentary_text = pair.get("commentary", "")
    
    # Check cache first if enabled
    if cache is not None:
        cached_translation = cache.get(root_text, commentary_text, target_language)
        if cached_translation is not None:
            logger.debug(f"Cache hit for commentary: {commentary_text[:30]}...")
            return cached_translation
    
    try:
        # Call the Claude API to translate the commentary
        translated_text = translate_with_claude(
            root_text=root_text,
            commentary_text=commentary_text,
            target_language=target_language,
            few_shot_examples=few_shot_examples,
            api_key=api_key
        )
        
        # Store in cache if enabled
        if cache is not None:
            cache.set(root_text, commentary_text, target_language, translated_text)
            
        return translated_text
    except Exception as e:
        logger.error(f"Error translating commentary: {str(e)}")
        raise