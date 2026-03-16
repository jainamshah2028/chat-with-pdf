# Advanced PDF Chat Assistant with Modern UI and Analytics
import json
import os
import re
import tempfile
import time
from collections import Counter
from datetime import datetime

import pandas as pd
import pdfplumber
import requests
import streamlit as st
import streamlit.components.v1 as components
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Advanced configuration
st.set_page_config(
    page_title="Advanced PDF Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Custom CSS for modern UI
def load_custom_css():
    st.markdown(
        """
    <style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
    }
    
    /* Chat container styling */
    .chat-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    /* Message bubbles */
    .user-message {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px auto;
        max-width: 70%;
        box-shadow: 0 4px 12px rgba(238, 90, 36, 0.3);
        display: block;
        text-align: right;
    }
    
    .bot-message {
        background: linear-gradient(45deg, #74b9ff, #0984e3);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px auto 8px 0;
        max-width: 70%;
        box-shadow: 0 4px 12px rgba(9, 132, 227, 0.3);
        display: block;
    }
    
    /* Analytics cards */
    .analytics-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 5px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    
    .analytics-card:hover {
        transform: translateY(-5px);
    }
    
    .analytics-card h3 {
        font-size: 2rem;
        margin: 0 0 0.5rem 0;
        font-weight: bold;
    }
    
    .analytics-card p {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(45deg, #00b894, #00cec9);
        color: white;
        padding: 12px 20px;
        border-radius: 25px;
        display: inline-block;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 184, 148, 0.3);
        font-weight: bold;
    }
    
    .status-warning {
        background: linear-gradient(45deg, #fdcb6e, #e17055);
        color: white;
        padding: 12px 20px;
        border-radius: 25px;
        display: inline-block;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(253, 203, 110, 0.3);
        font-weight: bold;
    }
    
    .status-error {
        background: linear-gradient(45deg, #e17055, #d63031);
        color: white;
        padding: 12px 20px;
        border-radius: 25px;
        display: inline-block;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(225, 112, 85, 0.3);
        font-weight: bold;
    }
    
    /* Search highlights */
    .highlight {
        background: linear-gradient(45deg, #ffeaa7, #fdcb6e);
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
        color: #2d3436;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Upload area */
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        margin: 1rem 0;
    }
    
    /* Loading animation */
    .loading-animation {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.8rem; }
        .analytics-card { margin: 5px 0; }
        .user-message, .bot-message { max-width: 90%; }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def get_document_analytics(docs):
    """Generate comprehensive document analytics"""
    if not docs:
        return {}

    # Combine all text
    full_text = " ".join([doc.page_content for doc in docs])

    # Basic stats
    word_count = len(full_text.split())
    char_count = len(full_text)
    sentence_count = len(re.findall(r"[.!?]+", full_text))
    paragraph_count = len([p for p in full_text.split("\n\n") if p.strip()])

    # Reading level analysis (simplified)
    avg_sentence_length = word_count / max(sentence_count, 1)
    if avg_sentence_length < 15:
        reading_level = "Easy"
        reading_score = 80
    elif avg_sentence_length < 25:
        reading_level = "Medium"
        reading_score = 60
    else:
        reading_level = "Hard"
        reading_score = 40

    # Word frequency analysis
    words = re.findall(r"\b\w+\b", full_text.lower())
    word_freq = Counter(words)

    # Remove common stop words
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "must",
        "can",
        "cannot",
        "this",
        "that",
        "these",
        "those",
    }
    filtered_freq = {
        word: count for word, count in word_freq.items() if word not in stop_words and len(word) > 2
    }

    return {
        "word_count": word_count,
        "char_count": char_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "reading_level": reading_level,
        "reading_score": reading_score,
        "avg_sentence_length": round(avg_sentence_length, 1),
        "top_words": dict(sorted(filtered_freq.items(), key=lambda x: x[1], reverse=True)[:15]),
        "chunks": len(docs),
    }


def create_analytics_dashboard(analytics):
    """Create an interactive analytics dashboard"""
    if not analytics:
        return

    st.markdown("### 📊 Document Analytics Dashboard")

    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="analytics-card">
            <h3>{analytics['word_count']:,}</h3>
            <p>Total Words</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="analytics-card">
            <h3>{analytics['sentence_count']:,}</h3>
            <p>Sentences</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="analytics-card">
            <h3>{analytics['reading_level']}</h3>
            <p>Reading Level</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
        <div class="analytics-card">
            <h3>{analytics['chunks']}</h3>
            <p>Text Chunks</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Additional metrics
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Document Statistics")
        stats_df = pd.DataFrame(
            {
                "Metric": ["Characters", "Paragraphs", "Avg Sentence Length", "Reading Score"],
                "Value": [
                    f"{analytics['char_count']:,}",
                    f"{analytics['paragraph_count']:,}",
                    f"{analytics['avg_sentence_length']} words",
                    f"{analytics['reading_score']}/100",
                ],
            }
        )
        st.dataframe(stats_df, hide_index=True, use_container_width=True)

    with col2:
        if analytics["top_words"]:
            st.markdown("#### 🔤 Most Frequent Words")
            words_df = pd.DataFrame(
                [
                    {"Word": word.title(), "Count": count}
                    for word, count in list(analytics["top_words"].items())[:8]
                ]
            )
            st.dataframe(words_df, hide_index=True, use_container_width=True)


def advanced_search(docs, question, search_type="semantic"):
    """Advanced search with multiple algorithms"""
    question_lower = question.lower()
    question_words = [
        word.strip(".,!?;:()[]{}")
        for word in question_lower.split()
        if len(word.strip(".,!?;:()[]{}")) > 2
    ]

    if search_type == "semantic":
        return enhanced_qa(docs, question)

    elif search_type == "fuzzy":
        # Fuzzy search implementation
        question_words_set = set(question_words)
        scored_docs = []

        for doc in docs:
            content_words = set(re.findall(r"\b\w+\b", doc.page_content.lower()))
            # Jaccard similarity
            intersection = len(question_words_set.intersection(content_words))
            union = len(question_words_set.union(content_words))
            similarity = intersection / union if union > 0 else 0
            scored_docs.append((doc, similarity))

        scored_docs.sort(key=lambda x: x[1], reverse=True)

        if scored_docs and scored_docs[0][1] > 0.1:
            best_doc = scored_docs[0][0]
            similarity_score = scored_docs[0][1]
            return f"**Fuzzy Search Result** (Similarity: {similarity_score:.2%})\n\n{best_doc.page_content[:600]}..."

        return "No relevant information found with fuzzy search."

    elif search_type == "keyword":
        # Enhanced keyword search with highlighting
        for doc in docs:
            content = doc.page_content.lower()
            matches = sum(1 for word in question_words if word in content)

            if matches >= max(1, len(question_words) // 2):  # At least half the keywords
                highlighted_content = doc.page_content
                for word in question_words:
                    pattern = re.compile(re.escape(word), re.IGNORECASE)
                    highlighted_content = pattern.sub(
                        f'<span class="highlight">{word}</span>', highlighted_content
                    )

                return f"**Keyword Search Results** ({matches}/{len(question_words)} keywords found)\n\n{highlighted_content[:800]}..."

        return "No documents found with the specified keywords."


def enhanced_qa(docs, question):
    """Enhanced QA with better context understanding"""
    question_lower = question.lower()
    question_words = [
        word.strip(".,!?;:") for word in question_lower.split() if len(word.strip(".,!?;:")) > 2
    ]

    relevant_chunks = []
    scores = []

    for doc in docs:
        content = doc.page_content.lower()
        score = 0

        # Basic keyword matching
        for word in question_words:
            word_count = content.count(word)
            score += word_count * 2

        # Proximity scoring - words appearing close together
        for i, word1 in enumerate(question_words):
            for word2 in question_words[i + 1 :]:
                if word1 in content and word2 in content:
                    pos1 = content.find(word1)
                    pos2 = content.find(word2)
                    if abs(pos1 - pos2) < 100:  # Within 100 characters
                        score += 5

        # Question type bonuses
        if question_lower.startswith(("what", "how", "why", "when", "where", "who")):
            question_starters = ["what", "how", "why", "when", "where", "who"]
            for starter in question_starters:
                if question_lower.startswith(starter) and starter in content:
                    score += 3

        if score > 0:
            relevant_chunks.append(doc.page_content)
            scores.append(score)

    if relevant_chunks:
        # Sort by relevance score
        sorted_chunks = sorted(zip(relevant_chunks, scores), key=lambda x: x[1], reverse=True)
        best_chunk = sorted_chunks[0][0]
        confidence = min(100, (sorted_chunks[0][1] / max(scores)) * 100)

        # Extract most relevant sentences
        sentences = re.split(r"[.!?]+", best_chunk)
        relevant_sentences = []

        for sentence in sentences:
            if len(sentence.strip()) < 10:  # Skip very short sentences
                continue
            sentence_lower = sentence.lower()
            sentence_score = sum(1 for word in question_words if word in sentence_lower)
            if sentence_score > 0:
                relevant_sentences.append((sentence.strip(), sentence_score))

        if relevant_sentences:
            # Sort sentences by relevance and take top 3
            relevant_sentences.sort(key=lambda x: x[1], reverse=True)
            best_sentences = [sent[0] for sent in relevant_sentences[:3] if sent[0]]
            answer = " ".join(best_sentences)
            return f"**Answer** (Confidence: {confidence:.0f}%)\n\n{answer}"
        else:
            return f"**Answer** (Confidence: {confidence:.0f}%)\n\n{best_chunk[:600]}..."

    return "I couldn't find specific information about your question in the document. Try rephrasing your question or using different keywords."


def setup_llm_and_embeddings(provider_choice, api_key=None):
    """Enhanced setup with more options"""
    if provider_choice == "OpenAI GPT-4":
        if not api_key:
            st.error("🔑 Please enter your OpenAI API key to use GPT-4")
            return None, None, False

        os.environ["OPENAI_API_KEY"] = api_key
        try:
            embeddings = OpenAIEmbeddings()
            llm = ChatOpenAI(temperature=0, model="gpt-4")
            return llm, embeddings, True
        except Exception as e:
            st.error(f"❌ OpenAI GPT-4 setup failed: {str(e)}")
            return None, None, False

    elif provider_choice == "OpenAI GPT-3.5":
        if not api_key:
            st.error("🔑 Please enter your OpenAI API key to use GPT-3.5")
            return None, None, False

        os.environ["OPENAI_API_KEY"] = api_key
        try:
            embeddings = OpenAIEmbeddings()
            llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
            return llm, embeddings, True
        except Exception as e:
            st.error(f"❌ OpenAI GPT-3.5 setup failed: {str(e)}")
            return None, None, False

    elif provider_choice == "Free (Advanced Local Processing)":
        try:
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            return "advanced", embeddings, True
        except Exception as e:
            st.error(f"❌ Free setup failed: {str(e)}")
            return None, None, False


def load_pdf_with_fallback(file_path):
    """Enhanced PDF loading with progress tracking"""
    documents = []

    with st.spinner("🔍 Analyzing PDF structure..."):
        time.sleep(0.5)  # Brief pause for UI

    # Method 1: Try PyPDFLoader first
    try:
        with st.spinner("📖 Loading with PyPDFLoader..."):
            loader = PyPDFLoader(file_path)
            documents = loader.load_and_split()
            st.markdown(
                '<div class="status-success">✅ PDF loaded successfully with PyPDFLoader!</div>',
                unsafe_allow_html=True,
            )
            return documents
    except Exception as e:
        st.markdown(
            f'<div class="status-warning">⚠️ PyPDFLoader failed: {str(e)}</div>',
            unsafe_allow_html=True,
        )

    # Method 2: Try pdfplumber as fallback
    try:
        with st.spinner("🔄 Trying alternative PDF reader (pdfplumber)..."):
            with pdfplumber.open(file_path) as pdf:
                text_content = ""
                total_pages = len(pdf.pages)

                progress_bar = st.progress(0)
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_content += f"\n--- Page {page_num + 1} ---\n"
                        text_content += page_text
                    progress_bar.progress((page_num + 1) / total_pages)

                if text_content.strip():
                    documents = [
                        Document(
                            page_content=text_content,
                            metadata={"source": file_path, "pages": total_pages},
                        )
                    ]
                    st.markdown(
                        '<div class="status-success">✅ PDF loaded successfully with pdfplumber!</div>',
                        unsafe_allow_html=True,
                    )
                    return documents
                else:
                    raise Exception("No text could be extracted from the PDF")

    except Exception as e:
        st.markdown(
            f'<div class="status-error">❌ All PDF loading methods failed: {str(e)}</div>',
            unsafe_allow_html=True,
        )
        return None


# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processed_docs" not in st.session_state:
    st.session_state.processed_docs = None
if "analytics" not in st.session_state:
    st.session_state.analytics = None
if "processing_time" not in st.session_state:
    st.session_state.processing_time = 0

# Load custom CSS
load_custom_css()

# Main app header
st.markdown(
    """
<div class="main-header">
    <h1>🤖 Advanced PDF Chat Assistant</h1>
    <p>Intelligent document analysis with AI-powered insights and modern interface</p>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    # Provider selection with more options
    provider_options = ["Free (Advanced Local Processing)", "OpenAI GPT-3.5", "OpenAI GPT-4"]
    provider_choice = st.selectbox("🤖 Choose AI Provider:", provider_options)

    # API Key input for OpenAI
    api_key = None
    if "OpenAI" in provider_choice:
        api_key = st.text_input(
            "🔑 OpenAI API Key:", type="password", help="Enter your OpenAI API key"
        )
        if not api_key:
            st.warning("⚠️ Please enter your OpenAI API key to use this provider.")

    # Advanced settings
    with st.expander("🔧 Advanced Settings", expanded=False):
        chunk_size = st.slider(
            "📄 Chunk Size:", 500, 2000, 1000, 50, help="Size of text chunks for processing"
        )

        chunk_overlap = st.slider(
            "🔄 Chunk Overlap:", 50, 300, 150, 25, help="Overlap between text chunks"
        )

        max_results = st.slider(
            "📊 Max Search Results:", 1, 5, 3, help="Maximum number of results to return"
        )

        # Search type selection
        search_type = st.selectbox(
            "🔍 Search Algorithm:",
            ["semantic", "keyword", "fuzzy"],
            help="Choose search algorithm type",
        )

    # Performance metrics
    if st.session_state.processing_time > 0:
        st.markdown("### ⚡ Performance")
        st.metric("Processing Time", f"{st.session_state.processing_time:.2f}s")

        if st.session_state.analytics:
            efficiency = st.session_state.analytics["word_count"] / st.session_state.processing_time
            st.metric("Processing Speed", f"{efficiency:.0f} words/sec")

    # Chat history management
    st.markdown("### 💬 Chat Management")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    with col2:
        if st.session_state.chat_history:
            chat_export = "\n".join(
                [
                    f"**Q:** {item['question']}\n**A:** {item['answer']}\n---"
                    for item in st.session_state.chat_history
                ]
            )
            st.download_button(
                label="📥 Export",
                data=chat_export,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
            )

    # Show chat stats
    if st.session_state.chat_history:
        st.markdown("### 📊 Chat Stats")
        st.metric("Total Questions", len(st.session_state.chat_history))
        avg_question_length = sum(
            len(item["question"].split()) for item in st.session_state.chat_history
        ) / len(st.session_state.chat_history)
        st.metric("Avg Question Length", f"{avg_question_length:.1f} words")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # File upload with enhanced UI
    st.markdown("### 📂 Document Upload")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload a PDF document to start intelligent analysis and chat",
    )

    if uploaded_file is not None:
        # Display file info
        file_size = len(uploaded_file.getbuffer()) / 1024 / 1024  # MB
        st.info(f"📄 **{uploaded_file.name}** ({file_size:.1f} MB)")

        # Process PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            file_path = tmp_file.name

        if st.button("🚀 Process Document", type="primary", use_container_width=True):
            start_time = time.time()

            with st.spinner("🔄 Setting up AI provider..."):
                # Setup AI provider
                llm, embeddings, setup_success = setup_llm_and_embeddings(provider_choice, api_key)

                if not setup_success:
                    st.error("❌ Failed to setup AI provider. Please check your configuration.")
                else:
                    # Load and process PDF
                    pages = load_pdf_with_fallback(file_path)

                    if pages is not None:
                        with st.spinner("✂️ Splitting document into chunks..."):
                            # Split documents
                            splitter = RecursiveCharacterTextSplitter(
                                chunk_size=chunk_size, chunk_overlap=chunk_overlap
                            )
                            docs = splitter.split_documents(pages)
                            st.session_state.processed_docs = docs

                        with st.spinner("📊 Generating analytics..."):
                            # Generate analytics
                            st.session_state.analytics = get_document_analytics(docs)

                            # Record processing time
                            st.session_state.processing_time = time.time() - start_time

                        # Success message with stats
                        st.markdown(
                            f"""
                        <div class="status-success">
                            ✅ Document processed successfully! 
                            {len(docs)} chunks created in {st.session_state.processing_time:.2f}s
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

# Chat interface
if st.session_state.processed_docs:
    st.markdown("### 💬 Intelligent Chat Interface")

    # Question input with enhanced UI
    question = st.text_input(
        "💭 Ask anything about your document:",
        placeholder="What is the main topic of this document?",
        help="Ask questions in natural language - the AI will find relevant information",
    )

    # Quick question suggestions
    if st.session_state.analytics:
        st.markdown("**💡 Suggested questions:**")
        suggestions = [
            "What is this document about?",
            "What are the key points?",
            "Summarize the main findings",
            "What are the conclusions?",
        ]

        cols = st.columns(len(suggestions))
        for i, suggestion in enumerate(suggestions):
            with cols[i]:
                if st.button(suggestion, key=f"suggestion_{i}", use_container_width=True):
                    question = suggestion

    if question:
        with st.spinner("🤔 Analyzing your question..."):
            start_time = time.time()

            # Process question based on provider
            if provider_choice == "Free (Advanced Local Processing)":
                answer = advanced_search(st.session_state.processed_docs, question, search_type)
            else:
                # Use full RAG pipeline for OpenAI
                try:
                    with st.spinner("🔍 Searching through document..."):
                        db = FAISS.from_documents(st.session_state.processed_docs, embeddings)
                        qa = RetrievalQA.from_chain_type(
                            llm=llm,
                            chain_type="stuff",
                            retriever=db.as_retriever(search_kwargs={"k": max_results}),
                        )
                        answer = qa.run(question)
                except Exception as e:
                    if "quota" in str(e).lower() or "429" in str(e):
                        st.markdown(
                            '<div class="status-error">❌ OpenAI quota exceeded. Switching to free mode...</div>',
                            unsafe_allow_html=True,
                        )
                        answer = advanced_search(
                            st.session_state.processed_docs, question, search_type
                        )
                    else:
                        st.error(f"Error: {str(e)}")
                        answer = None

            if answer:
                response_time = time.time() - start_time

                # Add to chat history
                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "answer": answer,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "response_time": response_time,
                        "search_type": search_type,
                        "provider": provider_choice,
                    }
                )

                # Display answer with enhanced formatting
                st.markdown(
                    f"""
                <div class="chat-container">
                    <div class="user-message">
                        {question}
                    </div>
                    <div class="bot-message">
                        {answer}
                    </div>
                    <small style="color: #666; margin-top: 10px; display: block;">
                        ⚡ Response time: {response_time:.2f}s | 🔍 Search: {search_type} | 🤖 Provider: {provider_choice}
                    </small>
                </div>
                """,
                    unsafe_allow_html=True,
                )

# Display recent chat history
if st.session_state.chat_history:
    st.markdown("### 📜 Recent Conversations")

    # Show last 3 conversations
    for i, chat in enumerate(reversed(st.session_state.chat_history[-3:])):
        with st.expander(f"💬 {chat['question'][:60]}... ({chat['timestamp']})", expanded=False):
            st.markdown(f"**🙋 Question:** {chat['question']}")
            st.markdown(f"**🤖 Answer:** {chat['answer']}")

            # Show metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"⏱️ {chat.get('response_time', 0):.2f}s")
            with col2:
                st.caption(f"🔍 {chat.get('search_type', 'N/A')}")
            with col3:
                st.caption(f"🤖 {chat.get('provider', 'N/A')}")

# Analytics panel
with col2:
    if st.session_state.analytics:
        create_analytics_dashboard(st.session_state.analytics)
    else:
        st.markdown(
            """
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; border-left: 4px solid #667eea;">
            <h3>📊 Document Analytics</h3>
            <p>Upload and process a PDF to see comprehensive document insights, reading level analysis, and word frequency statistics.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# Clean up temporary files
try:
    if "file_path" in locals():
        os.unlink(file_path)
except:
    pass

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "🚀 Advanced PDF Chat Assistant | Built with Streamlit & LangChain | "
    f"Session: {len(st.session_state.chat_history)} questions answered"
    "</div>",
    unsafe_allow_html=True,
)
