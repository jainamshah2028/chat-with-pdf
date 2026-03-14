# Environment Variables Reference

This document explains all available environment variables for configuring the Chat with PDF application.

## Quick Setup

```bash
# Copy template
cp .env.example .env

# Edit with your values
nano .env  # Linux/macOS
# or
notepad .env  # Windows
```

Never commit `.env` to version control. It should stay in `.gitignore`.

---

## LLM Provider Configuration

### OpenAI Configuration

```env
# Required for OpenAI provider
OPENAI_API_KEY=sk-your-actual-api-key

# Model selection (optional, defaults to gpt-3.5-turbo)
OPENAI_MODEL=gpt-3.5-turbo
# Options: gpt-3.5-turbo, gpt-4, gpt-4-turbo-preview
```

**Get your key at:** https://platform.openai.com/account/api-keys

### HuggingFace Configuration

```env
# Required for HuggingFace provider
HUGGINGFACE_API_KEY=hf_your-access-token

# Model repository ID
HUGGINGFACE_REPO_ID=mistralai/Mistral-7B-Instruct-v0.1
```

**Get your token at:** https://huggingface.co/settings/tokens

**Popular models:**
- `gpt2` (fastest, smallest)
- `mistralai/Mistral-7B-Instruct-v0.1` (balanced)
- `meta-llama/Llama-2-70b-chat-hf` (most capable)

### Ollama Configuration

```env
# Connection details (optional, defaults shown)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

**Setup Ollama:**
```bash
# Download at https://ollama.ai
ollama pull mistral
ollama serve
```

### Default Provider Selection

```env
# Choose which provider to use
DEFAULT_PROVIDER=openai
# Options: "openai", "huggingface", "ollama"
```

---

## Streamlit Settings

```env
# Server port (default: 8501)
STREAMLIT_SERVER_PORT=8501

# Run headless (for Docker/servers)
STREAMLIT_SERVER_HEADLESS=true

# Show error details (development only)
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=true

# Logging level
STREAMLIT_LOGGER_LEVEL=info
# Options: debug, info, warning, error, critical
```

---

## PDF Processing Settings

```env
# Maximum PDF file size (in MB)
MAX_PDF_SIZE_MB=20

# Text chunk size (characters)
CHUNK_SIZE=1000

# Overlap between chunks (characters)
CHUNK_OVERLAP=100
```

### Tuning Advice

**Smaller chunks:**
- ✅ More precise search results
- ✅ Better for small documents
- ❌ More tokens needed
- Example: `CHUNK_SIZE=500` for technical docs

**Larger chunks:**
- ✅ Fewer API calls
- ✅ Cheaper
- ❌ Less precise results
- Example: `CHUNK_SIZE=2000` for novels

**Overlap:**
- ✅ Maintains context continuity
- ❌ Slight performance increase
- Default: `CHUNK_OVERLAP=100`

---

## Embedding & Search Settings

```env
# Embedding model (HuggingFace hosted)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**Popular options:**
- `all-MiniLM-L6-v2` (fast, default)
- `all-mpnet-base-v2` (better quality, slower)
- `multi-qa-MiniLM-L6-cos-v1` (for Q&A tasks)

---

## Application Settings

```env
# Application name (for display)
APP_NAME=Chat with PDF

# Debug mode (verbose logging)
DEBUG=false
# Set to true for development

# Logging level
LOG_LEVEL=INFO
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## Docker-Specific Settings

When running in Docker, these settings are useful:

```env
# Prevent buffering of Python output (Docker)
PYTHONUNBUFFERED=1

# Allow connections from all interfaces (Docker)
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Disable file watcher (Docker)
STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
```

---

## Development Environment

```env
# Enable debug mode for verbose output
DEBUG=true

# Log level for development
LOG_LEVEL=DEBUG

# Show Streamlit details
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=true
STREAMLIT_LOGGER_LEVEL=debug
```

---

## Production Environment

```env
# Disable debug mode
DEBUG=false

# Only log important messages
LOG_LEVEL=WARNING

# Hide error details from users
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false

# Disable development features
STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
```

---

## Complete .env Template

```env
# ============ LLM Provider ============
OPENAI_API_KEY=sk-your-key-here
DEFAULT_PROVIDER=openai
OPENAI_MODEL=gpt-3.5-turbo

# Optional: Alternative providers
HUGGINGFACE_API_KEY=hf_your-token
HUGGINGFACE_REPO_ID=mistralai/Mistral-7B-Instruct-v0.1
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# ============ Streamlit Settings ============
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# ============ PDF Processing ============
MAX_PDF_SIZE_MB=20
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# ============ Application ============
APP_NAME=Chat with PDF
DEBUG=false
LOG_LEVEL=INFO
```

---

## Security Guidelines

### Do's ✅
- Keep `.env` in `.gitignore`
- Use strong API keys
- Rotate keys regularly
- Use service accounts (not personal keys)
- Limit key permissions to minimum needed

### Don'ts ❌
- Never commit `.env` file
- Never hardcode keys in code
- Never share keys in issues/discussions
- Never use keys in logs/error messages
- Never use same key across environments

### Secret Rotation

If you accidentally expose a key:

**OpenAI:**
1. Go to https://platform.openai.com/account/api-keys
2. Delete compromised key
3. Generate new key
4. Update `.env`

**HuggingFace:**
1. Go to https://huggingface.co/settings/tokens
2. Click ⏱️ on compromised token
3. Generate new token
4. Update `.env`

---

## Accessing Environment Variables in Code

### In app_enhanced.py

```python
import os

# Direct access
api_key = os.getenv("OPENAI_API_KEY")

# With default
model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Required variable (raise error if missing)
api_key = os.environ["OPENAI_API_KEY"]  # Raises KeyError if missing
```

### In Streamlit Cloud

Use `st.secrets`:

```python
import streamlit as st

api_key = st.secrets["OPENAI_API_KEY"]
model = st.secrets.get("OPENAI_MODEL", "gpt-3.5-turbo")
```

---

## Troubleshooting

### "Variable not found" Error

```bash
# Check variables are set
echo $OPENAI_API_KEY  # Linux/macOS
echo %OPENAI_API_KEY%  # Windows PowerShell

# Reload shell if just added
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### Docker: Env Vars Not Loading

```bash
# Verify .env file passed to container
docker run -p 8501:8501 --env-file .env YOUR_IMAGE

# Or set individually
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-... YOUR_IMAGE
```

### Streamlit Cloud: Secrets Not Working

1. Go to app Settings
2. Click **Secrets** tab
3. Paste values in TOML format
4. **Restart** app from menu

---

## Environment-Specific Configs

### Development (.env.dev)
```env
DEBUG=true
LOG_LEVEL=DEBUG
DEFAULT_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

### Testing (.env.test)
```env
DEBUG=true
LOG_LEVEL=DEBUG
OPENAI_API_KEY=test-key-for-mocks
```

### Production (.env.prod)
```env
DEBUG=false
LOG_LEVEL=WARNING
DEFAULT_PROVIDER=openai
MAX_PDF_SIZE_MB=100
```

Load specific file:
```bash
# Linux/macOS
export $(cat .env.prod | xargs)

# Windows PowerShell
Get-Content .env.prod | ForEach-Object {
    if ($_ -and -not $_.StartsWith("#")) {
        $name, $value = $_.split("=")
        [Environment]::SetEnvironmentVariable($name, $value)
    }
}
```

---

For more help, see:
- [SETUP.md](../SETUP.md) — Installation guide
- [API_PROVIDERS.md](./API_PROVIDERS.md) — Provider setup details
- [CONTRIBUTING.md](../CONTRIBUTING.md) — Development guidelines

Open an [Issue](https://github.com/YOUR_ORG/chat_with_pdf/issues) if you have questions!
