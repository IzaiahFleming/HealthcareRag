"""Offline eval over eval/golden.jsonl using DeepEval's RAG metrics.

DeepEval uses an LLM judge (set EVAL_MODEL + provider key in .env). Its API moves
fast -- verify metric imports/signatures against the current DeepEval docs if an
import fails. Record your baseline, then re-run after each change and track the delta.
"""
import json
from pathlib import Path
from rag.retrieve import retrieve
from rag.generate import generate

GOLDEN = Path(__file__).parent / "golden.jsonl"


def load_golden():
    rows = []
    for line in GOLDEN.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("//"):
            rows.append(json.loads(line))
    return rows


def run():
    rows = [r for r in load_golden() if "REPLACE" not in r.get("question", "")]
    if not rows:
        raise SystemExit("Replace the placeholder rows in eval/golden.jsonl with real Q&A first.")

    try:
        from deepeval import evaluate
        from deepeval.test_case import LLMTestCase
        from deepeval.metrics import (
            FaithfulnessMetric, AnswerRelevancyMetric,
            ContextualPrecisionMetric, ContextualRecallMetric,
        )
    except ImportError:
        raise SystemExit("pip install deepeval, then set your eval model in .env")

    cases = []
    for r in rows:
        passages = retrieve(r["question"])
        ctx = [p["text"] for p in passages]
        answer = generate(r["question"], passages)
        cases.append(LLMTestCase(
            input=r["question"], actual_output=answer,
            expected_output=r.get("ground_truth"), retrieval_context=ctx,
        ))

    metrics = [
        FaithfulnessMetric(), AnswerRelevancyMetric(),
        ContextualPrecisionMetric(), ContextualRecallMetric(),
    ]
    evaluate(cases, metrics)


if __name__ == "__main__":
    run()
