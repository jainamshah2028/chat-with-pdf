# Enhanced PDF Chat App with Modern Features
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
import pdfplumber
import tempfile
import requests
import json
import datetime
from pathlib import Path
import zipfile
import io

# Enhanced Configuration
class Config:
    DEFAULT_OPENAI_KEY = "your-key-here"
    SUPPORTED_FORMATS = ["pdf", "txt", "docx"]
    MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
    CHAT_HISTORY_FILE = "chat_history.json"

# Initialize session state
def init_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'processed_docs' not in st.session_state:
        st.session_state.processed_docs = []
    if 'current_files' not in st.session_state:
        st.session_state.current_files = []
    if 'qa_system' not in st.session_state:
        st.session_state.qa_system = None

def check_ollama_availability():
    """Check if Ollama is running locally"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def setup_llm_and_embeddings(provider_choice, api_key=None, model_name="gpt-3.5-turbo"):
    """Enhanced setup with more providers"""
    if provider_choice == "OpenAI":
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        else:
            os.environ["OPENAI_API_KEY"] = Config.DEFAULT_OPENAI_KEY
        
        try:
            embeddings = OpenAIEmbeddings()
            llm = ChatOpenAI(temperature=0, model=model_name)
            return llm, embeddings, True
        except Exception as e:
            st.error(f"OpenAI setup failed: {str(e)}")
            return None, None, False
    
    elif provider_choice == "Ollama (Local & Free)":
        if not check_ollama_availability():
            st.error("❌ Ollama is not running. Please install and start Ollama first.")
            st.info("📝 Install from: https://ollama.ai")
            return None, None, False
        
        try:
            from langchain_community.llms import Ollama
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            llm = Ollama(model="llama2")  # or "mistral", "codellama"
            return llm, embeddings, True
        except Exception as e:
            st.error(f"Ollama setup failed: {str(e)}")
            return None, None, False
    
    elif provider_choice == "Free (HuggingFace Only)":
        try:
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            return "simple", embeddings, True
        except Exception as e:
            st.error(f"Free setup failed: {str(e)}")
            return None, None, False

def load_multiple_files(uploaded_files):
    """Load multiple PDF files"""
    all_documents = []
    processing_status = []
    
    for uploaded_file in uploaded_files:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                file_path = tmp_file.name
            
            # Try PyPDFLoader first
            try:
                loader = PyPDFLoader(file_path)
                documents = loader.load_and_split()
                # Add file info to metadata
                for doc in documents:
                    doc.metadata['source_file'] = uploaded_file.name
                all_documents.extend(documents)
                processing_status.append(f"✅ {uploaded_file.name}")
            except Exception as e:
                # Fallback to pdfplumber
                try:
                    with pdfplumber.open(file_path) as pdf:
                        text_content = ""
                        for page_num, page in enumerate(pdf.pages):
                            page_text = page.extract_text()
                            if page_text:
                                text_content += f"\n--- Page {page_num + 1} ---\n"
                                text_content += page_text
                        
                        if text_content.strip():
                            doc = Document(
                                page_content=text_content, 
                                metadata={"source": file_path, "source_file": uploaded_file.name}
                            )
                            all_documents.append(doc)
                            processing_status.append(f"✅ {uploaded_file.name} (fallback)")
                        else:
                            processing_status.append(f"❌ {uploaded_file.name} - No text found")
                except Exception as e2:
                    processing_status.append(f"❌ {uploaded_file.name} - {str(e2)}")
            
            # Cleanup
            try:
                os.unlink(file_path)
            except:
                pass
                
        except Exception as e:
            processing_status.append(f"❌ {uploaded_file.name} - {str(e)}")
    
    return all_documents, processing_status

def enhanced_qa(docs, question, max_results=3):
    """Enhanced QA with better relevance scoring"""
    question_lower = question.lower()
    question_words = [word.strip('.,!?;:()[]{}') for word in question_lower.split() if len(word.strip('.,!?;:()[]{}')) > 2]
    
    chunk_scores = []
    
    for i, doc in enumerate(docs):
        content_lower = doc.page_content.lower()
        
        # Scoring algorithm
        exact_matches = sum(1 for word in question_words if word in content_lower)
        partial_matches = sum(1 for word in question_words 
                            if any(word[:4] in content_word for content_word in content_lower.split() if len(content_word) > 4))
        
        # Bonus for having words close together
        proximity_bonus = 0
        for word in question_words:
            if word in content_lower:
                word_positions = [j for j, w in enumerate(content_lower.split()) if word in w]
                if len(word_positions) > 1:
                    proximity_bonus += 1
        
        total_score = exact_matches * 3 + partial_matches * 1 + proximity_bonus * 0.5
        
        if total_score > 0:
            chunk_scores.append((i, total_score, doc))
    
    if not chunk_scores:
        return "I couldn't find relevant information for your question in the uploaded documents."
    
    # Sort by score and get top results
    chunk_scores.sort(key=lambda x: x[1], reverse=True)
    top_chunks = chunk_scores[:max_results]
    
    # Build comprehensive answer
    answer_parts = []
    for i, (chunk_idx, score, doc) in enumerate(top_chunks):
        source_file = doc.metadata.get('source_file', 'Unknown file')
        
        # Find most relevant paragraph
        paragraphs = [p.strip() for p in doc.page_content.split('\n') if p.strip() and len(p.strip()) > 50]
        best_paragraph = ""
        best_para_score = 0
        
        for paragraph in paragraphs:
            para_lower = paragraph.lower()
            para_score = sum(1 for word in question_words if word in para_lower)
            if para_score > best_para_score:
                best_para_score = para_score
                best_paragraph = paragraph
        
        if best_paragraph:
            answer_parts.append(f"**From {source_file}:**\n{best_paragraph}\n")
        elif doc.page_content.strip():
            # Fallback to first 400 chars
            content_preview = doc.page_content[:400] + "..." if len(doc.page_content) > 400 else doc.page_content
            answer_parts.append(f"**From {source_file}:**\n{content_preview}\n")
    
    return "\n".join(answer_parts) if answer_parts else "No relevant content found."

def save_chat_history():
    """Save chat history to file"""
    try:
        with open(Config.CHAT_HISTORY_FILE, 'w') as f:
            json.dump(st.session_state.chat_history, f, indent=2, default=str)
        return True
    except Exception as e:
        st.error(f"Failed to save chat history: {e}")
        return False

def load_chat_history():
    """Load chat history from file"""
    try:
        if os.path.exists(Config.CHAT_HISTORY_FILE):
            with open(Config.CHAT_HISTORY_FILE, 'r') as f:
                st.session_state.chat_history = json.load(f)
        return True
    except Exception as e:
        st.error(f"Failed to load chat history: {e}")
        return False

def export_chat_to_markdown():
    """Export chat history to markdown"""
    if not st.session_state.chat_history:
        return None
    
    markdown_content = f"# PDF Chat History\n\n*Exported on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    
    for i, chat in enumerate(st.session_state.chat_history, 1):
        markdown_content += f"## Chat {i}\n\n"
        markdown_content += f"**Question:** {chat['question']}\n\n"
        markdown_content += f"**Answer:** {chat['answer']}\n\n"
        markdown_content += f"*Timestamp: {chat['timestamp']}*\n\n---\n\n"
    
    return markdown_content

# Main App
def main():
    # Enhanced page config
    st.set_page_config(
        page_title="Advanced PDF Chat", 
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="📚"
    )
    
    # Initialize session state
    init_session_state()
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        text-align: center;
    }
    .feature-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .chat-message {
        background: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<div class="main-header"><h1>🚀 Advanced PDF Chat Assistant</h1></div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        # Provider selection with more options
        provider_options = [
            "Free (HuggingFace Only)",
            "Ollama (Local & Free)",
            "OpenAI GPT-3.5",
            "OpenAI GPT-4"
        ]
        provider_choice = st.selectbox("🤖 Choose AI Provider:", provider_options)
        
        # Model selection for OpenAI
        model_name = "gpt-3.5-turbo"
        if "GPT-4" in provider_choice:
            model_name = "gpt-4"
            st.warning("💰 GPT-4 costs more than GPT-3.5")
        
        # API Key input
        api_key = None
        if "OpenAI" in provider_choice:
            api_key = st.text_input("🔑 OpenAI API Key:", type="password", 
                                   help="Enter your OpenAI API key")
        
        # Advanced settings
        st.subheader("🔧 Advanced Settings")
        chunk_size = st.slider("📄 Text Chunk Size", 500, 2000, 1000)
        chunk_overlap = st.slider("🔄 Chunk Overlap", 50, 300, 150)
        max_results = st.slider("📊 Max Results per Query", 1, 5, 3)
        
        # Chat history management
        st.subheader("💬 Chat History")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save History"):
                if save_chat_history():
                    st.success("Saved!")
        with col2:
            if st.button("📂 Load History"):
                if load_chat_history():
                    st.success("Loaded!")
        
        if st.button("🗑️ Clear History"):
            st.session_state.chat_history = []
            st.success("Cleared!")
        
        # Export options
        if st.session_state.chat_history:
            st.subheader("📤 Export")
            if st.button("📝 Export to Markdown"):
                markdown_content = export_chat_to_markdown()
                if markdown_content:
                    st.download_button(
                        label="⬇️ Download Chat History",
                        data=markdown_content,
                        file_name=f"chat_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
    
    # Main content area
    # File upload section
    st.subheader("📁 Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF files", 
        type=["pdf"], 
        accept_multiple_files=True,
        help="You can upload multiple PDF files at once"
    )
    
    # Display current files
    if uploaded_files:
        st.info(f"📚 {len(uploaded_files)} file(s) selected")
        with st.expander("📋 File Details"):
            for file in uploaded_files:
                file_size = len(file.getbuffer()) / 1024 / 1024  # MB
                st.write(f"• **{file.name}** ({file_size:.1f} MB)")
    
    # Process files
    if uploaded_files and st.button("🔄 Process Documents", type="primary"):
        with st.spinner("Processing documents..."):
            # Setup AI provider
            llm, embeddings, setup_success = setup_llm_and_embeddings(provider_choice, api_key, model_name)
            
            if not setup_success:
                st.error("❌ Failed to setup AI provider")
                return
            
            # Load documents
            all_documents, processing_status = load_multiple_files(uploaded_files)
            
            # Display processing results
            st.subheader("📊 Processing Results")
            for status in processing_status:
                if "✅" in status:
                    st.success(status)
                else:
                    st.error(status)
            
            if all_documents:
                # Split documents
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=chunk_size, 
                    chunk_overlap=chunk_overlap
                )
                docs = splitter.split_documents(all_documents)
                
                # Store in session state
                st.session_state.processed_docs = docs
                st.session_state.current_files = [f.name for f in uploaded_files]
                
                # Setup QA system for advanced providers
                if provider_choice != "Free (HuggingFace Only)":
                    try:
                        db = FAISS.from_documents(docs, embeddings)
                        qa = RetrievalQA.from_chain_type(
                            llm=llm, 
                            chain_type="stuff", 
                            retriever=db.as_retriever(search_kwargs={"k": max_results})
                        )
                        st.session_state.qa_system = qa
                    except Exception as e:
                        st.error(f"Failed to setup QA system: {e}")
                        st.session_state.qa_system = None
                
                st.success(f"✅ Successfully processed {len(docs)} text chunks from {len(uploaded_files)} files!")
    
    # Chat interface
    if st.session_state.processed_docs:
        st.subheader("💬 Chat with Your Documents")
        
        # Display current document info
        with st.expander("📖 Current Documents", expanded=False):
            st.write(f"**Files:** {', '.join(st.session_state.current_files)}")
            st.write(f"**Text chunks:** {len(st.session_state.processed_docs)}")
            
            # Preview content
            if st.session_state.processed_docs:
                preview = st.session_state.processed_docs[0].page_content[:200] + "..."
                st.text_area("Content preview:", preview, height=100, disabled=True)
        
        # Chat input
        question = st.text_input("🤔 Ask a question about your documents:", key="question_input")
        
        if question:
            with st.spinner("🔍 Searching for answers..."):
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Get answer based on provider
                if st.session_state.qa_system and provider_choice != "Free (HuggingFace Only)":
                    try:
                        answer = st.session_state.qa_system.run(question)
                    except Exception as e:
                        if "quota" in str(e).lower() or "429" in str(e):
                            st.error("❌ API quota exceeded. Try the free option.")
                            answer = enhanced_qa(st.session_state.processed_docs, question, max_results)
                        else:
                            st.error(f"Error: {str(e)}")
                            answer = "An error occurred while processing your question."
                else:
                    # Use enhanced free QA
                    answer = enhanced_qa(st.session_state.processed_docs, question, max_results)
                
                # Display answer
                st.markdown('<div class="chat-message">', unsafe_allow_html=True)
                st.markdown(f"**🤖 Answer:**\n\n{answer}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Save to chat history
                chat_entry = {
                    "question": question,
                    "answer": answer,
                    "timestamp": timestamp,
                    "files": st.session_state.current_files.copy()
                }
                st.session_state.chat_history.append(chat_entry)
        
        # Display chat history
        if st.session_state.chat_history:
            st.subheader("📜 Chat History")
            
            # Reverse to show latest first
            for i, chat in enumerate(reversed(st.session_state.chat_history[-5:]), 1):
                with st.expander(f"💬 {chat['question'][:50]}... ({chat['timestamp']})"):
                    st.markdown(f"**Question:** {chat['question']}")
                    st.markdown(f"**Answer:** {chat['answer']}")
                    st.caption(f"Files: {', '.join(chat['files'])}")
    
    else:
        # Welcome message
        st.markdown("""
        <div class="feature-box">
        <h3>🎯 Features</h3>
        <ul>
        <li>📚 <strong>Multiple PDF Support:</strong> Upload and chat with multiple PDFs simultaneously</li>
        <li>🤖 <strong>Multiple AI Providers:</strong> Choose from OpenAI, Ollama, or free local processing</li>
        <li>💬 <strong>Chat History:</strong> Save, load, and export your conversation history</li>
        <li>🔍 <strong>Enhanced Search:</strong> Advanced relevance scoring for better answers</li>
        <li>📊 <strong>Detailed Analytics:</strong> See processing status and search details</li>
        <li>🎨 <strong>Modern UI:</strong> Clean, responsive interface with progress indicators</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("👆 Upload PDF files above to get started!")

if __name__ == "__main__":
    main()
