# Multi-judge comparison: trainee (dev)

- Model: `jev-1.13.0` (pinned), $0.042/Mtok input
- [partner]: `a2f566a+dirty` (lexicon vendored; see `src/jevlab/vendor/nav_lexicon.py`)
- [partner]: `7bf0a2c` (heuristics.py loaded live)
- Fixtures: see `fixtures/SOURCE.md`

## Trainee conduct, dev split: 180 replies (60 positives, 60 near-miss negatives, 60 clean), 0 contested

F1 over all replies for their cell's harm; false flag = flagged on a negative. 95% CIs: bootstrap over replies.

| Configuration | F1 | Recall | False flag (all negatives) | False flag (near-miss) |
|---|---|---|---|---|
| regex floor | 0.378 [0.229, 0.511] | 0.233 [0.129, 0.343] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| anthropic:claude-haiku-4-5-20251001 alone (p ≥ 0.5) | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| regex ∪ anthropic:claude-haiku-4-5-20251001 τ=0.3 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| anthropic:claude-opus-5 alone (p ≥ 0.5) | 0.984 [0.957, 1.000] | 1.000 [1.000, 1.000] | 0.017 [0.000, 0.043] | 0.017 [0.000, 0.056] |
| regex ∪ anthropic:claude-opus-5 τ=0.7 | 0.992 [0.972, 1.000] | 0.983 [0.946, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| anthropic:claude-sonnet-4-5-20250929 alone (p ≥ 0.5) | 0.992 [0.973, 1.000] | 1.000 [1.000, 1.000] | 0.008 [0.000, 0.026] | 0.017 [0.000, 0.054] |
| regex ∪ anthropic:claude-sonnet-4-5-20250929 τ=0.3 | 0.992 [0.973, 1.000] | 1.000 [1.000, 1.000] | 0.008 [0.000, 0.026] | 0.017 [0.000, 0.054] |
| anthropic:claude-sonnet-5 alone (p ≥ 0.5) | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| regex ∪ anthropic:claude-sonnet-5 τ=0.3 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| local:qwen36-mtplx alone (p ≥ 0.5) | 0.983 [0.955, 1.000] | 0.967 [0.914, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| regex ∪ local:qwen36-mtplx τ=0.3 | 0.992 [0.972, 1.000] | 0.983 [0.946, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| openai:gpt-4.1 alone (p ≥ 0.5) | 0.992 [0.972, 1.000] | 1.000 [1.000, 1.000] | 0.008 [0.000, 0.026] | 0.017 [0.000, 0.055] |
| regex ∪ openai:gpt-4.1 τ=0.3 | 0.992 [0.972, 1.000] | 1.000 [1.000, 1.000] | 0.008 [0.000, 0.026] | 0.017 [0.000, 0.055] |
| openai:gpt-5.4-mini alone (p ≥ 0.5) | 0.976 [0.941, 1.000] | 1.000 [1.000, 1.000] | 0.025 [0.000, 0.057] | 0.050 [0.000, 0.113] |
| regex ∪ openai:gpt-5.4-mini τ=0.7 | 0.984 [0.957, 1.000] | 1.000 [1.000, 1.000] | 0.017 [0.000, 0.042] | 0.033 [0.000, 0.085] |
| openai:gpt-5.5 alone (p ≥ 0.5) | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| regex ∪ openai:gpt-5.5 τ=0.3 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| typesafe:jev-1.13.0 alone (p ≥ 0.5) | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| regex ∪ typesafe:jev-1.13.0 τ=0.5 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

### Paired differences vs regex ∪ Jev

| Comparison | Metric | Difference [95% CI] | CI excludes 0 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 − Jev | f1 | 0.000 [0.000, 0.000] | no |
| anthropic:claude-haiku-4-5-20251001 − Jev | false_flag | 0.000 [0.000, 0.000] | no |
| anthropic:claude-opus-5 − Jev | f1 | -0.008 [-0.028, 0.000] | no |
| anthropic:claude-opus-5 − Jev | false_flag | 0.000 [0.000, 0.000] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | f1 | -0.008 [-0.027, 0.000] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | false_flag | 0.008 [0.000, 0.026] | no |
| anthropic:claude-sonnet-5 − Jev | f1 | 0.000 [0.000, 0.000] | no |
| anthropic:claude-sonnet-5 − Jev | false_flag | 0.000 [0.000, 0.000] | no |
| local:qwen36-mtplx − Jev | f1 | -0.008 [-0.028, 0.000] | no |
| local:qwen36-mtplx − Jev | false_flag | 0.000 [0.000, 0.000] | no |
| openai:gpt-4.1 − Jev | f1 | -0.008 [-0.028, 0.000] | no |
| openai:gpt-4.1 − Jev | false_flag | 0.008 [0.000, 0.026] | no |
| openai:gpt-5.4-mini − Jev | f1 | -0.016 [-0.043, 0.000] | no |
| openai:gpt-5.4-mini − Jev | false_flag | 0.017 [0.000, 0.042] | no |
| openai:gpt-5.5 − Jev | f1 | 0.000 [0.000, 0.000] | no |
| openai:gpt-5.5 − Jev | false_flag | 0.000 [0.000, 0.000] | no |

### Per-harm F1 (policy rows)

| Harm | n | regex | anthropic:claude-haiku-4-5-20251001 | anthropic:claude-opus-5 | anthropic:claude-sonnet-4-5-20250929 | anthropic:claude-sonnet-5 | local:qwen36-mtplx | openai:gpt-4.1 | openai:gpt-5.4-mini | openai:gpt-5.5 | typesafe:jev-1.13.0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| boundary | 18 | 0.29 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| false_reassurance | 18 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| interrogation | 18 | 0.67 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| judged | 18 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| leading | 18 | 0.67 | 1.00 | 0.91 | 1.00 | 1.00 | 0.91 | 1.00 | 1.00 | 1.00 | 1.00 |
| logistics | 18 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| minimize | 18 | 0.29 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.92 | 1.00 | 1.00 |
| moralizing | 18 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| secrecy | 18 | 0.50 | 1.00 | 1.00 | 0.92 | 1.00 | 1.00 | 1.00 | 0.92 | 1.00 | 1.00 |
| stated_feelings | 18 | 0.80 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.92 | 1.00 | 1.00 | 1.00 |

### Calibration, P(harm) vs intended (compare within an elicitation only)

| Judge | Elicitation | n | Brier | ECE |
|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 (ksample5) | ksample5 | 0/180 | not scored (coverage) |  |
| anthropic:claude-haiku-4-5-20251001 | verbalised | 180 | 0.008 | 0.069 |
| anthropic:claude-opus-5 | verbalised | 180 | 0.007 | 0.042 |
| anthropic:claude-sonnet-4-5-20250929 (ksample5) | ksample5 | 0/180 | not scored (coverage) |  |
| anthropic:claude-sonnet-4-5-20250929 | verbalised | 180 | 0.007 | 0.023 |
| anthropic:claude-sonnet-5 | verbalised | 180 | 0.006 | 0.052 |
| local:qwen36-35b-mtplx | verbalised | 2/180 | not scored (coverage) |  |
| local:qwen36-mtplx | verbalised | 180 | 0.012 | 0.023 |
| openai:gpt-4.1 | verbalised | 180 | 0.006 | 0.015 |
| openai:gpt-5.4-mini | verbalised | 180 | 0.015 | 0.031 |
| openai:gpt-5.5 | verbalised | 180 | 0.002 | 0.023 |
| typesafe:jev-1.13.0 | native | 180 | 0.005 | 0.046 |

### F1 by generator family and contested flag (policy row)

| Judge | Slice | n | F1 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | generated by anthropic | 90 | 1.000 [1.000, 1.000] |
| anthropic:claude-haiku-4-5-20251001 | generated by openai | 90 | 1.000 [1.000, 1.000] |
| anthropic:claude-haiku-4-5-20251001 | uncontested only | 180 | 1.000 [1.000, 1.000] |
| anthropic:claude-opus-5 | generated by anthropic | 90 | 0.983 [0.939, 1.000] |
| anthropic:claude-opus-5 | generated by openai | 90 | 1.000 [1.000, 1.000] |
| anthropic:claude-opus-5 | uncontested only | 180 | 0.992 [0.971, 1.000] |
| anthropic:claude-sonnet-4-5-20250929 | generated by anthropic | 90 | 0.984 [0.943, 1.000] |
| anthropic:claude-sonnet-4-5-20250929 | generated by openai | 90 | 1.000 [1.000, 1.000] |
| anthropic:claude-sonnet-4-5-20250929 | uncontested only | 180 | 0.992 [0.973, 1.000] |
| anthropic:claude-sonnet-5 | generated by anthropic | 90 | 1.000 [1.000, 1.000] |
| anthropic:claude-sonnet-5 | generated by openai | 90 | 1.000 [1.000, 1.000] |
| anthropic:claude-sonnet-5 | uncontested only | 180 | 1.000 [1.000, 1.000] |
| local:qwen36-mtplx | generated by anthropic | 90 | 0.983 [0.939, 1.000] |
| local:qwen36-mtplx | generated by openai | 90 | 1.000 [1.000, 1.000] |
| local:qwen36-mtplx | uncontested only | 180 | 0.992 [0.971, 1.000] |
| openai:gpt-4.1 | generated by anthropic | 90 | 0.984 [0.945, 1.000] |
| openai:gpt-4.1 | generated by openai | 90 | 1.000 [1.000, 1.000] |
| openai:gpt-4.1 | uncontested only | 180 | 0.992 [0.972, 1.000] |
| openai:gpt-5.4-mini | generated by anthropic | 90 | 0.968 [0.912, 1.000] |
| openai:gpt-5.4-mini | generated by openai | 90 | 1.000 [1.000, 1.000] |
| openai:gpt-5.4-mini | uncontested only | 180 | 0.984 [0.955, 1.000] |
| openai:gpt-5.5 | generated by anthropic | 90 | 1.000 [1.000, 1.000] |
| openai:gpt-5.5 | generated by openai | 90 | 1.000 [1.000, 1.000] |
| openai:gpt-5.5 | uncontested only | 180 | 1.000 [1.000, 1.000] |
| typesafe:jev-1.13.0 | generated by anthropic | 90 | 1.000 [1.000, 1.000] |
| typesafe:jev-1.13.0 | generated by openai | 90 | 1.000 [1.000, 1.000] |
| typesafe:jev-1.13.0 | uncontested only | 180 | 1.000 [1.000, 1.000] |

### Operations

| Judge | Calls | Parse failed | Errors | Re-asked | Unwrapped (A6) | p50 ms | p95 ms | USD/1k | Sampling | Reasoning |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 180 | 0 | 0 | 0 | 0 | 3544 | 7711 | $4.043 | temperature=0 | off |
| anthropic:claude-opus-5 | 180 | 0 | 0 | 0 | 0 | 4240 | 6724 | $23.984 | provider_default | adaptive-low |
| anthropic:claude-sonnet-4-5-20250929 | 180 | 0 | 0 | 0 | 0 | 3703 | 4230 | $11.620 | temperature=0 | off |
| anthropic:claude-sonnet-5 | 180 | 0 | 0 | 0 | 0 | 3517 | 6770 | $9.594 | provider_default | adaptive-low |
| local:qwen36-mtplx | 180 | 0 | 0 | 0 | 0 | 4041 | 5036 | $0.000 | temperature=0 | off |
| openai:gpt-4.1 | 180 | 0 | 0 | 0 | 0 | 7042 | 86863 | $4.612 | temperature=0 | off |
| openai:gpt-5.4-mini | 180 | 0 | 0 | 0 | 0 | 2516 | 3783 | $2.387 | provider_default | effort-low |
| openai:gpt-5.5 | 180 | 0 | 0 | 0 | 0 | 2776 | 5201 | $14.148 | provider_default | effort-low |
| typesafe:jev-1.13.0 | 180 | 0 | 0 | 0 | 0 | 264 | 404 | $0.051 | n/a | n/a |

Not scored (coverage < 95%): anthropic:claude-haiku-4-5-20251001 (ksample5), anthropic:claude-sonnet-4-5-20250929 (ksample5), local:qwen36-35b-mtplx
