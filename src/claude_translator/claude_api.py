"""
Claude API integration module for the Tibetan Buddhist Commentary Translation Library.
"""

import time
from typing import List, Dict, Optional
import anthropic

def translate_with_claude(
    root_text: str,
    commentary_text: str,
    target_language: str,
    few_shot_examples: List[Dict],
    api_key: str,
    max_retries: int = 3,
    retry_delay: float = 2.0
) -> str:
    """
    Translate a single Tibetan commentary using Claude's API.
    
    Args:
        root_text: The root text in Tibetan (not to be translated)
        commentary_text: The commentary text in Tibetan to translate
        target_language: Target language for translation
        few_shot_examples: Few-shot examples to guide translation
        api_key: Anthropic API key
        max_retries: Maximum number of retries on API failure
        retry_delay: Delay between retries in seconds
        
    Returns:
        Translated commentary text
    """
    client = anthropic.Anthropic(api_key=api_key)
    
    # Construct the messages with few-shot examples
    messages = []
    
    # System prompt will be passed as a separate parameter
    
    # Add few-shot examples as context
    for example in few_shot_examples:
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Root text: {example['human'].get('root', '')}\n\nCommentary: {example['human'].get('commentary', '')}\n\nTranslate only the commentary to {example['human'].get('target_language', target_language)}. Return just the translation without any other text. Do not include the original root text or commentary."
                }
            ]
        })
        
        messages.append({
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": example['assistant'].get('output', '')
                }
            ]
        })
    
    # Add the actual translation request
    # For empty commentary, we need a special case
    if not commentary_text.strip():
        # If commentary is empty, return empty right away without calling API
        return ""
        
    # Otherwise prepare the message
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"Root text: {root_text}\n\nCommentary: {commentary_text}\n\nTranslate only the commentary to {target_language}. Return just the translation without any other text. Do not include the original root text or commentary."
            }
        ]
    })
    
    # Retry logic for API calls
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4096,
                temperature=0.2,  # Lower temperature for more precise translation
                system="You are an expert translator of Tibetan Buddhist commentaries. Your task is to provide accurate, clear, and contextually appropriate translations while preserving the meaning and nuance of the original text. Follow these guidelines:\n\n1. Translate ONLY the commentary text, not the root text\n2. Maintain technical Buddhist terminology appropriately\n3. Preserve the logical flow and structure of the original\n4. When uncertain about a term, prefer the most contextually accurate translation\n5. Return only the translated text without explanations or meta-commentary",
                messages=messages
            )
            
            # Get the response text
            translated_text = response.content[0].text
            
            # If we got an empty response, retry
            if not translated_text.strip() and commentary_text.strip():
                if attempt < max_retries - 1:
                    sleep_time = retry_delay * (2 ** attempt)
                    print(f"Empty translation received, retrying in {sleep_time} seconds (attempt {attempt+1}/{max_retries})")
                    time.sleep(sleep_time)
                    continue
                else:
                    print(f"Empty translation received after {max_retries} attempts, returning empty result")
            
            return translated_text
        
        except (anthropic.APIError, anthropic.RateLimitError) as e:
            if attempt < max_retries - 1:
                # Exponential backoff
                sleep_time = retry_delay * (2 ** attempt)
                print(f"API error: {str(e)}, retrying in {sleep_time} seconds (attempt {attempt+1}/{max_retries})")
                time.sleep(sleep_time)
                continue
            else:
                raise
        except Exception as e:
            print(f"Unexpected error during API call: {str(e)}")
            raise