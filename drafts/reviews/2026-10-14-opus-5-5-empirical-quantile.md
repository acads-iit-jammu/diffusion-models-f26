# Independent Claude Opus 5.5 review: empirical quantile flow

The reviewer received the full Part 07 text, the earlier Part 01 CDF derivation, and saved notebook text outputs. It did not run code or inspect figures. Private language-modeling material was not included.

# Review of Part 07, with focus on §2.2 (empirical quantile flow)

I reviewed only the text and saved outputs in your message. I did not read repository files, run notebooks, or view figures. The notebook numbers below are your saved outputs, not my own results.

## Independent reconstruction

**VP relations.** With $\alpha_t=\exp(-\tfrac12\int_0^t\beta)$ and $\sigma_t^2=1-\alpha_t^2$:

- $\dot\alpha_t=-\tfrac12\beta\alpha_t$
- $\sigma_t\dot\sigma_t=\tfrac12\beta\alpha_t^2$

For $\beta=0.1+19.9t$, the integral is $0.1t+9.95t^2$. This gives the stated $\alpha_t$, $\sigma_t^2$, and $\alpha_1=e^{-5.025}$. All correct.

**Velocity (§2).** Substituting the score gives $x+\widehat s=\alpha_t(m-\alpha_tx)/\sigma_t^2$. So $v=\frac{\beta\alpha_t}{2\sigma_t^2}(\alpha_tx-m)$, and the backward Euler step has the stated sign. Correct.

**Rank conservation (§2.2), checked directly from $F_t$.** Let $z_i=(x-\alpha_tx_i)/\sigma_t$. Then:

$$-\partial_tF_t=\tfrac1n\sum_i\phi(z_i)\Big[\dot\alpha_tx_i+\tfrac{\dot\sigma_t}{\sigma_t}(x-\alpha_tx_i)\Big],\qquad \widehat p_t=\tfrac1n\sum_i\phi(z_i)/\sigma_t.$$

Dividing gives $v=\dot\alpha_t m+\frac{\sigma_t\dot\sigma_t}{\sigma_t^2}(x-\alpha_t m)$. Using the VP relations, this becomes $\frac{\beta\alpha_t}{2\sigma_t^2}\big[\alpha_tx-m(\alpha_t^2+\sigma_t^2)\big]=\frac{\beta\alpha_t}{2\sigma_t^2}(\alpha_tx-m)$. This matches §2 exactly.

The rank-conservation claim is therefore true. For $t\in(0,1]$, $F_t$ is a $C^1$ strictly increasing bijection $\mathbb R\to(0,1)$, and $v$ is locally Lipschitz in $x$. Hence the quantile curve is the unique ODE solution.

**Other checks:**

| Claim | Status |
|---|---|
| Single-atom formula ($z$ is constant along the path) | Correct |
| Constant-$\beta$ formulas | Correct |
| Linear $\alpha$: $\beta=-2\dot\alpha/\alpha=2/(1-t)$ | Correct |
| Uniformity of $U=F_1(X_1)$ and pushforward claim | Correct |
| $\lim_{t\downarrow0}F_t^{-1}(u)=x_{(\lceil nu\rceil)}$ for $u\in((k-1)/n,k/n)$ | Correct: $F_t(x_{(k)}\mp\epsilon)\to(k-1)/n,\ k/n$ bracket $u$ |
| tanh two-point formula, §1.3 logit expansion, §5 truncation bound and multipliers, §8 bandwidth $\sigma_t/\alpha_t$, §7.1 uniform limit | Correct |
| Quoted numbers in §6 and §7.1 vs. saved outputs | Consistent (118.14, 2.12, 0.00302, table entries, 0.000120, 6.03%/92.84%/100%, image 224 at 0.693) |

## Issues

### Should fix before publishing

**1. §2.2 — the "independent derivation" assumes the step it claims to derive.**

The argument starts from $\partial_t\widehat p_t=-\partial_x(\widehat p_tv)$ for *this specific* $v$. That fact is imported from the probability-flow construction of Song et al.; it is not derived here. As written, the derivation is circular with respect to its "independent" label. The fix is short, and it doubles as a consistency check with §2.

Proposed replacement for the paragraph after "$F_t$ has a unique inverse":

> Rather than assume that the probability-flow field satisfies the continuity equation, define the field the continuity equation would require, $v_F(x,t)=-\partial_tF_t(x)/\widehat p_t(x)$ (Part 01). The left-boundary flux vanishes because $\widehat p_t$ has Gaussian tails. Differentiating the boxed CDF with $z_i=(x-\alpha_tx_i)/\sigma_t$ gives
> $$v_F(x,t)=\dot\alpha_t\,m_t(x)+\frac{\dot\sigma_t}{\sigma_t}\bigl(x-\alpha_tm_t(x)\bigr).$$
> Using $\dot\alpha_t=-\tfrac12\beta\alpha_t$ and $\sigma_t\dot\sigma_t=\tfrac12\beta\alpha_t^2$, this equals $\frac{\beta(t)\alpha_t}{2\sigma_t^2}[\alpha_tx-m_t(x)]$, the field of Section 2. The softmax denoiser therefore reappears from the CDF alone.

The rest of the argument (chain rule, rank conservation) can then stay as written.

**2. §2.2 and §2.1 — notation clash on $x_1$.**

$x_1$ denotes both the first stored observation and the terminal state at $t=1$. In $F_1(x_1)=\frac1n\sum_i\Phi((x_1-\alpha_1x_i)/\sigma_1)$, the clash is genuinely confusing. Rename the terminal state, e.g. $\xi$, or use Part 01's $x(t)$ style.

> Starting from a terminal value $\xi=x(1)$, compute $u=F_1(\xi)$ once. The exact backward trajectory is $x(t)=F_t^{-1}(F_1(\xi))$, $t\in(0,1]$.

Make the same change in §2.1 step 2 ("set $x(1)=\alpha_1x_I+\sigma_1z$") and in the single-atom box ($\sigma_t(\xi-\alpha_1a)/\sigma_1$).

**3. §4 — $\Phi$ is reused for the flow map.**

§2.2 defines $\Phi$ as the standard-normal CDF. §4 then writes $R_\epsilon=(\Phi_{\epsilon\leftarrow1})_\#R_1$. Part 01 explicitly reserves $\Psi$ for flow maps. Change §4 to $(\Psi_{\epsilon\leftarrow1})_\#R_1$, and say once that $\Psi_{s\leftarrow t}$ is the ODE flow map.

(Optional, related: $\phi_i(x,t)$ in §1 versus the standard-normal density $\phi$ in Part 01. A one-line remark would avoid confusion.)

**4. §2 / §2.2 — the VP α–β relation is used but never stated.**

The constant-β and linear-α examples rely on $\alpha_t=\exp(-\frac12\int_0^t\beta)$, which the lecture never states. Add after the schedule in §2:

> For any VP schedule, $\alpha_t=\exp\!\bigl(-\tfrac12\int_0^t\beta(s)\,ds\bigr)$ and $\sigma_t^2=1-\alpha_t^2$, so $\dot\alpha_t=-\tfrac12\beta\alpha_t$ and $\sigma_t\dot\sigma_t=\tfrac12\beta\alpha_t^2$.

### Minor corrections and clarifications

**5. §2.2, boundary-rank sentence — understated.**

The zero-probability statement holds for *any* terminal law with a density, including $\mathcal N(0,1)$, not only matched initialization. Also, the boundary limit can be stated rather than deferred.

Balancing the two dominant Gaussian tails gives $F_t^{-1}(k/n)-\alpha_t\frac{x_{(k)}+x_{(k+1)}}2=O(\sigma_t^2)$ for $1\le k\le n-1$. This is my asymptotic sketch, so worth checking before you include it. The two-point zero path is the $n=2$ case. Proposed wording:

> The ranks $u=k/n$, $1\le k\le n-1$, have probability zero under any terminal law with a density, including standard Gaussian noise. Along such a rank the trajectory approaches the midpoint $\tfrac12(x_{(k)}+x_{(k+1)})$; the symmetric two-point path fixed at zero is the simplest case.

**6. §2.2, linear-α example — "singular at time one" may mislead.**

$\beta$ is singular, but the velocity is not. Since $\beta\alpha_t=2$, the field is $v=((1-t)x-m_t(x))/\sigma_t^2$, which is bounded near $t=1$. Moreover $\alpha_1=0$ and $\sigma_1=1$ make $F_1=\Phi$, so standard Gaussian initialization is *exactly* matched. That is a useful contrast with §4's $\alpha_1=e^{-5.025}>0$. Proposed wording:

> A linear amplitude $\alpha_t=1-t$ requires $\beta(t)=2/(1-t)$, which diverges at $t=1$. Nevertheless $\beta\alpha_t=2$, so the velocity $((1-t)x-m_t(x))/\sigma_t^2$ remains bounded there, and $F_1=\Phi$: a standard Gaussian terminal draw is then exactly matched.

**7. §2.2, invertibility sentence.** Positivity of the derivative gives injectivity. Surjectivity onto $(0,1)$ also needs the limits. Suggest: "...$\widehat p_t>0$ and $F_t(\mp\infty)=0,1$, so $F_t$ is a bijection from $\mathbb R$ onto $(0,1)$."

**8. §2.2 vs. §6 — the numerical-reference claim has no saved evidence.**

The section calls the quantile representation "a useful numerical reference." The saved 1D outputs show only Euler 800-vs-1600 differences; there is no bisection comparison. Either add a notebook cell (Euler vs. $F_t^{-1}(F_1(\xi))$ at the reported cutoffs) or soften the wording to "can serve as a reference."

Also add a numerical caution. Near a boundary rank at small $t$, $dx/du=1/\widehat p_t$ grows like $e^{g^2/(8\sigma_t^2)}$, where $g$ is the gap between adjacent atoms. Euler error and floating-point rounding of $u$ can then flip which atom is approached. Tail evaluations should use `log_ndtr`/`erfc` rather than raw $\Phi$.

### Optional improvements

- **§4 / §3:** In 1D, §2.2 makes the claim "prior mismatch alone does not guarantee interpolation" sharp. Under exact transport from Gaussian noise, endpoints are stored atoms with probability one, and atom $k$ is reached with probability $\Pr\{F_1(Z)\in((k-1)/n,k/n]\}$. A cross-reference would connect the sections.
- **§2.2 closing:** Note that for $d>1$ the probability-flow map is generally not a triangular (Knothe–Rosenblatt) quantile map. This is why the scalar construction does not extend.
- **Opening callout:** Mention the quantile representation among the derived results.

## Implicit representation vs. closed form

The section handles this well. The trajectory is labeled an exact implicit representation; the root-solve caveat is explicit; only the single-atom case is presented as an elementary formula; and the constant-β box says "the exact position solves." No change needed.

## Rest of the lecture

§§1, 3, 5, 7, 8 and the §6 reported numbers are mathematically sound and consistent with §2.2. §3's "regular invertible flow is not asserted at the endpoint" agrees with §2.2's treatment of the atomic limit. The restriction to $t>0$ correctly adapts Part 01's construction, which assumed positive density on all of $[0,1]$.

## Recommendation

The core mathematics of §2.2 is correct; I verified it independently, including agreement with the §2 field. It is **not quite ready to publish**. Fix items 1–4 first: the circular "independent" step, the $x_1$ and $\Phi$ notation clashes, and the missing α–β relation. Each is a few lines. Items 5–8 are worthwhile but not blocking. After items 1–4, the section is ready.
