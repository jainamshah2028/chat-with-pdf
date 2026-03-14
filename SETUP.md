# Setup and Installation Guide

This guide provides detailed instructions for setting up the **Chat with PDF** application for development or deployment.

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Linux, macOS, Windows (with WSL2 recommended on Windows)
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB free space

## Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_ORG/chat_with_pdf.git
cd chat_with_pdf
```

### 2. Create Virtual Environment

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
OPENAI_API_KEY=sk-your-actual-key-here
DEFAULT_PROVIDER=openai
```

### 5. Run the Application

```bash
streamlit run app_enhanced.py
```

The app will open at `http://localhost:8501`

---

## API Provider Setup

### OpenAI (Recommended)

1. Go to https://platform.openai.com/account/api-keys
2. Create a new API key
3. Add to `.env`:
   ```env
   OPENAI_API_KEY=sk-...
   DEFAULT_PROVIDER=openai
   ```

### HuggingFace

1. Create account at https://huggingface.co
2. Get your API token from Settings → Access Tokens
3. Add to `.env`:
   ```env
   HUGGINGFACE_API_KEY=hf_...
   DEFAULT_PROVIDER=huggingface
   ```

### Ollama (Local LLM)

1. Install Ollama from https://ollama.ai
2. Pull a model: `ollama pull llama2`
3. Ensure Ollama is running on `http://localhost:11434`
4. Add to `.env`:
   ```env
   DEFAULT_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   ```

See [docs/API_PROVIDERS.md](../docs/API_PROVIDERS.md) for detailed per-provider setup.

---

## Development Setup

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Install Pre-commit Hooks

```bash
pre-commit install
```

Pre-commit hooks will automatically format and lint your code on every commit.

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=. --cov-report=html

# Run specific test file
pytest tests/test_config.py -v

# Run tests matching pattern
pytest tests/ -k "test_openai" -v
```

### Code Formatting & Linting

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Check with flake8
flake8 .

# Type checking with mypy
mypy . --ignore-missing-imports

# All checks at once
black . && isort . && flake8 . && pytest tests/
```

---

## Docker Setup

### Build Docker Image

```bash
docker build -t chat-pdf:latest .
```

### Run with Docker

```bash
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=sk-your-key \
  -e DEFAULT_PROVIDER=openai \
  chat-pdf:latest
```

### Docker Compose (Recommended)

```bash
# Set up environment file
cp .env.example .env
# Edit .env with your API keys

# Start services
docker-compose up

# View logs
docker-compose logs -f chat-pdf

# Stop services
docker-compose down
```

Access at `http://localhost:8501`

---

## Troubleshooting

### "OPENAI_API_KEY not found"
- Ensure `.env` file exists in the project root
- Verify `OPENAI_API_KEY` is set in `.env`
- Check file is not in `.gitignore`

### Port 8501 already in use
```bash
# Change port in .env
STREAMLIT_SERVER_PORT=8502

# Or kill existing process:
# Linux/macOS: lsof -ti:8501 | xargs kill -9
# Windows: netstat -ano | findstr :8501
```

### Module import errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Slow PDF processing
- Check that PDF is not corrupted
- Verify sufficient RAM available
- Reduce `CHUNK_SIZE` in `.env` if needed

### Docker builds fail
```bash
# Clear Docker cache
docker system prune -a

# Rebuild
docker build -t chat-pdf:latest --no-cache .
```

---

## File Structure

```
chat_with_pdf/
├── app_enhanced.py          # Main application
├── config.py               # Configuration and LLM setup
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── .env.example           # Environment variables template
├── Dockerfile             # Container definition
├── docker-compose.yml     # Development container setup
├── tests/                 # Test suite
│   ├── test_config.py
│   ├── conftest.py
│   └── fixtures/
├── docs/                  # Documentation
│   ├── API_PROVIDERS.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── ENVIRONMENT.md
└── examples/              # Reference implementations
    ├── app_basic.py
    └── app_advanced.py
```

---

## Next Steps

- 📚 Read [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) to understand the codebase
- 🚀 See [docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md) for deployment options
- 🤝 Check [CONTRIBUTING.md](../CONTRIBUTING.md) to start contributing

---

For issues or questions, please open an [Issue](https://github.com/YOUR_ORG/chat_with_pdf/issues) or start a [Discussion](https://github.com/YOUR_ORG/chat_with_pdf/discussions).
