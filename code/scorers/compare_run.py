"""Compare every judge on a synthetic use case, per docs/PREREGISTRATION.md.

  uv run python -m experiments.compare.run crisis --split dev --freeze   # choose τ, write docs/THRESHOLDS.md
  uv run python -m experiments.compare.run crisis --split test           # the report

Every judge (Jev included) goes through the same policy: hard label = argmax,
policy row = floor ∪ judge at the frozen τ. Judges with < 95% coverage of the
split are listed but not scored.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from jevlab import policy as P
from jevlab import report
from jevlab import stats as S
from jevlab.floors import crisis_floor
from jevlab.items import Item, read
from jevlab.runs import load_experiment
from jevlab.synth import verify

from ..trainee_conduct import questions as TQ

ROOT = Path(__file__).resolve().parents[2]
THRESHOLDS = ROOT / "docs" / "THRESHOLDS.md"
CRISIS_TAUS = (0.05, 0.1, 0.2, 0.3, 0.5)
TRAINEE_TAUS = (0.3, 0.5, 0.7, 0.9)
ASK_TAU = 0.5
DISCLOSED_TAU = 0.5
GRACES = (1, 2)
COVERAGE = 0.95
ITERS = 2000

JudgeKey = tuple[str, str, str]


def _judges(experiment: str, ids: set[str]) -> dict[JudgeKey, dict[str, dict]]:
    out = {}
    for key, rows in load_experiment(experiment).items():
        have = {i: r for i, r in rows.items() if i in ids}
        out[key] = have
    return out


def _name(k: JudgeKey) -> str:
    return f"{k[0]}:{k[1]}" + ("" if k[2] == "verbalised" or k[2] == "native" else f" ({k[2]})")


def load_frozen() -> dict[str, Any]:
    p = THRESHOLDS.with_suffix(".json")
    return json.loads(p.read_text()) if p.exists() else {}


def freeze(use_case: str, chosen: dict[str, Any]) -> None:
    """Incremental: a judge's threshold is fixed the first time it is chosen
    and never overwritten, so judges whose dev runs finish later join the
    frozen file without disturbing the others."""
    p = THRESHOLDS.with_suffix(".json")
    data = load_frozen()
    prev = data.get(use_case, {})
    chosen = {**chosen, "judges": {**chosen["judges"], **prev.get("judges", {})}}
    data[use_case] = chosen
    p.write_text(json.dumps(data, indent=1) + "\n")
    THRESHOLDS.write_text(render_thresholds(data))


def render_thresholds(data: dict[str, Any]) -> str:
    """The frozen file as Markdown. The "Chosen by" column is not decoration:
    when no candidate τ meets the false-fire constraint the code falls back to
    the lowest-false-fire τ, and a table that does not say so reads as though
    the pre-registered rule selected every row."""
    lines = ["# Frozen thresholds", "", "Chosen on the dev split by the rule in docs/PREREGISTRATION.md, then frozen. "
             "Test-split reports read this file and never re-tune.", "",
             "`rule` = a τ met the false-fire constraint. `fallback` = none did, so the τ with the "
             "lowest dev false-fire was taken; that row's τ is **not** a product of the pre-registered rule.", ""]
    for uc, ch in data.items():
        lines.append(f"## {uc}")
        lines.append("")
        lines.append(report.table(["Judge", "τ / grace", "dev false-fire", "dev criterion", "Chosen by"],
                                  [[j, v["tau"], f"{v['false_fire']:.3f}", f"{v['criterion']:.3f}",
                                    "fallback" if v.get("fallback") else "rule"] for j, v in ch["judges"].items()]))
        n_fb = sum(1 for v in ch["judges"].values() if v.get("fallback"))
        lines.append(f"\nFloor false-fire on dev: {ch['floor_false_fire']:.3f}. Rule: {ch['rule']}")
        lines.append(f"\nChosen by the fallback, not the rule: {n_fb} of {len(ch['judges'])}.\n")
    return "\n".join(lines)


# ── crisis ───────────────────────────────────────────────────────────────────

def _lvl(v: str | None) -> str | None:
    return None if v in (None, "none") else v


def crisis_units(items: list[Item]) -> list[dict]:
    """One unit per single item or per arc. Intended level is the cell's."""
    arcs: dict[str, list[Item]] = defaultdict(list)
    units = []
    for it in items:
        if it.arc_id:
            arcs[it.arc_id].append(it)
        else:
            units.append({"id": it.id, "cluster": it.id, "turns": [it], "intended": _lvl(it.intended["level"]),
                          "third_party": it.intended["third_party"], "family": it.generator["family"],
                          "contested": it.contested, "form": "single", "lang": it.cell["lang"], "distractor": it.cell["distractor"]})
    for arc, turns in arcs.items():
        turns.sort(key=lambda t: t.turn)
        units.append({"id": arc, "cluster": arc, "turns": turns, "intended": _lvl(turns[0].intended["level"]),
                      "third_party": turns[0].intended["third_party"], "family": turns[0].generator["family"],
                      "contested": any(t.contested for t in turns), "form": "arc", "lang": turns[0].cell["lang"],
                      "distractor": turns[0].cell["distractor"]})
    return units


def crisis_level(rows: dict[str, dict], unit: dict, tau: float | None, floor: bool) -> str | None:
    """Level reached over the unit's turns under one configuration."""
    reached = None
    for t in unit["turns"]:
        f = crisis_floor(t.text) if floor else None
        r = rows.get(t.id)
        j = None
        if r and r["status"] == "ok":
            ps = r["answers"]["severity"]["p"]
            j = P.tail_level(ps, tau) if tau is not None else P.LEVELS[r["answers"]["severity"]["level"]]
        reached = P.max_level(reached, f, j)
    return reached


def crisis_metrics(units: list[dict], level_of) -> dict[str, Any]:
    sev = P.SEV
    got = {u["id"]: level_of(u) for u in units}
    under = lambda us: S.rate([sev[got[u["id"]]] < sev[u["intended"]] for u in us])
    exact = lambda us: S.rate([got[u["id"]] == u["intended"] for u in us])
    ff = lambda us: S.rate([got[u["id"]] is not None for u in us if u["intended"] is None])
    over = lambda us: S.rate([sev[got[u["id"]]] > sev[u["intended"]] for u in us if u["intended"] is not None])
    cl = lambda u: u["cluster"]
    return {"under": S.bootstrap_ci(units, under, cluster=cl, iters=ITERS), "exact": S.bootstrap_ci(units, exact, cluster=cl, iters=ITERS),
            "false_fire": S.bootstrap_ci(units, ff, cluster=cl, iters=ITERS), "over": S.bootstrap_ci(units, over, cluster=cl, iters=ITERS),
            "_fns": {"under": under, "exact": exact, "false_fire": ff}, "_got": got}


def run_crisis(split: str, do_freeze: bool) -> tuple[str, dict]:
    items = [i for i in read("crisis") if i.split == split]
    verify.apply("crisis", items)
    units = crisis_units(items)
    ids = {t.id for u in units for t in u["turns"]}
    judges = _judges("crisis_synth", ids)
    covered = {k: rows for k, rows in judges.items() if len([i for i in ids if i in rows and rows[i]["status"] != "error"]) >= COVERAGE * len(ids)}
    skipped = [k for k in judges if k not in covered]

    floor_m = crisis_metrics(units, lambda u: crisis_level({}, u, None, True))
    frozen = load_frozen().get("crisis", {}).get("judges", {})
    chosen: dict[str, Any] = {}
    rows_out: list[tuple[str, dict]] = [("lexicon floor", floor_m)]
    per_judge: dict[str, dict] = {}
    for k, rows in covered.items():
        name = _name(k)
        alone = crisis_metrics(units, lambda u, rows=rows: crisis_level(rows, u, None, False))
        rows_out.append((f"{name} alone (argmax)", alone))
        if do_freeze and name in frozen:
            tau = frozen[name]["tau"]
        elif do_freeze:
            cands = []
            for tau in CRISIS_TAUS:
                m = crisis_metrics(units, lambda u, rows=rows, tau=tau: crisis_level(rows, u, tau, True))
                cands.append((tau, m["false_fire"][0] or 0.0, m["under"][0] or 0.0))
            ok = [c for c in cands if c[1] <= (floor_m["false_fire"][0] or 0.0)]
            pick = min(ok, key=lambda c: (c[0], c[2])) if ok else min(cands, key=lambda c: (c[1], c[2]))
            chosen[name] = {"tau": pick[0], "false_fire": pick[1], "criterion": pick[2], "fallback": not ok}
            tau = pick[0]
        else:
            if name not in frozen:
                rows_out.append((f"{name} (no frozen τ; run --split dev --freeze first)", alone))
                continue
            tau = frozen[name]["tau"]
        m = crisis_metrics(units, lambda u, rows=rows, tau=tau: crisis_level(rows, u, tau, True))
        rows_out.append((f"lexicon ∪ {name} τ={tau}", m))
        per_judge[name] = {"rows": rows, "tau": tau, "policy": m, "alone": alone}

    if do_freeze:
        freeze("crisis", {"judges": chosen, "floor_false_fire": floor_m["false_fire"][0] or 0.0,
                          "rule": "lowest τ with dev false-fire ≤ floor's, tie → lower under-triage; fallback = lowest false-fire"})

    # paired differences vs Jev on the policy row
    jev = next((n for n in per_judge if n.startswith("typesafe:")), None)
    diffs = []
    if jev:
        for name, pj in per_judge.items():
            if name == jev:
                continue
            for metric in ("under", "exact"):
                d = S.paired_diff_ci(units, pj["policy"]["_fns"][metric], per_judge[jev]["policy"]["_fns"][metric],
                                     cluster=lambda u: u["cluster"], iters=ITERS)
                diffs.append([f"{name} − Jev", metric, S.fmt_ci(*d), "yes" if d[1] is not None and (d[1] > 0 or d[2] < 0) else "no"])

    # calibration: P(any risk) vs intended != none, single-turn items only.
    # Coverage gate (amendment B1): a judge is scored only if it answered nearly
    # every single-turn item. The old gate counted error rows toward a minimum of
    # 100 attempts, so a run that errored on 95% of its calls was still scored on
    # whichever rows happened to land.
    singles = [u for u in units if u["form"] == "single"]
    cal_rows, rel = [], {}
    for k, rows in judges.items():
        pr, tr = [], []
        for u in singles:
            r = rows.get(u["id"])
            if r and r["status"] == "ok":
                pr.append(1 - r["answers"]["severity"]["p"][0]); tr.append(u["intended"] is not None)
        if len(pr) < COVERAGE * len(singles):
            cal_rows.append([_name(k), k[2], f"{len(pr)}/{len(singles)}", "not scored (coverage)", ""])
            continue
        cal_rows.append([_name(k), k[2], len(pr), f"{S.brier(pr, tr):.3f}", f"{S.ece(pr, tr):.3f}"])
        rel[_name(k)] = {"elicitation": k[2], "ece": S.ece(pr, tr), "bins": S.reliability_bins(pr, tr)}

    # stratified (by family, contested) on the policy row, under-triage only
    strat = []
    for name, pj in per_judge.items():
        for fam in ("anthropic", "openai"):
            us = [u for u in units if u["family"] == fam]
            strat.append([name, f"generated by {fam}", len(us), S.fmt_ci(*S.bootstrap_ci(us, pj["policy"]["_fns"]["under"], cluster=lambda u: u["cluster"], iters=500))])
        us = [u for u in units if not u["contested"]]
        strat.append([name, "uncontested only", len(us), S.fmt_ci(*S.bootstrap_ci(us, pj["policy"]["_fns"]["under"], cluster=lambda u: u["cluster"], iters=500))])

    # cost / latency / parse failures
    ops = []
    for k, rows in covered.items():
        rs = [rows[i] for i in ids if i in rows]
        lat = [r["latency_ms"] for r in rs if r["status"] != "error" and not r.get("extra", {}).get("batch")]
        p50 = f"{S.percentile(lat, .5):.0f}" if lat else "batch only"
        p95 = f"{S.percentile(lat, .95):.0f}" if lat else ""
        ops.append([_name(k), len(rs), sum(r["status"] == "parse_failed" for r in rs), sum(r["status"] == "error" for r in rs),
                    sum("re_asked" in r["flags"] for r in rs), sum(any("unwrapped_answer" in f for f in r["flags"]) for r in rs), p50, p95,
                    f"${sum(r['cost_usd'] for r in rs) / len(rs) * 1000:.3f}", rs[0]["sampling"], rs[0]["reasoning"]])

    # Split the headline by conversational form. A judge can top the pooled table on
    # the strength of single messages alone while sitting near the bottom on the
    # multi-turn arcs the products actually process, and the pooled row hides it.
    by_form = []
    for name, pj in per_judge.items():
        row = [name]
        for form in ("single", "arc"):
            us = [u for u in units if u["form"] == form]
            got = pj["alone"]["_got"]
            ex = S.rate([got[u["id"]] == u["intended"] for u in us])
            un = S.rate([P.SEV[got[u["id"]]] < P.SEV[u["intended"]] for u in us])
            row += [f"{ex:.3f}" if ex is not None else "n/a", f"{un:.3f}" if un is not None else "n/a"]
        by_form.append(row)

    n_single, n_arc = sum(u["form"] == "single" for u in units), sum(u["form"] == "arc" for u in units)
    L = [f"## Crisis severity, {split} split: {n_single} single messages + {n_arc} arcs ({len(items)} turns), "
         f"{sum(u['contested'] for u in units)} contested\n",
         "Under-triage = final level below the cell's intended level (arcs: highest level reached). "
         "False fire = any level on an intended-none item. 95% CIs: bootstrap, clustered by arc.\n",
         report.table(["Configuration", "Under-triage", "Exact level", "False fire (none items)", "Over-triage"],
                      [[n, S.fmt_ci(*m["under"]), S.fmt_ci(*m["exact"]), S.fmt_ci(*m["false_fire"]), S.fmt_ci(*m["over"])] for n, m in rows_out])]
    if diffs:
        L += ["\n### Paired differences vs lexicon ∪ Jev (same resampled arcs)\n", report.table(["Comparison", "Metric", "Difference [95% CI]", "CI excludes 0"], diffs)]
    L += [f"\n### Argmax accuracy by conversational form ({n_single} single messages, {n_arc} arcs)\n",
          "The pooled row is dominated by single messages. Read both columns before calling any judge best.\n",
          report.table(["Judge", "Exact, singles", "Under-triage, singles", "Exact, arcs", "Under-triage, arcs"], by_form),
          "\n### Calibration, P(any risk) vs intended, single messages (compare within an elicitation only)\n",
          report.table(["Judge", "Elicitation", "n", "Brier", "ECE"], cal_rows),
          "\n### Under-triage by generator family and contested flag (policy row)\n",
          report.table(["Judge", "Slice", "n", "Under-triage"], strat),
          "\n### Operations\n",
          report.table(["Judge", "Calls", "Parse failed", "Errors", "Re-asked", "Unwrapped (A6)", "p50 ms", "p95 ms", "USD/1k", "Sampling", "Reasoning"], ops)]
    if skipped:
        L.append(f"\nNot scored (coverage < {COVERAGE:.0%}): {', '.join(_name(k) for k in skipped)}")
    raw = {"split": split, "rows": {n: {k: v for k, v in m.items() if not k.startswith('_')} for n, m in rows_out},
           "diffs": diffs, "calibration": rel, "strata": strat, "ops": ops, "chosen": chosen, "by_form": by_form}
    return "\n".join(L), raw


# ── trainee ──────────────────────────────────────────────────────────────────

def trainee_p(rows: dict[str, dict], it: Item) -> float | None:
    r = rows.get(it.id)
    if not r or r["status"] != "ok":
        return None
    h = it.intended["harm"]
    return r["answers"]["question_style"]["probabilities"]["leading"] if h == "leading" else r["answers"][h]["noul"]


def trainee_metrics(items: list[Item], flag_of) -> dict[str, Any]:
    got = {i.id: flag_of(i) for i in items}
    pairs = lambda its: [(i.intended["present"], got[i.id]) for i in its]
    f1 = lambda its: S.f1_binary(pairs(its))
    ff = lambda its: S.rate([got[i.id] for i in its if not i.intended["present"]])
    ff_near = lambda its: S.rate([got[i.id] for i in its if i.cell["truth"] == "near_miss"])
    recall = lambda its: S.rate([got[i.id] for i in its if i.intended["present"]])
    return {"f1": S.bootstrap_ci(items, f1, iters=ITERS), "recall": S.bootstrap_ci(items, recall, iters=ITERS),
            "false_flag": S.bootstrap_ci(items, ff, iters=ITERS), "false_flag_near_miss": S.bootstrap_ci(items, ff_near, iters=ITERS),
            "_fns": {"f1": f1, "false_flag": ff, "recall": recall}, "_got": got}


def run_trainee(split: str, do_freeze: bool) -> tuple[str, dict]:
    items = [i for i in read("trainee") if i.split == split]
    verify.apply("trainee", items)
    ids = {i.id for i in items}
    judges = _judges("trainee_synth", ids)
    covered = {k: rows for k, rows in judges.items() if len([i for i in ids if i in rows and rows[i]["status"] != "error"]) >= COVERAGE * len(ids)}
    skipped = [k for k in judges if k not in covered]
    floor_flag = lambda i: TQ.floor(i.intended["harm"], i.text, qc_step=False)
    floor_m = trainee_metrics(items, floor_flag)
    frozen = load_frozen().get("trainee", {}).get("judges", {})
    chosen: dict[str, Any] = {}
    rows_out = [("regex floor", floor_m)]
    per_judge = {}
    for k, rows in covered.items():
        name = _name(k)
        alone = trainee_metrics(items, lambda i, rows=rows: (trainee_p(rows, i) or 0.0) >= 0.5)
        rows_out.append((f"{name} alone (p ≥ 0.5)", alone))
        if do_freeze and name in frozen:
            tau = frozen[name]["tau"]
        elif do_freeze:
            cands = []
            for tau in TRAINEE_TAUS:
                m = trainee_metrics(items, lambda i, rows=rows, tau=tau: floor_flag(i) or (trainee_p(rows, i) or 0.0) >= tau)
                cands.append((tau, m["false_flag"][0] or 0.0, -(m["f1"][0] or 0.0)))
            ok = [c for c in cands if c[1] <= (floor_m["false_flag"][0] or 0.0)]
            pick = min(ok, key=lambda c: (c[0], c[2])) if ok else min(cands, key=lambda c: (c[1], c[2]))
            chosen[name] = {"tau": pick[0], "false_fire": pick[1], "criterion": -pick[2], "fallback": not ok}
            tau = pick[0]
        else:
            if name not in frozen:
                rows_out.append((f"{name} (no frozen τ; run --split dev --freeze first)", alone))
                continue
            tau = frozen[name]["tau"]
        m = trainee_metrics(items, lambda i, rows=rows, tau=tau: floor_flag(i) or (trainee_p(rows, i) or 0.0) >= tau)
        rows_out.append((f"regex ∪ {name} τ={tau}", m))
        per_judge[name] = {"rows": rows, "tau": tau, "policy": m}
    if do_freeze:
        freeze("trainee", {"judges": chosen, "floor_false_fire": floor_m["false_flag"][0] or 0.0,
                           "rule": "lowest τ with dev false-flag ≤ floor's, tie → higher F1; fallback = lowest false-flag"})

    jev = next((n for n in per_judge if n.startswith("typesafe:")), None)
    diffs = []
    if jev:
        for name, pj in per_judge.items():
            if name != jev:
                for metric in ("f1", "false_flag"):
                    d = S.paired_diff_ci(items, pj["policy"]["_fns"][metric], per_judge[jev]["policy"]["_fns"][metric], iters=ITERS)
                    diffs.append([f"{name} − Jev", metric, S.fmt_ci(*d), "yes" if d[1] is not None and (d[1] > 0 or d[2] < 0) else "no"])

    # per-harm F1 on the policy row
    harms = sorted({i.intended["harm"] for i in items})
    per_harm = []
    for h in harms:
        its = [i for i in items if i.intended["harm"] == h]
        row = [h, len(its), f"{S.f1_binary([(i.intended['present'], floor_m['_got'][i.id]) for i in its]) or 0:.2f}"]
        for name, pj in per_judge.items():
            row.append(f"{S.f1_binary([(i.intended['present'], pj['policy']['_got'][i.id]) for i in its]) or 0:.2f}")
        per_harm.append(row)

    # Coverage gate (amendment B1); see the note on the crisis calibration table.
    cal_rows, rel = [], {}
    for k, rows in judges.items():
        pr = [(trainee_p(rows, i), i.intended["present"]) for i in items if trainee_p(rows, i) is not None]
        if len(pr) < COVERAGE * len(items):
            cal_rows.append([_name(k), k[2], f"{len(pr)}/{len(items)}", "not scored (coverage)", ""])
            continue
        p, t = zip(*pr)
        cal_rows.append([_name(k), k[2], len(p), f"{S.brier(p, t):.3f}", f"{S.ece(p, t):.3f}"])
        rel[_name(k)] = {"elicitation": k[2], "ece": S.ece(p, t), "bins": S.reliability_bins(p, t)}
    strat = []
    for name, pj in per_judge.items():
        for fam in ("anthropic", "openai"):
            us = [i for i in items if i.generator["family"] == fam]
            strat.append([name, f"generated by {fam}", len(us), S.fmt_ci(*S.bootstrap_ci(us, pj["policy"]["_fns"]["f1"], iters=500))])
        us = [i for i in items if not i.contested]
        strat.append([name, "uncontested only", len(us), S.fmt_ci(*S.bootstrap_ci(us, pj["policy"]["_fns"]["f1"], iters=500))])
    ops = []
    for k, rows in covered.items():
        rs = [rows[i] for i in ids if i in rows]
        lat = [r["latency_ms"] for r in rs if r["status"] != "error" and not r.get("extra", {}).get("batch")]
        p50 = f"{S.percentile(lat, .5):.0f}" if lat else "batch only"
        p95 = f"{S.percentile(lat, .95):.0f}" if lat else ""
        ops.append([_name(k), len(rs), sum(r["status"] == "parse_failed" for r in rs), sum(r["status"] == "error" for r in rs),
                    sum("re_asked" in r["flags"] for r in rs), sum(any("unwrapped_answer" in f for f in r["flags"]) for r in rs), p50, p95,
                    f"${sum(r['cost_usd'] for r in rs) / len(rs) * 1000:.3f}", rs[0]["sampling"], rs[0]["reasoning"]])

    L = [f"## Trainee conduct, {split} split: {len(items)} replies ({sum(i.intended['present'] for i in items)} positives, "
         f"{sum(i.cell['truth'] == 'near_miss' for i in items)} near-miss negatives, {sum(i.cell['truth'] == 'clean' for i in items)} clean), "
         f"{sum(i.contested for i in items)} contested\n",
         "F1 over all replies for their cell's harm; false flag = flagged on a negative. 95% CIs: bootstrap over replies.\n",
         report.table(["Configuration", "F1", "Recall", "False flag (all negatives)", "False flag (near-miss)"],
                      [[n, S.fmt_ci(*m["f1"]), S.fmt_ci(*m["recall"]), S.fmt_ci(*m["false_flag"]), S.fmt_ci(*m["false_flag_near_miss"])] for n, m in rows_out])]
    if diffs:
        L += ["\n### Paired differences vs regex ∪ Jev\n", report.table(["Comparison", "Metric", "Difference [95% CI]", "CI excludes 0"], diffs)]
    L += ["\n### Per-harm F1 (policy rows)\n", report.table(["Harm", "n", "regex"] + list(per_judge), per_harm),
          "\n### Calibration, P(harm) vs intended (compare within an elicitation only)\n", report.table(["Judge", "Elicitation", "n", "Brier", "ECE"], cal_rows),
          "\n### F1 by generator family and contested flag (policy row)\n", report.table(["Judge", "Slice", "n", "F1"], strat),
          "\n### Operations\n", report.table(["Judge", "Calls", "Parse failed", "Errors", "Re-asked", "Unwrapped (A6)", "p50 ms", "p95 ms", "USD/1k", "Sampling", "Reasoning"], ops)]
    if skipped:
        L.append(f"\nNot scored (coverage < {COVERAGE:.0%}): {', '.join(_name(k) for k in skipped)}")
    raw = {"split": split, "rows": {n: {k: v for k, v in m.items() if not k.startswith('_')} for n, m in rows_out},
           "diffs": diffs, "per_harm": per_harm, "calibration": rel, "strata": strat, "ops": ops, "chosen": chosen}
    return "\n".join(L), raw


# ── omission ─────────────────────────────────────────────────────────────────

def omission_fire(rows: dict[str, dict], turns: list[Item], grace: int) -> int | None:
    from jevlab.floors import heuristics
    h = heuristics()
    disclosed_at = None
    for n, t in enumerate(turns, start=1):
        r = rows.get(t.id)
        if not r or r["status"] != "ok":
            return None
        a = r["answers"]
        if disclosed_at is None and (h.detect_risk(t.youth or "") or a["disclosed"]["noul"] >= DISCLOSED_TAU):
            disclosed_at = n
        if a["asked_directly"]["noul"] >= ASK_TAU:
            return None
        if disclosed_at is not None and n - disclosed_at + 1 >= grace:
            return n
    return None


def run_omission(split: str, do_freeze: bool) -> tuple[str, dict]:
    items = [i for i in read("omission") if i.split == split]
    verify.apply("omission", items)
    arcs: dict[str, list[Item]] = defaultdict(list)
    for it in items:
        arcs[it.arc_id].append(it)
    for ts in arcs.values():
        ts.sort(key=lambda t: t.turn)
    ids = {i.id for i in items}
    judges = _judges("omission_synth", ids)
    covered = {k: rows for k, rows in judges.items() if len([i for i in ids if i in rows and rows[i]["status"] != "error"]) >= COVERAGE * len(ids)}
    skipped = [k for k in judges if k not in covered]
    frozen = load_frozen().get("omission", {}).get("judges", {})
    chosen, out_rows, per_judge = {}, [], {}
    units = list(arcs.values())
    for k, rows in covered.items():
        name = _name(k)
        res = {}
        for g in GRACES:
            acc = lambda us, rows=rows, g=g: S.rate([(omission_fire(rows, ts, g) is not None) == ts[0].intended["omission"] for ts in us])
            fp = lambda us, rows=rows, g=g: S.rate([omission_fire(rows, ts, g) is not None for ts in us if not ts[0].intended["omission"]])
            res[g] = {"acc": S.bootstrap_ci(units, acc, iters=ITERS), "fp": S.bootstrap_ci(units, fp, iters=ITERS), "_acc": acc}
        if do_freeze and name in frozen:
            g = frozen[name]["tau"]
        elif do_freeze:
            best = max(GRACES, key=lambda g: (res[g]["acc"][0] or 0, -g))
            chosen[name] = {"tau": best, "false_fire": res[best]["fp"][0] or 0.0, "criterion": res[best]["acc"][0] or 0.0, "fallback": False}
            g = best
        else:
            if name not in frozen:
                out_rows.append([f"{name} (no frozen grace)", len(units), "not scored", ""])
                continue
            g = frozen[name]["tau"]
        out_rows.append([f"{name}, grace {g}", len(units), S.fmt_ci(*res[g]["acc"]), S.fmt_ci(*res[g]["fp"])])
        per_judge[name] = res[g]
    if do_freeze:
        freeze("omission", {"judges": chosen, "floor_false_fire": 0.0, "rule": "grace with highest dev accuracy, tie → smaller"})
    jev = next((n for n in per_judge if n.startswith("typesafe:")), None)
    diffs = []
    if jev:
        for name, pj in per_judge.items():
            if name != jev:
                d = S.paired_diff_ci(units, pj["_acc"], per_judge[jev]["_acc"], iters=ITERS)
                diffs.append([f"{name} − Jev", "accuracy", S.fmt_ci(*d), "yes" if d[1] is not None and (d[1] > 0 or d[2] < 0) else "no"])
    by_cell = []
    for asks in ("never", "immediately", "after_validating"):
        us = [ts for ts in units if ts[0].intended["asks"] == asks]
        by_cell.append([asks, len(us)] + [f"{pj['_acc'](us) or 0:.2f}" for pj in per_judge.values()])
    L = [f"## Omission (never asked directly), {split} split: {len(units)} arcs, {sum(any(t.contested for t in ts) for ts in units)} contested\n",
         f"Fires when a disclosure has happened (regex or P(disclosed) ≥ {DISCLOSED_TAU}) and `grace` trainee turns pass with P(asked directly) < {ASK_TAU}. "
         "Accuracy = fired iff the arc's cell says the trainee never asks. The regex floor has no omission detector.\n",
         report.table(["Judge", "Arcs", "Accuracy", "False fire (asks arcs)"], out_rows)]
    if diffs:
        L += ["\n### Paired differences vs Jev\n", report.table(["Comparison", "Metric", "Difference [95% CI]", "CI excludes 0"], diffs)]
    L += ["\n### Accuracy by arc type\n", report.table(["Arc type", "n"] + list(per_judge), by_cell)]
    if skipped:
        L.append(f"\nNot scored (coverage < {COVERAGE:.0%}): {', '.join(_name(k) for k in skipped)}")
    raw = {"split": split, "rows": out_rows, "diffs": diffs, "by_cell": by_cell, "chosen": chosen,
           "skipped": [_name(k) for k in skipped]}
    return "\n".join(L), raw


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("use_case", choices=["crisis", "trainee", "omission"])
    ap.add_argument("--split", default="test", choices=["dev", "test"])
    ap.add_argument("--freeze", action="store_true", help="choose thresholds on this split and write docs/THRESHOLDS.md (dev only)")
    a = ap.parse_args()
    if a.freeze and a.split != "dev":
        raise SystemExit("thresholds are chosen on the dev split only")
    body, raw = {"crisis": run_crisis, "trainee": run_trainee, "omission": run_omission}[a.use_case](a.split, a.freeze)
    print(body)
    path = report.write(f"compare-{a.use_case}-{a.split}", f"Multi-judge comparison: {a.use_case} ({a.split})", body, raw)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
