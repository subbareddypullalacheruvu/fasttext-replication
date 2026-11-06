"""make_figures.py - figures for the update presentation / report (results/figures/)."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from run_experiments import RES

BLUE, ORANGE, GRAY = "#2a78d6", "#eb6834", "#8a8984"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e6e5e0"
plt.rcParams.update({"font.size": 11, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.facecolor": "#fcfcfb",
                     "axes.facecolor": "#fcfcfb"})
OUT = RES / "figures"
OUT.mkdir(parents=True, exist_ok=True)
R = json.load(open(RES / "results.json"))

# ---- Figure 1: accuracy vs training time, fastText vs TF-IDF baseline
pairs = [("AG News", "ag_news_bigram", "ag_news_tfidf_lr"),
         ("20 Newsgroups", "20ng_epoch25", "20ng_tfidf_lr")]
pairs += [(lbl, f, b) for lbl, f, b in [("UCI News", "uci_paper_cfg", "uci_tfidf_lr"),
                                        ("RSS 2026", "rss2026_paper_cfg", "rss2026_tfidf_lr")]
          if f in R and b in R]
fig, ax = plt.subplots(figsize=(8, 4.2))
w = 0.36
for i, (lbl, f, b) in enumerate(pairs):
    for j, (key, col, name) in enumerate([(f, BLUE, "fastText"), (b, ORANGE, "TF-IDF + LogReg")]):
        r = R[key]
        x = i + (j - 0.5) * (w + 0.02)
        ax.bar(x, r["acc_mean"], w, color=col, label=name if i == 0 else None, zorder=2)
        ax.text(x, r["acc_mean"] + 1.2, f"{r['acc_mean']:.1f}%\n{r['train_s_mean']:.1f}s",
                ha="center", va="bottom", fontsize=9.5, color=INK)
ax.set_xticks(range(len(pairs)), [p[0] for p in pairs])
ax.set_ylabel("Test accuracy (%)")
ax.set_ylim(0, 112)
ax.yaxis.grid(True, color=GRID, zorder=0)
ax.legend(frameon=False, loc="upper right", ncol=2)
ax.set_title("Accuracy and training time (labels: accuracy / train seconds)",
             loc="left", color=INK, fontsize=12)
fig.tight_layout()
fig.savefig(OUT / "accuracy_vs_time.png", dpi=200)

# ---- Figure 2: 20NG epoch sweep
sweep_path = RES / "20ng_epoch_sweep.json"
if sweep_path.exists():
    S = json.load(open(sweep_path))
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for lr, col in [(0.25, BLUE), (1.0, ORANGE)]:
        pts = [s for s in S if s["lr"] == lr]
        ax.plot([s["epoch"] for s in pts], [s["acc_mean"] for s in pts], "-o", color=col,
                lw=2, ms=6, label=f"fastText lr={lr}" + (" (paper's AG News lr)" if lr == 0.25 else ""))
    base = R["20ng_tfidf_lr"]["acc_mean"]
    ax.axhline(base, color=GRAY, ls="--", lw=1.5)
    ax.text(100, base + 1.5, f"TF-IDF + LogReg {base:.1f}%", ha="right", color=INK2, fontsize=9.5)
    ax.annotate("paper setting\n(5 epochs)", (5, S[0]["acc_mean"]), (12, 12),
                color=INK2, fontsize=9.5, arrowprops=dict(arrowstyle="->", color=INK2))
    ax.set_xscale("log")
    ax.set_xticks([5, 10, 25, 50, 100], ["5", "10", "25", "50", "100"])
    ax.set_xlabel("Epochs")
    ax.set_ylabel("Test accuracy (%)")
    ax.set_ylim(0, 85)
    ax.yaxis.grid(True, color=GRID)
    ax.legend(frameon=False, loc="lower right")
    ax.set_title("20 Newsgroups: the paper's AG News settings underfit", loc="left",
                 color=INK, fontsize=12)
    fig.tight_layout()
    fig.savefig(OUT / "20ng_epoch_sweep.png", dpi=200)

# ---- Figure 3: confusion matrices, AG News test vs 2026 headlines (same AG News model)
def confusion(path):
    import csv
    names = ["World", "Sports", "Business", "Sci/Tech"]
    m = [[0] * 4 for _ in range(4)]
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            g, p = r["gold"].replace("__label__", ""), r["pred"].replace("__label__", "")
            m[int(g) - 1][int(p) - 1] += 1
    return names, [[c / max(sum(row), 1) * 100 for c in row] for row in m]


cm_files = [("AG News test (2004)", RES / "pred_ag_news_bigram.tsv"),
            ("2026 RSS headlines", RES / "pred_agnews_to_rss2026.tsv")]
if all(p.exists() for _, p in cm_files):
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9))
    for ax, (title, path) in zip(axes, cm_files):
        names, cm = confusion(path)
        ax.imshow(cm, cmap="Blues", vmin=0, vmax=100)
        for i in range(4):
            for j in range(4):
                ax.text(j, i, f"{cm[i][j]:.0f}", ha="center", va="center", fontsize=10,
                        color="white" if cm[i][j] > 55 else INK)
        ax.set_xticks(range(4), names, rotation=30, ha="right")
        ax.set_yticks(range(4), names)
        ax.set_xlabel("Predicted")
        ax.set_title(title, loc="left", color=INK, fontsize=11)
        for s in ax.spines.values():
            s.set_visible(False)
    axes[0].set_ylabel("True class")
    fig.suptitle("Same AG News model: row-normalised confusion (%)", x=0.02, ha="left",
                 color=INK, fontsize=12)
    fig.tight_layout()
    fig.savefig(OUT / "confusion_agnews_vs_2026.png", dpi=200)

print("figures in", OUT)
