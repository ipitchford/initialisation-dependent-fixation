# SPDX-License-Identifier: MIT
"""Semantic negative controls (standard library only).

Each control states a plausible false claim or corrupted receipt and checks
that the shipped evidence rejects it. The unmodified baseline must pass first.
Run from the package root:  python3 -B negative_controls.py
"""
import json
import math
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent
C = ROOT / "consensus"


def load(p):
    return json.loads(Path(p).read_text())


def bracket(rec):
    return F(rec["c_lower"]["rational"]), F(rec["c_upper"]["rational"])


def check_scalar(cert, claimed_limit=None):
    """Baseline semantics of certified_limits.json; optional claimed value must lie in the bracket."""
    lo, hi = bracket(cert["simple_witness"])
    if not (F(2, 3) < lo <= hi):
        return False, "constant-rate witness must strictly exceed the conjectured 2/3"
    if claimed_limit is not None and not (lo <= claimed_limit <= hi):
        return False, "claimed limit outside certified bracket"
    g = cert["sharp_global_gap"]
    glo, ghi = F(g["gap_lower"]["rational"]), F(g["gap_upper"]["rational"])
    if not (F("0.2733554343215126") < glo <= ghi < F("0.2733554343215181")):
        return False, "global supremum outside (41)"
    return True, "ok"


def check_identity(res, claimed_eq=None):
    w = res["part1_certified"]["witness"]
    lam, eta = F(w["lambda"]), F(w["E_TA"])
    eq = 1 - 1 / (lam * eta)
    if claimed_eq is not None and claimed_eq != eq:
        return False, "equilibrium-start limit is 1 - 1/(lambda m_A)"
    if eq != F(w["equilibrium_start_exact"]):
        return False, "receipt disagrees with Theorem 6"
    conj = (3 + math.sqrt(37)) / 12
    if not (float(eq) > conj):
        return False, "Corollary 7 strict excess fails"
    return True, "ok"


def ceiling(b0, R, lam, a=1.0):
    bb = b0 * R
    D = (lam - b0) * (bb - lam) / (b0 * bb)
    g = lam - a
    return g / (g + a * math.exp(-D)) - g / lam


def max_ceiling(b0, R):
    best = 0.0
    n = 20000
    for i in range(1, n):
        lam = b0 + (b0 * R - b0) * i / n
        best = max(best, ceiling(b0, R, lam))
    return 100 * best


def check_cap(claim_pp, ratio, b0s):
    """A claimed upper bound (percentage points) must dominate the ceiling (43) for every b0/a tested."""
    worst = max(max_ceiling(b0, ratio) for b0 in b0s)
    return (worst <= claim_pp, f"worst ceiling {worst:.4f}")


def check_finite_table(rows, exact):
    by = {(r["case"], int(r["N"])): r for r in rows}
    for e in exact:
        r = by.get((e["case"], e["N"]))
        if r is None or abs(float(r["fresh_fixation"]) - float(F(e["fresh_exact"]))) > 1e-15:
            return False, f"table row disagrees with exact chain {e['case']} N={e['N']}"
    return True, "ok"


def read_csv(p):
    lines = Path(p).read_text().splitlines()
    head = lines[0].split(",")
    return [dict(zip(head, l.split(","))) for l in lines[1:] if l]


def replay_certificate():
    with tempfile.TemporaryDirectory(prefix="nc_") as td:
        stage = Path(td) / "consensus"
        stage.mkdir()
        shutil.copy2(C / "certify_limits.py", stage / "certify_limits.py")
        r = subprocess.run([sys.executable, "-B", "-I", str(stage / "certify_limits.py")], cwd=td,
                           capture_output=True, text=True)
        if r.returncode:
            sys.exit("certificate replay failed: " + r.stderr[-400:])
        return load(stage / "certified_limits.json")


def main():
    cert = load(C / "certified_limits.json")
    res = load(C / "evidence/stationary_identity_results.json")
    fin = load(C / "evidence/finite_n_verification.json")
    rows = read_csv(C / "evidence/finite_n_values.csv")
    fresh = replay_certificate()

    baseline = [
        ("replayed certificate equals receipt", (fresh == cert, "")),
        ("scalar witness semantics", check_scalar(cert)),
        ("Theorem 6 identity", check_identity(res)),
        ("ratio-3 ceiling below 8.27", check_cap(8.27, 3, [1.25, 1.1, 1.01, 1.001, 1.0000001])),
        ("finite-N table matches exact chains", check_finite_table(rows, fin["exact"])),
    ]
    bad = [n for n, (ok, _) in baseline if not ok]
    if bad:
        sys.exit(f"BASELINE FAILED: {bad}")

    controls = []
    t = json.loads(json.dumps(cert))
    t["simple_witness"]["c_lower"]["decimal"] = "0.702032053928212711530878678866"
    controls.append(("tampered certificate decimal", (fresh == t, "")))
    controls.append(("conjectured 2/3 claimed as the fresh-start limit", check_scalar(cert, F(2, 3))))
    t = json.loads(json.dumps(cert))
    t["simple_witness"]["c_lower"]["rational"] = "1/2"
    controls.append(("fresh limit below the conjecture", check_scalar(t)))
    t = json.loads(json.dumps(cert))
    t["sharp_global_gap"]["gap_upper"]["rational"] = "2733554343215200/10000000000000000"
    controls.append(("global supremum widened beyond (41)", check_scalar(t)))
    controls.append(("Conjecture 2 value claimed under equilibrium start",
                     check_identity(res, F(int(1e12 * (3 + math.sqrt(37)) / 12), int(1e12)))))
    t = json.loads(json.dumps(res))
    t["part1_certified"]["witness"]["equilibrium_start_exact"] = "3/4"
    controls.append(("tampered Theorem 6 receipt", check_identity(t)))
    controls.append(("superseded 'below 8 points' ceiling at ratio 3",
                     check_cap(8.0, 3, [1.25, 1.1, 1.01, 1.001])))
    controls.append(("superseded 'about 14 points' ceiling at ratio 10",
                     check_cap(14.0, 10, [1.25, 1.1, 1.01])))
    t = [dict(r) for r in rows]
    t[1]["fresh_fixation"] = str(float(t[1]["fresh_fixation"]) + 1e-6)
    controls.append(("tampered finite-N table row", check_finite_table(t, fin["exact"])))

    failed = [n for n, (ok, _) in controls if ok]
    for n, (ok, msg) in controls:
        print(("REJECTED " if not ok else "ACCEPTED (BAD) ") + n, msg)
    if failed:
        sys.exit(f"NEGATIVE CONTROLS NOT REJECTED: {failed}")
    print(f"PASS baseline ({len(baseline)} checks) and {len(controls)} negative controls rejected")


if __name__ == "__main__":
    main()
