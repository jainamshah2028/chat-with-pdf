
# 📄 Chat with PDF

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Tests](https://github.com/YOUR_ORG/chat_with_pdf/workflows/Tests/badge.svg)](https://github.com/YOUR_ORG/chat_with_pdf/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An intelligent PDF chat application powered by state-of-the-art LLMs and semantic search. Upload any PDF and ask natural language questions about its content!

> **🎯 Getting Started?** Start with the **Simple App** for instant results:
> ```bash
> streamlit run app_simple.py  # No API keys needed - pure local processing
> ```
> Or use the **Advanced App** with AI features:
> ```bash
> streamlit run app_advanced.py  # Requires HuggingFace/OpenAI setup
> ```

## ✨ Features

- 📤 **Multi-file Upload** — Process multiple PDFs simultaneously
- 🤖 **Multi-Provider LLM Support** — Choose between OpenAI, HuggingFace, or local Ollama
- 💬 **Chat History** — Persistent conversation history within a session
- 🔍 **Semantic Search** — Uses FAISS vector database for accurate contextual retrieval
- 🎯 **Relevance Scoring** — Display confidence scores with retrieved chunks
- ⚡ **Fast Processing** — Efficient PDF parsing and chunking
- 🛡️ **Secure** — API keys loaded from environment variables (never committed)
- 🐳 **Docker Ready** — Deploy with a single command

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (get it [here](https://platform.openai.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_ORG/chat_with_pdf.git
   cd chat_with_pdf
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. **Run the app**
   ```bash
   streamlit run app_enhanced.py
   ```

The app will open at `http://localhost:8501`

## 📚 Documentation

- **[SETUP.md](SETUP.md)** — Detailed setup and configuration guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — Contributing guidelines and development workflow
- **[docs/API_PROVIDERS.md](docs/API_PROVIDERS.md)** — LLM provider-specific setup
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — Project structure and design
- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** — Deployment guides (Streamlit Cloud, Docker)

## 🎯 Available Versions

| Version | Features | Dependencies | Best For |
|---------|----------|-------------|----------|
| **app_simple.py** ✨ NEW | Local search, no API calls | PyPDF, pdfplumber | **Start here - no setup needed** |
| **app_enhanced.py** ⭐ | Chat history, 3 providers, modern UI | OpenAI/HuggingFace | Production with AI features |
| app_advanced.py | Analytics, search algorithms, dashboard | All of above + plotly | Advanced analysis |
| app.py | Single file, basic functionality | OpenAI only | Simple projects |

### Quick Start Recommendations:

1. **No APIs/Setup?** → `streamlit run app_simple.py`
2. **Want AI Answers?** → `streamlit run app_enhanced.py` 
3. **Need Analytics?** → `streamlit run app_advanced.py`

## 🔑 Environment Configuration

Create a `.env` file (see `.env.example` for template):

```env
# Required: Choose your LLM provider
OPENAI_API_KEY=sk-your-key-here
DEFAULT_PROVIDER=openai

# Optional: Multi-provider setup
HUGGINGFACE_API_KEY=hf_your-token
OLLAMA_BASE_URL=http://localhost:11434
```

See [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md) for all available options.

## 🐳 Docker Deployment

**Build and run with Docker:**

```bash
docker build -t chat-pdf .
docker run -p 8501:8501 --env-file .env chat-pdf
```

**Or use Docker Compose:**

```bash
docker-compose up
```

Visit `http://localhost:8501`

## ☁️ Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets in Streamlit Cloud dashboard: Settings → Secrets → Paste your API keys
5. Deploy!

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## 🧪 Development & Testing

### Install development dependencies
```bash
pip install -r requirements-dev.txt
pre-commit install
```

### Run tests
```bash
pytest tests/ -v --cov=.
```

### Format and lint code
```bash
black .
flake8 .
isort .
```

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for comprehensive testing documentation.

## 🏗️ Project Structure

```
chat_with_pdf/
├── app_enhanced.py              # Main application (primary)
├── config.py                    # LLM provider configuration
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── tests/                       # Test suite
├── docs/                        # Documentation
├── examples/                    # Reference implementations
├── .github/workflows/           # CI/CD pipelines
├── Dockerfile                   # Container image definition
├── docker-compose.yml          # Local dev container setup
└── .env.example                # Environment variables template
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Development setup
- Pull request process
- Testing requirements

## 📝 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io) — UI framework
- [LangChain](https://langchain.com) — LLM framework
- [FAISS](https://github.com/facebookresearch/faiss) — Vector search
- [OpenAI](https://openai.com) — LLM provider
- And the amazing open-source community!

## 📧 Support

- 💬 Start a [Discussion](https://github.com/YOUR_ORG/chat_with_pdf/discussions) for questions
- 🐛 Report bugs via [Issues](https://github.com/YOUR_ORG/chat_with_pdf/issues)
- 📚 Check [Discussions](https://github.com/YOUR_ORG/chat_with_pdf/discussions) for common questions

---

**⭐ If you find this helpful, please consider starring the repository!**
