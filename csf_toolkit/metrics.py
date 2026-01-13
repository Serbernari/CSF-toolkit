from __future__ import annotations

from typing import Callable, Mapping, Sequence, Any

from .core import Thread
from .sentiment.base import SentimentScorer
from .utils import wilson_ci, ProportionCI


def _labels(thread: Thread, scorer: SentimentScorer) -> list[int]:
    replies = [r.text for r in thread.replies]
    return scorer.score_replies(
        topic=thread.topic,
        comment=thread.comment,
        replies=replies,
        context=dict(thread.context),
    )


def ponos(thread: Thread, scorer: SentimentScorer, *, return_ci: bool = False) -> float | tuple[float, ProportionCI]:
    """PONOS: proportion of negative replies (label == -1).

    If return_ci=True, also returns a Wilson confidence interval.
    """
    labels = _labels(thread, scorer)
    n = len(labels)
    if n == 0:
        return (0.0, wilson_ci(0, 0)) if return_ci else 0.0
    k = sum(1 for x in labels if x == -1)
    score = k / n
    if not return_ci:
        return score
    return score, wilson_ci(k, n)


def ponos_net(thread: Thread, scorer: SentimentScorer) -> float:
    """PONOS-Net: average net sentiment over replies (mean of labels in {-1,0,+1})."""
    labels = _labels(thread, scorer)
    if not labels:
        return 0.0
    return sum(labels) / len(labels)


def ponos_early(thread: Thread, scorer: SentimentScorer, *, k: int = 5) -> float:
    """PONOS-Early: PONOS computed on the first k replies (preserves original ordering)."""
    if k <= 0:
        return 0.0
    sub = Thread(comment=thread.comment, replies=thread.replies[:k], topic=thread.topic, context=thread.context)
    return float(ponos(sub, scorer))


def ponos_weighted(
    thread: Thread,
    scorer: SentimentScorer,
    *,
    weight_fn: Callable[[Mapping[str, Any]], float] | None = None,
) -> float:
    """PONOS-Weighted: weighted proportion of negative replies.

    weight_fn receives reply.metadata and must return a non-negative weight.
    If weight_fn is None, falls back to unweighted PONOS.
    """
    if weight_fn is None:
        return float(ponos(thread, scorer))
    labels = _labels(thread, scorer)
    if not labels:
        return 0.0
    weights = [max(0.0, float(weight_fn(r.metadata))) for r in thread.replies[: len(labels)]]
    denom = sum(weights)
    if denom <= 0:
        return float(ponos(thread, scorer))
    num = sum(w for w, lab in zip(weights, labels) if lab == -1)
    return num / denom


def estimate_ponos_via_reactions(
    *,
    comment: str,
    generator,
    scorer: SentimentScorer,
    topic: str | None = None,
    n: int = 8,
    context: Mapping[str, Any] | None = None,
) -> float:
    """Estimate PONOS by generating plausible replies, then scoring them."""
    replies = generator.generate_replies(comment=comment, topic=topic, n=n, context=context)
    thread = Thread(comment=comment, replies=[type("R", (), {"text": t, "metadata": {}})() for t in replies], topic=topic, context=context or {})
    # The above avoids importing Reply for a tiny function, but users should pass Thread normally.
    return float(ponos(thread, scorer))
