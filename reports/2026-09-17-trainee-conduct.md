# Experiment B: [partner] trainee conduct

- Model: `jev-1.13.0` (pinned), $0.042/Mtok input
- [partner]: `a2f566a+dirty` (lexicon vendored; see `src/jevlab/vendor/nav_lexicon.py`)
- [partner]: `7bf0a2c` (heuristics.py loaded live)
- Fixtures: see `fixtures/SOURCE.md`

## 1. Clinical paraphrase guard ([partner] QA-016, 13 labelled replies)

| Detector | Harms caught | False flags on clean replies |
|---|---|---|
| regex floor | 6/7 | 0/6 |
| regex ∪ Jev τ=0.3 | 7/7 | 0/6 |
| regex ∪ Jev τ=0.5 | 7/7 | 0/6 |
| regex ∪ Jev τ=0.7 | 7/7 | 0/6 |
| regex ∪ Jev τ=0.9 | 7/7 | 0/6 |

One label here is the documented, accepted regex gap ("That's a silly thing to worry about." is judgmental; the floor is expected to miss it).

Errors at τ=0.7:

None.

## 2. Supplementary paraphrases (60 replies, NOT clinician-reviewed)

| Detector | Harms caught | False flags on clean replies |
|---|---|---|
| regex floor | 3/30 | 0/30 |
| regex ∪ Jev τ=0.3 | 30/30 | 1/30 |
| regex ∪ Jev τ=0.5 | 30/30 | 0/30 |
| regex ∪ Jev τ=0.7 | 30/30 | 0/30 |
| regex ∪ Jev τ=0.9 | 25/30 | 0/30 |

| Harm | Regex caught | +Jev caught (τ=0.7) | Regex false flags | +Jev false flags (τ=0.7) |
|---|---|---|---|---|
| secrecy | 0/3 | 3/3 | 0/3 | 0/3 |
| minimize | 0/3 | 3/3 | 0/3 | 0/3 |
| logistics | 0/3 | 3/3 | 0/3 | 0/3 |
| interrogation | 0/3 | 3/3 | 0/3 | 0/3 |
| moralizing | 0/3 | 3/3 | 0/3 | 0/3 |
| false_reassurance | 0/3 | 3/3 | 0/3 | 0/3 |
| boundary | 0/3 | 3/3 | 0/3 | 0/3 |
| stated_feelings | 1/3 | 3/3 | 0/3 | 0/3 |
| judged | 0/3 | 3/3 | 0/3 | 0/3 |
| leading | 2/3 | 3/3 | 0/3 | 0/3 |

Errors at τ=0.7:

None.

## 3. Misconduct suite (10 clinician-authored arcs)

| Detector | Harmful arcs with target harm flagged | Flags on good-practice control |
|---|---|---|
| regex floor | 8/8 | none |
| regex ∪ Jev τ=0.3 | 8/8 | none |
| regex ∪ Jev τ=0.5 | 8/8 | none |
| regex ∪ Jev τ=0.7 | 8/8 | none |
| regex ∪ Jev τ=0.9 | 8/8 | none |

These arcs were written alongside the regex, so the floor is expected to catch them; this section checks that the overlay adds nothing to the good-practice control.

## 4. Omission: never asking directly about suicide

| Arc | Source | Expected | Fires (grace 1) | Fires (grace 2) | P(asked) by turn | P(disclosed) by turn |
|---|---|---|---|---|---|---|
| mis_avoid_asking | clinical | should fire | turn 1 | turn 2 | [0.03, 0.03, 0.03] | [0.96, 0.97, 0.97] |
| mis_control_good_practice | clinical | should stay silent | silent | silent | [0.98, 0.98] | [0.96, 0.98] |
| extra_avoid_reframe | extra (unreviewed) | should fire | turn 1 | turn 2 | [0.02, 0.03, 0.03] | [0.9, 0.96, 0.96] |
| extra_validate_then_ask | extra (unreviewed) | should stay silent | turn 1 | silent | [0.03, 0.98] | [0.97, 0.96] |

Policy: after a disclosure (regex `detect_risk` on the youth, or P(disclosed) ≥ 0.5), fire once `grace` trainee turns pass with P(asked directly) < 0.5. The regex floor has no omission detector, so every arc is silent without Jev.

## Latency and cost (one call per trainee turn, 12 questions)

| p50 ms | p95 ms | Mean input tokens | USD per 1k turns |
|---|---|---|---|
| 270 | 674 | 1188 | $0.0499 |
