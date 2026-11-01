#!/usr/bin/env python3
"""
collect_rss.py - Build a 2026 news-headline dataset in AG News format
(COMP8240 project: replicating fastText, Joulin et al. 2017).

Each item = headline + lead sentence, labelled into the four AG News classes
using the RSS feed's own section:
    1 = World, 2 = Sports, 3 = Business, 4 = Sci/Tech

Usage:
    python collect_rss.py collect          # fetch all feeds, append NEW items only
    python collect_rss.py stats            # counts per class / source / collection run
    python collect_rss.py sample -n 50     # random sample sheet for manual spot-checking
    python collect_rss.py export           # write fastText-format training file

Run `collect` several times (e.g. now, this evening, and every few days after):
duplicates are skipped automatically, so the dataset grows across the news cycle.

Requires: pip install feedparser
"""
import argparse
import csv
import html
import os
import random
import re
import sys
from collections import Counter
from datetime import datetime, timezone

try:
    import feedparser
except ImportError:
    sys.exit("feedparser is missing - run:  pip install feedparser")

DATA_DIR = "data"
MASTER = os.path.join(DATA_DIR, "rss_2026_master.csv")
FASTTEXT_OUT = os.path.join(DATA_DIR, "rss_2026.fasttext.txt")
SPOTCHECK = os.path.join(DATA_DIR, "spotcheck_sample.csv")
USER_AGENT = "COMP8240-student-project/1.0 (academic research)"

LABEL_NAMES = {1: "World", 2: "Sports", 3: "Business", 4: "Sci/Tech"}

# (source, section, feed URL, AG News label)
# Mapping rule: the outlet's own section decides the label.
FEEDS = [
    # --- World ---
    ("BBC", "world", "https://feeds.bbci.co.uk/news/world/rss.xml", 1),
    ("Guardian", "world", "https://www.theguardian.com/world/rss", 1),
    ("NYT", "world", "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", 1),
    # --- Sports ---
    ("BBC", "sport", "https://feeds.bbci.co.uk/sport/rss.xml", 2),
    ("Guardian", "sport", "https://www.theguardian.com/sport/rss", 2),
    # NYT's Sports feed returned no items on 2026-10-09, so ESPN replaces it
    ("ESPN", "news", "https://www.espn.com/espn/rss/news", 2),
    # --- Business ---
    ("BBC", "business", "https://feeds.bbci.co.uk/news/business/rss.xml", 3),
    ("Guardian", "business", "https://www.theguardian.com/business/rss", 3),
    ("NYT", "business", "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml", 3),
    # --- Sci/Tech ---
    ("BBC", "technology", "https://feeds.bbci.co.uk/news/technology/rss.xml", 4),
    ("BBC", "science", "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml", 4),
    ("Guardian", "technology", "https://www.theguardian.com/technology/rss", 4),
    ("Guardian", "science", "https://www.theguardian.com/science/rss", 4),
    ("NYT", "technology", "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", 4),
    ("NYT", "science", "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml", 4),
]

FIELDS = ["id", "source", "section", "label", "label_name", "title", "description",
          "link", "published", "collected_at", "conflict"]

MIN_WORDS = 3  # drop items whose headline+lead is shorter than this


# ---------------------------------------------------------------- cleaning
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def clean(text):
    """Strip HTML tags/entities and boilerplate, collapse whitespace."""
    if not text:
        return ""
    text = html.unescape(TAG_RE.sub(" ", text))
    text = re.sub(r"Continue reading\.*", " ", text, flags=re.I)  # Guardian boilerplate
    return WS_RE.sub(" ", text).strip()


def lead_sentence(text):
    """Keep only the first sentence, to match AG News's short lead text."""
    first = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0]
    return first[:300]


def norm_title(title):
    return re.sub(r"[^a-z0-9 ]", "", title.lower()).strip()


# ---------------------------------------------------------------- storage
def load_master():
    if not os.path.exists(MASTER):
        return []
    with open(MASTER, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_master(rows):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(MASTER, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


# ---------------------------------------------------------------- commands
def collect(_args):
    rows = load_master()
    by_link = {r["link"]: r for r in rows if r["link"]}
    by_title = {norm_title(r["title"]): r for r in rows}
    next_id = max((int(r["id"]) for r in rows), default=0) + 1
    run_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    added = Counter()
    dup_skipped = too_short = new_conflicts = 0
    failed = []

    for source, section, url, label in FEEDS:
        feed = feedparser.parse(url, agent=USER_AGENT)
        if not feed.entries:
            failed.append(f"{source}/{section}")
            continue
        for e in feed.entries:
            title = clean(e.get("title", ""))
            desc = lead_sentence(clean(e.get("summary", "")))
            link = e.get("link", "")
            if len((title + " " + desc).split()) < MIN_WORDS:
                too_short += 1
                continue

            existing = by_link.get(link) or by_title.get(norm_title(title))
            if existing:
                # Same story under a different section = ambiguous label
                if existing["label"] != str(label) and existing["conflict"] != "1":
                    existing["conflict"] = "1"
                    new_conflicts += 1
                dup_skipped += 1
                continue

            row = {
                "id": next_id, "source": source, "section": section,
                "label": label, "label_name": LABEL_NAMES[label],
                "title": title, "description": desc, "link": link,
                "published": e.get("published", ""), "collected_at": run_time,
                "conflict": "0",
            }
            rows.append(row)
            by_link[link] = row
            by_title[norm_title(title)] = row
            next_id += 1
            added[label] += 1

    save_master(rows)
    print(f"Collection run: {run_time}")
    for lab, name in LABEL_NAMES.items():
        print(f"  +{added[lab]:4d} new  {name}")
    print(f"  Duplicates skipped: {dup_skipped}   too short: {too_short}   "
          f"new label conflicts: {new_conflicts}")
    if failed:
        print(f"  WARNING - feeds returned nothing: {', '.join(failed)}")
    print(f"Total rows in {MASTER}: {len(rows)}")


def stats(_args):
    rows = load_master()
    if not rows:
        sys.exit("No data yet - run:  python collect_rss.py collect")
    usable = [r for r in rows if r["conflict"] != "1"]
    print(f"Total collected: {len(rows)}   usable (no label conflict): {len(usable)}   "
          f"conflicts: {len(rows) - len(usable)}\n")

    print("Per class (usable):")
    c = Counter(r["label_name"] for r in usable)
    for name in LABEL_NAMES.values():
        print(f"  {name:10s} {c[name]:6d}  ({100 * c[name] / len(usable):.1f}%)")

    print("\nPer source x class (usable):")
    sources = sorted({r["source"] for r in usable})
    print("  " + "Source".ljust(10) + "".join(n.rjust(10) for n in LABEL_NAMES.values()))
    for s in sources:
        cs = Counter(r["label_name"] for r in usable if r["source"] == s)
        print("  " + s.ljust(10) + "".join(str(cs[n]).rjust(10) for n in LABEL_NAMES.values()))

    print("\nCollection runs:")
    for run, n in sorted(Counter(r["collected_at"] for r in rows).items()):
        print(f"  {run}: {n} new items")

    lens = [len((r["title"] + " " + r["description"]).split()) for r in usable]
    print(f"\nAvg words per item: {sum(lens) / len(lens):.1f}  (min {min(lens)}, max {max(lens)})")


def sample(args):
    rows = [r for r in load_master() if r["conflict"] != "1"]
    if not rows:
        sys.exit("No data yet - run:  python collect_rss.py collect")
    random.seed(args.seed)
    picked = random.sample(rows, min(args.n, len(rows)))
    with open(SPOTCHECK, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "source", "title", "description", "auto_label",
                    "correct (Y/N)", "your_label_if_N", "notes"])
        for r in picked:
            w.writerow([r["id"], r["source"], r["title"], r["description"],
                        r["label_name"], "", "", ""])
    print(f"Wrote {len(picked)} items to {SPOTCHECK} - fill in the 'correct' column by hand.")


PUNCT_RE = re.compile(r"([.,!?:;()\"'])")


def ft_normalise(text):
    """Same spirit as fastText's AG News preprocessing: lowercase, split punctuation."""
    text = PUNCT_RE.sub(r" \1 ", text.lower())
    return WS_RE.sub(" ", text).strip()


def export(_args):
    rows = [r for r in load_master() if r["conflict"] != "1"]
    if not rows:
        sys.exit("No data yet - run:  python collect_rss.py collect")
    with open(FASTTEXT_OUT, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(f"__label__{r['label']} {ft_normalise(r['title'] + ' ' + r['description'])}\n")
    print(f"Wrote {len(rows)} lines to {FASTTEXT_OUT}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("collect").set_defaults(func=collect)
    sub.add_parser("stats").set_defaults(func=stats)
    sp = sub.add_parser("sample")
    sp.add_argument("-n", type=int, default=50)
    sp.add_argument("--seed", type=int, default=42)
    sp.set_defaults(func=sample)
    sub.add_parser("export").set_defaults(func=export)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
