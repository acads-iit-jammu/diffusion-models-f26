# Claude Opus 5.5 review: one-dimensional tutorial rewrite

Reviewed the reading guide and four rewritten tutorials before the final corrections.
The figures and simulation code were validated separately by the authoring agent.

# Review: Four-Part One-Dimensional Score-Diffusion Sequence

**Scope.** I re-derived every displayed equation by hand. I did not review the figures or `materials/one-dimensional-score-examples.py`, because they were not included.

**Headline.** I found **no incorrect equation, sign, clock direction, or coefficient**. The problems are missing hypotheses, a few undefined or ambiguous objects, notation collisions across tutorials, and several places where a result is *checked* when it should be *derived*. The teaching order matches the required sequence.

---

## Must-fix

These are statements that are false as written, depend on something undefined, or refer to the wrong thing. Each fix is one sentence or one formula.

**M1. The initial state is never assumed independent of the Brownian motion.** Three claims depend on this assumption:
- T2 `#gaussian-langevin`: "The integral is independent of $X_0$."
- T3 `#gaussian-kernel`: "The added term is an independent centered Gaussian."
- T3 reverse SDE: the independence of $Y_0\sim p_T$ from the reverse noise.

Fixes:
- **T2 `#euler-maruyama`**, directly after the boxed SDE, insert:
  > Throughout, the initial state $X_0$ is independent of the Brownian motion $(W_t)_{t\ge0}$; in numerical schemes, $\xi_k$ is independent of $\widehat X_0,\xi_0,\dots,\xi_{k-1}$.
- **T3 `#vp`**, after the definitions of $f$ and $g$, insert:
  > Draw $X_0\sim p_{\mathrm{data}}$ independently of $W$.
- **T3 `#song-sde-conventions`**, after the boxed $\tau$-clock SDE, insert:
  > Here $\overline W_\tau$ is a standard Brownian motion in the increasing clock $\tau$, independent of $Y_0\sim p_T$.

**M2. T2 `## Mixtures` uses $m$ and $a$ without defining them.** This breaks the guide's claim that T2 is stand-alone. Replace the first sentence with:
> Take $p(x)=\tfrac12\phi_a(x-m)+\tfrac12\phi_a(x+m)$, an equal mixture of $\mathcal N(\pm m,a^2)$, where $\phi_a$ is the $\mathcal N(0,a^2)$ density. Since $\phi_a(x-m)/\phi_a(x+m)=e^{2mx/a^2}$, its score is $s(x)=[m\tanh(mx/a^2)-x]/a^2$. Use this score in the Langevin update.

**M3. T3 annealed Langevin: $p_{\sigma_i}$ is undefined.** It could be read as a VP marginal (with the factor $\alpha_t$) or as additive noise, and these are different laws. Replace "approximately samples the smoothed data law $p_{\sigma_i}$" with:
> approximately samples $p_{\sigma_i}$, the law of $X_0+\sigma_i\epsilon$ (additive noise with no $\alpha_t$ factor). This is the drift-free corruption $dX_t=g\,dW_t$ with $\sigma^2=g^2t$, sometimes called variance-exploding. Its score is $s_{\sigma}=\partial_x\log p_\sigma$.

**M4. T3 linear-schedule formula: $\beta_{\min}$ and $\beta_{\max}$ are undefined.** The displayed $\log\alpha_t$ is correct only for a schedule on $[0,1]$. Replace with:
> for the linear schedule $\beta(t)=\beta_{\min}+(\beta_{\max}-\beta_{\min})t$ on $0\le t\le T=1$, $\log\alpha_t=-\beta_{\min}t/2-(\beta_{\max}-\beta_{\min})t^2/4$.

**M5. T2 `#gaussian-langevin` points to the wrong term.** "Without noise, the second term supplying this nonzero limiting variance is absent." In the boxed formula, the second term is the *decaying initial* term; the variance comes from the third term. Replace with:
> Without noise, the stochastic integral—the only source of the limiting variance $a^2$—is absent, and the variance $a_0^2e^{-2t/a^2}$ collapses to zero.

---

## Should-fix

These are pedagogical gaps, missing essential derivations, and notation problems.

**S1. T2 `#expected-taylor-step`: the jump from averages to the pathwise Itô lemma is unexplained.** The Taylor argument justifies only $\frac{d}{dt}\mathbb E\varphi$. The $g\,\partial_xF\,dW_t$ term, and the reason $(\Delta X)^2$ can be replaced by $g^2h$ *pathwise*, both appear without explanation. Quadratic variation, which is the actual reason, is explained only afterward.

- After "The squared random increment survives at order $h$," insert:
  > Cubic and higher terms have $\mathbb E|\Delta X|^3=O(h^{3/2})$, so they vanish after dividing by $h$.
- Before the boxed full lemma, insert:
  > To follow paths rather than averages, keep the random parts. Summed over many steps, the fluctuation $\varphi'(x)\,g\sqrt h\,\xi_k$ builds the Itô integral $\int g\,\partial_xF\,dW$. The quadratic term $\tfrac12\varphi''g^2h\,\xi_k^2$ differs from $\tfrac12\varphi''g^2h$ by $\tfrac12\varphi''g^2h(\xi_k^2-1)$. These differences have mean zero and total variance $O(h)$, so their sum vanishes in mean square.
- Move the quadratic-variation paragraph ("Over finer partitions, $\sum_k(\Delta W_k)^2\to t$…") from the $W_t^2$ example to just before the boxed lemma. Keep the $W_t^2$ example as its application.

**S2. T2 `#langevin`: zero flux is imposed, but it can be derived. The general-$g$ balance is also missing, and T3 relies on it.** Replace "At equilibrium, impose zero probability flux … natural equilibrium condition. Solving for drift gives" with:
> Stationarity means $\partial_tq=-\partial_xJ=0$. In one dimension, $J$ is then the same constant at every $x$. Vanishing flux at $\pm\infty$ forces that constant to be zero: $J=fp-\tfrac12g^2p'=0$, so $f=\tfrac12g^2s$. In one dimension this is the *only* drift that makes $p$ stationary with vanishing flux. The conventional choice $g=\sqrt2$ makes the drift exactly the score:

T3's frozen-Langevin analysis ($A=D$) and its "balanced Langevin drift $\tfrac12g^2s_t$" then read as consequences of T2, not new claims.

**S3. The integrating factor is asserted, but it is Itô's lemma with no correction term.** Students have just learned the lemma, so they should see it applied.

- **T2 `#gaussian-langevin`**, replace "Multiplying $X_t-\mu$ by $e^{t/a^2}$ cancels the drift. Integrating gives" with:
  > Apply Itô's lemma to $F(x,t)=e^{t/a^2}(x-\mu)$. Here $\partial_tF=F/a^2$, $\partial_xF=e^{t/a^2}$, and $\partial_{xx}F=0$, so there is no Itô correction and the drift cancels: $dF(X_t,t)=\sqrt2\,e^{t/a^2}dW_t$. Integrate from $0$ to $t$ and multiply by $e^{-t/a^2}$:
- **T3 `#gaussian-kernel`**, replace "The integrating factor $1/\alpha_t$ cancels the drift, as in Gaussian Langevin:" with:
  > Apply Itô's lemma to $F(x,t)=x/\alpha_t$. The term $\partial_tF=\tfrac12\beta x/\alpha_t$ cancels the drift contribution $-\tfrac12\beta x/\alpha_t$, and $\partial_{xx}F=0$. Hence $d(X_t/\alpha_t)=\alpha_t^{-1}\sqrt{\beta(t)}\,dW_t$, and

**S4. T3 `#reverse-sde`: the reverse drift is verified but not derived, and there is no worked reverse-SDE example.** The guide promises that every worked model gets a density check; the reverse SDE currently has none.

- Replace "The increasing-clock SDE with drift $b=-f+g^2s_t$ gives … exactly the required derivative." with:
  > Seek $dY_\tau=\bar f(Y_\tau,\tau)\,d\tau+g\,dB_\tau$ whose density is $q_\tau$. Its Fokker–Planck equation must equal the reversed one: $-\partial_x(\bar fq_\tau)+\tfrac12g^2q_\tau''=\partial_x(fq_\tau)-\tfrac12g^2q_\tau''$, that is, $\partial_x[(\bar f+f)q_\tau-g^2q_\tau']=0$. As in the Langevin derivation, the bracket is constant in $x$ and vanishes at infinity. Therefore $\bar f=-f+g^2q_\tau'/q_\tau=-f+g^2s_t$.

  Using $\bar f$ instead of $b$ also removes a clash with T4's $b(t)$.
- Add a worked check after this derivation (all steps verified):
  > **Worked check: reversing Brownian spreading.** Take $dX_t=g\,dW_t$ from $\mathcal N(\mu,a_0^2)$, so $V_t=a_0^2+g^2t$. The reverse SDE is $dY_\tau=-\frac{g^2}{V_{T-\tau}}(Y_\tau-\mu)\,d\tau+g\,dB_\tau$ with $Y_0\sim\mathcal N(\mu,V_T)$. Itô gives $\frac{d}{d\tau}\operatorname{Var}Y_\tau=-\frac{2g^2}{V_{T-\tau}}\operatorname{Var}Y_\tau+g^2$. At $\operatorname{Var}Y_\tau=V_{T-\tau}$, both sides equal $-g^2$. The probability-flow ODE (half the drift, no noise) gives $-g^2V/V=-g^2$ as well. Keeping the full drift but deleting the noise gives $-2g^2$: the variance shrinks twice too fast.

  This makes the factor of two concrete.

**S5. T1 "From moving particles to a moving density": the flow notation conflicts with T3, and the change-of-variables step is only heuristic.** $F_t$ here means a flow; in T3 `$F_t$` means a CDF. Replace "For an increasing flow $x=F_t(x_0)$, [display]" with:
> One-dimensional ODE flows are increasing, because trajectories cannot cross. Hence $X_t\le x$ exactly when $X_0\le\Psi_{t\to0}(x)$, so $P(X_t\le x)=P(X_0\le\Psi_{t\to0}(x))$. Differentiating in $x$,
> $$\boxed{q_t(x)=q_0(\Psi_{t\to0}(x))\,\partial_x\Psi_{t\to0}(x).}$$

This also seeds T3's rank-preservation argument.

**S6. Notation collisions.** Each symbol below has two meanings somewhere in the series.

| Where | Collision | Replacement |
|---|---|---|
| T1 continuity | Interval $[a,b]$ vs. std $a$ | $[x_L,x_R]$ |
| T3 learning / Tweedie | $p(x\mid x_0)$ has no time index | $p_t(x\mid x_0)$, $p_t(x_0\mid x)$ |
| T3 two-point example | Denoiser $D_t$ vs. Langevin constant $D$ | $\widehat x_0(x,t)$ |
| T4 density tracking | $A_t$ vs. T3's $A$ | $\Psi'_{0\to t}(x_0)$ (ties back to the flow map) |
| T4 flow matching | Endpoints $A,B$ | $Z$ (source) and $X_{\rm data}$ (target) |
| T4 Jacobian | $J_F$ vs. flux $J$ | $DF$ or $\partial F/\partial x$ |
| T4 flow matching | $U$ and $U_t$ both used | $U_t=\partial_t\widetilde X_t$ throughout; note it equals $B-A$, constant in $t$ |

Also add these missing entries to the guide's symbol table: $\beta(t)$, $\tau$, $u$, $B_u$, $s_\theta$, $\pi_T$, $\lambda(t)$, $F_t$ (CDF, T3), $\widehat X_k$ (numerical state), and the denoiser.

**S7. T4 flow matching does not say which way its clock runs.** T3 runs data → noise; flow-matching papers usually run noise → data. After defining $\widetilde X_t$, add:
> Here $t=0$ is the source $Z$ and $t=1$ is data, the reverse of Tutorial 3's corruption clock. The Gaussian-interpolant subsection below returns to Tutorial 3's convention, with $t=0$ as data.

**S8. T3: the ODE and SDE generation updates use opposite index conventions.** The ODE uses a descending index ($x_{k-1}$); the SDE uses an ascending index ($y_{k+1}$). Rewrite the ODE step in the generation clock:
> With $t_k=T-kh$, Euler is $y_{k+1}=y_k-h\,v(y_k,t_k)$.

**S9. T4 "Their endpoint covariances…" is ambiguous.** Replace with:
> Their covariances with the starting point are $\operatorname{Cov}(X_0,X_t^{\rm SDE})=a_0^2$ and $\operatorname{Cov}(X_0,X_t^{\rm ODE})=a_0\sqrt{a_0^2+g^2t}$. The ODE's correlation with $X_0$ is exactly $1$; the SDE's is $a_0/\sqrt{a_0^2+g^2t}<1$.

**S10. T4 Gaussian Langevin: the 1D zero-flux argument does not carry over to several dimensions.** After "has target $p$ as its invariant density," add:
> In $d\ge2$, stationarity no longer forces zero flux. For example, adding $w=R\nabla\log p$ with $R$ constant and antisymmetric also keeps $p$ invariant, because $\nabla\cdot(R\nabla p)=0$. The score drift is the zero-flux, reversible choice.

**S11. T3 Tweedie section repeats itself.** The unscaled formula $\mathbb E[X\mid Y=y]=y+\sigma^2\partial_y\log p_Y$ and the "Bayes-optimal" sentence each appear twice. Delete "The squared-error decomposition above proves … possible clean sample." from the unscaled derivation, and move "It averages uncertainty rather than selecting one possible clean sample" to the end. Also delete the final "For unscaled additive noise … set $\alpha=1$ to get …" sentence.

**S12. Titles and legacy URLs.**
- The guide's reading-order table titles do not match the page titles. Copy them exactly, for example "ODEs in One Dimension: Particles, Flows, and Densities" and "From One-Dimensional Transport to Neural ODEs and Higher Dimensions".
- Old links will now land on unrelated content. Add a one-line callout at the top of each file:
  - 25: "Looking for score learning? It is now in Tutorial 3."
  - 26: "Looking for probability flow? It is now Tutorial 3 §probability-flow."
  - 27: "Looking for neural ODEs and normalizing flows? They are now Tutorial 4."
  - 28: "Looking for Langevin dynamics? It is now Tutorial 2 §langevin."

**S13. Undefined terms at first use.**
- T2, "almost surely" → add "(with probability one)".
- T2, "convergence in distribution" → add "(CDFs converge at every continuity point)".
- T3 training step 4 uses $\lambda(t)$ before it is defined → write "a positive time weight $\lambda(t)$ (see below)".
- T4, "Lipschitz" → add "$|v(x,t)-v(y,t)|\le L|x-y|$".

---

## Optional

Each of these is either a stylistic preference or an extra.

1. **T1 `#gaussian-score`.** Strengthen "generally nonzero" to: "$p''$ cannot vanish identically for a probability density on the line, so *no* target is stationary under its own score ODE."
2. **T1 `#mode-seeking`.** Add: "When $m\le a$ the mixture is unimodal and every particle approaches $0$."
3. **T1 Gaussian transport check.** Show the one-line computation: $-\partial_xv-v\,\partial_x\log q=-\dot a/a+(\dot m+\dot a\,y)\,y/a$.
4. **T3, after the decomposition.** For any $\gamma\ge0$, the drift $-f+\tfrac12(g^2+\gamma^2)s_t$ with noise $\gamma$ has the same marginals. $\gamma=0$ gives probability flow and $\gamma=g$ gives the reverse SDE. This unifies the section.
5. **T2 Itô integral.** Say "continuous $c$" for the left-endpoint Riemann sums; general $L^2$ integrands need step-function approximation.
6. **T3 two-point example.** Replace "continuous terminal law" with "terminal law with a density", so it is not read as continuous-time.
7. **T4.** Replace "its density falls by $1/a$" with "its density is divided by $a$".
8. **Rename the mixture half-separation $m$** (it collides with $m_t$), for example to $\pm\eta$.
9. **Titles.** T1 could append "…and Scores"; T3 could be "Corruption, Reversal, and Score Learning". The current titles are acceptable.
10. **T3 sources.** Consider adding Anderson (1982, time reversal), Vincent (2011, DSM), Efron (2011, Tweedie), and Ho et al. (2020, $\epsilon$-prediction).
11. **T2 order.** The SDE notation appears in the Euler–Maruyama section, before the Itô integral gives it meaning. This is acceptable; a forward pointer would help ("the next section makes $dW$ precise").

---

## Verified correct

Checked by hand, grouped by tutorial:

- **T1:** contraction flow, density, and continuity check; along-trajectory $-\partial_xv$; all three Gaussian score ODEs and their density checks; mixture score, $s'(0)$, and mode equation; Gaussian transport velocity, the $\mathcal N(2,4)$ example, and the log-density check.
- **T2:** random-walk variances; Euler–Maruyama numeric example; Itô isometry; $\int W\,dW$ and the quadratic-variation variance $2\sum\Delta t^2$; Fokker–Planck by parts; Brownian spreading check; Ornstein–Uhlenbeck solution, variance, and moment ODEs; the full Gaussian Fokker–Planck identity; ULA $V_h=a^2/(1-h/2a^2)$ and the exact transition.
- **T3:** $\alpha_t$ and $\sigma_t^2$ algebra; VP moments; probability-flow velocity; outward Brownian flow; VP transport equal to $\dot m+(\dot a/a)(x-m)$, including $v=0$ and $v=\dot m$; Song's three equations and the $\tau$-clock form; reverse Fokker–Planck; frozen $p^{A/D}$ and the $p_t^2$ mismatch; the drift decomposition; the two-point posterior ($e^{2\alpha x/\sigma^2}$, $\tanh$); marginal-score identity; MSE lemma; irreducible DSM loss $\alpha^2/\sigma^4$; $1/t$ divergence; $\epsilon$-parameterization; Tweedie (scaled and unscaled); quantile map.
- **T4:** Jacobian ODE; likelihood sign and the $v=-x$ example; flow-matching continuity; Gaussian-interpolant recovery of $bx-\tfrac12g^2s$; $\dot\sigma\sim t^{-1/2}$; multi-dimensional Itô, Fokker–Planck, and probability flow; $\log\det(I+hJ)$ and the 2×2 determinant.

The teaching order matches the required sequence. Deriving probability flow before the reverse SDE in T3 is the better choice, because the reverse-SDE decomposition then reuses it.

---

## Verdict

**Mathematically sound and well ordered; publishable after the five must-fix edits**, all of them sentence-level. I recommend S1–S4 before release: they supply the pathwise Itô argument, derive zero flux in 1D, show the integrating factor as an application of Itô's lemma, and give an actual reverse-drift derivation with a worked factor-of-two example. Those are the places where a student with no SDE background would otherwise have to take a step on faith. The rest is consistency polish, and no rewrite is needed.

---

## Revisions applied after review

All five must-fix findings were addressed. The thirteen should-fix findings were
also addressed, with the multidimensional stationarity qualification illustrated
by an explicit two-dimensional circulating Gaussian current instead of introducing
an arbitrary antisymmetric matrix.

- Added initial/noise independence assumptions and standalone mixture definitions.
- Defined additive-noise annealing separately from VP and specified the linear schedule interval.
- Corrected the reference to the stochastic integral supplying limiting variance.
- Expanded the pathwise Itô explanation using quadratic variation and explicit local bounds.
- Derived zero-flux Langevin balance for general constant noise amplitude.
- Applied Itô's lemma explicitly to both integrating factors.
- Derived reverse drift from density conservation and added a Gaussian variance check.
- Unified generation step indices and clarified flow-matching time direction.
- Removed notation collisions and expanded the guide's symbol table.
- Clarified endpoint covariance, finite-step versus exact dynamics, and prior content locations.
- Reduced Tweedie repetition and defined probabilistic terms at first use.
- Restricted point-sampled Itô sums to continuous deterministic integrands; general L2 integrands use step approximations.

Validation: full Quarto render; local link/anchor/image validation; rendered MathJax
checks; visual inspection of figures and page layouts; numerical Gaussian
Fokker–Planck, mixture score, Gaussian simulation, and ULA variance checks.
The review was not rerun after these corrections. This revision has not been deployed.
