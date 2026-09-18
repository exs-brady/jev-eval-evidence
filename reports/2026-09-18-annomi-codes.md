# AnnoMI utterance coding: judges vs expert majority

- Model: `jev-1.13.0` (pinned), $0.042/Mtok input
- [partner]: `a2f566a+dirty` (lexicon vendored; see `src/jevlab/vendor/nav_lexicon.py`)
- [partner]: `7bf0a2c` (heuristics.py loaded live)
- Fixtures: see `fixtures/SOURCE.md`

## behaviour: local sample (555 utterances; 543 with a gold label; 12 contested)

Of the 543 gold labels, **204 come from a ten-coder majority and 339 from a single coder** (62% of the total). AnnoMI codes most of its corpus once; only 428 utterances carry all ten annotators. The pooled AC1 column below is therefore mostly agreement with one arbitrary coder, whose own agreement with colleagues averages 0.74. The consensus-only column is the like-for-like expert comparison.

| Judge | n | AC1 vs pooled gold [95% CI, transcript-clustered] | AC1 CI (channel-clustered) | AC1 vs 10-coder gold | Kappa | Accuracy | Macro-F1 |
|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 543 | 0.792 [0.742, 0.837] | [0.742, 0.847] | 0.876 [0.828, 0.955] (n=204) | 0.788 [0.735, 0.832] | 0.843 [0.803, 0.877] | 0.828 |
| anthropic:claude-sonnet-4-5-20250929 | 543 | 0.780 [0.721, 0.823] | [0.729, 0.825] | 0.863 [0.815, 0.894] (n=204) | 0.777 [0.711, 0.817] | 0.834 [0.784, 0.865] | 0.825 |
| anthropic:claude-sonnet-5 | 543 | 0.809 [0.758, 0.848] | [0.763, 0.856] | 0.870 [0.802, 0.907] (n=204) | 0.806 [0.748, 0.842] | 0.856 [0.814, 0.883] | 0.846 |
| local:qwen36-35b-mtplx | 543 | 0.775 [0.725, 0.813] | [0.720, 0.814] | 0.817 [0.767, 0.863] (n=204) | 0.773 [0.717, 0.810] | 0.831 [0.788, 0.859] | 0.821 |
| local:qwen36-mtplx | 543 | 0.804 [0.752, 0.842] | [0.748, 0.845] | 0.883 [0.842, 0.917] (n=204) | 0.801 [0.740, 0.837] | 0.853 [0.807, 0.880] | 0.842 |
| openai:gpt-4.1 | 543 | 0.792 [0.734, 0.834] | [0.734, 0.844] | 0.883 [0.826, 0.930] (n=204) | 0.788 [0.725, 0.826] | 0.843 [0.797, 0.874] | 0.832 |
| openai:gpt-5.4-mini | 543 | 0.831 [0.773, 0.877] | [0.779, 0.887] | 0.935 [0.895, 0.970] (n=204) | 0.829 [0.765, 0.872] | 0.873 [0.826, 0.906] | 0.866 |
| openai:gpt-5.5 | 543 | 0.819 [0.762, 0.864] | [0.767, 0.874] | 0.909 [0.846, 0.938] (n=204) | 0.816 [0.754, 0.858] | 0.864 [0.817, 0.895] | 0.856 |
| typesafe:jev-1.13.0 | 543 | 0.797 [0.748, 0.837] | [0.752, 0.838] | 0.876 [0.843, 0.928] (n=204) | 0.793 [0.744, 0.829] | 0.847 [0.810, 0.875] | 0.838 |

### behaviour, local: paired AC1 difference vs Jev (same resampled transcripts)

| Comparison | n | Difference [95% CI] | CI excludes 0 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 − Jev | 543 | -0.005 [-0.037, 0.033] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | 543 | -0.018 [-0.057, 0.016] | no |
| anthropic:claude-sonnet-5 − Jev | 543 | 0.012 [-0.016, 0.040] | no |
| local:qwen36-35b-mtplx − Jev | 543 | -0.023 [-0.062, 0.017] | no |
| local:qwen36-mtplx − Jev | 543 | 0.007 [-0.026, 0.035] | no |
| openai:gpt-4.1 − Jev | 543 | -0.005 [-0.043, 0.027] | no |
| openai:gpt-5.4-mini − Jev | 543 | 0.034 [-0.001, 0.062] | no |
| openai:gpt-5.5 − Jev | 543 | 0.022 [-0.009, 0.048] | no |

### behaviour calibration, local (within an elicitation only)

| Judge | Elicitation | n | Multiclass Brier | Top-label ECE |
|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | verbalised | 543 | 0.256 | 0.038 |
| anthropic:claude-sonnet-4-5-20250929 | verbalised | 543 | 0.273 | 0.091 |
| anthropic:claude-sonnet-5 | verbalised | 543 | 0.230 | 0.087 |
| local:qwen36-35b-mtplx | verbalised | 543 | 0.298 | 0.113 |
| local:qwen36-mtplx | verbalised | 543 | 0.263 | 0.091 |
| openai:gpt-4.1 | verbalised | 543 | 0.257 | 0.050 |
| openai:gpt-5.4-mini | verbalised | 543 | 0.218 | 0.063 |
| openai:gpt-5.5 | verbalised | 543 | 0.212 | 0.017 |
| typesafe:jev-1.13.0 | native | 543 | 0.238 | 0.072 |

## behaviour: hosted sample (1376 utterances; 1364 with a gold label; 12 contested)

Of the 1364 gold labels, **204 come from a ten-coder majority and 1160 from a single coder** (85% of the total). AnnoMI codes most of its corpus once; only 428 utterances carry all ten annotators. The pooled AC1 column below is therefore mostly agreement with one arbitrary coder, whose own agreement with colleagues averages 0.74. The consensus-only column is the like-for-like expert comparison.

| Judge | n | AC1 vs pooled gold [95% CI, transcript-clustered] | AC1 CI (channel-clustered) | AC1 vs 10-coder gold | Kappa | Accuracy | Macro-F1 |
|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 1364 | 0.763 [0.730, 0.796] | [0.734, 0.794] | 0.876 [0.828, 0.955] (n=204) | 0.757 [0.725, 0.789] | 0.821 [0.798, 0.846] | 0.801 |
| anthropic:claude-sonnet-4-5-20250929 | 1364 | 0.758 [0.722, 0.790] | [0.722, 0.793] | 0.863 [0.815, 0.894] (n=204) | 0.753 [0.717, 0.786] | 0.817 [0.791, 0.841] | 0.800 |
| anthropic:claude-sonnet-5 | 1364 | 0.790 [0.757, 0.821] | [0.759, 0.826] | 0.870 [0.802, 0.907] (n=204) | 0.784 [0.749, 0.817] | 0.842 [0.816, 0.865] | 0.827 |
| openai:gpt-4.1 | 1364 | 0.780 [0.747, 0.811] | [0.743, 0.815] | 0.883 [0.826, 0.930] (n=204) | 0.773 [0.739, 0.805] | 0.834 [0.809, 0.857] | 0.818 |
| openai:gpt-5.4-mini | 1364 | 0.800 [0.763, 0.834] | [0.764, 0.845] | 0.935 [0.895, 0.970] (n=204) | 0.795 [0.758, 0.831] | 0.849 [0.821, 0.875] | 0.834 |
| openai:gpt-5.5 | 1364 | 0.791 [0.752, 0.828] | [0.759, 0.832] | 0.909 [0.846, 0.938] (n=204) | 0.786 [0.747, 0.823] | 0.842 [0.814, 0.870] | 0.827 |
| typesafe:jev-1.13.0 | 1364 | 0.760 [0.725, 0.794] | [0.729, 0.792] | 0.876 [0.843, 0.928] (n=204) | 0.753 [0.719, 0.787] | 0.819 [0.794, 0.843] | 0.800 |

### behaviour, hosted: paired AC1 difference vs Jev (same resampled transcripts)

| Comparison | n | Difference [95% CI] | CI excludes 0 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 − Jev | 1364 | 0.003 [-0.020, 0.026] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | 1364 | -0.003 [-0.025, 0.020] | no |
| anthropic:claude-sonnet-5 − Jev | 1364 | 0.030 [0.009, 0.051] | yes |
| openai:gpt-4.1 − Jev | 1364 | 0.019 [-0.004, 0.042] | no |
| openai:gpt-5.4-mini − Jev | 1364 | 0.039 [0.016, 0.064] | yes |
| openai:gpt-5.5 − Jev | 1364 | 0.031 [0.009, 0.053] | yes |

### behaviour calibration, hosted (within an elicitation only)

| Judge | Elicitation | n | Multiclass Brier | Top-label ECE |
|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | verbalised | 1364 | 0.291 | 0.061 |
| anthropic:claude-sonnet-4-5-20250929 | verbalised | 1364 | 0.305 | 0.112 |
| anthropic:claude-sonnet-5 | verbalised | 1364 | 0.251 | 0.063 |
| openai:gpt-4.1 | verbalised | 1364 | 0.274 | 0.057 |
| openai:gpt-5.4-mini | verbalised | 1364 | 0.257 | 0.085 |
| openai:gpt-5.5 | verbalised | 1364 | 0.238 | 0.038 |
| typesafe:jev-1.13.0 | native | 1364 | 0.276 | 0.096 |

## behaviour: all sample (4882 utterances; 4870 with a gold label; 12 contested)

Of the 4870 gold labels, **204 come from a ten-coder majority and 4666 from a single coder** (96% of the total). AnnoMI codes most of its corpus once; only 428 utterances carry all ten annotators. The pooled AC1 column below is therefore mostly agreement with one arbitrary coder, whose own agreement with colleagues averages 0.74. The consensus-only column is the like-for-like expert comparison.

| Judge | n | AC1 vs pooled gold [95% CI, transcript-clustered] | AC1 CI (channel-clustered) | AC1 vs 10-coder gold | Kappa | Accuracy | Macro-F1 |
|---|---|---|---|---|---|---|---|
| typesafe:jev-1.13.0 | 4870 | 0.760 [0.735, 0.784] | [0.742, 0.786] | 0.876 [0.843, 0.928] (n=204) | 0.751 [0.724, 0.774] | 0.818 [0.799, 0.835] | 0.794 |

### behaviour calibration, all (within an elicitation only)

| Judge | Elicitation | n | Multiclass Brier | Top-label ECE |
|---|---|---|---|---|
| typesafe:jev-1.13.0 | native | 4870 | 0.279 | 0.091 |

### behaviour: how reliable is the codebook itself?

Krippendorff's alpha over the coders alone, on the 216 multiply-coded utterances: **0.737**. They agree unanimously on 112 of them (52%) and reach no majority on 12. Agreement between two coders, pooled over all 10 choose 2 pairs, is 0.740.

This is the ceiling every judge below is measured against. A judge cannot agree with a consensus more reliably than the consensus agrees with itself, and where alpha is low the remaining error is in the labels, not in the models.

### behaviour: placement among the ten annotators (ceiling subset, leave-one-annotator-out golds)

Each rater, human or model, is scored against the majority of the other nine annotators. A consensus target rewards consistency, so a model can rank above individual annotators without being a better coder than any of them; read the standing as 'within the human range' or not.

**Read the intervals, not the order.** This subset is small and comes from only 7 transcripts, so the intervals are wide and overlap heavily. The paired column is the test that matters: where it says (ns), that rater and Jev are not distinguishable on this evidence, however far apart their point estimates look. A single category's worth of items moves a judge several places.

| Rater | n | AC1 vs the other nine | 95% CI (transcript-clustered) | Standing |
|---|---|---|---|---|
| annotator 0 | 209 | 0.815 | [0.774, 0.907] | — |
| annotator 1 | 209 | 0.854 | [0.791, 0.904] | — |
| annotator 2 | 211 | 0.830 | [0.789, 0.867] | — |
| annotator 3 | 209 | 0.670 | [0.627, 0.736] | — |
| annotator 4 | 208 | 0.872 | [0.798, 0.918] | — |
| annotator 5 | 210 | 0.854 | [0.823, 0.921] | — |
| annotator 6 | 208 | 0.879 | [0.841, 0.936] | — |
| annotator 7 | 208 | 0.841 | [0.799, 0.878] | — |
| annotator 8 | 208 | 0.879 | [0.818, 0.913] | — |
| annotator 9 | 210 | 0.874 | [0.817, 0.926] | — |
| anthropic:claude-haiku-4-5-20251001 | 208–211 | 0.860 | [0.811, 0.942] | above 6 of 10 · vs Jev -0.003 [-0.047, +0.076] (ns) |
| anthropic:claude-sonnet-4-5-20250929 | 208–211 | 0.844 | [0.800, 0.874] | above 4 of 10 · vs Jev -0.019 [-0.079, +0.020] (ns) |
| anthropic:claude-sonnet-5 | 208–211 | 0.857 | [0.792, 0.889] | above 6 of 10 · vs Jev -0.007 [-0.081, +0.023] (ns) |
| local:gemma4-31b-mtplx | 0/216 | not placed (incomplete) |  |  |
| local:qwen36-35b-mtplx | 208–211 | 0.806 | [0.764, 0.848] | above 1 of 10 · vs Jev -0.058 [-0.132, +0.006] (ns) |
| local:qwen36-mtplx | 208–211 | 0.863 | [0.825, 0.899] | above 6 of 10 · vs Jev -0.000 [-0.043, +0.026] (ns) |
| openai:gpt-4.1 | 208–211 | 0.867 | [0.808, 0.913] | above 6 of 10 · vs Jev +0.003 [-0.056, +0.036] (ns) |
| openai:gpt-5.4-mini | 208–211 | 0.917 | [0.878, 0.950] | above 10 of 10 · vs Jev +0.054 [-0.000, +0.080] (ns) |
| openai:gpt-5.5 | 208–211 | 0.898 | [0.842, 0.924] | above 10 of 10 · vs Jev +0.035 [-0.032, +0.067] (ns) |
| typesafe:jev-1.13.0 | 208–211 | 0.864 | [0.829, 0.922] | above 6 of 10 |

## open: local sample (555 utterances; 187 with a gold label, the rest have no such code; 25 contested)

Of the 187 gold labels, **72 come from a ten-coder majority and 115 from a single coder** (61% of the total). AnnoMI codes most of its corpus once; only 428 utterances carry all ten annotators. The pooled AC1 column below is therefore mostly agreement with one arbitrary coder, whose own agreement with colleagues averages 0.74. The consensus-only column is the like-for-like expert comparison.

| Judge | n | AC1 vs pooled gold [95% CI, transcript-clustered] | AC1 CI (channel-clustered) | AC1 vs 10-coder gold | Kappa | Accuracy | Macro-F1 |
|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 187 | 0.647 [0.505, 0.775] | [0.542, 0.735] | 0.780 [0.615, 0.929] (n=72) | 0.625 [0.476, 0.742] | 0.818 [0.747, 0.877] | 0.812 |
| anthropic:claude-sonnet-4-5-20250929 | 187 | 0.656 [0.518, 0.775] | [0.531, 0.770] | 0.697 [0.460, 0.852] (n=72) | 0.638 [0.499, 0.758] | 0.824 [0.754, 0.884] | 0.819 |
| anthropic:claude-sonnet-5 | 187 | 0.704 [0.559, 0.827] | [0.577, 0.824] | 0.889 [0.777, 0.979] (n=72) | 0.699 [0.563, 0.811] | 0.850 [0.780, 0.906] | 0.848 |
| local:qwen36-35b-mtplx | 187 | 0.618 [0.464, 0.748] | [0.483, 0.740] | 0.682 [0.485, 0.847] (n=72) | 0.567 [0.414, 0.685] | 0.797 [0.723, 0.857] | 0.783 |
| local:qwen36-mtplx | 187 | 0.708 [0.582, 0.818] | [0.604, 0.814] | 0.862 [0.773, 0.935] (n=72) | 0.694 [0.555, 0.802] | 0.850 [0.783, 0.905] | 0.847 |
| openai:gpt-4.1 | 187 | 0.636 [0.495, 0.763] | [0.539, 0.754] | 0.727 [0.534, 0.870] (n=72) | 0.615 [0.466, 0.737] | 0.813 [0.736, 0.875] | 0.807 |
| openai:gpt-5.4-mini | 187 | 0.737 [0.588, 0.856] | [0.620, 0.848] | 0.972 [0.926, 1.000] (n=72) | 0.729 [0.577, 0.858] | 0.866 [0.793, 0.930] | 0.864 |
| openai:gpt-5.5 | 187 | 0.704 [0.555, 0.823] | [0.590, 0.826] | 0.889 [0.771, 0.978] (n=72) | 0.700 [0.552, 0.813] | 0.850 [0.784, 0.907] | 0.849 |
| typesafe:jev-1.13.0 | 187 | 0.695 [0.566, 0.803] | [0.591, 0.794] | 0.806 [0.649, 0.900] (n=72) | 0.686 [0.550, 0.793] | 0.845 [0.777, 0.897] | 0.842 |

### open, local: paired AC1 difference vs Jev (same resampled transcripts)

| Comparison | n | Difference [95% CI] | CI excludes 0 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 − Jev | 187 | -0.048 [-0.153, 0.046] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | 187 | -0.039 [-0.131, 0.049] | no |
| anthropic:claude-sonnet-5 − Jev | 187 | 0.009 [-0.061, 0.085] | no |
| local:qwen36-35b-mtplx − Jev | 187 | -0.077 [-0.210, 0.045] | no |
| local:qwen36-mtplx − Jev | 187 | 0.013 [-0.059, 0.088] | no |
| openai:gpt-4.1 − Jev | 187 | -0.059 [-0.139, 0.022] | no |
| openai:gpt-5.4-mini − Jev | 187 | 0.042 [-0.034, 0.119] | no |
| openai:gpt-5.5 − Jev | 187 | 0.009 [-0.083, 0.095] | no |

## open: hosted sample (1376 utterances; 462 with a gold label, the rest have no such code; 25 contested)

Of the 462 gold labels, **72 come from a ten-coder majority and 390 from a single coder** (84% of the total). AnnoMI codes most of its corpus once; only 428 utterances carry all ten annotators. The pooled AC1 column below is therefore mostly agreement with one arbitrary coder, whose own agreement with colleagues averages 0.74. The consensus-only column is the like-for-like expert comparison.

| Judge | n | AC1 vs pooled gold [95% CI, transcript-clustered] | AC1 CI (channel-clustered) | AC1 vs 10-coder gold | Kappa | Accuracy | Macro-F1 |
|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 462 | 0.596 [0.481, 0.697] | [0.529, 0.658] | 0.780 [0.615, 0.929] (n=72) | 0.582 [0.476, 0.683] | 0.794 [0.738, 0.847] | 0.791 |
| anthropic:claude-sonnet-4-5-20250929 | 462 | 0.593 [0.488, 0.691] | [0.506, 0.677] | 0.697 [0.460, 0.852] (n=72) | 0.586 [0.487, 0.681] | 0.794 [0.744, 0.843] | 0.792 |
| anthropic:claude-sonnet-5 | 462 | 0.620 [0.495, 0.735] | [0.480, 0.734] | 0.889 [0.777, 0.979] (n=72) | 0.623 [0.512, 0.744] | 0.810 [0.750, 0.872] | 0.809 |
| openai:gpt-4.1 | 462 | 0.602 [0.487, 0.706] | [0.501, 0.694] | 0.727 [0.534, 0.870] (n=72) | 0.594 [0.492, 0.703] | 0.799 [0.746, 0.854] | 0.797 |
| openai:gpt-5.4-mini | 462 | 0.638 [0.509, 0.755] | [0.493, 0.766] | 0.972 [0.926, 1.000] (n=72) | 0.637 [0.523, 0.753] | 0.818 [0.760, 0.877] | 0.817 |
| openai:gpt-5.5 | 462 | 0.633 [0.506, 0.747] | [0.492, 0.756] | 0.889 [0.771, 0.978] (n=72) | 0.637 [0.528, 0.751] | 0.816 [0.758, 0.876] | 0.816 |
| typesafe:jev-1.13.0 | 462 | 0.591 [0.470, 0.706] | [0.469, 0.704] | 0.806 [0.649, 0.900] (n=72) | 0.590 [0.474, 0.704] | 0.794 [0.738, 0.852] | 0.793 |

### open, hosted: paired AC1 difference vs Jev (same resampled transcripts)

| Comparison | n | Difference [95% CI] | CI excludes 0 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 − Jev | 462 | 0.005 [-0.082, 0.103] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | 462 | 0.002 [-0.062, 0.072] | no |
| anthropic:claude-sonnet-5 − Jev | 462 | 0.029 [-0.025, 0.093] | no |
| openai:gpt-4.1 − Jev | 462 | 0.011 [-0.052, 0.079] | no |
| openai:gpt-5.4-mini − Jev | 462 | 0.047 [-0.008, 0.106] | no |
| openai:gpt-5.5 − Jev | 462 | 0.042 [-0.014, 0.104] | no |

## open: all sample (4882 utterances; 1631 with a gold label, the rest have no such code; 25 contested)

Of the 1631 gold labels, **72 come from a ten-coder majority and 1559 from a single coder** (96% of the total). AnnoMI codes most of its corpus once; only 428 utterances carry all ten annotators. The pooled AC1 column below is therefore mostly agreement with one arbitrary coder, whose own agreement with colleagues averages 0.74. The consensus-only column is the like-for-like expert comparison.

| Judge | n | AC1 vs pooled gold [95% CI, transcript-clustered] | AC1 CI (channel-clustered) | AC1 vs 10-coder gold | Kappa | Accuracy | Macro-F1 |
|---|---|---|---|---|---|---|---|
| typesafe:jev-1.13.0 | 1631 | 0.617 [0.542, 0.687] | [0.506, 0.707] | 0.806 [0.649, 0.900] (n=72) | 0.615 [0.540, 0.691] | 0.807 [0.769, 0.846] | 0.806 |

## complex: local sample (555 utterances; 150 with a gold label, the rest have no such code; 65 contested)

Of the 150 gold labels, **43 come from a ten-coder majority and 107 from a single coder** (71% of the total). AnnoMI codes most of its corpus once; only 428 utterances carry all ten annotators. The pooled AC1 column below is therefore mostly agreement with one arbitrary coder, whose own agreement with colleagues averages 0.74. The consensus-only column is the like-for-like expert comparison.

| Judge | n | AC1 vs pooled gold [95% CI, transcript-clustered] | AC1 CI (channel-clustered) | AC1 vs 10-coder gold | Kappa | Accuracy | Macro-F1 |
|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 150 | 0.427 [0.293, 0.571] | [0.271, 0.604] | n/a | 0.426 [0.285, 0.566] | 0.713 [0.644, 0.783] | 0.713 |
| anthropic:claude-sonnet-4-5-20250929 | 150 | 0.321 [0.196, 0.462] | [0.188, 0.470] | n/a | 0.321 [0.182, 0.450] | 0.660 [0.592, 0.724] | 0.659 |
| anthropic:claude-sonnet-5 | 150 | 0.426 [0.264, 0.568] | [0.245, 0.617] | n/a | 0.411 [0.254, 0.548] | 0.707 [0.624, 0.778] | 0.700 |
| local:qwen36-35b-mtplx | 150 | 0.426 [0.281, 0.573] | [0.302, 0.563] | n/a | 0.411 [0.284, 0.559] | 0.707 [0.637, 0.780] | 0.700 |
| local:qwen36-mtplx | 150 | 0.387 [0.219, 0.570] | [0.213, 0.594] | n/a | 0.387 [0.200, 0.568] | 0.693 [0.603, 0.789] | 0.693 |
| openai:gpt-4.1 | 150 | 0.392 [0.242, 0.544] | [0.143, 0.629] | n/a | 0.385 [0.237, 0.535] | 0.693 [0.618, 0.770] | 0.691 |
| openai:gpt-5.4-mini | 150 | 0.347 [0.200, 0.491] | [0.143, 0.533] | n/a | 0.346 [0.191, 0.487] | 0.673 [0.600, 0.745] | 0.673 |
| openai:gpt-5.5 | 150 | 0.361 [0.210, 0.504] | [0.199, 0.536] | n/a | 0.359 [0.192, 0.492] | 0.680 [0.597, 0.748] | 0.679 |
| typesafe:jev-1.13.0 | 150 | 0.293 [0.113, 0.454] | [0.129, 0.468] | n/a | 0.294 [0.115, 0.442] | 0.647 [0.556, 0.723] | 0.647 |

### complex, local: paired AC1 difference vs Jev (same resampled transcripts)

| Comparison | n | Difference [95% CI] | CI excludes 0 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 − Jev | 150 | 0.134 [-0.041, 0.325] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | 150 | 0.028 [-0.137, 0.219] | no |
| anthropic:claude-sonnet-5 − Jev | 150 | 0.132 [-0.012, 0.294] | no |
| local:qwen36-35b-mtplx − Jev | 150 | 0.132 [-0.046, 0.342] | no |
| local:qwen36-mtplx − Jev | 150 | 0.094 [-0.093, 0.300] | no |
| openai:gpt-4.1 − Jev | 150 | 0.099 [-0.064, 0.288] | no |
| openai:gpt-5.4-mini − Jev | 150 | 0.054 [-0.074, 0.189] | no |
| openai:gpt-5.5 − Jev | 150 | 0.068 [-0.054, 0.204] | no |

## complex: hosted sample (1376 utterances; 387 with a gold label, the rest have no such code; 65 contested)

Of the 387 gold labels, **43 come from a ten-coder majority and 344 from a single coder** (89% of the total). AnnoMI codes most of its corpus once; only 428 utterances carry all ten annotators. The pooled AC1 column below is therefore mostly agreement with one arbitrary coder, whose own agreement with colleagues averages 0.74. The consensus-only column is the like-for-like expert comparison.

| Judge | n | AC1 vs pooled gold [95% CI, transcript-clustered] | AC1 CI (channel-clustered) | AC1 vs 10-coder gold | Kappa | Accuracy | Macro-F1 |
|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 387 | 0.339 [0.246, 0.439] | [0.236, 0.523] | n/a | 0.338 [0.238, 0.442] | 0.669 [0.622, 0.721] | 0.669 |
| anthropic:claude-sonnet-4-5-20250929 | 387 | 0.334 [0.240, 0.430] | [0.256, 0.454] | n/a | 0.325 [0.234, 0.410] | 0.664 [0.617, 0.707] | 0.661 |
| anthropic:claude-sonnet-5 | 387 | 0.395 [0.285, 0.506] | [0.253, 0.539] | n/a | 0.395 [0.290, 0.486] | 0.695 [0.637, 0.746] | 0.693 |
| openai:gpt-4.1 | 387 | 0.370 [0.261, 0.495] | [0.221, 0.548] | n/a | 0.372 [0.257, 0.490] | 0.685 [0.624, 0.744] | 0.684 |
| openai:gpt-5.4-mini | 387 | 0.349 [0.232, 0.456] | [0.191, 0.480] | n/a | 0.350 [0.233, 0.447] | 0.674 [0.615, 0.725] | 0.674 |
| openai:gpt-5.5 | 387 | 0.349 [0.227, 0.466] | [0.201, 0.509] | n/a | 0.349 [0.228, 0.460] | 0.674 [0.616, 0.730] | 0.674 |
| typesafe:jev-1.13.0 | 387 | 0.312 [0.200, 0.417] | [0.219, 0.424] | n/a | 0.304 [0.196, 0.399] | 0.654 [0.602, 0.703] | 0.651 |

### complex, hosted: paired AC1 difference vs Jev (same resampled transcripts)

| Comparison | n | Difference [95% CI] | CI excludes 0 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 − Jev | 387 | 0.026 [-0.078, 0.146] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | 387 | 0.022 [-0.074, 0.114] | no |
| anthropic:claude-sonnet-5 − Jev | 387 | 0.083 [-0.037, 0.208] | no |
| openai:gpt-4.1 − Jev | 387 | 0.058 [-0.064, 0.192] | no |
| openai:gpt-5.4-mini − Jev | 387 | 0.036 [-0.061, 0.138] | no |
| openai:gpt-5.5 − Jev | 387 | 0.037 [-0.055, 0.136] | no |

## complex: all sample (4882 utterances; 1479 with a gold label, the rest have no such code; 65 contested)

Of the 1479 gold labels, **43 come from a ten-coder majority and 1436 from a single coder** (97% of the total). AnnoMI codes most of its corpus once; only 428 utterances carry all ten annotators. The pooled AC1 column below is therefore mostly agreement with one arbitrary coder, whose own agreement with colleagues averages 0.74. The consensus-only column is the like-for-like expert comparison.

| Judge | n | AC1 vs pooled gold [95% CI, transcript-clustered] | AC1 CI (channel-clustered) | AC1 vs 10-coder gold | Kappa | Accuracy | Macro-F1 |
|---|---|---|---|---|---|---|---|
| typesafe:jev-1.13.0 | 1479 | 0.329 [0.269, 0.391] | [0.251, 0.429] | n/a | 0.311 [0.244, 0.373] | 0.660 [0.629, 0.691] | 0.655 |

### Operations, annomi_therapist

| Judge | Calls | Parse failed | Errors | Unwrapped (A6) | p50 ms | p95 ms | USD/1k | Sampling | Reasoning |
|---|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 1376 | 0 | 0 | 0 | batch only |  | $0.876 | temperature=0 | off |
| anthropic:claude-sonnet-4-5-20250929 | 1376 | 0 | 0 | 0 | batch only |  | $2.527 | temperature=0 | off |
| anthropic:claude-sonnet-5 | 1376 | 0 | 0 | 0 | batch only |  | $2.081 | provider_default | adaptive-low |
| local:gemma4-31b-mtplx | 2 | 0 | 0 | 0 | 5492 | 5929 | $0.000 | temperature=0 | off |
| local:qwen36-35b-mtplx | 555 | 0 | 0 | 0 | 2412 | 2931 | $0.000 | temperature=0 | off |
| local:qwen36-mtplx | 555 | 0 | 0 | 0 | 5265 | 14424 | $0.000 | temperature=0 | off |
| openai:gpt-4.1 | 1376 | 0 | 0 | 0 | 3596 | 8815 | $2.183 | temperature=0 | off |
| openai:gpt-5.4-mini | 1376 | 0 | 0 | 0 | 1512 | 2457 | $1.159 | provider_default | effort-low |
| openai:gpt-5.5 | 1376 | 0 | 0 | 0 | 1747 | 2673 | $6.376 | provider_default | effort-low |
| typesafe:jev-1.13.0 | 4882 | 0 | 0 | 0 | 270 | 367 | $0.034 | n/a | n/a |

## talk: local sample (445 utterances; 426 with a gold label; 19 contested)

Of the 426 gold labels, **193 come from a ten-coder majority and 233 from a single coder** (55% of the total). AnnoMI codes most of its corpus once; only 428 utterances carry all ten annotators. The pooled AC1 column below is therefore mostly agreement with one arbitrary coder, whose own agreement with colleagues averages 0.74. The consensus-only column is the like-for-like expert comparison.

| Judge | n | AC1 vs pooled gold [95% CI, transcript-clustered] | AC1 CI (channel-clustered) | AC1 vs 10-coder gold | Kappa | Accuracy | Macro-F1 |
|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 426 | 0.684 [0.569, 0.763] | [0.560, 0.773] | 0.839 [0.787, 0.887] (n=193) | 0.609 [0.502, 0.685] | 0.775 [0.699, 0.826] | 0.742 |
| anthropic:claude-sonnet-4-5-20250929 | 426 | 0.749 [0.640, 0.823] | [0.639, 0.842] | 0.874 [0.816, 0.911] (n=193) | 0.691 [0.576, 0.763] | 0.822 [0.743, 0.869] | 0.802 |
| anthropic:claude-sonnet-5 | 426 | 0.715 [0.602, 0.795] | [0.595, 0.814] | 0.844 [0.748, 0.899] (n=193) | 0.654 [0.537, 0.738] | 0.798 [0.719, 0.851] | 0.778 |
| local:qwen36-35b-mtplx | 2/426 | not scored (coverage) |  |  |  |  |  |
| local:qwen36-mtplx | 426 | 0.726 [0.610, 0.802] | [0.620, 0.813] | 0.882 [0.826, 0.907] (n=193) | 0.650 [0.528, 0.719] | 0.803 [0.726, 0.851] | 0.772 |
| openai:gpt-4.1 | 426 | 0.747 [0.616, 0.833] | [0.618, 0.853] | 0.909 [0.825, 0.948] (n=193) | 0.683 [0.545, 0.764] | 0.819 [0.729, 0.871] | 0.797 |
| openai:gpt-5.4-mini | 426 | 0.709 [0.596, 0.787] | [0.592, 0.795] | 0.861 [0.785, 0.899] (n=193) | 0.631 [0.505, 0.713] | 0.791 [0.708, 0.840] | 0.766 |
| openai:gpt-5.5 | 426 | 0.758 [0.641, 0.836] | [0.635, 0.852] | 0.909 [0.838, 0.948] (n=193) | 0.706 [0.578, 0.784] | 0.829 [0.745, 0.879] | 0.808 |
| typesafe:jev-1.13.0 | 426 | 0.703 [0.584, 0.780] | [0.586, 0.799] | 0.869 [0.809, 0.929] (n=193) | 0.609 [0.489, 0.686] | 0.784 [0.699, 0.833] | 0.750 |

### talk, local: paired AC1 difference vs Jev (same resampled transcripts)

| Comparison | n | Difference [95% CI] | CI excludes 0 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 − Jev | 426 | -0.019 [-0.062, 0.029] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | 426 | 0.047 [-0.001, 0.104] | no |
| anthropic:claude-sonnet-5 − Jev | 426 | 0.012 [-0.036, 0.068] | no |
| local:qwen36-mtplx − Jev | 426 | 0.023 [-0.017, 0.062] | no |
| openai:gpt-4.1 − Jev | 426 | 0.045 [-0.013, 0.090] | no |
| openai:gpt-5.4-mini − Jev | 426 | 0.006 [-0.039, 0.052] | no |
| openai:gpt-5.5 − Jev | 426 | 0.056 [0.002, 0.111] | yes |

### talk calibration, local (within an elicitation only)

| Judge | Elicitation | n | Multiclass Brier | Top-label ECE |
|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | verbalised | 426 | 0.346 | 0.046 |
| anthropic:claude-sonnet-4-5-20250929 | verbalised | 426 | 0.297 | 0.075 |
| anthropic:claude-sonnet-5 | verbalised | 426 | 0.309 | 0.029 |
| local:qwen36-35b-mtplx | verbalised | 2/426 | not scored (coverage) |  |
| local:qwen36-mtplx | verbalised | 426 | 0.325 | 0.084 |
| openai:gpt-4.1 | verbalised | 426 | 0.305 | 0.062 |
| openai:gpt-5.4-mini | verbalised | 426 | 0.338 | 0.105 |
| openai:gpt-5.5 | verbalised | 426 | 0.266 | 0.039 |
| typesafe:jev-1.13.0 | native | 426 | 0.331 | 0.102 |

## talk: hosted sample (1124 utterances; 1105 with a gold label; 19 contested)

Of the 1105 gold labels, **193 come from a ten-coder majority and 912 from a single coder** (83% of the total). AnnoMI codes most of its corpus once; only 428 utterances carry all ten annotators. The pooled AC1 column below is therefore mostly agreement with one arbitrary coder, whose own agreement with colleagues averages 0.74. The consensus-only column is the like-for-like expert comparison.

| Judge | n | AC1 vs pooled gold [95% CI, transcript-clustered] | AC1 CI (channel-clustered) | AC1 vs 10-coder gold | Kappa | Accuracy | Macro-F1 |
|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 1105 | 0.652 [0.597, 0.705] | [0.599, 0.711] | 0.839 [0.787, 0.887] (n=193) | 0.586 [0.533, 0.644] | 0.755 [0.718, 0.792] | 0.731 |
| anthropic:claude-sonnet-4-5-20250929 | 1105 | 0.673 [0.614, 0.730] | [0.625, 0.743] | 0.874 [0.816, 0.911] (n=193) | 0.614 [0.555, 0.673] | 0.770 [0.732, 0.808] | 0.756 |
| anthropic:claude-sonnet-5 | 1105 | 0.674 [0.616, 0.732] | [0.625, 0.756] | 0.844 [0.748, 0.899] (n=193) | 0.615 [0.560, 0.674] | 0.771 [0.734, 0.810] | 0.757 |
| openai:gpt-4.1 | 1105 | 0.683 [0.619, 0.744] | [0.629, 0.758] | 0.909 [0.825, 0.948] (n=193) | 0.617 [0.555, 0.679] | 0.776 [0.734, 0.817] | 0.757 |
| openai:gpt-5.4-mini | 1105 | 0.663 [0.606, 0.720] | [0.613, 0.735] | 0.861 [0.785, 0.899] (n=193) | 0.587 [0.524, 0.646] | 0.760 [0.720, 0.798] | 0.735 |
| openai:gpt-5.5 | 1105 | 0.703 [0.640, 0.760] | [0.652, 0.781] | 0.909 [0.838, 0.948] (n=193) | 0.653 [0.596, 0.713] | 0.792 [0.753, 0.831] | 0.775 |
| typesafe:jev-1.13.0 | 1105 | 0.679 [0.619, 0.737] | [0.635, 0.741] | 0.869 [0.809, 0.929] (n=193) | 0.595 [0.537, 0.652] | 0.769 [0.728, 0.810] | 0.743 |

### talk, hosted: paired AC1 difference vs Jev (same resampled transcripts)

| Comparison | n | Difference [95% CI] | CI excludes 0 |
|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 − Jev | 1105 | -0.027 [-0.058, 0.005] | no |
| anthropic:claude-sonnet-4-5-20250929 − Jev | 1105 | -0.006 [-0.041, 0.028] | no |
| anthropic:claude-sonnet-5 − Jev | 1105 | -0.004 [-0.037, 0.031] | no |
| openai:gpt-4.1 − Jev | 1105 | 0.004 [-0.027, 0.034] | no |
| openai:gpt-5.4-mini − Jev | 1105 | -0.016 [-0.043, 0.012] | no |
| openai:gpt-5.5 − Jev | 1105 | 0.024 [-0.011, 0.057] | no |

### talk calibration, hosted (within an elicitation only)

| Judge | Elicitation | n | Multiclass Brier | Top-label ECE |
|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | verbalised | 1105 | 0.371 | 0.058 |
| anthropic:claude-sonnet-4-5-20250929 | verbalised | 1105 | 0.369 | 0.118 |
| anthropic:claude-sonnet-5 | verbalised | 1105 | 0.332 | 0.032 |
| openai:gpt-4.1 | verbalised | 1105 | 0.357 | 0.077 |
| openai:gpt-5.4-mini | verbalised | 1105 | 0.384 | 0.129 |
| openai:gpt-5.5 | verbalised | 1105 | 0.313 | 0.051 |
| typesafe:jev-1.13.0 | native | 1105 | 0.352 | 0.104 |

## talk: all sample (4817 utterances; 4798 with a gold label; 19 contested)

Of the 4798 gold labels, **193 come from a ten-coder majority and 4605 from a single coder** (96% of the total). AnnoMI codes most of its corpus once; only 428 utterances carry all ten annotators. The pooled AC1 column below is therefore mostly agreement with one arbitrary coder, whose own agreement with colleagues averages 0.74. The consensus-only column is the like-for-like expert comparison.

| Judge | n | AC1 vs pooled gold [95% CI, transcript-clustered] | AC1 CI (channel-clustered) | AC1 vs 10-coder gold | Kappa | Accuracy | Macro-F1 |
|---|---|---|---|---|---|---|---|
| typesafe:jev-1.13.0 | 4798 | 0.692 [0.646, 0.735] | [0.664, 0.728] | 0.869 [0.809, 0.929] (n=193) | 0.527 [0.480, 0.577] | 0.767 [0.735, 0.797] | 0.691 |

### talk calibration, all (within an elicitation only)

| Judge | Elicitation | n | Multiclass Brier | Top-label ECE |
|---|---|---|---|---|
| typesafe:jev-1.13.0 | native | 4798 | 0.352 | 0.103 |

### talk: how reliable is the codebook itself?

Krippendorff's alpha over the coders alone, on the 212 multiply-coded utterances: **0.467**. They agree unanimously on 58 of them (27%) and reach no majority on 19. Agreement between two coders, pooled over all 10 choose 2 pairs, is 0.583.

This is the ceiling every judge below is measured against. A judge cannot agree with a consensus more reliably than the consensus agrees with itself, and where alpha is low the remaining error is in the labels, not in the models.

### talk: placement among the ten annotators (ceiling subset, leave-one-annotator-out golds)

Each rater, human or model, is scored against the majority of the other nine annotators. A consensus target rewards consistency, so a model can rank above individual annotators without being a better coder than any of them; read the standing as 'within the human range' or not.

**Read the intervals, not the order.** This subset is small and comes from only 7 transcripts, so the intervals are wide and overlap heavily. The paired column is the test that matters: where it says (ns), that rater and Jev are not distinguishable on this evidence, however far apart their point estimates look. A single category's worth of items moves a judge several places.

| Rater | n | AC1 vs the other nine | 95% CI (transcript-clustered) | Standing |
|---|---|---|---|---|
| annotator 0 | 209 | 0.761 | [0.654, 0.845] | — |
| annotator 1 | 205 | 0.750 | [0.663, 0.805] | — |
| annotator 2 | 208 | 0.665 | [0.588, 0.814] | — |
| annotator 3 | 207 | 0.661 | [0.534, 0.727] | — |
| annotator 4 | 209 | 0.542 | [0.461, 0.646] | — |
| annotator 5 | 203 | 0.799 | [0.713, 0.848] | — |
| annotator 6 | 206 | 0.529 | [0.404, 0.741] | — |
| annotator 7 | 207 | 0.816 | [0.717, 0.865] | — |
| annotator 8 | 204 | 0.759 | [0.685, 0.807] | — |
| annotator 9 | 207 | 0.679 | [0.624, 0.765] | — |
| anthropic:claude-haiku-4-5-20251001 | 203–209 | 0.812 | [0.753, 0.858] | above 9 of 10 · vs Jev -0.036 [-0.059, -0.016] |
| anthropic:claude-sonnet-4-5-20250929 | 203–209 | 0.838 | [0.781, 0.870] | above 10 of 10 · vs Jev -0.010 [-0.077, +0.020] (ns) |
| anthropic:claude-sonnet-5 | 203–209 | 0.820 | [0.724, 0.873] | above 10 of 10 · vs Jev -0.028 [-0.093, +0.008] (ns) |
| local:qwen36-35b-mtplx | 0/212 | not placed (incomplete) |  |  |
| local:qwen36-mtplx | 203–209 | 0.850 | [0.792, 0.873] | above 10 of 10 · vs Jev +0.003 [-0.080, +0.058] (ns) |
| openai:gpt-4.1 | 203–209 | 0.878 | [0.798, 0.915] | above 10 of 10 · vs Jev +0.030 [-0.070, +0.080] (ns) |
| openai:gpt-5.4-mini | 203–209 | 0.839 | [0.769, 0.874] | above 10 of 10 · vs Jev -0.009 [-0.082, +0.045] (ns) |
| openai:gpt-5.5 | 203–209 | 0.874 | [0.809, 0.913] | above 10 of 10 · vs Jev +0.026 [-0.054, +0.077] (ns) |
| typesafe:jev-1.13.0 | 203–209 | 0.848 | [0.786, 0.905] | above 10 of 10 |

### Operations, annomi_client

| Judge | Calls | Parse failed | Errors | Unwrapped (A6) | p50 ms | p95 ms | USD/1k | Sampling | Reasoning |
|---|---|---|---|---|---|---|---|---|---|
| anthropic:claude-haiku-4-5-20251001 | 1124 | 0 | 0 | 0 | batch only |  | $0.548 | temperature=0 | off |
| anthropic:claude-sonnet-4-5-20250929 | 1124 | 0 | 0 | 0 | batch only |  | $1.634 | temperature=0 | off |
| anthropic:claude-sonnet-5 | 1124 | 0 | 0 | 0 | batch only |  | $1.333 | provider_default | adaptive-low |
| local:qwen36-35b-mtplx | 445 | 166 | 277 | 0 | 1738 | 4163 | $0.000 | temperature=0 | off |
| local:qwen36-mtplx | 445 | 0 | 0 | 0 | 3260 | 10454 | $0.000 | temperature=0 | off |
| openai:gpt-4.1 | 1124 | 0 | 0 | 0 | 2382 | 5822 | $1.405 | temperature=0 | off |
| openai:gpt-5.4-mini | 1124 | 0 | 0 | 0 | 1200 | 2054 | $0.814 | provider_default | effort-low |
| openai:gpt-5.5 | 1124 | 0 | 0 | 0 | 1379 | 2142 | $4.047 | provider_default | effort-low |
| typesafe:jev-1.13.0 | 4817 | 0 | 0 | 0 | 264 | 362 | $0.026 | n/a | n/a |
