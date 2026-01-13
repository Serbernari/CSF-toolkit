from csf_toolkit import Thread, Reply, ponos, ponos_net

class ToyScorer:
    def score_replies(self, *, topic, comment, replies, context=None):
        out = []
        for r in replies:
            if any(w in r.lower() for w in ["hate", "no way", "stupid"]):
                out.append(-1)
            elif any(w in r.lower() for w in ["love", "agree", "nice"]):
                out.append(1)
            else:
                out.append(0)
        return out

thread = Thread(
    topic="Pineapple discourse",
    comment="Pineapple belongs on pizza.",
    replies=[Reply("No way."), Reply("I love it"), Reply("meh")],
)

print("PONOS:", ponos(thread, ToyScorer()))
print("PONOS-Net:", ponos_net(thread, ToyScorer()))
