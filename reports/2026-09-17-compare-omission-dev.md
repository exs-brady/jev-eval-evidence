# Multi-judge comparison: omission (dev)

- Model: `jev-1.13.0` (pinned), $0.042/Mtok input
- [partner]: `a2f566a+dirty` (lexicon vendored; see `src/jevlab/vendor/nav_lexicon.py`)
- [partner]: `7bf0a2c` (heuristics.py loaded live)
- Fixtures: see `fixtures/SOURCE.md`

## Omission (never asked directly), dev split: 24 arcs, 0 contested

Fires when a disclosure has happened (regex or P(disclosed) ≥ 0.5) and `grace` trainee turns pass with P(asked directly) < 0.5. Accuracy = fired iff the arc's cell says the trainee never asks. The regex floor has no omission detector.

| Judge | Arcs | Accuracy | False fire (asks arcs) |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001, grace 2 | 24 | 0.958 [0.875, 1.000] | 0.000 [0.000, 0.000] |
| anthropic:claude-opus-5, grace 2 | 24 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] |
| anthropic:claude-sonnet-4-5-20250929, grace 2 | 24 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] |
| anthropic:claude-sonnet-5, grace 2 | 24 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] |
| local:qwen36-mtplx, grace 2 | 24 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] |
| openai:gpt-4.1, grace 2 | 24 | 0.958 [0.875, 1.000] | 0.000 [0.000, 0.000] |
| openai:gpt-5.4-mini, grace 2 | 24 | 0.917 [0.792, 1.000] | 0.000 [0.000, 0.000] |
| openai:gpt-5.5, grace 2 | 24 | 0.917 [0.792, 1.000] | 0.000 [0.000, 0.000] |
| typesafe:jev-1.13.0, grace 2 | 24 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] |

### Paired differences vs Jev

| Comparison | Metric | Difference [95% CI] | CI excludes 0 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 − Jev | accuracy | -0.042 [-0.125, 0.000] | no |
| anthropic:claude-opus-5 − Jev | accuracy | 0.000 [0.000, 0.000] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | accuracy | 0.000 [0.000, 0.000] | no |
| anthropic:claude-sonnet-5 − Jev | accuracy | 0.000 [0.000, 0.000] | no |
| local:qwen36-mtplx − Jev | accuracy | 0.000 [0.000, 0.000] | no |
| openai:gpt-4.1 − Jev | accuracy | -0.042 [-0.125, 0.000] | no |
| openai:gpt-5.4-mini − Jev | accuracy | -0.083 [-0.208, 0.000] | no |
| openai:gpt-5.5 − Jev | accuracy | -0.083 [-0.208, 0.000] | no |

### Accuracy by arc type

| Arc type | n | anthropic:claude-haiku-4-5-20251001 | anthropic:claude-opus-5 | anthropic:claude-sonnet-4-5-20250929 | anthropic:claude-sonnet-5 | local:qwen36-mtplx | openai:gpt-4.1 | openai:gpt-5.4-mini | openai:gpt-5.5 | typesafe:jev-1.13.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| never | 8 | 0.88 | 1.00 | 1.00 | 1.00 | 1.00 | 0.88 | 0.75 | 0.75 | 1.00 |
| immediately | 8 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| after_validating | 8 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
