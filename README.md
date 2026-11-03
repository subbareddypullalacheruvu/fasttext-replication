# Reproducing fastText: does the efficiency–accuracy trade-off generalise?

COMP8240 (Applications of Data Science), Macquarie University, Session 2 2026 – novel project.
Subbareddy Pullalacheruvu (48641626).

**Paper:** Joulin, Grave, Bojanowski & Mikolov (2017). *Bag of Tricks for Efficient Text
Classification.* EACL 2017 (CORE A). [ACL Anthology](https://aclanthology.org/E17-2068/) ·
[arXiv](https://arxiv.org/abs/1607.01759)
**Code:** official [facebookresearch/fastText](https://github.com/facebookresearch/fastText)
v0.9.2 (archived March 2024).
**Original data:** AG News (Zhang et al., 2015).

## Status (project update, October 2026)

| Stage | Status |
|---|---|
| Replicate AG News with the authors' code and settings | ✅ done – 92.33% (9 runs) vs 92.5% in the paper |
| Existing dataset not used in the paper: 20 Newsgroups | ✅ first results |
| Comparison model (TF-IDF + logistic regression) | ✅ AG News, 20 Newsgroups |
| New constructed dataset: 2026 RSS news headlines | 🔄 548 collected, 508 usable, 90% label agreement; collection ongoing |
| Existing dataset: UCI News Aggregator | ⏳ preprocessing ready, needs `newsCorpora.csv` |
| Temporal-shift test (train on AG News, test on 2026 headlines) | ⏳ script ready (`src/transfer_test.py`) |

Full numbers and discussion: [`results/RESULTS.md`](results/RESULTS.md).

## Repository layout

```
src/
  collect_rss.py      collects the 2026 headline dataset from 15 public RSS feeds
  preprocess.py       raw data -> fastText format, using the authors' normalize_text rules
  run_experiments.py  fastText + TF-IDF baseline over several seeds; accuracy AND train time
  epoch_sweep.py      sensitivity of 20 Newsgroups to epochs / learning rate
  transfer_test.py    train on AG News (2004), test on 2026 headlines
  error_analysis.py   confusion matrix + real misclassified examples
  make_figures.py     figures in results/figures/
data/
  rss_2026_master.csv     the new dataset: one row per headline, with source, section,
                          link and collection timestamp
  spotcheck_sample.csv    50-item manual label check (Y/N column)
  labelling_guideline.md  category rules used for the manual check
  processed/              dataset statistics (fastText-format files are not committed)
results/                  results.json, prediction files, error analyses, figures
```

`data/raw/` (AG News, 20 Newsgroups) is not committed because these are large public
datasets – see below for where to get them.

## How to reproduce

```bash
pip install -r requirements.txt

# 1. data – save into data/raw/
#    AG News -> ag_train.csv, ag_test.csv
#      https://github.com/mhjabreel/CharCnn_Keras/tree/master/data/ag_news_csv
#    20 Newsgroups (bydate training portion, 11,314 posts) -> newsgroups.json
#      https://raw.githubusercontent.com/selva86/datasets/master/newsgroups.json
#    UCI News Aggregator -> newsCorpora.csv
#      https://archive.ics.uci.edu/dataset/359/news+aggregator
python src/collect_rss.py collect        # repeat over several days; duplicates are skipped
python src/collect_rss.py stats
python src/preprocess.py all

# 2. experiments
python src/run_experiments.py --exp ag_news_bigram 20ng_paper_cfg 20ng_epoch25 --seeds 3 --baselines
python src/epoch_sweep.py --dataset 20ng
python src/transfer_test.py
python src/error_analysis.py ag_news_bigram
python src/make_figures.py
```

## Environment

Windows 11 · Python 3.11 · `fasttext-wheel` 0.9.2 (Python bindings for the official
fastText C++ code) · CPU only. Setting up on Windows required installing the Microsoft C++
build tools and pinning `numpy<2` for compatibility with the 0.9.2 bindings.
