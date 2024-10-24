# SEO Content Transformer

A Python-based tool for transforming and optimizing content using OpenAI's GPT models. This tool helps rewrite content while maintaining SEO value and improving readability.

## Features

- Content rewriting with GPT models
- Maintains SEO optimization while improving readability
- Supports both text files and direct input
- Configurable rewriting parameters
- Preserves original content structure
- Handles numbered and unnumbered text formats

## Requirements

- Python 3.x
- OpenAI API key
- Required Python packages:
  - openai
  - python-dotenv
  - os
  - re

## Setup

1. Clone the repository:
```bash
git clone https://github.com/mali1sav/SEO-content-transformer.git
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

The script can be used in two ways:

1. Processing text files:
```python
from rewrite import rewrite_text_from_file

# Rewrite content from a file
rewrite_text_from_file('input.txt', 'output.txt')
```

2. Direct text processing:
```python
from rewrite import rewrite_text

text = "Your content here..."
rewritten_text = rewrite_text(text)
```

## How It Works

1. The script reads input text (either from a file or direct input)
2. Processes the text to identify numbered sections if present
3. Sends the content to OpenAI's GPT model for rewriting
4. Maintains the original structure while improving the content
5. Preserves any numerical ordering in the original text
6. Outputs the rewritten content either to a file or returns it directly

## Error Handling

The script includes error handling for:
- File operations
- API calls
- Text processing
- Environment variable configuration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
