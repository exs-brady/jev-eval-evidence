"""Every judge on the phase-1 clinical fixtures, through the phase-1 scorers.

  uv run python -m experiments.compare.fixtures

Reuses crisis_severity.run.evaluate and trainee_conduct.run.flagged with
detector closures over the run store, so the floor-only rows must reproduce
the phase-1 reports exactly (that is the parity check). No thresholds are
tuned here: the phase-1 headline τ (0.2 crisis, 0.7 trainee) is applied to
every judge alike, and the argmax row needs none.
"""
from __future__ import annotations

from jevlab import metrics as M
from jevlab import policy as P
from jevlab import report
from jevlab import stats as S
from jevlab.floors import crisis_floor
from jevlab.runs import load_experiment

from ..crisis_severity.items import all_items
from ..crisis_severity.run import HEADLINE_TAU as CRISIS_TAU
from ..crisis_severity.run import evaluate, load_baseline
from ..trainee_conduct import questions as Q
from ..trainee_conduct.run import HEADLINE_TAU as TRAINEE_TAU
from ..trainee_conduct.run import CONTROL, OMISSION_ARC, TARGETS, arcs, extra_arcs, extra_turns, guard_turns


def _name(k) -> str:
    return f"{k[0]}:{k[1]}" + ("" if k[2] in ("verbalised", "native") else f" ({k[2]})")


def crisis_section() -> tuple[str, dict]:
    items = all_items()
    ids = {i.id for i in items}
    floor = {i.id: crisis_floor(i.text) for i in items}
    rows = [("lexicon floor", evaluate(items, lambda i: floor[i.id]))]
    base = load_baseline()
    if base:
        clf = {k: v["classifier_level"] for k, v in base["by_id"].items()}
        rows.append(("lexicon ∪ Sonnet 4.5 ([partner] incumbent, its own prompt)", evaluate(items, lambda i: P.max_level(floor[i.id], clf[i.id]))))
    judges = load_experiment("crisis_fixtures")
    ops = []
    for k, rr in sorted(judges.items()):
        ok = {i: r for i, r in rr.items() if i in ids and r["status"] == "ok"}
        if len(ok) < 0.95 * len(ids):
            continue
        probs = {i: r["answers"]["severity"]["p"] for i, r in ok.items()}
        lvl = lambda i, probs=probs: P.LEVELS[max(range(5), key=probs[i.id].__getitem__)] if i.id in probs else None
        rows.append((f"{_name(k)} alone (argmax)", evaluate(items, lvl)))
        rows.append((f"lexicon ∪ {_name(k)} τ={CRISIS_TAU}",
                     evaluate(items, lambda i, probs=probs: P.union(floor[i.id], probs[i.id], CRISIS_TAU) if i.id in probs else floor[i.id])))
        rs = [rr[i] for i in ids if i in rr]
        lat = [r["latency_ms"] for r in rs if r["status"] != "error"]
        ops.append([_name(k), len(rs), sum(r["status"] == "parse_failed" for r in rs), sum(r["status"] == "error" for r in rs),
                    f"{S.percentile(lat, .5):.0f}", f"{S.percentile(lat, .95):.0f}", f"${sum(r['cost_usd'] for r in rs) / len(rs) * 1000:.3f}",
                    rs[0]["sampling"], rs[0]["reasoning"]])
    # Two views of the probability distribution. The first asks what happens to a
    # judge's accuracy as the safety threshold is turned down; it runs on the 84 Set A
    # arcs alone, which are blind-authored and share no wording with any judge's
    # criteria, and it is the one Finding 1 rests on. The second asks why, and it runs
    # on all 305 fixture items, so 86 of them are the bank the lexicon was tuned on and
    # the criteria were adapted from. Read the second as mechanism, not as evidence. A judge whose uncertainty is compressed into a narrow band has a cliff
    # rather than a dial, because one threshold step moves nearly every item at once.
    LADDER = (0.05, 0.1, 0.2, 0.3, 0.5)
    COVERAGE = 0.95
    n_arcs = rows[0][1]["arcs"]
    ladder, shape = [], []
    for k, rr in sorted(judges.items()):
        probs = {i: r["answers"]["severity"]["p"] for i, r in rr.items() if i in ids and r["status"] == "ok"}
        if len(probs) < COVERAGE * len(ids):
            continue
        arc_exact = []
        for t in LADDER:
            arc_exact.append(evaluate(items, lambda i, t=t: P.tail_level(probs[i.id], t) if i.id in probs else None)["arc_exact"])
        am = evaluate(items, lambda i: P.LEVELS[max(range(5), key=probs[i.id].__getitem__)] if i.id in probs else None)["arc_exact"]
        vals = arc_exact + [am]
        ladder.append([_name(k), *[f"{v}/{n_arcs}" for v in vals], max(vals) - min(vals)])
        tails = []
        for i in ids:
            if i in probs:
                pr = probs[i]
                a = max(range(5), key=pr.__getitem__)
                tails.append(sum(pr[j] for j in range(a + 1, 5)))
        shape.append([_name(k), rr[next(iter(probs))]["elicitation"], len(tails),
                      f"{sum(1 for t in tails if t < 0.05) / len(tails):.1%}",
                      f"{sum(1 for t in tails if t > 0.2) / len(tails):.1%}",
                      f"{S.percentile(tails, .5):.3f}"])
    ladder.sort(key=lambda r: r[-1])

    body = ["## Crisis severity: [partner] clinical fixtures (86 bank phrases, 84 Set A arcs)\n",
            "Same scorer as the phase-1 report. Every judge receives the identical questions; the incumbent row is [partner]'s own prompt.\n",
            report.table(["Configuration", "Bank recall", "Bank false fires", "Bank exact", "Bank under", "Arc exact", "Arc under", "Arc over", "First-response under"],
                         [[n, M.ratio(r["bank_recall"], r["bank_must"]), M.ratio(r["bank_false_fires"], r["bank_must_not"]), M.ratio(r["bank_exact"], r["bank_must"]),
                           len(r["bank_under"]), M.ratio(r["arc_exact"], r["arcs"]), len(r["arc_under"]), r["arc_over"],
                           M.ratio(len(r["first_response_under"]), r["crisis_expected"])] for n, r in rows]),
            "\n### Set A arcs: exactness across the threshold ladder, judge alone\n",
            "Each judge's arc accuracy at every pre-registered threshold and at its own best answer. "
            "The span is best minus worst: a small span means the safety dial can be turned without "
            "changing what the judge does, a large one means safety and accuracy are the same dial.\n",
            report.table(["Judge", *[f"τ={t}" for t in LADDER], "argmax", "Span"], ladder),
            "\n### Shape of the probability output (all 305 fixture items)\n",
            "Mass a judge places outside its own chosen level. Confident is below 0.05, genuinely unsure above 0.2; "
            "a judge with little of either hedges in a narrow band, which is what makes a threshold a cliff.\n",
            report.table(["Judge", "Elicitation", "n", "Confident (<0.05)", "Unsure (>0.2)", "Median tail"], shape),
            "\n### Operations\n", report.table(["Judge", "Calls", "Parse failed", "Errors", "p50 ms", "p95 ms", "USD/1k", "Sampling", "Reasoning"], ops)]
    raw = {"rows": {n: {k: v for k, v in r.items() if k != "levels"} for n, r in rows}, "ops": ops,
           "ladder": ladder, "ladder_taus": list(LADDER), "shape": shape}
    return "\n".join(body), raw


def trainee_section() -> tuple[str, dict]:
    guard, extra, cases, xarcs = guard_turns(), extra_turns(), arcs(), extra_arcs()
    every = guard + extra + [t for ts in cases.values() for t in ts] + [t for _, ts in xarcs.values() for t in ts]
    ids = {t.key for t in every}
    judges = load_experiment("trainee_fixtures")

    def counts(turns, jev_rows, tau):
        tp = fn = fp = tn = 0
        for t in turns:
            for harm, truth in t.labels:
                if harm not in ("stated_feelings", "leading", "judged", "boundary") and not t.risk:
                    continue
                base = Q.floor(harm, t.trainee, qc_step=t.qc_step)
                got = base
                if jev_rows is not None and not Q.exempt(harm, t.trainee, qc_step=t.qc_step):
                    r = jev_rows.get(t.key)
                    if r and r["status"] == "ok":
                        a = r["answers"]
                        p = a["question_style"]["probabilities"]["leading"] if harm == "leading" else a[harm]["noul"]
                        got = base or p >= tau
                tp += got and truth; fn += (not got) and truth; fp += got and not truth; tn += (not got) and not truth
        return tp, fn, fp, tn

    rows = []
    for name, jr in [("regex floor", None)] + [(f"regex ∪ {_name(k)} τ={TRAINEE_TAU}", rr) for k, rr in sorted(judges.items())
                                                  if sum(1 for i in ids if i in rr and rr[i]["status"] == "ok") >= 0.95 * len(ids)]:
        g = counts(guard, jr, TRAINEE_TAU)
        e = counts(extra, jr, TRAINEE_TAU)
        all_harms = [h for h in Q.FLAGGABLE if h not in ("leading", "stated_feelings")]
        def flagged_case(cid, harms):
            for t in cases[cid]:
                for h in harms:
                    base = Q.floor(h, t.trainee, qc_step=False)
                    if base:
                        return True
                    if jr is not None:
                        r = jr.get(t.key)
                        if r and r["status"] == "ok":
                            a = r["answers"]
                            p = a["question_style"]["probabilities"]["leading"] if h == "leading" else a[h]["noul"]
                            if p >= TRAINEE_TAU:
                                return True
            return False
        caught = sum(1 for cid, harms in TARGETS.items() if harms and flagged_case(cid, harms))
        control = sum(1 for h in all_harms if flagged_case(CONTROL, [h]))
        rows.append([name, M.ratio(g[0], g[0] + g[1]), M.ratio(g[2], g[2] + g[3]), M.ratio(e[0], e[0] + e[1]), M.ratio(e[2], e[2] + e[3]),
                     M.ratio(caught, sum(1 for h in TARGETS.values() if h)), control])
    body = ["## Trainee conduct: [partner] clinical fixtures + supplementary paraphrases\n",
            f"Regex floor OR judge p ≥ {TRAINEE_TAU}, the phase-1 headline threshold, applied to every judge alike.\n",
            report.table(["Configuration", "Guard caught (13, clinical)", "Guard false flags", "Extra caught (60, unreviewed)", "Extra false flags",
                          "Misconduct arcs flagged", "Flags on good-practice control"], rows)]
    return "\n".join(body), {"rows": rows}


def main() -> None:
    c, craw = crisis_section()
    t, traw = trainee_section()
    body = c + "\n\n" + t
    print(body)
    print("\nwrote", report.write("compare-fixtures", "All judges on the phase-1 clinical fixtures", body, {"crisis": craw, "trainee": traw}))


if __name__ == "__main__":
    main()
