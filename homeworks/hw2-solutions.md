# HW 2 — Solutions and Marking Scheme

**ID-5-02 (TO) · Mathematical Foundations of Diffusion Models · Monsoon 2026**

*Worked solutions and marking scheme, released for student reference.*

Total: 50 points (5 problems × 10). **Graded on correctness** — unlike HW 1.
The per-part marks below are the marking scheme, not a formality.

---

## Problem 1 — Beta mean and variance (10)

*Setup:* germination rate varying across seed lots; Beta$(\alpha,\beta)$ on $[0,1]$.

Throughout, $B(\alpha,\beta) = \Gamma(\alpha)\Gamma(\beta)/\Gamma(\alpha+\beta)$
and $\Gamma(z+1) = z\Gamma(z)$.

**(a) (1)** $\int_0^1 f = \frac{1}{B(\alpha,\beta)}\int_0^1 x^{\alpha-1}(1-x)^{\beta-1}dx
= \frac{B(\alpha,\beta)}{B(\alpha,\beta)} = 1$ — immediate from the definition of $B$.

**(b) (3)** The integrand for $\EE[X]$ is the Beta kernel with $\alpha \to \alpha+1$:

$$
\EE[X] = \frac{1}{B(\alpha,\beta)}\int_0^1 x^{\alpha}(1-x)^{\beta-1}dx
= \frac{B(\alpha+1,\beta)}{B(\alpha,\beta)}
= \frac{\Gamma(\alpha+1)}{\Gamma(\alpha)}\cdot\frac{\Gamma(\alpha+\beta)}{\Gamma(\alpha+\beta+1)}
= \frac{\alpha}{\alpha+\beta}.
$$

*Marks:* 1 for recognising the shifted Beta kernel, 1 for the ratio of $B$'s,
1 for applying $\Gamma(z+1)=z\Gamma(z)$ twice to reach $\alpha/(\alpha+\beta)$.

**(c) (3)** Same move, shifting by two:

$$
\EE[X^2] = \frac{B(\alpha+2,\beta)}{B(\alpha,\beta)}
= \frac{\Gamma(\alpha+2)}{\Gamma(\alpha)}\cdot\frac{\Gamma(\alpha+\beta)}{\Gamma(\alpha+\beta+2)}
= \frac{\alpha(\alpha+1)}{(\alpha+\beta)(\alpha+\beta+1)} .
$$

*Marks:* as in (b).

**(d) (2)**

$$
\Var(X) = \frac{\alpha(\alpha+1)}{(\alpha+\beta)(\alpha+\beta+1)} - \frac{\alpha^2}{(\alpha+\beta)^2}
= \frac{\alpha}{\alpha+\beta}\left[\frac{\alpha+1}{\alpha+\beta+1} - \frac{\alpha}{\alpha+\beta}\right]
= \boxed{\dfrac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}}
$$

The bracket simplifies because $(\alpha+1)(\alpha+\beta) - \alpha(\alpha+\beta+1) = \beta$.
*Marks:* 1 for the subtraction set up, 1 for reaching the single fraction. Award
both if they get there by any correct route.

**(e) (1)** At $\alpha=\beta$ the mean is $\alpha/(2\alpha) = 1/2$. Obvious because
$f(x) \propto x^{\alpha-1}(1-x)^{\alpha-1}$ is then symmetric about $x = 1/2$.
*Marks:* 1, requires the symmetry reason, not just the number.

**Common errors.** Trying to integrate $x^\alpha(1-x)^{\beta-1}$ by parts instead
of recognising it as another Beta; forgetting the normaliser; algebra slips in (d)
— accept any equivalent correct form.

---

## Problem 2 — logit of a uniform (10)

*Setup:* a completely unknown probability $U\sim\mathrm{Uniform}(0,1)$ pushed to the
log-odds scale, $X=\mathrm{logit}(U)$.

**(a) (1)** $\sig(\operatorname{logit}(u)) = \dfrac{1}{1+e^{-\log\frac{u}{1-u}}}
= \dfrac{1}{1+\frac{1-u}{u}} = \dfrac{u}{u + (1-u)} = u$.
*Marks:* 1.

**(b) (3)** Since $\log$ is increasing and $u \mapsto u/(1-u)$ is increasing on
$(0,1)$:

$$
F_X(x) = \PP\!\left(\log\tfrac{U}{1-U} \le x\right)
= \PP\!\left(\tfrac{U}{1-U} \le e^{x}\right)
= \PP\!\big(U \le \tfrac{e^{x}}{1+e^{x}}\big)
= \PP\big(U \le \sig(x)\big) = \sig(x),
$$

the last step because $\PP(U \le c) = c$ for $c \in (0,1)$ and $\sig(x) \in (0,1)$.
*Marks:* 1 for each rearrangement step, 1 for invoking the uniform CDF. Deduct
nothing for not remarking on monotonicity, but note it if they invert an
inequality carelessly.

**(c) (3)** $f_X(x) = F_X'(x) = \sig'(x) = \sig(x)(1-\sig(x))$.
Writing $\sig(x) = 1/(1+e^{-x})$ and $1-\sig(x) = e^{-x}/(1+e^{-x})$ gives
$e^{-x}/(1+e^{-x})^2$; multiplying numerator and denominator by $e^{x}$ and using
$\cosh x = (e^x + e^{-x})/2$ gives $1/(2(\cosh x + 1))$.
It integrates to $1$ because $F_X = \sig$ runs from $0$ to $1$.
*Marks:* 1 for the derivative, 1 for showing the equivalences, 1 for the
normalisation argument (the CDF argument is the cleanest; accept direct
integration).

**(d) (2)** $f_X(-x) = \sig(-x)(1-\sig(-x)) = (1-\sig(x))\sig(x) = f_X(x)$, using
$\sig(-x) = 1 - \sig(x)$. A symmetric density with finite mean has mean at its
centre of symmetry, so $\EE[X] = 0$.
*Marks:* 1 for the symmetry, 1 for the conclusion. They must not just assert
mean $0$.

**(e) (1)** The **standard logistic distribution**. It was guaranteed because
$\sig$ *is* a CDF, and pushing a $\mathrm{Uniform}(0,1)$ through the inverse of a
CDF produces exactly the law with that CDF — the inverse-transform sampling
identity.
*Marks:* 1 for the name plus the inverse-transform reason. Name alone: 0.5,
round up.

**Worth saying in class.** $\Var(X) = \pi^2/3 \approx 3.290$; simulation with
$4\times10^5$ draws gave mean $+0.002$ and variance $3.282$. This is the same
"sampling is transport" identity the course uses for $Q(U)$ — here the target
just happens to be logistic.

---

## Problem 3 — Bernoulli to Binomial, and $\hat p$ (10)

*Setup:* A/B test on a checkout page; $n$ independent visitors, unknown conversion
probability $p$, $S$ conversions.

**(a) (1)** $\PP(x_i = x) = p^{x}(1-p)^{1-x}$ for $x \in \{0,1\}$.
*Marks:* 1. This single-expression trick is what makes (c) painless.

**(b) (3)** (i) A specific sequence with $k$ conversions has probability
$p^{k}(1-p)^{n-k}$ by independence — one factor $p$ per conversion and one
$(1-p)$ per non-conversion, and the *order* does not change the product.
(ii) There are $\binom{n}{k}$ such sequences (choose which of the $n$ visitors
converted).
(iii) Those sequences are disjoint events whose union is $\{S = k\}$, so their
probabilities add.
*Marks:* 1 each. Part (iii) is the one usually skipped; insist on it.

**(c) (2)**

$$
L(p) = \prod_{i=1}^n p^{x_i}(1-p)^{1-x_i} = p^{S}(1-p)^{n-S},
\qquad
\ell(p) = S\log p + (n-S)\log(1-p).
$$

*Marks:* 1 each.

**(d) (3)** $\ell'(p) = \dfrac{S}{p} - \dfrac{n-S}{1-p} = 0
\Rightarrow S(1-p) = (n-S)p \Rightarrow S = np \Rightarrow \boxed{\hat p = S/n}$.

Maximum because $\ell''(p) = -\dfrac{S}{p^2} - \dfrac{n-S}{(1-p)^2} < 0$ for all
$p \in (0,1)$ (both terms negative), so $\ell$ is strictly concave.
*Marks:* 1 for the derivative, 1 for solving, 1 for the second-derivative check.
The concavity mark is not a formality — do not award it for "it is obviously a
max".

Verified numerically: $n=200$, $S=70$; grid search over $p$ maximises at
$0.3500 = S/n$.

**(e) (1)** Nothing changes. The Binomial likelihood is
$\binom{n}{S}p^{S}(1-p)^{n-S}$; the coefficient does not involve $p$, so it is an
additive constant in $\ell$ and vanishes on differentiation. Same $\hat p$.
*Marks:* 1, requires "does not depend on $p$".

**Edge cases.** If $S = 0$ or $S = n$ the maximiser is at the boundary
($\hat p = 0$ or $1$) and $\ell'$ never vanishes in $(0,1)$. Worth a remark if a
student raises it; not required.

---

## Problem 4 — Uniform$(a,b)$ (10)

*Setup:* second-hand instrument with a lost datasheet; readings uniform on an
unknown $[a,b]$.

**(a) (3)**

$$
L(a,b) = \prod_{i=1}^n \frac{1}{b-a}\mathbf{1}\{a \le x_i \le b\}
= \frac{1}{(b-a)^n}\,\mathbf{1}\{a \le x_{(1)}\}\,\mathbf{1}\{x_{(n)} \le b\},
$$

where $x_{(1)} = \min_i x_i$ and $x_{(n)} = \max_i x_i$. The $n$ indicators
collapse into two because *all* observations lie in $[a,b]$ exactly when the
smallest and largest do.
*Marks:* 1 for $(b-a)^{-n}$, 1 for including indicators at all, 1 for collapsing
them to the min and max. **Omitting the indicator is the central error of this
problem** — without it the likelihood appears to increase without bound as
$b - a \to 0$.

**(b) (2)** Two reasons, either earns the marks if argued: the likelihood is not
differentiable in $a$ and $b$ (it jumps to $0$ as they cross the data), and where
it *is* differentiable the derivative never vanishes — $(b-a)^{-n}$ is strictly
decreasing in $b$ and strictly increasing in $a$, so there is no interior
stationary point. The maximum sits on the boundary of the feasible region.
*Marks:* 1 for identifying non-differentiability / boundary maximum, 1 for the
"derivative never zero" observation.

**(c) (3)** On the feasible set $\{a \le x_{(1)},\, b \ge x_{(n)}\}$ the
likelihood is $(b-a)^{-n}$, which is maximised by making $b - a$ **as small as
possible**. Feasibility forces $b - a \ge x_{(n)} - x_{(1)}$, and that lower
bound is attained at $a = x_{(1)}$, $b = x_{(n)}$, which is feasible. Hence
$\hat a = \min_i x_i$, $\hat b = \max_i x_i$.
*Marks:* 1 for "minimise the width", 1 for the feasibility bound, 1 for checking
the bound is attained.

**(d) (2)** Since $\hat a \ge a$ and $\hat b \le b$ always, $\hat b - \hat a \le b-a$
with probability $1$ — the estimate is **never** too wide and is almost surely too
narrow. So it is biased, and biased *downward*.
*Marks:* 1 for "biased", 1 for the correct direction with the containment reason.

**For your own reference** (not required of students): for
$\mathrm{Uniform}(a,b)$,
$\EE[x_{(1)}] = a + \frac{b-a}{n+1}$ and $\EE[x_{(n)}] = b - \frac{b-a}{n+1}$, so
$\EE[\hat b - \hat a] = \frac{n-1}{n+1}(b-a)$. Simulated at $a=2$, $b=7$, $n=10$
over $2\times10^5$ replicates: $\EE[\min] = 2.453$ (theory $2.4545$),
$\EE[\max] = 6.547$ (theory $6.5455$), width ratio $0.8187$ (theory $10/12 = 0.8182$).
The unbiased correction multiplies the width by $(n+1)/(n-1)$.

---

## Problem 5 — cross-entropy from maximum likelihood (10)

*Setup:* postal digit sorter, $K=10$ classes, logits $z_i=f_\theta(x_i)\in\mathbb{R}^K$,
$q_{ik}=e^{z_{ik}}/\sum_m e^{z_{im}}$, labels $y_i$ one-hot.

**(a) (2)** Positivity: $e^{z_{ik}}>0$ for every real $z_{ik}$, and the
denominator is a sum of positive terms, so $q_{ik}>0$. Normalisation:

$$
\sum_{k=1}^{K} q_{ik}
= \frac{\sum_{k=1}^{K} e^{z_{ik}}}{\sum_{m=1}^{K} e^{z_{im}}} = 1 ,
$$

the numerator and denominator being the same sum. Shift-invariance: replacing
$z_{ik}$ by $z_{ik}+c$,

$$
\frac{e^{z_{ik}+c}}{\sum_m e^{z_{im}+c}}
= \frac{e^{c}\,e^{z_{ik}}}{e^{c}\sum_m e^{z_{im}}}
= q_{ik} .
$$

So softmax is constant along the all-ones direction: only **$K-1$** of the $K$
logits are genuinely free. The map $\mathbb{R}^K \to$ (the $(K-1)$-simplex) is
onto but not injective, which is why implementations may pin $z_K = 0$ without
losing anything.

*Marks:* 1 for positivity **and** normalisation together, 1 for shift-invariance
with the $K-1$ conclusion. Accept "the extra degree of freedom is unidentifiable".

**(b) (2)** $y_i \mid x_i \sim \mathrm{Categorical}(q_i)$ — equivalently
$\mathrm{Multinomial}(1, q_i)$ — with pmf

$$
\PP(y_i \mid x_i, \theta) = \prod_{k=1}^{K} q_{ik}^{\,y_{ik}} .
$$

Because $y_i$ is one-hot, every factor with $y_{ik}=0$ is $q_{ik}^{0}=1$, so the
product collapses to $q_{i c_i}$, the predicted probability of the true class
$c_i$. This is the exact $K$-class analogue of $q^{y}(1-q)^{1-y}$.

*Marks:* 1 for naming Categorical/Multinoulli with $q_i$ as parameter, 1 for the
single-expression pmf. It must be **conditional on $x_i$**. Writing
$q_{i c_i}$ directly is fine and earns full marks if the one-hot product is also
given or clearly implied.

**(c) (3)**

$$
L(\theta) = \prod_{i=1}^{n}\prod_{k=1}^{K} q_{ik}^{\,y_{ik}},
\qquad
\ell(\theta) = \sum_{i=1}^{n}\sum_{k=1}^{K} y_{ik}\log q_{ik},
\qquad
-\tfrac{1}{n}\ell(\theta) = \mathrm{CE}(\theta).
$$

So **minimising cross-entropy is exactly maximising the likelihood** of the
observed labels under the assumed Categorical model; $-1/n$ is a monotone
rescaling, so it moves the objective's value but not its argmax.

The three assumptions:

1. **Form** — each label is Categorical, with its class probabilities given by
   the model output $\mathrm{softmax}(f_\theta(x_i))$. (Two things bundled: that
   the label is Categorical at all, and that the softmax link is the right
   parametrisation.)
2. **Across examples** — the labels are conditionally independent given the
   inputs, which is what licenses the product over $i$.
3. **The inputs** — $x_i$ are treated as fixed/given, not modelled. Nothing here
   assigns a distribution to $x$, so this is a *conditional* (discriminative)
   likelihood, not a joint model of $(x,y)$.

*Marks:* 1 for the likelihood and log, 1 for landing on $\mathrm{CE}$ with the
argmax remark, 1 for the assumptions — award the full point only if all three
appear. Assumption 3 is the one almost everyone omits and the one worth drawing
out in class.

**(d) (2)** Write the log-softmax in the form that makes the derivative trivial:

$$
\log q_k = z_k - \log\!\sum_{m} e^{z_m}
\;\Longrightarrow\;
\frac{\partial \log q_k}{\partial z_j}
= \delta_{kj} - \frac{e^{z_j}}{\sum_m e^{z_m}}
= \delta_{kj} - q_j .
$$

Then

$$
\frac{\partial \ell}{\partial z_j}
= -\sum_{k} y_k\big(\delta_{kj} - q_j\big)
= -y_j + q_j \underbrace{\sum_k y_k}_{=\,1}
= q_j - y_j .
$$

The constraint $\sum_k y_k = 1$ is used at exactly one place: pulling $q_j$ out
of the sum and collapsing what remains. Without one-hot (or at least
sum-to-one) labels the second term would carry a factor $\sum_k y_k \ne 1$.

*Marks:* 1 for $\partial \log q_k/\partial z_j = \delta_{kj}-q_j$ (however
obtained — quotient rule is fine but slower), 1 for the collapse to $q_j - y_j$
**with** the $\sum_k y_k = 1$ step identified. Do not award the second mark if
the student writes $q_j - y_j$ without ever using the constraint.

**(e) (1)** With $K=2$,

$$
q_2 = \frac{e^{z_2}}{e^{z_1}+e^{z_2}}
    = \frac{1}{1+e^{-(z_2-z_1)}} = \sig(z),
\qquad z := z_2 - z_1,
$$

after dividing numerator and denominator by $e^{z_2}$; and $q_1 = 1 - \sig(z)$.
Writing $y \in \{0,1\}$ for the indicator of class 2, the one-hot label is
$(1-y, y)$ and

$$
-\big[(1-y)\log q_1 + y\log q_2\big]
= -\big[y\log\sig(z) + (1-y)\log(1-\sig(z))\big],
$$

which is BCE. Two logits were one too many precisely by the shift-invariance of
(a): only the *difference* $z_2 - z_1$ is identifiable.

*Marks:* 1 for the reduction with the shift-invariance link. Getting
$q_2 = \sig(z_2-z_1)$ but not connecting it to (a) earns the mark only if the
BCE collapse is also shown.

**Why this is worth the time.** "Predicted minus observed", now in every
coordinate at once, is why softmax classifiers train as easily as they do, and
the same structure reappears throughout the course: the two-point posterior
$\PP(x_0 = +1 \mid x_\sigma) = \sig(2x/\sigma^2)$ is the $K=2$ case, and the
denoiser's loss has the same predicted-minus-observed shape. The binary case is
derived in the "binary cross-entropy is a likelihood" aside in tutorial 02 — this
problem is the general statement that aside is a special case of.

---

## Marking summary

| Problem | Topic | Points |
|:--|:--|--:|
| 1 | Beta: mean and variance by integration | 10 |
| 2 | Inverse sigmoid of a uniform → logistic | 10 |
| 3 | Bernoulli → Binomial; MLE of $p$ | 10 |
| 4 | Uniform$(a,b)$: MLE from the support | 10 |
| 5 | Softmax cross-entropy as maximum likelihood | 10 |
| | **Total** | **50** |

### Errors to expect

1. **Omitting the indicator in 4(a)** — the defining error of that problem.
2. Treating 4 as a calculus problem and reporting nonsense stationary points.
3. In 3(b), skipping the disjointness step and just asserting the coefficient.
4. In 5(c), missing that the inputs are unmodelled — the discriminative /
   generative distinction.
5. In 5(d), producing $q_j - y_j$ without ever invoking $\sum_k y_k = 1$, or
   grinding through the quotient rule instead of using
   $\log q_k = z_k - \log\sum_m e^{z_m}$.
6. In 5(a), verifying normalisation but skipping shift-invariance, and so missing
   that only $K-1$ logits are free.
7. In 1, attempting integration by parts rather than recognising the Beta kernel.
8. Asserting $\EE[X] = 0$ in 2(d) without the symmetry argument.
