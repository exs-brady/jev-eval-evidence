# Multi-judge comparison: crisis (dev)

- Model: `jev-1.13.0` (pinned), $0.042/Mtok input
- [partner]: `a2f566a+dirty` (lexicon vendored; see `src/jevlab/vendor/nav_lexicon.py`)
- [partner]: `7bf0a2c` (heuristics.py loaded live)
- Fixtures: see `fixtures/SOURCE.md`

## Crisis severity, dev split: 144 single messages + 24 arcs (231 turns), 7 contested

Under-triage = final level below the cell's intended level (arcs: highest level reached). False fire = any level on an intended-none item. 95% CIs: bootstrap, clustered by arc.

| Configuration | Under-triage | Exact level | False fire (none items) | Over-triage |
|---|---|---|---|---|
| lexicon floor | 0.506 [0.429, 0.577] | 0.452 [0.381, 0.530] | 0.054 [0.000, 0.119] | 0.036 [0.009, 0.076] |
| anthropic:claude-haiku-4-5-20251001 alone (argmax) | 0.018 [0.000, 0.042] | 0.935 [0.899, 0.970] | 0.000 [0.000, 0.000] | 0.071 [0.028, 0.120] |
| lexicon ∪ anthropic:claude-haiku-4-5-20251001 τ=0.2 | 0.018 [0.000, 0.042] | 0.881 [0.833, 0.929] | 0.054 [0.000, 0.119] | 0.125 [0.068, 0.190] |
| anthropic:claude-opus-5 alone (argmax) | 0.000 [0.000, 0.000] | 0.976 [0.952, 0.994] | 0.054 [0.000, 0.119] | 0.009 [0.000, 0.028] |
| lexicon ∪ anthropic:claude-opus-5 τ=0.5 | 0.000 [0.000, 0.000] | 0.935 [0.893, 0.970] | 0.107 [0.034, 0.194] | 0.045 [0.009, 0.087] |
| anthropic:claude-sonnet-4-5-20250929 alone (argmax) | 0.012 [0.000, 0.030] | 0.964 [0.935, 0.988] | 0.018 [0.000, 0.058] | 0.027 [0.000, 0.061] |
| lexicon ∪ anthropic:claude-sonnet-4-5-20250929 τ=0.2 | 0.000 [0.000, 0.000] | 0.851 [0.798, 0.905] | 0.071 [0.016, 0.145] | 0.188 [0.117, 0.263] |
| anthropic:claude-sonnet-5 alone (argmax) | 0.000 [0.000, 0.000] | 0.929 [0.887, 0.964] | 0.143 [0.056, 0.241] | 0.036 [0.008, 0.075] |
| lexicon ∪ anthropic:claude-sonnet-5 τ=0.5 | 0.000 [0.000, 0.000] | 0.893 [0.845, 0.940] | 0.179 [0.082, 0.278] | 0.071 [0.027, 0.126] |
| local:qwen36-mtplx alone (argmax) | 0.024 [0.006, 0.048] | 0.952 [0.917, 0.982] | 0.018 [0.000, 0.058] | 0.027 [0.000, 0.060] |
| lexicon ∪ local:qwen36-mtplx τ=0.1 | 0.000 [0.000, 0.000] | 0.613 [0.542, 0.690] | 0.071 [0.016, 0.145] | 0.545 [0.450, 0.636] |
| openai:gpt-4.1 alone (argmax) | 0.018 [0.000, 0.042] | 0.911 [0.863, 0.952] | 0.196 [0.094, 0.317] | 0.009 [0.000, 0.029] |
| lexicon ∪ openai:gpt-4.1 τ=0.05 | 0.000 [0.000, 0.000] | 0.506 [0.429, 0.589] | 0.232 [0.125, 0.351] | 0.625 [0.530, 0.714] |
| openai:gpt-5.4-mini alone (argmax) | 0.000 [0.000, 0.000] | 0.964 [0.935, 0.988] | 0.089 [0.018, 0.172] | 0.009 [0.000, 0.029] |
| lexicon ∪ openai:gpt-5.4-mini τ=0.3 | 0.000 [0.000, 0.000] | 0.917 [0.875, 0.952] | 0.143 [0.052, 0.245] | 0.054 [0.018, 0.101] |
| openai:gpt-5.5 alone (argmax) | 0.006 [0.000, 0.018] | 0.958 [0.923, 0.988] | 0.089 [0.021, 0.170] | 0.009 [0.000, 0.029] |
| lexicon ∪ openai:gpt-5.5 τ=0.2 | 0.006 [0.000, 0.018] | 0.905 [0.857, 0.946] | 0.143 [0.058, 0.241] | 0.062 [0.026, 0.110] |
| typesafe:jev-1.13.0 alone (argmax) | 0.000 [0.000, 0.000] | 0.988 [0.970, 1.000] | 0.036 [0.000, 0.094] | 0.000 [0.000, 0.000] |
| lexicon ∪ typesafe:jev-1.13.0 τ=0.5 | 0.000 [0.000, 0.000] | 0.940 [0.905, 0.976] | 0.107 [0.033, 0.196] | 0.036 [0.009, 0.076] |

### Paired differences vs lexicon ∪ Jev (same resampled arcs)

| Comparison | Metric | Difference [95% CI] | CI excludes 0 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 − Jev | under | 0.018 [0.000, 0.042] | no |
| anthropic:claude-haiku-4-5-20251001 − Jev | exact | -0.060 [-0.107, -0.018] | yes |
| anthropic:claude-opus-5 − Jev | under | 0.000 [0.000, 0.000] | no |
| anthropic:claude-opus-5 − Jev | exact | -0.006 [-0.030, 0.018] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | under | 0.000 [0.000, 0.000] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | exact | -0.089 [-0.137, -0.042] | yes |
| anthropic:claude-sonnet-5 − Jev | under | 0.000 [0.000, 0.000] | no |
| anthropic:claude-sonnet-5 − Jev | exact | -0.048 [-0.089, -0.012] | yes |
| local:qwen36-mtplx − Jev | under | 0.000 [0.000, 0.000] | no |
| local:qwen36-mtplx − Jev | exact | -0.327 [-0.405, -0.250] | yes |
| openai:gpt-4.1 − Jev | under | 0.000 [0.000, 0.000] | no |
| openai:gpt-4.1 − Jev | exact | -0.435 [-0.512, -0.357] | yes |
| openai:gpt-5.4-mini − Jev | under | 0.000 [0.000, 0.000] | no |
| openai:gpt-5.4-mini − Jev | exact | -0.024 [-0.054, 0.000] | no |
| openai:gpt-5.5 − Jev | under | 0.006 [0.000, 0.018] | no |
| openai:gpt-5.5 − Jev | exact | -0.036 [-0.071, 0.000] | no |

### Calibration, P(any risk) vs intended, single messages (compare within an elicitation only)

| Judge | Elicitation | n | Brier | ECE |
|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 (ksample5) | ksample5 | 0/144 | not scored (coverage) |  |
| anthropic:claude-haiku-4-5-20251001 | verbalised | 144 | 0.008 | 0.040 |
| anthropic:claude-opus-5 | verbalised | 144 | 0.014 | 0.061 |
| anthropic:claude-sonnet-4-5-20250929 (ksample5) | ksample5 | 0/144 | not scored (coverage) |  |
| anthropic:claude-sonnet-4-5-20250929 | verbalised | 144 | 0.007 | 0.033 |
| anthropic:claude-sonnet-5 | verbalised | 144 | 0.028 | 0.069 |
| local:qwen36-35b-mtplx | verbalised | 7/144 | not scored (coverage) |  |
| local:qwen36-mtplx | verbalised | 144 | 0.007 | 0.019 |
| openai:gpt-4.1 | verbalised | 144 | 0.047 | 0.046 |
| openai:gpt-5.4-mini | verbalised | 144 | 0.027 | 0.030 |
| openai:gpt-5.5 | verbalised | 144 | 0.015 | 0.043 |
| typesafe:jev-1.13.0 | native | 144 | 0.008 | 0.026 |

### Under-triage by generator family and contested flag (policy row)

| Judge | Slice | n | Under-triage |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | generated by anthropic | 84 | 0.012 [0.000, 0.036] |
| anthropic:claude-haiku-4-5-20251001 | generated by openai | 84 | 0.024 [0.000, 0.060] |
| anthropic:claude-haiku-4-5-20251001 | uncontested only | 161 | 0.012 [0.000, 0.031] |
| anthropic:claude-opus-5 | generated by anthropic | 84 | 0.000 [0.000, 0.000] |
| anthropic:claude-opus-5 | generated by openai | 84 | 0.000 [0.000, 0.000] |
| anthropic:claude-opus-5 | uncontested only | 161 | 0.000 [0.000, 0.000] |
| anthropic:claude-sonnet-4-5-20250929 | generated by anthropic | 84 | 0.000 [0.000, 0.000] |
| anthropic:claude-sonnet-4-5-20250929 | generated by openai | 84 | 0.000 [0.000, 0.000] |
| anthropic:claude-sonnet-4-5-20250929 | uncontested only | 161 | 0.000 [0.000, 0.000] |
| anthropic:claude-sonnet-5 | generated by anthropic | 84 | 0.000 [0.000, 0.000] |
| anthropic:claude-sonnet-5 | generated by openai | 84 | 0.000 [0.000, 0.000] |
| anthropic:claude-sonnet-5 | uncontested only | 161 | 0.000 [0.000, 0.000] |
| local:qwen36-mtplx | generated by anthropic | 84 | 0.000 [0.000, 0.000] |
| local:qwen36-mtplx | generated by openai | 84 | 0.000 [0.000, 0.000] |
| local:qwen36-mtplx | uncontested only | 161 | 0.000 [0.000, 0.000] |
| openai:gpt-4.1 | generated by anthropic | 84 | 0.000 [0.000, 0.000] |
| openai:gpt-4.1 | generated by openai | 84 | 0.000 [0.000, 0.000] |
| openai:gpt-4.1 | uncontested only | 161 | 0.000 [0.000, 0.000] |
| openai:gpt-5.4-mini | generated by anthropic | 84 | 0.000 [0.000, 0.000] |
| openai:gpt-5.4-mini | generated by openai | 84 | 0.000 [0.000, 0.000] |
| openai:gpt-5.4-mini | uncontested only | 161 | 0.000 [0.000, 0.000] |
| openai:gpt-5.5 | generated by anthropic | 84 | 0.000 [0.000, 0.000] |
| openai:gpt-5.5 | generated by openai | 84 | 0.012 [0.000, 0.036] |
| openai:gpt-5.5 | uncontested only | 161 | 0.006 [0.000, 0.019] |
| typesafe:jev-1.13.0 | generated by anthropic | 84 | 0.000 [0.000, 0.000] |
| typesafe:jev-1.13.0 | generated by openai | 84 | 0.000 [0.000, 0.000] |
| typesafe:jev-1.13.0 | uncontested only | 161 | 0.000 [0.000, 0.000] |

### Operations

| Judge | Calls | Parse failed | Errors | Re-asked | Unwrapped (A6) | p50 ms | p95 ms | USD/1k | Sampling | Reasoning |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 231 | 0 | 0 | 0 | 0 | 1251 | 2407 | $1.536 | temperature=0 | off |
| anthropic:claude-opus-5 | 231 | 0 | 0 | 0 | 0 | 2843 | 4740 | $9.222 | provider_default | adaptive-low |
| anthropic:claude-sonnet-4-5-20250929 | 231 | 0 | 0 | 0 | 0 | 2151 | 2439 | $4.462 | temperature=0 | off |
| anthropic:claude-sonnet-5 | 231 | 0 | 0 | 0 | 0 | 2156 | 3466 | $3.689 | provider_default | adaptive-low |
| local:qwen36-mtplx | 231 | 0 | 0 | 0 | 0 | 1989 | 2185 | $0.000 | temperature=0 | off |
| openai:gpt-4.1 | 231 | 0 | 0 | 0 | 0 | 3136 | 7610 | $1.951 | temperature=0 | off |
| openai:gpt-5.4-mini | 231 | 0 | 0 | 0 | 0 | 1412 | 2146 | $1.026 | provider_default | effort-low |
| openai:gpt-5.5 | 231 | 0 | 0 | 0 | 0 | 2420 | 3712 | $7.106 | provider_default | effort-low |
| typesafe:jev-1.13.0 | 231 | 0 | 0 | 0 | 0 | 275 | 382 | $0.031 | n/a | n/a |

Not scored (coverage < 95%): anthropic:claude-haiku-4-5-20251001 (ksample5), anthropic:claude-sonnet-4-5-20250929 (ksample5), local:qwen36-35b-mtplx
