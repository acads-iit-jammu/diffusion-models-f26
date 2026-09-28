"""Exact-score reverse SDE / probability-flow ODE example (standard library only).

Run: python3 materials/score-diffusion-example.py --steps 1600 --particles 5000
The clean law is 0.5 N(-2, 0.35**2) + 0.5 N(2, 0.35**2).
Forward SDE: dX = -X/2 dt + dW. Generation runs from T=8 to zero.
Use --csv /tmp/samples.csv to save the paired starting and final samples.
The common start does not imply matching SDE and ODE endpoints.
"""

import argparse
import csv
import math
import random
import statistics


def mixture_parameters(t):
    return 2 * math.exp(-t / 2), 0.35**2 * math.exp(-t) - math.expm1(-t)


def score(x, t):
    b, q = mixture_parameters(t)
    return (b * math.tanh(b * x / q) - x) / q


def sample(steps=400, particles=1200, seed=21, prior="exact"):
    if steps < 1 or particles < 2:
        raise ValueError("Use at least one step and two particles")
    rng = random.Random(seed)
    terminal_time = 8.0
    b, q = mixture_parameters(terminal_time)
    initial = [
        rng.choice((-b, b)) + math.sqrt(q) * rng.gauss(0, 1)
        if prior == "exact" else rng.gauss(0, 1)
        for _ in range(particles)
    ]
    ode, sde = initial.copy(), initial.copy()
    h = terminal_time / steps
    for k in range(steps):
        t = terminal_time - k * h  # coefficients at current forward time
        ode = [x + h * (x / 2 + score(x, t) / 2) for x in ode]
        sde = [x + h * (x / 2 + score(x, t)) + math.sqrt(h) * rng.gauss(0, 1)
               for x in sde]
    return initial, ode, sde


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", type=int, default=400)
    parser.add_argument("--particles", type=int, default=1200)
    parser.add_argument("--seed", type=int, default=21)
    parser.add_argument("--prior", choices=("exact", "gaussian"), default="exact")
    parser.add_argument("--csv", help="Optional output path for samples")
    args = parser.parse_args()
    if args.steps < 1 or args.particles < 2:
        parser.error("--steps must be positive and --particles must be at least 2")
    initial, ode, sde = sample(args.steps, args.particles, args.seed, args.prior)
    print("Target: mean 0; variance 4.1225; P(X > 0) = 0.5")
    for label, xs in (("ODE", ode), ("SDE", sde)):
        print(f"{label}: mean {statistics.mean(xs):.4f}; variance {statistics.pvariance(xs):.4f}; "
              f"positive fraction {sum(x > 0 for x in xs) / len(xs):.4f}")
    print("Differences reflect finite particles, finite steps, and (if selected) the Gaussian prior approximation.")
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(("initial_at_T", "probability_flow_ode", "reverse_sde"))
            writer.writerows(zip(initial, ode, sde))


if __name__ == "__main__":
    main()
