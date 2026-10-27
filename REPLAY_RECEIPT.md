# Replay receipt

## Clean-copy replay (27 October 2026)

After the final editor fixes, the whole approved bundle was copied to a fresh directory and every script was run there with `uv run --no-project [--with numpy --with scipy] python3 -I` (Python 3.11.14, NumPy 2.4.6, SciPy 1.17.1, macOS arm64):

| Command | Result |
|---|---|
| `consensus/certify_limits.py` | PASS; `certified_limits.json` byte-identical to the stored receipt |
| `consensus/evidence/verify_finite_n.py` | PASS (all assertions; exact records match) |
| `consensus/evidence/multitype_bracket.py` | PASS (all consistency checks; values numerical, not certified) |
| `consensus/evidence/stationary_identity_and_caps.py` | PASS (exact Theorem 6/Corollary 7 certificates and small-N chains match) |
| `evidence/run_checks.py` (replays all four in a temporary copy) | `"status": "PASS"`, `"all_four_scripts_passed": true` (1339 s under shared load) |

Every script in this package is byte-identical to the replayed copy. The in-place runs regenerated the stored outputs byte for byte, except `finite_n_verification.json`, whose elapsed-time field differs; its exact records are identical. The publication step changed only the manuscript text (DOI and repository link; reference formatting), the PDF and the added records.

## Frozen-archive checks

On the frozen release archive, from a fresh extraction: `negative_controls.py` (standard library; replays `certify_limits.py` and rejects all nine corruptions), manifest and archive integrity, PDF text preflight, rating-leak scan, AI-index and research-gate completeness. CI (`.github/workflows/replay.yml`) repeats the certificate comparison and negative controls, and runs `evidence/run_checks.py` on Linux.

Producer-side replay only; not independent reproduction.
