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
    
    # Add few-shot examples as context
    for example in few_shot_examples:
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Root text: {example['human'].get('root', '')}\n\nCommentary: {example['human'].get('commentary', '')}\n\nPlease translate the commentary to {example['human'].get('target_language', target_language)}. Leave the root text untranslated."
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
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"Root text: {root_text}\n\nCommentary: {commentary_text}\n\nPlease translate the commentary to {target_language}. Leave the root text untranslated."
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
                messages=messages
            )
            
            # Extract the response text
            translated_text = response.content[0].text
            return translated_text
        
        except (anthropic.APIError, anthropic.RateLimitError) as e:
            if attempt < max_retries - 1:
                # Exponential backoff
                sleep_time = retry_delay * (2 ** attempt)
                time.sleep(sleep_time)
                continue
            else:
                raise
        except Exception as e:
            raise