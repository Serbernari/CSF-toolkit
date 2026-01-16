# csf-toolkit (starter package)

A small, composable Python toolkit for CSF-style reception metrics (PONOS + variants).

## Install

```bash
pip install -e .
```

## Quickstart

```python
from csf_toolkit import Thread, Reply, ponos

class ToyScorer:
    def score_replies(self, *, topic, comment, replies, context=None):
        # demo: label anything containing "no" as negative
        out = []
        for r in replies:
            out.append(-1 if "no" in r.lower() else 0)
        return out

thread = Thread(
    topic="Example topic",
    comment="I like pineapple on pizza.",
    replies=[Reply("no way"), Reply("sure"), Reply("NO!")],
)

print(ponos(thread, ToyScorer()))  # 0.666...
```

## What’s included (v0.1)
- `ponos`, `ponos_net`, `ponos_early`, `ponos_weighted`
- simple Wilson confidence interval helper (`ponos(..., return_ci=True)`)

## Next steps
- Plug-in sentiment scorers (HF / LLM prompting / fine-tuned models)
- Thread loaders for your platform(s)
- Evaluation helpers (quadrant analysis: intrinsic vs reception)
