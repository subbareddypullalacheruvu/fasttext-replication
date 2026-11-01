"""
run_experiments.py - train/test fastText (official code) and a TF-IDF + logistic
regression baseline, recording accuracy AND training time over several seeds.

Backend: uses the `fasttext` Python package if installed (fasttext-wheel 0.9.2,
as on Windows), otherwise the compiled CLI binary given by --ft-bin.

Examples:
    python src/run_experiments.py --exp ag_news_bigram ag_news_unigram --seeds 5
    python src/run_experiments.py --exp all --ft-bin ../fastText/fasttext
"""
import argparse
import json
import os
import platform
import statistics
import subprocess
import tempfile
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "processed"
RES = ROOT / "results"

# Paper / classification-results.sh settings for AG News
PAPER = dict(dim=10, lr=0.25, wordNgrams=2, minCount=1, bucket=10_000_000, epoch=5)

EXPERIMENTS = {
    # name: (dataset, fastText params, paper-reported accuracy or None)
    "ag_news_bigram":  ("ag_news", PAPER, 92.5),
    "ag_news_unigram": ("ag_news", {**PAPER, "wordNgrams": 1}, 91.5),
    "20ng_paper_cfg":  ("20ng", PAPER, None),
    "20ng_epoch25":    ("20ng", {**PAPER, "epoch": 25}, None),
    "20ng_epoch25_hs": ("20ng", {**PAPER, "epoch": 25, "loss": "hs"}, None),
    "uci_paper_cfg":   ("uci", PAPER, None),
    "rss2026_paper_cfg": ("rss2026", PAPER, None),
}
BASELINES = ["ag_news", "20ng", "uci", "rss2026"]


# ------------------------------------------------------------------ helpers
def read_ft(path):
    labels, texts = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            lab, _, txt = line.rstrip("\n").partition(" ")
            labels.append(lab.replace("__label__", ""))
            texts.append(txt)
    return labels, texts


def metrics(gold, pred):
    classes = sorted(set(gold))
    acc = sum(g == p for g, p in zip(gold, pred)) / len(gold)
    f1s, per_class = [], {}
    for c in classes:
        tp = sum(g == c and p == c for g, p in zip(gold, pred))
        fp = sum(g != c and p == c for g, p in zip(gold, pred))
        fn = sum(g == c and p != c for g, p in zip(gold, pred))
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1s.append(2 * prec * rec / (prec + rec) if prec + rec else 0.0)
        per_class[c] = round(rec, 4)
    confusion = Counter(f"{g}->{p}" for g, p in zip(gold, pred) if g != p)
    return {"accuracy": round(acc * 100, 2), "macro_f1": round(100 * sum(f1s) / len(f1s), 2),
            "per_class_recall": per_class, "top_confusions": confusion.most_common(5)}


class FastText:
    def __init__(self, ft_bin, threads):
        self.threads = threads
        self.bin = ft_bin
        try:
            import fasttext  # noqa
            self.py = fasttext
        except ImportError:
            self.py = None
            if not ft_bin or not Path(ft_bin).exists():
                raise SystemExit("Install fasttext-wheel or pass --ft-bin path/to/fasttext")

    def run(self, train, test, params, seed):
        if self.py:
            t0 = time.perf_counter()
            m = self.py.train_supervised(input=str(train), thread=self.threads, seed=seed,
                                         verbose=0, **params)
            secs = time.perf_counter() - t0
            _, texts = read_ft(test)
            pred = [p[0].replace("__label__", "") for p in m.predict(texts)[0]]
            return pred, secs
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "model")
            args = [self.bin, "supervised", "-input", str(train), "-output", out,
                    "-thread", str(self.threads), "-seed", str(seed), "-verbose", "0"]
            for k, v in params.items():
                args += [f"-{k}", str(v)]
            t0 = time.perf_counter()
            subprocess.run(args, check=True, stdout=subprocess.DEVNULL)
            secs = time.perf_counter() - t0
            r = subprocess.run([self.bin, "predict", out + ".bin", str(test)],
                               check=True, capture_output=True, text=True)
            pred = [l.replace("__label__", "") for l in r.stdout.split()]
            return pred, secs


def run_fasttext(name, ft, seeds):
    ds, params, paper = EXPERIMENTS[name]
    train, test = DATA / f"{ds}.train", DATA / f"{ds}.test"
    if not train.exists():
        print(f"skip {name}: {train} missing")
        return None
    gold, texts = read_ft(test)
    runs = []
    for s in range(seeds):
        pred, secs = ft.run(train, test, params, seed=s)
        m = metrics(gold, pred)
        m.update(seed=s, train_seconds=round(secs, 2))
        runs.append(m)
        print(f"  {name} seed={s}: acc={m['accuracy']:.2f}  train={secs:.1f}s")
        if s == 0:  # keep seed-0 predictions for error analysis
            with open(RES / f"pred_{name}.tsv", "w", encoding="utf-8") as f:
                f.write("gold\tpred\ttext\n")
                for g, p, t in zip(gold, pred, texts):
                    f.write(f"{g}\t{p}\t{t}\n")
    accs = [r["accuracy"] for r in runs]
    times = [r["train_seconds"] for r in runs]
    return {"model": "fastText", "dataset": ds, "params": params, "paper_accuracy": paper,
            "n_runs": seeds, "acc_mean": round(statistics.mean(accs), 2),
            "acc_sd": round(statistics.stdev(accs), 2) if seeds > 1 else 0.0,
            "acc_min": min(accs), "acc_max": max(accs),
            "train_s_mean": round(statistics.mean(times), 2),
            "macro_f1_mean": round(statistics.mean(r["macro_f1"] for r in runs), 2),
            "runs": runs}


def run_baseline(ds):
    """Slower comparison model: TF-IDF (word 1-2 grams) + logistic regression."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    train, test = DATA / f"{ds}.train", DATA / f"{ds}.test"
    if not train.exists():
        return None
    ytr, xtr = read_ft(train)
    yte, xte = read_ft(test)
    t0 = time.perf_counter()
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
    X = vec.fit_transform(xtr)
    clf = LogisticRegression(max_iter=1000, C=10).fit(X, ytr)
    secs = time.perf_counter() - t0
    m = metrics(yte, list(clf.predict(vec.transform(xte))))
    print(f"  tfidf_lr {ds}: acc={m['accuracy']:.2f}  train={secs:.1f}s")
    return {"model": "TF-IDF + LogReg", "dataset": ds, "acc_mean": m["accuracy"], "acc_sd": 0.0,
            "n_runs": 1, "train_s_mean": round(secs, 2), "macro_f1_mean": m["macro_f1"],
            "runs": [m]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", nargs="+", default=["all"])
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--threads", type=int, default=os.cpu_count())
    ap.add_argument("--ft-bin", default=None)
    ap.add_argument("--baselines", action="store_true", help="also run TF-IDF + LogReg")
    a = ap.parse_args()
    RES.mkdir(exist_ok=True)
    out_path = RES / "results.json"
    results = json.load(open(out_path)) if out_path.exists() else {}
    results["_environment"] = {"platform": platform.platform(), "threads": a.threads,
                               "python": platform.python_version()}

    ft = FastText(a.ft_bin, a.threads)
    names = list(EXPERIMENTS) if a.exp == ["all"] else a.exp
    for n in names:
        r = run_fasttext(n, ft, a.seeds)
        if r:
            results[n] = r
            json.dump(results, open(out_path, "w"), indent=2)
    if a.baselines:
        for ds in BASELINES:
            if a.exp != ["all"] and not any(EXPERIMENTS[n][0] == ds for n in names):
                continue
            r = run_baseline(ds)
            if r:
                results[f"{ds}_tfidf_lr"] = r
                json.dump(results, open(out_path, "w"), indent=2)
    print(f"saved {out_path}")


if __name__ == "__main__":
    main()
