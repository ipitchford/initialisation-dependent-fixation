#!/usr/bin/env python3
"""Evidence for Theorem 6, Corollary 7 and the rate-cap table (Section 5.4).

Run (from the directory containing this file or anywhere):
    python3 stationary_identity_and_caps.py

Part 1 uses only the standard library and EXACT RATIONAL ARITHMETIC. It
certifies, for several finite favourable-type laws, that the equilibrium-start
single-founder limit 1 - sum_i G_A(i) a_i/(a_i + lam c*) equals
1 - E[T_B]/E[T_A] = 1 - 1/(lam m_A), and that it strictly exceeds the
Conjecture 2 value 1 - pi. The fixed point c* is enclosed by rational
bisection; monotonicity of every expression in c turns the bracket into a
certified enclosure.

Part 2 (NumPy/SciPy) solves the exact finite-population count chain with two
favourable and two resident rates. N = 2..5 use exact fractions; larger N use
floating sparse solves with recorded residuals. It also integrates the backward
equations for the fresh-resident limits. These are FLOATING approximations.

Part 3 (NumPy/SciPy) evaluates the stationary error under finite rate caps.
These are FLOATING approximations of exactly defined quantities.
"""
from __future__ import annotations

from fractions import Fraction as Fr
from math import comb, isqrt
from pathlib import Path
import json
import platform
import sys

OUT = Path(__file__).resolve().parent


# ---------------------------------------------------------------- Part 1
def fixed_point_bracket(fa, lam, width=Fr(1, 10**40)):
    """Rational bracket for the unique c in (0,1] with sum w lam/(a+lam c) = 1."""
    def g(c):
        return sum(w * lam / (a + lam * c) for a, w in fa) - 1
    lo, hi = Fr(0), Fr(1)
    assert g(lo) > 0 and g(hi) < 0, "betterness or separation fails"
    while hi - lo > width:
        mid = (lo + hi) / 2
        if g(mid) > 0:
            lo = mid
        else:
            hi = mid
    return lo, hi


def certify_identity(fa, fb):
    """fa, fb: lists of (rate, probability) with Fractions."""
    assert sum(w for _, w in fa) == 1 and sum(w for _, w in fb) == 1
    assert max(a for a, _ in fa) < min(r for r, _ in fb), "supports must be separated"
    lam = 1 / sum(w / r for r, w in fb)          # 1/E[T_B]
    m_a = sum(w / a for a, w in fa)              # E[T_A]
    c_lo, c_hi = fixed_point_bracket(fa, lam)
    mass = sum(w / a for a, w in fa)
    g_a = [(a, (w / a) / mass) for a, w in fa]   # size-biased (equilibrium) A law
    # Each a/(a+lam c) decreases in c, so 1 - average increases in c.
    def fixation(law, c):
        return 1 - sum(w * a / (a + lam * c) for a, w in law)
    conj = (fixation(fa, c_lo), fixation(fa, c_hi))
    stat = (fixation(g_a, c_lo), fixation(g_a, c_hi))
    exact = 1 - 1 / (lam * m_a)
    assert stat[0] <= exact <= stat[1], "identity bracket fails"
    assert conj[1] < stat[0], "strict inequality not certified"
    return {
        "favourable_law": [[str(a), str(w)] for a, w in fa],
        "resident_law": [[str(r), str(w)] for r, w in fb],
        "lambda": str(lam), "E_TA": str(m_a), "E_TB": str(1 / lam),
        "c_star_bracket": [dec(c_lo), dec(c_hi)],
        "conjecture_value_bracket": [dec(conj[0]), dec(conj[1])],
        "equilibrium_start_value_bracket": [dec(stat[0]), dec(stat[1])],
        "equilibrium_start_exact": str(exact),
        "identity_certified": True,
        "strict_excess_over_conjecture_certified": True,
    }


def dec(x, digits=24):
    s = x.numerator * 10**digits // x.denominator
    sign = "-" if s < 0 else ""
    s = abs(s)
    return f"{sign}{s // 10**digits}.{s % 10**digits:0{digits}d}"


def sqrt37_bracket(scale=10**30):
    r = isqrt(37 * scale * scale)
    return Fr(r, scale), Fr(r + 1, scale)


def part1():
    h = Fr(1, 2)
    witness = certify_identity([(h, h), (Fr(1), h)], [(Fr(2), h), (Fr(6), h)])
    lo, hi = sqrt37_bracket()
    conj_lo, conj_hi = (3 + lo) / 12, (3 + hi) / 12
    c = witness["conjecture_value_bracket"]
    assert Fr(c[0]) - Fr(1, 10**20) < conj_hi and conj_lo < Fr(c[1]) + Fr(1, 10**20)
    assert witness["equilibrium_start_exact"] == "7/9"
    others = [
        certify_identity([(Fr(1, 4), Fr(1, 3)), (Fr(1, 2), Fr(1, 3)), (Fr(3, 2), Fr(1, 3))],
                         [(Fr(2), Fr(1, 5)), (Fr(5), Fr(2, 5)), (Fr(9), Fr(2, 5))]),
        certify_identity([(Fr(1, 10), Fr(9, 10)), (Fr(9, 10), Fr(1, 10))],
                         [(Fr(1), Fr(1))]),
        certify_identity([(Fr(3, 10), Fr(1, 2)), (Fr(7, 10), Fr(1, 4)), (Fr(1), Fr(1, 4))],
                         [(Fr(11, 10), Fr(1, 2)), (Fr(3), Fr(1, 2))]),
    ]
    return {"arithmetic": "exact fractions; rational bisection; monotone enclosure",
            "witness": witness,
            "witness_conjecture_closed_form": "(3+sqrt(37))/12",
            "additional_laws": others}


# ---------------------------------------------------------------- Part 2
A_RATES = (Fr(1, 2), Fr(1))
A_REDRAW = (Fr(1, 2), Fr(1, 2))
R_SLOW, R_FAST, P_SLOW = Fr(2), Fr(6), Fr(1, 2)
INITS = {  # name: (A founder law, resident slow probability)
    "fresh_A_fresh_B": ((Fr(1, 2), Fr(1, 2)), Fr(1, 2)),
    "fresh_A_equilibrium_B": ((Fr(1, 2), Fr(1, 2)), Fr(3, 4)),
    "equilibrium_A_equilibrium_B": ((Fr(2, 3), Fr(1, 3)), Fr(3, 4)),
    "equilibrium_A_fresh_B": ((Fr(2, 3), Fr(1, 3)), Fr(1, 2)),
}


def transitions(N, state, numeric=False):
    """Yield (new_state, rate) for the count chain (m1, m2, j)."""
    a_rates, w, r1, r2, p = A_RATES, A_REDRAW, R_SLOW, R_FAST, P_SLOW  # read at call time
    if numeric:
        a_rates, w = tuple(map(float, a_rates)), tuple(map(float, w))
        r1, r2, p = float(r1), float(r2), float(p)
    m1, m2, j = state
    M = m1 + m2
    n = N - M
    d = N - 1
    out = []
    for i in range(2):
        def add(st, di):
            s = list(st)
            s[i] += di
            return s
        # resident copies favourable vertex and becomes type i
        out.append(((*add((m1, m2), 1), j - 1), r1 * j * M * w[i] / d))
        out.append(((*add((m1, m2), 1), j), r2 * (n - j) * M * w[i] / d))
        mi = (m1, m2)[i]
        # type-i favourable vertex copies a resident
        out.append(((*add((m1, m2), -1), j + 1), a_rates[i] * mi * n * p / d))
        out.append(((*add((m1, m2), -1), j), a_rates[i] * mi * n * (1 - p) / d))
        # type-i favourable vertex copies a favourable vertex, redraws type i'
        other = 1 - i
        s = [m1, m2]
        s[i] -= 1
        s[other] += 1
        out.append(((s[0], s[1], j), a_rates[i] * mi * (M - 1) * w[other] / d))
    out.append(((m1, m2, j - 1), r1 * j * (n - 1) * (1 - p) / d))
    out.append(((m1, m2, j + 1), r2 * (n - j) * (n - 1) * p / d))
    return [(s, rate) for s, rate in out if rate != 0]


def transient_states(N):
    return [(m1, m2, j) for M in range(1, N) for m1 in range(M + 1)
            for m2 in (M - m1,) for j in range(N - M + 1)]


def initial_average(N, h, init):
    law, theta = init
    total = 0
    for i, wi in enumerate(law):
        start = [0, 0]
        start[i] = 1
        for j in range(N):
            pj = comb(N - 1, j) * theta**j * (1 - theta)**(N - 1 - j)
            total += wi * pj * h((start[0], start[1], j))
    return total


def solve_exact(N):
    states = transient_states(N)
    idx = {s: k for k, s in enumerate(states)}
    n = len(states)
    A = [[Fr(0)] * n for _ in range(n)]
    rhs = [Fr(0)] * n
    for s, k in idx.items():
        out = 0
        for t, rate in transitions(N, s):
            out += rate
            M = t[0] + t[1]
            if M == N:
                rhs[k] += rate
            elif M > 0:
                A[k][idx[t]] -= rate
        A[k][k] += out
    # Gauss-Jordan elimination in exact arithmetic
    for c in range(n):
        piv = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        rhs[c], rhs[piv] = rhs[piv], rhs[c]
        inv = 1 / A[c][c]
        A[c] = [x * inv for x in A[c]]
        rhs[c] *= inv
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
                rhs[r] -= f * rhs[c]
    sol = dict(zip(states, rhs))
    # exact residual check of the harmonic equations
    for s in states:
        acc = 0
        for t, rate in transitions(N, s):
            M = t[0] + t[1]
            ht = 1 if M == N else 0 if M == 0 else sol[t]
            acc += rate * (ht - sol[s])
        assert acc == 0
    return sol


def solve_float(N):
    import numpy as np
    import scipy.sparse as sp
    import scipy.sparse.linalg as spla
    states = transient_states(N)
    idx = {s: k for k, s in enumerate(states)}
    rows, cols, vals = [], [], []
    rhs = np.zeros(len(states))
    for s, k in idx.items():
        out = 0.0
        for t, rate in transitions(N, s, numeric=True):
            out += rate
            M = t[0] + t[1]
            if M == N:
                rhs[k] += rate
            elif M > 0:
                rows.append(k); cols.append(idx[t]); vals.append(-rate)
        rows.append(k); cols.append(k); vals.append(out)
    A = sp.csr_matrix((vals, (rows, cols)), shape=(len(states),) * 2)
    x = spla.spsolve(A.tocsc(), rhs)
    residual = float(np.max(np.abs(A @ x - rhs)) / max(1.0, float(np.max(np.abs(rhs)))))
    assert residual < 1e-9
    return {s: float(x[k]) for s, k in idx.items()}, residual, len(states)


def fresh_limits():
    """Backward equations (49) with b(t)=3+exp(-4t); floating approximations."""
    import math
    import numpy as np
    from scipy.integrate import solve_ivp
    a = np.array([0.5, 1.0])
    w = np.array([0.5, 0.5])
    rho = 1.0 / 2.0  # a_+/b_-

    def endpoint(T, z, b, method):
        rhs = lambda s, e: a * (e - 1) + b(s) * e * (1 - w @ e)
        sol = solve_ivp(rhs, (T, 0.0), np.full(2, z), method=method, rtol=2e-12, atol=2e-14)
        assert sol.success
        return sol.y[:, -1]

    out = {}
    for name, (law, theta) in INITS.items():
        law = np.array([float(x) for x in law])
        fresh = theta == Fr(1, 2)
        b = (lambda s: 3 + math.exp(-4 * s)) if fresh else (lambda s: 3.0)
        lo = 1 - law @ endpoint(12.0, rho, b, "DOP853")
        hi = 1 - law @ endpoint(12.0, 0.0, b, "DOP853")
        lo2 = 1 - law @ endpoint(12.0, rho, b, "Radau")
        assert abs(lo - lo2) < 1e-9 and -1e-10 <= hi - lo < 1e-8
        out[name] = {"T": 12.0, "lower_approx": float(lo), "upper_approx": float(hi)}
    return out


def part2():
    # Sanity: identical favourable rates reproduce the scalar exact values.
    global A_RATES
    saved = A_RATES
    A_RATES = (Fr(1), Fr(1))
    scalar = [initial_average(N, solve_exact(N).__getitem__, INITS["fresh_A_fresh_B"])
              for N in (2, 3, 4)]
    assert scalar == [Fr(16, 21), Fr(2864, 4051), Fr(443968, 639901)], scalar
    A_RATES = saved

    exact = {}
    for N in (2, 3, 4, 5):
        sol = solve_exact(N)
        exact[N] = {k: initial_average(N, sol.__getitem__, v) for k, v in INITS.items()}
    floats = {}
    for N in (10, 25, 50, 100):
        sol, res, size = solve_float(N)
        floats[N] = {k: float(initial_average(N, lambda s: sol[s],
                                              (tuple(float(x) for x in v[0]), float(v[1]))))
                     for k, v in INITS.items()}
        floats[N]["residual"] = res
        floats[N]["transient_states"] = size
    for N in (2, 3):  # float solver agrees with exact solver
        sol, _, _ = solve_float(N)
        for k, v in INITS.items():
            fv = initial_average(N, lambda s: sol[s], (tuple(float(x) for x in v[0]), float(v[1])))
            assert abs(fv - float(exact[N][k])) < 1e-12
    limits = fresh_limits()
    lo, hi = sqrt37_bracket()
    for key, exact_value in (("fresh_A_equilibrium_B", float((3 + lo) / 12)),
                             ("equilibrium_A_equilibrium_B", 7 / 9)):
        row = limits[key]
        assert row["lower_approx"] - 1e-10 <= exact_value <= row["upper_approx"] + 1e-10, (key, row)
    return {
        "model": "favourable rates 1/2,1 (redraw 1/2 each); resident rates 2,6 (redraw 1/2 each); one founder",
        "exact_small_N": {N: {k: [str(v), float(v)] for k, v in d.items()} for N, d in exact.items()},
        "floating_sparse": floats,
        "limits_floating_backward_ODE_T8": limits,
        "limits_exact": {"fresh_A_equilibrium_B": "(3+sqrt(37))/12",
                         "equilibrium_A_equilibrium_B": "7/9"},
        "scalar_reduction_check": "identical favourable rates reproduce 16/21, 2864/4051, 443968/639901",
    }


# ---------------------------------------------------------------- Part 3
def two_point_c(a, r, s, p, terms=400):
    import math
    kappa = (1 - p) * r + p * s
    lam = r * s / kappa
    C = p * (1 - p) * (s - r) ** 2 / kappa
    zeta, omega = C / kappa, (lam - a) / kappa
    term, total = 1.0, 1.0 / omega
    for j in range(1, terms):
        term *= zeta / j
        total += term / (omega + j)
        if term < 1e-18 * total:
            break
    return 1.0 / (1.0 + a / kappa * math.exp(-zeta) * total), lam


def general_c(a, rates, probs):
    """c_F for a finite law via the symmetrised generator (floating)."""
    import numpy as np
    from scipy.integrate import quad
    r = np.asarray(rates, float)
    f = np.asarray(probs, float)
    lam = 1.0 / float(f @ (1 / r))
    mu = lam * f / r
    L = np.diag(r) @ (np.outer(np.ones_like(r), f) - np.eye(len(r)))
    W = np.sqrt(mu)
    S = (W[:, None] * L) / W[None, :]
    S = (S + S.T) / 2
    vals, vecs = np.linalg.eigh(S)
    coef = (vecs.T @ (W * r)) ** 2 / lam
    keep = vals < -1e-10
    x, c = -vals[keep], coef[keep]
    D = lambda t: float(np.sum(c * (-np.expm1(-x * t)) / x))
    integral, _ = quad(lambda t: np.exp(-(lam - a) * t - D(t)), 0, np.inf, limit=400,
                       epsabs=1e-13, epsrel=1e-11)
    return 1.0 / (1.0 + a * integral), lam, float(np.sum(c / x))


def part3():
    import numpy as np
    from scipy.optimize import minimize_scalar
    a = 1.0
    # cross-check the two evaluators on the witness
    c1, _ = two_point_c(1.0, 2.0, 6.0, 0.5)
    c2, _, D2 = general_c(1.0, [2.0, 6.0], [0.5, 0.5])
    assert abs(c1 - 0.7020320539282127) < 1e-12 and abs(c2 - c1) < 1e-9 and abs(D2 - 0.25) < 1e-12
    rows = []
    for b0 in (1.25, 2.0):
        for ratio in (2.0, 3.0, 10.0, 100.0):
            bb = b0 * ratio
            gap = lambda p: two_point_c(a, b0, bb, p)[0] - (1 - a / two_point_c(a, b0, bb, p)[1])
            grid = np.linspace(0.001, 0.999, 999)
            p0 = grid[int(np.argmax([gap(p) for p in grid]))]
            res = minimize_scalar(lambda p: -gap(p), bounds=(max(1e-6, p0 - 0.002), min(1 - 1e-6, p0 + 0.002)),
                                  method="bounded", options={"xatol": 1e-12})
            two_gap, two_p = -res.fun, res.x
            nodes, weights = np.polynomial.legendre.leggauss(120)
            rr = b0 + (bb - b0) * (nodes + 1) / 2
            cu, lamu, _ = general_c(a, rr, weights / weights.sum())
            uni_gap = cu - (1 - a / lamu)
            def ceiling(lam):
                Dbar = (lam - b0) * (bb - lam) / (b0 * bb)
                g = lam - a
                return g / (g + a * np.exp(-Dbar)) - g / lam
            lg = np.linspace(b0, bb, 20001)
            cv = ceiling(lg)
            k = int(np.argmax(cv))
            res2 = minimize_scalar(lambda l: -ceiling(l), bounds=(lg[max(k - 1, 0)], lg[min(k + 1, len(lg) - 1)]),
                                   method="bounded", options={"xatol": 1e-12})
            assert two_gap <= -res2.fun + 1e-12 and uni_gap <= -res2.fun + 1e-12
            rows.append({"a": a, "b_min": b0, "b_max": bb, "rate_ratio": ratio,
                         "best_two_point_gap_pp": 100 * two_gap, "best_two_point_slow_prob": two_p,
                         "uniform_gap_pp": 100 * uni_gap, "proved_ceiling_pp": 100 * (-res2.fun)})
    return {"arithmetic": "floating point (series (30), symmetric eigen-decomposition, quadrature)",
            "rows": rows}


def main():
    result = {"python": platform.python_version(), "part1_certified": part1()}
    try:
        import numpy, scipy
        result["numpy"], result["scipy"] = numpy.__version__, scipy.__version__
        result["part2_finite_N_multitype"] = part2()
        result["part3_rate_caps"] = part3()
    except ImportError:
        result["part2_finite_N_multitype"] = "skipped: NumPy/SciPy not installed"
    result["all_assertions_passed"] = True
    (OUT / "stationary_identity_results.json").write_text(json.dumps(result, indent=2) + "\n")
    w = result["part1_certified"]["witness"]
    print("Witness conjecture value in", w["conjecture_value_bracket"])
    print("Witness equilibrium-start value in", w["equilibrium_start_value_bracket"], "= 7/9")
    if isinstance(result.get("part2_finite_N_multitype"), dict):
        p2 = result["part2_finite_N_multitype"]
        for N, d in p2["floating_sparse"].items():
            print(N, {k: round(v, 10) for k, v in d.items() if k in INITS})
        print("limits", p2["limits_floating_backward_ODE_T8"])
        for row in result["part3_rate_caps"]["rows"]:
            print(row)
    print("PASS")


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
