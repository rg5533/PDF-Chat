# app.py

import streamlit as st
from utils.pdf_processor import extract_text_from_pdf
from utils.vector_store import (
    get_chroma_client,
    create_collection,
    add_documents,
    query_collection
)
from utils.openai_connector import generate_response
import os
import uuid
import logging
from dotenv import load_dotenv

# Initialize logging
from utils.logger import setup_logging
setup_logging()

# Load environment variables
load_dotenv()

# Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def split_text(text, chunk_size=1000, overlap=100):
    """
    Splits text into chunks of specified size with overlap.

    :param text: The complete text to split.
    :param chunk_size: Number of characters per chunk.
    :param overlap: Number of overlapping characters between chunks.
    :return: List of text chunks.
    """
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # Move back by 'overlap' characters
    return chunks

# Set Streamlit page configuration at the very beginning
st.set_page_config(page_title="Chat with PDF", page_icon="📄💬", layout="wide")

# Initialize ChromaDB client and collection
try:
    client = get_chroma_client()
    collection = create_collection(client, "pdf_collection")
except Exception as e:
    st.error(f"Error initializing ChromaDB: {e}")
    logging.error(f"Error initializing ChromaDB: {e}")

# Streamlit App Title
st.title("📄💬 Chat with PDF")

# Sidebar for PDF Upload
st.sidebar.header("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("Uploaded file is too large. Maximum allowed size is 10MB.")
        logging.warning(f"Uploaded file {uploaded_file.name} exceeds the size limit.")
    else:
        with st.spinner("Processing PDF..."):
            # Save uploaded PDF to a temporary location
            temp_pdf_path = f"temp_{uuid.uuid4().hex}.pdf"
            try:
                with open(temp_pdf_path, "wb") as f:
                    f.write(uploaded_file.read())
                logging.info(f"Saved uploaded file to {temp_pdf_path}.")

                # Extract text using PyMuPDF
                text = extract_text_from_pdf(temp_pdf_path)
                logging.info(f"Extracted text length: {len(text) if text else 'No text'}")

                if not text:
                    st.error("Failed to extract text from the uploaded PDF. Please try a different file.")
                else:
                    # Implement text chunking for large PDFs
                    documents = split_text(text.strip())
                    metadatas = [{"source": uploaded_file.name, "chunk": i+1} for i in range(len(documents))]
                    ids = [str(uuid.uuid4()) for _ in range(len(documents))]

                    # Add to ChromaDB
                    try:
                        add_documents(collection, documents, metadatas, ids)
                        st.success("PDF processed and added to the knowledge base.")
                        logging.info(f"Added {len(documents)} documents from {uploaded_file.name} to ChromaDB.")
                    except Exception as e:
                        st.error(f"Error adding documents to ChromaDB: {e}")
                        logging.error(f"Error adding documents to ChromaDB: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                logging.error(f"An unexpected error occurred: {e}")
            finally:
                # Clean up temporary file
                if os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)
                    logging.info(f"Deleted temporary file {temp_pdf_path}.")

# Chat Interface
st.header("Ask questions about your PDF")

user_query = st.text_input("Enter your question:")

if st.button("Ask") and user_query:
    with st.spinner("Generating response..."):
        try:
            # Query ChromaDB
            query_results = query_collection(collection, user_query)
            retrieved_texts = query_results["documents"][0]

            if not retrieved_texts:
                st.error("No relevant information found in the uploaded PDFs.")
                logging.info("Query returned no relevant documents.")
            else:
                # Construct prompt
                context = "\n\n".join(retrieved_texts)
                prompt = f"Context:\n{context}\n\nQuestion: {user_query}\nAnswer:"
                logging.info(f"Constructed prompt: {prompt[:100]}...")  # Log first 100 chars

                # Generate response using OpenAI
                answer = generate_response(prompt)

                st.write("**Answer:**")
                st.write(answer)
        except Exception as e:
            st.error(f"Error during query or response generation: {e}")
            logging.error(f"Error during query or response generation: {e}")

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ using Streamlit, OpenAI, and ChromaDB.")
