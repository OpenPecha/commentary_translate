# Tibetan Buddhist Commentary Translation Library

## Project Overview
Create a Python library for translating Tibetan Buddhist commentaries. The library will handle translation of commentary text while preserving the root text for separate processing. The library must efficiently manage empty commentary strings and use multithreading for parallel processing of multiple commentary-root pairs.

## Core Requirements

### Input/Output Format
- **Input**: List of dictionaries, each containing "root" and "commentary" keys with Tibetan text
- **Output**: List of dictionaries with the same structure, but with translated commentary text
- **Important**: Empty commentary strings (`""`) must remain empty in the output

### Translation Capabilities
- Support translation into multiple languages (English, Chinese, French, etc.)
- Only translate the commentary text, leave root text unchanged
- Use Claude's API for translation quality
- Handle multi-turn translation with few-shot examples to guide translation style and terminology

### Performance Optimization
- Implement multithreading for parallel processing of commentary translations
- Skip processing of empty commentary strings (returning them as-is)
- Ensure efficient resource utilization

### Implementation Details
- Use the existing library template from the repository as foundation
- Read API key from .env file for security
- Implement proper error handling and logging
- Include comprehensive unit and integration tests

## API Design

```python
def translate_commentaries(
    commentary_root_pairs: List[Dict[str, str]],
    target_language: str,
    few_shot_examples: Optional[List[Dict]] = None,
    num_threads: int = 4,
    api_key: Optional[str] = None,
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
        
    Returns:
        List of dictionaries with 'root' (unchanged) and 'commentary' (translated) keys
    """
    # If few_shot_examples is None, use default examples
    if few_shot_examples is None:
        few_shot_examples = get_default_few_shot_examples(target_language)
    
    # Implementation continues...
```

## Multi-Turn Multilingual Few-Shot Example Format

The few-shot examples should follow a multi-turn conversation structure with language switching to better guide the Claude model in understanding proper translation patterns across multiple languages:

```python
few_shot_examples = [
    # First example - English translation
    {
        "human": {
            "root": "དེ་ནས་བཅོམ་ལྡན་འདས་མཉན་ཡོད་ཀྱི་གྲོང་ཁྱེར་ཆེན་པོར་བསོད་སྙོམས་ཀྱི་ཕྱིར་གཤེགས་ནས་ཞལ་ཟས་གསོལ་ཏེ་ཟས་ཀྱི་བྱ་བ་མཛད་དེ།",
            "commentary": "བསོད་སྙོམས་བླངས་ཏེ་མཇུག་ཏུ་སླར་བྱོན་ནས་ཞལ་ཟས་གསོལ་བའི་བྱ་བ་མཛད་དོ། །",
            "target_language": "English"
        },
        "assistant": {
            "output": "Having received alms, he returned afterward and partook of the meal."
        }
    },
    # Same example - Chinese translation
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
    # Same example - French translation
    {
        "human": {
            "root": "དེ་ནས་བཅོམ་ལྡན་འདས་མཉན་ཡོད་ཀྱི་གྲོང་ཁྱེར་ཆེན་པོར་བསོད་སྙོམས་ཀྱི་ཕྱིར་གཤེགས་ནས་ཞལ་ཟས་གསོལ་ཏེ་ཟས་ཀྱི་བྱ་བ་མཛད་དེ།",
            "commentary": "བསོད་སྙོམས་བླངས་ཏེ་མཇུག་ཏུ་སླར་བྱོན་ནས་ཞལ་ཟས་གསོལ་བའི་བྱ་བ་མཛད་དོ། །",
            "target_language": "French"
        },
        "assistant": {
            "output": "Ayant reçu des aumônes, il revint ensuite et prit son repas."
        }
    },
    # Second example - English translation
    {
        "human": {
            "root": "ཟས་ཕྱི་མའི་བསོད་སྙོམས་སྤངས་ནས་ལྷུང་བཟེད་དང་ཆོས་གོས་བཞག་ནས། ཞབས་བསིལ་ཏེ་གདན་བཤམས་པ་ལ་སྐྱིལ་མོ་ཀྲུང་བཅས་ནས་སྐུ་དྲང་པོར་བསྲང་སྟེ། དྲན་པ་མངོན་དུ་བཞག་ནས་བཞུགས་སོ། །",
            "commentary": "ཟས་ཕྱི་མ་ཕྱི་དྲོའི་བསོད་སྙོམས་ཟ་བ་སྤངས་ནས། ལྷུང་བཟེད་སོགས་བཞག་ནས་ཞབས་བཀྲུས་ཤིང་བསིལ་ཏེ། གདན་བཤམས་པ་ཉིད་ལ་དཀྱིལ་མོ་ཀྲུང་བཅས་ནས་སྐུ་དྲང་པོར་སྲང་སྟེ། གཞུང་འདི་སྟོན་པར་འགྱུར་བ་མཁྱེན་པའི་དྲན་པ་མངོན་དུ་བཞག་ནས་བཞུགས་སོ། །",
            "target_language": "English"
        },
        "assistant": {
            "output": "Having given up the afternoon alms food, he set aside his alms bowl and so forth, washed and cooled his feet, and sat in the full lotus posture on the prepared seat, straightened his body, and established mindfulness of his knowledge that he would teach this scripture."
        }
    },
    # Same example - Chinese translation
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
    # Third example with empty root - English translation
    {
        "human": {
            "root": "",
            "commentary": "བཅོམ་ལྡན་འདས་བསོད་སྙོམས་ལ་འབྱོན་པ་ནི། རང་ཉིད་བསོད་སྙོམས་ཀྱི་ཟས་ཟ་དགོས་པའི་ཆེད་མིན་གྱི། གདུལ་བྱ་ལ་ཚོགས་གསོག་པ་དང་ཆོས་སྟོན་པ་སོགས་ཀྱི་ཆེད་དུའོ། །",
            "target_language": "English"
        },
        "assistant": {
            "output": "The Blessed One goes for alms not because he himself needs to eat alms food, but for the sake of disciples to accumulate merit and teach the Dharma, among other purposes."
        }
    },
    # Example with empty commentary - French translation
    {
        "human": {
            "root": "གང་ཞིག་རྐྱེན་ལས་སྐྱེ་བ་དེ་ནི་རང་བཞིན་གྱིས་མ་སྐྱེས་པ་ཡིན་ནོ། །",
            "commentary": "",
            "target_language": "French"
        },
        "assistant": {
            "output": ""
        }
    }
]
```

This format provides:
1. Multiple turns of conversation with language switching for the same texts
2. Examples using authentic Tibetan Buddhist text and commentary pairs
3. Clear demonstration of how to handle empty root or commentary strings
4. Consistent structure showing target language in the input and only the translated commentary in the output
5. Preservation of specialized Buddhist terminology across languages

The multi-turn multilingual structure helps Claude understand how to maintain consistent translations of Buddhist terminology across different languages while preserving the conversation flow.

## Implementation Guidelines

### Environment Setup
- Use Claude's Python SDK (Claude SDK readme.md in this repository)
- Read API key from .env file using python-dotenv
- Implement proper exception handling for API failures

### Default Few-Shot Examples
The library should include default few-shot examples for common languages to ensure quality translations even when custom examples aren't provided:

```python
def get_default_few_shot_examples(target_language: str) -> List[Dict]:
    """
    Return default few-shot examples for the specified target language.
    
    Args:
        target_language: Target language name (e.g., 'English', 'Chinese', 'French')
        
    Returns:
        List of dictionaries containing conversation examples for the specified language
    """
    # Common examples dictionary
    default_examples = {
        "English": [
            {
                "human": {
                    "root": "དེ་ནས་བཅོམ་ལྡན་འདས་མཉན་ཡོད་ཀྱི་གྲོང་ཁྱེར་ཆེན་པོར་བསོད་སྙོམས་ཀྱི་ཕྱིར་གཤེགས་ནས་ཞལ་ཟས་གསོལ་ཏེ་ཟས་ཀྱི་བྱ་བ་མཛད་དེ།",
                    "commentary": "བསོད་སྙོམས་བླངས་ཏེ་མཇུག་ཏུ་སླར་བྱོན་ནས་ཞལ་ཟས་གསོལ་བའི་བྱ་བ་མཛད་དོ། །",
                    "target_language": "English"
                },
                "assistant": {
                    "output": "Having received alms, he returned afterward and partook of the meal."
                }
            },
            {
                "human": {
                    "root": "ཟས་ཕྱི་མའི་བསོད་སྙོམས་སྤངས་ནས་ལྷུང་བཟེད་དང་ཆོས་གོས་བཞག་ནས། ཞབས་བསིལ་ཏེ་གདན་བཤམས་པ་ལ་སྐྱིལ་མོ་ཀྲུང་བཅས་ནས་སྐུ་དྲང་པོར་བསྲང་སྟེ། དྲན་པ་མངོན་དུ་བཞག་ནས་བཞུགས་སོ། །",
                    "commentary": "ཟས་ཕྱི་མ་ཕྱི་དྲོའི་བསོད་སྙོམས་ཟ་བ་སྤངས་ནས། ལྷུང་བཟེད་སོགས་བཞག་ནས་ཞབས་བཀྲུས་ཤིང་བསིལ་ཏེ། གདན་བཤམས་པ་ཉིད་ལ་དཀྱིལ་མོ་ཀྲུང་བཅས་ནས་སྐུ་དྲང་པོར་སྲང་སྟེ། གཞུང་འདི་སྟོན་པར་འགྱུར་བ་མཁྱེན་པའི་དྲན་པ་མངོན་དུ་བཞག་ནས་བཞུགས་སོ། །",
                    "target_language": "English"
                },
                "assistant": {
                    "output": "Having given up the afternoon alms food, he set aside his alms bowl and so forth, washed and cooled his feet, and sat in the full lotus posture on the prepared seat, straightened his body, and established mindfulness of his knowledge that he would teach this scripture."
                }
            }
        ],
        "Chinese": [
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
            }
        ],
        "French": [
            {
                "human": {
                    "root": "དེ་ནས་བཅོམ་ལྡན་འདས་མཉན་ཡོད་ཀྱི་གྲོང་ཁྱེར་ཆེན་པོར་བསོད་སྙོམས་ཀྱི་ཕྱིར་གཤེགས་ནས་ཞལ་ཟས་གསོལ་ཏེ་ཟས་ཀྱི་བྱ་བ་མཛད་དེ།",
                    "commentary": "བསོད་སྙོམས་བླངས་ཏེ་མཇུག་ཏུ་སླར་བྱོན་ནས་ཞལ་ཟས་གསོལ་བའི་བྱ་བ་མཛད་དོ། །",
                    "target_language": "French"
                },
                "assistant": {
                    "output": "Ayant reçu des aumônes, il revint ensuite et prit son repas."
                }
            },
            {
                "human": {
                    "root": "ཟས་ཕྱི་མའི་བསོད་སྙོམས་སྤངས་ནས་ལྷུང་བཟེད་དང་ཆོས་གོས་བཞག་ནས། ཞབས་བསིལ་ཏེ་གདན་བཤམས་པ་ལ་སྐྱིལ་མོ་ཀྲུང་བཅས་ནས་སྐུ་དྲང་པོར་བསྲང་སྟེ། དྲན་པ་མངོན་དུ་བཞག་ནས་བཞུགས་སོ། །",
                    "commentary": "ཟས་ཕྱི་མ་ཕྱི་དྲོའི་བསོད་སྙོམས་ཟ་བ་སྤངས་ནས། ལྷུང་བཟེད་སོགས་བཞག་ནས་ཞབས་བཀྲུས་ཤིང་བསིལ་ཏེ། གདན་བཤམས་པ་ཉིད་ལ་དཀྱིལ་མོ་ཀྲུང་བཅས་ནས་སྐུ་དྲང་པོར་སྲང་སྟེ། གཞུང་འདི་སྟོན་པར་འགྱུར་བ་མཁྱེན་པའི་དྲན་པ་མངོན་དུ་བཞག་ནས་བཞུགས་སོ། །",
                    "target_language": "French"
                },
                "assistant": {
                    "output": "Ayant renoncé à la nourriture d'aumône de l'après-midi, il déposa son bol et ses effets, se lava et rafraîchit les pieds, s'assit en posture du lotus complet sur le siège préparé, redressa son corps, et établit la pleine conscience de sa connaissance qu'il allait enseigner ce texte."
                }
            }
        ]
        # Add more languages as needed
    }
    
    # Return examples for requested language, or English as fallback
    return default_examples.get(target_language, default_examples["English"])
```

### Threading Implementation
1. Create a thread pool based on num_threads parameter
2. Filter out empty commentaries before processing
3. Process valid commentaries in parallel
4. Reconstruct the full result list preserving original order and empty strings

### Error Handling
- Implement proper error handling for API rate limits
- Handle network issues with appropriate retries
- Log all errors for debugging

### Testing Requirements
- Unit tests for all core functions
- Integration tests with mock API responses
- Test cases for empty commentaries
- Test multithreading functionality
- Test with various language combinations

## Example Implementation Structure

```
tibetan_translator/
├── __init__.py
├── translator.py
├── threading.py
├── claude_api.py
├── utils.py
└── tests/
    ├── __init__.py
    ├── test_translator.py
    ├── test_threading.py
    ├── test_claude_api.py
    └── test_utils.py
```

## Claude SDK Integration

Follow the Claude Python SDK guidelines for implementation:
- Use appropriate authentication methods
- Implement proper prompt construction for few-shot examples
- Handle API response parsing correctly
- Implement rate limiting and retry logic

## Important Constraints
1. The library MUST preserve empty commentary strings as empty
2. Root text MUST remain untranslated
3. Translation MUST only happen for non-empty commentary text
4. The library MUST maintain the original order of input dictionaries

## Performance Expectations
- The library should efficiently process large batches of commentaries
- Threading should provide significant speedup for large inputs
- Proper resource management to avoid unnecessary API calls

## Documentation Requirements
- Clear installation instructions
- API documentation with examples
- Explanation of few-shot example format
- Usage examples for different languages
- Performance optimization guidelines
