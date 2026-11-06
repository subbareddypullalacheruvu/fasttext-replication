# Results (final batch, 2 November 2026)

Every number in this file and in the report comes from `results.json`,
`20ng_epoch_sweep.json` and `llm_judge/summary.json`. Everything was generated in one batch
with the same versions: Python 3.11, `fasttext-wheel` 0.9.2 (the authors' release),
NumPy 1.26, Linux, 2 threads.

fastText results are the mean ± standard deviation over 5 seeds (0–4). Training time is
wall-clock training time only, measured on the same machine for every model. Earlier
Windows runs from 9 October 2026 are kept in `archive/` and agree to within 0.1 pp. The
report's numbers come from `report/make_numbers.py`, so they always match these files.

## Phase 1 – replication on AG News

Settings exactly as in the authors' `classification-results.sh`:
`dim=10 lr=0.25 wordNgrams=2 minCount=1 bucket=10M epoch=5`, softmax loss. Preprocessing is
a Python port of the authors' `normalize_text`.

| Model | Paper | Mine (5 seeds) | Gap | Train time |
|---|---|---|---|---|
| fastText, unigrams | 91.5% | **91.43 ± 0.05%** | −0.07 pp | 3.2 s |
| fastText, + bigrams | 92.5% | **92.34 ± 0.10%** (range 92.22–92.45) | −0.16 pp | 4.8 s |
| TF-IDF (1–2 grams) + logistic regression | – | 92.58% | – | 71.9 s |

* Both of the paper's numbers replicate to within seed-to-seed variation. The bigram gain
  (+0.9 pp) matches the paper (+1.0 pp).
* The efficiency claim holds: the baseline is no more accurate but takes about 15× longer
  to train.
* Per-class recall: Sports 98.0%, World 92.2%, Sci/Tech 89.8%, Business 89.3%. Most errors
  are Business ↔ Sci/Tech. Some look like label noise in AG News itself, e.g. a Tata
  Consultancy share listing labelled *World* (`errors_ag_news_bigram.md`).

## Phase 2a – 20 Newsgroups (existing dataset, not used in the paper)

10,959 posts after removing headers, signatures and quoted replies, which would otherwise
leak the label. 20 classes, stratified 80/20 split (seed 42), about 262 tokens per post.

| Model | Accuracy | Macro-F1 | Train time |
|---|---|---|---|
| fastText, paper's AG News settings (5 epochs) | 16.41 ± 0.17% | 9.6% | 2.3 s |
| fastText, 25 epochs | 62.17 ± 0.18% | 61.1% | 7.0 s |
| fastText, 25 epochs, hierarchical softmax | 56.97 ± 0.42% | 56.3% | 6.7 s |
| fastText, best in sweep (lr 0.25, 100 epochs) | 66.50 ± 0.39% | – | 20.4 s |
| fastText, lr 1.0, 10 epochs | 65.08 ± 0.17% | – | 2.8 s |
| TF-IDF + logistic regression | **76.53%** | 75.5% | 54.7 s |

* **The paper's configuration does not transfer.** It underfits badly, because there is
  about 14× less training data than AG News.
* After tuning (`20ng_epoch_sweep.json`), fastText plateaus about 10 pp below the baseline.
  Speed survives (65% in 2.8 s, against 76.5% in 54.7 s); accuracy parity does not.
* Hierarchical softmax costs 5 pp and saves almost no time with only 20 classes.

## Phase 2b – new dataset: 2026 RSS headlines

548 items from 15 RSS section feeds (BBC, Guardian, NYT, ESPN), collected on 9 October 2026.
40 items appeared under two sections and are excluded, which leaves **508 usable**
(World 127, Sports 135, Business 106, Sci/Tech 140). A manual spot-check of 50 items
against `data/labelling_guideline.md` found 45/50 = **90% agreement** with the automatic
labels (`data/spotcheck_sample.csv`).

| Train → test | Accuracy |
|---|---|
| AG News → AG News test (in-domain, for reference) | 92.34 ± 0.10% |
| **AG News → 2026 headlines** (all 508) | **74.41 ± 0.50%** |
| 2026 → 2026 (407 train / 101 test), fastText paper settings | 37.22 ± 7.72% |
| 2026 → 2026, TF-IDF + logistic regression | 72.28% |

* A **17.9 pp drop** after twenty years. Recall: World 81.7%, Sports 82.1%,
  Business 59.1%, Sci/Tech 72.0%.
* New confusion appears: Business and Sci/Tech leak into World (about 13% each, against
  3% on AG News), because many 2026 business and technology stories are about government.
* Vocabulary gap: *openai*, *chatgpt* and *deepfake* never occur in AG News training data,
  and NYT's "A.I." is tokenised to `a . i .`.
* `errors_agnews_to_rss2026.md` lists the confusion matrix and example errors.
* The in-domain 2026 numbers come from a 101-item test set, so they are indicative only.

## LLM-as-judge on the 127 transfer-test errors (seed 0)

Protocol, prompt and per-item verdicts with reasons: `llm_judge/`.

| Verdict | Count | Share |
|---|---|---|
| MODEL_ERROR (gold clearly right) | 55 | 43% |
| AMBIGUOUS (both labels defensible) | 37 | 29% |
| LABEL_NOISE (gold wrong / no class fits) | 35 | 28% |

* Seed-0 accuracy is 75.00%. Without the items the judge called label noise it is **80.5%**,
  and also accepting the ambiguous items gives **88.4%**. These are estimates that depend on
  the judge (see the human check below).
* **Human check of the judge** (30 random errors, labelled by me without seeing its verdicts):
  46.7% exact agreement, Cohen's κ = 0.20 (slight to fair), and 63.3% agreement on whether the
  error is the model's fault. In 8 of the 16 disagreements, the judge said the gold label was
  right where I called it label noise, so I was stricter about the feed labels. Either way, a
  large share of errors are not clear model errors (judge 15/30, me 20/30). The exact split
  depends on who judges. Details: `llm_judge/human_check.csv`, `llm_judge/summary.json`.

## UCI News Aggregator

Not run. The preprocessing exists (`preprocess.py uci`), but only two of its four classes
overlap with AG News, so it cannot test transfer. The time went to the LLM-as-judge
analysis instead.
