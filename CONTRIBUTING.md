# Contributing to Chat with PDF

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions. We're building a welcoming community for developers of all skill levels.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/chat_with_pdf.git
   cd chat_with_pdf
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
5. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

## Development Workflow

### Code Style

This project uses:
- **Black** for code formatting (line length: 88)
- **flake8** for linting
- **isort** for import sorting
- **pylint** for code analysis

All code is automatically formatted via pre-commit hooks before committing. To manually format:
```bash
black .
isort .
flake8 .
```

### Writing Tests

- Tests should be placed in the `tests/` directory
- Use `pytest` as the test framework
- Aim for >80% code coverage
- Follow naming convention: `test_<module_name>.py`

Example:
```bash
pytest tests/ -v --cov=. --cov-report=html
```

### Commit Messages

Use clear, descriptive commit messages:
- ✅ `"feat: add support for OCR in PDF processing"`
- ✅ `"fix: handle empty PDFs gracefully"`
- ✅ `"refactor: simplify config initialization"`
- ❌ `"update"`, `"fix bug"`, `"changes"`

Use conventional commits format: `type(scope): description`

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

### Creating a Pull Request

1. Create a feature branch:
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "feat: describe your changes"
   ```

3. Push to your fork:
   ```bash
   git push origin feat/your-feature-name
   ```

4. Open a Pull Request with:
   - Clear title describing the change
   - Description of what and why you changed it
   - Reference to any related issues (`Closes #123`)
   - Confirmation that tests pass locally

### Pull Request Checklist

- [ ] Code follows project style guidelines (pre-commit hooks pass)
- [ ] Tests written and pass (`pytest -v`)
- [ ] Code coverage maintained (>80%)
- [ ] Documentation updated if needed
- [ ] Commit messages follow conventional commits format
- [ ] No hardcoded API keys or secrets
- [ ] CI/CD checks pass on GitHub Actions

## Reporting Issues

### Bug Reports

Include:
- Clear title and description
- Steps to reproduce
- Expected vs. actual behavior
- Python version and OS
- Error logs/tracebacks

### Feature Requests

Include:
- Use case and motivation
- Proposed solution (if any)
- Alternative approaches considered

## Project Structure

```
chat_with_pdf/
├── app_enhanced.py       # Main application (primary version)
├── config.py             # Configuration and provider setup
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── tests/                # Test suite
├── docs/                 # Documentation
├── examples/             # Reference implementations
└── .github/workflows/    # CI/CD pipelines
```

## Documentation

- Update `README.md` for public-facing changes
- Update `docs/` files for detailed guides
- Add docstrings to new functions/classes
- Use Google-style docstrings:
  ```python
  def process_pdf(file_path: str) -> dict:
      """Process a PDF file and extract text.
      
      Args:
          file_path: Path to the PDF file.
          
      Returns:
          Dictionary containing extracted text and metadata.
      """
  ```

## Questions?

- Check existing issues and discussions
- Join our community discussions
- Comment on relevant issues
- Create a new discussion topic

## Recognition

Contributors will be recognized in:
- Project README
- Release notes for features
- GitHub contributors page

Thank you for helping make Chat with PDF better! 🎉
