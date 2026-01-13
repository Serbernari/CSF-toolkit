from __future__ import annotations

from typing import Protocol, Mapping, Any


class ReactionGenerator(Protocol):
    """Generates plausible replies to a comment/post given context."""

    def generate_replies(
        self,
        *,
        comment: str,
        topic: str | None = None,
        n: int = 8,
        context: Mapping[str, Any] | None = None,
    ) -> list[str]:
        ...
