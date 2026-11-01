"""
transfer_test.py - temporal-shift test: train fastText on AG News (2004-era news)
with the paper's settings, then test it on the 2026 RSS headlines.

    python src/transfer_test.py --seeds 5 [--ft-bin path/to/fasttext]
"""
import argparse
import json
import statistics

from run_experiments import DATA, PAPER, RES, FastText, metrics, read_ft

ap = argparse.ArgumentParser()
ap.add_argument("--seeds", type=int, default=5)
ap.add_argument("--threads", type=int, default=2)
ap.add_argument("--ft-bin", default=None)
a = ap.parse_args()

ft = FastText(a.ft_bin, a.threads)
train, test = DATA / "ag_news.train", DATA / "rss2026.all"
gold, texts = read_ft(test)
runs = []
for s in range(a.seeds):
    pred, secs = ft.run(train, test, PAPER, seed=s)
    m = metrics(gold, pred)
    runs.append(m)
    print(f"seed={s}: acc={m['accuracy']:.2f}  per-class recall={m['per_class_recall']}")
    if s == 0:
        with open(RES / "pred_agnews_to_rss2026.tsv", "w", encoding="utf-8") as f:
            f.write("gold\tpred\ttext\n")
            for g, p, t in zip(gold, pred, texts):
                f.write(f"{g}\t{p}\t{t}\n")
accs = [r["accuracy"] for r in runs]
out = {"train": "ag_news", "test": "rss2026 (all usable items)", "n_test": len(gold),
       "acc_mean": round(statistics.mean(accs), 2),
       "acc_sd": round(statistics.stdev(accs), 2) if len(accs) > 1 else 0.0, "runs": runs}
results = json.load(open(RES / "results.json"))
results["agnews_to_rss2026"] = out
json.dump(results, open(RES / "results.json", "w"), indent=2)
print(f"AG News -> 2026 RSS: {out['acc_mean']} +/- {out['acc_sd']} (n={len(gold)})")
