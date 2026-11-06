"""
llm_judge_agreement.py - summarise the LLM-as-judge verdicts and, once the human check
sheet is filled in, measure agreement between the human and the LLM judge.

    python src/llm_judge_agreement.py

Inputs (results/llm_judge/):
  verdicts.csv     one row per misclassified 2026 item: id, gold, pred, verdict, judge_label, reason
  human_check.csv  30 of those rows; fill the `human_verdict` column with
                   MODEL_ERROR / AMBIGUOUS / LABEL_NOISE (the LLM verdict is in `llm_verdict`)
"""
import csv
import json
from collections import Counter

from run_experiments import RES

J = RES / "llm_judge"
VERDICTS = ["MODEL_ERROR", "AMBIGUOUS", "LABEL_NOISE"]


def cohen_kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(a) | set(b)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main():
    rows = list(csv.DictReader(open(J / "verdicts.csv", encoding="utf-8")))
    n = len(rows)
    counts = Counter(r["verdict"] for r in rows)
    summary = {"n_errors_judged": n,
               "verdicts": {v: counts[v] for v in VERDICTS},
               "verdict_pct": {v: round(100 * counts[v] / n, 1) for v in VERDICTS}}
    by_pair = Counter((r["gold"], r["pred"], r["verdict"]) for r in rows)
    summary["by_confusion"] = [
        {"gold": g, "pred": p, "verdict": v, "n": k} for (g, p, v), k in by_pair.most_common()]

    hc = list(csv.DictReader(open(J / "human_check.csv", encoding="utf-8")))
    done = [r for r in hc if r["human_verdict"].strip()]
    if done:
        h = [r["human_verdict"].strip().upper() for r in done]
        l = [r["llm_verdict"] for r in done]
        summary["human_check"] = {
            "n": len(done),
            "raw_agreement_pct": round(100 * sum(x == y for x, y in zip(h, l)) / len(done), 1),
            "cohen_kappa": round(cohen_kappa(h, l), 3),
            # coarser question: is the error the model's fault, or the data's?
            "binary_agreement_pct": round(100 * sum((x == "MODEL_ERROR") == (y == "MODEL_ERROR")
                                                    for x, y in zip(h, l)) / len(done), 1),
        }
    else:
        summary["human_check"] = "not filled in yet: complete human_verdict in human_check.csv"

    json.dump(summary, open(J / "summary.json", "w"), indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
