# Rolex RAG Assistant

**Rolex RAG Assistant** is a conversational AI app built with Streamlit and powered by Retrieval-Augmented Generation (RAG). It uses official Rolex documents such as brochures, FAQs, pricing sheets , and product guides to answer user questions about watches. The system is based on the Gemini 2.5 Flash model and LangChain for accurate, fast, and context-aware responses.

## Features

- Ask natural language questions about Rolex watches and get offical-document-backed answers (except the watch prices). 
- Supports both PDF and DOCX file formats from official Rolex sources
- Uses Gemini 2.5 Flash for intelligent response generation
- Memory-enabled: remembers the last 3 interactions for continuity
- Retrieval-augmented using a vector database powered by Chroma
- Custom prompt with fallback strategy if no answer is found
- Automatically chunks and embeds documents using LangChain’s text splitter
- Clean and intuitive Streamlit interface
- Supports over 25 watches with real Rolex brochures and manuals

## How It Works

1. All official Rolex documents are preloaded from the `data/` directory
2. Text is extracted and split into overlapping chunks to maintain context
3. Chunks are embedded using Gemini’s embedding model and stored in a Chroma vector store
4. When a user asks a question:
   - The assistant retrieves the most relevant chunks
   - Gemini 2.5 Flash generates a precise, human-like response based on retrieved content and recent memory

## Project Structure

- main.py # Streamlit frontend
- rolex_core.py # RAG logic, document loading, and retrieval
- data/ # Official Rolex documents (PDFs and DOCX)
- demos/ # Example test cases and flows
- .env # API key and local paths (excluded from GitHub)
- requirements.txt # Required Python dependencies