"""
preprocess.py - turn raw datasets into fastText's `__label__X text` format.

normalize_text() reproduces the authors' own preprocessing from
classification-results.sh in the official repo (lowercase, split punctuation,
drop quotes/semicolons/colons), so new datasets are treated exactly like AG News.

Usage:
    python src/preprocess.py ag_news      # data/raw/ag_train.csv, ag_test.csv
    python src/preprocess.py 20ng         # data/raw/newsgroups.json
    python src/preprocess.py uci          # data/raw/newsCorpora.csv (download from UCI)
    python src/preprocess.py all
"""
import csv
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
SEED = 42


def normalize_text(text):
    """Python port of normalize_text() in fastText's classification-results.sh."""
    t = text.lower()
    t = t.replace("'", " ' ").replace('"', "")
    t = t.replace(".", " . ").replace("<br />", " ").replace(",", " , ")
    t = t.replace("(", " ( ").replace(")", " ) ").replace("!", " ! ").replace("?", " ? ")
    t = t.replace(";", " ").replace(":", " ")
    return re.sub(r"\s+", " ", t).strip()


def write_ft(rows, path):
    """rows: list of (label, text)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    rows = rows[:]
    rng.shuffle(rows)  # the authors shuffle too (myshuf)
    with open(path, "w", encoding="utf-8") as f:
        for label, text in rows:
            f.write(f"__label__{label} {normalize_text(text)}\n")
    return len(rows)


def stratified_split(rows, test_frac=0.2):
    by_label = defaultdict(list)
    for r in rows:
        by_label[r[0]].append(r)
    rng = random.Random(SEED)
    train, test = [], []
    for label in sorted(by_label):
        items = by_label[label]
        rng.shuffle(items)
        k = round(len(items) * test_frac)
        test += items[:k]
        train += items[k:]
    return train, test


def report(name, train, test):
    c = Counter(l for l, _ in train)
    lens = [len(normalize_text(t).split()) for _, t in train]
    print(f"{name}: train={len(train)} test={len(test)} classes={len(c)} "
          f"avg_tokens={sum(lens) / len(lens):.1f}")
    return {"train": len(train), "test": len(test), "classes": len(c),
            "avg_tokens": round(sum(lens) / len(lens), 1),
            "min_class": min(c.values()), "max_class": max(c.values())}


# ------------------------------------------------------------------ datasets
def ag_news():
    def read(p):
        with open(p, encoding="utf-8") as f:
            # leading ", " mirrors the authors' sed output: "__label__3 , title , desc"
            return [(r[0], ", " + ", ".join(r[1:])) for r in csv.reader(f)]
    train, test = read(RAW / "ag_train.csv"), read(RAW / "ag_test.csv")
    write_ft(train, OUT / "ag_news.train")
    write_ft(test, OUT / "ag_news.test")
    return report("ag_news", train, test)


def twenty_ng():
    """20 Newsgroups (bydate training portion, 11,314 posts).
    Headers, signatures and quoted replies are removed - otherwise the
    'Newsgroups:'/email lines leak the label."""
    from sklearn.datasets._twenty_newsgroups import (
        strip_newsgroup_footer, strip_newsgroup_header, strip_newsgroup_quoting)
    d = json.load(open(RAW / "newsgroups.json", encoding="utf-8"))
    rows = []
    for k, text in d["content"].items():
        t = strip_newsgroup_quoting(strip_newsgroup_footer(strip_newsgroup_header(text)))
        if len(t.split()) >= 3:
            rows.append((d["target_names"][k].replace(".", "_"), t))
    train, test = stratified_split(rows)
    write_ft(train, OUT / "20ng.train")
    write_ft(test, OUT / "20ng.test")
    return report("20ng", train, test)


def uci():
    """UCI News Aggregator (newsCorpora.csv, tab-separated, headline only).
    Download: https://archive.ics.uci.edu/dataset/359/news+aggregator"""
    path = RAW / "newsCorpora.csv"
    if not path.exists():
        print("uci: data/raw/newsCorpora.csv not found - download it from UCI first")
        return None
    names = {"b": "business", "t": "scitech", "e": "entertainment", "m": "health"}
    rows, seen = [], set()
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 5 or p[4] not in names:
                continue
            key = p[1].strip().lower()
            if key in seen:  # many headlines are syndicated duplicates
                continue
            seen.add(key)
            rows.append((names[p[4]], p[1]))
    train, test = stratified_split(rows)
    write_ft(train, OUT / "uci.train")
    write_ft(test, OUT / "uci.test")
    return report("uci", train, test)


def rss2026():
    """Our newly constructed 2026 headline dataset (src/collect_rss.py output).
    Labels use AG News ids (1 World, 2 Sports, 3 Business, 4 Sci/Tech), so a model
    trained on AG News can be tested on it directly (temporal-shift test)."""
    path = ROOT / "data" / "rss_2026_master.csv"
    if not path.exists():
        print("rss2026: data/rss_2026_master.csv not found - run src/collect_rss.py collect")
        return None
    with open(path, newline="", encoding="utf-8") as f:
        rows = [(r["label"], ", " + r["title"] + ", " + r["description"])
                for r in csv.DictReader(f) if r["conflict"] != "1"]
    write_ft(rows, OUT / "rss2026.all")      # whole set: AG News -> 2026 transfer test
    train, test = stratified_split(rows)
    write_ft(train, OUT / "rss2026.train")   # in-domain split (small for now)
    write_ft(test, OUT / "rss2026.test")
    return report("rss2026", train, test)


DATASETS = {"ag_news": ag_news, "20ng": twenty_ng, "uci": uci, "rss2026": rss2026}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    names = DATASETS if which == "all" else [which]
    stats = {n: DATASETS[n]() for n in names}
    OUT.mkdir(parents=True, exist_ok=True)
    old = {}
    sp = OUT / "dataset_stats.json"
    if sp.exists():
        old = json.load(open(sp))
    old.update({k: v for k, v in stats.items() if v})
    json.dump(old, open(sp, "w"), indent=2)
