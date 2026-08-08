# An Intuitive Introduction to Probability Spaces, Events, and Random Variables

## 1. Motivation

Probability theory begins with a simple question:

> **What are the possible outcomes of an experiment, and how can we
> reason about uncertainty?**

Whether we toss a coin, roll a die, measure tomorrow's temperature, or
observe stock prices, probability theory provides a unified mathematical
framework for describing uncertainty.

The key objects in this framework are:

-   **Sample Space**
-   **Sigma Algebra (Events)**
-   **Probability Measure**
-   **Random Variable**

Although these concepts are introduced together, they play very
different roles.

------------------------------------------------------------------------

# 2. Step 1: The Sample Space

Every probabilistic experiment has a collection of all possible
outcomes.

This collection is called the **sample space**, denoted by

\[ `\Omega`{=tex}. \]

An element of the sample space is called an **outcome** (or elementary
outcome).

### Example: Tossing a Coin

Possible outcomes are

\[ `\Omega`{=tex}={H,T}. \]

Exactly one outcome occurs.

If the coin lands Heads,

\[ `\omega`{=tex}=H. \]

### Example: Rolling a Die

For a six-sided die,

\[ `\Omega`{=tex}={1,2,3,4,5,6}. \]

Exactly one outcome occurs.

------------------------------------------------------------------------

# 3. Step 2: Events

An **event** is any subset of the sample space.

For the die,

-   `{2,4,6}` → "Even"
-   `{1,2,3}` → "At most 3"
-   `{6}` → "Exactly 6"
-   `Ω` → Certain event
-   `∅` → Impossible event

Exactly **one outcome** occurs, but **many events** containing that
outcome occur simultaneously.

------------------------------------------------------------------------

# 4. Power Set and Sigma Algebra

The collection of all subsets of the sample space is called the **power
set**.

For a die,

\[ \|`\Omega`{=tex}\|=6, \]

so the power set contains

\[ 2\^6=64 \]

subsets.

For finite sample spaces, we usually take the sigma algebra to be the
entire power set.

Thus,

\[ `\mathcal `{=tex}F=2\^`\Omega`{=tex}. \]

------------------------------------------------------------------------

# 5. Probability Measure

A probability measure assigns probabilities to events.

\[ P:`\mathcal `{=tex}F`\rightarrow[0,1]`{=tex}. \]

For a fair die,

-   (P({4})=1/6)
-   (P({2,4,6})=1/2)
-   (P(`\Omega`{=tex})=1)
-   (P(`\emptyset`{=tex})=0)

The triple

\[ (`\Omega`{=tex},`\mathcal `{=tex}F,P) \]

is called the **probability space**.

------------------------------------------------------------------------

# 6. Random Variables

A random variable is **not** a function from events to numbers.

Instead,

\[ X:`\Omega`{=tex}`\rightarrow`{=tex}`\mathbb `{=tex}R. \]

It assigns a real number to every elementary outcome.

## Identity Random Variable

\[ X(`\omega`{=tex})=`\omega`{=tex}. \]

For a die,

-   X(1)=1
-   X(2)=2
-   ...
-   X(6)=6

## Even-Odd Indicator

Suppose we only care whether the outcome is even or odd.

\[ Y(`\omega`{=tex})=
```{=tex}
\begin{cases}
0,&\omega\in\{2,4,6\}\\
1,&\omega\in\{1,3,5\}.
\end{cases}
```
\]

Notice that Y does **not** map the event "even" to 0.

Instead,

-   Y(2)=0
-   Y(4)=0
-   Y(6)=0
-   Y(1)=1
-   Y(3)=1
-   Y(5)=1

Multiple outcomes simply receive the same numerical value.

------------------------------------------------------------------------

# 7. Events from Random Variables

Events are obtained as inverse images.

For example,

\[ {`\omega`{=tex}:Y(`\omega`{=tex})=0} = {2,4,6}. \]

Similarly,

\[ {`\omega`{=tex}:Y(`\omega`{=tex})=1} = {1,3,5}. \]

Thus,

Random Variable → Numerical Set → Event.

------------------------------------------------------------------------

# 8. Continuous Random Variables

Suppose we measure tomorrow's temperature.

The sample space is **not** the real numbers.

It is the set of all physically possible states of tomorrow's world.

The temperature random variable

\[ T:`\Omega`{=tex}`\rightarrow`{=tex}`\mathbb `{=tex}R \]

extracts one numerical quantity from each possible world.

When we write

\[ T`\sim `{=tex}N(`\mu`{=tex},`\sigma`{=tex}\^2), \]

we mean that the **distribution induced by T** on the real line is
Gaussian.

The underlying sample space remains the collection of possible worlds.

------------------------------------------------------------------------

# 9. Canonical Probability Space

Often, statistics ignores the underlying sample space and works directly
with

\[
(`\mathbb `{=tex}R,`\mathcal `{=tex}B,N(`\mu`{=tex},`\sigma`{=tex}\^2)),
\]

where

-   sample space = real numbers,
-   sigma algebra = Borel sets,
-   probability measure = Gaussian,
-   random variable = identity function.

------------------------------------------------------------------------

# 10. Summary

  -------------------------------------------------------------------------------------------------
  Object        Mathematical Form                                        Interpretation
  ------------- -------------------------------------------------------- --------------------------
  Sample Space  (`\Omega`{=tex})                                         All possible outcomes

  Sigma Algebra (`\mathcal `{=tex}F)                                     Collection of measurable
                                                                         events

  Probability   \(P\)                                                    Assigns probabilities to
  Measure                                                                events

  Random        (X:`\Omega`{=tex}`\rightarrow`{=tex}`\mathbb `{=tex}R)   Maps outcomes to numbers
  Variable                                                               
  -------------------------------------------------------------------------------------------------

The key distinction is:

-   **Probability measures assign probabilities to events.**
-   **Random variables assign numbers to outcomes.**
-   **Distributions are induced by combining a probability measure with
    a random variable.**
