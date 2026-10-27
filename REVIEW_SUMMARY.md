# Review summary (rating-free)

All review was internal and AI-assisted. It is not peer review.

1. **First-round review (five roles plus an outside-model correctness review).** Main objections: the finite-time coupling lacked an explicit thinning bound; Theorem 4 needed a vector (type-resolved) coupling; "survival implies divergence" used overlapping intervals; the conjecture had to be quoted and the source's own Section 4.7 discussed; the 27.3-point figure is a non-attained supremum; the bias direction is not universal across starting laws; the ODE values were mislabelled "certified". Every item and its disposition is in [REVISION_RESPONSE.md](REVISION_RESPONSE.md).
2. **Revision.** New Lemma 3.2 (common-thinning coupling), explicit construction (§3.3), Proposition 3.4 for the multiset of favourable rates, Lemma 3.5, Proposition 5.1, Theorem 6 and Corollary 7 (equilibrium start with varied favourable rates), rate-cap Table 3, burn-in Section 6.
3. **Verification re-review.** All required items present; quotes and 16 DOIs verified. Raised: the rate-cap ceiling at ratio 3 was overstated as "below 8 points" (true limit 8.27); "never overestimates" needed restriction to fresh and equilibrium starts; a Gamma-noise scope sentence in §1.3; the practical message for varied favourable rates; an article number.
4. **Targeted proof audit.** Every audited item correct; Lemma 3.2 needed a predictable-measurability hypothesis; wording nits in Lemmas 7.2 and 7.3. An independent exact solver reproduced Tables 4 and 5, and Monte Carlo on a different law agreed with Theorem 6 (and excluded the conjectured value by about 20 standard errors).
5. **Second outside-model audit.** No fatal defect. Repairable: Lemma 3.2 generality (standard Borel space, predictable maps, accepted atoms); Lemma 3.5 construction and non-explosion; Proposition 5.1 class; the burn-in bound controls only the single-founder probability (a k-founder bound was supplied); novelty claims to be narrowed.
6. **Final editor fixes.** All of the above applied; see [FINAL_FIXES.md](FINAL_FIXES.md).

Unresolved and disclosed: overlapping supports, general graphs, the sharp capped envelope, a finite-N rate, non-exponential signalling, uncertified multitype numerics, and an exhaustive comparison with multitype-branching and extremal-renewal literature.
