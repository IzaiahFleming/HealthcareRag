"""Build a grounded, citation-forcing prompt and produce the answer."""
from rag.llm import complete

PROMPT = """Answer the question using ONLY the numbered context passages below.
Cite the passages you rely on as [1], [2], etc. If the context does not contain
the answer, say you don't have enough information -- do not guess.

Question: {question}

Context:
{context}

Answer (with citations):"""


def generate(question, passages):
    context = "\n\n".join(
        f"[{i + 1}] (source: {p['metadata'].get('title')}) {p['text']}"
        for i, p in enumerate(passages)
    )
    return complete(PROMPT.format(question=question, context=context))
