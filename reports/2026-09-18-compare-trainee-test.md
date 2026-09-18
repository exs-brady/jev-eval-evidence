# Multi-judge comparison: trainee (test)

- Model: `jev-1.13.0` (pinned), $0.042/Mtok input
- [partner]: `a2f566a+dirty` (lexicon vendored; see `src/jevlab/vendor/nav_lexicon.py`)
- [partner]: `7bf0a2c` (heuristics.py loaded live)
- Fixtures: see `fixtures/SOURCE.md`

## Trainee conduct, test split: 714 replies (239 positives, 236 near-miss negatives, 239 clean), 1 contested

F1 over all replies for their cell's harm; false flag = flagged on a negative. 95% CIs: bootstrap over replies.

| Configuration | F1 | Recall | False flag (all negatives) | False flag (near-miss) |
|---|---|---|---|---|
| regex floor | 0.316 [0.245, 0.383] | 0.188 [0.140, 0.237] | 0.002 [0.000, 0.007] | 0.004 [0.000, 0.013] |
| anthropic:claude-haiku-4-5-20251001 alone (p ≥ 0.5) | 0.988 [0.977, 0.996] | 1.000 [1.000, 1.000] | 0.013 [0.004, 0.024] | 0.025 [0.008, 0.047] |
| regex ∪ anthropic:claude-haiku-4-5-20251001 τ=0.3 | 0.988 [0.977, 0.996] | 1.000 [1.000, 1.000] | 0.013 [0.004, 0.024] | 0.025 [0.008, 0.047] |
| anthropic:claude-sonnet-4-5-20250929 alone (p ≥ 0.5) | 0.996 [0.989, 1.000] | 1.000 [1.000, 1.000] | 0.004 [0.000, 0.011] | 0.008 [0.000, 0.022] |
| regex ∪ anthropic:claude-sonnet-4-5-20250929 τ=0.3 | 0.994 [0.986, 1.000] | 1.000 [1.000, 1.000] | 0.006 [0.000, 0.014] | 0.013 [0.000, 0.029] |
| anthropic:claude-sonnet-5 alone (p ≥ 0.5) | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| regex ∪ anthropic:claude-sonnet-5 τ=0.3 | 0.998 [0.994, 1.000] | 1.000 [1.000, 1.000] | 0.002 [0.000, 0.007] | 0.004 [0.000, 0.013] |
| local:qwen36-35b-mtplx alone (p ≥ 0.5) | 0.983 [0.971, 0.994] | 0.996 [0.986, 1.000] | 0.015 [0.004, 0.027] | 0.030 [0.009, 0.054] |
| local:qwen36-35b-mtplx (no frozen τ; run --split dev --freeze first) | 0.983 [0.971, 0.994] | 0.996 [0.986, 1.000] | 0.015 [0.004, 0.027] | 0.030 [0.009, 0.054] |
| local:qwen36-mtplx alone (p ≥ 0.5) | 0.994 [0.985, 1.000] | 1.000 [1.000, 1.000] | 0.006 [0.000, 0.015] | 0.013 [0.000, 0.030] |
| regex ∪ local:qwen36-mtplx τ=0.3 | 0.992 [0.983, 0.998] | 1.000 [1.000, 1.000] | 0.008 [0.002, 0.017] | 0.017 [0.004, 0.036] |
| openai:gpt-5.4-mini alone (p ≥ 0.5) | 0.964 [0.946, 0.980] | 1.000 [1.000, 1.000] | 0.038 [0.022, 0.056] | 0.068 [0.037, 0.101] |
| regex ∪ openai:gpt-5.4-mini τ=0.7 | 0.964 [0.946, 0.980] | 1.000 [1.000, 1.000] | 0.038 [0.022, 0.056] | 0.068 [0.037, 0.101] |
| openai:gpt-5.5 alone (p ≥ 0.5) | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| regex ∪ openai:gpt-5.5 τ=0.3 | 0.998 [0.994, 1.000] | 1.000 [1.000, 1.000] | 0.002 [0.000, 0.007] | 0.004 [0.000, 0.013] |
| typesafe:jev-1.13.0 alone (p ≥ 0.5) | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| regex ∪ typesafe:jev-1.13.0 τ=0.5 | 0.998 [0.994, 1.000] | 1.000 [1.000, 1.000] | 0.002 [0.000, 0.007] | 0.004 [0.000, 0.013] |

### Paired differences vs regex ∪ Jev

| Comparison | Metric | Difference [95% CI] | CI excludes 0 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 − Jev | f1 | -0.010 [-0.020, -0.002] | yes |
| anthropic:claude-haiku-4-5-20251001 − Jev | false_flag | 0.011 [0.002, 0.021] | yes |
| anthropic:claude-sonnet-4-5-20250929 − Jev | f1 | -0.004 [-0.011, 0.000] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | false_flag | 0.004 [0.000, 0.011] | no |
| anthropic:claude-sonnet-5 − Jev | f1 | 0.000 [0.000, 0.000] | no |
| anthropic:claude-sonnet-5 − Jev | false_flag | 0.000 [0.000, 0.000] | no |
| local:qwen36-mtplx − Jev | f1 | -0.006 [-0.015, 0.000] | no |
| local:qwen36-mtplx − Jev | false_flag | 0.006 [0.000, 0.015] | no |
| openai:gpt-5.4-mini − Jev | f1 | -0.034 [-0.052, -0.019] | yes |
| openai:gpt-5.4-mini − Jev | false_flag | 0.036 [0.020, 0.054] | yes |
| openai:gpt-5.5 − Jev | f1 | 0.000 [0.000, 0.000] | no |
| openai:gpt-5.5 − Jev | false_flag | 0.000 [0.000, 0.000] | no |

### Per-harm F1 (policy rows)

| Harm | n | regex | anthropic:claude-haiku-4-5-20251001 | anthropic:claude-sonnet-4-5-20250929 | anthropic:claude-sonnet-5 | local:qwen36-mtplx | openai:gpt-5.4-mini | openai:gpt-5.5 | typesafe:jev-1.13.0 |
|---|---|---|---|---|---|---|---|---|---|
| boundary | 72 | 0.00 | 0.98 | 1.00 | 1.00 | 0.96 | 0.94 | 1.00 | 1.00 |
| false_reassurance | 72 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 | 1.00 | 1.00 |
| interrogation | 72 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 | 1.00 | 1.00 |
| judged | 72 | 0.15 | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 | 1.00 | 1.00 |
| leading | 72 | 0.63 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| logistics | 72 | 0.22 | 1.00 | 0.98 | 1.00 | 0.98 | 0.92 | 1.00 | 1.00 |
| minimize | 69 | 0.22 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| moralizing | 70 | 0.41 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| secrecy | 72 | 0.33 | 0.91 | 0.96 | 0.98 | 0.98 | 0.86 | 0.98 | 0.98 |
| stated_feelings | 71 | 0.45 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

### Calibration, P(harm) vs intended (compare within an elicitation only)

| Judge | Elicitation | n | Brier | ECE |
|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 (ksample5) | ksample5 | 150/714 | not scored (coverage) |  |
| anthropic:claude-haiku-4-5-20251001 | verbalised | 714 | 0.015 | 0.062 |
| anthropic:claude-opus-5 | verbalised | 100/714 | not scored (coverage) |  |
| anthropic:claude-sonnet-4-5-20250929 (ksample5) | ksample5 | 150/714 | not scored (coverage) |  |
| anthropic:claude-sonnet-4-5-20250929 | verbalised | 714 | 0.004 | 0.026 |
| anthropic:claude-sonnet-5 | verbalised | 714 | 0.005 | 0.052 |
| local:qwen36-35b-mtplx | verbalised | 714 | 0.011 | 0.006 |
| local:qwen36-mtplx | verbalised | 714 | 0.006 | 0.032 |
| openai:gpt-4.1 | verbalised | 0/714 | not scored (coverage) |  |
| openai:gpt-5.4-mini | verbalised | 714 | 0.025 | 0.034 |
| openai:gpt-5.5 | verbalised | 714 | 0.001 | 0.020 |
| typesafe:jev-1.13.0 | native | 714 | 0.004 | 0.045 |

### F1 by generator family and contested flag (policy row)

| Judge | Slice | n | F1 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | generated by anthropic | 354 | 0.983 [0.967, 0.996] |
| anthropic:claude-haiku-4-5-20251001 | generated by openai | 360 | 0.992 [0.978, 1.000] |
| anthropic:claude-haiku-4-5-20251001 | uncontested only | 713 | 0.988 [0.977, 0.996] |
| anthropic:claude-sonnet-4-5-20250929 | generated by anthropic | 354 | 0.992 [0.977, 1.000] |
| anthropic:claude-sonnet-4-5-20250929 | generated by openai | 360 | 0.996 [0.986, 1.000] |
| anthropic:claude-sonnet-4-5-20250929 | uncontested only | 713 | 0.996 [0.990, 1.000] |
| anthropic:claude-sonnet-5 | generated by anthropic | 354 | 0.996 [0.987, 1.000] |
| anthropic:claude-sonnet-5 | generated by openai | 360 | 1.000 [1.000, 1.000] |
| anthropic:claude-sonnet-5 | uncontested only | 713 | 0.998 [0.994, 1.000] |
| local:qwen36-mtplx | generated by anthropic | 354 | 0.996 [0.987, 1.000] |
| local:qwen36-mtplx | generated by openai | 360 | 0.988 [0.970, 1.000] |
| local:qwen36-mtplx | uncontested only | 713 | 0.994 [0.986, 1.000] |
| openai:gpt-5.4-mini | generated by anthropic | 354 | 0.967 [0.942, 0.988] |
| openai:gpt-5.4-mini | generated by openai | 360 | 0.960 [0.932, 0.981] |
| openai:gpt-5.4-mini | uncontested only | 713 | 0.964 [0.948, 0.980] |
| openai:gpt-5.5 | generated by anthropic | 354 | 0.996 [0.987, 1.000] |
| openai:gpt-5.5 | generated by openai | 360 | 1.000 [1.000, 1.000] |
| openai:gpt-5.5 | uncontested only | 713 | 0.998 [0.994, 1.000] |
| typesafe:jev-1.13.0 | generated by anthropic | 354 | 0.996 [0.987, 1.000] |
| typesafe:jev-1.13.0 | generated by openai | 360 | 1.000 [1.000, 1.000] |
| typesafe:jev-1.13.0 | uncontested only | 713 | 0.998 [0.994, 1.000] |

### Operations

| Judge | Calls | Parse failed | Errors | Re-asked | Unwrapped (A6) | p50 ms | p95 ms | USD/1k | Sampling | Reasoning |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 714 | 0 | 0 | 0 | 0 | 2147 | 7715 | $2.305 | temperature=0 | off |
| anthropic:claude-sonnet-4-5-20250929 | 714 | 0 | 0 | 0 | 0 | batch only |  | $5.810 | temperature=0 | off |
| anthropic:claude-sonnet-5 | 714 | 0 | 0 | 0 | 0 | 3467 | 6890 | $5.468 | provider_default | adaptive-low |
| local:qwen36-35b-mtplx | 714 | 0 | 0 | 307 | 0 | 5671 | 9732 | $0.000 | temperature=0 | off |
| local:qwen36-mtplx | 714 | 0 | 0 | 1 | 0 | 4077 | 5119 | $0.000 | temperature=0 | off |
| openai:gpt-5.4-mini | 714 | 0 | 0 | 0 | 0 | 2233 | 3253 | $2.372 | provider_default | effort-low |
| openai:gpt-5.5 | 714 | 0 | 0 | 0 | 0 | 2638 | 4777 | $14.141 | provider_default | effort-low |
| typesafe:jev-1.13.0 | 714 | 0 | 0 | 0 | 0 | 263 | 416 | $0.051 | n/a | n/a |

Not scored (coverage < 95%): anthropic:claude-haiku-4-5-20251001 (ksample5), anthropic:claude-opus-5, anthropic:claude-sonnet-4-5-20250929 (ksample5), openai:gpt-4.1
