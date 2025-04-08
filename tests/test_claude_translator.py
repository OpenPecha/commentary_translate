"""
Tests for the translation functionality of the Claude Translator.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from typing import List, Dict

from claude_translator.translator import translate_commentaries
from claude_translator.utils import get_default_few_shot_examples

# Sample test data
TEST_DATA = [
    {
        "root": "དེ་ནས་བཅོམ་ལྡན་འདས་མཉན་ཡོད་ཀྱི་གྲོང་ཁྱེར་ཆེན་པོར་བསོད་སྙོམས་ཀྱི་ཕྱིར་གཤེགས་ནས་ཞལ་ཟས་གསོལ་ཏེ་ཟས་ཀྱི་བྱ་བ་མཛད་དེ།",
        "commentary": "བསོད་སྙོམས་བླངས་ཏེ་མཇུག་ཏུ་སླར་བྱོན་ནས་ཞལ་ཟས་གསོལ་བའི་བྱ་བ་མཛད་དོ། །"
    },
    {
        "root": "གང་ཞིག་རྐྱེན་ལས་སྐྱེ་བ་དེ་ནི་རང་བཞིན་གྱིས་མ་སྐྱེས་པ་ཡིན་ནོ། །",
        "commentary": ""  # Empty commentary
    },
    {
        "root": "",  # Empty root
        "commentary": "བཅོམ་ལྡན་འདས་བསོད་སྙོམས་ལ་འབྱོན་པ་ནི། རང་ཉིད་བསོད་སྙོམས་ཀྱི་ཟས་ཟ་དགོས་པའི་ཆེད་མིན་གྱི། གདུལ་བྱ་ལ་ཚོགས་གསོག་པ་དང་ཆོས་སྟོན་པ་སོགས་ཀྱི་ཆེད་དུའོ། །"
    }
]

class MockResponse:
    def __init__(self, text):
        self.content = [MagicMock(text=text)]

@pytest.fixture
def mock_anthropic():
    """Mock the Anthropic client and API responses."""
    with patch('claude_translator.claude_api.anthropic.Anthropic') as mock_client:
        client_instance = MagicMock()
        mock_client.return_value = client_instance
        
        messages_mock = MagicMock()
        client_instance.messages = messages_mock
        
        create_mock = MagicMock()
        messages_mock.create = create_mock
        
        # Set up the mock to return different translations for different inputs
        def side_effect(*args, **kwargs):
            messages = kwargs.get('messages', [])
            # Get the input text from the last message
            if len(messages) > 0:
                input_text = messages[-1].get('content', [])[0].get('text', '')
                
                if "བསོད་སྙོམས་བླངས་ཏེ་མཇུག་ཏུ་སླར་བྱོན་ནས་ཞལ་ཟས་གསོལ་བའི་བྱ་བ་མཛད་དོ། །" in input_text:
                    return MockResponse("Having received alms, he returned afterward and partook of the meal.")
                elif "བཅོམ་ལྡན་འདས་བསོད་སྙོམས་ལ་འབྱོན་པ་ནི།" in input_text:
                    return MockResponse("The Blessed One goes for alms not because he himself needs to eat alms food, but for the sake of disciples to accumulate merit and teach the Dharma, among other purposes.")
            
            # Default response
            return MockResponse("Default translation")
        
        create_mock.side_effect = side_effect
        
        yield mock_client

def test_translate_commentaries_with_mock(mock_anthropic):
    """Test the translate_commentaries function with a mocked API."""
    # Test with English as target language
    result = translate_commentaries(
        commentary_root_pairs=TEST_DATA,
        target_language="English",
        api_key="mock_api_key"
    )
    
    # Check that the result has the same length as the input
    assert len(result) == len(TEST_DATA)
    
    # Check that the first item has been translated
    assert result[0]["root"] == TEST_DATA[0]["root"]
    assert result[0]["commentary"] == "Having received alms, he returned afterward and partook of the meal."
    
    # Check that empty commentary remains empty
    assert result[1]["commentary"] == ""
    
    # Check that the third item with empty root has been translated
    assert result[2]["root"] == ""
    assert result[2]["commentary"] == "The Blessed One goes for alms not because he himself needs to eat alms food, but for the sake of disciples to accumulate merit and teach the Dharma, among other purposes."

def test_default_examples():
    """Test that default examples are provided for supported languages."""
    english_examples = get_default_few_shot_examples("English")
    chinese_examples = get_default_few_shot_examples("Chinese")
    french_examples = get_default_few_shot_examples("French")
    
    # Check that we get examples for supported languages
    assert len(english_examples) > 0
    assert len(chinese_examples) > 0
    assert len(french_examples) > 0
    
    # Check that we get English examples as fallback for unsupported languages
    unknown_language_examples = get_default_few_shot_examples("Klingon")
    assert unknown_language_examples == english_examples