# Results so far (9 October 2026)

All numbers below were produced on my own PC (Windows, Python 3.11, `fasttext-wheel` 0.9.2,
the authors' fastText code) using the scripts in `src/`. fastText results are averaged over
3 runs (seeds 0–2); training time is wall-clock training time on the same machine for every
model. Raw numbers: `results.json`. Figures: `figures/`.

## Phase 1 – replication on AG News

Settings exactly as in the authors' `classification-results.sh`:
`dim=10 lr=0.25 wordNgrams=2 minCount=1 bucket=10M epoch=5`. Preprocessing follows the
authors' own `normalize_text` step, so the input matches the original pipeline.

| Model | Paper | Mine | Train time |
|---|---|---|---|
| fastText (+ bigrams), run A, 3 seeds | 92.5% | 92.43 / 92.32 / 92.37 → **92.37%** | ~5 s |
| fastText (+ bigrams), run B, 3 seeds | 92.5% | 92.36 / 92.12 / 92.28 → **92.25%** | ~4 s |
| fastText (+ bigrams), run C, 3 seeds | 92.5% | 92.46 / 92.21 / 92.39 → **92.35%** | ~4 s |
| TF-IDF (1–2 grams) + logistic regression | – | **92.50%** | 81.9 s |

* Over all 9 runs the mean is **92.33%**, within 0.2 pp of the paper. Run-to-run spread
  (92.12–92.46) is larger than the remaining gap, so the result replicates.
* The efficiency claim holds on AG News: the comparison model reaches the same accuracy
  but takes about **20× longer** to train.
* Error analysis (`errors_ag_news_bigram.md`): most errors are Business ↔ Sci/Tech
  confusions. Several look like label noise in AG News itself (e.g. a Tata Consultancy
  share listing labelled *World*).

## Phase 2a – 20 Newsgroups (existing dataset not used in the paper)

10,959 posts after removing headers, signatures and quoted replies (which otherwise leak the
label); 20 classes; stratified 80/20 split (seed 42); ~262 tokens per post vs ~45 for AG News.

| Model | Accuracy | Train time |
|---|---|---|
| fastText, paper's AG News settings (5 epochs) | 16.89 / 16.44 / 16.35 → **16.56%** | ~3 s |
| fastText, 25 epochs | 62.42 / 62.24 / 61.83 → **62.16%** | ~6 s |
| fastText, best in sweep (lr 0.25, 100 epochs) | **66.12%** | 53 s |
| TF-IDF + logistic regression | **76.53%** | 103.3 s |

* **The paper's configuration does not transfer.** With ~9k training documents (13× fewer
  than AG News), 5 epochs is far too few updates and the model barely learns.
* Even after tuning epochs and learning rate (`20ng_epoch_sweep.json`), fastText plateaus
  around **66%**, about **10 pp below** the comparison model. The speed advantage remains,
  but "comparable accuracy" no longer holds on long, small, 20-class data.

## Phase 2b – new dataset: 2026 RSS headlines (constructed by me)

Collector: `src/collect_rss.py`. Labelling rules: `data/labelling_guideline.md`.

**Collection**
* 15 section feeds from BBC, The Guardian, NYT and ESPN, mapped to the four AG News
  classes by the outlet's own section label.
* Run 1 (9 Oct 2026, 01:59 UTC): 505 new items. Run 2 (03:18 UTC): 43 new items.
* NYT Sports returned no items and was replaced by ESPN.

**Preprocessing**
* HTML and boilerplate removed; lead text cut to the first sentence (AG News style);
  duplicates removed by link and normalised headline (554 skipped in run 2).
* **40 stories appeared under two different sections** (e.g. World *and* Business) and are
  excluded as ambiguous → **548 collected, 508 usable**.
* Class balance (usable): World 127 (25.0%), Sports 135 (26.6%), Business 106 (20.9%),
  Sci/Tech 140 (27.6%). Average 37.3 words per item.

**Annotation (manual spot-check)**
* 50 randomly sampled items checked by hand against the guideline: **45/50 = 90% agreement**,
  above the 85% threshold, so the feed-to-label mapping is kept.
* Disagreements are boundary cases: politics about technology (e.g. AI regulation) labelled
  Sci/Tech, arts/culture stories that fit no AG News class, and one broken item with no
  real headline.

**Known issues to fix**
* Guardian descriptions often run past the first sentence (their summaries lack sentence
  breaks), so they are longer than AG News leads.
* Excel shows mis-encoded characters (e.g. `â€™`) when opening the CSV directly; the stored
  data is correct UTF-8.

**Next steps**
* Keep collecting over the coming weeks (target: a few thousand items per class).
* Temporal-shift test: train on 2004-era AG News, test on 2026 headlines (`src/transfer_test.py`).
* UCI News Aggregator as a second existing dataset (`src/preprocess.py uci`, needs `newsCorpora.csv`).
