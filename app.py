
import os
from fastapi import FastAPI
import chromadb
import ollama
from pydantic import BaseModel
import uuid

# Load environment variables if using a .env file (uncomment if needed)
# from dotenv import load_dotenv
# load_dotenv()app = FastAPI()
# Use an environment variable for the ChromaDB path, with a default


chroma_db_path = os.getenv("CHROMA_DB_PATH", "./db")
chroma = chromadb.PersistentClient(path=chroma_db_path)
collection = chroma.get_or_create_collection("docs")

app = FastAPI()
class Document(BaseModel):
    text: str
    
@app.post("/query")
def query(q: str):
    results = collection.query(query_texts=[q], n_results=1)
    context = results["documents"][0][0] if results["documents"] else ""
    answer = ollama.generate(
        model="tinyllama",
        prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
    )
    return {"answer": answer["response"]}
    
@app.post("/add")
def add_document(doc: Document):
    collection.add(documents=[doc.text], ids=[str(uuid.uuid4())])
    return {"message": "Document added successfully"}
    
@app.get("/health")
def health_check():
    return {"status": "ok"}
