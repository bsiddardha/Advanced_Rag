from pathlib import Path
from langchain_core.documents import Document
from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.loader import load_logs
from src.splitter import split_documents
from src.vector_store import create_vector_store
from src.bm25_retriever import create_bm25_retriever
from src.rag_chain import ask_question

# -----------------------------
# Global Objects
# -----------------------------
vector_store = None
bm25_retriever = None

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(title="AI Log Analyzer")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


# -----------------------------
# Home Page
# -----------------------------
@app.get("/")
def home():
    return FileResponse("frontend/index.html")


# -----------------------------
# Upload Log File
# -----------------------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global vector_store
    global bm25_retriever

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Load logs
    documents = load_logs(str(file_path))

    # Split into chunks
    chunks = split_documents(documents)

    # Create FAISS Vector Store
    vector_store = create_vector_store(chunks)

    # Create BM25 Retriever
    bm25_retriever = create_bm25_retriever(chunks)

    return {
        "message": "Logs indexed successfully",
        "chunks": len(chunks)
    }
@app.post("/paste")
async def paste_logs(data: dict = Body(...)):
    global vector_store
    global bm25_retriever

    logs = data.get("logs", "").strip()

    if not logs:
        return {
            "message": "No logs provided.",
            "chunks": 0
        }

    documents = [
        Document(
            page_content=logs,
            metadata={
                "source": "Pasted Logs"
            }
        )
    ]

    chunks = split_documents(documents)

    vector_store = create_vector_store(chunks)

    bm25_retriever = create_bm25_retriever(chunks)

    return {
        "message": "Pasted logs indexed successfully.",
        "chunks": len(chunks)
    }


# -----------------------------
# Ask Questions
# -----------------------------
@app.post("/ask")
async def ask(data: dict = Body(...)):
    global vector_store
    global bm25_retriever

    if vector_store is None or bm25_retriever is None:
        return {
            "answer": "Please upload logs first."
        }

    answer, docs = ask_question(
        vector_store,
        bm25_retriever,
        data["question"]
    )

    return {
        "answer": answer,
        "sources": [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in docs
        ]
    }