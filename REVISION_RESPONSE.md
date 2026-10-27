# Revision response: "Initialisation-dependent fixation in noisy weighted voter models"

Single revision round, 27 October 2026. Every finding from the five panel reports and the outside-model review is merged below. Each item is given as **R** (reviewer finding) → **A** (author response and disposition) → **C** (change made, with location in the revised `consensus/manuscript.md` and PDF).

Reviewer IDs: **EIC** = Editor-in-Chief; **METH** = methodology (R1); **DOM** = domain (R2); **PER** = perspective (R3); **DA** = Devil's Advocate; **SOL** = outside-model correctness review (`sol/sol-review.md`); **TASK** = editorial instruction for this round. Dispositions: Accepted, Partly accepted, Declined, or Moved to Open problems.

Section, equation and theorem numbers below refer to the revised manuscript. Theorem 1–4 and Corollary 5 keep their original numbers. The new results are Theorem 6, Corollary 7 and Proposition 5.1. Lemmas and propositions are numbered by section.

---

## A. Correctness

### C1. Formal coupling lemma for Theorem 1
- **R:** The finite-time coupling invokes a common Poisson construction without stating the mismatch estimate. The intensity is adapted to the population history, so an explicit predictable-thinning bound is needed (SOL 1.1; EIC "check §3.2"; TASK).
- **A:** Accepted. The original sketch described aggregate births and deaths through Poisson measures but never built the population from them. Doing so required a new construction.
- **C:** New **Lemma 3.2** (coupling by common thinning, bound (14)) with full proof. New explicit construction in **§3.3** that drives the whole population from resident clocks Π_v, a birth measure Π⁺ and a favourable-update measure Π⁻, together with the "disturbed vertex" bookkeeping (15)–(16). **Proposition 3.4** applies Lemma 3.2 and gives the explicit bound (18) plus the truncation bound (19).

### C2. Explicit vector coupling for Theorem 4
- **R:** Convergence of the scalar count does not give convergence of the type vector. A per-type coupling with child-type marks and favourable-to-favourable redraws is needed (METH M1; SOL 6.1; TASK).
- **A:** Accepted, and done in more generality than asked. Proposition 3.4 couples the full **multiset of favourable rates** for an arbitrary compact favourable law F_A. Finite mixtures are a special case.
- **C:** **Proposition 3.4**. Its mismatch rates are M|S/(N−1) − b_ν| for births (common child-type mark) and ≤ a₊M(M−1)/(N−1) for favourable updates that copy a favourable vertex. Theorem 4 (§7.1) now cites Propositions 3.4 and 3.6, not "the argument is unchanged".

### C3. Stopping-time gap in "survival implies divergence"
- **R:** "Repeated conditioning at successive visits" may use overlapping unit intervals (SOL 6.2; TASK).
- **A:** Accepted.
- **C:** New **Lemma 3.5** uses integer stopping times σ_{ℓ+1} = inf{n ≥ σ_ℓ + 1 : 1 ≤ Z(n) ≤ m₀}, the strong Markov property and P(σ_{ℓ+1} < ∞) ≤ (1 − ε)P(σ_ℓ < ∞).

### C4. Theorem 2 positivity misstated
- **R:** "Strictly positive as an operator" could be read as positivity-preserving. What is needed is a strictly positive quadratic form, via the spectral theorem (METH m2; SOL 2.1; TASK).
- **A:** Accepted.
- **C:** **Theorem 2 proof**, (24)–(26): ⟨φ, P_tφ⟩ = ∫ e^{−ξt} ρ_φ(dξ) with total mass ‖φ‖² > 0. The same representation now drives §5.1 (spectral support in [b₀, ∞)) and §6.

### C5. Missing global-supremum (diagonal) step after Theorem 3
- **R:** The step from fixed (b, λ) to the two-parameter supremum is asserted, not proved (SOL 4.4; TASK).
- **A:** Accepted.
- **C:** New **Proposition 5.1** with proof. The upper bound c_F − (1 − a/λ) < Δ(λ/a − 1) holds for every model, with b₀ = min supp F. The approach is a diagonal sequence b_n ↓ a with Theorem 3 laws. Non-attainment is proved.

### C6. Finite-horizon bracket called "certified"
- **R:** The ODE bracket uses floating solvers and is not a certificate. Either certify it or label it as numerical (EIC m4; METH m9; TASK).
- **A:** Accepted (relabelled). An interval-arithmetic enclosure was not attempted in this round.
- **C:** **§7.4**: "The inequalities (53) are proved. The *values* we report … are numerical, not certified." Table 1 and Table 4 captions mark the numerical entries. The word "certified" now appears only for rational-arithmetic results.

### C7. Unstable 12th decimal (N = 100, fresh)
- **R:** The bundle gives …904 and the replay gives …903 (METH m1; TASK).
- **A:** Accepted (rounded).
- **C:** **Table 5** values are rounded to ten decimals. The caption states that the 11th and 12th decimals vary across library versions. Table 4 is also at ten decimals.

### C8. Stray `.pyc`
- **R:** `consensus/evidence/__pycache__/verify_finite_n.cpython-312.pyc` was shipped and checksummed (METH m8; TASK).
- **A:** Accepted.
- **C:** Removed, with its directory. The new `SHA256SUMS` lists no cache files. `run_checks.py` runs scripts with `-I`, and each staged copy ignores `__pycache__`.

### C9. Rational sub-steps of (34) not checked by script
- **R:** The script checks the three final rational inequalities, but not b(1/10) > 38 or the generating-function value (METH m3).
- **A:** Accepted.
- **C:** `verify_finite_n.py::rational_certificate` now asserts the birth-rate lower bound 1000/59 + (21609/295)·L > 38 and 37/(38 + 36/U) > 370/389. Both steps are explained in §4.3.

### C10. Grid argument and (16) under-written
- **R:** The uniform law of large numbers needs normalisation and a maximal bound. "A count increase marks at most one vertex" needs saying (SOL 1.2; METH m4; DA 8).
- **A:** Accepted.
- **C:** **Lemma 3.3** has a three-step proof: grid law of large numbers, Poisson atom count C_{N,j}, and Lipschitz constant |b_ν′| ≤ b₊(b₊ − b₋). (16) is derived explicitly, including gap atoms of the new construction.

### C11. Pre-ageing monotonicity step implicit
- **R:** That c_τ is strictly decreasing needs one line (EIC m3).
- **A:** Accepted.
- **C:** **§6** first paragraph: I_{ν_τ}(t) = γt + ∫_τ^{τ+t} χ, with χ′ < 0 from (26).

### C12. Tighter derivative bound in pre-ageing
- **R:** aδ/λ² is tighter than 1/4 (DA 7).
- **A:** Accepted, with the correct case split. The derivative is at most aγ/λ² when γ ≥ a, and 1/4 otherwise.
- **C:** (45)–(46). The witness burn-in is now τ ≥ ½ log 55.6 ≈ 2.01 (was 2.07).

### C13. Scope of the bias direction
- **R:** The direction is not universal for arbitrary ν. The abstract must keep "fresh" (SOL 2.3).
- **A:** Accepted.
- **C:** §4.2 says explicitly that starts over-representing slow residents make the formula an *overestimate*. The "practical message" (§1.4) is restricted to fresh and equilibrium starts.

### C14. Terminology for Q^{(T,z)}
- **R:** Do not reuse extinction notation for generating functions with terminal value z (SOL 8).
- **A:** Accepted.
- **C:** **Lemma 7.1** defines Q^{(T,z)}_s(x) = E[z^{Z(T)}], with e^{(T)} = Q^{(T,0)}. It proves the integral form (47) and derives the ODE (48) from it, so (48) no longer rests on "conditioning on the first event".

### C15. Formal clock construction for Corollary 5
- **R:** Specify common clocks recursively (SOL 7).
- **A:** Accepted.
- **C:** **Corollary 5 proof** has per-individual lifetime, baseline stream (rate λ), extra stream (intensity χ) and child-type marks. It includes genealogical inclusion and the strictness event, with the subtree bound from new **Lemma 7.2**.

### C16. Uniform separation not uniform near the supremum
- **R:** The supremum needs b ↓ a, so ρ → 1 (METH m6; DA strongest counter-argument).
- **A:** Accepted.
- **C:** §5.3 paragraph after (41).

---

## B. Framing and fidelity to the source

### F1. Quote Conjecture 2 verbatim
- **R:** Fidelity is asserted, not shown. Quote the conjecture and the model rule, and state admissibility of the witness (EIC M1; METH M2; DA 1; SOL 13; TASK).
- **A:** Partly accepted. The source is copyrighted. We do not reproduce the full ~150-word statement. Instead we quote its load-bearing clauses verbatim, each short, with page numbers: "with initial values of T_A and T_B sampled as above" (p. 187); "even if the opinion did not change" (p. 175); "signals the chosen opinion for the corresponding length of time" (p. 186). We then restate every clause formally in our notation. The text was taken from the source PDF obtained by the domain reviewer (`scratch-domain/src.pdf`).
- **C:** New **§2.3 "Conjecture 2, restated"** (model, betterness, initialisation and prediction, with pages), the admissibility paragraph and the redraw-rule quote in §2.1.

### F2. Discuss the source's §4.7
- **R:** The source flagged the fresh-versus-steady-state subtlety and simulated under size-biased initialisation. The paper should confirm the prediction under that start and refute it under the stated start (DOM M1; PER P1; TASK).
- **A:** Accepted, and strengthened by the extension (X1). Under the simulated equilibrium start the prediction is exact for a constant favourable rate. It fails for varied favourable rates (Corollary 7). The contribution is now called a *resolution*.
- **C:** New **§1.3**, with a verbatim quote from p. 202–203. Also equation (7), Table 1, the subtitle and §9 "What is resolved" and "Fair reading of the source".

### F3. Lead with the varied-favourable-rate counterexample
- **R:** A constant favourable rate could be called degenerate. Promote 0.7842 vs (3+√37)/12 ≈ 0.7569 (EIC M1(iii); DA 1; TASK).
- **A:** Accepted.
- **C:** Abstract, §1.4 item 2 (varied-rate witness first) and **Table 1** (all four starts for that example).

### F4. 27.3 points as a non-attained supremum; table at realistic caps
- **R:** It is a non-attained triple limit and should not be oversold. Add realistic regimes (DA 2; PER §3, P2, ext 4; TASK).
- **A:** Accepted. The new numbers showed that my first-draft phrase "a few points under realistic caps" was too strong for extreme two-point laws, so the text reports the numbers as computed.
- **C:** Abstract and §1.4 item 4 say "supremum … which no single model attains". New **§5.4** has the Bhatia–Davis ceiling (43) and **Table 3**: best two-point law, uniform law and proved ceiling for b₀/a ∈ {1.25, 2} and b̄/b₀ ∈ {2, 3, 10, 100}. With ratio ≤ 3 the ceiling is < 8 points. Uniform laws give ≤ 3.5 points. Ratio 10 allows up to ~14 points for extreme two-point laws.

### F5. Detectability at 1000 runs
- **R:** Note that the 3.5-point gap is not detectable at 1000 simulation runs (DOM m1; TASK).
- **A:** Partly accepted. The literal claim is not accurate. At p ≈ 0.7, 1000 runs give a standard error of 1.45 points, so 3.5 points is about 2.4 SE. A dedicated 5%-level test would detect it with probability about two thirds. The claim that does hold is that it is marginal, and invisible by eye on a plotted curve. More fundamentally, the source simulated the equilibrium start, where the constant-rate gap is exactly zero.
- **C:** New **§5.5**.

### F6. Notation map to the source
- **R:** Map F, μ, λ to F_B, G_B, eq. (6) (DOM m2; TASK).
- **A:** Accepted.
- **C:** **Table 2** (§2.2).

### F7. Complete-graph scope
- **R:** State it explicitly (DOM m5; PER §3; TASK).
- **A:** Accepted.
- **C:** "Scope" paragraph in §2.3, opening sentence of §1.4, and open problem 2.

### F8. Abstract scope (compact, separated supports)
- **R:** "Every nondegenerate mixture" and "arbitrary distributions" omit compact support strictly above the favourable rate (EIC m1; SOL 1.5; DA 10).
- **A:** Accepted.
- **C:** Abstract ("When rates are bounded and every favourable rate lies strictly below every resident rate"), §1.4 preamble and §2.3 Scope.

### F9. Broader lesson; cross-disciplinary context
- **R:** Make explicit the general message about equilibrium approximations used from fresh starts and the inspection paradox. Add the links to population genetics (burn-in), epidemics and bursty networks, ageing voter models, swarm best-of-n, and Monte Carlo warm-up (EIC M2; PER §2; TASK).
- **A:** Accepted. Six references were added, each verified on Crossref.
- **C:** **§1.2** (inspection paradox), **§1.5** "The broader lesson", §9 "The general lesson". New references: Pal et al. 2022, Karsai et al. 2011, Stark et al. 2008, Fernández-Gracia et al. 2011, Valentini et al. 2017, White 1997.

### F10. Novelty positioning and standard references
- **R:** Cite standard branching-approximation and density-dependent Markov-chain sources. Isolate what is new. Note that (35) is the renewal constant, (40) is Bhatia–Davis and the global constant is an elementary corollary (SOL 9–12; DA 4; DOM m4).
- **A:** Accepted. For DOM m4 this is partial: generalised-Moran fixation references were not added.
- **C:** **§1.6** (bullet list of classical ingredients, with Athreya–Ney 1972 and Ethier–Kurtz 1986 added, and an explicit four-item list of what is new). Bhatia–Davis is named at (42). §4.1 credits Brown (1980) for renewal monotonicity.

### F11. Remark on a redraw-only-on-switch variant
- **R:** Say what changes if redraws happen only on an opinion switch (METH M2).
- **A:** Accepted as a brief heuristic remark. The source's rule is confirmed verbatim, so this variant is outside scope.
- **C:** Paragraph in §2.1.

### F12. Finite-N context (N = 200 gaps, observed rate)
- **R:** Add gaps to the limit and an observed rate (EIC m7; PER §3).
- **A:** Accepted. The rate is reported as observed, not proved.
- **C:** **Table 5** gap columns. The text notes that doubling N halves the gaps, consistent with O(1/N), and that this is not proved. Figure 1 caption: "the gap is already visible at N ≈ 10".

### F13. Erratum or prior correction check
- **R:** Check for an erratum or later version before submission (PER P1).
- **A:** Accepted. On 27 October 2026, Crossref listed no update, correction or citing work for DOI 10.1007/s11721-025-00248-z (`is-referenced-by-count` 0; no `updated-by`). Its only relation is a 2023 Research Square preprint.
- **C:** None needed in the text.

### F14. Definition of b in §5; must b lie in the support?
- **R:** b is reused for a lower bound. Theorem 3 needs mass at b (EIC m2; METH m5; DA 5).
- **A:** Accepted.
- **C:** Renamed **b₀**, any number with a < b₀ ≤ b₋ (§5 preamble). The extremal family (39) puts mass at b₀. Proposition 5.1 uses b₀ = min supp F.

### F15. Physical meaning of R → ∞
- **R:** Unbounded rates are unphysical for robots, so the finite-cap bound is the relevant one (PER P2).
- **A:** Accepted.
- **C:** §5.3 closing paragraph and §5.4.

---

## C. Readability

### D1. Plain "why it fails" paragraph in the Introduction
- **R:** No intuition before the formalism (PER R1; TASK).
- **A:** Accepted.
- **C:** New **§1.2** with the rates-2-and-6 example: fresh mean 4, equilibrium mean 3, relaxation 3 + e^{−4t}, and three quarters slow at equilibrium.

### D2. Roadmap and signposts
- **R:** No roadmap. Headline results are not separated from technical ones (PER R3; TASK).
- **A:** Accepted.
- **C:** New **§1.7 Roadmap**. §1.4 lists the main results. §3 opens with "can be skipped on a first reading" and a two-part plan. §7 opens with a section plan.

### D3. Symbol reuse
- **R:** q, b, t, C, K, δ, d, s and g were each overloaded (PER R4; EIC m2; TASK).
- **A:** Accepted.
- **C:** Renamings:
  - q → **ρ** (fixation ratio), and q_i → **e_s(x)** (extinction probabilities);
  - δ = λ − a → **γ**; δ_N, β_N → **β_N^±**;
  - g(r) → **φ**; g_N → **w_N**; global gap g(t) → **Δ(ξ)**;
  - t in (42) → **ξ**; K(t) → **Φ**; h(t) → **Ω**;
  - b (§5) → **b₀**; finite cap B → **b̄**;
  - C → **C_p** / C_θ; η → **ω**;
  - d(t) → **χ(t)**, with cumulative **D(t)**;
  - two-rate r, s → **r₁, r₂**; generating-function argument s → **w**;
  - A_ν(t) → **I_ν(t)**; M in the Theorem 4 proof → **m₀**.

  The letter A is now only the opinion.

### D4. Lower rate means better option
- **R:** "Lower rate = better" is counter-intuitive (PER R2).
- **A:** Accepted.
- **C:** §1.1 (mean signalling time T = 1/R) and §2.1 last paragraph.

### D5. Practical message
- **R:** The stationary formula is *conservative*; say so in those words (PER §3, R5; TASK).
- **A:** Accepted, within the stated scope.
- **C:** Abstract and **§1.4 "The practical message"**, with the burn-in use for experimenters (§6 last paragraph).

### D6. Figure captions
- **R:** Say what the reader should notice and identify the curves (PER R6).
- **A:** Accepted.
- **C:** Figure 1 and Figure 2 captions. The Figure 2 annotation now reads "Supremum, not attained", and its axis uses ξ.

### D7. Defensive sentences
- **R:** Referee-style sentences interrupt the flow (PER R7).
- **A:** Partly accepted. Most were removed or rewritten as plain statements. The order-of-limits remark is kept, because a reviewer specifically checked it.
- **C:** §3.4 last paragraph and §3.5.

### D8. Paths and "evidence file" in the body
- **R:** Use supplementary-material references with a persistent identifier (PER R8; METH m7).
- **A:** Partly accepted. No persistent identifier exists yet. Body text now names scripts only where a reader needs them, and the Declarations list them once. The README path problem (METH m7) is fixed: `README.md` now sits at the bundle root.
- **C:** Declarations, "Data and code availability", and the new `README.md`.

### D9. Hard-coded section numbers and manual tags
- **R:** Use theorem environments and \label/\ref (EIC m6; PER R9).
- **A:** Declined for this round. The Pandoc-Markdown source is kept. All numbers were checked by hand against the rendered PDF.
- **C:** None.

---

## D. Hygiene

### H1. AI provenance in a Declarations section
- **R:** The author field was empty and the provenance appeared only in the README (EIC m5; TASK).
- **A:** Accepted.
- **C:** New **Declarations** section (Author, AI provenance, Data and code availability, Competing interests and funding).

### H2. Author "Anonymous"
- **R:** TASK.
- **A:** Accepted.
- **C:** YAML front matter `author: "Anonymous"`. The running header now shows the short title, not "Research mathematics".

### H3. Remove research-assessment rating language from shipped files
- **R:** TASK.
- **A:** Accepted.
- **C:** `novelty_report.md` §7 sentence reworded. The original README and the review PDFs, which carried ratings, are not part of this bundle. A case-insensitive search of every shipped text file for assessment-exercise names and rating notation returns nothing.

### H4. Issue number for Ganesh et al.
- **R:** Crossref gives issue 3 (DOM m3; TASK).
- **A:** Accepted.
- **C:** *Swarm Intelligence, 19*(3), 173–214. Issue numbers were also added for Jafarpour et al. (108(3)), Fernández-Gracia et al., Karsai et al., Stark et al. and Pal et al., from Crossref.

### H5. Verify every citation
- **R:** TASK: via Crossref or doi.org; never write a DOI from memory.
- **A:** Accepted.
- **C:** All 16 DOIs were resolved against `api.crossref.org/works/<DOI>`, and titles, authors, venues, volumes, issues and pages were compared with the reference list. One correction: White (1997) carries no "Jr." in Crossref.

---

## E. Extensions

### X1. Random favourable rates (proved; included)
- **R:** Random favourable types, initialised fresh or size-biased, covering the source's §4.7 set-up (DOM ext 1). Also a general, non-finite favourable law in Theorem 4 (EIC ext 4) (TASK: one extension, included only if completely proved).
- **A:** Accepted and proved.
- **C:**
  - **Theorem 4** now holds for any compact favourable law F_A and any initial favourable law ν^A (via Propositions 3.4 and 3.6).
  - New **Lemma 7.1**: backward integral equation (47) and ODE (48).
  - New **Lemma 7.2**: uniform survival bound ρ^m.
  - New **Lemma 7.3**: equilibrium residents give e(x) = x/(x + λc\*), recovering the source's Theorem 5 in our class.
  - New **Theorem 6**: from the equilibrium start, lim α_k = 1 − (E T_B / E T_A)^k, the mean-quality formula.
  - New **Corollary 7**: under the simulated start the conjectured value is strictly too small whenever F_A is non-degenerate.
  - Evidence: the new script `consensus/evidence/stationary_identity_and_caps.py`. Its exact rational certification covers the identity and strict inequality for four laws, with the witness value exactly 7/9 and conjecture value (3+√37)/12. It also gives an exact (N ≤ 5) and floating (N ≤ 100) multitype finite-population chain under all four starts (Table 4).

### X2. Sharp envelope under a finite rate cap
- **R:** Prove two-point extremality or a sharp finite-cap bound (PER ext 1; DA 6; TASK option).
- **A:** Moved to Open problems. Table 3 brackets the extremum between attained two-point values and the proved ceiling (43).
- **C:** §9 open problem 3.

### X3. Overlapping favourable and resident supports
- **R:** EIC ext 1; METH ext 3; DOM ext 3; DA 3; TASK option.
- **A:** Moved to Open problems. Lemma 3.1 fails, and no substitute bridge from survival to fixation was found.
- **C:** §9 open problem 1; scope stated in the abstract, §1.4 and §2.3.

### X4. Non-complete graphs; sparse-graph simulation
- **R:** EIC ext 2; METH ext 4; PER ext 2; DOM ext 2 (Gamma-noise simulation).
- **A:** Moved to Open problems. Simulations were declined: the paper uses no stochastic simulation, and the source's Gamma-noise regime has overlapping supports, outside the theory.
- **C:** §9 open problem 2.

### X5. Finite-N error rate
- **R:** EIC ext 3; METH ext 2; DA.
- **A:** Moved to Open problems. Observed O(1/N) behaviour is reported without proof.
- **C:** §8 after Table 5; §9 open problem 4.

### X6. Certified multitype example
- **R:** Interval-arithmetic integration of (48) (METH ext 1, m9; EIC m4).
- **A:** Not done this round; the values are labelled numerical (C6). The equilibrium-resident multitype values are now exact closed forms.
- **C:** §7.4.

### X7. Non-exponential signalling and sign reversal
- **R:** PER ext 3.
- **A:** Moved to Open problems.
- **C:** §9 open problem 5.

---

## F. Editor questions

- **EIC Q1** (is a constant a admissible?): Yes. The answer is given in §2.3, and the varied-rate witness (F3) makes the question moot.
- **EIC Q2** (an initialisation between fresh and equilibrium?): The burn-in family ν_τ = FP_τ of §6 interpolates monotonically. The two-phase classification in §4.2 covers every other start.

## Verification of this revision

- All four scripts were rerun from a clean copy with `uv run --no-project [--with numpy --with scipy] python3 -I`, and `evidence/run_checks.py` passed. The rational and exact outputs were identical to the stored references.
- The PDF was rebuilt with Pandoc and TinyTeX XeLaTeX, with no overfull boxes or missing characters. All 26 pages were rendered and inspected.
