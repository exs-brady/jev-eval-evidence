"""Statistics for the reports: clustered bootstrap CIs, paired differences,
agreement coefficients, calibration bins. Pure functions over plain lists so
every number in a report can be recomputed from the JSON next to it."""
from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from typing import Any, Callable, Hashable, Sequence

from .vendor.who_agreement import ac1_binary, kappa_binary, qwk  # noqa: F401  (re-exported)

Stat = Callable[[Sequence[Any]], float | None]


def _clusters(units: Sequence[Any], cluster: Callable[[Any], Hashable] | None) -> list[list[Any]]:
    if cluster is None:
        return [[u] for u in units]
    groups: dict[Hashable, list[Any]] = defaultdict(list)
    for u in units:
        groups[cluster(u)].append(u)
    return list(groups.values())


def bootstrap_ci(units: Sequence[Any], stat: Stat, *, cluster: Callable[[Any], Hashable] | None = None,
                 iters: int = 2000, seed: int = 0, alpha: float = 0.05) -> tuple[float | None, float | None, float | None]:
    """(point, lo, hi): percentile CI resampling clusters with replacement."""
    groups = _clusters(units, cluster)
    point = stat(units)
    if not groups or point is None:
        return point, None, None
    rnd = random.Random(seed)
    vals = []
    for _ in range(iters):
        sample = [u for g in (groups[rnd.randrange(len(groups))] for _ in groups) for u in g]
        v = stat(sample)
        if v is not None and v == v:
            vals.append(v)
    if len(vals) < iters // 4:
        return point, None, None
    vals.sort()
    return point, vals[int(alpha / 2 * len(vals))], vals[min(len(vals) - 1, int((1 - alpha / 2) * len(vals)))]


def paired_diff_ci(units: Sequence[Any], stat_a: Stat, stat_b: Stat, *, cluster=None, iters: int = 2000,
                   seed: int = 0) -> tuple[float | None, float | None, float | None]:
    """CI of stat_a - stat_b over the SAME resampled clusters (paired)."""
    groups = _clusters(units, cluster)
    a, b = stat_a(units), stat_b(units)
    if a is None or b is None:
        return None, None, None
    rnd = random.Random(seed)
    vals = []
    for _ in range(iters):
        sample = [u for g in (groups[rnd.randrange(len(groups))] for _ in groups) for u in g]
        x, y = stat_a(sample), stat_b(sample)
        if x is not None and y is not None:
            vals.append(x - y)
    if len(vals) < iters // 4:
        return a - b, None, None
    vals.sort()
    return a - b, vals[int(0.025 * len(vals))], vals[min(len(vals) - 1, int(0.975 * len(vals)))]


def rate(flags: Sequence[bool]) -> float | None:
    return sum(flags) / len(flags) if flags else None


def macro_f1(pairs: Sequence[tuple[Any, Any]], labels: Sequence[Any] | None = None) -> float | None:
    """pairs of (gold, pred)."""
    if not pairs:
        return None
    labels = list(labels) if labels is not None else sorted({g for g, _ in pairs} | {p for _, p in pairs}, key=str)
    f1s = []
    for lab in labels:
        tp = sum(g == lab and p == lab for g, p in pairs)
        fp = sum(g != lab and p == lab for g, p in pairs)
        fn = sum(g == lab and p != lab for g, p in pairs)
        if tp + fp + fn == 0:
            continue
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1s.append(2 * prec * rec / (prec + rec) if prec + rec else 0.0)
    return sum(f1s) / len(f1s) if f1s else None


def f1_binary(pairs: Sequence[tuple[bool, bool]]) -> float | None:
    tp = sum(g and p for g, p in pairs)
    fp = sum((not g) and p for g, p in pairs)
    fn = sum(g and not p for g, p in pairs)
    if tp + fp + fn == 0:
        return None
    return 2 * tp / (2 * tp + fp + fn)


def kappa_nominal(pairs: Sequence[tuple[Any, Any]]) -> float | None:
    n = len(pairs)
    if not n:
        return None
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else None


def ac1_nominal(pairs: Sequence[tuple[Any, Any]]) -> float | None:
    """Gwet's AC1 for q nominal categories: pe = 1/(q-1) * sum_k pi_k (1 - pi_k)."""
    n = len(pairs)
    if not n:
        return None
    cats = sorted({a for a, _ in pairs} | {b for _, b in pairs}, key=str)
    q = len(cats)
    if q < 2:
        return 1.0 if all(a == b for a, b in pairs) else None
    po = sum(a == b for a, b in pairs) / n
    pi = {k: (sum(a == k for a, _ in pairs) + sum(b == k for _, b in pairs)) / (2 * n) for k in cats}
    pe = sum(p * (1 - p) for p in pi.values()) / (q - 1)
    return (po - pe) / (1 - pe) if pe < 1 else None


def krippendorff_alpha_nominal(units: Sequence[Sequence[Any]]) -> float | None:
    """Panel reliability over many raters, nominal categories.

    `units` is one list of labels per unit; units may carry different numbers of
    raters and units with fewer than two are skipped, which is why this and not
    Fleiss' kappa: a corpus coded once for most items and ten times for a few
    would otherwise have to discard almost all of itself to get a square matrix.

    This answers a different question from the per-rater agreement tables. Those
    ask how close one rater is to a consensus; this asks whether the coding
    scheme is dependable at all. On a complete matrix it coincides with Fleiss.
    """
    o: dict[tuple[Any, Any], float] = defaultdict(float)
    for vals in units:
        m = len(vals)
        if m < 2:
            continue
        c = Counter(vals)
        for a in c:
            for b in c:
                o[(a, b)] += (c[a] * (c[a] - 1) if a == b else c[a] * c[b]) / (m - 1)
    cats = sorted({a for a, _ in o}, key=str)
    if len(cats) < 2:
        return None
    n_c = {x: sum(o[(x, k)] for k in cats) for x in cats}
    n = sum(n_c.values())
    if n < 2:
        return None
    do = sum(o[(a, b)] for a in cats for b in cats if a != b) / n
    de = sum(n_c[a] * n_c[b] for a in cats for b in cats if a != b) / (n * (n - 1))
    return 1 - do / de if de else None


def brier(probs: Sequence[float], truths: Sequence[bool]) -> float | None:
    if not probs:
        return None
    return sum((p - float(t)) ** 2 for p, t in zip(probs, truths, strict=True)) / len(probs)


def reliability_bins(probs: Sequence[float], truths: Sequence[bool], bins: int = 10) -> list[dict]:
    out = []
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        idx = [i for i, p in enumerate(probs) if lo <= p < hi or (b == bins - 1 and p == 1.0)]
        out.append({"lo": lo, "hi": hi, "count": len(idx),
                    "confidence": sum(probs[i] for i in idx) / len(idx) if idx else None,
                    "accuracy": sum(truths[i] for i in idx) / len(idx) if idx else None})
    return out


def ece(probs: Sequence[float], truths: Sequence[bool], bins: int = 10) -> float | None:
    n = len(probs)
    if not n:
        return None
    return sum(b["count"] / n * abs(b["confidence"] - b["accuracy"]) for b in reliability_bins(probs, truths, bins) if b["count"])


def multiclass_brier(prob_rows: Sequence[Sequence[float]], gold_idx: Sequence[int]) -> float | None:
    if not prob_rows:
        return None
    tot = 0.0
    for ps, g in zip(prob_rows, gold_idx, strict=True):
        tot += sum((p - (1.0 if i == g else 0.0)) ** 2 for i, p in enumerate(ps))
    return tot / len(prob_rows)


def top_label_ece(prob_rows: Sequence[Sequence[float]], gold_idx: Sequence[int], bins: int = 10) -> float | None:
    conf = [max(ps) for ps in prob_rows]
    hit = [max(range(len(ps)), key=ps.__getitem__) == g for ps, g in zip(prob_rows, gold_idx, strict=True)]
    return ece(conf, hit, bins)


def fmt_ci(point: float | None, lo: float | None, hi: float | None, digits: int = 3) -> str:
    if point is None:
        return "n/a"
    if lo is None:
        return f"{point:.{digits}f}"
    return f"{point:.{digits}f} [{lo:.{digits}f}, {hi:.{digits}f}]"


def percentile(values: Sequence[float], q: float) -> float | None:
    if not values:
        return None
    s = sorted(values)
    k = (len(s) - 1) * q
    f, c = math.floor(k), math.ceil(k)
    return s[f] if f == c else s[f] + (s[c] - s[f]) * (k - f)
