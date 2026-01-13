from __future__ import annotations

from typing import Protocol, Sequence


class SentimentScorer(Protocol):
    """Scores reply sentiment given conversational context.

    Implementations should return one label per reply.
    Convention: -1=Negative, 0=Neutral, +1=Positive.
    """

    def score_replies(
        self,
        *,
        topic: str | None,
        comment: str,
        replies: Sequence[str],
        context: dict | None = None,
    ) -> list[int]:
        ...
