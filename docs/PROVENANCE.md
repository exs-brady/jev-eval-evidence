# Fixture provenance

Snapshot copies taken 2026-09-17. All content is synthetic or model-authored eval material; no real user data. Refresh by re-copying and updating this table.

**None of this material was authored by a clinician.** Read the Authorship column before describing it anywhere. "Clinical fixtures" in this repo means *the products' own safety eval sets*, not clinician-written text, and no expected level in any of them has been ratified at a clinical sign-off gate.

| File | Source | Last commit touching source | Source dirty at copy? | sha256 (first 16) |
|---|---|---|---|---|
| [partner]/crisis_recall_bank.json | [partner]/RIF/backend/app/data/nav/crisis_recall_bank.json | 95d7715 | no | 222bb991c3323cab |
| [partner]/[partner]_scenarios.json | [partner]/RIF/backend/app/data/nav/eval/[partner]_scenarios.json | 146564b | no | b45deac1279f0629 |
| [partner]/[partner]_scenarios.json | [partner]/RIF/backend/app/data/nav/eval/[partner]_scenarios.json | 869c84f | no | aa757550fb9f9aab |
| [partner]/paraphrase_guard.json | [partner]/harness/fixtures/paraphrase_guard.json | 3071f60 | no | bc7ad3b8275322e1 |
| [partner]/trainee_misconduct_suite.json | [partner]/harness/fixtures/trainee_misconduct_suite.json | a373246 | no | 695265790d8dabce |


## Authorship and sign-off

| File | Who wrote it, and what has been signed off |
|---|---|
| [partner]/crisis_recall_bank.json | Engineering draft. Its own `_metadata.SAFETY_NOTES`: "MUST be reviewed and signed off by a qualified clinician and the org's safeguarding lead before go-live." Not reviewed. This is also the set the lexicon was tuned on. |
| [partner]/[partner]_scenarios.json | 52 Set A arcs. Claude, independent session, no access to the RIF codebase, engine, fixtures or detector (2026-08-01). Written from the population description only. `expect_level` is the author's grade; Gate A disposition blank. |
| [partner]/[partner]_scenarios.json | 32 Set A arcs. Claude, independent session, same blind constraints (2026-09-07). Written from [partner]'s anonymised enquiries as variants rather than copies, plus the population description. `expect_level` is the author's grade; Gate A disposition blank. |
| [partner]/paraphrase_guard.json | Authored in [partner]'s harness. No clinician sign-off recorded. |
| [partner]/trainee_misconduct_suite.json | Authored in [partner]. **The only clinician-touched fixture here:** severities returned by [partner] at Gate A rounds one (2026-09-02) and two (2026-09-04); remaining items closed on defaults 2026-09-15. Status `misconduct-v2-draft`, not shipped. |

`paraphrase_extra.yaml` is authored in this repo and is always reported separately from the clinical fixtures.
