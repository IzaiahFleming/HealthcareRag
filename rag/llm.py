"""Thin, provider-agnostic LLM wrapper.

In a real HIPAA deployment this would point at a BAA-covered endpoint
(Azure OpenAI, AWS Bedrock, or an Anthropic enterprise contract) and no PHI
would ever be sent to a non-covered model.
"""
import config

_SYSTEM = "You are a careful medical-coding and coverage-policy assistant."


def complete(prompt, system=None, model=None, max_tokens=1024):
    model = model or config.LLM_MODEL
    system = system or _SYSTEM
    if config.LLM_PROVIDER == "anthropic":
        from anthropic import Anthropic
        client = Anthropic()  # reads ANTHROPIC_API_KEY
        msg = client.messages.create(
            model=model, max_tokens=max_tokens, system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    if config.LLM_PROVIDER == "openai":
        from openai import OpenAI
        client = OpenAI()  # reads OPENAI_API_KEY
        resp = client.chat.completions.create(
            model=model, max_tokens=max_tokens,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content
    raise ValueError(f"Unknown LLM_PROVIDER: {config.LLM_PROVIDER}")
