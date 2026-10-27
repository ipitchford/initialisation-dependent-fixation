#!/usr/bin/env python3
"""Exact and deterministic numerical checks for the noisy-voter counterexamples.

Python standard library supplies all exact arithmetic. NumPy/SciPy supply the
explicitly non-certified sparse checks at larger N and an independent labelled
configuration-chain check. No random sampling is used.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import platform
import time
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent
CASES = [
    {"name": "rates_2_6", "a": Q(1), "r": Q(2), "s": Q(6), "p": Q(1, 2)},
    {"name": "rates_2_100", "a": Q(1), "r": Q(2), "s": Q(100), "p": Q(1, 10)},
]


def transient_states(n):
    return [(m, j) for m in range(1, n) for j in range(n - m + 1)]


def exact_generator(n, case):
    """Negative transient generator H=-L, Hh=rhs, six count transitions."""
    states = transient_states(n)
    index = {x: i for i, x in enumerate(states)}
    hmat = [[Q(0) for _ in states] for _ in states]
    rhs = [Q(0) for _ in states]
    a, r, s, p = (case[x] for x in ("a", "r", "s", "p"))
    for (m, j), row in index.items():
        b = n - m
        transitions = [
            ((m - 1, j + 1), a * Q(m * b, n - 1) * p),
            ((m - 1, j), a * Q(m * b, n - 1) * (1 - p)),
            ((m + 1, j - 1), r * Q(j * m, n - 1)),
            ((m + 1, j), s * Q((b - j) * m, n - 1)),
            ((m, j - 1), r * Q(j * (b - 1), n - 1) * (1 - p)),
            ((m, j + 1), s * Q((b - j) * (b - 1), n - 1) * p),
        ]
        for target, rate in transitions:
            if rate == 0:
                continue
            assert rate > 0
            hmat[row][row] += rate
            if target in index:
                hmat[row][index[target]] -= rate
            elif target[0] == n:
                rhs[row] += rate
            else:
                assert target[0] == 0
    return states, index, hmat, rhs


def exact_solve(mat, rhs):
    aug = [row[:] + [v] for row, v in zip(mat, rhs)]
    n = len(mat)
    determinant = Q(1)
    for col in range(n):
        pivot = next(i for i in range(col, n) if aug[i][col] != 0)
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
            determinant = -determinant
        scale = aug[col][col]
        determinant *= scale
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor:
                aug[row] = [x - factor * y for x, y in zip(aug[row], aug[col])]
    sol = [row[-1] for row in aug]
    residual = [sum(x * y for x, y in zip(row, sol)) - b for row, b in zip(mat, rhs)]
    assert all(x == 0 for x in residual)
    assert determinant != 0
    assert all(Q(0) < x < Q(1) for x in sol)
    return sol, determinant


def exact_binomial_average(n, theta, values, index, k=1):
    return sum(
        Q(math.comb(n - k, j)) * theta**j * (1 - theta) ** (n - k - j) * values[index[k, j]]
        for j in range(n - k + 1)
    )


def exact_charpoly(mat):
    """Faddeev-LeVerrier; coefficients descending, checks final zero matrix."""
    n = len(mat)
    bmat = [[Q(int(i == j)) for j in range(n)] for i in range(n)]
    coeff = [Q(1)]
    for k in range(1, n + 1):
        prod = [
            [sum(mat[i][l] * bmat[l][j] for l in range(n)) for j in range(n)]
            for i in range(n)
        ]
        c = -sum(prod[i][i] for i in range(n)) / k
        coeff.append(c)
        for i in range(n):
            prod[i][i] += c
        bmat = prod
    assert all(x == 0 for row in bmat for x in row)
    return coeff


def exact_record(n, case):
    states, index, mat, rhs = exact_generator(n, case)
    sol, determinant = exact_solve(mat, rhs)
    p, r, s = (case[x] for x in ("p", "r", "s"))
    lam = 1 / (p / r + (1 - p) / s)
    fresh = exact_binomial_average(n, p, sol, index)
    stationary = exact_binomial_average(n, lam * p / r, sol, index)
    charpoly = exact_charpoly(mat)
    assert charpoly[-1] == (-1) ** len(mat) * determinant
    canonical = json.dumps([[str(x) for x in row] for row in mat], separators=(",", ":"))
    return {
        "case": case["name"], "N": n, "states": states,
        "state_count": len(states), "negative_killed_generator": [[str(x) for x in row] for row in mat],
        "rhs": [str(x) for x in rhs], "harmonic_solution": [str(x) for x in sol],
        "equations_checked": len(states), "exact_residual": "0", "matrix_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "matrix_rank": len(states), "matrix_trace": str(sum(mat[i][i] for i in range(len(mat)))),
        "matrix_determinant": str(determinant), "characteristic_polynomial_descending": [str(x) for x in charpoly],
        "fresh_exact": str(fresh), "fresh_decimal": float(fresh),
        "stationary_exact": str(stationary), "stationary_decimal": float(stationary),
        "source_asymptotic_prediction_exact": str(1 - case["a"] / lam),
    }


def sparse_count_solution(n, case):
    """Separate floating implementation, using four opinion/phase events."""
    import numpy as np
    from scipy.sparse import coo_matrix
    from scipy.sparse.linalg import spsolve
    from scipy.stats import binom

    a, r, s, p = (float(case[x]) for x in ("a", "r", "s", "p"))
    states = transient_states(n)
    index = {x: i for i, x in enumerate(states)}
    rows, cols, vals = [], [], []
    rhs = np.zeros(len(states))

    def add(row, state, rate):
        if rate == 0:
            return
        rows.append(row); cols.append(row); vals.append(rate)
        if state[0] == n:
            rhs[row] += rate
        elif state[0] != 0:
            rows.append(row); cols.append(index[state]); vals.append(-rate)

    for row, (m, j) in enumerate(states):
        b = n - m
        # A death: a uniformly copied B opinion then receives a fresh phase.
        ad = a * m * b / (n - 1)
        add(row, (m - 1, j + 1), p * ad)
        add(row, (m - 1, j), (1 - p) * ad)
        # Each B phase may copy A, or copy B and redraw a different phase.
        for phase_count, rate, slow in [(j, r, True), (b - j, s, False)]:
            clock = phase_count * rate / (n - 1)
            add(row, (m + 1, j - int(slow)), clock * m)
            other_phase_probability = (1 - p) if slow else p
            add(row, (m, j - 1 if slow else j + 1), clock * (b - 1) * other_phase_probability)

    mat = coo_matrix((vals, (rows, cols)), shape=(len(states), len(states))).tocsc()
    sol = spsolve(mat, rhs)
    res = mat @ sol - rhs
    norm = float(np.max(np.asarray(abs(mat).sum(axis=1))))
    backward = float(np.max(abs(res))) / (norm * float(np.max(abs(sol))) + float(np.max(abs(rhs))))
    js = np.arange(n)
    vals1 = np.array([sol[index[1, int(j)]] for j in js])
    lam = 1 / (p / r + (1 - p) / s)
    fresh = float(binom.pmf(js, n - 1, p) @ vals1)
    stationary = float(binom.pmf(js, n - 1, lam * p / r) @ vals1)
    assert np.min(sol) >= -1e-8 and np.max(sol) <= 1 + 1e-8
    assert backward < 1e-12
    return {
        "case": case["name"], "N": n, "state_count": len(states), "nonzero_entries": int(mat.nnz),
        "fresh_numeric": fresh, "stationary_numeric": stationary,
        "maximum_absolute_residual": float(np.max(abs(res))), "normwise_backward_error": backward,
        "solution_min": float(np.min(sol)), "solution_max": float(np.max(sol)),
        "status": "ordinary double-precision sparse solve; residual checked; not an interval certificate",
    }


def labelled_numeric(n, case):
    """Independent labelled vertex chain: enumerate clocks/copy targets/draws."""
    import numpy as np
    from scipy.sparse import coo_matrix
    from scipy.sparse.linalg import spsolve

    a, r, s, p = (float(case[x]) for x in ("a", "r", "s", "p"))
    # 0=A, 1=B slow, 2=B fast. All-B rate states collapse to fixation boundary 0.
    states = [x for x in itertools.product((0, 1, 2), repeat=n) if 0 in x and any(y != 0 for y in x)]
    index = {x: i for i, x in enumerate(states)}
    rows, cols, vals = [], [], []
    rhs = np.zeros(len(states))
    for x, row in index.items():
        for v in range(n):
            clock = (a, r, s)[x[v]] / (n - 1)
            for u in range(n):
                if u == v:
                    continue
                outcomes = [(0, 1.0)] if x[u] == 0 else [(1, p), (2, 1 - p)]
                for new_phase, probability in outcomes:
                    if new_phase == x[v]:
                        continue
                    y = list(x); y[v] = new_phase; y = tuple(y)
                    rate = clock * probability
                    rows.append(row); cols.append(row); vals.append(rate)
                    if y in index:
                        rows.append(row); cols.append(index[y]); vals.append(-rate)
                    elif all(z == 0 for z in y):
                        rhs[row] += rate
                    else:
                        assert 0 not in y
    mat = coo_matrix((vals, (rows, cols)), shape=(len(states), len(states))).tocsc()
    sol = spsolve(mat, rhs)
    answer = 0.0
    for phases in itertools.product((1, 2), repeat=n - 1):
        probability = math.prod(p if x == 1 else 1 - p for x in phases)
        answer += probability * sol[index[(0,) + phases]]
    return {"case": case["name"], "N": n, "labelled_transient_states": len(states), "fresh_numeric": float(answer), "maximum_absolute_residual": float(np.max(abs(mat @ sol - rhs)))}


def integral_check(case):
    from scipy.integrate import quad
    a, r, s, p = (float(case[x]) for x in ("a", "r", "s", "p"))
    kap = (1 - p) * r + p * s
    lam = r * s / kap
    excess = p * r + (1 - p) * s - lam
    delta, zeta = lam - a, excess / kap
    integral, estimated_error = quad(lambda t: math.exp(-delta*t - zeta*(-math.expm1(-kap*t))), 0, math.inf, epsabs=1e-13, epsrel=1e-13)
    return {"case": case["name"], "lambda": lam, "kappa": kap, "excess_amplitude": excess,
            "integral_numeric": integral, "quadrature_error_estimate": estimated_error,
            "corrected_fixation_numeric": 1/(1+a*integral), "source_prediction_numeric": 1-a/lam,
            "status": "deterministic floating quadrature; not an interval certificate"}


def rational_certificate():
    lower = sum((-Q(59,50))**j / math.factorial(j) for j in range(6))
    positive = sum(Q(37,10)**j / math.factorial(j) for j in range(10))
    assert lower > Q(3,10)
    assert positive > 40
    # b(t) = 1000/59 + (21609/295) exp(-59 t/5) is decreasing; at t = 1/10 it exceeds 38.
    birth_lower = Q(1000,59) + Q(21609,295) * lower
    assert birth_lower > 38
    # Homogeneous birth 38, death 1, horizon 1/10, fixation ratio 1/2:
    # 1 - G(1/2) = 37/(38 + 36 exp(-37/10)) > 37/(38 + 36/positive) > 370/389.
    gf_lower = Q(37) / (38 + 36 / positive)
    assert gf_lower > Q(370,389)
    assert Q(370,389) > Q(941,1000)
    return {"exp_minus_59_over_50_lower": str(lower), "comparison_lower": "3/10",
            "birth_rate_lower_bound_on_0_to_1_over_10": str(birth_lower),
            "generating_function_lower_bound": str(gf_lower),
            "exp_37_over_10_lower": str(positive), "comparison_upper_inverse": "40",
            "fixation_liminf_strict_lower": "370/389", "source_prediction": "941/1000",
            "strict_gap_exact": str(Q(370,389)-Q(941,1000)), "passed": True}


def main():
    import numpy as np
    import scipy
    started = time.time()
    exact = [exact_record(n, case) for case in CASES for n in (2,3,4,5)]
    labelled = [labelled_numeric(n, case) for case in CASES for n in (2,3,4)]
    for item in labelled:
        reference = next(x for x in exact if x["case"] == item["case"] and x["N"] == item["N"])
        item["difference_from_exact_count_chain"] = abs(item["fresh_numeric"]-reference["fresh_decimal"])
        assert item["difference_from_exact_count_chain"] < 2e-13
    numerical = []
    for case in CASES:
        for n in (10,25,50,100,200):
            row = sparse_count_solution(n,case)
            numerical.append(row)
            print(case["name"], n, f"fresh={row['fresh_numeric']:.12f}", f"stationary={row['stationary_numeric']:.12f}", flush=True)
    result = {
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "cases": [{k:str(v) for k,v in case.items()} for case in CASES],
        "exact": exact, "independent_labelled_checks": labelled, "large_n_numerical": numerical,
        "limiting_integral_numerical": [integral_check(case) for case in CASES],
        "rational_strict_separation": rational_certificate(),
        "elapsed_seconds": time.time()-started, "all_assertions_passed": True,
    }
    (HERE/"finite_n_verification.json").write_text(json.dumps(result,indent=2)+"\n")
    with (HERE/"finite_n_values.csv").open("w",newline="") as stream:
        out=csv.writer(stream)
        out.writerow(["case","N","fresh_fixation","stationary_fixation","arithmetic"])
        for x in exact:out.writerow([x["case"],x["N"],x["fresh_decimal"],x["stationary_decimal"],"exact rational"])
        for x in numerical:out.writerow([x["case"],x["N"],x["fresh_numeric"],x["stationary_numeric"],"double-precision sparse"])
    print("All exact residuals, characteristic-polynomial identities, independent labelled checks, and rational inequalities passed.")
    print(f"Elapsed {result['elapsed_seconds']:.3f} seconds")


if __name__ == "__main__":
    main()
