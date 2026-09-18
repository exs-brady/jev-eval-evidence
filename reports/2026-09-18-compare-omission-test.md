# Multi-judge comparison: omission (test)

- Model: `jev-1.13.0` (pinned), $0.042/Mtok input
- [partner]: `a2f566a+dirty` (lexicon vendored; see `src/jevlab/vendor/nav_lexicon.py`)
- [partner]: `7bf0a2c` (heuristics.py loaded live)
- Fixtures: see `fixtures/SOURCE.md`

## Omission (never asked directly), test split: 98 arcs, 4 contested

> **Every number in this section is an upper bound.** The generator prompt was handed the same level
> descriptions the judges are scored on applying, sharing whole level names verbatim
> (`synth/generate.py`, line 39), so the items encode the answers. The inflation is not uniform:
> it most rewards whichever judge follows a written criterion most literally. The blind-authored
> arcs and AnnoMI carry the findings instead; see `reports/2026-09-18-clean-subset-audit.md`.

Fires when a disclosure has happened (regex or P(disclosed) ≥ 0.5) and `grace` trainee turns pass with P(asked directly) < 0.5. Accuracy = fired iff the arc's cell says the trainee never asks. The regex floor has no omission detector.

| Judge | Arcs | Accuracy | False fire (asks arcs) |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001, grace 2 | 98 | 0.980 [0.949, 1.000] | 0.000 [0.000, 0.000] |
| anthropic:claude-sonnet-4-5-20250929, grace 2 | 98 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] |
| anthropic:claude-sonnet-5, grace 2 | 98 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] |
| local:qwen36-35b-mtplx (no frozen grace) | 98 | not scored |  |
| local:qwen36-mtplx, grace 2 | 98 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] |
| openai:gpt-5.4-mini, grace 2 | 98 | 0.867 [0.796, 0.929] | 0.000 [0.000, 0.000] |
| typesafe:jev-1.13.0, grace 2 | 98 | 0.990 [0.969, 1.000] | 0.000 [0.000, 0.000] |

### Paired differences vs Jev

| Comparison | Metric | Difference [95% CI] | CI excludes 0 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 − Jev | accuracy | -0.010 [-0.051, 0.020] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | accuracy | 0.010 [0.000, 0.031] | no |
| anthropic:claude-sonnet-5 − Jev | accuracy | 0.010 [0.000, 0.031] | no |
| local:qwen36-mtplx − Jev | accuracy | 0.010 [0.000, 0.031] | no |
| openai:gpt-5.4-mini − Jev | accuracy | -0.122 [-0.194, -0.051] | yes |

### Accuracy by arc type

| Arc type | n | anthropic:claude-haiku-4-5-20251001 | anthropic:claude-sonnet-4-5-20250929 | anthropic:claude-sonnet-5 | local:qwen36-mtplx | openai:gpt-5.4-mini | typesafe:jev-1.13.0 |
|---|---|---|---|---|---|---|---|
| never | 34 | 0.94 | 1.00 | 1.00 | 1.00 | 0.62 | 0.97 |
| immediately | 32 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| after_validating | 32 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

Not scored (coverage < 95%): anthropic:claude-opus-5, openai:gpt-4.1, openai:gpt-5.5
