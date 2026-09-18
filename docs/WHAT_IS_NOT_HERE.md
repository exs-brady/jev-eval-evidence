# What is not in this bundle, and why

Stated positively, so that no absence has to be guessed at.

## The item text

**Not here:** the 86 crisis phrases, the 84 multi-turn arcs, the trainee fixtures,
and the 2,438-unit synthetic grid.

**Why, for the clinical fixtures:** they are two partner organisations' held-out
safety suites, and one set is derived from that partner's anonymised real enquiries.
They are those organisations' to release, not ours. The organisations appear
throughout as the stable pseudonyms `org-a` and `org-b`.

**Why, for the synthetic grid:** it is ours, but 194 of its highest-severity items
carry method and means detail. The clinical fixtures were written under an explicit
rule never to enumerate a method; the generator had no such constraint. We are not
publishing a searchable corpus of self-harm method text in order to substantiate a
measurement.

**What replaces it:** `items/*.outcomes.csv` gives one row per item — the expected
label and every judge's answer with its full probability vector. Every published
number can be recomputed from it, and every disagreement between judges is visible
item by item. What a reviewer *cannot* do is audit whether a label is correct. That
is a real limit on this bundle, and it bites hardest on the unratified arcs named in
`README.md`.

**If you need the text:** the clinical fixtures require partner consent; ask, and we
will take it to them. The synthetic grid can be shared directly with a named
researcher under terms.

## The harness

**Not here:** the provider layer, the prompt renderer, the run store, the batching,
the elicitation machinery, the synthetic generator, and the products' own detection
code — a keyword lexicon and a regex suite, both vendored from the partners.

**Why:** it is the working system, and in the partners' case it is theirs.

**What replaces it:** the rendered prompts, which make the parity claim checkable by
hash without shipping the renderer; and `code/`, which is enough to recompute every
number in `reports/` from `runs/`. The blind replication included in `reports/` was
carried out this way — against the sealed claims in `docs/replication_claims.json`,
by a party with no access to the harness — so the arrangement is known to work.

## Identifiers

Partner and product names, personal names and account identifiers are removed
throughout. `org-a` and `org-b` are stable: the same id always means the same
organisation.
