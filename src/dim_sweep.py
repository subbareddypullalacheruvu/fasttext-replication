"""
dim_sweep.py - is the small hidden layer (dim=10) the reason fastText trails TF-IDF on
20 Newsgroups? Re-trains the two best 20NG settings with dim = 10, 50 and 100.

    python src/dim_sweep.py --seeds 5
"""
import argparse
import json
import statistics

from run_experiments import DATA, PAPER, RES, FastText, metrics, read_ft

ap = argparse.ArgumentParser()
ap.add_argument("--dataset", default="20ng")
ap.add_argument("--seeds", type=int, default=5)
ap.add_argument("--threads", type=int, default=2)
ap.add_argument("--ft-bin", default=None)
a = ap.parse_args()

ft = FastText(a.ft_bin, a.threads)
train, test = DATA / f"{a.dataset}.train", DATA / f"{a.dataset}.test"
gold, _ = read_ft(test)
SETTINGS = [{"epoch": 25, "lr": 0.25}, {"epoch": 10, "lr": 1.0}]
rows = []
for setting in SETTINGS:
    for dim in (10, 50, 100):
        accs, secs = [], []
        for s in range(a.seeds):
            pred, t = ft.run(train, test, {**PAPER, **setting, "dim": dim}, seed=s)
            accs.append(metrics(gold, pred)["accuracy"])
            secs.append(t)
        row = {**setting, "dim": dim, "acc_mean": round(statistics.mean(accs), 2),
               "acc_sd": round(statistics.stdev(accs), 2), "train_s": round(statistics.mean(secs), 2)}
        rows.append(row)
        print(row)
json.dump(rows, open(RES / f"{a.dataset}_dim_sweep.json", "w"), indent=2)
