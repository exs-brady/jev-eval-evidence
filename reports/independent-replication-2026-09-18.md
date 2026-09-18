# Independent replication of the multi-judge study

Date: 2026-09-18. All calculations were offline. No provider was called. The
independent implementation is `scripts/independent_replication.py`; its complete
machine-readable output is `reports/independent-replication-2026-09-18.json`.
It does not import either questioned analysis module, or the study's metric and
statistics helpers. It implements nominal Gwet AC1, Cohen kappa, macro/binary F1,
all rate metrics, thresholding, and the clustered/paired bootstrap directly.

## Bottom line

The published point estimates reproduce. The surprising inversion is not good
evidence for a stable model property: Jev's synthetic lead is concentrated in the
synthetic material, especially single messages, and disappears on synthetic arcs.
On the clinician-authored phrase bank Jev's conservative argmax is genuinely poor,
but the headline “best to worst” contrast mixes differently composed tables and a
synthetic generator prompt that closely restates the judging criteria.

The answer key is numerically accurate within its stated tolerances. I contradict
none of its explicit numeric claims. Its coverage-defect inventory is incomplete:
the same defect occurs in trainee calibration and both dev calibration reports.

## A — Published figures

Verdict: **confirmed with qualification**. Every recomputed headline point estimate
differs from the committed JSON by less than 0.0006 (in fact, none differs at the
stored precision). Bootstrap bounds differ slightly with seed and remain within the
specified 0.01 tolerance. The qualification is the placement-table `n` defect below.

Scoring units are:

| Dataset/table | Raw/current rows | Scored units |
|---|---:|---:|
| Crisis test | 916 turns | 499 single messages + 117 arc maxima = 616 |
| Trainee test | 714 replies | 714 |
| Omission test | 294 turns | 98 arcs |
| AnnoMI | 9,699 utterances in 133 transcripts | task/tier majority-gold count |
| Crisis fixtures | 305 calls | 86 phrases + 84 arc maxima |

### Crisis test

The table gives argmax and each judge's own frozen policy row.

| Judge | Argmax under | Argmax exact | Policy under | Policy exact |
|---|---:|---:|---:|---:|
| Haiku 4.5 | 0.026 [0.013, 0.039] | 0.950 [0.932, 0.966] | 0.018 [0.008, 0.029] | 0.867 [0.839, 0.891] |
| Sonnet 4.5 | 0.028 [0.015, 0.041] | 0.958 [0.942, 0.972] | 0.016 [0.006, 0.026] | 0.828 [0.799, 0.857] |
| Sonnet 5 | 0.006 [0.002, 0.013] | 0.951 [0.933, 0.968] | 0.005 [0.000, 0.011] | 0.898 [0.873, 0.920] |
| Qwen3.6-27B | 0.028 [0.015, 0.041] | 0.968 [0.953, 0.981] | 0.002 [0.000, 0.005] | 0.602 [0.563, 0.641] |
| GPT-5.4 mini | 0.016 [0.006, 0.028] | 0.946 [0.930, 0.964] | 0.015 [0.006, 0.024] | 0.886 [0.862, 0.912] |
| GPT-5.5 | 0.016 [0.006, 0.026] | 0.959 [0.943, 0.974] | 0.015 [0.006, 0.024] | 0.888 [0.864, 0.912] |
| Jev | 0.008 [0.002, 0.016] | 0.974 [0.961, 0.985] | 0.008 [0.002, 0.016] | 0.916 [0.893, 0.937] |

The floor alone reproduces: under 0.503, exact 0.437, false fire 0.096, and
positive-item over-triage 0.042.

### Trainee and omission test

| Trainee judge | F1 alone | False flag alone | Policy F1 | Policy false flag |
|---|---:|---:|---:|---:|
| Haiku 4.5 | 0.988 | 0.013 | 0.988 | 0.013 |
| Sonnet 4.5 | 0.996 | 0.004 | 0.994 | 0.006 |
| Sonnet 5 | 1.000 | 0.000 | 0.998 | 0.002 |
| Qwen3.6-35B | 0.983 | 0.015 | not frozen | not frozen |
| Qwen3.6-27B | 0.994 | 0.006 | 0.992 | 0.008 |
| GPT-5.4 mini | 0.964 | 0.038 | 0.964 | 0.038 |
| GPT-5.5 | 1.000 | 0.000 | 0.998 | 0.002 |
| Jev | 1.000 | 0.000 | 0.998 | 0.002 |

| Omission judge, grace 2 | Accuracy | False fire on asks arcs |
|---|---:|---:|
| Haiku 4.5 | 0.980 [0.949, 1.000] | 0.000 |
| Sonnet 4.5 | 1.000 | 0.000 |
| Sonnet 5 | 1.000 | 0.000 |
| Qwen3.6-27B | 1.000 | 0.000 |
| GPT-5.4 mini | 0.867 [0.796, 0.929] | 0.000 |
| Jev | 0.990 [0.969, 1.000] | 0.000 |

### AnnoMI

All AC1, kappa, accuracy and macro-F1 points in all twelve task/tier tables
reproduce. As a compact headline, hosted therapist-behaviour AC1 is 0.763 Haiku,
0.758 Sonnet 4.5, 0.790 Sonnet 5, 0.780 GPT-4.1, 0.800 GPT-5.4 mini, 0.791
GPT-5.5, and 0.760 Jev (n=1,364 majority-gold utterances). Complete values for
behaviour, open, complex and talk at local, hosted and all tiers are in the JSON.

The main-table `n` values match actual gold pairs. The pre-fix placement tables do
not: they print 216 for every therapist rater although each held-out reference uses
208–211 pairs, and 212 for every client rater although the actual range is 203–209.
The placement AC1 values themselves reproduce. The post-fix report correctly shows
the ranges.

## B — Coverage

Verdict: **confirmed with qualification**. The answer key's five crisis-test cases
are real, and the same report simultaneously calls all five “not scored”. The table
below distinguishes errors from absent rows. `Calibration n` is the successful
single-message subset that nevertheless received a numeric calibration score.

| Crisis-test judge | Usable/916 | Errors | Missing | Calibration n/499 |
|---|---:|---:|---:|---:|
| Qwen3.6-35B | 44 | 872 | 0 | 23 |
| Opus 5 | 100 | 0 | 816 | 100 |
| GPT-4.1 | 103 | 0 | 813 | 103 |
| Haiku k-sample-5 | 150 | 0 | 766 | 150 |
| Sonnet 4.5 k-sample-5 | 150 | 0 | 766 | 150 |

Additional scored-below-bar cases omitted by the answer key are:

| Report/table | Judge | Numeric score based on | Overall usable status | Also declared unscored? |
|---|---|---:|---:|---|
| Crisis dev calibration | Qwen3.6-35B | 7/144 singles | 8/231 turns; 223 errors | yes |
| Trainee dev calibration | Qwen3.6-35B | 2/180 | 2/180; 178 errors | yes |
| Trainee test calibration | Haiku k-sample-5 | 150/714 | 150/714; 564 missing | yes |
| Trainee test calibration | Sonnet 4.5 k-sample-5 | 150/714 | 150/714; 564 missing | yes |
| Trainee test calibration | Opus 5 | 100/714 | 100/714; 614 missing | yes |

No main performance table scores a below-bar judge. The post-fix reports gate or
explicitly disclose these rows. The pre-fix omission report silently omitted its
incomplete judges; the post-fix report discloses them. GPT-5.5 omission test has
223/294 usable turns, 3 errors and 68 missing turns and is correctly unscored.

## C — Cross-judge significance

Verdict: **confirmed** (the answer key is right; `totoro.md` is wrong as written).
The sentence is attached to the synthetic crisis **argmax** paragraph, but the
published paired-difference table compares each frozen **floor-union policy** with
Jev's frozen policy. On policy exactness all six CIs exclude zero. On argmax only
three do:

| Judge minus Jev, argmax exact | Difference [95% CI] | Excludes zero? |
|---|---:|---|
| Haiku 4.5 | -0.0244 [-0.0422, -0.0065] | yes |
| Sonnet 4.5 | -0.0162 [-0.0325, 0.0000] | no |
| Sonnet 5 | -0.0227 [-0.0406, -0.0065] | yes |
| Qwen3.6-27B | -0.0065 [-0.0211, 0.0081] | no |
| GPT-5.4 mini | -0.0276 [-0.0438, -0.0114] | yes |
| GPT-5.5 | -0.0146 [-0.0308, 0.0016] | no |

## D — Frozen crisis thresholds

Verdict: **confirmed**. Dev contains 144 singles and 24 arcs = 168 scoring units;
the floor false-fire rate is 3/56 = 0.0536. Rates below are for floor union judge.

| Judge | False fire at τ=.05/.1/.2/.3/.5 | Under-triage at same τ | Derived |
|---|---|---|---|
| Haiku 4.5 | .946/.089/.054/.054/.054 | .000/.006/.018/.018/.018 | .2, rule |
| Opus 5 | .857/.500/.339/.214/.107 | .000/.000/.000/.000/.000 | .5, fallback |
| Sonnet 4.5 | .893/.161/.071/.071/.071 | .000/.000/.000/.006/.006 | .2, fallback |
| Sonnet 5 | 1.000/.589/.304/.196/.179 | .000/.000/.000/.000/.000 | .5, fallback |
| Qwen3.6-27B | .857/.071/.071/.071/.071 | .000/.000/.018/.018/.018 | .1, fallback |
| GPT-4.1 | .232/.232/.232/.232/.232 | .000/.006/.006/.006/.006 | .05, fallback |
| GPT-5.4 mini | .518/.250/.179/.143/.143 | .000/.000/.000/.000/.000 | .3, fallback |
| GPT-5.5 | .536/.268/.143/.143/.143 | .000/.000/.006/.006/.006 | .2, fallback |
| Jev | .357/.268/.125/.125/.107 | .000/.000/.000/.000/.000 | .5, fallback |

Only one of nine meets the main condition; eight use fallback. False fire is
necessarily non-increasing with τ, but it plateaus for seven judges (GPT-4.1 across
the entire ladder). The procedure has no single high/low bias. The main rule selects
the lowest eligible τ. The fallback first favours high τ by minimizing false fire,
then on a plateau favours the lowest-under-triage point, often the plateau's low-τ
edge; Qwen (.1), GPT-4.1 (.05), Sonnet 4.5 (.2) and GPT-5.5 (.2) demonstrate this.
Thus the result depends strongly on the probability shape.

All nine frozen crisis entries rederive exactly from current dev data. Alternative
Jev ladder points would materially change test behaviour: model-alone τ=.2 changes
under/exact/false-fire/over from .008/.974/.029/.012 at argmax to
.002/.942/.111/.029; τ=.05 reaches .000/.864/.240/.083.

## E — Deterministic-floor ablation

Verdict: **confirmed with qualification**. The qualification is interpretive: the
floor's benefit is specific to the phrase bank on which its lexicon was tuned.

### Jev on synthetic test

| Policy | Under off/on | Exact off/on | False fire off/on | Over off/on |
|---|---:|---:|---:|---:|
| argmax | .008/.008 | .974/.917 | .029/.120 | .012/.051 |
| τ=.05 | .000/.000 | .864/.825 | .240/.293 | .083/.115 |
| τ=.1 | .000/.000 | .907/.864 | .168/.231 | .054/.088 |
| τ=.2 | .002/.002 | .942/.891 | .111/.188 | .029/.066 |
| τ=.3 | .002/.002 | .958/.904 | .087/.168 | .017/.056 |
| τ=.5 | .008/.008 | .972/.916 | .034/.125 | .012/.051 |

The floor buys no synthetic under-triage reduction at any setting. It consistently
costs exactness and increases false fire and over-triage.

### Jev on clinician-authored crisis fixtures

Phrase-bank under/exact use the 60 must-trigger phrases; false fire uses 26
must-not phrases. Set-A under/exact use 84 arcs; false fire uses 14 no-crisis arcs
and over uses 70 risk arcs.

| Policy | Bank under off/on | Bank exact off/on | Bank false fire off/on | Arc under off/on | Arc exact off/on |
|---|---:|---:|---:|---:|---:|
| argmax | .250/.000 | .700/.950 | .000/.000 | .155/.155 | .786/.774 |
| τ=.05 | .033/.000 | .833/.867 | .308/.308 | .036/.036 | .798/.798 |
| τ=.1 | .083/.000 | .817/.900 | .115/.115 | .036/.036 | .833/.821 |
| τ=.2 | .117/.000 | .833/.950 | .000/.000 | .060/.060 | .833/.821 |
| τ=.3 | .133/.000 | .817/.950 | .000/.000 | .107/.107 | .821/.810 |
| τ=.5 | .250/.000 | .717/.950 | .000/.000 | .155/.155 | .786/.774 |

On the phrase bank, the floor eliminates all under-triage and sharply improves
exactness. On the independently authored Set A arcs it reduces under-triage at no
setting and usually trades a little exactness for extra over-triage. This is exactly
what tuning ancestry predicts: the lexicon is useful on its design phrases, while
contextual paraphrases outside that design do not receive the same recall benefit.

## F — Jev versus Qwen3.6-27B

Verdict: **confirmed with qualification**. The key's listed comparisons reproduce;
the extension to all shared AnnoMI tasks also finds no significant difference.
All differences are Qwen minus Jev and use paired cluster draws.

| Dataset/metric | Jev | Qwen | Difference [95% CI] | Distinguishable? |
|---|---:|---:|---:|---|
| Crisis argmax under | .008 | .028 | +.0195 [.0081, .0308] | yes, Jev safer |
| Crisis argmax exact | .974 | .968 | -.0065 [-.0211, .0081] | no |
| Trainee policy F1 | .998 | .992 | -.0062 [-.0140, .0000] | no |
| Trainee policy false flag | .002 | .008 | +.0063 [.0000, .0146] | no |
| Omission accuracy | .990 | 1.000 | +.0102 [.0000, .0306] | no |
| AnnoMI behaviour AC1 (n=543) | .797 | .804 | +.0071 [-.0243, .0370] | no |
| AnnoMI open AC1 (n=187) | .695 | .708 | +.0127 [-.0604, .0911] | no |
| AnnoMI complex AC1 (n=150) | .293 | .387 | +.0937 [-.0791, .2799] | no |
| AnnoMI talk AC1 (n=426) | .703 | .726 | +.0235 [-.0186, .0620] | no |

On crisis fixtures at argmax, Qwen is better descriptively: bank exact 50/60 vs
Jev 42/60 and under 6 vs 15; arc exact 70/84 vs 66/84 and under 10 vs 13. The
trainee clinical-fixture headline is identical for both: 7/7 guard positives with
0/6 false flags, 30/30 supplementary positives with 0/30 false flags, all 8/8
misconduct arcs, and no flag on the good-practice control.

Probability shape explains the frozen-policy divergence. Share of crisis turns with
upward tail mass below .05 is .818 Jev, .532 GPT-5.4 mini, .459 GPT-5.5, .245
Haiku, .242 Sonnet 4.5, .201 Qwen and .142 Sonnet 5. Model-alone over-triage at
τ=.05/.1/.2/.3/.5/argmax is:

| Judge | Over-triage sequence |
|---|---|
| Jev | 8.3%, 5.4%, 2.9%, 1.7%, 1.2%, 1.2% |
| Qwen | 70.1%, 52.9%, 2.0%, 0.5%, 0.5%, 0.5% |
| Sonnet 5 | 73.5%, 71.3%, 28.2%, 8.1%, 4.7%, 4.7% |
| Sonnet 4.5 | 69.1%, 56.4%, 15.7%, 2.0%, 2.0%, 2.0% |
| Haiku | 56.4%, 38.0%, 8.3%, 3.4%, 3.4%, 3.4% |
| GPT-5.4 mini | 44.4%, 10.0%, 1.7%, 1.5%, 1.5%, 1.5% |
| GPT-5.5 | 55.6%, 15.2%, 2.5%, 1.5%, 0.5%, 0.5% |

The verbalised judges differ greatly from one another, but all place more frequent
small mass above argmax than the sole native judge. That is consistent with an
elicitation-method effect, not proof of one: model and method are confounded because
there is only one native judge. Qwen's sharp .1-to-.2 cliff plus the fallback tie
break selects .1 and creates the very poor frozen-policy exact rate (.602); its
argmax is otherwise close to Jev.

For an organisation that already has the harness, the commercial model's supported
advantage in these data is narrower than “better judge”: lower synthetic crisis
under-triage, native probabilities that behave more smoothly under thresholding,
and much lower measured latency. It does not deliver a detectable accuracy or AC1
gain over Qwen on trainee, omission, any shared AnnoMI task, or the clinical crisis
fixtures. The purchase case is therefore operational and probability-interface
quality, not demonstrated broad superiority.

## Part 2 — Adjudication of the inversion

The two point estimates are real on their own tables, but the claimed inversion as
a property of the models is a **benchmark artefact**.

The label spaces are both the same five ordered levels, but the table scorers are
not identical: synthetic exact includes all 616 units, including 208 no-crisis
units, whereas phrase-bank exact is 60 must-trigger phrases and reports its 26
must-not phrases separately. Conditioning synthetic results on risk does not remove
Jev's advantage (risk exact .975), so denominator choice is not the whole cause.

Form and construction are more revealing. Jev synthetic exact is .980 on singles
but .949 on arcs; Qwen is .983 on synthetic arcs. On the clinician-authored arcs
Jev is tied for the lowest exact count (66/84), so Jev is not “best” once the
synthetic headline is decomposed by conversational form. The effect is concentrated
in synthetic single messages.

The synthetic cell descriptions and generation prompts closely restate the Jev
question's five criteria: no crisis, distress, passive ideation/current self-harm,
explicit ideation, and plan/means/timeframe/attempt. This makes the generated text a
test of how well judges recover the grid that instructed its writers, not a clean
external-validity test. The Jev criteria themselves were adapted from [partner]'s
classifier prompt, which had been tuned against the phrase bank. That shared ancestry
does not rescue the phrase-bank result—Jev argmax still under-triages 15/60—but it
does make neither side an independent generalisation benchmark.

Finally, argmax is a materially more conservative object for Jev on the phrase bank.
Moving Jev to τ=.2 improves bank exact from 42/60 to 50/60 and under-triage from 15
to 7, while worsening synthetic specificity. That is a policy choice, not an
intrinsic reversal of semantic ability.

The clinician-authored Set A arcs should carry more evidential weight than the
synthetic headline or the lexicon design bank. They show Jev in the lower group, not
universally worst, and they do not support a headline that Jev is the best judge.

## Answer-key diff and additional findings

No explicit answer-key value is contradicted. Group statuses are:

| Group | Status |
|---|---|
| A | confirmed with qualification |
| B | confirmed with qualification |
| C | confirmed |
| D | confirmed |
| E | confirmed with qualification |
| F | confirmed with qualification |

Qualifications are: the answer key omits five additional below-coverage calibration
scores; its Group F list is not every shared dataset/task; and its ablation numbers
need the design-bank versus independent-arc distinction to avoid over-generalising
the floor's benefit.

Other findings:

- The pre-fix placement-table `n` is the ceiling pool, not the actual pair count.
- The pre-fix AnnoMI operations table renders batch-only latency as zero; the current
  report correctly says “batch only”.
- The old omission report omitted incomplete judges without a disclosure line. The
  current report fixes that without changing scored rows.
- Threshold fallback is not intrinsically a high-τ rule. On probability plateaus,
  the under-triage tie-break can select the lowest threshold on the plateau.
