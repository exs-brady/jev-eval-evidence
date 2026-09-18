# The synthetic grid is contaminated

The synthetic items were produced by a generator whose prompt was handed the
same level descriptions the judges are then scored on applying. The text was
written from the rubric the judges are marked against, so **every synthetic
number in this bundle is an upper bound.** This page publishes both sides of
the comparison so the claim can be checked rather than taken on trust.

## Measured overlap

Two measures, because neither alone is convincing. *Sequence similarity* is
`difflib.SequenceMatcher.ratio()` over the two strings. *Token containment* is
the share of the generator string's word types that also appear in the judge
criterion. Both are computed on the strings printed below.

| Generator level | Judge criterion | Sequence similarity | Token containment |
|---|---|---|---|
| `none` | 0 | 17% | 76% |
| `L4` | 1 | 45% | 87% |
| `L3` | 2 | 71% | 88% |
| `L2` | 3 | 70% | 61% |
| `L1` | 4 | 68% | 83% |

Sequence similarity spans **17% to 71%** (45% to 71% across the four crisis levels; the `none` cell is the outlier). Token containment spans **61% to 88%**.

## Strings shared verbatim

Runs of 12 characters or more appearing identically in both. Whole level names
are copied word for word, as are the example phrases a judge would key on:

- **none / criterion 0:** `ith no acuity signal`
- **L4 / criterion 1:** `hopelessness or acute emotional distress with no suicidal ideation`
- **L3 / criterion 2:** `passive suicidal ideation or current self-harm`; `'wish i wasn't here', '`; `better off without me',`
- **L2 / criterion 3:** `explicit suicidal ideation`; `direct statement`; `of wanting to die or`
- **L1 / criterion 4:** `imminent risk`; `a plan, means or method`; `a timeframe`; `an attempt`; `intent to harm another person`

## What is affected, and what is not

| Arm | Contaminated | Why |
|---|---|---|
| Synthetic grid (crisis, trainee, omission) | **Yes** | the generator was fed the judge criteria, as above |
| Clinical phrase bank, 86 items | **Yes, by a different route** | the keyword lexicon was tuned on this bank, and the judges' level descriptions were themselves adapted from a prompt tuned against it |
| Clinical Set A arcs, 84 items | No | authored blind to the detector, the codebase and the fixtures; shares no wording with any judge's criteria |
| AnnoMI | No | the criteria restate the published MI coding scheme, which is the task definition rather than a leak of the answers |

This distinction matters for reading the figures:

- The **threshold ladder** and its span — the study's principal finding — are
  computed on the 84 arcs alone. Clean.
- The **probability-shape** table is computed on all 305 fixture items, so 86 of
  them are the contaminated bank. Its own heading says so. Treat it as
  suggestive of the mechanism, not as an independent result.
- Every **synthetic** table is an upper bound on every judge. The inflation is
  not uniform: it most rewards whichever judge follows a written criterion most
  literally, which is the disposition the study is trying to measure.
