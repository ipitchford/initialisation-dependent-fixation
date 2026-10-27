# Formula-first novelty and object-identity audit

**Audit date:** 19 October 2026.  
**Target:** Conjecture 2 in Ganesh, Hauert and Valla (2025), and the corrected fixation theorem and sharp initialisation-error envelope in the accompanying manuscript.  
**Status:** A precise published conjecture is contradicted by the proved examples. No prior statement of the replacement theorem or sharp fixation envelope was found within the searches recorded below. That bounded search finding is not a certificate of historical priority.

## 1. Scope and decision

The contribution is a correction to a specified population process. For a constant favourable update rate \(a\), resident reset-rate law \(F\), initial resident-rate law \(\nu\), and fixed number \(k\) of favourable founders, the manuscript proves

\[
\lim_{N\to\infty}\alpha_k(N;\nu)=1-(1-c_\nu)^k,\qquad
c_\nu=\left[1+a\int_0^\infty
\exp\!\left(-\int_0^t[b_\nu(s)-a]\,ds\right)dt\right]^{-1},
\]

where \(b_\nu(t)\) is the mean rate of the independent resident reset process started from \(\nu\). Resident rates have compact support strictly above \(a\). A further theorem allows finite favourable-rate mixtures, still with separated supports.

The source conjecture uses stationary birth intensity
\(\lambda=(\mathbb E_F[1/R])^{-1}\), although its initial resident rates are sampled freshly from \(F\). For every nondegenerate \(F\) in the proved class, fresh initialisation gives \(c_F>1-a/\lambda\). The distinction is therefore not a negligible correction that vanishes as the population grows.

The formula for survival in a deterministic time-dependent birth–death process is classical. The equilibrium rate bias, two-exponential renewal calculation, monotonicity of the renewal density and integrated renewal excess also have classical antecedents. General dependence of invasion on age structure is established prior art. These facts are explicitly credited, and none is presented as an independent discovery.

The search gate therefore gives the following decisions.

| Contribution unit | Decision | Reason |
|---|---|---|
| Time-dependent branching survival formula | Existing object; no novelty claim | Kendall (1948), and its use in fixation by Uecker and Hermisson (2011) |
| Two-rate resident renewal intensity | Existing object; no novelty claim | A two-phase renewal calculation, also a rank-one perturbation of a diagonal generator |
| Fresh renewal intensity is decreasing to equilibrium | Existing principle; no novelty claim | Mixtures of exponentials have decreasing failure rate; Brown's renewal-monotonicity work is relevant |
| Initial age structure can affect fixation | Existing observation; no novelty claim | Shpak (2007), Jafarpour et al. (2023), and related life-history models |
| Exact correction of the specified reset-and-copy model, with finite-population justification | Clear to prove, subject to bounded prior-art uncertainty | The source explicitly labels its different limit as a conjecture; no later correction was located |
| Strict fresh-versus-stationary direction for the entire separated resident class | Clear to prove, subject to bounded prior-art uncertainty | Combines the identified population limit with a classical renewal property; no matching model-specific theorem was found |
| Sharp fixation envelope and global \(27.33554343215\)-percentage-point supremum | Clear to prove, subject to bounded prior-art uncertainty | The renewal moment estimate is classical in form; the resulting extremal fixation functional and sharp family were not located |
| Finite support and pre-ageing bounds | Consequences of the proved functional, with no claim of optimality for fixed upper support | The finite-support variance bound and spectral decay estimate are elementary ingredients |
| Exact finite-\(N\) certificates | Independent verification artefacts | They verify examples and generator construction; they are not substitutes for the limit proof |

“Clear to prove” means that no identity collision in this audit prevents proceeding with the specified theorem. It does not mean that all possible historical sources have been excluded.

## 2. Exact source identity and quantifiers

Ganesh, Hauert and Valla, *Consensus in the weighted voter model with noise-free and noisy observations*, Swarm Intelligence 19, 173–214 (2025), DOI [10.1007/s11721-025-00248-z](https://doi.org/10.1007/s11721-025-00248-z).

Full text: [Springer](https://link.springer.com/article/10.1007/s11721-025-00248-z), [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12327191/).

The following passages were inspected.

| Locator | Source fact relevant to identity |
|---|---|
| Section 1.1, formal model | An agent's measured quality is the mean of its exponential advertising time. It resamples quality after updating, including an update that preserves its opinion. |
| Section 3, definitions of \(T_A,T_B,R_A,R_B\) | The random rate is the reciprocal of measured quality; the holding time is conditionally exponential. |
| Equations (5)–(6) | The resident-rate distribution used for the branching approximation is biased by inverse rate, and its total intensity is the harmonic mean \(\lambda\). |
| Conjecture 2 | Initial quality samples are fresh; \(k\) is fixed as \(N\) grows; the graph is complete. The claimed limit is the survival probability of a branching process with constant birth intensity \(\lambda\). |
| Theorem 5, equation (7) | The stationary branching process itself has a correct fixed-point description. Its solution does not establish the population approximation under fresh resident initialisation. |

The wording of the conjecture abbreviates the signalling-time description. The surrounding formal model specifies conditionally exponential times, and the manuscript uses that model consistently. It does not substitute deterministic signalling durations.

The counterexample uses a constant favourable rate and two resident rates. Thus all quality moments exist, the favourable mean signalling time is strictly longer, and the example satisfies stronger support separation than the source requires.

## 3. Normalisation, finite fingerprints and invariants

All rates may be multiplied by one positive constant without changing fixation. The principal witness is normalised to
\(a=1\), \(F=(\delta_2+\delta_6)/2\), and fresh initialisation.

The resident generator, with column vectors for probability distributions, is

\[
K=\begin{pmatrix}-1&3\\1&-3\end{pmatrix}.
\]

Its rank is one, trace is \(-4\), determinant is zero, characteristic polynomial is \(z(z+4)\), and equilibrium distribution is \((3/4,1/4)\). The intensity is

\[
b_F(t)=3+e^{-4t},\qquad
\widehat b_F(z)=\frac3z+\frac1{z+4}
=\frac{4(z+3)}{z(z+4)}.
\]

Its derivatives at zero are
\(4,-4,16,-64,256,-1024,4096,\ldots\).
The constant-plus-exponential form is a classical two-phase renewal identity, not evidence of a new renewal theorem.

The exact fresh one-founder fixation values are:

| \(N\) | Exact value |
|---:|---:|
| 2 | \(16/21\) |
| 3 | \(2864/4051\) |
| 4 | \(443968/639901\) |
| 5 | \(310846319872/449354284245\) |

The transient count-state sizes for \(N=2,\ldots,7\) are
\(2,5,9,14,20,27\), with formula \((N-1)(N+2)/2\).
An OEIS search returned the familiar triangular-number-related sequence, including a row of A059797 and the A000096 reference in A285192. This collision is expected and carries no novelty: it simply counts the chosen states.

The first two exact fixation fractions were searched together. No matching fixation result was returned. This is only a fingerprint check. Fractions, phase labels, choice of time scale and complete-graph aggregation can disguise an equivalent result.

The exact \(N=2,3\) killed generators are recorded in target.yaml. The verification JSON contains exact rational solutions and zero residuals for every harmonic equation for \(N=2,3,4,5\), for both the principal witness and \(F=0.1\delta_2+0.9\delta_{100}\). A separately constructed labelled-vertex chain checks the count-chain interpretation for \(N=2,3,4\). Larger deterministic sparse solves are explicitly labelled floating-point calculations.

## 4. Formula and model alias audit

The formula-first gate was rerun after reducing the resident dynamics to a reversible reset process, after reducing the two-rate case to one decaying exponential, and after expressing the upper bound through the renewal excess.

| Current object | Equivalent descriptions searched | Collision or boundary |
|---|---|---|
| Reset chain \(Lf(r)=r(\int f\,dF-f(r))\) | Renewal process with hyperexponential lifetimes; phase-type renewal process; state-dependent stochastic resetting; rank-one generator perturbation | Standard representation. A reset to the same phase is still a renewal but is invisible as a state transition. |
| Population update rule | Weighted voter model; death–birth Moran process with renewed update rates; non-Markovian voter model; age-dependent opinion dynamics; annealed rate disorder | Birth-driven models with random expulsion are not automatically identical. Here the receiving vertex's clock triggers copying, and its rate is redrawn from the copied opinion's law. |
| Rare favourable lineage | Branching process in a varying environment; time-inhomogeneous linear birth–death process | Classical branching law. The contribution is identification of the correct resident-driven birth intensity and a population fixation limit. |
| \(b_F-\lambda\) | Equilibrium covariance under a reversible semigroup; completely monotone renewal-density excess; decreasing-failure-rate renewal process | Classical monotonicity principle. The manuscript includes a direct proof specialised to the reset chain. |
| \(D=\int_0^\infty(b_F-\lambda)\) | Renewal-function constant; integrated renewal-density excess; squared coefficient of variation of \(1/R\) | A standard renewal-moment quantity. No claim that the moment identity itself is new. |
| \(c_F\le\delta/(\delta+a e^{-D})\) | Early birth burst; fixation under a transient environment; extremal renewal functionals | Burst–death literature changes offspring bursts and generation times. No exact matching sharp bound for this process was found. |
| \(g(t)=t/(t+e^{-t})-t/(1+t)\) | Maximum error of stationary fixation; harmonic-mean fixation approximation; sharp initialisation envelope | No matching extremal expression was located by exact-form and semantic searches. |

The gate's mandatory worked example, involving a purported new combinatorial identity that was already a classical identity under another normalisation, informed this audit. Matching a sequence or transform was treated as an object-identity warning, not dismissed because the application vocabulary differed.

## 5. Nearest literature and passage-level comparison

### Classical varying-environment branching

Kendall, D. G. (1948). *On the generalized “birth-and-death” process*. Annals of Mathematical Statistics, 19(1), 1–15. [DOI](https://doi.org/10.1214/aoms/1177730285).

Uecker, H., & Hermisson, J. (2011). *On the fixation process of a beneficial mutation in a variable environment*. Genetics, 188(4), 915–930. [DOI](https://doi.org/10.1534/genetics.110.124297); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3176092/).

The indexed primary full text of Uecker and Hermisson was inspected around its time-dependent birth and death rates, forward equations and fixation integral, equations (7)–(16). It explicitly attributes the general time-inhomogeneous linear birth–death formalism to Kendall. Some subsequent direct PMC opens produced a sign-in or bot-check page. The original Kendall article was not fully replayed in this audit. The manuscript does not rely on a hidden formula from that source: it verifies its generating function and initial condition directly.

The identification of \(b_\nu(t)\) from a freshly initialised resident population, and its use to prove an exact large-\(N\) fixation limit for the stated copying model, are additional steps beyond the branching formula.

### Renewal monotonicity

Brown, M. (1980). *Bounds, inequalities, and monotonicity properties for some specialized renewal processes*. Annals of Probability, 8(2), 227–240. [DOI](https://doi.org/10.1214/aop/1176994773).

Brown, M. (1981). *Further monotonicity properties for specialized renewal processes*. Annals of Probability, 9(5), 891–895. [Primary publisher archive](https://www.jstor.org/stable/2243747).

The 1980 bibliographic identity was checked; its original full text was not available through the inspected routes. Indexed material and the primary 1981 abstract identify concavity of the renewal function for decreasing-failure-rate interarrival distributions as established work. The manuscript consequently credits the renewal-monotonicity background and proves the needed special case itself by reversibility. It does not claim to reproduce every hypothesis or the strongest theorem in Brown (1980).

### Age structure and non-exponential generation times

Shpak, M. (2007). *Selection against demographic stochasticity in age-structured populations*. Genetics, 177(4), 2181–2194. [DOI](https://doi.org/10.1534/genetics.107.080747); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2219467/).

The discussion of initial versus stable age structure provides prior context for initialisation effects. This work concerns age-structured demographic models and diffusion approximations. An erratum is indexed in Genetics 195(2), 623 (2013); its quantitative corrections were not used. The manuscript's reference is confined to the prior existence of the age-structure issue.

Jafarpour, F., Levien, E., & Amir, A. (2023). *Evolutionary dynamics in non-Markovian models of microbial populations*. Physical Review E, 108, 034402. [DOI](https://doi.org/10.1103/PhysRevE.108.034402); [accepted full manuscript](https://link.aps.org/accepted/10.1103/PhysRevE.108.034402); [repository PDF](https://dspace.library.uu.nl/bitstream/handle/1874/435133/PhysRevE.108.034402.pdf?sequence=1).

The full manuscript was inspected, especially the model and early invasion discussion. Division triggers birth followed by removal from a fixed population. Transient mutant division rates can determine fate. This directly blocks a claim to the first discovery that non-Markovian transients affect fixation. It differs from the receiving-vertex update rule of the target, and it does not establish the stated fresh-resident correction or the envelope found here.

Hubbarde, J. E., Wild, G., & Wahl, L. M. (2007). *Fixation probabilities when generation times are variable: The burst–death model*. Genetics, 176(3), 1703–1712. [DOI](https://doi.org/10.1534/genetics.107.072009); [publisher](https://academic.oup.com/genetics/article/176/3/1703/6062224).

The primary abstract describes exponential generation times with offspring produced in bursts. It is an important alias collision for broad statements about bursts and fixation. A birth burst caused by an initially fresh resident clock population is a different mechanism. No assertion of historical priority for the general life-history effect is made.

Alexandre, A., Abbara, A., Fruet, C., Loverdo, C., & Bitbol, A.-F. (2025). *Bridging Wright–Fisher and Moran models*. Journal of Theoretical Biology, 599, 112030. [DOI](https://doi.org/10.1016/j.jtbi.2024.112030); [arXiv](https://arxiv.org/abs/2407.12560).

The primary manuscript's renewal discussion distinguishes transient update probabilities from their asymptotic values, including equation (37). The process uses discrete partial replacement and is developed through a different population approximation. The general transient-versus-asymptotic distinction is therefore prior art; no identical fixation theorem was found there.

## 6. Reproducible search log

The queries below were run through a live public web and full-text index on 19 October 2026. Queries were grouped in batches, with adaptive follow-up to primary sources. Search-result absence is not interpreted as proof of nonexistence.

### Source identification, status and exact model

    "conjecture" "2025" "consensus" "matrix"
    "weighted voter" "Conjecture 1" error probability
    "Ganesh" "Hauert" "Valla" conjecture counterexample
    "weighted voter model" "conjecture" -"noisy observations" -site:researchgate.net
    "weighted voter" "error" "N_1+N_2"
    "Ganesh" "Hauert" "Valla" "Conjecture 2"
    "weighted voter" "renewal" "fixation"
    "noisy weighted voter" "initial" "equilibrium"
    "Ganesh" "Valla" "conjecture" -site:link.springer.com -site:pmc.ncbi.nlm.nih.gov -site:researchgate.net
    "weighted voter" "initialisation" "conjecture"
    "noisy weighted voter" conjecture counterexample

These searches located the published conjecture and related copies of its paper. No later resolution of Conjecture 2 was located.

### Population-process and branching aliases

    "Moran" "non-exponential" "fixation" lifetime
    "Moran" "renewal" "branching" fixation transient
    "age-dependent" "voter model" "fixation"
    "Moran process" "non-exponential"
    "voter model" "renewal" "fixation"
    "fixation" "initial age" branching
    "fixation probability" "time-dependent" "birth" "death"
    "renewal" "Moran" "lifetimes"
    "non-Markovian" "Moran" "fixation"
    "voter model" "renewal processes" initial
    "mutation" "fixation" "non-exponential" lifetime
    "Evolutionary dynamics in non-Markovian models" "2023"
    "Bridging Wright–Fisher and Moran models" authors
    "fixation" "resident" "initial distribution" "age"
    "Selection Against Demographic Stochasticity" "initial" age
    site:pmc.ncbi.nlm.nih.gov/articles/PMC2219467/ "initial" "age"

These searches produced the varying-environment and age-structured prior art discussed above. They ruled out broad novelty claims about time-dependent branching or initial age effects.

### Renewal reduction and exact fingerprints

    "renewal density" "mixture of exponentials" decreasing
    "stochastic resetting" "state-dependent" "stationary" "rate"
    "weighted voter" "2" "6" "fixation"
    "renewal density" "completely monotone" mixture
    "renewal density" "decreasing" "exponential" Brown
    "renewal" "DFR" "density" monotone
    "3+e" "renewal" density
    "3+exp(-4t)" renewal
    "2, 5, 9, 14, 20, 27" OEIS
    "16/21" "2864/4051"
    "Bounds, Inequalities, and Monotonicity Properties" Brown 1980 pdf
    "Bounds, Inequalities, and Monotonicity Properties" "decreasing failure"
    "Kendall" "1948" "generalized birth-and-death process"
    "Uecker" "Hermisson" "2011" "915" "doi"

The renewal reduction is a known object. The count sequence is also known. No exact matching fixation fraction pair was returned.

### Sharp-envelope rerun

    "fixation probability" "burst" "renewal"
    "renewal" "excess" "coefficient of variation" "mixture"
    "fixation" "t+e" probability
    "renewal density" "integral" "variance"
    "fixation" "initialisation" "renewal" "Ganesh"
    "fixation" "t/(t" "e" "envelope"
    "t/(t+exp(-t))" fixation
    "lambda/b" "fixation" "renewal"
    "fixation" "harmonic mean" "initial" voter

The burst–death literature was an important semantic near match, but the inspected model is different. No matching sharp envelope or extremising two-rate construction was returned.

## 7. Remaining uncertainty and publication wording

The audit did not include a complete citation graph from MathSciNet, zbMATH, Scopus or Web of Science, and no author correspondence was sent. Public web indexes do not cover all full texts, theses or recent manuscripts. The original Kendall and Brown papers were not fully inspected. Direct access to some PMC pages was intermittent. The Shpak erratum was not used for any quantitative claim. These limits should accompany any claim of priority.

The defensible wording is: “We disprove Conjecture 2 under the initialisation stated in Ganesh et al. (2025), prove a corrected limit for separated supports, and establish a sharp envelope for the resulting single-founder initialisation error.” It is not defensible to call the birth–death integral, decreasing renewal intensity, inverse-rate equilibrium bias or broad effect of age structure new discoveries.

The source paper's equilibrium branching theorem is not contradicted. The manuscript identifies the additional initialisation assumption needed for that branching process to govern this population limit. It neither resolves arbitrary overlapping supports nor claims that a fixed finite upper rate range attains the global supremum.

The deliverable is a research draft with self-contained proofs and independently checkable arithmetic. Its novelty and significance remain matters for expert review; the exact counterexample and theorem do not depend on any such assessment.

## 8. Final multitype strict-comparison corollary

The last addition applies the existing strict inequality $b_F(t)>\lambda$ to the finite favourable-type theorem. A common-clock branching coupling orders the survival events. A founder who dies childless in the stationary process can nevertheless have a surviving extra child in the fresh process, giving a strictly positive, explicit lower bound on the difference. This identifies the argument as a classical monotone coupling with a positive-probability separating event; it is not a new coupling principle or a separate claim about arbitrary multitype processes.

The formula-first identity check remains within the same source-model contribution. Two final targeted web searches on 19 October 2026 were:

    "Ganesh" "Valla" "fixation" "multitype" initialisation
    "noisy weighted voter" "fresh" "equilibrium" conjecture

The returned relevant primary material was the originating 2025 paper, including Conjecture 2 and its equilibrium branching Theorem 5. No matching correction was located in this small additional check. This does not expand the priority guarantee beyond the limitations in Section 7. The corollary was separately audited for the correct shared-clock construction and the distinction between the founder's potential baseline clock and all descendant clocks.
