"""
epoch_sweep.py - why does the paper's AG News configuration fail on 20 Newsgroups?
Sweeps epochs (and two learning rates) with everything else fixed to the paper.

    python src/epoch_sweep.py --dataset 20ng --ft-bin ../fastText/fasttext
"""
import argparse
import json
import statistics

from run_experiments import DATA, PAPER, RES, FastText, metrics, read_ft

ap = argparse.ArgumentParser()
ap.add_argument("--dataset", default="20ng")
ap.add_argument("--seeds", type=int, default=3)
ap.add_argument("--threads", type=int, default=2)
ap.add_argument("--ft-bin", default=None)
a = ap.parse_args()

ft = FastText(a.ft_bin, a.threads)
train, test = DATA / f"{a.dataset}.train", DATA / f"{a.dataset}.test"
gold, _ = read_ft(test)
rows = []
for lr in (0.25, 1.0):
    for ep in (5, 10, 25, 50, 100):
        accs, secs = [], []
        for s in range(a.seeds):
            pred, t = ft.run(train, test, {**PAPER, "lr": lr, "epoch": ep}, seed=s)
            accs.append(metrics(gold, pred)["accuracy"])
            secs.append(t)
        row = {"lr": lr, "epoch": ep, "acc_mean": round(statistics.mean(accs), 2),
               "acc_sd": round(statistics.stdev(accs), 2), "train_s": round(statistics.mean(secs), 2)}
        rows.append(row)
        print(row)
json.dump(rows, open(RES / f"{a.dataset}_epoch_sweep.json", "w"), indent=2)
