# Contributing to LLM-Router

First off, thank you for considering contributing to LLM-Router! It's people like you that make this project a great tool for the community.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples and error logs
* Describe the behavior you observed and what you expected
* Include your environment details (OS, Python version, LLM provider)
* Sanitize any API keys or sensitive information

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples and use cases
* Explain why this enhancement would be useful to most users

### Pull Requests

* Fill in the required template
* Follow the Python style guide (PEP 8)
* Include thoughtful comments in English
* Add type hints where appropriate
* Write or update tests for your changes
* Update documentation as needed
* End all files with a newline

## Development Process

### Setting Up Development Environment

```bash
# Clone the repository
git clone git@github.com:legeling/LLM-Router.git
cd LLM-Router

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Copy example config
cp config/models.example.json config/models.json
# Edit config/models.json with your API keys
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_llm_service.py
```

### Code Style

* Follow PEP 8
* Use type hints for function signatures
* Write docstrings for all public methods (Google style)
* Use meaningful variable names
* Keep functions focused and small
* Maximum line length: 100 characters
* Use English for all code, comments, and documentation

### Example Code Style

```python
from typing import Dict, List, Optional

def process_llm_request(
    model_id: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> Dict[str, any]:
    """
    Process an LLM request and return the response.
    
    Args:
        model_id: Unique identifier for the LLM model
        messages: List of message dictionaries with 'role' and 'content'
        temperature: Sampling temperature (0.0 to 2.0)
        max_tokens: Maximum tokens to generate
        
    Returns:
        Dictionary containing the LLM response
        
    Raises:
        ModelNotFoundError: If the specified model doesn't exist
        APIError: If the LLM provider returns an error
    """
    # Implementation here
    pass
```

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests after the first line
* No emojis in commit messages

Example:
```
Add support for Anthropic Claude models

- Implement ClaudeService class
- Add configuration schema for Claude
- Update documentation with Claude examples

Fixes #123
```

### Documentation

* Update README.md for user-facing changes
* Update QUICKSTART.md for setup changes
* Add docstrings to all public APIs
* Include code examples where appropriate
* Keep documentation up to date with code changes

## Project Structure

```
LLM-Router/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models
│   ├── auth.py              # Authentication
│   ├── api/                 # API routes
│   │   ├── chat.py
│   │   └── models.py
│   └── services/            # LLM service implementations
│       └── llm_service.py
├── tests/                   # Test files
├── config/                  # Configuration files
├── .github/                 # GitHub templates
└── spec/                    # Internal specifications (gitignored)
```

## Adding a New LLM Provider

1. Create a new service class in `app/services/`
2. Inherit from `BaseLLMService`
3. Implement required methods: `chat_completion()`, `test_connection()`
4. Add provider configuration schema
5. Update documentation
6. Add tests

## Testing Guidelines

* Write tests for all new features
* Maintain or improve code coverage
* Use pytest fixtures for common setup
* Mock external API calls
* Test error handling and edge cases

## Questions?

Feel free to open an issue with your question or contact the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for your contributions!
