# Probability-flow teaching code (Draft)

Companion to Lecture Notes 15–16. Data time is 0; terminal time is 1.

## Setup

Create a Python 3.12 environment and install `requirements.txt`. Open the
notebooks with that environment as the kernel in a Jupyter-compatible editor.
The notebooks are self-contained mini-tutorials with LaTeX derivations, explanations before the code, interpretations of results, exercises, and executed outputs. No GPU or
external data is needed for the scalar experiments.

Run notebooks 01–04 in order. Notebook 03 optionally writes `toy-noise.pt`;
Notebook 04 trains independently if it cannot find that checkpoint.

`verification.json` records the local CPU run and its quantitative checks.
`tested-versions.txt` records the versions used. Minor platform-dependent
numerical and timing differences are expected.

## Image example

`python image-model/ddpm_mnist.py smoke --checkpoint runs/smoke.pt`

This checks the complete model, loss gradient, schedule identities,
checkpoint round trip, and both samplers using synthetic input.

`python image-model/ddpm_mnist.py train --device cpu --updates 10000`

Training downloads MNIST if needed. Use `--device cuda` for a CUDA GPU.
The default writes `runs/mnist-ddpm.pt`; use a different path for independent
runs. This command starts fresh; it does not resume training automatically.

`python image-model/ddpm_mnist.py sample --method ddpm --output runs/ddpm.png`

`python image-model/ddpm_mnist.py sample --method ddim --ddim-steps 50 --output runs/ddim.png`

Raw tensors are saved alongside display images. Full MNIST training and
image-quality evaluation have not been run for the draft. A successful smoke
check does not establish image quality. See Lecture 16 for the full recipe.

## Browser reading copies

The course build runs `quarto render materials/probability-flow/notebooks`
before rendering the book. The nested Quarto configuration renders saved
notebook outputs without executing the training cells. Lecture 15 links to
both the rendered HTML and the downloadable notebook sources. After changing
code, rerun and save the notebook to update its outputs before rendering.
