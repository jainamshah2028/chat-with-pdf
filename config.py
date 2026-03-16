# config.py - Configuration file for Enhanced PDF Chat App

import os
from pathlib import Path

class AppConfig:
    """Application configuration settings"""
    
    # File settings
    SUPPORTED_FORMATS = ["pdf", "txt", "docx"]
    MAX_FILE_SIZE_MB = 200
    MAX_FILES_PER_UPLOAD = 10
    
    # Processing settings
    DEFAULT_CHUNK_SIZE = 1000
    DEFAULT_CHUNK_OVERLAP = 150
    MAX_RESULTS_PER_QUERY = 5
    
    # Storage settings
    DATA_DIR = Path("data")
    CHAT_HISTORY_FILE = DATA_DIR / "chat_history.json"
    PROCESSED_DOCS_DIR = DATA_DIR / "processed_docs"
    
    # UI settings
    PAGE_TITLE = "Advanced PDF Chat Assistant"
    PAGE_ICON = "📚"
    LAYOUT = "wide"
    
    # AI Provider settings
    OPENAI_MODELS = {
        "GPT-3.5 Turbo": "gpt-3.5-turbo",
        "GPT-4": "gpt-4",
        "GPT-4 Turbo": "gpt-4-turbo-preview"
    }
    
    OLLAMA_MODELS = {
        "Llama 2": "llama2",
        "Mistral": "mistral", 
        "CodeLlama": "codellama",
        "Phi": "phi"
    }
    
    HUGGINGFACE_EMBEDDING_MODELS = {
        "All MiniLM L6 v2 (Fast)": "sentence-transformers/all-MiniLM-L6-v2",
        "All mpnet base v2 (Accurate)": "sentence-transformers/all-mpnet-base-v2",
        "Multi-QA MiniLM": "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
    }
    
    # Security settings
    HIDE_API_KEYS = True
    AUTO_SAVE_CHAT = True
    
    # Performance settings
    ENABLE_CACHING = True
    CACHE_TTL_HOURS = 24
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.PROCESSED_DOCS_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def get_openai_key(cls):
        """Get OpenAI API key from environment or return None"""
        return os.getenv("OPENAI_API_KEY")
    
    @classmethod
    def set_openai_key(cls, api_key):
        """Set OpenAI API key in environment"""
        os.environ["OPENAI_API_KEY"] = api_key

# Theme configurations
class Themes:
    """UI theme configurations"""
    
    DEFAULT = {
        "primary_color": "#667eea",
        "background_color": "#ffffff",
        "secondary_background_color": "#f0f2f6",
        "text_color": "#262730"
    }
    
    DARK = {
        "primary_color": "#764ba2",
        "background_color": "#0e1117",
        "secondary_background_color": "#262730",
        "text_color": "#fafafa"
    }
    
    BLUE = {
        "primary_color": "#1f77b4",
        "background_color": "#ffffff",
        "secondary_background_color": "#e8f4fd",
        "text_color": "#262730"
    }

# Custom CSS styles
CUSTOM_CSS = """
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.main-header h1 {
    color: white;
    margin: 0;
    text-align: center;
    font-size: 2.5rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.feature-box {
    background: linear-gradient(135deg, #f0f2f6 0%, #e8f4fd 100%);
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    border-left: 5px solid #667eea;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-message {
    background: linear-gradient(135deg, #e8f4fd 0%, #f0f8ff 100%);
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    border-left: 5px solid #1f77b4;
    box-shadow: 0 2px 8px rgba(31, 119, 180, 0.1);
}

.status-success {
    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    color: #155724;
    padding: 0.75rem;
    border-radius: 8px;
    border-left: 4px solid #28a745;
}

.status-error {
    background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
    color: #721c24;
    padding: 0.75rem;
    border-radius: 8px;
    border-left: 4px solid #dc3545;
}

.status-warning {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    color: #856404;
    padding: 0.75rem;
    border-radius: 8px;
    border-left: 4px solid #ffc107;
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-top: 3px solid #667eea;
}

.sidebar-section {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    border-left: 3px solid #667eea;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.5s ease-in;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-header h1 {
        font-size: 1.8rem;
    }
    
    .feature-box, .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
    }
}
</style>
"""

# Alias for backward compatibility
Config = AppConfig
