"""Cheap groundedness proxy for v1: fraction of answer sentences whose key words
appear in the retrieved context. Replace with an NLI model or DeepEval's
FaithfulnessMetric once the eval harness is in place.
"""


def groundedness_score(answer, contexts):
    blob = " ".join(contexts).lower()
    sentences = [s.strip() for s in answer.replace("\n", " ").split(".") if len(s.strip()) > 15]
    if not sentences:
        return 1.0
    supported = 0
    for s in sentences:
        words = [w for w in s.lower().split() if len(w) > 4]
        if words and sum(w in blob for w in words) / len(words) > 0.5:
            supported += 1
    return round(supported / len(sentences), 3)
