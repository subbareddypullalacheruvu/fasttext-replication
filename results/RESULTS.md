# Results so far (9 October 2026)

All fastText runs use the official v0.9.2 code, 2 threads, seeds 0–4; mean ± standard
deviation over 5 runs. Training time is wall-clock for training only, on the same machine
for every model. Raw numbers: `results.json`.

## Phase 1 – replication on AG News

Settings exactly as in the authors' `classification-results.sh`:
`dim=10 lr=0.25 wordNgrams=2 minCount=1 bucket=10M epoch=5`, default softmax loss.
Preprocessing is a Python port of the authors' `normalize_text`, checked line-for-line
against their `sed` pipeline.

| Model | Paper | Ours (5 runs) | Gap | Train time |
|---|---|---|---|---|
| fastText, unigrams | 91.5% | **91.47 ± 0.05%** | −0.03 pp | 2.2 s |
| fastText, + bigrams | 92.5% | **92.38 ± 0.07%** | −0.12 pp | 3.5 s |
| TF-IDF (1–2 grams) + logistic regression | – | 92.50% | – | 60.5 s |

* Both paper numbers are reproduced to within about 0.1 pp, and the bigram gain (+0.9 pp)
  also matches (paper: +1.0 pp).
* The efficiency claim holds on AG News: the comparison model reaches the same accuracy
  but takes about 17× longer to train.
* Per-class recall: Sports 97.9%, World 92.2%, Business 89.8%, Sci/Tech 89.7%. Most errors
  are Business ↔ Sci/Tech (259 of 576). Several "errors" look like label noise in AG News
  itself, e.g. a Tata Consultancy share listing labelled *World*, and a Nortel revenue
  warning labelled *Sci/Tech* (see `errors_ag_news_bigram.md`).

## Phase 2a – 20 Newsgroups (not used in the paper)

10,959 posts after removing headers, signatures and quoted replies (which otherwise leak
the label); 20 classes; stratified 80/20 split (seed 42); about 262 tokens per post vs
45 for AG News.

| Model | Accuracy | Macro-F1 | Train time |
|---|---|---|---|
| fastText, paper's AG News settings (5 epochs) | 16.54 ± 0.23% | 9.8% | 2.2 s |
| fastText, 25 epochs | 62.30 ± 0.40% | 61.2% | 5.5 s |
| fastText, 25 epochs, hierarchical softmax | 56.79 ± 0.50% | 56.1% | 5.4 s |
| fastText, best in sweep (lr 0.25, 100 epochs) | 66.59 ± 0.19% | – | 17.9 s |
| TF-IDF + logistic regression | **76.53%** | 75.5% | 50.7 s |

* **The paper's configuration does not transfer.** With about 9k training documents,
  5 epochs is far too few updates and the model barely learns (16.5%). AG News works
  because it has 13× more training examples.
* Even after tuning (`epoch_sweep.json`), fastText plateaus around 66%, about 10 pp
  below the comparison model. On long, small, 20-class data the speed advantage remains
  (3–10× faster) but "comparable accuracy" no longer holds.
* Hierarchical softmax gives **no speed-up** with 20 classes and costs 5.5 pp accuracy. Its
  benefit in the paper comes from tag prediction with hundreds of thousands of labels.

## Phase 2a – UCI News Aggregator

Preprocessing written (`preprocess.py uci`): headline only, classes business /
sci-tech / entertainment / health, duplicate syndicated headlines removed, stratified
80/20 split. Waiting on `newsCorpora.csv` download. Only two classes overlap with AG News,
so this dataset tests in-domain training, not transfer from AG News.

## Phase 2b – new dataset: 2026 RSS headlines

See `../data/labelling_guideline.md` and `../src/collect_rss.py`.

* **Sources:** 15 section feeds from BBC, The Guardian, NYT and ESPN, mapped to the four
  AG News classes by the outlet's own section label.
* **Collection run 1 (9 Oct 2026, 01:59 UTC):** 505 headlines (World 138, Sports 98,
  Business 118, Sci/Tech 151); 52 duplicates skipped; **40 stories appeared under two
  different sections** and are excluded as ambiguous labels. NYT Sports returned no items
  and was replaced by ESPN.
* **Preprocessing:** HTML and boilerplate removed, lead text cut to the first sentence (AG News
  style), de-duplication by link and normalised headline, and the authors' `normalize_text`.
* **Next:** repeated collection over the coming weeks (target a few thousand per class),
  50-item manual spot-check against the guideline, and the temporal-shift test (train on
  2004-era AG News, test on 2026 headlines) with `transfer_test.py`.
