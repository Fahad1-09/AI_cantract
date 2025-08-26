from .config import settings
from pinecone import Pinecone
import google.generativeai as genai   # Gemini for embeddings

# Init Pinecone client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index(settings.PINECONE_INDEX_NAME)

# Init Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_embedding(text: str):
    """Generate embedding using Gemini"""
    model = "models/embedding-001"
    emb = genai.embed_content(model=model, content=text)
    return emb['embedding']

def embed_and_store(chunks, doc_id, namespace="contracts"):
    vectors = []
    for i, chunk in enumerate(chunks):
        emb = generate_embedding(chunk)
        vectors.append({
            "id": f"{doc_id}_chunk{i}",
            "values": emb,
            "metadata": {"doc_id": doc_id, "chunk": chunk}
        })
    
    # Upsert into Pinecone
    index.upsert(vectors=vectors, namespace=namespace)
    return len(vectors)
