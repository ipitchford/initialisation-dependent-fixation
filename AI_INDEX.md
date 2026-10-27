# Agent navigation

## Identity

- Release slug: `initialisation-dependent-fixation`. Version `1.0.0-candidate`, tag `v1.0.0-candidate`. DOI 10.5281/zenodo.23687032; concept DOI 10.5281/zenodo.23687031.
- Repository: https://github.com/ipitchford/initialisation-dependent-fixation. Release page: https://evidencepress.org/releases/initialisation-dependent-fixation/
- Scholarly creator: Anonymous. Status: unrefereed candidate ([STATUS.md](STATUS.md)).
- Manuscript: [PDF](consensus/initialisation_dependent_fixation.pdf) (28 pages); source [manuscript.md](consensus/manuscript.md), generated [manuscript.tex](consensus/manuscript.tex), bibliography [references.bib](consensus/references.bib).
- Claims: [CLAIMS.json](CLAIMS.json). Overview: [README.md](README.md). Assurance: [ASSURANCE.md](ASSURANCE.md). Review: [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md), [REVISION_RESPONSE.md](REVISION_RESPONSE.md), [FINAL_FIXES.md](FINAL_FIXES.md).
- Provenance and sources: [PROVENANCE.md](PROVENANCE.md), [SOURCES.md](SOURCES.md), [CITATION_AUDIT.md](CITATION_AUDIT.md), [RESEARCH_GATES.json](RESEARCH_GATES.json). Citation: [CITATION.cff](CITATION.cff). Licences: [LICENSES.md](LICENSES.md).

## Scientific map

Object: the noisy weighted voter model on the complete graph K_N. Each vertex holds opinion A or B and a rate R; at rate R it copies a uniformly chosen other vertex and redraws its rate from F_A (opinion A) or F (opinion B). k vertices start with A. Hypothesis (1): all favourable rates lie in [a_-, a_+], all resident rates in [b_-, b_+], with a_+ < b_-.

- Population limit: Proposition 3.6 (fixation equals survival of a time-inhomogeneous branching process with birth rate b_nu(t), the transient mean resident rate). Ingredients: Lemma 3.1 (fixation bound from every configuration), Lemma 3.2 (common-thinning coupling), Lemma 3.3 (resident environment LLN), Proposition 3.4 (exact agreement on finite windows), Lemma 3.5 (extinction or explosion).
- Constant favourable rate: Theorem 1 (formula (4)-(5)); Theorem 2 (fresh start strictly helps); witness (31)-(34) with exact certificates.
- Error size: Theorem 3 (sharp envelope), Proposition 5.1 (supremum 27.3355 points, not attained), Section 5.4 and Table 3 (rate caps; ceiling at ratio 3 below 8.27 points), Section 6 (burn-in, single- and k-founder).
- Random favourable rates: Theorem 4, Corollary 5, Theorem 6 (equilibrium start 1-(E T_B/E T_A)^k), Corollary 7.
- Conjecture status: refuted as stated (fresh start) whenever resident rates vary; exact under the equilibrium start for a constant favourable rate; refuted under the equilibrium start for varied favourable rates.

## Evidence and replay

- [consensus/certify_limits.py](consensus/certify_limits.py) → [certified_limits.json](consensus/certified_limits.json): exact rational, standard library.
- [consensus/evidence/verify_finite_n.py](consensus/evidence/verify_finite_n.py), [multitype_bracket.py](consensus/evidence/multitype_bracket.py), [stationary_identity_and_caps.py](consensus/evidence/stationary_identity_and_caps.py): NumPy/SciPy; outputs beside each script.
- [evidence/run_checks.py](evidence/run_checks.py): replays all four in a temporary copy. [negative_controls.py](negative_controls.py): nine corruptions, each rejected.
- CI: [.github/workflows/replay.yml](.github/workflows/replay.yml). Records: [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), [ENVIRONMENT.txt](ENVIRONMENT.txt). Integrity: [SHA256SUMS](SHA256SUMS).
- The scripts check constants and examples; the limit theorems rest on the written proofs.

## Trust boundary

Internal AI-assisted review only. No peer review, independent reproduction or formal verification. Bounded prior-art search. Multitype values in Section 7.4 are uncertified floating point.
