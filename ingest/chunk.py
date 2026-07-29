"""Split documents into overlapping word-windows. Upgrade to token-based chunking later."""
import config


def chunk_documents(docs):
    chunks = []
    size, overlap = config.CHUNK_SIZE, config.CHUNK_OVERLAP
    step = max(1, size - overlap)
    for d in docs:
        words = d["text"].split()
        for i in range(0, len(words), step):
            piece = " ".join(words[i:i + size]).strip()
            if not piece:
                continue
            chunks.append({
                "text": piece,
                "title": d["title"],
                "source": d["source"],
                "doc_id": d["id"],
                "chunk_index": i // step,
            })
    print(f"Created {len(chunks)} chunks.")
    return chunks
