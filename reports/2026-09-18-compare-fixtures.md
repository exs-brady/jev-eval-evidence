# All judges on the phase-1 clinical fixtures

- Model: `jev-1.13.0` (pinned), $0.042/Mtok input
- [partner]: `a2f566a+dirty` (lexicon vendored; see `src/jevlab/vendor/nav_lexicon.py`)
- [partner]: `7bf0a2c` (heuristics.py loaded live)
- Fixtures: see `fixtures/SOURCE.md`

## Crisis severity: [partner] clinical fixtures (86 bank phrases, 84 Set A arcs)

Same scorer as the phase-1 report. Every judge receives the identical questions; the incumbent row is [partner]'s own prompt.

| Configuration | Bank recall | Bank false fires | Bank exact | Bank under | Arc exact | Arc under | Arc over | First-response under |
|---|---|---|---|---|---|---|---|---|
| lexicon floor | 60/60 | 0/26 | 59/60 | 0 | 26/84 | 55 | 3 | 36/51 |
| lexicon ∪ Sonnet 4.5 ([partner] incumbent, its own prompt) | 60/60 | 0/26 | 54/60 | 0 | 69/84 | 5 | 10 | 5/51 |
| anthropic:claude-haiku-4-5-20251001 alone (argmax) | 60/60 | 0/26 | 50/60 | 6 | 74/84 | 8 | 2 | 6/51 |
| lexicon ∪ anthropic:claude-haiku-4-5-20251001 τ=0.2 | 60/60 | 0/26 | 55/60 | 0 | 73/84 | 7 | 4 | 6/51 |
| anthropic:claude-opus-5 alone (argmax) | 60/60 | 2/26 | 55/60 | 3 | 77/84 | 3 | 4 | 7/51 |
| lexicon ∪ anthropic:claude-opus-5 τ=0.2 | 60/60 | 6/26 | 46/60 | 0 | 61/84 | 0 | 23 | 10/51 |
| anthropic:claude-sonnet-4-5-20250929 alone (argmax) | 60/60 | 0/26 | 51/60 | 6 | 66/84 | 15 | 3 | 11/51 |
| lexicon ∪ anthropic:claude-sonnet-4-5-20250929 τ=0.2 | 60/60 | 0/26 | 47/60 | 0 | 62/84 | 10 | 12 | 7/51 |
| anthropic:claude-sonnet-5 alone (argmax) | 60/60 | 1/26 | 54/60 | 1 | 73/84 | 3 | 8 | 6/51 |
| lexicon ∪ anthropic:claude-sonnet-5 τ=0.2 | 60/60 | 1/26 | 38/60 | 0 | 48/84 | 0 | 36 | 7/51 |
| local:qwen36-35b-mtplx alone (argmax) | 60/60 | 2/26 | 47/60 | 6 | 70/84 | 6 | 8 | 8/51 |
| lexicon ∪ local:qwen36-35b-mtplx τ=0.2 | 60/60 | 2/26 | 51/60 | 0 | 68/84 | 6 | 10 | 8/51 |
| local:qwen36-mtplx alone (argmax) | 60/60 | 0/26 | 50/60 | 6 | 70/84 | 10 | 4 | 11/51 |
| lexicon ∪ local:qwen36-mtplx τ=0.2 | 60/60 | 0/26 | 53/60 | 0 | 67/84 | 10 | 7 | 12/51 |
| openai:gpt-4.1 alone (argmax) | 60/60 | 2/26 | 46/60 | 13 | 71/84 | 9 | 4 | 12/51 |
| lexicon ∪ openai:gpt-4.1 τ=0.2 | 60/60 | 2/26 | 58/60 | 0 | 69/84 | 9 | 6 | 12/51 |
| openai:gpt-5.4-mini alone (argmax) | 59/60 | 2/26 | 52/60 | 7 | 69/84 | 9 | 6 | 8/51 |
| lexicon ∪ openai:gpt-5.4-mini τ=0.2 | 60/60 | 2/26 | 58/60 | 0 | 70/84 | 7 | 7 | 9/51 |
| openai:gpt-5.5 alone (argmax) | 60/60 | 1/26 | 48/60 | 10 | 72/84 | 6 | 6 | 8/51 |
| lexicon ∪ openai:gpt-5.5 τ=0.2 | 60/60 | 1/26 | 57/60 | 0 | 72/84 | 5 | 7 | 6/51 |
| typesafe:jev-1.13.0 alone (argmax) | 58/60 | 0/26 | 42/60 | 15 | 66/84 | 13 | 5 | 11/51 |
| lexicon ∪ typesafe:jev-1.13.0 τ=0.2 | 60/60 | 0/26 | 57/60 | 0 | 69/84 | 5 | 10 | 7/51 |

### Set A arcs: exactness across the threshold ladder, judge alone

Each judge's arc accuracy at every pre-registered threshold and at its own best answer. The span is best minus worst: a small span means the safety dial can be turned without changing what the judge does, a large one means safety and accuracy are the same dial.

| Judge | τ=0.05 | τ=0.1 | τ=0.2 | τ=0.3 | τ=0.5 | argmax | Span |
|---|---|---|---|---|---|---|---|
| typesafe:jev-1.13.0 | 67/84 | 70/84 | 70/84 | 69/84 | 66/84 | 66/84 | 4 |
| openai:gpt-5.4-mini | 38/84 | 69/84 | 71/84 | 70/84 | 68/84 | 69/84 | 33 |
| openai:gpt-5.5 | 33/84 | 67/84 | 73/84 | 72/84 | 72/84 | 72/84 | 40 |
| anthropic:claude-sonnet-4-5-20250929 | 25/84 | 38/84 | 63/84 | 66/84 | 66/84 | 66/84 | 41 |
| openai:gpt-4.1 | 27/84 | 46/84 | 70/84 | 71/84 | 71/84 | 71/84 | 44 |
| local:qwen36-mtplx | 22/84 | 39/84 | 68/84 | 70/84 | 70/84 | 70/84 | 48 |
| anthropic:claude-haiku-4-5-20251001 | 23/84 | 50/84 | 75/84 | 74/84 | 74/84 | 74/84 | 52 |
| local:qwen36-35b-mtplx | 18/84 | 42/84 | 69/84 | 70/84 | 70/84 | 70/84 | 52 |
| anthropic:claude-sonnet-5 | 10/84 | 18/84 | 48/84 | 70/84 | 73/84 | 73/84 | 63 |
| anthropic:claude-opus-5 | 13/84 | 32/84 | 62/84 | 73/84 | 76/84 | 77/84 | 64 |

### Shape of the probability output (all 305 fixture items)

Mass a judge places outside its own chosen level. Confident is below 0.05, genuinely unsure above 0.2; a judge with little of either hedges in a narrow band, which is what makes a threshold a cliff.

| Judge | Elicitation | n | Confident (<0.05) | Unsure (>0.2) | Median tail |
|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | verbalised | 305 | 21.6% | 0.3% | 0.050 |
| anthropic:claude-opus-5 | verbalised | 305 | 17.4% | 24.6% | 0.100 |
| anthropic:claude-sonnet-4-5-20250929 | verbalised | 305 | 32.8% | 2.6% | 0.080 |
| anthropic:claude-sonnet-5 | verbalised | 305 | 16.7% | 18.0% | 0.150 |
| local:qwen36-35b-mtplx | verbalised | 305 | 27.9% | 0.0% | 0.050 |
| local:qwen36-mtplx | verbalised | 305 | 21.6% | 0.0% | 0.050 |
| openai:gpt-4.1 | verbalised | 305 | 37.7% | 1.3% | 0.050 |
| openai:gpt-5.4-mini | verbalised | 305 | 49.8% | 5.2% | 0.050 |
| openai:gpt-5.5 | verbalised | 305 | 39.0% | 6.6% | 0.050 |
| typesafe:jev-1.13.0 | native | 305 | 67.9% | 16.1% | 0.010 |

### Operations

| Judge | Calls | Parse failed | Errors | p50 ms | p95 ms | USD/1k | Sampling | Reasoning |
|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 305 | 0 | 0 | 1317 | 2239 | $1.508 | temperature=0 | off |
| anthropic:claude-opus-5 | 305 | 0 | 0 | 2869 | 5426 | $9.073 | provider_default | adaptive-low |
| anthropic:claude-sonnet-4-5-20250929 | 305 | 0 | 0 | 2208 | 2586 | $4.367 | temperature=0 | off |
| anthropic:claude-sonnet-5 | 305 | 0 | 0 | 2208 | 3128 | $3.612 | provider_default | adaptive-low |
| local:qwen36-35b-mtplx | 305 | 0 | 0 | 2398 | 2548 | $0.000 | temperature=0 | off |
| local:qwen36-mtplx | 305 | 0 | 0 | 3866 | 9859 | $0.000 | temperature=0 | off |
| openai:gpt-4.1 | 305 | 0 | 0 | 1928 | 4887 | $1.909 | temperature=0 | off |
| openai:gpt-5.4-mini | 305 | 0 | 0 | 1272 | 2120 | $1.048 | provider_default | effort-low |
| openai:gpt-5.5 | 305 | 0 | 0 | 2373 | 3764 | $7.408 | provider_default | effort-low |
| typesafe:jev-1.13.0 | 305 | 0 | 0 | 276 | 374 | $0.030 | n/a | n/a |

## Trainee conduct: [partner] clinical fixtures + supplementary paraphrases

Regex floor OR judge p ≥ 0.7, the phase-1 headline threshold, applied to every judge alike.

| Configuration | Guard caught (13, clinical) | Guard false flags | Extra caught (60, unreviewed) | Extra false flags | Misconduct arcs flagged | Flags on good-practice control |
|---|---|---|---|---|---|---|
| regex floor | 6/7 | 0/6 | 3/30 | 0/30 | 8/8 | 0 |
| regex ∪ anthropic:claude-haiku-4-5-20251001 τ=0.7 | 7/7 | 1/6 | 30/30 | 0/30 | 8/8 | 0 |
| regex ∪ anthropic:claude-opus-5 τ=0.7 | 7/7 | 0/6 | 30/30 | 0/30 | 8/8 | 0 |
| regex ∪ anthropic:claude-sonnet-4-5-20250929 τ=0.7 | 7/7 | 1/6 | 30/30 | 0/30 | 8/8 | 0 |
| regex ∪ anthropic:claude-sonnet-5 τ=0.7 | 7/7 | 1/6 | 30/30 | 0/30 | 8/8 | 0 |
| regex ∪ local:qwen36-35b-mtplx τ=0.7 | 7/7 | 1/6 | 30/30 | 1/30 | 8/8 | 0 |
| regex ∪ local:qwen36-mtplx τ=0.7 | 7/7 | 0/6 | 30/30 | 0/30 | 8/8 | 0 |
| regex ∪ openai:gpt-4.1 τ=0.7 | 7/7 | 0/6 | 30/30 | 0/30 | 8/8 | 0 |
| regex ∪ openai:gpt-5.4-mini τ=0.7 | 7/7 | 0/6 | 29/30 | 4/30 | 8/8 | 0 |
| regex ∪ openai:gpt-5.5 τ=0.7 | 7/7 | 0/6 | 30/30 | 0/30 | 8/8 | 0 |
| regex ∪ typesafe:jev-1.13.0 τ=0.7 | 7/7 | 0/6 | 30/30 | 0/30 | 8/8 | 0 |
