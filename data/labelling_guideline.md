# Labelling guideline – 2026 RSS headline dataset

Each item is a headline plus its lead sentence. Labels follow the four AG News
classes. Automatic labels come from the outlet's own section (the feed it was
published in). During manual spot-checking, judge the label using the rules below,
**based only on the headline and lead sentence** (the same information the model sees).

| Label | Includes | Excludes (goes elsewhere) |
|---|---|---|
| **1 World** | International and national politics, elections, government, war and conflict, diplomacy, disasters, crime and courts, social issues | A company's results or a market move (→ Business), even if it happens abroad |
| **2 Sports** | Matches, results, athletes, teams, transfers, sporting bodies and events | A club's sale or sponsorship deal described mainly in financial terms (→ Business) |
| **3 Business** | Companies, markets, economy, trade, prices, jobs, interest rates, earnings, consumer and workplace issues | Government trade or tariff *disputes* between countries (→ World) unless the focus is the market or company impact |
| **4 Sci/Tech** | Science, research, space, health research, environment science, technology products, AI, software, internet, cybersecurity | Tech companies' earnings, share prices or acquisitions (→ Business) |

**Tie-break rule:** choose the class that describes what the story is *mainly about*
– the actor and action in the headline – not where it happened.

**How to spot-check**
1. `python collect_rss.py sample -n 50` writes `data/spotcheck_sample.csv`.
2. For each row, mark `correct (Y/N)`; if N, write the label you would give.
3. Agreement = Y count ÷ 50. Report it together with the common disagreement types.
4. If agreement is below about 85%, revise the feed-to-label mapping (e.g. drop a
   feed that mixes topics) and re-check a fresh sample.
