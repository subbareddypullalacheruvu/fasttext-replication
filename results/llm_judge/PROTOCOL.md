# LLM-as-judge protocol

**What is judged.** Every item that the AG News-trained fastText model (seed 0, the paper's
settings) misclassifies in the 2026 RSS headline set. That run's predictions are frozen in
`judged_predictions_seed0.tsv` (127 errors out of 508), because multi-threaded fastText is
not bit-reproducible.

**Why.** Accuracy counts every wrong prediction the same way. The judge separates three
kinds of error, which change how the accuracy drop should be read:

| Verdict | Meaning |
|---|---|
| `MODEL_ERROR` | The gold label is clearly right by the guideline and fastText got it wrong. |
| `AMBIGUOUS` | The headline genuinely fits both the gold and the predicted class (a boundary case). |
| `LABEL_NOISE` | The gold label from the RSS section is wrong by the guideline, or no AG News class fits. |

**Judge.** Claude (model identifier `claude-opus-5-5`), used through the Claude app on
2 November 2026. There was no API access, so the judgements were made in one session with
the fixed prompt below and saved verbatim to `verdicts.csv`. The judge saw only the
headline and lead sentence, the gold label and the predicted label. It did not see the
source outlet, so it could not judge by outlet.

**Prompt (applied to every item):**

> You are checking errors made by a news topic classifier. Classes: World, Sports,
> Business, Sci/Tech, defined by this guideline: [contents of `data/labelling_guideline.md`].
> For the item below, the gold label comes from the news outlet's own section, and the
> predicted label comes from the classifier. Using only the headline and lead sentence,
> answer with exactly one verdict:
> MODEL_ERROR (gold is clearly correct), AMBIGUOUS (both labels are defensible), or
> LABEL_NOISE (gold is wrong, or no class fits). Then give one short reason, and the
> label you would assign.
> Headline + lead: {text}   Gold: {gold}   Predicted: {pred}

**Human check.** 30 items (random, seed 1) are copied to `human_check.csv`. The LLM's
verdict is in the last column (`llm_verdict`). **Hide that column before labelling.** Fill
`human_verdict` for each row using the same three verdicts and the guideline, then run
`python src/llm_judge_agreement.py`, which reports raw agreement and Cohen's kappa.

**Limitations.** One judge model and one pass only, with no measured self-consistency. The
judge may share the guideline author's biases, because the same guideline is given to
both. A newer model would give different verdicts, so the verdict file is stored rather
than regenerated.
