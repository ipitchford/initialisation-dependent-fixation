# Initialisation-dependent fixation in the noisy weighted voter model

Working derivation, 19 October 2026. Mathematical statements below distinguish the proved model limit from classical ingredients and the source conjecture. No authorship attribution is made here.

## 1. The source statement and the precise failure

Ganesh, Hauert and Valla (2025), *Consensus in the weighted voter model with noise-free and noisy observations*, *Swarm Intelligence*, 19, 173–214, https://doi.org/10.1007/s11721-025-00248-z, introduce the noisy model in Section 3. A reported quality `T` is the **mean** of an exponential signalling time, so its rate is `R=1/T`. Each vertex redraws the rate when it updates its opinion, including updates that leave its opinion unchanged. Rates are not inherited from the copied vertex. Their equations (5)–(6) correctly identify the equilibrium resident-rate law and its mean rate. Conjecture 2 then applies the resulting stationary branching process to an initial condition with newly sampled rates. This last replacement omits the resident's transient distribution.

The principal counterexample has constant A-rate 1 and independent B-rate draws equal to 2 or 6, each with probability one half. A has mean signalling time 1; B has mean signalling time `(1/2)(1/2+1/6)=1/3`, so A is strictly better under the source definition. The source predicts single-A fixation probability tending to `1-1/3=2/3`. We prove that the limit is approximately 0.702032053928, with an explicit exact expression and strict inequality.

This settles the universal conjecture negatively. The positive theorem below covers arbitrary compactly supported B-rate laws under uniform rate separation and a constant A-rate. It does not claim to characterise arbitrary mixtures of A-rates or overlapping rate supports.

## 2. Model and theorem

Let `a>0` and let `F` and `nu` be probability measures on a compact interval `[b_-,b_+]` satisfying

\[
0<a<b_-\le b_+<\infty.
\]

There are `N` vertices on the complete graph without self-neighbours. A vertex with opinion A updates at rate `a`. A vertex with opinion B and current rate `r` updates at rate `r`. At an update, it copies a uniformly chosen different vertex. If the copied opinion is B, it draws an independent rate from `F`; if the copied opinion is A, it takes rate `a`. Initially `k` vertices hold A, where `k>=1` is fixed, and all remaining rates are independent with law `nu`. Write `alpha_k(N;nu)` for the probability of eventual consensus on A.

Independently of this finite population, define the resident reset process `R(t)` on `[b_-,b_+]` by the bounded generator

\[
\mathcal L f(r)=r\left(\int f(s)F(ds)-f(r)\right),
\qquad R(0)\sim\nu.
\tag{2.1}
\]

Its update events include redraws that reproduce the same rate. Those events have no effect on the state trajectory but contribute to the renewal intensity. Put

\[
b_\nu(t)=\mathbb E_\nu[R(t)],\quad
A_\nu(t)=\int_0^t(b_\nu(s)-a)\,ds,\quad
J_\nu(t)=a\int_0^t e^{-A_\nu(s)}\,ds.
\tag{2.2}
\]

Because `b_nu(t)>=b_->a`, the integral `J_nu(infinity)` is finite. Define

\[
c_\nu=\frac1{1+J_\nu(\infty)}.
\tag{2.3}
\]

**Theorem.** For every fixed positive integer `k`,

\[
\boxed{\displaystyle
\lim_{N\to\infty}\alpha_k(N;\nu)
=1-(1-c_\nu)^k.}
\tag{2.4}
\]

The resident law therefore enters through its whole transient renewal intensity, rather than just the mean holding time of newly sampled residents.

**Stationary corollary.** Let

\[
\lambda=\left(\int\frac1rF(dr)\right)^{-1},
\qquad \mu(dr)=\frac\lambda rF(dr).
\tag{2.5}
\]

If `nu=mu`, then `b_nu(t)=lambda`, `c_nu=1-a/lambda`, and (2.4) becomes

\[
\lim_{N\to\infty}\alpha_k(N;\mu)
=1-(a/\lambda)^k.
\tag{2.6}
\]

This is exactly the source's stationary branching prediction in the present constant-A special case. The formula's interpretation is correct after the initial resident-rate law is changed to its stationary law.

## 3. Resident renewal equation

Let `nu_t` be the law of `R(t)`. Conditioning on the last redraw gives the measure identity

\[
\nu_t(dr)=e^{-rt}\nu(dr)
+F(dr)\int_0^t e^{-r(t-s)}b_\nu(s)\,ds.
\tag{3.1}
\]

Consequently, if

\[
h_\eta(t)=\int r e^{-rt}\eta(dr),
\]

then

\[
b_\nu(t)=h_\nu(t)+\int_0^t h_F(t-s)b_\nu(s)\,ds.
\tag{3.2}
\]

For `z>0`,

\[
\widehat b_\nu(z)
=\frac{\widehat h_\nu(z)}{1-\widehat h_F(z)},
\qquad
\widehat h_\eta(z)=\int\frac r{z+r}\eta(dr).
\tag{3.3}
\]

For fresh initialisation `nu=F`, this is the classical renewal-density transform. Thus the expression `b_F` is an ordinary renewal density for a hyperexponential or continuous mixture-of-exponentials holding-time law. No novelty is claimed for (3.1)–(3.3).

For a finite rate law `F=sum_i p_i delta_{r_i}`, with column probability vector `x(t)`,

\[
x'(t)=\left(p r^\top-\operatorname{diag}(r)\right)x(t),
\quad x(0)=\nu,\quad b_\nu(t)=r^\top x(t).
\tag{3.4}
\]

Here `p` and `r` are column vectors. Column sums of the displayed generator are zero; one must transpose it when using a row-vector convention.

## 4. A uniform fixation bound from every finite configuration

Let `M_N(t)` denote the number of A vertices, and put

\[
S_N(t)=\sum_{v:X_v(t)=B}R_v(t).
\]

Conditional on the full current state, A-count births and deaths have rates

\[
\beta_N(t)=\frac{M_N(t)S_N(t)}{N-1},\qquad
\delta_N(t)=\frac{aM_N(t)(N-M_N(t))}{N-1}.
\tag{4.1}
\]

While `0<M_N<N`,

\[
b_-\frac{M_N(N-M_N)}{N-1}
\le\beta_N\le
b_+\frac{M_N(N-M_N)}{N-1}.
\tag{4.2}
\]

These bounds hold regardless of the resident-rate configuration and its history. Put `q=a/b_-<1` and

\[
g_N(m)=\frac{1-q^m}{1-q^N}.
\]

Since

\[
g_N(m+1)-g_N(m)=\frac{q^m(1-q)}{1-q^N},\qquad
g_N(m-1)-g_N(m)=-\frac{q^{m-1}(1-q)}{1-q^N},
\]

the full generator applied to `g_N(M_N)` is nonnegative: it is a positive multiple of `q beta_N-delta_N`. Hence `g_N(M_N(t))` is a bounded submartingale up to consensus.

Consensus occurs almost surely. For fixed `N`, while both opinions remain present, the total opinion-changing rate is at least `a+b_-`, since `m(N-m)/(N-1)>=1`. The next opinion change increases A with conditional probability at least `b_-/(a+b_-)`. From any nonabsorbing configuration, at most `N-1` consecutive increases reach consensus; their conditional probability is bounded below by `[b_-/(a+b_-)]^(N-1)>0`. Repeated blocks of at most `N-1` changes therefore reach an absorbing state almost surely. Rates are bounded above, so there is no explosion.

Optional stopping now gives, from every state with `m` A vertices,

\[
\mathbb P(\text{A fixes}\mid\text{current full state})
\ge g_N(m)\ge1-q^m.
\tag{4.3}
\]

This is the step that turns the rare-lineage approximation into a theorem about ultimate fixation. A finite-time branching approximation alone would not establish (2.4).

## 5. Finite-time convergence of the rare lineage

**Lemma.** For each fixed `T<infinity`, the A-count process on `[0,T]` converges in distribution, and can be coupled to agree with probability tending to one, to the linear time-inhomogeneous birth-death process `Z` with

\[
Z(0)=k,\qquad z\longrightarrow z+1\text{ at rate }zb_\nu(t),
\quad z\longrightarrow z-1\text{ at rate }za.
\tag{5.1}
\]

Here is an elementary coupling argument that works for arbitrary compact rate laws.

### 5.1 Independent virtual residents

Assign to each vertex an independent virtual resident reset process `R_v^0(t)` with generator (2.1) and initial law `nu`. Use a rate-`b_+` Poisson proposal clock at each vertex. At each proposal, draw independent marks for acceptance, a fresh rate from `F`, and a copied neighbour. The virtual resident accepts with probability `R_v^0/b_+`; the actual population vertex accepts with probability equal to its current rate divided by `b_+`, where the actual rate is `a` for A and its stored rate for B. The neighbour mark does not affect the virtual process.

Mark a vertex once it has ever held opinion A, including the initial A vertices. At every unmarked vertex, its actual B-rate and its virtual resident rate agree: before its first A adoption it only copies B, and every accepted update redraws from `F` using the common mark. This assertion uses the source's independent redraw rule. It would fail for a different model in which a copied vertex's rate is inherited.

Let `H_N(T)` be the number of marked vertices by time `T`. Since an A-count increase can mark at most one new vertex,

\[
H_N(T)\le k+\#\{\text{A-count births by }T\}.
\]

Moreover `beta_N<=b_+M_N`, including at the absorbing states. The A count is dominated by a pure-birth Yule process of individual birth rate `b_+`. In particular,

\[
\mathbb E[M_N(t)]\le k e^{b_+t},\qquad
\mathbb E[H_N(T)]\le k e^{b_+T}.
\tag{5.2}
\]

Define the virtual average

\[
\overline R_N^0(t)=\frac1N\sum_{v=1}^N R_v^0(t).
\]

At all times `t<=T`,

\[
\left|\frac{S_N(t)}N-\overline R_N^0(t)\right|
\le\frac{b_+ H_N(T)}N.
\tag{5.3}
\]

Indeed, the two summands agree at unmarked vertices; every marked vertex contributes a discrepancy bounded by `b_+`.

### 5.2 Uniform law of large numbers

The virtual resident paths are independent and identically distributed, bounded by `b_+`, and their proposal rates are bounded by `b_+`. Therefore

\[
\sup_{0\le t\le T}|\overline R_N^0(t)-b_\nu(t)|
\xrightarrow{\mathbb P}0.
\tag{5.4}
\]

One direct proof first uses the ordinary law of large numbers on a finite time grid of mesh `Delta`. Between two adjacent grid times, the oscillation of the empirical average is bounded by `b_+` times the mean number of proposal events in that interval. The proposal counts are independent Poisson variables with mean at most `b_+Delta`; their empirical means converge at every interval of the fixed grid. Also, `b_nu(t)` is Lipschitz with constant at most `b_+^2`, because a virtual state changes by at most `b_+` at rate at most `b_+`. After `N->infinity`, let `Delta->0`. This proves (5.4) without a finite-state assumption.

Equations (5.2)–(5.4), and the factor `N/(N-1)`, yield

\[
\sup_{t\le T}\left|\frac{S_N(t)}{N-1}-b_\nu(t)\right|
\xrightarrow{\mathbb P}0.
\tag{5.5}
\]

The quantity on the left is uniformly bounded by a constant depending only on `b_+`; hence convergence also holds in mean.

### 5.3 Coupling the counts

Represent aggregate A births and deaths using independent unit-intensity Poisson random measures and their predictable intensities (4.1). Drive (5.1) with the same random measures. Stop both count processes at the first time either exceeds `K`. Before their first disagreement, the integrated difference of their birth intensities is bounded by

\[
K\int_0^T\left|\frac{S_N(t)}{N-1}-b_\nu(t)\right|dt,
\]

and the integrated difference of death intensities is bounded by

\[
\frac{aK(K-1)T}{N-1}.
\]

The expected total mismatch hazard tends to zero for fixed `K,T`. Thus the stopped processes agree with probability tending to one. Both full processes are dominated by a Yule process of birth rate `b_+`; the probability that either exceeds `K` by time `T` is at most `2k e^{b_+T}/K`. Taking `N->infinity` and then `K->infinity` proves the lemma.

The aggregate Poisson representation is used only after constructing the full population and its intensities. The resident environment can depend on those Poisson measures; the coupling argument requires predictable intensities, not independence of the actual environment from the A count. The limiting process has deterministic birth coefficient `b_nu(t)`.

## 6. Branching survival and the passage to fixation

For a single initial particle, the probability generating function of (5.1) is

\[
G_t(s)=1-
\frac{1-s}{(1+J_\nu(t))(1-s)+e^{-A_\nu(t)}s},
\qquad 0\le s\le1.
\tag{6.1}
\]

This is a classical formula for a linear birth-death process with time-dependent rates, going back to Kendall (1948). It can be checked directly by substituting in the forward equation

\[
\partial_tG_t(s)=(s-1)(b_\nu(t)s-a)\partial_sG_t(s),
\qquad G_0(s)=s.
\]

For `k` initial particles, independence of lineages gives `E[s^{Z(t)}]=G_t(s)^k`. At `s=0`,

\[
\mathbb P(Z(t)=0)=\left(\frac{J_\nu(t)}{1+J_\nu(t)}\right)^k.
\tag{6.2}
\]

For every fixed `0<=s<1`, since `A_nu(t)>=(b_--a)t` and `J_nu(t)->J_nu(infinity)`,

\[
G_t(s)\longrightarrow1-c_\nu.
\tag{6.3}
\]

Let `T` be any fixed deterministic time. If no A remains at `T`, A cannot fix. Applying (4.3) conditionally at `T`,

\[
1-\mathbb E[q^{M_N(T)}]
\le \alpha_k(N;\nu)
\le \mathbb P(M_N(T)>0).
\tag{6.4}
\]

The finite-time convergence lemma permits passage to the limit in these bounded quantities. Therefore

\[
1-G_T(q)^k
\le\liminf_N\alpha_k(N;\nu)
\le\limsup_N\alpha_k(N;\nu)
\le1-G_T(0)^k.
\tag{6.5}
\]

Finally let `T->infinity` and use (6.3). Both bounds tend to `1-(1-c_nu)^k`, proving (2.4). This proof explicitly separates the large-population limit at a fixed time from the later infinite-time limit; it does not interchange them without control.

## 7. Stationarity and fresh initialisation

The measure `mu` in (2.5) is stationary and reversible for (2.1), since

\[
\mu(dr)\,rF(ds)=\lambda F(dr)F(ds)
\]

is symmetric in `r,s`. Moreover `int r mu(dr)=lambda`. This proves the stationary corollary.

For completeness, a compact self-contained proof of the direction of fresh-initialisation bias follows. Let `P_t=exp(t L)` be the semigroup on `L^2(mu)`, write `g(r)=r-lambda`, and observe that `F(dr)=r mu(dr)/lambda`. Then

\[
b_F(t)=\frac1\lambda\langle r,P_tr\rangle_\mu
=\lambda+\frac1\lambda\langle g,P_tg\rangle_\mu.
\tag{7.1}
\]

The generator is bounded, self-adjoint and nonpositive. Indeed,

\[
\langle f,Lf\rangle_\mu
=-\frac\lambda2\iint(f(r)-f(s))^2F(dr)F(ds)\le0.
\tag{7.2}
\]

By the spectral theorem, `P_t` is a strictly positive operator: for every nonzero `g`, `<g,P_tg>_mu>0` at every finite `t`. Thus, for nondegenerate `F`,

\[
b_F(t)>\lambda\quad(t\ge0),\qquad
A_F(t)>(\lambda-a)t\quad(t>0).
\tag{7.3}
\]

Consequently

\[
J_F(\infty)<\frac a{\lambda-a},\qquad
c_F>1-\frac a\lambda.
\tag{7.4}
\]

The same spectral representation shows that `b_F(t)-lambda` is completely monotone. This renewal-monotonicity fact is classical (mixtures of exponentials have decreasing failure rate; Brown's 1980 renewal results apply). The contribution here is its consequence for the correctly proved fixation limit and the source conjecture, not a new renewal-monotonicity theorem.

## 8. Exact two-phase formula

Let

\[
F=p\delta_r+(1-p)\delta_s,\quad a<r<s,\quad0<p<1.
\]

Let the initial slow-rate probability be `theta`, so `nu=theta delta_r+(1-theta)delta_s`. Define

\[
\kappa=(1-p)r+ps,\qquad
\lambda=\frac{rs}{\kappa},\qquad
C_\theta=\theta r+(1-\theta)s-\lambda.
\tag{8.1}
\]

The phase probability solves

\[
x'(t)=ps-\kappa x(t),\quad x(0)=\theta,
\]

so

\[
x(t)=\frac{ps}{\kappa}
+\left(\theta-\frac{ps}{\kappa}\right)e^{-\kappa t},
\qquad
b_\nu(t)=\lambda+C_\theta e^{-\kappa t}.
\tag{8.2}
\]

Therefore

\[
A_\nu(t)=(\lambda-a)t+\frac{C_\theta}{\kappa}(1-e^{-\kappa t}).
\tag{8.3}
\]

Writing `eta=(lambda-a)/kappa>0` and `zeta=C_theta/kappa`, substitution `y=exp(-kappa t)` gives

\[
c_\nu^{-1}
=1+\frac a\kappa e^{-\zeta}
\int_0^1y^{\eta-1}e^{\zeta y}\,dy
=1+\frac a\kappa e^{-\zeta}
\sum_{j=0}^{\infty}\frac{\zeta^j}{j!(\eta+j)}.
\tag{8.4}
\]

The series is absolutely convergent for every real `zeta`. It may equivalently be written using the confluent hypergeometric function `1F1(eta;eta+1;zeta)/eta`. These are classical special-function identities.

Fresh initialisation has `theta=p` and

\[
C_p=\frac{p(1-p)(s-r)^2}{\kappa}>0.
\tag{8.5}
\]

Stationary initialisation has `theta=ps/kappa`, making `C_theta=0`. The sign of the bias is fully classified for this family: `C_theta>0` raises the limiting fixation probability above `1-(a/lambda)^k`; `C_theta<0` lowers it; equality holds exactly at the stationary slow-rate probability. Monotonicity follows directly from (8.3)–(8.4).

### Principal witness

Choose `a=1`, `r=2`, `s=6`, `p=theta=1/2`. Then

\[
\kappa=4,\quad\lambda=3,\quad C=1,\quad
b(t)=3+e^{-4t},\quad
\mu=(3/4,1/4).
\]

Equation (8.4) reduces to

\[
\boxed{\displaystyle
c=\left[1+\frac{\sqrt\pi}{2}e^{-1/4}
\operatorname{erfi}(1/2)\right]^{-1}
=0.702032053928\ldots >\frac23.}
\tag{8.6}
\]

Here `erfi(x)=(2/sqrt(pi)) int_0^x exp(u^2)du`. The strict inequality also follows without special functions: the integral in (2.3) is strictly less than `int_0^infinity e^(-2t)dt=1/2`.

### A separate rational strict-separation certificate

Choose `a=1`, `r=2`, `s=100`, `p=theta=1/10`. The source prediction is

\[
1-\frac1\lambda=\frac{941}{1000},\qquad
\lambda=\frac{1000}{59}.
\]

The fresh intensity is

\[
b(t)=\frac{1000}{59}+\frac{21609}{295}e^{-59t/5}.
\tag{8.7}
\]

For `0<=t<=1/10`, the alternating Taylor polynomial of degree five gives

\[
e^{-59/50}\ge\sum_{j=0}^{5}\frac{(-59/50)^j}{j!}
=\frac{11402965951}{37500000000}>\frac3{10}.
\]

It follows that `b(t)>38` on that interval. The limiting A lineage therefore dominates a homogeneous birth-death process with individual birth rate 38 and death rate 1 up to `t=1/10`. After that time, use the universal fixation bound with `q=1/2`. Its generating function gives

\[
\liminf_N\alpha_1(N;F)
\ge\frac{37}{38+36e^{-37/10}}.
\tag{8.8}
\]

The positive Taylor polynomial of degree nine gives

\[
e^{37/10}>\sum_{j=0}^{9}\frac{(37/10)^j}{j!}
=\frac{14606356247821567}{362880000000000}>40.
\]

Therefore

\[
\boxed{\displaystyle
\liminf_N\alpha_1(N;F)>\frac{370}{389}
>\frac{941}{1000}.}
\tag{8.9}
\]

The final difference is exactly `370/389-941/1000=3951/389000>0`. This independent strict-separation argument does not require evaluating the exact limiting integral. The exact limit from (8.4) is approximately 0.987409482521.

## 9. Finite count-chain checks

For the two-phase family, use state `(m,j)` with `m` A vertices, `n=N-m` B vertices, and `j` slow B vertices. The nonzero state-changing rates are

| New state | Rate |
|---|---:|
| `(m-1,j+1)` | `a*m*n*p/(N-1)` |
| `(m-1,j)` | `a*m*n*(1-p)/(N-1)` |
| `(m+1,j-1)` | `r*j*m/(N-1)` |
| `(m+1,j)` | `s*(n-j)*m/(N-1)` |
| `(m,j-1)` | `r*j*(n-1)*(1-p)/(N-1)` |
| `(m,j+1)` | `s*(n-j)*(n-1)*p/(N-1)` |

States with `m=0` and `m=N` are boundaries for the fixation problem. Resident-rate redraws continue when all opinions are B, but they cannot change fixation, so that boundary can be collapsed for this computation. At fresh initialisation, `j` is binomial with parameters `N-k,p`. Solve the linear harmonic equations exactly and average over that initial binomial distribution.

For the principal witness `(a,r,s,p)=(1,2,6,1/2)`, the exact single-A values are:

| `N` | Number of transient states | Exact fixation probability | Decimal |
|---:|---:|---:|---:|
| 2 | 2 | `16/21` | 0.761904761905 |
| 3 | 5 | `2864/4051` | 0.706985929400 |
| 4 | 9 | `443968/639901` | 0.693807323320 |
| 5 | 14 | `310846319872/449354284245` | 0.691762225867 |

Finite-population values need not approach the limit monotonically. These small examples therefore verify the transition construction and exact arithmetic, rather than proving an asymptotic trend.

For `(a,r,s,p)=(1,2,100,1/10)` the corresponding exact values are:

| `N` | Exact fixation probability | Decimal |
|---:|---:|---:|
| 2 | `1451/1515` | 0.957755775578 |
| 3 | `63225097/64870435` | 0.974636550533 |
| 4 | `30637139922283018/31191422722894425` | 0.982229640323 |
| 5 | `5031607771163105394776900299/5108992639248497828009754355` | 0.984853204232 |

All fractions above were calculated by exact rational Gaussian elimination. Independent reconstruction is required before final publication.

## 10. What is established and what is inherited

The contribution is a rigorous fixation limit for the source's noisy copying model, a correction of its initialisation-dependent branching environment, an explicit disproof of its universal conjecture, and a broad family in which the direction of the discrepancy is determined. The resident renewal equation, stationary length bias, the linear birth-death survival formula, and decreasing-failure-rate renewal monotonicity are classical ingredients. Their formulas are recorded so that reviewers can verify object identity and attribution.

The full conjecture with arbitrary A-rate mixtures is not resolved positively. The present theorem proves enough to refute it as stated and to state a correct replacement under transparent, broad sufficient assumptions. The narrow overlap-free assumption is a proof boundary; it should not be concealed by phrasing the replacement as a full classification of every noisy weighted voter model.

### Primary and closely related sources inspected

- Ganesh, A., Hauert, S., & Valla, E. (2025). Consensus in the weighted voter model with noise-free and noisy observations. *Swarm Intelligence, 19*, 173–214. https://doi.org/10.1007/s11721-025-00248-z . Section 3, equations (5)–(7), and Conjecture 2 establish the target and initialisation convention.
- Uecker, H., & Hermisson, J. (2011). On the fixation process of a beneficial mutation in a variable environment. *Genetics, 188*, 915–930. https://pmc.ncbi.nlm.nih.gov/articles/PMC3176092/ . Equations (7) onward and the discussion credit the time-dependent branching formalism to Kendall (1948); this is a prior ingredient, not the target copying model.
- Jafarpour, F., Levien, E., & Amir, A. (2023). Evolutionary dynamics in non-Markovian models of microbial populations. *Physical Review E, 108*, 034402. https://doi.org/10.1103/PhysRevE.108.034402 . This uses age-dependent reproduction followed by random expulsion; inspect Sections II and IV before asserting any relationship to the death/reset-copy model here.
- Alexandre, A., Abbara, A., Fruet, C., Loverdo, C., & Bitbol, A.-F. (2025). Bridging Wright–Fisher and Moran models. *Journal of Theoretical Biology, 599*, 112030. https://doi.org/10.1016/j.jtbi.2024.112030 . The model uses discrete partial replacement and a diffusion approximation; its renewal treatment explicitly separates transient and asymptotic update probabilities.

The separate novelty report records search queries, formula comparisons and missingness. A failed search is not a proof of historical priority.
