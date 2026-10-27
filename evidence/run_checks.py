"""Replay the consensus manuscript's verification scripts in a temporary copy.

The supplied files are not modified. Exact outputs are compared with the
delivered references. Floating consistency tests are explicitly not certificates.

Run from anywhere, ideally as
    uv run --no-project --with numpy --with scipy python3 -I evidence/run_checks.py
"""
from pathlib import Path
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    results = []
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="consensus_replay_") as tmp:
        stage = Path(tmp)
        shutil.copytree(ROOT / "consensus", stage / "consensus",
                        ignore=shutil.ignore_patterns("*.pdf", "*.tex", "__pycache__"))

        def run(relative):
            t = time.perf_counter()
            process = subprocess.run([sys.executable, "-I", str(stage / relative)],
                                     cwd=stage, text=True, capture_output=True)
            if process.returncode:
                raise RuntimeError(relative + " failed:\n" + process.stdout + process.stderr)
            record = {"script": relative, "exit_code": process.returncode,
                      "seconds": round(time.perf_counter() - t, 4)}
            results.append(record)
            return process.stdout, record

        _, record = run("consensus/certify_limits.py")
        actual = json.loads((stage / "consensus/certified_limits.json").read_text())
        reference = json.loads((ROOT / "consensus/certified_limits.json").read_text())
        assert actual == reference, "Scalar rational certificate differs"
        record.update(arithmetic="exact fractions", reference_match=True)

        _, record = run("consensus/evidence/verify_finite_n.py")
        actual = json.loads((stage / "consensus/evidence/finite_n_verification.json").read_text())
        reference = json.loads((ROOT / "consensus/evidence/finite_n_verification.json").read_text())
        assert actual["all_assertions_passed"]
        assert actual["exact"] == reference["exact"], "Exact finite-population records differ"
        assert actual["rational_strict_separation"] == reference["rational_strict_separation"]
        record.update(arithmetic="exact small chains; residual-checked floating comparisons",
                      exact_reference_match=True, environment=actual["environment"])

        _, record = run("consensus/evidence/multitype_bracket.py")
        actual = json.loads((stage / "consensus/evidence/multitype_bracket_results.json").read_text())
        assert actual["checks"]["all_checks_passed"]
        record.update(arithmetic="floating ODE approximations; not certified enclosures",
                      consistency_assertions_passed=True)

        _, record = run("consensus/evidence/stationary_identity_and_caps.py")
        actual = json.loads((stage / "consensus/evidence/stationary_identity_results.json").read_text())
        reference = json.loads((ROOT / "consensus/evidence/stationary_identity_results.json").read_text())
        assert actual["all_assertions_passed"]
        assert actual["part1_certified"] == reference["part1_certified"], "Certified identity records differ"
        a2, r2 = actual["part2_finite_N_multitype"], reference["part2_finite_N_multitype"]
        assert a2["exact_small_N"] == r2["exact_small_N"], "Exact multitype chain values differ"
        record.update(arithmetic="exact fractions (identity, small N); floating (large N, ODE, rate caps)",
                      exact_reference_match=True)

    return {"status": "PASS", "python": platform.python_version(),
            "all_four_scripts_passed": True,
            "elapsed_seconds": round(time.perf_counter() - started, 4),
            "checks": results,
            "scope": "Replays supplied algorithms and exact reference outputs; the conventional proofs remain the justification for asymptotic limits."}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
