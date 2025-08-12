# app.py

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
import requests
# Configuration
DEFAULT_OPENAI_KEY = "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"

def check_ollama_availability():
    """Check if Ollama is running locally"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def setup_llm_and_embeddings(provider_choice, api_key=None):
    """Setup LLM and embeddings based on provider choice"""
    if provider_choice == "OpenAI":
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        else:
            os.environ["OPENAI_API_KEY"] = DEFAULT_OPENAI_KEY
        
        try:
            embeddings = OpenAIEmbeddings()
            llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
            return llm, embeddings, True
        except Exception as e:
            st.error(f"OpenAI setup failed: {str(e)}")
            return None, None, False
    
    elif provider_choice == "Free (HuggingFace Embeddings + Local Processing)":
        try:
            # Use free HuggingFace embeddings
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            # Simple text processing without external API
            return "simple", embeddings, True
        except Exception as e:
            st.error(f"Free setup failed: {str(e)}")
            return None, None, False

def load_pdf_with_fallback(file_path):
    """Try multiple methods to load PDF content"""
    documents = []
    
    # Method 1: Try PyPDFLoader first
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load_and_split()
        st.success("PDF loaded successfully with PyPDFLoader!")
        return documents
    except Exception as e:
        st.warning(f"PyPDFLoader failed: {str(e)}")
    
    # Method 2: Try pdfplumber as fallback
    try:
        st.info("Trying alternative PDF reader...")
        with pdfplumber.open(file_path) as pdf:
            text_content = ""
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text_content += f"\n--- Page {page_num + 1} ---\n"
                    text_content += page_text
            
            if text_content.strip():
                # Create a Document object
                documents = [Document(page_content=text_content, metadata={"source": file_path})]
                st.success("PDF loaded successfully with pdfplumber!")
                return documents
            else:
                raise Exception("No text could be extracted from the PDF")
                
    except Exception as e:
        st.error(f"All PDF loading methods failed: {str(e)}")
        return None

def simple_qa(docs, question):
    """Enhanced keyword-based QA for free tier"""
    question_lower = question.lower()
    question_words = [word.strip('.,!?;:') for word in question_lower.split() if len(word.strip('.,!?;:')) > 2]
    
    relevant_chunks = []
    scores = []
    
    for doc in docs:
        content = doc.page_content.lower()
        # Count keyword matches
        matches = sum(1 for word in question_words if word in content)
        
        if matches > 0:
            relevant_chunks.append(doc.page_content)
            scores.append(matches)
    
    if relevant_chunks:
        # Sort by relevance score (most matches first)
        sorted_chunks = sorted(zip(relevant_chunks, scores), key=lambda x: x[1], reverse=True)
        best_chunk = sorted_chunks[0][0]
        
        # Find the most relevant paragraph within the chunk
        paragraphs = [p.strip() for p in best_chunk.split('\n') if p.strip()]
        best_paragraph = ""
        best_score = 0
        
        for paragraph in paragraphs:
            paragraph_lower = paragraph.lower()
            para_matches = sum(1 for word in question_words if word in paragraph_lower)
            if para_matches > best_score:
                best_score = para_matches
                best_paragraph = paragraph
        
        if best_paragraph:
            return f"Based on the document content:\n\n{best_paragraph}"
        else:
            # Fallback to first part of best chunk
            return f"Based on the document content:\n\n{best_chunk[:800]}..." if len(best_chunk) > 800 else best_chunk
    else:
        # If no keyword matches, try partial matching
        for doc in docs:
            content = doc.page_content.lower()
            for word in question_words:
                if any(word[:4] in content_word for content_word in content.split() if len(content_word) > 4):
                    # Found partial match
                    paragraphs = [p.strip() for p in doc.page_content.split('\n') if p.strip()]
                    if paragraphs:
                        return f"Based on related content I found:\n\n{paragraphs[0]}"
        
        return f"I couldn't find specific information about '{question}' in the document. Here's some content from the document that might be relevant:\n\n{docs[0].page_content[:500]}..." if docs else "No relevant information found."
# Streamlit app to chat with a PDF document
st.set_page_config(page_title="Chat with your PDF", layout="wide")
st.title("📄 Chat with your PDF")

# Sidebar for configuration
st.sidebar.title("Configuration")

# Provider selection
provider_options = ["Free (HuggingFace Embeddings + Local Processing)", "OpenAI"]
provider_choice = st.sidebar.selectbox("Choose AI Provider:", provider_options)

# API Key input for OpenAI
api_key = None
if provider_choice == "OpenAI":
    api_key = st.sidebar.text_input("OpenAI API Key (optional):", type="password", 
                                   help="Leave empty to use default key, or enter your own")
    st.sidebar.warning("⚠️ You exceeded your OpenAI quota. Consider using the free option or updating your API key.")

# Provider info
if provider_choice == "Free (HuggingFace Embeddings + Local Processing)":
    st.sidebar.info("✅ Using free local processing - no API costs!")
elif provider_choice == "OpenAI":
    st.sidebar.info("💰 Using OpenAI API - charges may apply")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
if uploaded_file is not None:
    # Use a temporary file to avoid conflicts
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        file_path = tmp_file.name

    st.success("PDF uploaded successfully. Processing...")

    # Setup LLM and embeddings based on user choice
    llm, embeddings, setup_success = setup_llm_and_embeddings(provider_choice, api_key)
    
    if not setup_success:
        st.error("Failed to setup AI provider. Please check your configuration.")
    else:
        # Try to load the PDF with fallback methods
        pages = load_pdf_with_fallback(file_path)
        
        if pages is None:
            st.error("Failed to process the PDF. Please try a different file or check if the PDF is corrupted.")
        else:
            try:
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
                docs = splitter.split_documents(pages)

                if provider_choice == "Free (HuggingFace Embeddings + Local Processing)":
                    # For free option, use simple processing
                    st.success("✅ PDF processed successfully with free local processing!")
                    st.info(f"📄 Processed {len(docs)} text chunks from your PDF")
                    
                    # Show a preview of the content
                    with st.expander("📖 Preview of extracted content"):
                        preview_text = docs[0].page_content[:300] + "..." if len(docs[0].page_content) > 300 else docs[0].page_content
                        st.text(preview_text)
                    
                    question = st.text_input("Ask a question about your PDF:")
                    if question:
                        with st.spinner("Searching through your document..."):
                            answer = simple_qa(docs, question)
                            st.markdown(f"**Answer:** {answer}")
                            
                            # Debug info in expander
                            with st.expander("🔍 Search Details"):
                                question_words = [word.strip('.,!?;:') for word in question.lower().split() if len(word.strip('.,!?;:')) > 2]
                                st.write(f"Search keywords: {', '.join(question_words)}")
                                st.write(f"Total document chunks searched: {len(docs)}")
                
                else:
                    # For OpenAI option, use full RAG pipeline
                    db = FAISS.from_documents(docs, embeddings)
                    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever())
                    
                    st.success("✅ PDF processed successfully with AI-powered search!")
                    question = st.text_input("Ask a question about your PDF:")
                    if question:
                        with st.spinner("Thinking..."):
                            try:
                                answer = qa.run(question)
                                st.markdown(f"**Answer:** {answer}")
                            except Exception as e:
                                if "quota" in str(e).lower() or "429" in str(e):
                                    st.error("❌ OpenAI quota exceeded. Please switch to the free option or update your API key.")
                                    st.info("💡 Try selecting 'Free (HuggingFace Embeddings + Local Processing)' from the sidebar.")
                                else:
                                    st.error(f"Error: {str(e)}")

            except Exception as e:
                st.error(f"Error processing the document: {str(e)}")
            finally:
                # Clean up temporary file
                try:
                    os.unlink(file_path)
                except:
                    pass
