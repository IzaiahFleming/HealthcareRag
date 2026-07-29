"""End-to-end query: PHI redaction -> retrieve -> generate -> redact + score."""
import sys
from rag.retrieve import retrieve
from rag.generate import generate
from guardrails.phi import redact
from guardrails.groundedness import groundedness_score


def query(question):
    clean_q, phi_in = redact(question)          # never send PHI downstream
    passages = retrieve(clean_q)
    answer = generate(clean_q, passages)
    safe_answer, _ = redact(answer)
    grounded = groundedness_score(safe_answer, [p["text"] for p in passages])
    return {
        "question": question,
        "answer": safe_answer,
        "grounded": grounded,
        "phi_found_in_input": phi_in,
        "citations": [p["metadata"] for p in passages],
    }


if __name__ == "__main__":
    from pprint import pprint
    q = " ".join(sys.argv[1:]) or "What are the coverage criteria described in the policy?"
    pprint(query(q))
