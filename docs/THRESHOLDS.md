# Frozen thresholds

Chosen on the dev split by the rule in docs/PREREGISTRATION.md, then frozen. Test-split reports read this file and never re-tune.

`rule` = a τ met the false-fire constraint. `fallback` = none did, so the τ with the lowest dev false-fire was taken; that row's τ is **not** a product of the pre-registered rule.

## crisis

| Judge | τ / grace | dev false-fire | dev criterion | Chosen by |
|---|---|---|---|---|
| local:qwen36-mtplx | 0.1 | 0.071 | 0.000 | fallback |
| openai:gpt-4.1 | 0.05 | 0.232 | 0.000 | fallback |
| openai:gpt-5.4-mini | 0.3 | 0.143 | 0.000 | fallback |
| openai:gpt-5.5 | 0.2 | 0.143 | 0.006 | fallback |
| anthropic:claude-haiku-4-5-20251001 | 0.2 | 0.054 | 0.018 | rule |
| anthropic:claude-opus-5 | 0.5 | 0.107 | 0.000 | fallback |
| anthropic:claude-sonnet-4-5-20250929 | 0.2 | 0.071 | 0.000 | fallback |
| anthropic:claude-sonnet-5 | 0.5 | 0.179 | 0.000 | fallback |
| typesafe:jev-1.13.0 | 0.5 | 0.107 | 0.000 | fallback |

Floor false-fire on dev: 0.054. Rule: lowest τ with dev false-fire ≤ floor's, tie → lower under-triage; fallback = lowest false-fire

Chosen by the fallback, not the rule: 8 of 9.

## trainee

| Judge | τ / grace | dev false-fire | dev criterion | Chosen by |
|---|---|---|---|---|
| local:qwen36-mtplx | 0.3 | 0.000 | 0.992 | rule |
| openai:gpt-4.1 | 0.3 | 0.008 | 0.992 | fallback |
| openai:gpt-5.4-mini | 0.7 | 0.017 | 0.984 | fallback |
| openai:gpt-5.5 | 0.3 | 0.000 | 1.000 | rule |
| anthropic:claude-haiku-4-5-20251001 | 0.3 | 0.000 | 1.000 | rule |
| anthropic:claude-opus-5 | 0.7 | 0.000 | 0.992 | rule |
| anthropic:claude-sonnet-4-5-20250929 | 0.3 | 0.008 | 0.992 | fallback |
| anthropic:claude-sonnet-5 | 0.3 | 0.000 | 1.000 | rule |
| typesafe:jev-1.13.0 | 0.5 | 0.000 | 1.000 | rule |

Floor false-fire on dev: 0.000. Rule: lowest τ with dev false-flag ≤ floor's, tie → higher F1; fallback = lowest false-flag

Chosen by the fallback, not the rule: 3 of 9.

## omission

| Judge | τ / grace | dev false-fire | dev criterion | Chosen by |
|---|---|---|---|---|
| local:qwen36-mtplx | 2 | 0.000 | 1.000 | rule |
| openai:gpt-4.1 | 2 | 0.000 | 0.958 | rule |
| openai:gpt-5.4-mini | 2 | 0.000 | 0.917 | rule |
| openai:gpt-5.5 | 2 | 0.000 | 0.917 | rule |
| anthropic:claude-haiku-4-5-20251001 | 2 | 0.000 | 0.958 | rule |
| anthropic:claude-opus-5 | 2 | 0.000 | 1.000 | rule |
| anthropic:claude-sonnet-4-5-20250929 | 2 | 0.000 | 1.000 | rule |
| anthropic:claude-sonnet-5 | 2 | 0.000 | 1.000 | rule |
| typesafe:jev-1.13.0 | 2 | 0.000 | 1.000 | rule |

Floor false-fire on dev: 0.000. Rule: grace with highest dev accuracy, tie → smaller

Chosen by the fallback, not the rule: 0 of 9.
