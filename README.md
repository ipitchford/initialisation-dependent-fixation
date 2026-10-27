# Initialisation-dependent fixation in noisy weighted voter models

**A resolution of Conjecture 2 of Ganesh, Hauert and Valla.** Version 1.0.0-candidate, 27 October 2026. Author: Anonymous.

**Status: unrefereed research candidate.** Internal AI-assisted review only; not peer-reviewed, independently reproduced or formally verified. See [STATUS.md](STATUS.md) and [ASSURANCE.md](ASSURANCE.md).

DOI: [10.5281/zenodo.23687032](https://doi.org/10.5281/zenodo.23687032) (concept DOI [10.5281/zenodo.23687031](https://doi.org/10.5281/zenodo.23687031)). Release page: https://evidencepress.org/releases/initialisation-dependent-fixation/

## In brief

Ganesh, Hauert and Valla (*Swarm Intelligence* 19(3), 173–214, 2025; [doi:10.1007/s11721-025-00248-z](https://doi.org/10.1007/s11721-025-00248-z)) conjectured that, in the noisy weighted voter model on a complete graph, the probability that k agents holding the better option eventually win tends to the survival probability of a branching process built from the *equilibrium* law of the agents' signalling rates. The conjecture states that the initial rates are *freshly sampled*.

- **Refuted as stated.** Under the fresh start, the limit is governed by the transient mean resident rate. Whenever resident rates vary, the better option wins strictly more often than conjectured (Theorems 1, 2 and 4; Corollary 5). Example: favourable rates 1/2 or 1 and resident rates 2 or 6, each with probability 1/2, give 0.7842… instead of (3+√37)/12 = 0.7569…; with constant favourable rate 1 the limit is 0.70203… instead of 2/3.
- **Confirmed in part.** Under the equilibrium start that the source simulated, the conjectured formula is exact for a constant favourable rate (equation (7)).
- **Replaced for varied favourable rates.** From equilibrium the limit is 1 − (E T_B / E T_A)^k (Theorem 6), which strictly exceeds the conjectured value (Corollary 7). The formula holds exactly only for equilibrium residents with fresh favourable founders.
- **Size of the error.** The single-founder underestimate has supremum 27.3355… percentage points, not attained (Proposition 5.1); rate caps reduce it (Table 3). An explicit burn-in time removes it (Section 6).

Scope: complete graph, exponential signalling periods, bounded rates with every favourable rate strictly below every resident rate.

## Contents

| Path | What it is |
|---|---|
| [consensus/initialisation_dependent_fixation.pdf](consensus/initialisation_dependent_fixation.pdf) | The manuscript (28 pages) |
| [consensus/manuscript.md](consensus/manuscript.md) | Source (Pandoc Markdown); [manuscript.tex](consensus/manuscript.tex) is generated from it |
| [consensus/references.bib](consensus/references.bib) | The bibliography, checked against Crossref |
| [consensus/certify_limits.py](consensus/certify_limits.py) → [certified_limits.json](consensus/certified_limits.json) | Exact rational certificates (Appendix A) |
| [consensus/evidence/verify_finite_n.py](consensus/evidence/verify_finite_n.py) | Constant-rate finite-population chains (Section 8, Table 5) and the rational chain (34) |
| [consensus/evidence/multitype_bracket.py](consensus/evidence/multitype_bracket.py) | Numerical (not certified) integration for the bracket (53) |
| [consensus/evidence/stationary_identity_and_caps.py](consensus/evidence/stationary_identity_and_caps.py) | Exact certification of Theorem 6 and Corollary 7; Table 4; Table 3 |
| [evidence/run_checks.py](evidence/run_checks.py) | Replays all four scripts in a temporary copy and compares exact outputs |
| [negative_controls.py](negative_controls.py) | Nine semantic corruptions that the evidence must reject |
| [evidence/make_figures.py](evidence/make_figures.py), [evidence/build_pdfs.py](evidence/build_pdfs.py) | Figures and PDF build |
| `consensus/evidence/derivation.md`, `novelty_report.md`, `target.yaml` | Development notes from the original research run (19 October 2026); the manuscript takes precedence |
| [REVISION_RESPONSE.md](REVISION_RESPONSE.md), [FINAL_FIXES.md](FINAL_FIXES.md), [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md) | Review findings, dispositions and final editor fixes |
| [CLAIMS.json](CLAIMS.json), [AI_INDEX.md](AI_INDEX.md), [RESEARCH_GATES.json](RESEARCH_GATES.json) | Machine-readable claims, agent index, prior-art and limitation records |

## Reproduce

From the package root. `certify_limits.py` and `negative_controls.py` need only the standard library; the rest need NumPy and SciPy ([requirements.txt](requirements.txt)).

```bash
python3 -B -I negative_controls.py
python3 -m pip install -r requirements.txt
python3 -B -I evidence/run_checks.py      # about 3-8 minutes
```

Each script writes outputs beside itself, so run individual scripts in a copy if you want to keep the stored references; `run_checks.py` does this for you. Exact (rational) outputs replay identically; floating values can differ in the last digits across NumPy/SciPy versions, which is why the manuscript rounds them to ten decimals. No stochastic simulation is used.

To rebuild: `python3 -I evidence/make_figures.py` (needs matplotlib) and `python3 -I evidence/build_pdfs.py` (needs Pandoc and XeLaTeX with Latin Modern OpenType fonts).

## Licence

Text, figures, data and records: CC0-1.0 ([LICENSE](LICENSE)). Code: MIT ([LICENSE-MIT.txt](LICENSE-MIT.txt)). See [LICENSES.md](LICENSES.md). `SHA256SUMS` lists every file except itself.
