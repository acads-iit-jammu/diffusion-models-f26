Student-facing files (notes, scans, handouts) referenced from week pages. Solutions and question papers go in `private/`, never here.

## Score and Flow Lab

Open `score-flow-lab.html` directly, or use the copy under `_site/materials/`
after rendering the course. It uses the adjacent `score-flow-core.js` and
`score-flow-lab.js`, with no external dependencies. The four experiments cover
ODE fields and flows, score ascent versus Langevin sampling, reverse SDE versus
probability-flow ODE, and Tweedie's posterior-mean denoiser.

Companion notes: tutorials 22 (vector fields to score diffusion), 24 (sampling
with scores, with solved Gaussian flows), and 23 (Tweedie).
The notes share the detailed probability-flow draft's notation: reverse clock
`tau = T - t` and backward steps `h_k < 0`. The lab's positive step size is
`h = |h_k|`; fixed-target Langevin dynamics use an independent clock `u`.
Render with `quarto render`. Run numerical checks with
`node materials/score-flow-checks.cjs` from the project root.

The standard-library Python example runs with
`python3 materials/score-diffusion-example.py --steps 1600 --particles 5000`.
Use `--csv /tmp/score-samples.csv` to save the samples. Both examples distinguish
an exact terminal mixture from an approximate Gaussian initialization.
