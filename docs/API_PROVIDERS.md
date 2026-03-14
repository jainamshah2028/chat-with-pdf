# API Provider Configuration Guide

This document provides detailed setup instructions for each supported LLM provider.

## Quick Reference

| Provider | Setup Complexity | Cost | Recommended For |
|----------|------------------|------|-----------------|
| **OpenAI** | Low | Paid | Production, reliability |
| **HuggingFace** | Medium | Free/Paid | Experimentation, cost-conscious |
| **Ollama** | Medium | Free | Local dev, privacy-focused |

---

## OpenAI ⭐ (Recommended)

### What You Get
- Most capable models (GPT-4, GPT-4 Turbo)
- Reliable API with 99.9% uptime
- Excellent documentation
- Pay per token (cheap at scale)

### Setup Steps

#### 1. Create an API Key
1. Go to https://platform.openai.com/account/api-keys
2. Sign up or log in
3. Click **Create new secret key**
4. Copy the key (starts with `sk-`)

#### 2. Add to Environment

```bash
# Create .env file from template
cp .env.example .env

# Edit .env and add your key
OPENAI_API_KEY=sk-your-actual-key-here
DEFAULT_PROVIDER=openai
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4, gpt-4-turbo
```

#### 3. Verify Setup

```bash
python -c "from config import Config; c = Config(); print('OpenAI ready!')"
```

### Model Options

```env
# Recommended (fastest, cheapest)
OPENAI_MODEL=gpt-3.5-turbo

# More capable (slower, more expensive)
OPENAI_MODEL=gpt-4

# Latest & best (preview, may change)
OPENAI_MODEL=gpt-4-turbo-preview
```

### Pricing
- **gpt-3.5-turbo**: $0.0005 per 1K input tokens
- **gpt-4**: $0.03 per 1K input tokens
- Typical conversation: ~100-500 tokens

### Troubleshooting

**"Invalid API key"**
- Verify key starts with `sk-`
- Check key is not in quotes in .env
- Ensure no leading/trailing spaces

**"Rate limit exceeded"**
- Wait a minute before retrying
- Consider upgrading account
- Implement exponential backoff

**"Insufficient quota"**
- Add payment method: https://platform.openai.com/account/billing/overview
- Check current usage: https://platform.openai.com/account/billing/usage

---

## HuggingFace

### What You Get
- Free tier with rate limits (50K requests/month)
- Thousands of models available
- Community-driven development
- Privacy-friendly (local inference available)

### Setup Steps

#### 1. Get API Token
1. Go to https://huggingface.co (sign up if needed)
2. Click profile → Settings
3. Go to **Access Tokens**
4. Click **New token**, set to **Read**
5. Copy the token

#### 2. Add to Environment

```bash
# Edit .env
HUGGINGFACE_API_KEY=hf_your-token-here
DEFAULT_PROVIDER=huggingface
HUGGINGFACE_REPO_ID=mistralai/Mistral-7B-Instruct-v0.1
```

#### 3. Choose a Model

Popular free options on HuggingFace:

```env
# Fastest
HUGGINGFACE_REPO_ID=gpt2

# Balanced (recommended)
HUGGINGFACE_REPO_ID=mistralai/Mistral-7B-Instruct-v0.1

# Most capable (slower)
HUGGINGFACE_REPO_ID=meta-llama/Llama-2-70b-chat-hf
```

Access model via: https://huggingface.co/{repo_id}

#### 4. Verify Setup

```bash
python -c "from config import Config; c = Config(); print('HuggingFace ready!')"
```

### Rate Limits

Free tier limits:
- 50,000 requests/month
- ~1600 requests/day
- ~67 requests/hour

### Troubleshooting

**"API rate limit exceeded"**
- Free tier is limited; wait before retrying
- Upgrade to Pro: https://huggingface.co/pricing

**"Model not found"**
- Verify repo ID is correct
- Check model requires license acceptance
- Some models require manual acceptance: visit https://huggingface.co/{repo_id}

**"Token is invalid"**
- Verify token from: https://huggingface.co/settings/tokens
- Regenerate if expired

---

## Ollama (Local LLM)

### What You Get
- 100% private (runs locally)
- No API costs
- Works offline
- Good for development

### Setup Steps

#### 1. Install Ollama
1. Download from https://ollama.ai
2. Follow installation for your OS
3. Open terminal/command prompt

#### 2. Download a Model

```bash
ollama pull mistral
# or
ollama pull llama2
# or any other model: ollama pull <model_name>
```

List available models at: https://ollama.ai/library

#### 3. Start Ollama Server

```bash
# On macOS/Linux
ollama serve

# On Windows (should auto-start after installation)
# Or manually: Run Ollama app
```

Ollama will start on `http://localhost:11434`

#### 4. Configure Application

```bash
# Edit .env
DEFAULT_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

#### 5. Verify Setup

```bash
# Test Ollama is running
curl http://localhost:11434/api/tags

# Then test config
python -c "from config import Config; c = Config(); print('Ollama ready!')"
```

### Model Options

```bash
# Lightweight (fast)
ollama pull mistral

# Balanced (recommended)
ollama pull llama2
ollama pull neural-chat

# Large (slow, requires 20+ GB RAM)
ollama pull llama2-uncensored
```

Full list: https://ollama.ai/library

### Performance Tips

- **Model Size**: Smaller models are faster (Mistral ~4GB, Llama2 ~7GB)
- **GPU Acceleration**: Significantly faster with NVIDIA/AMD GPU
- **RAM**: 8GB+ recommended
- **First Run**: Model download takes time, subsequent runs are cached

### Troubleshooting

**"Connection refused on localhost:11434"**
- Ensure Ollama is running: `ollama serve`
- On macOS: Check menu bar for Ollama
- Check firewall isn't blocking port 11434

**"Model not found"**
- Pull model first: `ollama pull mistral`
- Verify model directory: `~/.ollama/models`

**"Out of memory"**
- Ollama using too much RAM
- Reduce context window: Less chat history
- Switch to smaller model: `ollama pull mistral`

**"Slow responses"**
- Running on CPU? GPU much faster
- Reduce max tokens in responses
- Use smaller model

---

## Switching Providers

To switch between providers, edit `.env`:

```bash
# Current: OpenAI
DEFAULT_PROVIDER=openai

# Switch to HuggingFace
DEFAULT_PROVIDER=huggingface

# Switch to Ollama
DEFAULT_PROVIDER=ollama
```

No code changes needed! The `config.py` module handles initialization.

---

## Multi-Provider Testing

Test all providers in `.env`:

```env
# OpenAI
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-3.5-turbo

# HuggingFace
HUGGINGFACE_API_KEY=hf_your-token
HUGGINGFACE_REPO_ID=mistralai/Mistral-7B-Instruct-v0.1

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Choose which one to use
DEFAULT_PROVIDER=openai  # Change to test others
```

---

## Performance Comparison

| Metric | OpenAI | HuggingFace | Ollama |
|--------|--------|-------------|--------|
| Speed | Fast | Slow | Very Slow |
| Cost | $$ | $ | Free |
| Quality | Excellent | Good | Good |
| Privacy | ✗ | ✗ | ✓ |
| Offline | ✗ | ✗ | ✓ |
| Setup | 2 min | 5 min | 10 min |

---

## Cost Estimation

### OpenAI (Default Model: gpt-3.5-turbo)
```
Typical conversation:
- User query: 50 tokens × $0.0005 = $0.000025
- Response: 200 tokens × $0.0015 = $0.0003
- Per conversation: ~$0.0003
- 100 conversations/month: ~$0.03
```

### HuggingFace
```
Free: 50,000 requests/month
Paid: Starting at $4/month
```

### Ollama
```
$0.00 — runs locally
Only cost: Electricity & your time
```

---

## Recommended Setup for Different Use Cases

### 👨‍💻 Development
```env
DEFAULT_PROVIDER=ollama
OLLAMA_MODEL=mistral
```
Free, fast iteration, offline by default.

### 🏭 Production
```env
DEFAULT_PROVIDER=openai
OPENAI_MODEL=gpt-4-turbo-preview
```
Most reliable, best quality.

### 💰 Cost-Conscious
```env
DEFAULT_PROVIDER=openai
OPENAI_MODEL=gpt-3.5-turbo
```
Good balance of quality and cost.

### 🔐 Privacy-Focused
```env
DEFAULT_PROVIDER=ollama
OLLAMA_MODEL=llama2
```
All data stays local.

---

For help, see [CONTRIBUTING.md](../CONTRIBUTING.md) or open an [Issue](https://github.com/YOUR_ORG/chat_with_pdf/issues).
