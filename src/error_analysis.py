"""
error_analysis.py - confusion matrix and real misclassified examples from a
saved prediction file (results/pred_<experiment>.tsv).

    python src/error_analysis.py ag_news_bigram
"""
import csv
import random
import sys
from collections import Counter

from run_experiments import RES

NAMES = {"1": "World", "2": "Sports", "3": "Business", "4": "Sci/Tech"}

exp = sys.argv[1] if len(sys.argv) > 1 else "ag_news_bigram"
rows = list(csv.DictReader(open(RES / f"pred_{exp}.tsv", encoding="utf-8"),
                           delimiter="\t", quoting=csv.QUOTE_NONE))
labels = sorted({r["gold"] for r in rows})
name = lambda l: NAMES.get(l, l)  # 20 Newsgroups labels are already names

cm = Counter((r["gold"], r["pred"]) for r in rows)
out = [f"# Error analysis: {exp}\n",
       f"Test items: {len(rows)}; errors: {sum(r['gold'] != r['pred'] for r in rows)}\n",
       "## Confusion matrix (rows = true, columns = predicted)\n",
       "| true \\ pred | " + " | ".join(name(l) for l in labels) + " | recall |",
       "|---" * (len(labels) + 2) + "|"]
for g in labels:
    tot = sum(cm[(g, p)] for p in labels)
    out.append(f"| **{name(g)}** | " + " | ".join(str(cm[(g, p)]) for p in labels)
               + f" | {100 * cm[(g, g)] / tot:.1f}% |")

errors = [r for r in rows if r["gold"] != r["pred"]]
pairs = Counter((r["gold"], r["pred"]) for r in errors).most_common(3)
random.seed(0)
out.append("\n## Examples from the three most common confusions\n")
for (g, p), n in pairs:
    out.append(f"### {name(g)} predicted as {name(p)} ({n} cases)\n")
    cases = [e for e in errors if (e["gold"], e["pred"]) == (g, p)]
    for r in random.sample(cases, min(4, len(cases))):
        text = r["text"].strip(" ,")
        out.append(f"- {text[:160]}{'…' if len(text) > 160 else ''}")
    out.append("")

(RES / f"errors_{exp}.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
