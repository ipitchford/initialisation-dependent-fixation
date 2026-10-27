# Final editor fixes (27 October 2026)

Applied directly after the verification re-review, the targeted proof audit and the outside-model correctness audit. No new review round. All edits are in `consensus/manuscript.md`; `manuscript.tex` and the PDF (now 28 pages) were regenerated from it with `evidence/build_pdfs.py` (no layout warnings). Every page was inspected as a rendered image. No theorem statement changed in substance; no number in any table changed.

## Claims in the abstract and Section 1.4

| Issue | Fix |
|---|---|
| Rate-cap ceiling at resident-rate ratio 3 called "below 8 points" | Recomputed the ceiling (43) independently (mpmath, 30 digits): 7.772 at b0/a = 1.25, 8.112 at 1.1, 8.257 at 1.01, 8.2688 as b0/a -> 1. Text now says "below 8.27 points", tends to 8.27 as b0/a -> 1, below 8 when b0/a >= 1.25. |
| "About 14 points at ratio 10" | Recomputed: best two-point law attains 13.88 at b0/a = 1.25, 15.30 at 1.1, 16.28 at 1.01, 16.38 at 1.001; the ceiling (43) tends to about 22.52. Text now ties "about 14" to b0/a = 1.25 and says attained values exceed 16 and the ceiling tends to about 22.5 as b0/a -> 1. Ratio-3 attained values (4.86 -> about 5.3) also qualified. |
| Uniform-law "below 3.5 points" | Now names the computed cases (b0/a in {1.25, 2}). |
| Abstract "never overestimates" | Limited to the fresh start stated by the conjecture and the equilibrium start the source simulated; notes that other starts over-representing slow residents can overestimate (Section 4.2). Section 9 given the same qualifier. |
| Section 1.3 | New sentence: the source's Gamma-noise examples have overlapping supports and lie outside the class (Section 5.5). |
| Section 1.4 practical message | "Start in equilibrium or burn in" now restricted to a constant favourable rate; for varied favourable rates only equilibrium residents with fresh founders give the formula (Corollary 7). |

## Proofs

| Item | Fix |
|---|---|
| Lemma 3.2 generality (proof audit GAP; outside-model audit item 1) | State space now standard Borel (measurable diagonal, so sigma is a stopping time). Maps Phi are jointly P x B(E) x B(Theta)-measurable with P the predictable sigma-field. Every accepted atom assigns the image (possibly the same state). Simultaneous atoms excluded outside a null event. Note that m_t = infinity makes (14) trivial. The proof cites these hypotheses for measurability of B_i. |
| Lemma 3.5 (audit item 2) | Construction from independent lifetime clocks and Poisson birth streams stated first; Yule domination gives non-explosion, existence of Z(n) and the strong Markov property. |
| Proposition 5.1 (audit item 3) | Class now "support a compact subset of (a, infinity)", i.e. supp F in [b0, bbar] with a < b0. |
| Burn-in scope (audit item 4) | (45)-(46) stated as single-founder bounds. Added the k-founder bound 0 <= p_k(c_tau) - p_k(c_0) <= k(a/lambda)^(k-1) L D e^(-b0 tau) and the corresponding sufficient burn-in; the worked example (tau ~ 2.01) labelled single-founder. |
| Lemma 7.2 | Localisation plus Fatou for the supermartingale; final step is bounded convergence, not optional stopping. |
| Lemma 7.3 | Root existence stated: g(0+) = lambda m_A > 1 > g(1), g continuous and strictly decreasing. |
| Novelty (audit A-D) | Section 1.6 now says the techniques are standard, Theorem 2 is Brown's renewal monotonicity transferred to fixation, Theorem 6 is a short averaging calculation new for this model but not claimed as a new branching-process theorem, and the Proposition 5.1 envelope has not been compared exhaustively with extremal renewal results. |

## References

- Valentini, Ferrante & Dorigo (2017): article number 9 added (written "4, article 9"). Crossref (queried 27 October 2026) confirms the title, volume 4 and year for DOI 10.3389/frobt.2017.00009; its record has no article-number field, and 9 is the Frontiers article number encoded in that DOI.

## Replay

All four scripts and `evidence/run_checks.py` were rerun from a clean copy with `uv run python3 -I`. No script changed, so `certified_limits.json` and the other stored outputs are unchanged. See `REPLAY_RECEIPT` in the public package.
