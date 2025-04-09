"""
Basic usage example for the Claude Translator library.
"""

import os
from dotenv import load_dotenv
from claude_translator import translate_commentaries

# Load environment variables from .env file
load_dotenv()

def main():
    # Sample Tibetan commentary-root pairs
    sample_data = [
        {
            "root": "དེ་ནས་བཅོམ་ལྡན་འདས་མཉན་ཡོད་ཀྱི་གྲོང་ཁྱེར་ཆེན་པོར་བསོད་སྙོམས་ཀྱི་ཕྱིར་གཤེགས་ནས་ཞལ་ཟས་གསོལ་ཏེ་ཟས་ཀྱི་བྱ་བ་མཛད་དེ",
            "commentary": "བསོད་སྙོམས་བླངས་ཏེ་མཇུག་ཏུ་སླར་བྱོན་ནས་ཞལ་ཟས་གསོལ་བའི་བྱ་བ་མཛདདོ། །"
        },
        {
            "root": "གང་ཞིག་རྐྱེན་ལས་སྐྱེ་བ་དེ་ནི་རང་བཞིན་གྱིས་མ་སྐྱེས་པ་ཡིན་ནོ། །",
            "commentary": ""  # Empty commentary - should remain empty
        },
        {
            "root": "",  # Empty root
            "commentary": "བཅོམ་ལྡན་འདས་བསོད་སྙོམས་ལ་འབྱོན་པ་ནི། རང་ཉིད་བསོད་སྙོམས་ཀྱི་ཟས་ཟ་དགོས་པའི་ཆེད་མིན་གྱི། གདུལ་བྱ་ལ་ཚོགས་གསོག་པ་དང་ཆོས་སྟོན་པ་སོགས་ཀྱི་ཆེད་དུའོ། །"
        }
    ]

    # Translate to English
    print("Translating to English...")
    english_translations = translate_commentaries(
        commentary_root_pairs=sample_data,
        target_language="German",
        num_threads=2
    )

    # Display the results
    print("\nEnglish Translations:")
    for i, item in enumerate(english_translations):
        print(f"\nExample {i+1}:")
        print(f"Root (untranslated): {item['root']}")
        print(f"Commentary (original): {item['commentary']}")
        print(f"Commentary (translated): {item['commentary_translation']}")

    # Translate to French
    print("\n\nTranslating to French...")
    french_translations = translate_commentaries(
        commentary_root_pairs=sample_data,
        target_language="French",
        num_threads=4
    )

    # Display the results
    print("\nFrench Translations:")
    for i, item in enumerate(french_translations):
        print(f"\nExample {i+1}:")
        print(f"Root (untranslated): {item['root']}")
        print(f"Commentary (original): {item['commentary']}")
        print(f"Commentary (translated): {item['commentary_translation']}")

if __name__ == "__main__":
    main()