# 🧪 Testing Guide

This guide covers both automated testing (unit tests, CI/CD) and manual testing scenarios for the Chat with PDF application.

## Table of Contents
1. [Quick Start (Automated)](#quick-start-automated)
2. [Unit Tests](#unit-tests)
3. [Manual Test Scenarios](#manual-test-scenarios)
4. [Code Quality Checks](#code-quality-checks)
5. [GitHub Actions CI/CD](#github-actions-cicd)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start (Automated)

### Install Test Dependencies

```bash
# Install development tools
pip install -r requirements-dev.txt

# Install pre-commit hooks (auto-format on commit)
pre-commit install
```

### Run All Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=. --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

### Run Specific Tests

```bash
# Test configuration module only
pytest tests/test_config.py -v

# Test specific test class
pytest tests/test_config.py::TestConfigInitialization -v

# Test matching pattern
pytest tests/ -k "openai" -v

# Stop on first failure
pytest tests/ -x

# Show print statements
pytest tests/ -v -s
```

---

## Unit Tests

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures and config
├── test_config.py           # Tests for config.py module
├── fixtures/                # Sample test data
└── README.md               # Test documentation
```

### Available Tests

#### `test_config.py` — Configuration Module Tests

**What it tests:**
- Config initialization with different providers
- Environment variable loading
- API key validation
- Provider selection
- Error handling

**Test Classes:**
1. `TestConfigInitialization` — Config startup tests
2. `TestConfigMethods` — Config method functionality
3. `TestConfigEdgeCases` — Error handling & edge cases

**Run config tests:**
```bash
pytest tests/test_config.py -v
```

### Test Fixtures

Fixtures in `conftest.py` provide reusable test resources:

```python
# Mock environment variables
@pytest.fixture
def mock_env_vars()

# Mock OpenAI client
@pytest.fixture
def mock_openai_client()

# Sample text
@pytest.fixture
def sample_text()

# Sample chunks
@pytest.fixture
def sample_chunks()

# Mock FAISS index
@pytest.fixture
def mock_faiss_index()
```

**Use fixtures in tests:**
```python
def test_something(mock_env_vars, sample_text):
    # Use mock_env_vars and sample_text
    assert mock_env_vars["OPENAI_API_KEY"] == "test-key-12345"
```

### Writing New Tests

Template for adding tests:

```python
# tests/test_my_module.py
import pytest
from my_module import MyClass

class TestMyClass:
    """Test MyClass functionality."""

    def test_initialization(self, mock_env_vars):
        """Test MyClass initializes correctly."""
        obj = MyClass()
        assert obj is not None

    def test_method_works(self, sample_text):
        """Test MyClass method works."""
        obj = MyClass()
        result = obj.process(sample_text)
        assert result is not None
        
    @pytest.mark.skip(reason="Not implemented yet")
    def test_future_feature(self):
        """Test for future implementation."""
        pass
```

**Run your new tests:**
```bash
pytest tests/test_my_module.py -v
```

---

## Code Quality Checks

### Black (Code Formatting)

```bash
# Check formatting without changing files
black --check .

# Show what would change
black --diff .

# Format all Python files
black .
```

### isort (Import Sorting)

```bash
# Check import order
isort --check-only .

# Show what would change
isort --diff .

# Fix import order
isort .
```

### flake8 (Linting)

```bash
# Run linter
flake8 .

# Show statistics
flake8 . --statistics

# Ignore specific errors
flake8 . --extend-ignore=E203,W503
```

### pylint (Code Analysis)

```bash
# Advanced linting
find . -type f -name "*.py" ! -path "./venv/*" -exec pylint {} +

# Check specific file
pylint app_enhanced.py

# Generate report
pylint app_enhanced.py --output-format=text > lint_report.txt
```

### mypy (Type Checking)

```bash
# Check type hints
mypy . --ignore-missing-imports

# Verbose output
mypy . --verbose
```

### Run All Checks at Once

```bash
# Format and lint (ideal before committing)
black . && isort . && flake8 . && pytest tests/ -v
```

---

## Pre-commit Hooks

Pre-commit hooks automatically run on every commit:

```bash
# Install hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Run on staged files only
pre-commit run

# Skip hooks (not recommended)
git commit --no-verify
```

**Hooks configured:**
- Black (format)
- isort (import sort)
- flake8 (linting)
- Trailing whitespace removal
- YAML validation
- Merge conflict detection

---

## GitHub Actions CI/CD

### Automated Workflows

Two workflows run on every push and pull request:

#### 1. **Tests Workflow** (`.github/workflows/test.yml`)

Runs on: Every push and pull request

Steps:
- Set up Python (3.8, 3.9, 3.10, 3.11)
- Install dependencies
- Lint with flake8
- Format check with Black
- Import check with isort
- Run pytest with coverage
- Upload coverage to Codecov

**View results:**
1. Go to GitHub repo
2. Click **Actions**
3. Select **Tests** workflow
4. Click recent run to see details

#### 2. **Code Quality Workflow** (`.github/workflows/lint.yml`)

Runs on: Every push and pull request

Steps:
- Black formatting check
- isort import sorting check
- flake8 linting
- pylint code analysis
- mypy type checking

### Running Workflows Locally

Test workflows before pushing:

```bash
# Install act (runs GitHub Actions locally)
# macOS: brew install act
# Windows: choco install act-cli
# Linux: https://github.com/nektos/act

# Run all workflows
act

# Run specific workflow
act -j test

# Run with verbose output
act -v
```

### Viewing Coverage Reports

After tests pass:

1. Go to action run
2. Look for **Codecov** step
3. Click repo link to see coverage dashboard
4. Review coverage percentage by file

**Coverage thresholds:**
- Target: ≥80% overall
- Priority: Core modules (config.py, app functions)

---

## Manual Test Scenarios

### Test 1: Basic Functionality ⭐

1. **Start app:**
   ```bash
   streamlit run app_enhanced.py
   ```

2. **Upload a PDF**
   - Click "Upload PDF" button
   - Select a test PDF file
   - Wait for processing confirmation

3. **Ask a question**
   - Type a question in the chat input
   - Expected: Answer appears with sources

4. **Check features**
   - Chat history appears
   - Source citations are shown
   - Relevance scores visible

**Expected Results:**
- ✅ App loads without errors
- ✅ PDF uploads successfully
- ✅ Answers are contextual
- ✅ UI is responsive

### Test 2: Multi-File Upload

1. Upload 2-3 PDFs
2. Ask questions that might span multiple documents
3. Verify source attribution between files

**Expected:**
- Multiple files processed
- Answers reference correct sources
- No memory leaks during processing

### Test 3: Provider Switching

1. Upload a PDF with OpenAI provider
2. Get an answer
3. Change provider in config (or sidebar if available)
4. Upload same PDF again
5. Ask similar question

**Expected:**
- Both providers work
- Answers vary slightly (different models)
- No crashes on provider switch

### Test 4: Edge Cases

**Test 4a: Empty PDF**
- Upload an empty or corrupted PDF
- Expected: Graceful error message

**Test 4b: Very Large PDF**
- Upload a 50+ MB PDF
- Expected: Either processes or helpful error

**Test 4c: Special Characters**
- Upload PDF with special characters/languages
- Expected: Handles without error

**Test 4d: Missing API Keys**
- Remove API key from .env
- Run app
- Expected: Clear error message about missing key

### Test 5: Configuration

1. Modify `.env` values:
   - `CHUNK_SIZE=500`
   - `CHUNK_OVERLAP=0`
2. Restart app
3. Upload PDF and test search
4. Compare with defaults

**Expected:**
- Settings applied correctly
- Search results vary by chunk size
- No crashes on config changes

### Test 6: Docker Deployment

```bash
# Build image
docker build -t chat-pdf:test .

# Run container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=sk-your-test-key \
  chat-pdf:test

# Test in browser
open http://localhost:8501
```

**Expected:**
- Container builds without errors
- App runs on port 8501
- All features work same as local

---

## Test Coverage Report

Generate and view coverage:

```bash
# Generate HTML report
pytest tests/ --cov=. --cov-report=html

# View report
open htmlcov/index.html
```

**Coverage target:**
- Overall: ≥80%
- Critical modules: ≥85%
- config.py: ≥90%

---

## Performance Testing

### Load Testing (Optional)

```bash
# Install locust
pip install locust

# Create locustfile.py with test scenarios
# Run load tests
locust -f locustfile.py --host=http://localhost:8501
```

### Speed Testing

```bash
# Time a PDF processing
python -m cProfile -s cumtime app_enhanced.py

# Memory profiling
pip install memory-profiler
python -m memory_profiler app_enhanced.py
```

---

## Troubleshooting

### Tests Fail with "Module not found"

```bash
# Ensure dev dependencies installed
pip install -r requirements-dev.txt

# Ensure virtual env is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### Pre-commit hook fails

```bash
# View what failed
pre-commit run --all-files

# Fix automatically
black . && isort .

# Then try commit again
git commit -m "message"
```

### GitHub Actions fail but local tests pass

Common causes:
1. Different Python version (check `.github/workflows/test.yml`)
2. Missing environment variable
3. Platform-specific issue (Windows vs Linux path separators)

**Solution:**
```bash
# Test with same Python version as Actions
python3.10 -m pytest tests/ -v

# Export env vars
export OPENAI_API_KEY=test-key
```

### Coverage report shows 0%

```bash
# Ensure pytest-cov installed
pip install pytest-cov

# Run with coverage plugin
pytest tests/ --cov=. --cov-report=term-missing

# Check for syntax errors
python -m py_compile app_enhanced.py config.py
```

---

## Best Practices

✅ **Do:**
- Write tests for new features
- Run full test suite before committing
- Maintain >80% coverage
- Use meaningful test names
- Test error cases, not just happy paths
- Keep tests isolated and independent

❌ **Don't:**
- Skip failing tests temporarily
- Write tests that depend on external APIs
- Use hardcoded file paths
- Make tests too complex
- Ignore coverage gaps

---

## CI/CD Pipeline Summary

```
Code Push
   ↓
[GitHub Actions Triggered]
   ├─ test.yml
   │  ├─ Setup Python (3.8, 3.9, 3.10, 3.11)
   │  ├─ Install dependencies
   │  ├─ Lint (flake8, black, isort)
   │  ├─ Run tests (pytest)
   │  └─ Upload coverage (codecov)
   │
   └─ lint.yml
      ├─ Black check
      ├─ isort check
      ├─ flake8 check
      ├─ pylint check
      └─ mypy check
   ↓
[All pass?]
   ├─ YES → PR can merge
   └─ NO  → Blocking errors shown
```

---

For more information:
- 📚 [pytest documentation](https://docs.pytest.org)
- 🔍 [Coverage.py documentation](https://coverage.readthedocs.io)
- ⚙️ [GitHub Actions documentation](https://docs.github.com/en/actions)
- 💻 [Black documentation](https://black.readthedocs.io)

Questions? Open an [Issue](https://github.com/YOUR_ORG/chat_with_pdf/issues)!

### 📋 **Test 6: Error Handling**
1. **Try uploading a corrupted/protected PDF**
2. **See graceful error handling**
3. **Try with OpenAI but wrong API key**
4. **Check fallback to free option**

**Expected**: Clear error messages, helpful suggestions

## 🎯 **Success Criteria**

✅ **UI/UX**: Modern design loads properly  
✅ **Multi-file**: Can upload and process multiple PDFs  
✅ **Chat History**: Conversations are saved and exportable  
✅ **AI Providers**: Can switch between different providers  
✅ **Configuration**: Settings affect processing and results  
✅ **Search Quality**: Better answers with source attribution  
✅ **Error Handling**: Graceful failures with helpful messages  

## 🚨 **If Issues Occur**

### **Common Solutions**
- **UI not loading**: Refresh browser, check terminal for errors
- **Processing fails**: Try smaller PDFs, check file permissions
- **Slow performance**: Reduce chunk size, use fewer max results
- **Ollama errors**: Make sure Ollama is installed and running

### **Fallback Options**
- Use "Free (HuggingFace Only)" if API issues
- Use original app.py if enhanced version has problems
- Check terminal output for detailed error messages

## 📊 **Performance Comparison**

Test the same PDF with:
1. **Original app** (app.py)
2. **Enhanced app** with free option
3. **Enhanced app** with OpenAI

Compare:
- Answer quality
- Processing speed  
- User experience
- Feature availability

---

**Happy Testing! 🎉**
