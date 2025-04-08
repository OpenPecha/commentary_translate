# Tibetan Buddhist Commentary Translation Library

<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

## Table of contents
<p align="center">
  <a href="#project-description">Project description</a> •
  <a href="#who-this-project-is-for">Who this project is for</a> •
  <a href="#project-dependencies">Project dependencies</a> •
  <a href="#instructions-for-use">Instructions for use</a> •
  <a href="#contributing-guidelines">Contributing guidelines</a> •
  <a href="#additional-documentation">Additional documentation</a> •
  <a href="#how-to-get-help">How to get help</a> •
  <a href="#terms-of-use">Terms of use</a>
</p>
<hr>

## Project description

With the Tibetan Buddhist Commentary Translation Library, you can translate Tibetan Buddhist commentaries into multiple languages while preserving the root texts. This library efficiently processes commentary translations in parallel while ensuring empty commentary strings remain empty in the output.



## Project dependencies
Before using this library, ensure you have:
* Python 3.8+
* Anthropic API key with access to Claude models
* Required Python packages (installed via pip):
  * anthropic
  * python-dotenv

## Instructions for use
Get started with the Tibetan Buddhist Commentary Translation Library by setting up your environment and API key.

### Install the library
1. Install from PyPI:

   ```bash
   pip install claude-translator
   ```

   Or install from source:

   ```bash
   git clone https://github.com/yourusername/claude-translator.git
   cd claude-translator
   pip install -e .
   ```

2. Set up your API key:
 
   a. Create a `.env` file in your project root
   
   b. Add your Anthropic API key: `ANTHROPIC_API_KEY=your_api_key_here`

### Basic usage
1. Import the library and load your API key:

   ```python
   from dotenv import load_dotenv
   from claude_translator import translate_commentaries

   # Load API key from .env
   load_dotenv()
   ```

2. Prepare your data and translate:

   ```python
   # Sample data
   commentary_root_pairs = [
       {
           "root": "དེ་ནས་བཅོམ་ལྡན་འདས་མཉན་ཡོད་ཀྱི་གྲོང་ཁྱེར་ཆེན་པོར་བསོད་སྙོམས་ཀྱི་ཕྱིར་གཤེགས་ནས་ཞལ་ཟས་གསོལ་ཏེ་ཟས་ཀྱི་བྱ་བ་མཛད་དེ།",
           "commentary": "བསོད་སྙོམས་བླངས་ཏེ་མཇུག་ཏུ་སླར་བྱོན་ནས་ཞལ་ཟས་གསོལ་བའི་བྱ་བ་མཛད་དོ། །"
       },
       {
           "root": "གང་ཞིག་རྐྱེན་ལས་སྐྱེ་བ་དེ་ནི་རང་བཞིན་གྱིས་མ་སྐྱེས་པ་ཡིན་ནོ། །",
           "commentary": ""  # Empty commentary - will be preserved
       }
   ]

   # Translate commentaries to English
   translated_pairs = translate_commentaries(
       commentary_root_pairs=commentary_root_pairs,
       target_language="English",
       num_threads=2
   )

   # Display results
   for pair in translated_pairs:
       print(f"Root: {pair['root']}")
       print(f"Translated Commentary: {pair['commentary']}")
       print()
   ```

### Advanced features

1. Custom few-shot examples:

   ```python
   custom_examples = [
       {
           "human": {
               "root": "Tibetan root text here",
               "commentary": "Tibetan commentary here",
               "target_language": "English"
           },
           "assistant": {
               "output": "English translation here"
           }
       },
       # Add more examples...
   ]

   translated_pairs = translate_commentaries(
       commentary_root_pairs=commentary_root_pairs,
       target_language="English",
       few_shot_examples=custom_examples
   )
   ```

2. Multithreaded processing:

   ```python
   translated_pairs = translate_commentaries(
       commentary_root_pairs=large_dataset,
       target_language="English",
       num_threads=8  # Increase for larger datasets
   )
   ```

### Troubleshooting

<table>
  <tr>
   <td>
    Issue
   </td>
   <td>
    Solution
   </td>
  </tr>
  <tr>
   <td>
    API key not found
   </td>
   <td>
    Check that your .env file exists and contains ANTHROPIC_API_KEY=your_api_key_here
   </td>
  </tr>
  <tr>
   <td>
    Rate limiting errors
   </td>
   <td>
    Reduce the number of threads or implement a delay between API calls
   </td>
  </tr>
  <tr>
   <td>
    Translation quality issues
   </td>
   <td>
    Provide more specific few-shot examples for your target language and style
   </td>
  </tr>
</table>

## Contributing guidelines
If you'd like to help out, check out our [contributing guidelines](/CONTRIBUTING.md).

## Additional documentation

For more information:
* [Claude API documentation](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
* See the `examples/` directory for complete usage examples
* See the `docs/` directory for detailed documentation

## How to get help
* File an issue.
* Email us at openpecha[at]gmail.com.
* Join our [discord](https://discord.com/invite/7GFpPFSTeA).

## Terms of use
Tibetan Buddhist Commentary Translation Library is licensed under the [MIT License](/LICENSE.md).
