"""Explicit Euler sampling backward in time for the draft's invertible Gaussian flow.
Requires NumPy and Matplotlib. Run from any directory; writes a tutorial SVG.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

rng = np.random.default_rng(20260930)
n, steps = 20000, 200
h = 1 / steps
rate = np.log(2.)
z = rng.standard_normal(n)
x = z.copy()
paths = np.empty((steps+1, 20))
paths[0] = x[:20]
for k in range(steps):
    x += h * rate * (x+2)
    paths[k+1] = x[:20]

# Euler's finite-step map is affine and differs from the exact inverse.
factor = (1+h*rate)**steps
assert np.allclose(x, -2+factor*(z+2), atol=1e-12)
exact = 2+2*z
fine_factor = (1+h*rate/2)**(2*steps)
assert abs(fine_factor-2) < abs(factor-2)
assert abs(x.mean()-2) < .08 and abs(x.var()-4) < .15

def pdf(y, mean=0, sd=1):
    return np.exp(-.5*((y-mean)/sd)**2) / (sd*np.sqrt(2*np.pi))

plt.rcParams.update({'font.size': 11, 'svg.fonttype': 'none',
                     'svg.hashsalt': 'draft-inverse-sampling',
                     'axes.spines.top': False, 'axes.spines.right': False})
fig, ax = plt.subplots(1, 3, figsize=(12.5, 4.1), layout='constrained')
grid = np.linspace(-6, 10, 1000)
ax[0].hist(z, bins=65, density=True, color='#0072B2', alpha=.4, label='Starting draws')
ax[0].plot(grid, pdf(grid), color='#0072B2', lw=2, label='Standard normal PDF')
ax[0].set(title='1. Draw at t = 1', xlabel='Position', ylabel='Density', xlim=(-4,4))
ax[0].legend(frameon=False, fontsize=9)
t = np.linspace(1, 0, steps+1)
ax[1].plot(t, paths, lw=1.1, alpha=.8)
ax[1].set(title='2. Follow the flow backward', xlabel='Time t (decreasing)', ylabel='Position x(t)', xlim=(1,0))
ax[1].grid(alpha=.18)
ax[2].hist(x, bins=65, density=True, color='#009E73', alpha=.4, label='Euler samples (reverse time)')
ax[2].plot(grid, pdf(grid,2,2), color='#D55E00', lw=2, label='Target PDF: N(2, 4)')
ax[2].set(title='3. Return samples at t = 0', xlabel='Position', ylabel='Density', xlim=(-6,10))
ax[2].legend(frameon=False, fontsize=9)
out = Path(__file__).resolve().parents[1] / 'tutorials' / 'figs' / 'draft-ode-inverse-sampling.svg'
fig.savefig(out, metadata={'Date':None})
plt.close(fig)
print(f'Generated mean={x.mean():.4f}, variance={x.var():.4f}; target mean=2, variance=4.')
print(f'Euler scale={factor:.6f}; exact scale=2; step refinement reduces error.')
