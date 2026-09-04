import io
import os
from typing import Optional

from docx import Document
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from index_generator import IndexGenerator


DEFAULT_MODEL = os.getenv("SPACY_MODEL", "en_core_web_trf")
DEFAULT_WORDS_PER_PAGE = int(os.getenv("WORDS_PER_PAGE", "250"))
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "25"))

app = FastAPI(title="Indexer API", version="1.0.0")

# Allow your GitHub Pages frontend + local preview.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://likhitayerra.github.io",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

_generator: Optional[IndexGenerator] = None


def get_generator(words_per_page: int) -> IndexGenerator:
    # Cache NLP model in memory for speed; recreate if words/page changed.
    global _generator
    if _generator is None or _generator.words_per_page != words_per_page:
        _generator = IndexGenerator(words_per_page=words_per_page, model_name=DEFAULT_MODEL)
    # Clear previous run state.
    _generator.index_terms.clear()
    return _generator


@app.get("/health")
def health() -> dict:
    return {"ok": True, "model": DEFAULT_MODEL}


@app.post("/generate-index")
async def generate_index(
    file: UploadFile = File(...),
    words_per_page: int = Form(DEFAULT_WORDS_PER_PAGE),
) -> JSONResponse:
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail="Please upload a .docx file.")

    contents = await file.read()
    if len(contents) > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File too large (max {MAX_UPLOAD_MB}MB).")

    try:
        doc = Document(io.BytesIO(contents))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid .docx file.") from exc

    try:
        generator = get_generator(words_per_page=words_per_page)
        text_with_pages = generator.extract_text_with_positions_from_document(doc)
        generator.extract_indexable_terms(text_with_pages)
        index_text = generator.generate_index()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Index generation failed: {exc}") from exc

    return JSONResponse(
        {
            "index": index_text,
            "terms_count": len(generator.index_terms),
            "model": DEFAULT_MODEL,
            "words_per_page": words_per_page,
        }
    )
