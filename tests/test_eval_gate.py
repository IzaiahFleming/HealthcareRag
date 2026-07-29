"""CI quality gate. Skips if no index/key is present so the suite still runs in CI.
Tune the threshold to your measured baseline once you have real data."""
import os
import pytest
import config

if not config.INDEX_DIR.exists():
    pytest.skip("no index built (run: python -m ingest.build_index)", allow_module_level=True)
if not (os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")):
    pytest.skip("no LLM key set", allow_module_level=True)


def test_smoke_pipeline_grounded():
    from rag.pipeline import query
    out = query("What are the coverage criteria described in the policy?")
    assert out["grounded"] >= 0.3
