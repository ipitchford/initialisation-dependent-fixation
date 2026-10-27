#!/usr/bin/env python3
"""Exact rational enclosures for the scalar fixation formula and sharp envelope.

Only the Python standard library is required. Numerical labels are decimal
presentations of proved rational bounds; no floating point enters a certificate.
"""
from fractions import Fraction as F
from math import factorial
from decimal import Decimal, localcontext
import json
from pathlib import Path


def exp_bounds(x, degree=140):
    """Enclose exp(x), x>=0, by a positive Taylor sum and geometric tail."""
    x = F(x)
    assert x >= 0 and F(degree + 2) > x
    term = F(1)
    total = term
    for j in range(1, degree + 1):
        term *= x / j
        total += term
    next_term = term * x / (degree + 1)
    tail = next_term / (1 - x / (degree + 2))
    return total, total + tail


def scalar_bounds(a, r, R, p, degree=100):
    a, r, R, p = map(F, (a, r, R, p))
    assert 0 < a < r < R and 0 < p < 1
    kappa = p * R + (1 - p) * r
    lam = r * R / kappa
    delta = lam - a
    D = p * (1 - p) * (R - r) ** 2 / kappa ** 2
    exp_lo, exp_hi = exp_bounds(D, degree + 40)
    term = F(1)
    total = term / delta
    for j in range(1, degree + 1):
        term *= D / j
        total += term / (delta + kappa * j)
    next_term = term * D / (degree + 1)
    tail = next_term / (1 - D / (degree + 2))
    tail /= delta + kappa * (degree + 1)
    I_lo, I_hi = total / exp_hi, (total + tail) / exp_lo
    c_lo, c_hi = 1 / (1 + a * I_hi), 1 / (1 + a * I_lo)
    assert c_lo > 1 - a / lam
    return dict(a=a, r=r, R=R, p=p, kappa=kappa, lam=lam, D=D,
                stationary=1-a/lam, c_lower=c_lo, c_upper=c_hi,
                integral_lower=I_lo, integral_upper=I_hi)


def envelope_at(t):
    t = F(t)
    e_lo, e_hi = exp_bounds(t)
    q_lo, q_hi = 1/e_hi, 1/e_lo
    return t/(t+q_hi), t/(t+q_lo)


def derivative_sign(t):
    t = F(t)
    e_lo, e_hi = exp_bounds(t)
    q_lo, q_hi = 1/e_hi, 1/e_lo
    # f(q)=q(1+t)^3-(t+q)^2 is increasing on this enclosure.
    assert (1+t)**3 - 2*t - 2*q_hi > 0
    f = lambda q: q*(1+t)**3-(t+q)**2
    return f(q_lo), f(q_hi)


def dec(x, digits=30):
    with localcontext() as ctx:
        ctx.prec = digits
        return str(Decimal(x.numerator) / Decimal(x.denominator))


def encode(obj):
    if isinstance(obj, F):
        return {'rational': str(obj), 'decimal': dec(obj)}
    if isinstance(obj, dict):
        return {k: encode(v) for k, v in obj.items()}
    return obj


def main():
    simple = scalar_bounds(1, 2, 6, F(1, 2))
    strong = scalar_bounds(1, 2, 100, F(1, 10))
    t_lo, t_hi = F('1.71891151345837'), F('1.71891151345839')
    assert derivative_sign(t_lo)[0] > 0
    assert derivative_sign(t_hi)[1] < 0
    c_l = envelope_at(t_lo)[0]
    c_u = envelope_at(t_hi)[1]
    gap_lo = c_l - t_hi/(1+t_hi)
    gap_hi = c_u - t_lo/(1+t_lo)
    checks = {
        'arithmetic': 'exact fractions; positive exponential series plus geometric tails',
        'simple_witness': encode(simple),
        'strong_witness': encode(strong),
        'sharp_global_gap': encode(dict(t_lower=t_lo, t_upper=t_hi,
                                       gap_lower=gap_lo, gap_upper=gap_hi)),
        'assertions': 'PASS',
        'scope': 'certifies scalar integrals and maximiser bracket; analytic theorem proves uniqueness and attainability as a supremum'
    }
    out = Path(__file__).with_name('certified_limits.json')
    out.write_text(json.dumps(checks, indent=2) + '\n')
    for label, result in [('simple', simple), ('strong', strong)]:
        print(label, 'c in', dec(result['c_lower'], 24), dec(result['c_upper'], 24))
    print('maximum gap in', dec(gap_lo, 24), dec(gap_hi, 24))
    print('PASS', out.name)


if __name__ == '__main__':
    main()
