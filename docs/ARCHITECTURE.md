# Project Architecture

## Overview

**Chat with PDF** is a Streamlit-based application that enables users to upload PDF documents and ask natural language questions about their content using large language models (LLMs).

```
┌─────────────────────────────────────────────────────────┐
│                  Streamlit Frontend                       │
│  (Web UI, File Upload, Chat Interface)                   │
└───────────────┬─────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────┐
│              Application Layer (app_enhanced.py)         │
│  • Session state management                             │
│  • Chat history handling                                │
│  • PDF upload validation                                │
└───────────────┬─────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────┐
│              Configuration & LLM Setup (config.py)       │
│  • Provider initialization (OpenAI, HuggingFace, Ollama)│
│  • API key management                                   │
│  • Model instantiation                                  │
└───────────────┬─────────────────────────────────────────┘
                │
        ┌───────┴────────┬──────────────┐
        │                │              │
    ┌───▼──┐         ┌──▼───┐      ┌──▼────┐
    │ LLM  │         │ Text │      │Vector │
    │      │         │Proc. │      │Search │
    └──────┘         └──────┘      └───────┘
```

## Components

### 1. **app_enhanced.py** (Main Application)
The primary Streamlit application entry point.

**Responsibilities:**
- Initialize Streamlit UI components
- Manage session state (chat history, uploaded files)
- Handle PDF file uploads and validation
- Orchestrate document processing pipeline
- Render chat interface and responses

**Key Sections:**
```python
# Session initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# File upload handling
uploaded_file = st.file_uploader("Upload PDF")

# Chat interaction
user_query = st.chat_input("Ask a question...")
```

### 2. **config.py** (Configuration & LLM Setup)
Handles LLM provider initialization and configuration.

**Responsibilities:**
- Load and validate environment variables
- Initialize LLM clients (OpenAI, HuggingFace, Ollama)
- Provide unified interface for different providers
- Error handling and validation

**Key Classes:**
```python
class Config:
    """Initialize appropriate LLM provider based on config."""
    - get_llm()  # Return configured LLM instance
    - get_embeddings()  # Return embedding model
```

### 3. **LangChain Integration**
Document processing and semantic search pipeline.

**Key Components:**
- **PyPDFLoader**: Extract text from PDFs
- **RecursiveCharacterTextSplitter**: Split documents into chunks
- **FAISS**: Vector database for semantic search
- **Embeddings**: Convert text to vectors (HuggingFace embeddings)
- **RetrievalQA**: Chain for Q&A over documents

**Data Flow:**
```
PDF File
   ↓
[PyPDFLoader] → Raw Text
   ↓
[TextSplitter] → Chunks
   ↓
[Embeddings] → Vectors
   ↓
[FAISS] → Vector DB
   ↓
[RetrievalQA + LLM] → Answer
```

### 4. **Vector Database (FAISS)**
Facebook's AI Similarity Search for fast semantic retrieval.

**Purpose:**
- Store embeddings of document chunks
- Perform similarity search given user query
- Retrieve most relevant chunks for LLM context

**Process:**
1. User asks question
2. Question is embedded
3. FAISS finds k most similar chunks
4. Chunks sent to LLM as context

## Data Flow

### Document Upload & Processing

```
1. User uploads PDF
   └─ Validation (format, size)
   
2. PDF Text Extraction
   └─ PyPDFLoader reads PDF
   └─ Raw text extracted
   
3. Text Chunking
   └─ Split into overlapping chunks
   └─ Default: 1000 chars, 100 char overlap
   
4. Embedding & Indexing
   └─ Each chunk embedded with HuggingFace
   └─ Embeddings stored in FAISS
   └─ Index saved to session state
```

### Query Processing

```
1. User asks question
   └─ Question text received
   
2. Semantic Search
   └─ Question embedded
   └─ FAISS similarity search (top-k chunks)
   
3. Context Preparation
   └─ Relevant chunks formatted as context
   
4. LLM Generation
   └─ LLM generates answer using context
   └─ Maintains chat history
   
5. Response Display
   └─ Answer rendered in Streamlit
   └─ Interaction saved to history
```

## Supported LLM Providers

### OpenAI
- **Models**: gpt-3.5-turbo, gpt-4, gpt-4-turbo
- **Setup**: API key from https://platform.openai.com
- **Cost**: Pay-as-you-go token-based pricing

### HuggingFace
- **Models**: Any HF-hosted model (Mistral, Llama, etc.)
- **Setup**: API token from https://huggingface.co
- **Cost**: Free with rate limits, paid for higher usage

### Ollama (Local)
- **Models**: Llama2, Mistral, Neural Chat (run locally)
- **Setup**: Self-hosted via https://ollama.ai
- **Cost**: Free (requires local GPU/CPU)

## Session Management

Streamlit's `session_state` manages state across reruns:

```python
st.session_state = {
    'chat_history': [],      # List of messages
    'pdf_content': "",       # Raw PDF text
    'embeddings_index': {},  # FAISS vector DB
    'file_uploaded': False   # Upload status
}
```

**Why Needed:**
- PDFs are re-uploaded on every rerun without session state
- Chat history would be lost with every interaction
- Embeddings would be re-computed unnecessarily

## Configuration & Environment

### Environment Variables
```env
OPENAI_API_KEY=sk-...
DEFAULT_PROVIDER=openai
OPENAI_MODEL=gpt-3.5-turbo
```

### Multi-Provider Configuration
The `config.py` module allows runtime provider selection:

```python
config = Config()  # Auto-detects provider from env
llm = config.get_llm()  # Get initialized LLM instance
```

## Error Handling

### File Upload Errors
- Empty files rejected
- Unsupported formats rejected
- File size validation (max 20MB by default)

### API Errors
- Missing API keys caught at startup
- Rate limiting handled gracefully
- Network errors logged and reported

### Processing Errors
- PDF parsing failures handled
- Empty document detection
- Embedding failures managed

## Performance Considerations

### Optimization Strategies
1. **Chunk Overlap**: Maintains context continuity (default: 100 chars)
2. **Vector Caching**: FAISS index cached in session state
3. **Lazy Loading**: Embeddings computed only when needed
4. **Batch Processing**: Multiple documents processed sequentially

### Scalability Limits
- Single session limitation: ~100MB text max
- Recommendation: Split large documents
- Alternative: Use advanced.py for analytics

## Testing Strategy

### Unit Tests (tests/test_config.py)
- Config initialization with different providers
- Environment variable validation
- Error handling for missing keys

### Integration Tests (future)
- End-to-end PDF processing
- LLM query and response
- Session state management

### Test Fixtures (tests/conftest.py)
- Mock LLM clients
- Sample text and chunks
- FAISS index mocks

## Dependencies

### Core
- **streamlit**: Web framework
- **langchain**: LLM and document processing
- **openai**: OpenAI API client
- **faiss-cpu**: Vector search library
- **PyPDF2/pdfplumber**: PDF parsing

### Development
- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Linting
- **pre-commit**: Git hooks

See [requirements.txt](../requirements.txt) and [requirements-dev.txt](../requirements-dev.txt) for versions.

## Security Considerations

1. **API Keys**: Never hardcoded, loaded from environment only
2. **Input Validation**: All user inputs validated
3. **File Uploads**: Restricted to PDF format, size capped
4. **.env File**: Added to .gitignore, never committed
5. **Docker Secrets**: Loaded via environment variables

## Future Enhancements

- [ ] Database persistence (save chat history)
- [ ] User authentication
- [ ] Rate limiting per user
- [ ] Advanced analytics (tokens used, response times)
- [ ] Streaming responses
- [ ] Document metadata extraction
- [ ] Support for other document formats (DOCX, TXT, etc.)
- [ ] Fine-tuning on domain-specific data

---

For questions, see [CONTRIBUTING.md](../CONTRIBUTING.md) or open an [Issue](https://github.com/YOUR_ORG/chat_with_pdf/issues).
