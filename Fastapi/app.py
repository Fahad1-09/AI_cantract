from fastapi import FastAPI, UploadFile, File ,Query
from .pinecone_utilis import embed_and_store, generate_embedding ,index
from PyPDF2 import PdfReader
import tempfile
from .pydantic_models import SearchResponse, SearchResult

app = FastAPI()

# Read text from PDF
def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Split into word chunks
def split_text(text: str, max_length=500):
    words = text.split()
    chunks, current_chunk = [], []
    
    for word in words:
        if len(current_chunk) + len(word.split()) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

@app.get("/")
def root():
    return {"message": "FastAPI backend is running 🚀"}


@app.post("/ingest-pdf/")
async def ingest_pdf(file: UploadFile = File(...)):
    try:
        # Save uploaded PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # 1. Extract text from PDF
        text = read_pdf(tmp_path)

        # 2. Split text into chunks
        chunks = split_text(text, max_length=500)

        # 3. Embed + Store in Pinecone
        result = embed_and_store(chunks, doc_id=file.filename, namespace="contracts")

        return {
            "status": "success",
            "file_name": file.filename,
            "total_chunks": len(chunks),
            "vectors_stored": result
        }
    except Exception as e:
        return {"status": "error", "details": str(e)}


@app.post("/search/", response_model=SearchResponse)
async def semantic_search(query: str = Query(..., description="Search query text"), top_k: int = 1):
    try:
        # 1. Generate embedding for query
        query_embedding = generate_embedding(query)

        # 2. Search Pinecone
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            namespace="contracts",
            include_metadata=True
        )

        # 3. Format results
        matches = [
            SearchResult(
                chunk=match['metadata']['chunk'],
                doc_id=match['metadata']['doc_id']
            )
            for match in results['matches']
        ]

        return SearchResponse(
            status="success",
            query=query,
            results=matches
        )

    except Exception as e:
        return SearchResponse(status="error", query=query, results=[])
    
    