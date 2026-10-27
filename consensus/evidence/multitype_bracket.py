#!/usr/bin/env python3
"""Deterministic demonstration of the multitype finite-horizon bracket.

Run:
    python multitype_bracket.py
    python multitype_bracket.py --output-dir /path/to/output

Dependencies: Python 3, NumPy and SciPy. No stochastic simulation is used.

All reported numbers are FLOATING-POINT APPROXIMATIONS. The underlying
finite-horizon inequalities are proved analytically in the manuscript, but
ordinary ODE tolerances are not rigorous error bounds. The computed endpoint
values are therefore NOT certified numerical enclosures.

For terminal vector s, Q_i(t) is the PGF at terminal time T, from one type-i
individual at t. It solves
    Q_i' = a_i*(Q_i-1) + b(t)*Q_i*(1-dot(p,Q)),  Q(T)=s.
With q=max(a_i)/b_min<1, Q(T)=q*1 evaluates E[q**Z(T)], and
Q(T)=0 evaluates P(Z(T)=0). Thus, for k iid initial types with law nu,
    1-(nu dot Q^{T,q}(0))**k <= limiting fixation
                              <= 1-(nu dot Q^{T,0}(0))**k.

The exact lower endpoints increase with T: q**Z(t) is a supermartingale,
since total deaths are <=max(a_i)*Z(t) and total births >=b_min*Z(t).
The exact upper endpoints decrease with T. Both converge by the
extinction/survival dichotomy proved in the manuscript.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
from scipy.special import erfi


HORIZONS = (0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0)
RTOL = 2e-12
ATOL = 2e-14


def backward_pgf(T, terminal, rates, redraw, intensity, method="DOP853"):
    """Return Q(0) without clipping the ODE solution to the unit interval."""
    rates = np.asarray(rates, dtype=float)
    redraw = np.asarray(redraw, dtype=float)
    terminal = np.broadcast_to(np.asarray(terminal, dtype=float), rates.shape)
    assert T >= 0 and np.all(rates > 0)
    assert np.all(redraw >= 0) and abs(float(redraw.sum()) - 1) < 1e-14
    assert np.all((0 <= terminal) & (terminal <= 1))
    if T == 0:
        return terminal.copy()

    def rhs(t, value):
        return rates * (value - 1.0) + intensity(t) * value * (
            1.0 - float(redraw @ value)
        )

    sol = solve_ivp(
        rhs, (float(T), 0.0), terminal, method=method, rtol=RTOL, atol=ATOL
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    value = sol.y[:, -1]
    if np.any(value < -1e-10) or np.any(value > 1.0 + 1e-10):
        raise ArithmeticError("PGF solution outside probability range")
    return value


def fixation_bracket(T, rates, redraw, initial, intensity, b_min, k=1,
                     method="DOP853"):
    rates = np.asarray(rates, dtype=float)
    initial = np.asarray(initial, dtype=float)
    assert np.all(initial >= 0) and abs(float(initial.sum()) - 1) < 1e-14
    assert isinstance(k, int) and k >= 1
    q = float(max(rates) / b_min)
    assert 0 < q < 1
    Q_zero = backward_pgf(T, 0.0, rates, redraw, intensity, method)
    Q_q = backward_pgf(T, q, rates, redraw, intensity, method)
    assert np.all(Q_zero <= Q_q + 1e-10)
    lower = 1.0 - float(initial @ Q_q) ** k
    upper = 1.0 - float(initial @ Q_zero) ** k
    return {
        "T": float(T),
        "lower_approx": lower,
        "upper_approx": upper,
        "width_approx": upper - lower,
        "Q_zero_at_0": Q_zero.tolist(),
        "Q_q_at_0": Q_q.tolist(),
    }


def scalar_pgf_by_quadrature(T, s, a=1.0, lam=3.0, C=1.0, kappa=4.0):
    """Independent classical PGF evaluation for b(t)=lam+C*exp(-kappa*t)."""
    def cumulative(t):
        return (lam - a) * t - (C / kappa) * math.expm1(-kappa * t)

    J, _ = quad(lambda t: a * math.exp(-cumulative(t)), 0.0, T,
                epsabs=2e-14, epsrel=2e-13)
    E = math.exp(-cumulative(T))
    return 1.0 - (1.0 - s) / ((1.0 + J) * (1.0 - s) + E * s)


def check_monotonicity(rows, tolerance=1e-10):
    """Numerical consistency check; this is not a proof of monotonicity."""
    for previous, current in zip(rows[:-1], rows[1:]):
        assert current["lower_approx"] >= previous["lower_approx"] - tolerance
        assert current["upper_approx"] <= previous["upper_approx"] + tolerance


def main(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    rates = np.array([0.5, 1.0])
    redraw = np.array([0.5, 0.5])
    initial = redraw.copy()
    b_min, lam, C, kappa = 2.0, 3.0, 1.0, 4.0
    fresh = lambda t: lam + C * math.exp(-kappa * t)
    equilibrium = lambda t: lam

    fresh_rows = [
        fixation_bracket(T, rates, redraw, initial, fresh, b_min)
        for T in HORIZONS
    ]
    equilibrium_rows = [
        fixation_bracket(T, rates, redraw, initial, equilibrium, b_min)
        for T in HORIZONS
    ]
    check_monotonicity(fresh_rows)
    check_monotonicity(equilibrium_rows)

    # An independent implicit ODE algorithm checks that the two-component
    # implementation does not depend materially on the explicit integrator.
    algorithm_checks = []
    for T in (2.0, 4.0, 8.0):
        explicit = fixation_bracket(T, rates, redraw, initial, fresh, b_min)
        implicit = fixation_bracket(
            T, rates, redraw, initial, fresh, b_min, method="Radau"
        )
        difference = max(
            abs(explicit[key] - implicit[key])
            for key in ("lower_approx", "upper_approx")
        )
        assert difference < 2e-10
        algorithm_checks.append({"T": T, "DOP853_vs_Radau_max_difference": difference})

    # Scalar reduction checks both terminal conditions against the known PGF,
    # evaluated by an independent one-dimensional quadrature.
    scalar_errors = []
    for T in HORIZONS:
        for s in (0.0, 0.5):
            ode = float(backward_pgf(T, s, [1.0], [1.0], fresh)[0])
            formula = scalar_pgf_by_quadrature(T, s)
            scalar_errors.append(abs(ode - formula))
    assert max(scalar_errors) < 2e-10
    scalar_limit_erfi = 1.0 / (
        1.0 + math.sqrt(math.pi) / 2 * math.exp(-0.25) * float(erfi(0.5))
    )
    scalar_rows = [
        fixation_bracket(T, [1.0], [1.0], [1.0], fresh, b_min)
        for T in HORIZONS
    ]
    for row in scalar_rows:
        assert row["lower_approx"] - 2e-10 <= scalar_limit_erfi
        assert scalar_limit_erfi <= row["upper_approx"] + 2e-10

    # In equilibrium, a scalar fixed point determines the multitype limit.
    # For the chosen data it also simplifies exactly to (3+sqrt(37))/12.
    scalar_fixed_point = brentq(
        lambda c: float(np.sum(redraw * lam / (rates + lam * c))) - 1.0,
        0.0, 1.0, xtol=5e-15, rtol=1e-14,
    )
    exact_expression_float = (3.0 + math.sqrt(37.0)) / 12.0
    assert abs(scalar_fixed_point - exact_expression_float) < 2e-14
    Q_stationary = rates / (rates + lam * scalar_fixed_point)
    stationary_fixation = 1.0 - float(initial @ Q_stationary)
    stationary_rhs = rates * (Q_stationary - 1.0) + lam * Q_stationary * (
        1.0 - float(redraw @ Q_stationary)
    )
    terminal_fixed_point_check = backward_pgf(
        8.0, Q_stationary, rates, redraw, equilibrium
    )
    stationary_drift = float(np.max(abs(terminal_fixed_point_check - Q_stationary)))
    assert stationary_drift < 2e-10
    assert float(np.max(abs(stationary_rhs))) < 2e-14
    for row in equilibrium_rows:
        assert row["lower_approx"] - 2e-10 <= stationary_fixation
        assert stationary_fixation <= row["upper_approx"] + 2e-10

    result = {
        "status": (
            "FLOATING-POINT APPROXIMATIONS ONLY. The analytical inequalities "
            "are proved, but these ODE outputs are not certified enclosures."
        ),
        "method": "SciPy solve_ivp DOP853, with selected independent Radau comparisons",
        "rtol": RTOL,
        "atol": ATOL,
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "model": {
            "A_rates": rates.tolist(),
            "A_redraw_probabilities": redraw.tolist(),
            "A_initial_probabilities": initial.tolist(),
            "B_rates": [2.0, 6.0],
            "B_redraw_probabilities": [0.5, 0.5],
            "fresh_B_initial_probabilities": [0.5, 0.5],
            "equilibrium_B_initial_probabilities": [0.75, 0.25],
            "fresh_B_intensity": "3+exp(-4*t)",
            "equilibrium_B_intensity": "3",
            "q": float(max(rates) / b_min),
            "founders": 1,
        },
        "fresh_multitype": fresh_rows,
        "equilibrium_multitype": equilibrium_rows,
        "fresh_scalar_check": scalar_rows,
        "checks": {
            "scalar_PGF_max_ODE_vs_quadrature_error": max(scalar_errors),
            "scalar_fresh_limit_erfi_approx": scalar_limit_erfi,
            "equilibrium_multitype_limit_expression": "(3+sqrt(37))/12",
            "equilibrium_multitype_limit_approx": stationary_fixation,
            "equilibrium_fixed_point_residual": float(np.max(abs(stationary_rhs))),
            "equilibrium_terminal_fixed_point_max_drift": stationary_drift,
            "independent_ODE_algorithm_comparisons": algorithm_checks,
            "monotonicity_numerical_tolerance": 1e-10,
            "all_checks_passed": True,
        },
    }
    (output_dir / "multitype_bracket_results.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    with (output_dir / "multitype_bracket_values.csv").open("w", newline="") as out:
        writer = csv.DictWriter(
            out, fieldnames=("initialisation", "T", "lower_approx",
                             "upper_approx", "width_approx")
        )
        writer.writeheader()
        for label, rows in (
            ("fresh_multitype", fresh_rows),
            ("equilibrium_multitype", equilibrium_rows),
            ("fresh_scalar_check", scalar_rows),
        ):
            for row in rows:
                writer.writerow({
                    "initialisation": label,
                    **{key: row[key] for key in writer.fieldnames[1:]},
                })

    print(result["status"])
    print("\nFresh resident population; two favourable types:")
    print(" T       lower approximation     upper approximation       width")
    for row in fresh_rows:
        print(f"{row['T']:4.1f}     {row['lower_approx']:.14f}       "
              f"{row['upper_approx']:.14f}       {row['width_approx']:.6g}")
    print("\nEquilibrium multitype limit:", f"{stationary_fixation:.14f}",
          " = (3+sqrt(37))/12")
    print("Scalar fresh limit:", f"{scalar_limit_erfi:.14f}")
    print("Maximum scalar PGF cross-check error:", f"{max(scalar_errors):.3g}")
    print("All numerical consistency checks passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path, default=Path(__file__).resolve().parent
    )
    main(parser.parse_args().output_dir)
