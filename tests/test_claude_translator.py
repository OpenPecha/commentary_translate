"""
Tests for the translation functionality of the Claude Translator.
"""

import os
import pytest
import tempfile
import shutil
import time
from unittest.mock import patch, MagicMock, call
from typing import List, Dict

from claude_translator.translator import translate_commentaries
from claude_translator.utils import get_default_few_shot_examples
from claude_translator.cache import TranslationCache

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
    assert result[0]["commentary"] == TEST_DATA[0]["commentary"]  # Original preserved
    assert result[0]["commentary_translation"] == "Having received alms, he returned afterward and partook of the meal."
    
    # Check that empty commentary remains empty
    assert result[1]["commentary"] == ""
    assert result[1]["commentary_translation"] == ""
    
    # Check that the third item with empty root has been translated
    assert result[2]["root"] == ""
    assert result[2]["commentary"] == TEST_DATA[2]["commentary"]  # Original preserved
    assert result[2]["commentary_translation"] == "The Blessed One goes for alms not because he himself needs to eat alms food, but for the sake of disciples to accumulate merit and teach the Dharma, among other purposes."

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

@pytest.fixture
def temp_cache_dir():
    """Create a temporary directory for cache testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after the test
    shutil.rmtree(temp_dir)

def test_translation_cache_basic():
    """Test basic cache functionality."""
    # Create a cache in a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        cache = TranslationCache(cache_dir=temp_dir)
        
        # Test storing and retrieving a translation
        root = "Root text"
        commentary = "Commentary text"
        target_language = "English"
        translation = "Translated commentary"
        
        # Initially cache should be empty
        assert cache.get(root, commentary, target_language) is None
        
        # Store in cache
        cache.set(root, commentary, target_language, translation)
        
        # Retrieve from cache
        cached = cache.get(root, commentary, target_language)
        assert cached == translation
        
        # Check stats
        stats = cache.stats()
        assert stats["files"] == 1
        assert stats["memory_entries"] == 1
        
        # Clear cache
        cache.clear()
        assert cache.get(root, commentary, target_language) is None
        stats = cache.stats()
        assert stats["files"] == 0
        assert stats["memory_entries"] == 0

def test_cache_ttl():
    """Test cache time-to-live functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a cache with a 1-second TTL
        cache = TranslationCache(cache_dir=temp_dir, ttl=1)
        
        root = "Root text"
        commentary = "Commentary text"
        target_language = "English"
        translation = "Translated commentary"
        
        # Store in cache
        cache.set(root, commentary, target_language, translation)
        
        # Should be available immediately
        assert cache.get(root, commentary, target_language) == translation
        
        # Wait for TTL to expire
        time.sleep(1.1)
        
        # Should now be expired
        assert cache.get(root, commentary, target_language) is None

@patch('claude_translator.claude_api.anthropic.Anthropic')
def test_translator_with_cache(mock_anthropic, temp_cache_dir):
    """Test that the translator uses the cache correctly."""
    # Setup mock
    client_instance = MagicMock()
    mock_anthropic.return_value = client_instance
    
    messages_mock = MagicMock()
    client_instance.messages = messages_mock
    
    create_mock = MagicMock()
    messages_mock.create = create_mock
    create_mock.return_value = MockResponse("Test translation")
    
    # First call - should use API
    result1 = translate_commentaries(
        commentary_root_pairs=[
            {"root": "Test root", "commentary": "Test commentary"}
        ],
        target_language="English",
        api_key="mock_api_key",
        use_cache=True,
        cache_dir=temp_cache_dir
    )
    
    # Second call with same data - should use cache
    result2 = translate_commentaries(
        commentary_root_pairs=[
            {"root": "Test root", "commentary": "Test commentary"}
        ],
        target_language="English",
        api_key="mock_api_key",
        use_cache=True,
        cache_dir=temp_cache_dir
    )
    
    # API should be called only once
    assert create_mock.call_count == 1
    
    # Both results should be the same
    assert result1[0]["commentary_translation"] == result2[0]["commentary_translation"]
    
    # Third call with different data - should use API again
    result3 = translate_commentaries(
        commentary_root_pairs=[
            {"root": "Different root", "commentary": "Different commentary"}
        ],
        target_language="English",
        api_key="mock_api_key",
        use_cache=True,
        cache_dir=temp_cache_dir
    )
    
    # API should now be called twice
    assert create_mock.call_count == 2
    
@patch('claude_translator.claude_api.anthropic.Anthropic')
def test_translator_with_cache_disabled(mock_anthropic, temp_cache_dir):
    """Test that the translator doesn't use the cache when disabled."""
    # Setup mock
    client_instance = MagicMock()
    mock_anthropic.return_value = client_instance
    
    messages_mock = MagicMock()
    client_instance.messages = messages_mock
    
    create_mock = MagicMock()
    messages_mock.create = create_mock
    create_mock.return_value = MockResponse("Test translation")
    
    # First call with same data but cache disabled
    translate_commentaries(
        commentary_root_pairs=[
            {"root": "Test root", "commentary": "Test commentary"}
        ],
        target_language="English",
        api_key="mock_api_key",
        use_cache=False,
        cache_dir=temp_cache_dir
    )
    
    # Second call with same data and cache still disabled
    translate_commentaries(
        commentary_root_pairs=[
            {"root": "Test root", "commentary": "Test commentary"}
        ],
        target_language="English",
        api_key="mock_api_key",
        use_cache=False,
        cache_dir=temp_cache_dir
    )
    
    # API should be called twice since caching is disabled
    assert create_mock.call_count == 2