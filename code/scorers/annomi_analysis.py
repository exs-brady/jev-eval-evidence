"""AnnoMI report: judge vs majority gold, human placement, calibration.

  uv run python -m experiments.annomi_codes.analysis
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any

from jevlab import report
from jevlab import stats as S
from jevlab.runs import load_experiment

from . import gold, sample
from .questions import BEHAVIOUR, TALK

ITERS = 2000
PLACEMENT_ITERS = 500   # 10 leave-one-out golds per draw; 500 is the practical ceiling
COVERAGE = 0.95
BEH = list(BEHAVIOUR.criteria)
TLK = list(TALK.criteria)


def _name(k) -> str:
    return f"{k[0]}:{k[1]}"


def _hard(task: str, row: dict) -> str | None:
    a = row["answers"]
    if task == "behaviour":
        return a["behaviour"]["choice"]
    if task == "talk":
        return a["talk"]["choice"]
    if task == "open":
        return "open" if a["open"]["noul"] >= 0.5 else "closed"
    if task == "complex":
        return "complex" if a["complex"]["noul"] >= 0.5 else "simple"
    raise ValueError(task)


def _probs(task: str, row: dict) -> list[float]:
    a = row["answers"]
    if task == "behaviour":
        return [a["behaviour"]["probabilities"][o] for o in BEH]
    if task == "talk":
        return [a["talk"]["probabilities"][o] for o in TLK]
    raise ValueError(task)


def task_units(task: str, ids: list[str] | None) -> list[dict]:
    role = "client" if task == "talk" else "therapist"
    gtask = {"behaviour": "behaviour", "open": "question", "complex": "reflection", "talk": "talk"}[task]
    out = []
    keep = set(ids) if ids is not None else None
    for u in gold.load().values():
        if u.role != role:
            continue
        uid = f"{u.tid}:{u.uid}"
        if keep is not None and uid not in keep:
            continue
        g = gold.gold_for(u, gtask)
        # How many coders stand behind that label. AnnoMI is 9,271 singly-coded
        # utterances plus 428 coded by all ten, so majority() returns a lone
        # coder's opinion for most units. "Majority gold" is then a courtesy
        # title, and a table that does not separate the two is comparing a
        # ten-coder consensus with one person's reading under a single heading.
        out.append({"id": uid, "tid": u.tid, "url": u.video_url, "gold": g, "n_raters": len(u.annotators),
                    "consensus": len(u.annotators) > 1, "contested": gold.contested(u, gtask), "utt": u})
    return out


def agreement_table(task: str, tier: str, judges: dict, units: list[dict], chan: dict[str, str]) -> tuple[list[list], dict]:
    scored = [u for u in units if u["gold"] is not None]
    rows, raw = [], {}
    for k, rr in judges.items():
        pairs_all = [(u["gold"], _hard(task, rr[u["id"]])) for u in scored if u["id"] in rr and rr[u["id"]]["status"] == "ok"]
        if len(pairs_all) < COVERAGE * len(scored):
            rows.append([_name(k), f"{len(pairs_all)}/{len(scored)}", "not scored (coverage)", "", "", "", "", ""])
            continue
        us = [u for u in scored if u["id"] in rr and rr[u["id"]]["status"] == "ok"]
        pairs_of = lambda xs, rr=rr: [(u["gold"], _hard(task, rr[u["id"]])) for u in xs]
        ac1 = S.bootstrap_ci(us, lambda xs: S.ac1_nominal(pairs_of(xs)), cluster=lambda u: u["tid"], iters=ITERS)
        ac1_ch = S.bootstrap_ci(us, lambda xs: S.ac1_nominal(pairs_of(xs)), cluster=lambda u: chan.get(u["url"], u["url"]), iters=500)
        kap = S.bootstrap_ci(us, lambda xs: S.kappa_nominal(pairs_of(xs)), cluster=lambda u: u["tid"], iters=500)
        acc = S.bootstrap_ci(us, lambda xs: S.rate([g == p for g, p in pairs_of(xs)]), cluster=lambda u: u["tid"], iters=500)
        mf1 = S.macro_f1(pairs_of(us))
        # The same figure against a ten-coder consensus only. Where the pooled
        # column and this one disagree, the pooled column is measuring agreement
        # with individual coders' idiosyncrasies, not with expert consensus.
        cons = [u for u in us if u["consensus"]]
        # Carries its own interval: a bare point estimate beside CI-bearing columns
        # reads as the precise one, which is backwards — this column has the smaller n.
        c_ac1 = (S.bootstrap_ci(cons, lambda xs: S.ac1_nominal(pairs_of(xs)), cluster=lambda u: u["tid"], iters=500)
                 if len(cons) >= 50 else (None, None, None))
        rows.append([_name(k), len(us), S.fmt_ci(*ac1), f"[{ac1_ch[1]:.3f}, {ac1_ch[2]:.3f}]" if ac1_ch[1] is not None else "n/a",
                     f"{S.fmt_ci(*c_ac1)} (n={len(cons)})" if c_ac1[0] is not None else "n/a",
                     S.fmt_ci(*kap), S.fmt_ci(*acc), f"{mf1:.3f}" if mf1 is not None else "n/a"])
        raw[_name(k)] = {"n": len(us), "ac1": ac1, "ac1_channel_ci": ac1_ch[1:], "kappa": kap, "accuracy": acc,
                         "macro_f1": mf1, "ac1_consensus_gold": c_ac1, "n_consensus": len(cons)}
    return rows, raw


def paired_vs_jev(task: str, judges: dict, units: list[dict]) -> tuple[list[list], dict]:
    """AC1 difference judge − Jev over the same resampled transcripts, on units both scored."""
    jev = next((k for k in judges if k[0] == "typesafe"), None)
    rows, raw = [], {}
    if jev is None:
        return rows, raw
    jr = judges[jev]
    for k, rr in judges.items():
        if k == jev:
            continue
        us = [u for u in units if u["gold"] is not None and u["id"] in rr and rr[u["id"]]["status"] == "ok"
              and u["id"] in jr and jr[u["id"]]["status"] == "ok"]
        if len(us) < 50:
            continue
        a = lambda xs, rr=rr: S.ac1_nominal([(u["gold"], _hard(task, rr[u["id"]])) for u in xs])
        b = lambda xs: S.ac1_nominal([(u["gold"], _hard(task, jr[u["id"]])) for u in xs])
        d = S.paired_diff_ci(us, a, b, cluster=lambda u: u["tid"], iters=ITERS)
        sig = "yes" if d[1] is not None and (d[1] > 0 or d[2] < 0) else "no"
        rows.append([f"{_name(k)} − Jev", len(us), S.fmt_ci(*d), sig])
        raw[_name(k)] = {"n": len(us), "diff": d, "excludes_zero": sig == "yes"}
    return rows, raw


def panel_reliability(task: str) -> dict | None:
    """Krippendorff's alpha over the coders themselves. Every other table here asks
    how close a rater is to a consensus; this asks whether the codebook is
    dependable, which is the ceiling all of them are measured against."""
    gtask = {"behaviour": "behaviour", "talk": "talk"}[task]
    role = "client" if task == "talk" else "therapist"
    field = {"behaviour": "behaviour", "talk": "talk"}[task]
    valid = set(BEH if task == "behaviour" else TLK)
    ann = gold.annotator_ids()
    units, unanimous, no_majority = [], 0, 0
    for u in gold.load().values():
        if u.role != role:
            continue
        vals = [u.annotators[a][field] for a in ann if a in u.annotators and u.annotators[a][field] in valid]
        if len(vals) < 2:
            continue
        units.append(vals)
        unanimous += len(set(vals)) == 1
        no_majority += gold.gold_for(u, gtask) is None
    if not units:
        return None
    pairs = [(x, y) for vals in units for i, x in enumerate(vals) for y in vals[i + 1:]]
    # One AC1 over every coder pair pooled, not the mean of the individual pair
    # coefficients: same quantity to within rounding here, but it is the pooled
    # estimator and the label should say what was computed.
    return {"alpha": S.krippendorff_alpha_nominal(units), "n_units": len(units),
            "unanimous": unanimous, "no_majority": no_majority,
            "pooled_pairwise_ac1": S.ac1_nominal(pairs)}


def placement(task: str, judges: dict) -> tuple[list[list], dict]:
    """Leave-one-annotator-out AC1 for each annotator and each judge on the ceiling
    subset, with a transcript-clustered bootstrap interval for every rater.

    The interval is not decoration. Without it this table prints nine point
    estimates in a line and reads as a ranking; the differences between most of
    them are smaller than the interval, and a whole category's worth of items can
    move a judge several places. Humans and judges are bootstrapped the same way,
    because an interval on one and not the other is the asymmetry that produced
    amendment B1."""
    gtask = {"behaviour": "behaviour", "talk": "talk"}[task]
    role = "client" if task == "talk" else "therapist"
    field = {"behaviour": "behaviour", "talk": "talk"}[task]
    opts = BEH if task == "behaviour" else TLK
    ceiling = [u for u in gold.ceiling_subset() if u.role == role]
    ann = gold.annotator_ids()
    uids = [f"{u.tid}:{u.uid}" for u in ceiling]
    cl = lambda x: x.split(":")[0]
    n_tid = len({cl(x) for x in uids})

    # Resolve every leave-one-out gold and own-label once; scoring then only indexes.
    loo: dict[str, dict[str, str | None]] = {a: {} for a in ann}
    own: dict[str, dict[str, str | None]] = {a: {} for a in ann}
    for u in ceiling:
        uid = f"{u.tid}:{u.uid}"
        for a in ann:
            loo[a][uid] = gold.gold_for(u, gtask, exclude=a)
            mine = u.annotators.get(a, {}).get(field)
            own[a][uid] = mine if mine in opts else None

    def ann_score(a: str, xs):
        prs = [(loo[a][x], own[a][x]) for x in xs if loo[a][x] is not None and own[a][x] is not None]
        return S.ac1_nominal(prs)

    def judge_score(hard: dict[str, str | None], xs):
        vals = [v for v in (S.ac1_nominal([(loo[a][x], hard[x]) for x in xs
                                           if loo[a][x] is not None and hard.get(x) is not None]) for a in ann)
                if v is not None]
        return sum(vals) / len(vals) if vals else None

    rows, raw = [], {"annotators": {}, "judges": {}, "n_transcripts": n_tid}
    for a in ann:
        pt, lo, hi = S.bootstrap_ci(uids, lambda xs, a=a: ann_score(a, xs), cluster=cl, iters=PLACEMENT_ITERS)
        n = sum(1 for x in uids if loo[a][x] is not None and own[a][x] is not None)
        raw["annotators"][a] = {"ac1": pt, "ci": [lo, hi], "n": n}
        rows.append([f"annotator {a}", n, f"{pt:.3f}" if pt is not None else "n/a",
                     f"[{lo:.3f}, {hi:.3f}]" if lo is not None else "n/a", "—"])

    for k, rr in judges.items():
        # A judge is placed only if it answered nearly every ceiling utterance.
        # Without this a partial run yields a confident-looking number computed on
        # whichever subset happened to land (amendment B1).
        answered = [u for u in ceiling if (rr.get(f"{u.tid}:{u.uid}") or {}).get("status") == "ok"]
        if len(answered) < COVERAGE * len(ceiling):
            rows.append([_name(k), f"{len(answered)}/{len(ceiling)}", "not placed (incomplete)", "", ""])
            continue
        hard = {x: (_hard(task, rr[x]) if (rr.get(x) or {}).get("status") == "ok" else None) for x in uids}
        pt, lo, hi = S.bootstrap_ci(uids, lambda xs: judge_score(hard, xs), cluster=cl, iters=PLACEMENT_ITERS)
        if pt is None:
            continue
        # The ten leave-one-out golds do not all resolve on the same utterances, so
        # the score is a mean over ten slightly different pair sets. Printing the
        # largest of them (what this did before) overstates the evidence.
        counts = [sum(1 for x in uids if loo[a][x] is not None and hard.get(x) is not None) for a in ann]
        used = f"{min(counts)}" if min(counts) == max(counts) else f"{min(counts)}–{max(counts)}"
        human = [v["ac1"] for v in raw["annotators"].values() if v["ac1"] is not None]
        beats = sum(1 for v in human if pt > v)
        # Paired against Jev over the same resampled transcripts.
        jev = next((kk for kk in judges if kk[0] == "typesafe"), None)
        sig = ""
        if jev is not None and k != jev:
            jh = {x: (_hard(task, judges[jev][x]) if (judges[jev].get(x) or {}).get("status") == "ok" else None) for x in uids}
            d = S.paired_diff_ci(uids, lambda xs: judge_score(hard, xs), lambda xs: judge_score(jh, xs),
                                 cluster=cl, iters=PLACEMENT_ITERS)
            if d[1] is not None:
                sig = f"{d[0]:+.3f} [{d[1]:+.3f}, {d[2]:+.3f}]" + ("" if (d[1] > 0 or d[2] < 0) else " (ns)")
        raw["judges"][_name(k)] = {"ac1": pt, "ci": [lo, hi], "n_pairs_min": min(counts), "n_pairs_max": max(counts),
                                   "n_answered": len(answered), "vs_jev": sig}
        rows.append([_name(k), used, f"{pt:.3f}", f"[{lo:.3f}, {hi:.3f}]" if lo is not None else "n/a",
                     f"above {beats} of {len(human)}" + (f" · vs Jev {sig}" if sig else "")])
    return rows, raw


def calibration(task: str, judges: dict, units: list[dict]) -> tuple[list[list], dict]:
    opts = BEH if task == "behaviour" else TLK
    rows, rel = [], {}
    for k, rr in judges.items():
        pr, gi = [], []
        for u in units:
            r = rr.get(u["id"])
            if u["gold"] is not None and r and r["status"] == "ok":
                pr.append(_probs(task, r)); gi.append(opts.index(u["gold"]))
        # Coverage gate (amendment B1), not a bare minimum count: a flat "at least
        # 50 rows" floor scores a judge on whatever subset happened to land, which
        # is how a 95%-failed run reached a calibration table once already.
        scorable = sum(u["gold"] is not None for u in units)
        if len(pr) < COVERAGE * scorable:
            rows.append([_name(k), k[2], f"{len(pr)}/{scorable}", "not scored (coverage)", ""])
            continue
        el = k[2]
        b, e = S.multiclass_brier(pr, gi), S.top_label_ece(pr, gi)
        rows.append([_name(k), el, len(pr), f"{b:.3f}", f"{e:.3f}"])
        conf = [max(p) for p in pr]; hit = [max(range(len(p)), key=p.__getitem__) == g for p, g in zip(pr, gi)]
        rel[_name(k)] = {"elicitation": el, "ece": e, "bins": S.reliability_bins(conf, hit)}
    return rows, rel


def ops(judges: dict, ids: set[str]) -> list[list]:
    out = []
    for k, rr in judges.items():
        rs = [rr[i] for i in ids if i in rr]
        if not rs:
            continue
        # Batch rows carry latency_ms = 0; averaging them in prints "0 ms" for a
        # judge that was never measured live (compare/run.py guards this the same way).
        lat = [r["latency_ms"] for r in rs if r["status"] != "error" and not r.get("extra", {}).get("batch")]
        p50 = f"{S.percentile(lat, .5):.0f}" if lat else "batch only"
        p95 = f"{S.percentile(lat, .95):.0f}" if lat else ""
        out.append([_name(k), len(rs), sum(r["status"] == "parse_failed" for r in rs), sum(r["status"] == "error" for r in rs),
                    sum(any("unwrapped_answer" in f for f in r["flags"]) for r in rs),
                    p50, p95, f"${sum(r['cost_usd'] for r in rs) / len(rs) * 1000:.3f}",
                    rs[0]["sampling"], rs[0]["reasoning"]])
    return out


def main() -> None:
    samples = sample.load()
    chan = gold.channels()
    L: list[str] = []
    raw: dict[str, Any] = {}
    for exp, tasks in (("annomi_therapist", ("behaviour", "open", "complex")), ("annomi_client", ("talk",))):
        judges = load_experiment(exp)
        for task in tasks:
            raw[task] = {}
            for tier, ids in (("local", samples["local"]), ("hosted", samples["hosted"]), ("all", None)):
                units = task_units(task, ids)
                present = {k: rr for k, rr in judges.items() if sum(u["id"] in rr for u in units) >= COVERAGE * len(units)}
                if not present:
                    continue
                rows, r = agreement_table(task, tier, present, units, chan)
                n_gold = sum(u["gold"] is not None for u in units)
                n_cons = sum(u["gold"] is not None and u["consensus"] for u in units)
                n_single = n_gold - n_cons
                L.append(f"## {task}: {tier} sample ({len(units)} utterances; {n_gold} with a gold label"
                         + (", the rest have no such code" if task in ("open", "complex") else "")
                         + f"; {sum(u['contested'] for u in units)} contested)\n")
                L.append(f"Of the {n_gold} gold labels, **{n_cons} come from a ten-coder majority and {n_single} "
                         f"from a single coder** ({n_single / n_gold:.0%} of the total). AnnoMI codes most of its "
                         "corpus once; only 428 utterances carry all ten annotators. The pooled AC1 column below is "
                         "therefore mostly agreement with one arbitrary coder, whose own agreement with colleagues "
                         "averages 0.74. The consensus-only column is the like-for-like expert comparison.\n")
                L.append(report.table(["Judge", "n", "AC1 vs pooled gold [95% CI, transcript-clustered]", "AC1 CI (channel-clustered)",
                                       "AC1 vs 10-coder gold", "Kappa", "Accuracy", "Macro-F1"], rows))
                raw[task][tier] = r
                prow, praw = paired_vs_jev(task, present, units)
                if prow:
                    L.append(f"\n### {task}, {tier}: paired AC1 difference vs Jev (same resampled transcripts)\n")
                    L.append(report.table(["Comparison", "n", "Difference [95% CI]", "CI excludes 0"], prow))
                    raw[task][f"{tier}_paired"] = praw
                if task in ("behaviour", "talk"):
                    crow, rel = calibration(task, present, units)
                    if crow:
                        L.append(f"\n### {task} calibration, {tier} (within an elicitation only)\n")
                        L.append(report.table(["Judge", "Elicitation", "n", "Multiclass Brier", "Top-label ECE"], crow))
                        raw[task][f"{tier}_calibration"] = rel
                L.append("")
            if task in ("behaviour", "talk") and judges:
                pan = panel_reliability(task)
                if pan and pan["alpha"] is not None:
                    L.append(f"### {task}: how reliable is the codebook itself?\n")
                    L.append(f"Krippendorff's alpha over the coders alone, on the {pan['n_units']} multiply-coded utterances: "
                             f"**{pan['alpha']:.3f}**. They agree unanimously on {pan['unanimous']} of them "
                             f"({pan['unanimous'] / pan['n_units']:.0%}) and reach no majority on {pan['no_majority']}. "
                             f"Agreement between two coders, pooled over all {len(gold.annotator_ids())} choose 2 pairs, is "
                             f"{pan['pooled_pairwise_ac1']:.3f}.\n")
                    L.append("This is the ceiling every judge below is measured against. A judge cannot agree with a "
                             "consensus more reliably than the consensus agrees with itself, and where alpha is low the "
                             "remaining error is in the labels, not in the models.\n")
                    raw[task]["panel_reliability"] = pan
                prow, praw = placement(task, judges)
                L.append(f"### {task}: placement among the ten annotators (ceiling subset, leave-one-annotator-out golds)\n")
                L.append("Each rater, human or model, is scored against the majority of the other nine annotators. "
                         "A consensus target rewards consistency, so a model can rank above individual annotators without "
                         "being a better coder than any of them; read the standing as 'within the human range' or not.\n")
                L.append(f"**Read the intervals, not the order.** This subset is small and comes from only "
                         f"{praw.get('n_transcripts', '?')} transcripts, so the intervals are wide and overlap heavily. "
                         "The paired column is the test that matters: where it says (ns), that rater and Jev are not "
                         "distinguishable on this evidence, however far apart their point estimates look. A single "
                         "category's worth of items moves a judge several places.\n")
                L.append(report.table(["Rater", "n", "AC1 vs the other nine", "95% CI (transcript-clustered)", "Standing"], prow))
                L.append("")
                raw[task]["placement"] = praw
        L.append(f"### Operations, {exp}\n")
        L.append(report.table(["Judge", "Calls", "Parse failed", "Errors", "Unwrapped (A6)", "p50 ms", "p95 ms", "USD/1k", "Sampling", "Reasoning"],
                              ops(judges, {u["id"] for u in task_units(tasks[0], None)})))
        L.append("")
    body = "\n".join(L)
    print(body)
    print("\nwrote", report.write("annomi-codes", "AnnoMI utterance coding: judges vs expert majority", body, raw))


if __name__ == "__main__":
    main()
