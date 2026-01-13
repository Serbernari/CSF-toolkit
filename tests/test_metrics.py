from csf_toolkit import Thread, Reply, ponos, ponos_net, ponos_early, ponos_weighted

class FixedScorer:
    def __init__(self, labels):
        self.labels = labels
    def score_replies(self, *, topic, comment, replies, context=None):
        return self.labels[: len(replies)]

def test_ponos_basic():
    thread = Thread(comment="c", replies=[Reply("a"), Reply("b"), Reply("c")])
    scorer = FixedScorer([-1, 0, -1])
    assert ponos(thread, scorer) == 2/3

def test_ponos_net():
    thread = Thread(comment="c", replies=[Reply("a"), Reply("b")])
    scorer = FixedScorer([1, -1])
    assert ponos_net(thread, scorer) == 0.0

def test_ponos_early():
    thread = Thread(comment="c", replies=[Reply("a"), Reply("b"), Reply("c")])
    scorer = FixedScorer([-1, -1, 0])
    assert ponos_early(thread, scorer, k=2) == 1.0

def test_weighted_reduces_to_unweighted():
    thread = Thread(comment="c", replies=[Reply("a", {"w": 1}), Reply("b", {"w": 1})])
    scorer = FixedScorer([-1, 0])
    w = lambda md: md.get("w", 1)
    assert ponos_weighted(thread, scorer, weight_fn=w) == ponos(thread, scorer)

def test_weighted():
    thread = Thread(comment="c", replies=[Reply("a", {"w": 10}), Reply("b", {"w": 1})])
    scorer = FixedScorer([-1, -1])
    w = lambda md: md["w"]
    assert ponos_weighted(thread, scorer, weight_fn=w) == 1.0
