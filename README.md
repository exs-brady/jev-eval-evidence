# Jev evaluation study — evidence bundle

This is the record of every judgment made in a study comparing TypeSafe's Jev
(`jev-1.13.0`) with ten hosted and local LLM judges, and with the deterministic
keyword and regex floors two products already run. **55,347 judgments, 11 judges,
7 experiments, 4 questions.**

It is not the harness. It carries what a reviewer needs to check the numbers and to
attack the claims, and deliberately not the machinery that produced them or the text
that was judged. `docs/WHAT_IS_NOT_HERE.md` says what is missing and why, so that
nothing has to be inferred from an absence.

## Start here

```
python3 verify.py      # re-proves the parity chain and every file hash
```

Then read `docs/LEVELS.md` before computing anything: two severity scales appear in
this bundle and one of them runs backwards.

## What is in it

| Path | What it is |
|---|---|
| `runs/` | Every judgment, one JSONL row each: item id, prompt hash, the typed answer with its probability vector, status, tokens, latency, cost |
| `items/*.outcomes.csv` | One row per item: the expected label and each judge's answer, side by side. **No item text** |
| `reports/` | The study's own aggregate tables, Markdown and JSON, dated |
| `prompts/` | The four rendered prompts, verbatim as sent |
| `docs/PREREGISTRATION.md` | Written and committed before any test-split or live run |
| `docs/THRESHOLDS.md` | Every frozen threshold, and whether it came from the selection rule or its fallback |
| `docs/CONTAMINATION.md` | Which arms are contaminated, with both sides of the overlap printed |
| `docs/REPLICATION_BRIEF.md` | The blind re-audit protocol, with `replication_claims.json` sealed against it |
| `reports/independent-replication-*` | A different model family's blind replication, working only from that brief |
| `code/` | The metric implementations and the scorers: enough to recompute every published number from `runs/` |

The study's limitations are not summarised here. Each one is recorded where the
evidence for it sits: `docs/CONTAMINATION.md` for which arms are compromised and
what that does to which figure, `docs/PROVENANCE.md` for who authored each fixture
and what has been ratified, `docs/THRESHOLDS.md` for which thresholds came from the
selection rule and which from its fallback, `docs/WHAT_IS_NOT_HERE.md` for what this
bundle omits, and every report's own caveats. The synthetic reports carry an
upper-bound notice in their headers.

## Prompt parity is checkable, not asserted

The study claims every judge was asked an identical question. That claim is a hash.
`prompt_sha` on each run row is `sha256(task_id + "\n" + system_prompt)[:16]`, and
the system prompts are in `prompts/`:

```python
import hashlib, json, pathlib
for tid, m in json.load(open("prompts/prompts.json")).items():
    txt = pathlib.Path("prompts", m["file"]).read_text()
    assert hashlib.sha256((tid + "\n" + txt).encode()).hexdigest()[:16] == m["prompt_sha"]
```

All 55,347 rows carry one of exactly four hashes. No judge received a different
prompt, none was tuned per vendor, and no reviewer has to take that on trust.
`verify.py` runs this.

Note what the prompts also show: Jev answers these questions **natively**, returning
a distribution over the same levels; every other judge is asked to **write the
numbers in JSON**. That difference is real, it is visible in the prompts, and the
probability-shape tables in `reports/` are about its consequences.

## AnnoMI is fully replicable from public data

Item ids in `runs/annomi_*` and `items/annomi_*` are `transcript:utterance` indices
into the public AnnoMI corpus. A reviewer who fetches AnnoMI at the pinned commit can
reconstruct every input, re-derive the gold labels and recompute the agreement
figures end to end, with nothing from us but the prompts. This arm is the one place
the whole pipeline can be checked from the outside, and it is where we would start.

## Licence

Data, results and documents: CC BY 4.0 (`LICENSE-DATA.md`). AnnoMI is not
redistributed here; fetch it upstream under its own terms.
