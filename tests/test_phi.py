"""Always-runnable test: the PHI guardrail must catch synthetic identifiers."""
from guardrails.phi import redact
from guardrails.synthetic_fixtures import fake_note


def test_redacts_synthetic_phi():
    note = fake_note()
    redacted, found = redact(note)
    assert found
    assert redacted != note
