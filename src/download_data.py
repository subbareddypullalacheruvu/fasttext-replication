"""
download_data.py - fetch the raw datasets into data/raw/ (not stored in the repo).

    python src/download_data.py

AG News     Zhang et al. (2015) classification CSVs, from a public GitHub mirror of
            the original ag_news_csv release (120,000 train / 7,600 test).
20NG        20 Newsgroups "bydate" training portion (11,314 posts) as one JSON file
            (keys: content, target, target_names), from a public GitHub mirror.
UCI         News Aggregator (newsCorpora.csv) is not fetched automatically; download
            it by hand from https://archive.ics.uci.edu/dataset/359/news+aggregator
            and put newsCorpora.csv in data/raw/ if you want to run `preprocess.py uci`.

The 2026 RSS headlines are already in data/rss_2026_master.csv.
"""
import hashlib
import urllib.request
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"

FILES = {
    "ag_train.csv": "https://raw.githubusercontent.com/mhjabreel/CharCnn_Keras/master/data/ag_news_csv/train.csv",
    "ag_test.csv": "https://raw.githubusercontent.com/mhjabreel/CharCnn_Keras/master/data/ag_news_csv/test.csv",
    "newsgroups.json": "https://raw.githubusercontent.com/selva86/datasets/master/newsgroups.json",
}

# expected line counts, so a broken or different mirror is noticed straight away
EXPECTED_LINES = {"ag_train.csv": 120000, "ag_test.csv": 7600}


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    for name, url in FILES.items():
        dest = RAW / name
        if dest.exists():
            print(f"{name}: already present, skipping")
            continue
        print(f"{name}: downloading {url}")
        urllib.request.urlretrieve(url, dest)
        digest = hashlib.sha256(dest.read_bytes()).hexdigest()[:16]
        print(f"  saved {dest.stat().st_size:,} bytes  sha256={digest}...")
        if name in EXPECTED_LINES:
            n = sum(1 for _ in open(dest, encoding="utf-8"))
            status = "OK" if n == EXPECTED_LINES[name] else f"UNEXPECTED (want {EXPECTED_LINES[name]})"
            print(f"  {n:,} rows - {status}")
    print("Done. Next: python src/preprocess.py all")


if __name__ == "__main__":
    main()
