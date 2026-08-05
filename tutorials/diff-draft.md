Probability-Flow ODEs in Score-Based Diffusion Models

From Forward VP Diffusion to Deterministic Sampling

1. Introduction

Score-based diffusion models are usually introduced as stochastic denoising procedures:

1. Gradually add Gaussian noise to data.
2. Learn how to reverse this corruption.
3. Start from Gaussian noise and iteratively generate a sample.

This description is correct, but it hides an important alternative interpretation.

A score-based diffusion model can also be viewed as learning a time-dependent velocity field that transports a simple Gaussian distribution into the data distribution. Once this velocity field is known, samples can be generated deterministically by solving an ordinary differential equation.

This deterministic dynamics is called the probability-flow ODE.

The central idea is:

\boxed{
\text{Learn local score information}
\quad\Longrightarrow\quad
\text{construct a velocity field}
\quad\Longrightarrow\quad
\text{integrate a global transport map}.
}

This tutorial develops that interpretation carefully.

We will proceed through the following steps:

1. Define the forward Variance-Preserving diffusion.
2. Explain how the noise schedule determines the forward SDE.
3. Derive the family of noisy distributions.
4. Define the score function.
5. Explain how a neural network learns the score.
6. Derive the probability-flow ODE.
7. Interpret it as particle motion.
8. Explain how to numerically integrate from X_T to X_0.
9. Work through the symmetric two-point distribution.
10. Clarify the relation between the direct sign map and incremental diffusion sampling.

⸻

2. The generative modeling problem

Let the data distribution be

p_0(x)=p_{\mathrm{data}}(x).

We can sample training examples from p_0, but we generally cannot evaluate its density or directly sample new points from it without access to the dataset.

We would like to transform a simple distribution, typically

p_T(x)\approx\mathcal N(0,I),

into the data distribution.

Thus the generative problem is

\boxed{
\mathcal N(0,I)
\longrightarrow
p_{\mathrm{data}}.
}

One possible approach would be to learn a direct map

T:\mathbb R^d\rightarrow\mathbb R^d

such that

X_T\sim\mathcal N(0,I)
\quad\Longrightarrow\quad
T(X_T)\sim p_{\mathrm{data}}.

Diffusion models take a different approach.

Instead of learning T directly, they construct a continuous path of distributions

p_0,p_t,p_T

and learn the local information required to move through that path.

⸻

3. The forward stochastic differential equation

A general diffusion process is defined by the stochastic differential equation

\boxed{
dX_t=f(X_t,t)\,dt+g(t)\,dW_t.
}

Each symbol has a specific meaning.

3.1 State variable X_t

The random variable

X_t\in\mathbb R^d

is the sample at diffusion time t.

At the beginning,

X_0\sim p_{\mathrm{data}}.

As t increases, information about the original sample is gradually destroyed.

⸻

3.2 Time t

The variable t indexes the amount of corruption.

It need not represent physical time. It is simply a continuous noise-level parameter.

Usually,

t\in[0,T].

The endpoint t=0 corresponds to data, while t=T corresponds to nearly Gaussian noise.

⸻

3.3 Drift f(x,t)

The function

f(x,t)

describes deterministic motion.

If the stochastic term were removed, the dynamics would be

\frac{dX_t}{dt}=f(X_t,t).

The drift therefore specifies how a particle would move in the absence of random noise.

⸻

3.4 Diffusion coefficient g(t)

The scalar or matrix-valued function

g(t)

controls the strength of the stochastic perturbation.

Larger g(t) means more noise is injected per unit time.

⸻

3.5 Brownian motion W_t

The process

W_t

is standard Brownian motion.

Its infinitesimal increment satisfies

dW_t\sim\mathcal N(0,dt\,I).

Thus the stochastic term

g(t)dW_t

adds Gaussian noise.

⸻

4. Variance-Preserving diffusion

A particularly important forward process is the Variance-Preserving, or VP, diffusion:

\boxed{
dX_t
=
-\frac12\beta(t)X_t\,dt
+
\sqrt{\beta(t)}\,dW_t.
}

Here,

f(x,t)=-\frac12\beta(t)x,

and

g(t)=\sqrt{\beta(t)}.

The function

\beta(t)>0

is called the noise schedule.

⸻

5. Role of the noise schedule

The noise schedule determines how quickly information is destroyed.

Once \beta(t) is selected, both the drift and diffusion terms are known:

\boxed{
\beta(t)
\Longrightarrow
f(x,t)=-\frac12\beta(t)x,
\qquad
g(t)=\sqrt{\beta(t)}.
}

Thus the schedule determines the entire forward stochastic process.

A small value of \beta(t) means slow corruption.

A large value means rapid corruption.

A commonly used schedule gradually increases \beta(t), so that early diffusion steps make small perturbations while later steps strongly destroy the remaining signal.

⸻

6. Why is it called variance preserving?

Consider a simple case where

X_0\sim\mathcal N(0,I).

The forward VP process keeps the variance equal to I.

The deterministic term

-\frac12\beta(t)X_t

contracts the sample toward zero.

The stochastic term

\sqrt{\beta(t)}dW_t

adds variance.

These two effects balance each other.

The drift prevents variance from growing without bound, while the diffusion term continually adds noise.

Hence the name Variance-Preserving diffusion.

For arbitrary data, the distribution is not Gaussian at intermediate times, but as t grows, it approaches a standard Gaussian while maintaining a controlled variance scale.

⸻

7. Closed-form forward corruption

The VP SDE has the closed-form conditional solution

\boxed{
X_t=\alpha_tX_0+\sigma_t\epsilon,
}

where

\epsilon\sim\mathcal N(0,I),

and

\alpha_t
=
\exp\left(
-\frac12\int_0^t\beta(s)\,ds
\right),

\sigma_t^2=1-\alpha_t^2.

Different papers sometimes use a_t, \bar\alpha_t^{1/2}, or other notation for \alpha_t.

The interpretation is simple:

\boxed{
\text{noisy sample}
=
\text{attenuated clean sample}
+
\text{Gaussian noise}.
}

At t=0,

\alpha_0=1,
\qquad
\sigma_0=0,

so

X_0=X_0.

At large t,

\alpha_t\rightarrow0,
\qquad
\sigma_t\rightarrow1,

and therefore

X_t\approx\epsilon\sim\mathcal N(0,I).

⸻

8. What the forward process really constructs

The purpose of the forward process is not merely to corrupt data.

It constructs a continuous sequence of distributions

\boxed{
p_0
\rightarrow
p_t
\rightarrow
p_T.
}

At t=0,

p_0=p_{\mathrm{data}}.

At t=T,

p_T\approx\mathcal N(0,I).

The intermediate density is

p_t(x)
=
\int
p_t(x\mid x_0)p_0(x_0)\,dx_0.

Since

p_t(x\mid x_0)
=
\mathcal N(x;\alpha_tx_0,\sigma_t^2I),

the data distribution is progressively convolved with Gaussian noise.

This sequence of smoothed densities is the path through which the model will later transport probability mass.

⸻

9. The score function

For every intermediate distribution p_t, define its score:

\boxed{
s_t(x)
=
\nabla_x\log p_t(x).
}

The score is a vector in the same dimension as x.

It points in the direction in which the log-density increases most rapidly.

Since the logarithm is monotonic, it also points toward increasing probability density.

⸻

9.1 Geometric interpretation

Imagine the probability density as a landscape.

Regions of high probability are mountains.

Regions of low probability are valleys.

Then

\nabla_x\log p_t(x)

points uphill.

The score therefore gives local geometric information:

At location x and noise level t, which direction leads toward more probable samples?

The score does not tell us the final destination directly.

It gives only a local direction.

⸻

9.2 Score of a Gaussian

For

p(x)=\mathcal N(\mu,\sigma^2I),

the score is

\nabla_x\log p(x)
=
-\frac{x-\mu}{\sigma^2}.

It points toward the mean.

For a standard Gaussian,

p(x)=\mathcal N(0,I),

we obtain

\boxed{
\nabla_x\log p(x)=-x.
}

⸻

10. Why the score is unknown

The schedule \beta(t) determines the conditional corruption distribution

p_t(x_t\mid x_0).

However, the marginal

p_t(x_t)
=
\int p_t(x_t\mid x_0)p_0(x_0)\,dx_0

depends on the unknown data distribution.

We therefore cannot directly evaluate

\nabla\log p_t(x).

This is the unknown quantity learned by a neural network.

⸻

11. Neural score estimation

A neural network

s_\theta(x,t)

is trained to approximate

s_t(x)=\nabla_x\log p_t(x).

The network receives:

* a noisy sample x_t,
* the corresponding time or noise level t,

and returns a vector with the same shape as x_t.

The network therefore learns a time-dependent vector field.

⸻

12. How training examples are generated

Training is possible because the forward corruption process is known.

Given a clean training example

x_0\sim p_{\mathrm{data}},

we sample a time

t\sim p(t),

and noise

\epsilon\sim\mathcal N(0,I).

We construct

\boxed{
x_t=\alpha_tx_0+\sigma_t\epsilon.
}

This gives an exact noisy sample at arbitrary time t without numerically simulating the entire forward SDE.

⸻

13. Conditional score target

The conditional distribution is

p_t(x_t\mid x_0)
=
\mathcal N(\alpha_tx_0,\sigma_t^2I).

Its score is analytically known:

\begin{aligned}
\nabla_{x_t}\log p_t(x_t\mid x_0)
&=
-\frac{x_t-\alpha_tx_0}{\sigma_t^2}\\
&=
-\frac{\epsilon}{\sigma_t}.
\end{aligned}

Thus a denoising score-matching objective is

\boxed{
\mathcal L(\theta)
=
\mathbb E
\left[
\lambda(t)
\left\|
s_\theta(x_t,t)
+
\frac{\epsilon}{\sigma_t}
\right\|^2
\right],
}

where \lambda(t) is an optional weighting function.

Even though the target uses the conditional score, the optimal neural network recovers the marginal score

\nabla\log p_t(x_t).

⸻

14. Equivalent noise prediction

Many implementations train a network

\epsilon_\theta(x_t,t)

to predict the injected noise.

Because

s_t(x_t)
=
-\frac{\epsilon}{\sigma_t}

for the conditional Gaussian corruption target, the score and noise predictions are related by

\boxed{
s_\theta(x_t,t)
=
-\frac{\epsilon_\theta(x_t,t)}{\sigma_t}.
}

Thus score prediction and noise prediction are alternative parameterizations of the same information.

⸻

15. From the score to a deterministic velocity field

The forward SDE is

dX_t=f(X_t,t)\,dt+g(t)\,dW_t.

Its density evolves according to the Fokker–Planck equation:

\boxed{
\frac{\partial p_t}{\partial t}
=
-\nabla\cdot(f p_t)
+
\frac12g(t)^2\Delta p_t.
}

The first term represents deterministic transport by the drift.

The second term represents spreading caused by Brownian motion.

Now consider deterministic particle motion

\frac{dX_t}{dt}=v(X_t,t).

The corresponding density evolves according to the continuity equation:

\boxed{
\frac{\partial p_t}{\partial t}
=
-\nabla\cdot(p_tv).
}

We seek a velocity field v whose continuity equation matches the Fokker–Planck equation.

⸻

16. Derivation of the probability-flow velocity

Choose

v(x,t)
=
f(x,t)
-
\frac12g(t)^2\nabla_x\log p_t(x).

Then

p_t v
=
p_tf
-
\frac12g(t)^2p_t\nabla\log p_t.

Using

p_t\nabla\log p_t=\nabla p_t,

we get

p_tv
=
p_tf
-
\frac12g(t)^2\nabla p_t.

Therefore,

\begin{aligned}
-\nabla\cdot(p_tv)
&=
-\nabla\cdot(p_tf)
+
\frac12g(t)^2\nabla\cdot(\nabla p_t)\\
&=
-\nabla\cdot(p_tf)
+
\frac12g(t)^2\Delta p_t.
\end{aligned}

This is exactly the Fokker–Planck equation.

Hence the deterministic ODE

\boxed{
\frac{dX_t}{dt}
=
f(X_t,t)
-
\frac12g(t)^2\nabla\log p_t(X_t)
}

has the same marginal densities p_t as the original forward SDE.

This is the probability-flow ODE.

⸻

17. Probability-flow ODE for VP diffusion

For VP diffusion,

f(x,t)=-\frac12\beta(t)x,

and

g(t)^2=\beta(t).

Therefore,

\boxed{
\frac{dX_t}{dt}
=
-\frac12\beta(t)X_t
-
\frac12\beta(t)s_t(X_t).
}

Equivalently,

\boxed{
\frac{dX_t}{dt}
=
-\frac12\beta(t)
\left[
X_t+s_t(X_t)
\right].
}

With a learned score,

\boxed{
\frac{dX_t}{dt}
=
-\frac12\beta(t)
\left[
X_t+s_\theta(X_t,t)
\right].
}

⸻

18. Is the score the velocity?

No.

The score is one component of the velocity field.

The probability-flow velocity is

\boxed{
v(x,t)
=
f(x,t)
-
\frac12g(t)^2s_t(x).
}

Thus,

\boxed{
\text{velocity}
=
\text{known forward drift}
+
\text{score-dependent correction}.
}

For VP diffusion,

v(x,t)
=
-\frac12\beta(t)x
-
\frac12\beta(t)s_t(x).

The score gives the geometry of the current distribution.

The schedule determines how strongly that geometry influences motion.

⸻

19. Newtonian and kinematic interpretation

The equation

\frac{dX_t}{dt}=v(X_t,t)

is the standard equation for particle motion under a velocity field.

It is more precisely a kinematic description than a full Newtonian one.

Newton’s second law normally describes acceleration:

m\frac{d^2X_t}{dt^2}=F(X_t,t).

The probability-flow ODE is first order:

\frac{dX_t}{dt}=v(X_t,t).

It directly specifies velocity rather than force.

A useful analogy is fluid flow.

Imagine that every point in space has an arrow attached to it.

The arrow at (x,t) is

v(x,t).

A particle located at x follows that arrow.

As the particle moves, the arrow changes because:

1. the particle reaches a new position;
2. the time-dependent field changes.

The complete trajectory is obtained by continuously following these local arrows.

⸻

20. Probability as a flowing fluid

Suppose many particles are sampled from p_T.

Each particle follows

\frac{dX_t}{dt}=v(X_t,t).

Individually, the particles move deterministically.

Collectively, their density changes.

The continuity equation ensures that probability mass is conserved:

\frac{\partial p_t}{\partial t}
+
\nabla\cdot(p_tv)=0.

Therefore, the term probability flow means:

Probability mass flows through space under a deterministic velocity field.

No Brownian noise is added in the ODE.

Once the starting point X_T is fixed, the complete trajectory is deterministic.

⸻

21. Forward versus reverse use of the ODE

The probability-flow ODE reproduces the same distribution path p_t as the forward SDE when integrated from 0 to T.

However, for generation, we solve it backward:

t=T\longrightarrow0.

We begin with

X_T\sim p_T\approx\mathcal N(0,I),

and solve

\frac{dX_t}{dt}=v_\theta(X_t,t)

toward t=0.

The resulting endpoint approximates a data sample:

X_0\sim p_{\mathrm{data}}.

⸻

22. What is known during sampling?

Once the model has been trained, the following quantities are available.

Known from the schedule

The schedule supplies

\beta(t).

For VP diffusion, this determines

f(x,t)=-\frac12\beta(t)x

and

g(t)^2=\beta(t).

It also determines

\alpha_t

and

\sigma_t.

Learned from data

The neural network supplies

s_\theta(x,t)\approx\nabla\log p_t(x).

Computed from both

The velocity is

\boxed{
v_\theta(x,t)
=
f(x,t)
-
\frac12g(t)^2s_\theta(x,t).
}

Therefore, after training, the entire right-hand side of the ODE is known.

⸻

23. Is the trajectory analytically known?

Usually not.

Given

X_T=z,

the ODE defines a unique flow map

X_0=\Phi_{T\to0}(z).

Formally,

X_0
=
X_T+
\int_T^0v(X_t,t)\,dt.

However, this is an implicit integral because v depends on the unknown trajectory X_t.

For realistic neural scores, there is no closed-form symbolic solution.

The trajectory must be computed numerically.

⸻

24. Numerical solution of the probability-flow ODE

Choose a descending time grid:

T=t_N>t_{N-1}>\cdots>t_1>t_0=\varepsilon,

where \varepsilon>0 is a small final time.

Define

\Delta t_k=t_{k-1}-t_k<0.

The negative sign reflects backward integration.

⸻

25. Complete sampling procedure

Step 1: Sample terminal noise

Draw

\boxed{
X_T\sim\mathcal N(0,I).
}

Set

X\leftarrow X_T.

⸻

Step 2: Select the current time

Begin at

t=t_N=T.

⸻

Step 3: Evaluate the score

At the current state X, compute

\boxed{
s=s_\theta(X,t).
}

This is the local score of the noisy distribution at the current noise level.

⸻

Step 4: Evaluate the schedule

Compute

\beta(t).

For VP diffusion,

f(X,t)=-\frac12\beta(t)X,

and

g(t)^2=\beta(t).

⸻

Step 5: Construct the velocity

Compute

\boxed{
v
=
f(X,t)-\frac12g(t)^2s.
}

For VP diffusion,

\boxed{
v
=
-\frac12\beta(t)(X+s).
}

⸻

Step 6: Take a numerical step

Using explicit Euler integration,

\boxed{
X\leftarrow X+\Delta t\,v.
}

Since

\Delta t<0,

this moves the particle backward in diffusion time.

⸻

Step 7: Move to the next time

Set

t\leftarrow t+\Delta t.

Then recompute the score at the new location and time.

⸻

Step 8: Repeat

Continue until

t\approx0.

Return the final state as the generated sample.

⸻

26. Euler sampler

The probability-flow Euler sampler is

\boxed{
\begin{aligned}
&X\sim\mathcal N(0,I),\\
&\text{for }k=N,N-1,\ldots,1:\\
&\qquad s\leftarrow s_\theta(X,t_k),\\
&\qquad v\leftarrow
f(X,t_k)-\frac12g(t_k)^2s,\\
&\qquad X\leftarrow
X+(t_{k-1}-t_k)v,\\
&\text{return }X.
\end{aligned}
}

For VP diffusion,

\boxed{
\begin{aligned}
&X\sim\mathcal N(0,I),\\
&\text{for }k=N,N-1,\ldots,1:\\
&\qquad s\leftarrow s_\theta(X,t_k),\\
&\qquad v\leftarrow
-\frac12\beta(t_k)(X+s),\\
&\qquad X\leftarrow
X+(t_{k-1}-t_k)v,\\
&\text{return }X.
\end{aligned}
}

⸻

27. Why the score must be recomputed

The score cannot be evaluated only once.

At every step,

s_\theta(X_t,t)

changes because both arguments change.

The particle moves:

X_t\rightarrow X_{t-\Delta t}.

The noise level changes:

t\rightarrow t-\Delta t.

Therefore, each step follows the pattern

\boxed{
\text{evaluate score}
\rightarrow
\text{construct velocity}
\rightarrow
\text{move}
\rightarrow
\text{repeat}.
}

The sampler is incrementally reconstructing a global transport map from local information.

⸻

28. Heun’s method

Euler assumes the velocity is constant across the step.

A more accurate second-order method is Heun’s method.

First compute

v_k=v_\theta(X_k,t_k).

Take a provisional step:

\widetilde X_{k-1}
=
X_k+\Delta t_kv_k.

Evaluate the velocity at the provisional endpoint:

\widetilde v_{k-1}
=
v_\theta(\widetilde X_{k-1},t_{k-1}).

Then use the average velocity:

\boxed{
X_{k-1}
=
X_k
+
\frac{\Delta t_k}{2}
\left(
v_k+\widetilde v_{k-1}
\right).
}

Heun’s method usually produces greater accuracy for the same number of time intervals, but it uses two network evaluations per step.

⸻

29. Higher-order and adaptive solvers

Since the probability-flow dynamics is an ODE, standard ODE solvers can be used:

* Euler;
* midpoint;
* Heun;
* Runge–Kutta;
* adaptive Runge–Kutta;
* multistep methods;
* diffusion-specific solvers.

Adaptive solvers choose the step size based on estimated numerical error.

However, each function evaluation requires running the score network, so the principal computational cost is the number of neural function evaluations.

This is often abbreviated as NFE.

⸻

30. Direct transport versus incremental transport

Suppose the final deterministic transport map is

T:X_T\mapsto X_0.

The probability-flow ODE does not usually represent T explicitly.

Instead,

T

is represented implicitly as the composition of many infinitesimal maps:

X_{t-\Delta t}
\approx
X_t+\Delta t\,v(X_t,t).

Thus,

\boxed{
T
=
\lim_{\Delta t\to0}
\prod_t
\left(
I+\Delta t\,v_t
\right).
}

Here the product denotes composition in time order.

The global map is reconstructed by integrating the local velocity field.

⸻

31. Symmetric two-point example

Consider the limiting data distribution

\boxed{
p_0(x)
=
\frac12\delta_{-1}(x)
+
\frac12\delta_{+1}(x).
}

Equivalently,

X_0\in\{-1,+1\}

with equal probability.

The natural one-shot transport from a standard Gaussian is

\boxed{
X_0=\operatorname{sign}(X_T).
}

Indeed, since

P(X_T>0)=P(X_T<0)=\frac12,

the sign map sends exactly half the Gaussian mass to each atom.

⸻

32. Forward corruption of the two-point distribution

Under VP diffusion,

X_t=\alpha_tX_0+\sigma_t\epsilon.

Conditioned on the component,

X_t\mid X_0=+1
\sim
\mathcal N(\alpha_t,\sigma_t^2),

and

X_t\mid X_0=-1
\sim
\mathcal N(-\alpha_t,\sigma_t^2).

Therefore,

\boxed{
p_t(x)
=
\frac12\mathcal N(x;-\alpha_t,\sigma_t^2)
+
\frac12\mathcal N(x;+\alpha_t,\sigma_t^2).
}

At high noise, the two components overlap strongly.

At low noise, they separate sharply.

⸻

33. Posterior component probability

Let

C\in\{-1,+1\}

denote the original component.

Using Bayes’ rule,

P(C=+1\mid X_t=x)
=
\frac{
\exp\left[-(x-\alpha_t)^2/(2\sigma_t^2)\right]
}{
\exp\left[-(x-\alpha_t)^2/(2\sigma_t^2)\right]
+
\exp\left[-(x+\alpha_t)^2/(2\sigma_t^2)\right]
}.

This simplifies to

\boxed{
P(C=+1\mid X_t=x)
=
\frac{1}{
1+\exp\left(-2\alpha_tx/\sigma_t^2\right)
}.
}

The posterior mean of the component is

\begin{aligned}
\mathbb E[C\mid X_t=x]
&=
P(C=+1\mid x)-P(C=-1\mid x)\\
&=
\tanh\left(
\frac{\alpha_tx}{\sigma_t^2}
\right).
\end{aligned}

Thus,

\boxed{
\widehat X_0(x,t)
=
\tanh\left(
\frac{\alpha_tx}{\sigma_t^2}
\right).
}

This is a smooth, noise-dependent approximation to the sign function.

⸻

34. Score of the two-component mixture

The score is

\boxed{
s_t(x)
=
\frac{
-x+\alpha_t
\tanh\left(
\alpha_tx/\sigma_t^2
\right)
}{
\sigma_t^2
}.
}

The first term,

-\frac{x}{\sigma_t^2},

resembles the score of a Gaussian centered at zero.

The second term introduces the bimodal structure.

For positive x, the hyperbolic tangent becomes positive and favors the +1 component.

For negative x, it favors the -1 component.

⸻

35. Limiting sign function

As t\rightarrow0,

\alpha_t\rightarrow1,
\qquad
\sigma_t^2\rightarrow0.

Therefore, for x\neq0,

\frac{\alpha_tx}{\sigma_t^2}
\rightarrow
\begin{cases}
+\infty,&x>0,\\
-\infty,&x<0.
\end{cases}

Since

\tanh(z)\rightarrow
\begin{cases}
+1,&z\rightarrow+\infty,\\
-1,&z\rightarrow-\infty,
\end{cases}

we obtain

\boxed{
\widehat X_0(x,t)
\rightarrow
\operatorname{sign}(x).
}

Thus the Bayesian denoiser gradually sharpens from a smooth \tanh into the discontinuous sign map.

⸻

36. Probability-flow velocity for the example

For VP diffusion,

v_t(x)
=
-\frac12\beta(t)
\left[
x+s_t(x)
\right].

Substituting the exact score,

\boxed{
v_t(x)
=
-\frac12\beta(t)
\left[
x+
\frac{
-x+\alpha_t\tanh(\alpha_tx/\sigma_t^2)
}{
\sigma_t^2
}
\right].
}

This is a deterministic, time-dependent nonlinear velocity field.

To generate a sample:

1. Draw X_T\sim\mathcal N(0,1).
2. Evaluate the exact score at X_T.
3. Construct the velocity.
4. Move a small step backward.
5. Recompute the score.
6. Continue until t\approx0.

⸻

37. Why positive points end at +1

The model and the distribution are symmetric:

s_t(-x)=-s_t(x).

The origin is therefore the boundary between two basins.

In one dimension, trajectories of a smooth ODE cannot cross before the singular endpoint.

Thus a trajectory that begins with

X_T>0

remains on the positive side.

Similarly,

X_T<0

remains negative.

As the endpoint distribution collapses to two atoms,

X_T>0\rightarrow+1,

and

X_T<0\rightarrow-1.

Hence,

\boxed{
X_0=\operatorname{sign}(X_T).
}

⸻

38. Is reverse diffusion merely a numerical sign function?

For this special example, the endpoint map is indeed the sign function.

The direct solution is

X_0=\operatorname{sign}(X_T).

The probability-flow ODE reaches the same endpoint incrementally.

Thus one may write

\boxed{
\operatorname{sign}
=
\text{integrated score-driven probability flow}.
}

However, one qualification matters.

The ODE solver is not numerically approximating a known formula such as the sign function in general. It is solving a differential equation whose endpoint happens, in this special symmetric limit, to equal the sign map.

For arbitrary data distributions, the endpoint transport map is not known in advance.

⸻

39. Finite component variance

Suppose instead that

p_0(x)
=
\frac12\mathcal N(-1,\tau^2)
+
\frac12\mathcal N(+1,\tau^2).

The target is now continuous.

The probability-flow map is no longer exactly the sign function.

In one dimension, the deterministic order-preserving transport is characterized by

\boxed{
X_0
=
F_0^{-1}\bigl(F_T(X_T)\bigr).
}

If

p_T=\mathcal N(0,1),

then

\boxed{
X_0
=
F_0^{-1}\bigl(\Phi(X_T)\bigr).
}

As

\tau\rightarrow0,

this quantile transport converges almost surely to

\operatorname{sign}(X_T).

⸻

40. Posterior denoiser versus probability-flow endpoint

A common confusion is to identify the posterior mean

\mathbb E[X_0\mid X_t=x]

with the final ODE endpoint.

They are not generally the same object.

For VP diffusion,

\boxed{
\mathbb E[X_0\mid X_t=x]
=
\frac{x+\sigma_t^2s_t(x)}{\alpha_t}.
}

This gives a one-step estimate of the original clean sample.

The probability-flow endpoint instead solves

\frac{dX_t}{dt}
=
f(X_t,t)
-
\frac12g(t)^2s_t(X_t)

using the score field at every time.

Thus,

\boxed{
\text{single denoising estimate}
\neq
\text{integrated transport trajectory}.
}

In the two-point limit, both eventually approach the same sign decision, but conceptually they remain different.

⸻

41. What the forward process learns for us

The forward VP process performs three critical functions.

41.1 It creates a tractable endpoint

It converts the unknown data distribution into a nearly standard Gaussian.

41.2 It creates supervised corruption pairs

We can generate

(x_0,x_t,t,\epsilon)

exactly.

41.3 It creates local score targets

The Gaussian corruption gives an analytically known conditional score.

Thus the forward process is carefully designed to manufacture the training signal needed to learn the local geometry of p_t.

The forward process does not learn anything itself.

It constructs the conditions under which score learning becomes possible.

⸻

42. What the reverse process learns

The reverse process does not learn a separate dynamics after training.

The neural network learns

s_\theta(x,t).

During reverse generation, this learned score is inserted into either:

* the reverse-time SDE;
* the probability-flow ODE.

For the probability-flow ODE, the score determines the deterministic velocity correction needed to transport probability mass through the sequence of densities.

A more precise statement than “it transports particles having higher likelihood” is:

It moves particles according to a velocity field whose induced density evolution matches the prescribed family p_t.

The score points toward locally increasing density, but the full velocity also contains the forward drift and schedule-dependent scaling.

⸻

43. Local likelihood versus global transport

The score is local:

s_t(x)=\nabla\log p_t(x).

It says how density changes around x.

The endpoint map is global:

X_0=\Phi_{T\to0}(X_T).

It says where the complete trajectory ends.

The ODE connects the two:

\boxed{
\text{local score field}
\quad\xrightarrow{\text{integration}}\quad
\text{global deterministic transport}.
}

This is the deepest geometric interpretation of the probability-flow ODE.

⸻

44. Complete conceptual pipeline

The full procedure can be summarized as follows.

Forward construction

Choose a schedule:

\beta(t).

This determines

f(x,t)

and

g(t).

The resulting VP diffusion constructs

p_0\rightarrow p_t\rightarrow p_T.

Training

Sample

x_0\sim p_{\mathrm{data}},
\qquad
t,
\qquad
\epsilon\sim\mathcal N(0,I),

and form

x_t=\alpha_tx_0+\sigma_t\epsilon.

Train

s_\theta(x_t,t)

to approximate

\nabla\log p_t(x_t).

Sampling

Draw

X_T\sim\mathcal N(0,I).

Construct

v_\theta(x,t)
=
f(x,t)-\frac12g(t)^2s_\theta(x,t).

Numerically integrate

\frac{dX_t}{dt}=v_\theta(X_t,t)

from T to 0.

Return

X_0.

⸻

45. Minimal algorithmic summary

Training

\boxed{
\begin{aligned}
&x_0\sim p_{\mathrm{data}},\\
&t\sim p(t),\\
&\epsilon\sim\mathcal N(0,I),\\
&x_t=\alpha_tx_0+\sigma_t\epsilon,\\
&\theta\leftarrow
\arg\min_\theta
\left\|
s_\theta(x_t,t)+\epsilon/\sigma_t
\right\|^2.
\end{aligned}
}

Sampling

\boxed{
\begin{aligned}
&X_T\sim\mathcal N(0,I),\\
&v_\theta(x,t)
=
f(x,t)-\frac12g(t)^2s_\theta(x,t),\\
&\frac{dX_t}{dt}=v_\theta(X_t,t),\\
&\text{integrate from }T\text{ to }0,\\
&\text{return }X_0.
\end{aligned}
}

⸻

46. Main takeaways

1. The VP noise schedule \beta(t) determines the drift f, diffusion coefficient g, and corruption parameters \alpha_t,\sigma_t.
2. The forward process constructs a smooth family of noisy distributions connecting data to Gaussian noise.
3. The only unknown required for reverse generation is the score

\nabla\log p_t(x).

4. A neural network learns this score from synthetically generated noisy samples.
5. The score is not itself the probability-flow velocity.
6. The deterministic velocity is

v=f-\frac12g^2s.

7. The probability-flow ODE moves particles deterministically while reproducing the same marginal distribution path as the diffusion SDE.
8. Given X_T, the endpoint X_0 is obtained by numerically integrating the ODE backward.
9. Each numerical step performs:

\text{score evaluation}
\rightarrow
\text{velocity construction}
\rightarrow
\text{small transport update}.

10. In the symmetric two-point limit, the integrated probability-flow map becomes

X_0=\operatorname{sign}(X_T).

⸻

47. Final interpretation

The probability-flow ODE offers a different way to understand score-based diffusion models.

The model is not merely learning to remove Gaussian noise.

It learns the local geometry of a continuous family of probability distributions.

The noise schedule constructs that family.

The score network estimates its local log-density gradients.

The probability-flow equation converts those gradients into a deterministic velocity field.

The numerical ODE solver integrates that field.

The final result is a global transport map:

\boxed{
\mathcal N(0,I)
\longrightarrow
p_{\mathrm{data}}.
}

In the simple two-point example, the global map is the sign function. In realistic high-dimensional problems, the map is not available in closed form, but the same principle applies: the global generative transformation is obtained by integrating locally learned score information.