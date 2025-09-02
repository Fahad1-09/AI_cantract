from fastapi import FastAPI, UploadFile, File , HTTPException
from .pinecone_utilis import embed_and_store ,index
from .services.pdf_parsing import read_pdf, split_text
from .schema.pydantic_models import ProjectInput ,RetrieveResponse,DraftResponse
from .services.drafting import generate_draft
from .session_memory import session_store
from .services.compliance import check_compliance
import tempfile

app = FastAPI()


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
    
@app.post("/input/")
async def project_input(details: ProjectInput):  # <-- now uses Pydantic model
    session_id = session_store.create_session(details.dict())
    return {
        "session_id": session_id,
        "message": "Project details stored",
        "data": details.dict()  # optional: echo back for confirmation
    }


@app.post("/retrieve/", response_model=RetrieveResponse)
async def retrieve_contract(session_id: str):
    data = session_store.get(session_id)
    if not data:
        raise HTTPException(404, "Session not found")

    # Instead of semantic search, just pull all chunks for this contract doc
    results = index.query(
        vector=[0.0] * 768,   # dummy vector, required by Pinecone API
        top_k=10,
        namespace="contracts",
        include_metadata=True,
        filter={"doc_id": {"$eq": "sample docs.pdf"}}  # ✅ only your base contract
    )

    chunks = [m["metadata"]["chunk"] for m in results["matches"]]
    session_store.update(session_id, {"chunks": chunks})

    return {"session_id": session_id, "chunks": chunks}

@app.post("/draft/", response_model=DraftResponse)
async def draft_contract(session_id: str):
    data = session_store.get(session_id)
    if not data or "chunks" not in data:
        raise HTTPException(400, "No template chunks found. Run /retrieve first.")

    # AI call with user input + 4 chunks as structure
    draft = generate_draft(data["chunks"], data)
    session_store.update(session_id, {"draft": draft})

    return {"session_id": session_id, "draft": draft}


@app.post("/compliance/")
async def compliance_check(session_id: str):
    data = session_store.get(session_id)
    if not data or "draft" not in data:
        raise HTTPException(400, "No drafted contract found. Run /draft first.")

    report = check_compliance(data["draft"])
    session_store.update(session_id, {"compliance": report})

    # Return plain text so frontend shows it nicely
    return report





