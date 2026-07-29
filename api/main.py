"""FastAPI wrapper around the RAG pipeline."""
from fastapi import FastAPI
from pydantic import BaseModel
from rag.pipeline import query

app = FastAPI(title="Healthcare Coding-Policy RAG")


class Q(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query")
def ask(q: Q):
    return query(q.question)
