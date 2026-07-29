"""Embed chunks and load them into a persistent Chroma collection."""
import chromadb
from sentence_transformers import SentenceTransformer
import config
from ingest.parse import load_documents
from ingest.chunk import chunk_documents


def build():
    docs = load_documents()
    chunks = chunk_documents(docs)
    if not chunks:
        raise SystemExit("No chunks produced. Check your CMS columns / FILTER settings in config.py.")

    embedder = SentenceTransformer(config.EMBED_MODEL)
    embeddings = embedder.encode(
        [c["text"] for c in chunks], show_progress_bar=True, normalize_embeddings=True
    ).tolist()

    client = chromadb.PersistentClient(path=str(config.INDEX_DIR))
    try:
        client.delete_collection("policies")
    except Exception:
        pass
    col = client.create_collection("policies", metadata={"hnsw:space": "cosine"})
    col.add(
        ids=[str(i) for i in range(len(chunks))],
        embeddings=embeddings,
        documents=[c["text"] for c in chunks],
        metadatas=[{
            "title": str(c["title"]),
            "source": str(c["source"]),
            "doc_id": str(c["doc_id"]),
            "chunk_index": c["chunk_index"],
        } for c in chunks],
    )
    print(f"Indexed {len(chunks)} chunks into {config.INDEX_DIR}")


if __name__ == "__main__":
    build()
