# Rag-API

A FastAPI-based Retrieval-Augmented Generation (RAG) API that combines document embeddings with local LLM inference to answer questions based on your documents.

## Overview

This project provides a REST API for:
- **Adding documents** to a vector database (ChromaDB)
- **Querying documents** with semantic search
- **Generating answers** using a local Ollama LLM model with document context

## Features

- 🔍 **Semantic Search**: Uses ChromaDB for efficient document retrieval
- 🤖 **Local LLM**: Integrates with Ollama for on-device inference (using TinyLLaMA by default)
- 📝 **Document Management**: Add and query documents through REST endpoints
- 🏥 **Health Checks**: Built-in endpoint to verify service status

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai) installed and running locally
- The TinyLLaMA model pulled in Ollama: `ollama pull tinyllama`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Rag-API
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install packages manually:
```bash
pip install fastapi uvicorn chromadb ollama pydantic
```

3. Ensure Ollama is running:
```bash
ollama serve
```

## Configuration

Set the ChromaDB database path using an environment variable (optional):

```bash
export CHROMA_DB_PATH="./db"
```

The default path is `./db` if not specified.

## Running the Application

Start the FastAPI server:

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
**GET** `/health`

Returns the service status.

**Response:**
```json
{
  "status": "ok"
}
```

### Add Document
**POST** `/add`

Add a document to the vector database.

**Request Body:**
```json
{
  "text": "Your document text here"
}
```

**Response:**
```json
{
  "message": "Document added successfully"
}
```

### Query
**POST** `/query`

Query the documents and get an AI-generated answer based on retrieved context.

**Request Parameters:**
- `q` (string): The question to ask

**Response:**
```json
{
  "answer": "Generated answer based on document context"
}
```

## Usage Example

```bash
# Check if service is running
curl http://localhost:8000/health

# Add a document
curl -X POST http://localhost:8000/add \
  -H "Content-Type: application/json" \
  -d '{"text": "Kubernetes is an open-source container orchestration system."}'

# Query the document
curl -X POST "http://localhost:8000/query?q=What%20is%20Kubernetes%3F"
```

## Project Structure

```
Rag-API/
├── app.py           # FastAPI application with endpoints
├── embed.py         # Script to embed documents into ChromaDB
├── k8s.txt          # Sample document file
├── db/              # ChromaDB database directory
└── README.md        # This file
```

## Database

The project uses **ChromaDB** as a vector database:
- Persistent storage in `./db/` directory
- Collection name: `docs`
- Automatic document embedding and retrieval

## LLM Model

The API uses **TinyLLaMA** through Ollama:
- Model: `tinyllama`
- Lightweight model suitable for local inference
- Responds to questions with context from retrieved documents

## Environment Variables

- `CHROMA_DB_PATH`: Path to ChromaDB persistent storage (default: `./db`)

## Development

To embed initial documents into the database, run:

```bash
python embed.py
```

This script reads `k8s.txt` and stores the embedding in ChromaDB.

## Troubleshooting

- **Ollama connection error**: Ensure Ollama is running (`ollama serve`)
- **Model not found**: Pull the model with `ollama pull tinyllama`
- **Permission denied on db directory**: Ensure the `./db` directory has proper write permissions
