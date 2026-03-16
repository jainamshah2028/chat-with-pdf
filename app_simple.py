# Simple PDF Chat App - Robust Local Processing
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import pdfplumber
import tempfile
import time
import re
from datetime import datetime
from collections import Counter
import os

st.set_page_config(
    page_title="PDF Chat Assistant",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
}
.status-success { background-color: #d4edda; color: #155724; padding: 1rem; border-radius: 5px; }
.status-error { background-color: #f8d7da; color: #721c24; padding: 1rem; border-radius: 5px; }
.user-message { background-color: #e7f3ff; padding: 1rem; margin: 1rem 0; border-radius: 5px; }
.bot-message { background-color: #f0f8ff; padding: 1rem; margin: 1rem 0; border-radius: 5px; border-left: 4px solid #667eea; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'processed_docs' not in st.session_state:
    st.session_state.processed_docs = None
if 'analytics' not in st.session_state:
    st.session_state.analytics = None

# Header
st.markdown("""
<div class="main-header">
    <h1>📚 Simple PDF Chat Assistant</h1>
    <p>Local-only processing. No API calls. Pure Python search.</p>
</div>
""", unsafe_allow_html=True)

def load_pdf(file_path):
    """Load PDF with fallback methods"""
    documents = []
    
    # Method 1: PyPDFLoader
    try:
        with st.spinner("📖 Loading PDF with PyPDFLoader..."):
            loader = PyPDFLoader(file_path)
            documents = loader.load_and_split()
            st.success("✅ PDF loaded successfully!")
            return documents
    except Exception as e:
        st.warning(f"PyPDFLoader failed: {e}")
    
    # Method 2: pdfplumber
    try:
        with st.spinner("🔄 Trying pdfplumber..."):
            with pdfplumber.open(file_path) as pdf:
                text_content = ""
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_content += f"\n--- Page {page_num + 1} ---\n{page_text}"
                
                if text_content.strip():
                    doc = Document(page_content=text_content, metadata={"source": file_path})
                    st.success("✅ PDF loaded with pdfplumber!")
                    return [doc]
    except Exception as e:
        st.error(f"pdfplumber failed: {e}")
    
    return None

def get_analytics(docs):
    """Generate document analytics"""
    if not docs:
        return {}
    
    full_text = " ".join([doc.page_content for doc in docs])
    
    word_count = len(full_text.split())
    char_count = len(full_text)
    sentence_count = len(re.findall(r'[.!?]+', full_text))
    
    words = re.findall(r'\b\w+\b', full_text.lower())
    word_freq = Counter(words)
    
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
    filtered = {w: c for w, c in word_freq.items() if w not in stop_words and len(w) > 2}
    
    return {
        'word_count': word_count,
        'char_count': char_count,
        'sentence_count': sentence_count,
        'top_words': dict(sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:10])
    }

def search_documents(docs, question, search_type="keyword"):
    """Search documents with different algorithms"""
    question_lower = question.lower()
    question_words = set(w.strip('.,!?;:') for w in question_lower.split() if len(w.strip('.,!?;:')) > 2)
    
    results = []
    
    for doc in docs:
        content_lower = doc.page_content.lower()
        
        if search_type == "keyword":
            # Count matching keywords
            matches = sum(1 for w in question_words if w in content_lower)
            if matches > 0:
                score = matches
                results.append((doc.page_content, score))
        
        elif search_type == "sentence":
            # Find sentences with matching words
            sentences = re.split(r'[.!?]+', doc.page_content)
            for sentence in sentences:
                sent_lower = sentence.lower()
                matches = sum(1 for w in question_words if w in sent_lower)
                if matches > 0:
                    results.append((sentence.strip(), matches))
    
    if not results:
        return "❌ No relevant information found. Try different keywords."
    
    # Sort by relevance
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Return top match
    answer = results[0][0][:500]
    confidence = min(100, (results[0][1] / len(question_words)) * 100) if question_words else 0
    
    return f"🎯 **Answer** (Confidence: {confidence:.0f}%)\n\n{answer}"

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    search_type = st.radio("Search Type:", ["keyword", "sentence"])
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📂 Document Upload")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        file_size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)
        st.info(f"📄 {uploaded_file.name} ({file_size_mb:.1f} MB)")
        
        if st.button("🚀 Process Document", type="primary", use_container_width=True):
            if file_size_mb > 50:
                st.error("❌ File too large (max 50MB)")
            else:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(uploaded_file.getbuffer())
                        file_path = tmp.name
                    
                    docs = load_pdf(file_path)
                    
                    if docs:
                        # Split into chunks
                        splitter = RecursiveCharacterTextSplitter(
                            chunk_size=1000,
                            chunk_overlap=150
                        )
                        st.session_state.processed_docs = splitter.split_documents(docs)
                        st.session_state.analytics = get_analytics(st.session_state.processed_docs)
                        
                        st.success(f"✅ Processed {len(st.session_state.processed_docs)} chunks!")
                    else:
                        st.error("❌ Failed to load PDF")
                    
                    os.unlink(file_path)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Chat interface
    if st.session_state.processed_docs:
        st.markdown("### 💬 Ask Questions")
        
        question = st.text_input(
            "Your question:",
            placeholder="What is this document about?"
        )
        
        if question:
            answer = search_documents(st.session_state.processed_docs, question, search_type)
            
            st.session_state.chat_history.append({
                'question': question,
                'answer': answer,
                'time': datetime.now().strftime('%H:%M:%S')
            })
            
            st.markdown(f'<div class="user-message"><b>Q:</b> {question}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="bot-message"><b>A:</b> {answer}</div>', unsafe_allow_html=True)

# Sidebar analytics
with col2:
    if st.session_state.analytics:
        st.markdown("### 📊 Document Stats")
        analytics = st.session_state.analytics
        
        st.metric("Words", f"{analytics['word_count']:,}")
        st.metric("Sentences", f"{analytics['sentence_count']:,}")
        
        if analytics['top_words']:
            st.markdown("**Top Words:**")
            for word, count in list(analytics['top_words'].items())[:5]:
                st.write(f"- {word.title()}: {count}")

# Chat history
if st.session_state.chat_history:
    st.markdown("### 📜 Chat History")
    for i, chat in enumerate(st.session_state.chat_history[-5:]):
        with st.expander(f"{chat['question'][:50]}... ({chat['time']})"):
            st.write(f"**Q:** {chat['question']}")
            st.write(f"**A:** {chat['answer']}")
