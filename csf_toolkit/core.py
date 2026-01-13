from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class Reply:
    """A reply message in a thread.

    metadata can include: timestamp, author_id, upvotes, etc.
    """
    text: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Thread:
    """A minimal discussion thread: a post/comment plus its replies."""
    comment: str
    replies: Sequence[Reply]
    topic: str | None = None
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CSFResult:
    """Container for CSF-style two-axis outputs.

    - intrinsic: optional dictionary for text-intrinsic scores (e.g., toxicity classifier output)
    - reception: dictionary for reception-based scores (e.g., PONOS variants)
    """
    reception: Mapping[str, float]
    intrinsic: Mapping[str, float] | None = None
