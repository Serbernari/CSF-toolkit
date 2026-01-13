from __future__ import annotations

def sentiment_prompt(topic: str | None, comment: str, reply: str) -> str:
    """A safe, generic prompt template for reply sentiment (-/0/+).

    This is intentionally domain-agnostic; you can specialize it per community.
    """
    t = topic or ""
    return f"""You are a sentiment classification assistant.

Classify the *reply* as one of: Positive, Neutral, Negative.

Use the conversation context:
Topic: {t}
Comment: {comment}
Reply: {reply}

Return exactly one token: Positive, Neutral, or Negative.
"""
