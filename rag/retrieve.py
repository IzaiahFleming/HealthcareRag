"""Vector search followed by cross-encoder reranking."""
import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder
import config

_embedder = None
_reranker = None
_collection = None


def _lazy():
    global _embedder, _reranker, _collection
    if _embedder is None:
        _embedder = SentenceTransformer(config.EMBED_MODEL)
    if _reranker is None:
        _reranker = CrossEncoder(config.RERANK_MODEL)
    if _collection is None:
        client = chromadb.PersistentClient(path=str(config.INDEX_DIR))
        _collection = client.get_collection("policies")


def retrieve(query, top_k=None, rerank_top_n=None):
    _lazy()
    top_k = top_k or config.TOP_K
    rerank_top_n = rerank_top_n or config.RERANK_TOP_N

    q_emb = _embedder.encode([query], normalize_embeddings=True).tolist()
    res = _collection.query(query_embeddings=q_emb, n_results=top_k)
    docs, metas = res["documents"][0], res["metadatas"][0]
    if not docs:
        return []

    scores = _reranker.predict([(query, d) for d in docs])
    ranked = sorted(zip(docs, metas, scores), key=lambda x: x[2], reverse=True)[:rerank_top_n]
    return [{"text": d, "metadata": m, "score": float(s)} for d, m, s in ranked]
