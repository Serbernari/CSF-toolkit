from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Tuple


@dataclass(frozen=True)
class ProportionCI:
    p: float
    n: int
    lower: float
    upper: float


def wilson_ci(k: int, n: int, z: float = 1.96) -> ProportionCI:
    """Wilson score interval for a binomial proportion.

    Returns a 95% CI by default (z=1.96).
    """
    if n <= 0:
        return ProportionCI(p=0.0, n=0, lower=0.0, upper=0.0)
    p = k / n
    denom = 1.0 + (z*z)/n
    center = (p + (z*z)/(2*n)) / denom
    radius = (z * sqrt((p*(1-p)/n) + (z*z)/(4*n*n))) / denom
    lower = max(0.0, center - radius)
    upper = min(1.0, center + radius)
    return ProportionCI(p=p, n=n, lower=lower, upper=upper)
