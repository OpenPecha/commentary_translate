"""
Advanced usage example for the Claude Translator library.

This example demonstrates:
1. Using custom few-shot examples
2. Handling larger datasets
3. Using more threads for better performance
4. Custom API key handling
"""

import os
import time
from dotenv import load_dotenv
from claude_translator import translate_commentaries

# Load environment variables from .env file
load_dotenv()

def main():
    # Sample Tibetan commentary-root pairs (larger dataset)
    sample_data = [
        {
            "root": "དེ་ནས་བཅོམ་ལྡན་འདས་མཉན་ཡོད་ཀྱི་གྲོང་ཁྱེར་ཆེན་པོར་བསོད་སྙོམས་ཀྱི་ཕྱིར་གཤེགས་ནས་ཞལ་ཟས་གསོལ་ཏེ་ཟས་ཀྱི་བྱ་བ་མཛད་དེ།",
            "commentary": "བསོད་སྙོམས་བླངས་ཏེ་མཇུག་ཏུ་སླར་བྱོན་ནས་ཞལ་ཟས་གསོལ་བའི་བྱ་བ་མཛད་དོ། །"
        },
        {
            "root": "གང་ཞིག་རྐྱེན་ལས་སྐྱེ་བ་དེ་ནི་རང་བཞིན་གྱིས་མ་སྐྱེས་པ་ཡིན་ནོ། །",
            "commentary": ""  # Empty commentary - should remain empty
        },
        {
            "root": "",  # Empty root
            "commentary": "བཅོམ་ལྡན་འདས་བསོད་སྙོམས་ལ་འབྱོན་པ་ནི། རང་ཉིད་བསོད་སྙོམས་ཀྱི་ཟས་ཟ་དགོས་པའི་ཆེད་མིན་གྱི། གདུལ་བྱ་ལ་ཚོགས་གསོག་པ་དང་ཆོས་སྟོན་པ་སོགས་ཀྱི་ཆེད་དུའོ། །"
        },
        {
            "root": "ཟས་ཕྱི་མའི་བསོད་སྙོམས་སྤངས་ནས་ལྷུང་བཟེད་དང་ཆོས་གོས་བཞག་ནས། ཞབས་བསིལ་ཏེ་གདན་བཤམས་པ་ལ་སྐྱིལ་མོ་ཀྲུང་བཅས་ནས་སྐུ་དྲང་པོར་བསྲང་སྟེ། དྲན་པ་མངོན་དུ་བཞག་ནས་བཞུགས་སོ། །",
            "commentary": "ཟས་ཕྱི་མ་ཕྱི་དྲོའི་བསོད་སྙོམས་ཟ་བ་སྤངས་ནས། ལྷུང་བཟེད་སོགས་བཞག་ནས་ཞབས་བཀྲུས་ཤིང་བསིལ་ཏེ། གདན་བཤམས་པ་ཉིད་ལ་དཀྱིལ་མོ་ཀྲུང་བཅས་ནས་སྐུ་དྲང་པོར་སྲང་སྟེ། གཞུང་འདི་སྟོན་པར་འགྱུར་བ་མཁྱེན་པའི་དྲན་པ་མངོན་དུ་བཞག་ནས་བཞུགས་སོ། །"
        },
        {
            "root": "བཅོམ་ལྡན་འདས་ཀྱིས་དེ་སྐད་ཅེས་བཀའ་སྩལ་ནས།",
            "commentary": "འདི་ནི་མདོ་རྫོགས་པའི་མཇུག་གི་ཚིག་ཡིན་ལ། དེ་ཡང་བཅོམ་ལྡན་འདས་ཀྱིས་ཆོས་འདི་ཐམས་ཅད་གསུངས་ཟིན་པའི་རྗེས་སུ།"
        },
    ]

    # Custom few-shot examples for Chinese translation
    # In a real application, you might load these from a separate file
    custom_chinese_examples = [
        {
            "human": {
                "root": "དེ་ནས་བཅོམ་ལྡན་འདས་མཉན་ཡོད་ཀྱི་གྲོང་ཁྱེར་ཆེན་པོར་བསོད་སྙོམས་ཀྱི་ཕྱིར་གཤེགས་ནས་ཞལ་ཟས་གསོལ་ཏེ་ཟས་ཀྱི་བྱ་བ་མཛད་དེ།",
                "commentary": "བསོད་སྙོམས་བླངས་ཏེ་མཇུག་ཏུ་སླར་བྱོན་ནས་ཞལ་ཟས་གསོལ་བའི་བྱ་བ་མཛད་དོ། །",
                "target_language": "Chinese"
            },
            "assistant": {
                "output": "他接受了施舍的食物，然后返回并享用了餐食。"
            }
        },
        {
            "human": {
                "root": "ཟས་ཕྱི་མའི་བསོད་སྙོམས་སྤངས་ནས་ལྷུང་བཟེད་དང་ཆོས་གོས་བཞག་ནས། ཞབས་བསིལ་ཏེ་གདན་བཤམས་པ་ལ་སྐྱིལ་མོ་ཀྲུང་བཅས་ནས་སྐུ་དྲང་པོར་བསྲང་སྟེ། དྲན་པ་མངོན་དུ་བཞག་ནས་བཞུགས་སོ། །",
                "commentary": "ཟས་ཕྱི་མ་ཕྱི་དྲོའི་བསོད་སྙོམས་ཟ་བ་སྤངས་ནས། ལྷུང་བཟེད་སོགས་བཞག་ནས་ཞབས་བཀྲུས་ཤིང་བསིལ་ཏེ། གདན་བཤམས་པ་ཉིད་ལ་དཀྱིལ་མོ་ཀྲུང་བཅས་ནས་སྐུ་དྲང་པོར་སྲང་སྟེ། གཞུང་འདི་སྟོན་པར་འགྱུར་བ་མཁྱེན་པའི་དྲན་པ་མངོན་དུ་བཞག་ནས་བཞུགས་སོ། །",
                "target_language": "Chinese"
            },
            "assistant": {
                "output": "舍弃了下午的托钵食物，他放下了钵盂等物，洗净并冷却双脚，在准备好的座位上结跏趺坐，端正身体，他以将要宣讲此经典的智慧正念而安住。"
            }
        },
        {
            "human": {
                "root": "བཅོམ་ལྡན་འདས་ཀྱིས་དེ་སྐད་ཅེས་བཀའ་སྩལ་ནས།",
                "commentary": "འདི་ནི་མདོ་རྫོགས་པའི་མཇུག་གི་ཚིག་ཡིན་ལ། དེ་ཡང་བཅོམ་ལྡན་འདས་ཀྱིས་ཆོས་འདི་ཐམས་ཅད་གསུངས་ཟིན་པའི་རྗེས་སུ།",
                "target_language": "Chinese"
            },
            "assistant": {
                "output": "这是经文结尾的词语，是指世尊说完所有这些法之后。"
            }
        }
    ]

    # Get API key from environment variable
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables. Please set ANTHROPIC_API_KEY.")

    # Translate to Chinese with custom examples, more threads, and caching
    print("Translating to Chinese with custom examples and caching...")
    chinese_translations = translate_commentaries(
        commentary_root_pairs=sample_data,
        target_language="Chinese",
        few_shot_examples=custom_chinese_examples,
        num_threads=4,  # Use more threads for better performance
        api_key=api_key,
        use_cache=True,
        cache_dir="./translation_cache",  # Cache directory path
        cache_ttl=None  # No expiration
    )
    # Display the results
    print("\nChinese Translations:")
    for i, item in enumerate(chinese_translations):
        print(f"\nExample {i+1}:")
        print(f"Root (untranslated): {item['root']}")
        print(f"Commentary (original): {item['commentary']}")
        print(f"Commentary (translated): {item['commentary_translation']}")

    print("\nNote: Empty commentaries remain empty in the output, as required.")
    print("Using more threads improves performance with larger datasets.")
    
    # Demonstrate cache hit by running the same translation again
    print("\n\nRunning same translation again (should use cache)...")
    start_time = time.time()
    chinese_translations_cached = translate_commentaries(
        commentary_root_pairs=sample_data,
        target_language="Chinese",
        few_shot_examples=custom_chinese_examples,
        num_threads=4,
        api_key=api_key,
        use_cache=True,
        cache_dir="./translation_cache"
    )
    end_time = time.time()
    
    print(f"\nSecond run completed in {end_time - start_time:.2f} seconds (should be faster due to cache hits)")
    
    # Show cache statistics
    from claude_translator.cache import TranslationCache
    cache = TranslationCache(cache_dir="./translation_cache")
    cache_stats = cache.stats()
    print(f"\nCache statistics: {cache_stats}")
    
    print("\nTo clear the cache, you can use: cache.clear()")

if __name__ == "__main__":
    main()