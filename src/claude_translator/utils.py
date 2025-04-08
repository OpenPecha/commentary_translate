"""
Utility functions for the Tibetan Buddhist Commentary Translation Library.
"""

import logging
from typing import List, Dict

def setup_logging() -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger("claude_translator")
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create console handler
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
    
    return logger

def get_default_few_shot_examples(target_language: str) -> List[Dict]:
    """
    Return default few-shot examples for the specified target language.
    
    Args:
        target_language: Target language name (e.g., 'English', 'Chinese', 'French')
        
    Returns:
        List of dictionaries containing conversation examples for the specified language
    """
    # Define the multilingual few-shot examples as specified in the client requirements
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
    
    # Filter examples for the requested target language
    if target_language == "all":
        # Return all examples for multilingual training
        return few_shot_examples
    else:
        # Return only examples relevant to the requested language
        filtered_examples = [
            example for example in few_shot_examples 
            if example["human"]["target_language"] == target_language
        ]
        
        # If no examples found for the requested language, return English examples as fallback
        if not filtered_examples:
            filtered_examples = [
                example for example in few_shot_examples 
                if example["human"]["target_language"] == "English"
            ]
        
        return filtered_examples