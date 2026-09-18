import random

from jevlab import stats as S


def test_bootstrap_ci_brackets_point_and_is_deterministic():
    units = [(i, i % 3 == 0) for i in range(200)]
    stat = lambda u: S.rate([f for _, f in u])
    p, lo, hi = S.bootstrap_ci(units, stat, seed=1)
    p2, lo2, hi2 = S.bootstrap_ci(units, stat, seed=1)
    assert (p, lo, hi) == (p2, lo2, hi2) and lo <= p <= hi and hi - lo < 0.2


def test_cluster_bootstrap_is_wider_when_clusters_are_homogeneous():
    # 20 clusters of 10 identical outcomes: item-level CI is far too narrow
    units = [(c, c % 2 == 0) for c in range(20) for _ in range(10)]
    stat = lambda u: S.rate([f for _, f in u])
    _, lo_i, hi_i = S.bootstrap_ci(units, stat, seed=0)
    _, lo_c, hi_c = S.bootstrap_ci(units, stat, cluster=lambda u: u[0], seed=0)
    assert (hi_c - lo_c) > (hi_i - lo_i)


def test_paired_diff_excludes_zero_for_a_real_difference():
    rnd = random.Random(0)
    units = [(rnd.random() < 0.8, rnd.random() < 0.5) for _ in range(300)]
    d, lo, hi = S.paired_diff_ci(units, lambda u: S.rate([a for a, _ in u]), lambda u: S.rate([b for _, b in u]))
    assert lo > 0 and abs(d - 0.3) < 0.1


def test_macro_f1_and_kappa():
    pairs = [("a", "a"), ("b", "b"), ("a", "b"), ("c", "c")]
    assert abs(S.macro_f1(pairs) - (2 / 3 + 2 / 3 + 1) / 3) < 1e-9
    perfect = [(x, x) for x in "aabbcc"]
    assert S.kappa_nominal(perfect) == 1.0 and S.ac1_nominal(perfect) == 1.0
    assert S.f1_binary([(True, True), (True, False), (False, True)]) == 0.5


def test_ac1_nominal_matches_binary_on_two_categories():
    pairs = [(True, True)] * 118 + [(True, False)] * 5 + [(False, True)] * 2
    assert abs(S.ac1_nominal(pairs) - S.ac1_binary(pairs)) < 1e-9


def test_calibration_helpers():
    probs = [0.9, 0.8, 0.1, 0.2]
    truths = [True, True, False, False]
    assert S.brier(probs, truths) < 0.05
    bins = S.reliability_bins(probs, truths, 10)
    assert sum(b["count"] for b in bins) == 4
    assert S.ece(probs, truths) < 0.2
    assert S.multiclass_brier([[0.9, 0.1], [0.2, 0.8]], [0, 1]) < 0.1
    assert S.top_label_ece([[0.9, 0.1], [0.2, 0.8]], [0, 1]) < 0.2


def test_fmt_ci():
    assert S.fmt_ci(0.5, 0.4, 0.6) == "0.500 [0.400, 0.600]"
    assert S.fmt_ci(None, None, None) == "n/a"


def _fleiss(units, cats):
    """Reference implementation, valid only on a complete matrix."""
    from collections import Counter
    n_units, n_rat = len(units), len(units[0])
    p_i = [(sum(Counter(u)[c] ** 2 for c in cats) - n_rat) / (n_rat * (n_rat - 1)) for u in units]
    p_j = [sum(Counter(u)[c] for u in units) / (n_units * n_rat) for c in cats]
    pbar, pe = sum(p_i) / n_units, sum(p * p for p in p_j)
    return (pbar - pe) / (1 - pe)


def test_krippendorff_alpha_converges_to_fleiss_on_a_complete_matrix():
    """Alpha carries a finite-sample correction Fleiss omits, so the two are close
    but not equal, and the gap must shrink as units are added. Asserting equality
    would be asserting a fact that is false."""
    cats = ["a", "b", "c"]
    diffs = []
    for n_units in (50, 2000):
        rnd = random.Random(7)
        units = [[rnd.choice(cats) if rnd.random() < 0.3 else cats[i % 3] for _ in range(10)] for i in range(n_units)]
        diffs.append(abs(S.krippendorff_alpha_nominal(units) - _fleiss(units, cats)))
    assert diffs[0] < 5e-3 and diffs[1] < diffs[0] / 10


def test_krippendorff_alpha_edges():
    assert S.krippendorff_alpha_nominal([["a", "a"], ["b", "b"], ["a", "a"], ["b", "b"]]) == 1.0
    # units with a single rater carry no agreement information and are skipped
    assert S.krippendorff_alpha_nominal([["a"], ["b"]]) is None
    mixed = [["a", "a"], ["b", "b"], ["a"], ["b"], ["a"]]
    assert S.krippendorff_alpha_nominal(mixed) == S.krippendorff_alpha_nominal([["a", "a"], ["b", "b"]])
