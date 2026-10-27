# Assurance boundary

## What was done

1. **Written proofs.** Every theorem is proved in the manuscript ([PDF](consensus/initialisation_dependent_fixation.pdf), source [manuscript.md](consensus/manuscript.md)).
2. **Internal AI-assisted review.** A five-role review of the first version (editor, methodology, domain, perspective and devil's-advocate reviewers) and a correctness review by an AI model from a different family. Every finding has a recorded disposition in [REVISION_RESPONSE.md](REVISION_RESPONSE.md). A verification re-review checked the revision; a targeted proof audit, with an independently written exact finite-population solver and a Monte Carlo check of Theorem 6 on a different law, found every new proof correct with one repairable gap; a second outside-model audit found no counterexample and four repairable gaps. The editor made the final fixes in [FINAL_FIXES.md](FINAL_FIXES.md) without a further review round. [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md) gives a rating-free summary.
3. **Computation.** Exact rational certificates for the witnesses, the global supremum bracket and the Theorem 6 identity; exact finite-population chains for small N; floating evaluations elsewhere, labelled as such. All scripts were replayed from a clean copy and are replayed in CI. Nine semantic negative controls ([negative_controls.py](negative_controls.py)) confirm that the evidence rejects corrupted certificates, false limit values and the superseded rate-cap claims.
4. **Citations.** All 16 DOIs were resolved at doi.org and matched on Crossref by title, first author and year ([CITATION_AUDIT.md](CITATION_AUDIT.md)). Quotations of Conjecture 2 were checked against the published source.

## What was not done

- No human specialist review or journal peer review.
- No independent reproduction by an unaffiliated party.
- No proof-assistant formalisation.
- The prior-art search was bounded ([RESEARCH_GATES.json](RESEARCH_GATES.json)); it is not a claim of historical priority. Theorem 6 and the Proposition 5.1 envelope have not been compared exhaustively with multitype branching (reproductive-value) and extremal renewal literature.
- The multitype values in §7.4 come from an uncertified floating-point ODE solver.

Agreement between AI reviewers is not independent evidence. All review was internal checking.
