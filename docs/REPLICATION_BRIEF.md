# Replication brief: examine the data, draw your own conclusions

**For:** an independent analyst (human or model) with shell access to this working tree
**Date issued:** 2026-09-18
**Answer key:** `docs/replication_claims.json` — **do not open it until Part 3**

---

## Why you are being asked

A multi-judge evaluation study (`reports/`, summarised on a public page) was audited,
then extended with ablations and a head-to-head comparison. The analysis produced a
set of claims. Some of those claims are surprising, at least one earlier statement in
the same analysis was over-generalised and had to be retracted under challenge, and
the study owner is not confident the picture is internally consistent.

**Your job is not to check my working. It is to look at the same data and say what
you think it shows.** If you reach different conclusions, that is the useful outcome.

Two honest warnings about your predecessor's reliability:

1. It claimed a threshold-selection fallback "always returns the largest τ on the
   ladder". True for one judge, false for two others. Caught only because a human
   pushed back on it. Assume there are more of these.
2. It wrote the corrected analysis code. Where a claim depends on code it changed,
   you should be more suspicious, not less. Those files are listed in Part 4.

---

## Part 0: environment and hard constraints

**You must work on this machine, in this working tree.** A git clone will not do:

| Path | Tracked in git | On disk | Notes |
|---|---|---|---|
| `runs/` | **0 files** | 75 files | The entire raw judgment store. Gitignored. |
| `fixtures/annomi/*.csv` | no | yes | AnnoMI corpus. Gitignored. |
| `datasets/` | 6 of 492 | 492 | Item store partly gitignored. |
| `reports/` | 22 of 28 | 28 | |

**Spend zero.** Make no API calls to any provider. Everything below is computable
offline from cached rows: the deterministic floor is applied at *analysis* time, not
at judging time, so any combination of floor on/off and threshold can be recomputed
for free. If you think a question needs a fresh model call, stop and say so instead.

**Run tests before and after anything you touch:** `uv run pytest` (79 expected).

---

## Part 1: what the study asserts, and what to test

Compute each of these independently. **Do not reuse the study's own analysis
functions for verification** — `experiments/compare/run.py` and
`experiments/annomi_codes/analysis.py` are the code whose output is in question, and
re-running them would reproduce their own faults. Write your own implementations of
Gwet's AC1, the clustered bootstrap, macro/binary F1, and the rate metrics from the
definitions. Read `docs/PREREGISTRATION.md` for the intended method, and
`src/jevlab/policy.py` for the level ordering and the tail-threshold rule.

### Group A — Do the published headline figures reproduce?

For the crisis, trainee and omission test splits and the AnnoMI corpus, recompute
every judge's headline metric from `runs/` and `datasets/` and compare to the
committed reports in `reports/`. Report any figure that does not reproduce, and the
size of the discrepancy. Also report the unit counts each table is computed over,
and whether the `n` printed in each table matches the rows actually used.

### Group B — Was any judge scored on data it largely failed to produce?

For every (experiment, judge, table) combination, compute what fraction of the
relevant items the judge actually returned a usable answer for. Then check whether
that judge appears with a score in that table. Pay attention to rows whose status is
`error` as distinct from a missing row. Report every case where a scored judge falls
below the study's stated 95% coverage bar, and say whether the report simultaneously
declares it unscored.

### Group C — Is the cross-judge significance claim supported?

`totoro.md` states that, paired against the reference judge, every other judge's
exact-level rate is lower with the confidence interval excluding zero. Establish
which table that claim is attached to, which table it was computed from, and whether
it holds on both. Report the paired differences and intervals you compute.

### Group D — How were the frozen thresholds actually chosen?

`docs/THRESHOLDS.json` records a τ per judge per use case, and a `fallback` flag.
Reconstruct the selection from the **dev** split for every crisis judge: the
candidate thresholds, each one's dev false-alarm rate, the floor's own rate, which
candidates satisfied the pre-registered constraint, and what the tie-breaks did.
Then answer:

- How many thresholds came from the rule's main condition, and how many from its
  fallback?
- Is the false-alarm rate monotone in τ for every judge, or does it plateau?
- Does the selection procedure systematically favour high or low τ, and does the
  answer depend on the shape of the judge's probability distribution?
- Is there any τ on the candidate ladder the procedure could have chosen that would
  materially change the reference judge's behaviour on the test split?

The freeze is incremental and never overwrites an existing entry, so also check
whether every frozen τ still re-derives from the dev data as it currently stands.

### Group E — What does the deterministic harness contribute?

The published configuration is `floor ∪ judge at frozen τ`. Decompose it. For the
reference judge on both the synthetic test split and the blind-authored
fixtures, compute the full grid of {floor on, floor off} × {argmax, τ ∈ 0.05, 0.1,
0.2, 0.3, 0.5} against under-triage, exact level, false-alarm and over-triage.

Then say, in your own words: what does the deterministic floor buy, on which
dataset, and what does it cost? Does your answer differ between the synthetic items
and the blind-authored material? If it does, explain why — the difference is the
most important thing in this brief.

Note while doing this: the phrase bank is the set the keyword lexicon was originally
tuned against; the 84 Set A arcs were authored blind to the detector by a separate
model session, not by a clinician, and their expected levels are unratified.

### Group F — Does a free local model match the commercial one?

Compare `typesafe:jev-1.13.0` against `local:qwen36-mtplx` (Qwen3.6-27B) on every
dataset where both have coverage, paired on the same resampled clusters. Report
point estimates, differences, intervals and which differences are distinguishable
from zero.

Then extend to all judges with coverage and characterise the *shape* of each one's
probability output: how much mass sits above its own top answer, how that mass is
distributed, and how each judge's behaviour responds as the threshold is lowered.
Consider whether any difference you find tracks the elicitation method
(`native` vs `verbalised` — see `src/jevlab/judges/`) rather than the model.

Form your own view on this question: **if an organisation already has this harness,
what does the commercial model give them that the free local one does not?** Support
it or refute it from the data.

---

## Part 2: the tension to adjudicate

One result pair is the reason this brief exists. State plainly whether you think it
is a real property of the models or an artefact of how the study was built:

> On the synthetic test split, the reference judge is the **best** of every judge
> tested. On the [partner] phrase bank, judged the same way, it is the
> **worst** of every judge tested.

Candidate explanations to test rather than assume:

- The synthetic grid and the reference judge's question definitions may share
  ancestry. Check how `datasets/*/items.jsonl` was generated (`src/jevlab/synth/`)
  and where the judge's criteria came from — `reports/2026-09-17-crisis-severity.md`
  carries a caveat about this that you should read and then verify independently.
- The two sets differ in form: decontextualised single phrases versus items carrying
  conversational history. Check whether the effect concentrates in one form.
- "Best" and "worst" are being measured with different scorers on different label
  spaces. Check they are commensurable before treating the inversion as real.
- The comparison may be argmax-versus-argmax where one judge's argmax is a
  systematically more conservative object than another's.

If the inversion is real, say what it implies about which dataset should carry the
study's headline. If it is an artefact, say which figures are compromised.

---

## Part 3: only now, open the answer key

When you have your own numbers, read `docs/replication_claims.json` and diff
mechanically. Tolerances are stated in the file. Bootstrap interval bounds are
seed-dependent — treat a bound difference under 0.01 as agreement and any point
estimate difference over 0.0006 as a discrepancy worth reporting.

For each group, report one of: **confirmed**, **confirmed with qualification**,
**contradicted**, or **not testable from available data**. A claim you cannot test
is a finding; do not guess.

---

## Part 4: files the prior analysis modified

Be more sceptical of claims resting on these. All were changed after the defects
were found, so the current code is *not* the code that produced the committed
reports dated `2026-09-17`.

- `experiments/compare/run.py` — coverage gate on calibration tables; threshold-doc
  rendering; disclosure rows for unscored judges
- `experiments/annomi_codes/analysis.py` — coverage gate on calibration; batch-row
  latency guard; placement pair-count reporting and standings wording
- `docs/THRESHOLDS.md` — regenerated from the existing JSON, no re-tuning

The `2026-09-17-*` reports are the pre-fix originals and the `2026-09-18-*` reports
are post-fix. Diffing them tells you exactly what the changes did. `git diff` and
`git log` are available; the working tree has uncommitted changes.

---

## What to hand back

1. Your numbers for Groups A–F, with the code you used.
2. Your verdict on Part 2, argued.
3. Your answer to the Group F question, argued.
4. A list of claims from the answer key you **contradict**, with evidence.
5. Anything you found that this brief did not ask about. The prior analysis found
   four defects of one family — a table scoring a judge on whichever rows happened
   to succeed. Assume that family has more members and that this brief, written by
   the same analysis, is blind to whatever it was blind to before.
