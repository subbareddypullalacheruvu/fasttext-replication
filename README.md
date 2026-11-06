# Replicating fastText (Joulin et al., 2017) on AG News and new data

COMP8240 (Applications of Data Science), Macquarie University, Session 2 2026.
Author: Subbareddy Pullalacheruvu (48641626).

This repository reproduces the AG News result of *Bag of Tricks for Efficient Text
Classification* (Joulin et al., EACL 2017) with the authors' own fastText code, and then
tests whether its speed-versus-accuracy claim holds on data the paper never used:

1. **20 Newsgroups**, an existing dataset with 20 classes and long documents, and
2. **2026 RSS headlines**, a new dataset I built with the same four classes and format as
   AG News, collected about twenty years after it.

Results are in [`results/RESULTS.md`](results/RESULTS.md). The final report is
[`report/final_report.pdf`](report/final_report.pdf).

## Setup

You need **Python 3.11**. `fasttext-wheel==0.9.2` (the authors' last release) has no
prebuilt wheels for Python 3.12+ and fails to build on 3.13.

```bash
python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

On Windows, building `fasttext-wheel` needs the *Microsoft C++ Build Tools*. `numpy<2` is
pinned because fastText 0.9.2's Python binding breaks with NumPy 2.

## Reproduce everything

Run these from the repository root. On a laptop CPU the whole pipeline takes about 15 minutes.

```bash
python src/download_data.py               # AG News + 20 Newsgroups -> data/raw/
python src/preprocess.py all              # -> data/processed/*.train / *.test / *.all
python src/run_experiments.py --seeds 5 --threads 2 --baselines   # Table: AG News, 20NG, 2026 in-domain
python src/epoch_sweep.py --dataset 20ng --seeds 5                # why the paper's settings fail on 20NG
python src/dim_sweep.py --seeds 5                                 # is the small hidden layer the cause? (no)
python src/transfer_test.py --seeds 5                             # train on AG News, test on 2026 headlines
python src/error_analysis.py ag_news_bigram                       # error examples -> results/errors_*.md
python src/error_analysis.py 20ng_epoch25
python src/error_analysis.py agnews_to_rss2026
python src/make_figures.py                                        # -> results/figures/
```

All runs append to `results/results.json`. fastText uses seeds 0 to 4 and 2 threads, and
results are the mean ± standard deviation over the 5 runs.
fastText trains with several threads (Hogwild SGD), so a run is **not bit-identical** even
with a fixed seed. Expect differences of a few tenths of a point. For this reason the exact
predictions that the LLM judge assessed are frozen in
`results/llm_judge/judged_predictions_seed0.tsv`, and rerunning `transfer_test.py` does not
change the judge results.

## The 2026 RSS headline dataset

| File | What it is |
|---|---|
| `data/rss_2026_master.csv` | All 548 collected items (id, source, section, label, title, lead sentence, link, publication and collection time, `conflict` flag) |
| `data/labelling_guideline.md` | The rules each label is checked against |
| `data/spotcheck_sample.csv` | The 50-item manual spot-check (45/50 = 90% agreement) |
| `results/llm_judge/` | LLM-as-judge prompt, verdicts on the transfer-test errors, and a human check of 30 of them |

**Known data issues, kept in the frozen version:** 93 of the 508 leads (84 Guardian) are cut
mid-sentence by the feed. 20 Guardian leads contain sign-up text ("Get our breaking news
email..."). 4 items are promotions with no real headline (ids 112, 183, 233, 280).

Each item is a headline plus its lead sentence from one of 15 public RSS section feeds
(BBC, The Guardian, The New York Times, ESPN), collected on 9 October 2026. Its label is the
outlet's own section, mapped to World, Sports, Business or Sci/Tech. The 40 stories that
appeared under two different sections are flagged `conflict=1` and left out, which leaves
508 usable items. The dataset is frozen at this version for the report.

```bash
python src/collect_rss.py collect     # fetch feeds again, appending only new items
python src/collect_rss.py stats       # counts per class / source / collection run
python src/collect_rss.py sample -n 50   # new spot-check sheet
```

**Copyright note.** Headlines and lead sentences belong to the publishers. They are
included here only for non-commercial research and teaching, to make the results
reproducible. Each row keeps its source link. See the ethics section of the report.

## Repository layout

```
src/
  download_data.py     fetch raw datasets
  preprocess.py        Python port of the authors' normalize_text; writes fastText format
  run_experiments.py   fastText + TF-IDF/LogReg baseline, multi-seed, timing
  epoch_sweep.py       epochs x learning-rate sweep (20NG)
  dim_sweep.py         hidden-size (dim) check on 20NG
  transfer_test.py     AG News -> 2026 headlines temporal-shift test
  error_analysis.py    misclassified examples per class pair
  make_figures.py      figures for the report
  collect_rss.py       builds the 2026 dataset from RSS feeds
data/                  new dataset, guideline, spot-check (raw downloads are git-ignored)
results/               results.json, RESULTS.md, predictions, error lists, figures
results/archive/       earlier Windows runs (9 Oct 2026), kept for provenance
report/                LaTeX source and PDF of the final report
```

## Source

Official code: <https://github.com/facebookresearch/fastText> (archived March 2024, v0.9.2).
Paper: <https://aclanthology.org/E17-2068/>.
